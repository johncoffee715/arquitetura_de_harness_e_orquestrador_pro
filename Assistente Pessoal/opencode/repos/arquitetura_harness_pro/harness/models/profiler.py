"""Estimativa de capacidades e recursos por heurística calibrada (T4.2).

Priors de família e penalidades de quantização vêm da SPEC F2/GMB-1.
Valores MEDIDOS têm precedência sobre estimativas: a tabela
_MEASURED_VRAM_GIB_32K é alimentada pelos runs isolados do GMB-1 @ctx 32768
(evidência: .planning/GMB1-relatorio-interim.md).
"""
from __future__ import annotations

import math
import re
from typing import Any, Dict, Optional

# prior por família (SPEC F2 §2.1) — capacidades em [0,1]
FAMILY_PRIORS: Dict[str, Dict[str, float]] = {
    "qwen": {"reasoning": 0.82, "coding": 0.85, "planning": 0.80, "tool_use": 0.86, "analysis": 0.84},
    "ornith": {"reasoning": 0.85, "coding": 0.78, "planning": 0.82, "tool_use": 0.84, "analysis": 0.80},
    "bonsai": {"reasoning": 0.88, "coding": 0.65, "planning": 0.60, "tool_use": 0.70, "analysis": 0.82},
    "llama": {"reasoning": 0.78, "coding": 0.74, "planning": 0.72, "tool_use": 0.76, "analysis": 0.76},
    "phi": {"reasoning": 0.75, "coding": 0.70, "planning": 0.65, "tool_use": 0.72, "analysis": 0.72},
}
_DEFAULT_PRIOR: Dict[str, float] = {
    "reasoning": 0.72,
    "coding": 0.70,
    "planning": 0.68,
    "tool_use": 0.70,
    "analysis": 0.70,
}

QUANT_PENALTY: Dict[str, float] = {
    "F16": 1.0, "Q8_0": 0.995, "Q6_K": 0.985, "Q5_K_M": 0.97, "Q5_K_S": 0.96,
    "Q4_K_M": 0.95, "Q4_K_S": 0.93, "Q3_K_M": 0.88, "Q3_K_S": 0.85,
    "Q2_K": 0.75, "IQ2_M": 0.70, "IQ2_XXS": 0.65,
}
# bits-por-peso médios p/ heurística de parâmetros quando não há size_label
_BPW: Dict[str, float] = {
    "F16": 16.0, "Q8_0": 8.5, "Q6_K": 6.6, "Q5_K_M": 5.7, "Q5_K_S": 5.55,
    "Q4_K_M": 4.85, "Q4_K_S": 4.6, "Q3_K_M": 4.0, "Q3_K_S": 3.7,
    "Q2_K": 3.3, "IQ2_M": 2.8, "IQ2_XXS": 2.6,
}
_QUANT_RE = re.compile(r"(IQ[23]_\w+|Q[2-8]_K_[SML]+|Q[4568]_0|BF16|F16)")

# overrides empíricos GMB-1 (smoke tríade 2026-08-23) — ORDEM IMPORTA:
# o fragmento mais específico primeiro ("ornith" também contém "-9b-q4")
_MEASURED_VRAM_GIB_32K: Dict[str, float] = {
    "ornith": 14.2,
    "iq2-xxs": 15.7,
    "-9b-q4": 14.9,
}
_SAFETY_FACTOR = 1.18  # buffers/compute pool observados nos runs reais


def detect_quant_tag(filename: str) -> str:
    """Extrai a tag de quantização do nome do arquivo; default conservador Q4_K_M."""
    match = _QUANT_RE.search(filename.upper())
    tag = match.group(1).upper() if match else ""
    return tag if tag in QUANT_PENALTY else "Q4_K_M"


def detect_family(name: str, arch: Optional[str], filename: Optional[str] = None) -> str:
    """Família por prioridade de evidência: nome do arquivo > general.name > arquitetura.

    O arquivo é o sinal mais forte no lab (convenção de nomenclatura); a
    arquitetura interna (ex.: 'qwen3' em finetune Ornith) nunca deve vencer.
    """
    for source in (filename or "", str(name or ""), str(arch or "")):
        low = source.lower()
        for fam in FAMILY_PRIORS:
            if fam in low:
                return fam
    return "desconhecida"


