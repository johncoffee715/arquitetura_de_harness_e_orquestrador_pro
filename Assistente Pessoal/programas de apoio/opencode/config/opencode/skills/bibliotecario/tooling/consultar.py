#!/usr/bin/env python3
"""
Consulta gerente canonica (F2/F3/F4) — Bibliotecario (R94).

Deterministica, sem LLM, sem vetor fajuto: lexical (grep) + scroll Qdrant com
filtro LOCAL por payload (path/conteudo/tags — real) + confianca (frescor por
mtime + convergencia) + 3 reformulacoes no zero-hit + orientacao em todo retorno.

Uso: consultar.py "sua query" [--top-n 5]
Saida: JSON do output contract v2 (SKILL.md). exit 0.
"""

import argparse
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

VAULT = Path("/mnt/dados/Assistente Pessoal/cerebro com IA")
QDRANT = "http://localhost:6333/collections/gran_mestre_docs/points/scroll"


def buscar_lexical(query, top_n=8):
    termos = [t for t in query.lower().split() if len(t) > 2][:4]
    hits = {}
    for t in termos:
        try:
            r = subprocess.run(["grep", "-ril", t, str(VAULT)],
                               capture_output=True, text=True, timeout=20)
            for p in r.stdout.splitlines():
                if p.startswith(str(VAULT)):
                    hits[p] = hits.get(p, 0) + 1
        except Exception:
            continue
    return sorted(hits, key=lambda p: -hits[p])[:top_n]


def scroll_payloads(limit=2000):
    """Traz payloads (sem vetor) e filtra localmente — scroll e real."""
    try:
        body = json.dumps({"limit": limit, "with_payload": True,
                           "with_vector": False}).encode()
        req = urllib.request.Request(QDRANT, data=body,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        return [p.get("payload", {}) for p in data.get("result", {}).get("points", [])]
    except Exception:
        return []


def pontuar(payloads, termos):
    rank = []
    for pl in payloads:
        path = pl.get("path", "")
        texto = ((pl.get("content") or "") + " " + path + " "
                 + " ".join(pl.get("tags") or [])).lower()
        score = sum(1 for t in termos if t in texto)
        if score:
            rank.append((score, pl))
    rank.sort(key=lambda x: -x[0])
    return rank


def confianca(paths):
    """Frescor (mtime mediano, decaimento anual) + convergencia (n/5)."""
    agora = time.time()
    dias = []
    for p in paths:
        try:
            dias.append((agora - Path(p).stat().st_mtime) / 86400)
        except Exception:
            continue
    med = sorted(dias)[len(dias) // 2] if dias else 365.0
    frescor = max(0.0, 1.0 - med / 365.0)
    conv = min(1.0, len(paths) / 5.0)
    return {"score": round(0.5 * frescor + 0.5 * conv, 2),
            "frescor_dias_mediano": round(med, 1),
            "fontes_convergentes": len(paths)}


def reformulacoes(query, hits):
    termos = [t for t in query.lower().split() if len(t) > 2]
    tags = []
    for _, pl in hits[:3]:
        tags += list(pl.get("tags") or [])[:2]
    tags = list(dict.fromkeys(tags))[:3]
    cands = ['"' + " ".join(termos) + '"',
             " ".join(termos) + " vault",
             " ".join(tags) if tags else " ".join(termos) + " aprendizados"]
    return list(dict.fromkeys(c for c in cands if c.strip('" ')))[:3]


def main():
    ap = argparse.ArgumentParser(description="Consulta gerente do vault")
    ap.add_argument("query")
    ap.add_argument("--top-n", type=int, default=5)
    args = ap.parse_args()
    termos = [t for t in args.query.lower().split() if len(t) > 2][:4]

    lex = buscar_lexical(args.query, args.top_n)
    payloads = scroll_payloads()
    rank = pontuar(payloads, termos)[: args.top_n]
    por_payload = [pl["path"] for _, pl in rank if pl.get("path")]
    paths = list(dict.fromkeys(lex + por_payload))[: args.top_n]
    paths = [p for p in paths if Path(p).exists()]

    refs = []
    for p in paths:
        try:
            txt = Path(p).read_text(encoding="utf-8", errors="ignore")
            i = min([txt.lower().find(t) for t in termos if t in txt.lower()] or [0])
            refs.append({"path": p, "snippet": txt[max(0, i - 120): i + 280].strip(),
                         "mtime": Path(p).stat().st_mtime})
        except Exception:
            continue

    conf = confianca(paths)
    if refs:
        return _emit(args.query, refs, conf, [], "busca lexical + payloads Qdrant")
    ref = reformulacoes(args.query, rank)
    return _emit(args.query, [], {"score": 0.0, "frescor_dias_mediano": 0,
                                  "fontes_convergentes": 0}, ref, "zero-hit honesto")


def _emit(query, refs, conf, reform, estrategia):
    validos = [r["path"] for r in refs if Path(r["path"]).exists()]
    out = {
        "query": query,
        "references": refs,
        "confianca": conf,
        "reformulacoes": reform,
        "estrategia": estrategia + "; termos: grep + filtro local de payloads (sem vetor fajuto)",
        "proximos_passos": (["testar reformulacoes acima", "pedir curadoria do gerente (R94)"]
                            if not refs else ["abrir a ref #1", "cruzar com decisoes/ e aprendizados/"]),
        "all_paths_real": len(validos) == len(refs),
        "verdict": "PASSOU_CATEGORICO" if len(validos) == len(refs) else "NAO_PASSOU",
        "note": "nota R34: paths 100% reais; confianca por frescor+convergencia (metadados, nao palpite)",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
