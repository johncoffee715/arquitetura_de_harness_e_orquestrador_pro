#!/usr/bin/env python3
"""
Triagem semântica do secretário — classifica intents por cosseno (R96 real, zero-LLM).

Uso:
    triagem.py "<texto>" [--threshold 0.55] [--no-cache]

Motor: Qwen3-Embedding-0.6B (:9094 CPU canônico — GPU :9097 descontinuado 2026-09-18) via cliente
canônico do bibliotecário (reuso R8 — NÃO duplicado aqui).
Fallback offline: matching lexical por palavras-chave dos protótipos, saída com
"modo": "lexical_placebo" (flag honesta; registro vetorial bloqueia neste modo).

Saída: JSON {intent, confidence, rota, acao_critica, scores, modo} — exit 0.
Erro real (protótipos ilegíveis etc.): exit 1 com {"erro": ...}.
"""

import argparse
import hashlib
import json
import logging
import math
import os
import re
import sys

logging.basicConfig(level=logging.WARNING,
                    format="%(levelname)s triagem: %(message)s")

BASE = os.path.dirname(os.path.abspath(__file__))
PROTOS = os.path.join(BASE, "prototipos_intent.json")
CACHE = os.path.join(BASE, "data", "protos_cache.json")

sys.path.insert(0, "/home/johncoffee/.config/opencode/skills/bibliotecario/tooling")
try:
    from embeddings import embed  # noqa: E402
except Exception as e:  # pragma: no cover
    embed = None
    _IMPORT_ERRO = str(e)
else:
    _IMPORT_ERRO = ""


def _norm(v):
    n = math.sqrt(sum(x * x for x in v))
    return [x / n for x in v] if n else v


def _cosseno(a, b):
    return sum(x * y for x, y in zip(a, b))


def _media(vecs):
    n = len(vecs)
    dim = len(vecs[0])
    return [sum(v[i] for v in vecs) / n for i in range(dim)]


def _sha1(path):
    with open(path, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()


def _centroides(protos, use_cache=True):
    """Retorna {intent: vetor-médio normalizado}. Cache em data/protos_cache.json."""
    digest = _sha1(PROTOS)
    if use_cache and os.path.exists(CACHE):
        try:
            with open(CACHE, encoding="utf-8") as f:
                blob = json.load(f)
            if blob.get("protos_sha1") == digest:
                return {k: v for k, v in blob["centroides"].items()}, "cache"
        except Exception as e:
            logging.warning("cache de centroides inválido/ausente — recomputando (%s)", e)
    # embedding real dos exemplos (lote -> GPU via prefer=auto)
    todos, donos = [], []
    for intent, spec in protos["intents"].items():
        for ex in spec["exemplos"]:
            todos.append(ex)
            donos.append(intent)
    vecs = embed(todos, timeout=30, prefer="auto")
    if vecs is None:
        return None, "offline"
    por_intent = {}
    for dono, v in zip(donos, vecs):
        por_intent.setdefault(dono, []).append(v)
    cents = {k: _norm(_media(vs)) for k, vs in por_intent.items()}
    try:
        with open(CACHE, "w", encoding="utf-8") as f:
            json.dump({"protos_sha1": digest, "centroides": cents}, f)
    except Exception as e:
        logging.warning("cache de centroides: escrita ignorada (%s)", e)
    return cents, "semantic"


def _tokens(s):
    return set(re.findall(r"[a-zà-ú0-9]+", s.lower()))


def _lexical(texto, protos):
    """Fallback honesto: overlap de palavras contra os exemplos. Retorna (intent, scores)."""
    tt = _tokens(texto)
    scores = {}
    for intent, spec in protos["intents"].items():
        best = 0.0
        for ex in spec["exemplos"]:
            te = _tokens(ex)
            if not tt or not te:
                continue
            overlap = len(tt & te) / len(tt)
            if overlap > best:
                best = overlap
        scores[intent] = round(best, 4)
    intent = max(scores, key=scores.get)
    return intent, scores


def triar(texto, threshold=0.55, use_cache=True):
    with open(PROTOS, encoding="utf-8") as f:
        protos = json.load(f)
    margem = protos.get("margem_desempate", 0.05)

    if embed is None:
        intent, scores = _lexical(texto, protos)
        spec = protos["intents"][intent]
        return {
            "intent": intent, "confidence": scores[intent],
            "rota": spec["rota"], "acao_critica": spec["acao_critica"],
            "scores": scores, "modo": "lexical_placebo",
        }, 0

    cents, _ = _centroides(protos, use_cache=use_cache)
    if cents is None:  # motores fora -> fallback lexical flagado
        intent, scores = _lexical(texto, protos)
        spec = protos["intents"][intent]
        return {
            "intent": intent, "confidence": scores[intent],
            "rota": spec["rota"], "acao_critica": spec["acao_critica"],
            "scores": scores, "modo": "lexical_placebo",
        }, 0

    v = embed(texto, timeout=15, prefer="auto")
    if v is None:
        intent, scores = _lexical(texto, protos)
        spec = protos["intents"][intent]
        return {
            "intent": intent, "confidence": scores[intent],
            "rota": spec["rota"], "acao_critica": spec["acao_critica"],
            "scores": scores, "modo": "lexical_placebo",
        }, 0
    v = _norm(v)
    scores = {k: round(_cosseno(v, c), 4) for k, c in cents.items()}
    ranking = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    top1, s1 = ranking[0]
    s2 = ranking[1][1] if len(ranking) > 1 else 0.0
    if s1 < threshold:
        return {
            "intent": "fora_escopo", "confidence": s1,
            "rota": protos["intents"]["fora_escopo"]["rota"],
            "acao_critica": False, "scores": scores, "modo": "semantic",
        }, 0
    if (s1 - s2) < margem:
        return {
            "intent": "ambiguo", "confidence": round(s1, 4),
            "rota": "escalar_orquestrador", "acao_critica": False,
            "scores": scores, "modo": "semantic",
            "candidatos": [ranking[0][0], ranking[1][0]],
        }, 0
    spec = protos["intents"][top1]
    return {
        "intent": top1, "confidence": s1,
        "rota": spec["rota"], "acao_critica": spec["acao_critica"],
        "scores": scores, "modo": "semantic",
    }, 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Triagem semântica do secretário")
    ap.add_argument("texto", help="pedido em linguagem natural")
    ap.add_argument("--threshold", type=float, default=0.55)
    ap.add_argument("--no-cache", action="store_true")
    args = ap.parse_args(argv)
    try:
        out, code = triar(args.texto, threshold=args.threshold,
                          use_cache=not args.no_cache)
    except Exception as e:
        print(json.dumps({"erro": str(e), "exit_status": "failed"},
                         ensure_ascii=False), flush=True)
        return 1
    print(json.dumps(out, ensure_ascii=False), flush=True)
    return code


if __name__ == "__main__":
    sys.exit(main())