def params_billion(meta: Dict[str, Any], file_size_gb: float, quant_tag: str = "Q4_K_M") -> float:
    """Parâmetros em bilhões: usa general.size_label se houver; senão deriva
    do tamanho do arquivo dividido pelos bits/peso da quantização."""
    label = str(meta.get("general.size_label", "") or "")
    match = re.search(r"(\d+(?:\.\d+)?)\s*B", label, re.I)
    if match:
        return float(match.group(1))
    bpw = _BPW.get(quant_tag.upper(), 4.85)
    return round(file_size_gb * 8.0 / bpw, 2)


def param_scale(params_b: float) -> float:
    """Scaling logarítmico calibrado: 0.25B→~0.68 · 1B→~0.82 · 9B→~1.04 · ≥20B→cap 1.08."""
    if params_b <= 0:
        return 0.60
    return min(1.08, 0.68 + 0.07 * math.log2(max(params_b, 0.25) / 0.25))


def context_bonus(ctx_len: int) -> float:
    """Bônus para contexto nativo grande (>64K), conforme SPEC."""
    return 0.05 if ctx_len and ctx_len > 65536 else 0.0


def confidence(measured_runs: int) -> float:
    """SPEC F2 §2.1: confiança = measured/(measured+10); 0 sem medições."""
    if measured_runs <= 0:
        return 0.0
    return round(measured_runs / (measured_runs + 10), 3)


def _arch_int(meta: Dict[str, Any], suffix: str) -> Optional[int]:
    """Primeiro valor int cuja chave termina com o sufixo por-arquitetura."""
    for key, val in meta.items():
        if key.endswith(suffix) and isinstance(val, (int, float)):
            return int(val)
    return None


def estimate_vram_gib(meta: Dict[str, Any], model_id: str, ctx_len: int) -> float:
    """VRAM estimada em GiB.

    Em ctx 32768 (isolamento GMB-1) o override MEDIDO vence a fórmula.
    Fórmula: pesos×1.03 + KV(K q8 1B + V q4 0.5B) + overhead, ×fator segurança.
    """
    if int(ctx_len or 0) == 32768:
        norm = (model_id or "").lower().replace("_", "-")
        for frag, gib in _MEASURED_VRAM_GIB_32K.items():
            if frag in norm:
                return gib
    size_gib = float(meta.get("file_size_bytes", 0)) / 2**30
    weights = size_gib * 1.03
    layers = _arch_int(meta, ".block_count")
    kv_heads = _arch_int(meta, ".head_count_kv")
    klen = _arch_int(meta, ".key_length")
    if layers and kv_heads and klen:
        kv_gib = layers * (kv_heads * klen) * max(ctx_len, 1) * 1.5 / 2**30
    else:
        kv_gib = 1.0 * (max(ctx_len, 1) / 32768.0)  # heurística conservadora
    overhead = max(1.2, weights * 0.08)
    return round((weights + kv_gib + overhead) * _SAFETY_FACTOR, 2)


def estimate_capabilities(meta: Dict[str, Any], filename: str) -> Dict[str, float]:
    """Capacidades estimadas = prior(família) × penalidade(quant) × scaling(params) + bônus(ctx)."""
    fam = detect_family(
        str(meta.get("general.name") or ""),
        meta.get("general.architecture"),
        filename=filename,
    )
    prior = FAMILY_PRIORS.get(fam, _DEFAULT_PRIOR)
    quant = detect_quant_tag(filename)
    penalty = QUANT_PENALTY.get(quant, 0.90)
    gb = float(meta.get("file_size_bytes", 0)) / 2**30
    scale = param_scale(params_billion(meta, gb, quant))
    bonus = context_bonus(_arch_int(meta, ".context_length") or 0)
    caps = {k: round(min(0.99, v * penalty * scale + bonus), 3) for k, v in prior.items()}
    return caps
