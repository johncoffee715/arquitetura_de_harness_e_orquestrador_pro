#!/usr/bin/env python3
"""llama_budget.py — Orçamento dinâmico de VRAM para os 4 llama-servers (MI50 16GB).

Probe real da VRAM via nvidia-smi ou rocm-smi (fallback 16.0GB) e calcula
ctx/slots por modelo de modo que:

    SOMA(dos 4 modelos + KV) + ~2GB headroom de sistema <= VRAM disponível

Uso pelo start-all-models.sh:

    eval "$(python3 "$(dirname "$0")/llama_budget.py" --export)"

Consistência com a spec: o harness pede heavy_execution Bonsai ctx=16384 slots
4-5, mas o script antigo usava `-c 4096 -np 2`. Em 16GB reais, o Bonsai 27B-1bit
(Q4, ~3.6GB de pesos + KV q8 ≈ 0.0625GB por slot por 4096 tokens) entrega:

    ctx 8192 slots 2 (~5.5GB)   ← recomendado em 16GB
    ctx 4096 slots 4 (~5.2GB)   ← alternativa (mais concorrência, ctx curto)

ctx 16384 slots 4-5 exige ~24GB+ de VRAM (ver _bonsai_candidates).
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from typing import Optional

VRAM_FALLBACK_GB = 16.0  # MI50 16GB HBM2
HEADROOM_GB = 2.0  # sistema + compute buffers não modelados
# KV q8: 2 bytes/param/token → 27B*2B = 54MB por slot por 4096 tokens
KV_GB_PER_4096_PER_SLOT = 0.0625
BONSAI_WEIGHTS_GB = 3.6  # Bonsai-27B-1bit Q4_K_M
_BONSAI_OVERHEAD_GB = 1.65  # compute buffer Vulkan, inferido do anchor 8192/2

# Âncoras da spec (estimativas observadas na MI50 16GB)
_BONSAI_ANCHORS = {
    (4096, 4): 5.2,
    (8192, 2): 5.5,
}

# Modelos fixos (pesos + KV q8; invariantes dentro do orçamento)
_FIXED_MODELS = {
    "gran_mestre": {  # ornith-1.0-9B Q4_K_M
        "ctx": 4096,
        "slots": 2,
        "est_vram_gb": 5.5,
        "kv_q8": True,
    },
    "filter_medium": {  # nanbeige-3b Q4_K_M
        "ctx": 4096,
        "slots": 2,
        "est_vram_gb": 2.3,
        "kv_q8": True,
    },
    "filter_fast": {  # lfm-1.6b Q4_K_M
        "ctx": 2048,
        "slots": 2,
        "est_vram_gb": 0.7,
        "kv_q8": False,
    },
}

# Ordem de exportação (modelo → prefixo da variável)
_EXPORT_ORDER = (
    ("filter_fast", "LFM"),
    ("filter_medium", "NANBEIGE"),
    ("gran_mestre", "ORNITH"),
    ("heavy", "BONSAI"),
)


def _probe_vram_gb() -> Optional[float]:
    """Probe VRAM total via nvidia-smi (MiB) ou rocm-smi (bytes/"HBM")."""
    if shutil.which("nvidia-smi"):
        try:
            out = subprocess.run(
                ["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader"],
                capture_output=True, text=True, timeout=5,
            ).stdout
            m = re.search(r"([\d.]+)\s*MiB", out)
            if m:
                return float(m.group(1)) / 1024.0
        except (OSError, subprocess.TimeoutExpired):
            pass
    if shutil.which("rocm-smi"):
        try:
            out = subprocess.run(
                ["rocm-smi", "--showmeminfo", "vram"],
                capture_output=True, text=True, timeout=5,
            ).stdout
            m = re.search(r"VRAM Total Memory[^\d]*(\d+)", out)
            if m:
                return int(m.group(1)) / (1024.0 ** 3)
        except (OSError, subprocess.TimeoutExpired):
            pass
    return None


def _bonsai_candidates() -> list:
    """Candidatos (ctx, slots) para o Bonsai 27B-1bit, do menor ao maior uso."""
    configs = [
        (4096, 4),
        (8192, 2),
        (8192, 4),
        (16384, 2),
        (16384, 4),
        (32768, 2),
        (32768, 4),
    ]
    out = []
    for ctx, slots in configs:
        if (ctx, slots) in _BONSAI_ANCHORS:
            est = _BONSAI_ANCHORS[(ctx, slots)]
        else:
            kv = (ctx / 4096.0) * KV_GB_PER_4096_PER_SLOT * slots
            est = BONSAI_WEIGHTS_GB + kv + _BONSAI_OVERHEAD_GB
        out.append(
            {"ctx": ctx, "slots": slots,
             "est_vram_gb": round(est, 2), "kv_q8": True}
        )
    return out


def compute_plan(vram_gb: Optional[float] = None) -> dict:
    """Calcula o plano de ctx/slots dos 4 modelos dado o VRAM disponível.

    vram_gb explícito vence; senão probe nvidia-smi/rocm-smi; fallback 16.0.
    O valor efetivo é arredondado para o inteiro mais próximo (VRAM de placa
    é nominal: "16GB" real ≈ 15.98 GiB).
    """
    if vram_gb is None:
        probed = _probe_vram_gb()
        vram_gb = probed if probed is not None else VRAM_FALLBACK_GB
    usable = int(vram_gb + 0.5)

    fixed_gb = sum(m["est_vram_gb"] for m in _FIXED_MODELS.values())
    budget_bonsai = usable - fixed_gb - HEADROOM_GB

    candidates = _bonsai_candidates()
    fitting = [c for c in candidates if c["est_vram_gb"] <= budget_bonsai + 1e-6]
    bonsai = max(fitting, key=lambda c: (c["ctx"], c["slots"])) if fitting \
        else min(candidates, key=lambda c: c["est_vram_gb"])

    models = {name: dict(cfg) for name, cfg in _FIXED_MODELS.items()}
    models["heavy"] = bonsai

    total = round(fixed_gb + bonsai["est_vram_gb"], 2)
    guard_ok = (total + HEADROOM_GB) <= usable + 1e-6

    plan = dict(models)
    plan.update({
        "vram_gb": usable,
        "vram_probed_gb": round(vram_gb, 2),
        "headroom_gb": HEADROOM_GB,
        "total_estimated_vram_gb": total,
        "guard_ok": guard_ok,
    })
    return plan


def render_export(plan: Optional[dict] = None) -> str:
    """Bloco `export A=1; export B=2; ...` que start-all-models.sh pode source."""
    plan = plan if plan is not None else compute_plan()
    parts = []
    for key, prefix in _EXPORT_ORDER:
        m = plan[key]
        parts.append("export %s_CTX=%s" % (prefix, m["ctx"]))
        parts.append("export %s_SLOTS=%s" % (prefix, m["slots"]))
    return "; ".join(parts) + "\n"


def _print_plan(plan: dict) -> None:
    rows = (
        ("gran_mestre", "ornith-9b (Q4_K_M)"),
        ("heavy", "bonsai-27b-1bit (Q4_K_M)"),
        ("filter_medium", "nanbeige-3b (Q4_K_M)"),
        ("filter_fast", "lfm-1.6b (Q4_K_M)"),
    )
    for key, label in rows:
        m = plan[key]
        kv = "q8" if m.get("kv_q8") else "-"
        print("  %-28s ctx=%-6s slots=%-3s kv=%-3s ~%sGB" % (
            label, m["ctx"], m["slots"], kv, m["est_vram_gb"]))
    print("  %-28s %sGB" % ("TOTAL (4 modelos + KV)", plan["total_estimated_vram_gb"]))
    print("  %-28s %sGB" % ("Headroom sistema", plan["headroom_gb"]))
    print("  %-28s %s / %sGB" % (
        "VRAM (probe/efetiva)", plan["vram_probed_gb"], plan["vram_gb"]))
    print("  Guarda (total+headroom<=vram): %s" % (
        "OK" if plan["guard_ok"] else "FALHOU"))


def selfcheck() -> int:
    """Imprime o plano para a VRAM assumida de 16.0GB."""
    plan = compute_plan(VRAM_FALLBACK_GB)
    print("llama_budget.py selfcheck — VRAM assumida: 16.0GB")
    print("-" * 60)
    _print_plan(plan)
    print("-" * 60)
    print("Bloco export:")
    print(render_export(plan), end="")
    return 0


def main(argv: Optional[list] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if "--export" in argv:
        print(render_export(), end="")
        return 0
    if "--selfcheck" in argv:
        return selfcheck()
    plan = compute_plan()
    if "--json" in argv:
        print(json.dumps(plan, indent=2, ensure_ascii=False))
        return 0
    print("llama_budget.py — VRAM probe: %sGB (efetiva %sGB)" % (
        plan["vram_probed_gb"], plan["vram_gb"]))
    print("-" * 60)
    _print_plan(plan)
    return 0


if __name__ == "__main__":
    sys.exit(main())
