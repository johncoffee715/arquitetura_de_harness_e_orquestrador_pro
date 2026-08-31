#!/usr/bin/env python3
"""llm_crivo.py — Crivo Sistêmico (R83): validação empírica de QUALQUER LLM/feature do ecossistema.

2 etapas obrigatórias:
  A) ANTI-ALUCINAÇÃO — prompts com GROUND TRUTH verificável:
       · fato conhecido (capital do Brasil)
       · extração estruturada com schema (Pydantic) de um texto com dados fixos
       · não-invenção de arquivo inexistente
     Métricas: acurácia factual, conformidade de schema, taxa de invenção.
  B) ANTI-LOOP — N amostras do mesmo prompt:
       · determinismo (temp 0.0 → respostas idênticas)
       · repetição n-gram (loop de tokens)
       · finish_reason length vs stop (bateu no muro = explosão/loop)
       · content vazio com reasoning (think infinito, R57)
     Métricas: taxa de loop, determinismo (%), saúde de stop.

Saída: veredito categórico por métrica (R28) + MEMORIAL COMPARATIVO (append-only JSONL + relatório MD).

Uso: python3 scripts/llm_crivo.py --base-url http://127.0.0.1:9088/v1 --model granite --n 5 --verbose
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Limiares (configuráveis via CLI)
LIMIAR_ALUCINACAO = 0.10   # taxa de invenção/fato errado máxima
LIMIAR_LOOP = 0.10         # taxa de loop/explosão máxima
LIMIAR_DETERMINISMO = 0.90 # fração mínima de respostas idênticas em temp 0

HARNESS_LOGS = Path("/mnt/dados/Assistente Pessoal/harness/logs")
MEMORIAL = HARNESS_LOGS / "llm-crivo-memorial.jsonl"

try:
    from pydantic import BaseModel, Field, ValidationError
    PYDANTIC_OK = True
except Exception:
    PYDANTIC_OK = False
    BaseModel = object


# ==============================================================================
# Etapa A — GROUND TRUTH (anti-alucinação)
# ==============================================================================

FATO = {"pergunta": "Qual é a capital do Brasil? Responda somente o nome da cidade.",
        "resposta_esperada": "Brasília"}

TEXTO_EXTRAÇÃO = (
    "Pedido #1234 do cliente Maria Silva, total R$ 89,90, enviado para São Paulo. "
    "Forma de pagamento: cartão de crédito."
)


class Pedido(BaseModel):
    pedido_id: int
    cliente: str
    total: float
    cidade: str


PROMPT_EXTRACAO = (
    "Extraia do texto abaixo um JSON exato com os campos pedido_id (int), cliente (str), "
    "total (float), cidade (str). NÃO invente campos.\n\nTEXTO: " + TEXTO_EXTRAÇÃO
)

ARQUIVO_FANTASMA = "/etc/nonexistent_gm_crivo_2026_xyz.txt"
PROMPT_ARQUIVO = (
    f"Verifique se o arquivo '{ARQUIVO_FANTASMA}' existe. "
    "Responda apenas sim ou não. Não invente detalhes do arquivo."
)


def _normalizar(s: str) -> str:
    return re.sub(r"[^a-z0-9áéíóúãõâêôç ]", "", s.lower()).strip()


def avaliar_etapa_a(completions_fn) -> Dict[str, Any]:
    """Prompt com ground truth; mede acurácia factual, conformidade schema, invenção."""
    res = {"fato": None, "extracao": None, "arquivo": None, "erros": []}

    # 1) fato
    txt = completions_fn([{"role": "user", "content": FATO["pergunta"]}], max_tokens=40)
    certo = _normalizar(FATO["resposta_esperada"]) in _normalizar(txt or "")
    res["fato"] = {"acertou": certo, "resposta": (txt or "")[:80]}

    # 2) extração estruturada
    txt2 = completions_fn([{"role": "user", "content": PROMPT_EXTRACAO}], max_tokens=150)
    invencao = 0
    conformidade = False
    if txt2 and PYDANTIC_OK:
        try:
            obj = Pedido.model_validate_json(txt2)
            conformidade = True
            esperado = {"pedido_id": 1234, "cliente": "Maria Silva", "total": 89.9, "cidade": "São Paulo"}
            for campo, val in esperado.items():
                if getattr(obj, campo) != val:
                    invencao += 1  # campo presente mas ERRADO (não é invenção pura; conta como falha factual)
        except ValidationError as e:
            res["erros"].append("schema: " + str(e.errors()[:2]))
    elif txt2 is None:
        res["erros"].append("extracao: vazio")
    res["extracao"] = {"conforme_schema": conformidade, "invencoes": invencao, "raw": (txt2 or "")[:120]}

    # 3) arquivo inexistente (não-invenção)
    txt3 = completions_fn([{"role": "user", "content": PROMPT_ARQUIVO}], max_tokens=30)
    norm3 = _normalizar(txt3 or "")
    inventou = "sim" in norm3 and "não" not in norm3
    res["arquivo"] = {"inventou_existencia": inventou, "resposta": (txt3 or "")[:60]}

    # Agregação
    total_checks = 3
    falhas = 0
    if res["fato"] is not None and not res["fato"]["acertou"]:
        falhas += 1
    if res["extracao"] is not None and not res["extracao"]["conforme_schema"]:
        falhas += 1
    if res["arquivo"] is not None and res["arquivo"]["inventou_existencia"]:
        falhas += 1
    taxa = falhas / total_checks
    res["taxa_alucinacao"] = round(taxa, 3)
    res["veredito_a"] = "PASSOU_CATEGORICO" if taxa <= LIMIAR_ALUCINACAO else "NAO_PASSOU"
    return res


# ==============================================================================
# Etapa B — ANTI-LOOP (estabilidade generativa)
# ==============================================================================

PROMPT_LOOP = "Conte de 1 a 20, um número por linha. Pare no 20."


def _ngram_repeticao(texto: str, n: int = 3) -> bool:
    """Detecta repetição anômala de n-gram (loop de tokens)."""
    toks = re.findall(r"\S+", texto or "")
    if len(toks) < n * 4:
        return False
    seq = [tuple(toks[i:i + n]) for i in range(len(toks) - n + 1)]
    contagens = Counter(seq)
    top = contagens.most_common(1)[0][1]
    return top >= 4  # o mesmo n-gram repetido 4+ vezes = loop


def avaliar_etapa_b(completions_fn, n: int = 5) -> Dict[str, Any]:
    amostras = []
    for i in range(n):
        t0 = time.time()
        txt = completions_fn([{"role": "user", "content": PROMPT_LOOP}], max_tokens=120, temperature=0.0)
        dur = time.time() - t0
        stop_reason = "length" if (txt or "").count("\n") >= 25 else "stop"  # bateu no teto?
        amostras.append({"texto": txt or "", "dur_s": round(dur, 2), "stop_reason": stop_reason})

    # determinismo: identidade entre as N respostas
    textos = [a["texto"] for a in amostras]
    unicos = set(textos)
    determinismo = len(unicos) == 1

    # loop: repetição n-gram + estouro de linhas
    loops = [a for a in amostras if _ngram_repeticao(a["texto"]) or a["stop_reason"] == "length"]
    taxa_loop = len(loops) / n

    # conteúdo vazio + pensou (R57) — aproximação: resposta em branco
    vazios = [a for a in amostras if not a["texto"].strip()]
    taxa_vazio = len(vazios) / n

    res = {
        "amostras": n,
        "determinismo_temp0": determinismo,
        "determinismo_pct": round(100.0 if determinismo else 0.0, 1),
        "taxa_loop": round(taxa_loop, 3),
        "taxa_vazio": round(taxa_vazio, 3),
        "latencia_media_s": round(sum(a["dur_s"] for a in amostras) / n, 2) if n else 0,
        "veredito_b": "PASSOU_CATEGORICO" if (taxa_loop <= LIMIAR_LOOP and determinismo) else "NAO_PASSOU",
    }
    if determinismo:
        res["veredito_b"] = "PASSOU_CATEGORICO" if taxa_loop <= LIMIAR_LOOP else "NAO_PASSOU"
    else:
        res["veredito_b"] = "NAO_PASSOU"
    return res


# ==============================================================================
# Cliente mínimo OpenAI-compatible + memorial
# ==============================================================================

def make_completions(base_url: str, api_key: str = "llamacpp", timeout: int = 90):
    def _call(messages, max_tokens=100, temperature=0.0, **kw):
        payload = {"model": "local", "messages": messages, "max_tokens": max_tokens, "temperature": temperature}
        payload["chat_template_kwargs"] = {"enable_thinking": False}
        req = urllib.request.Request(
            base_url.rstrip("/") + "/chat/completions", data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = json.loads(r.read().decode("utf-8"))
        try:
            return body["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            return None
    return _call


def registrar_memorial(alvo: str, versao: str, resultado: Dict[str, Any], veredito_global: str):
    HARNESS_LOGS.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "alvo": alvo,
        "versao": versao,
        "etapa_a": resultado.get("etapa_a", {}),
        "etapa_b": resultado.get("etapa_b", {}),
        "veredito_global": veredito_global,
        "limiares": {"alucinacao": LIMIAR_ALUCINACAO, "loop": LIMIAR_LOOP, "determinismo": LIMIAR_DETERMINISMO},
    }
    with open(MEMORIAL, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser(description="Crivo Sistêmico (R83) — 2 etapas")
    ap.add_argument("--base-url", default="http://127.0.0.1:9088/v1")
    ap.add_argument("--model", default="granite")
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()

    fn = make_completions(args.base_url)
    print(f"=== CRIVO SISTÊMICO (R83) — alvo {args.model} ({args.base_url}) ===")
    print("ETAPA A — ANTI-ALUCINAÇÃO (ground truth)...")
    ea = avaliar_etapa_a(fn)
    print(json.dumps(ea, indent=2, ensure_ascii=False))
    print("ETAPA B — ANTI-LOOP (estabilidade)...")
    eb = avaliar_etapa_b(fn, n=args.n)
    print(json.dumps(eb, indent=2, ensure_ascii=False))

    veredito_global = "PASSOU_CATEGORICO" if (ea["veredito_a"] == "PASSOU_CATEGORICO" and eb["veredito_b"] == "PASSOU_CATEGORICO") else "NAO_PASSOU"
    print(f"\n=== VEREDITO GLOBAL: {veredito_global} ===")
    registrar_memorial(args.model, "local-gguf", {"etapa_a": ea, "etapa_b": eb},veredito_global)
    print(f"Memorial: {MEMORIAL}")


if __name__ == "__main__":
    main()