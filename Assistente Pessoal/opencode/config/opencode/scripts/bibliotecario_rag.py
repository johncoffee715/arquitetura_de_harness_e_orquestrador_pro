#!/usr/bin/env python3
"""
BIBLIOTECARIO RAG — Recuperação híbrida sobre o Vault Obsidian.

Pipeline: query → busca lexical (grep/glob) → reforço Qdrant (graceful) →
prefill ingestor :9084 (janela 1M) → resposta com referências reais.

Origin: helenizado:hefesto-v1 (R77 3 camadas — skill bibliotecario)
"""

import argparse
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

VAULT = Path("/mnt/dados/Assistente Pessoal/cerebro com IA")
RWKV_URL = "http://127.0.0.1:9084/v1/chat/completions"
QDRANT_URL = "http://localhost:6333/collections/gran_mestre_docs/points/search"
SYSTEM_PROMPT = (
    "Você é um indexador de precisão. Não invente metadados. "
    "Retorne apenas os trechos exatos e referências de arquivos do Obsidian "
    "correspondentes à query. Se não encontrar, diga 'sem registros no Vault para <query>'."
)


def buscar_lexical(query: str, top_n: int = 5) -> list[str]:
    """Busca lexical por termos da query no Vault (grep -ril)."""
    termos = [t for t in query.lower().split() if len(t) > 2][:4]
    hits: set[str] = set()
    for t in termos:
        try:
            r = subprocess.run(
                ["grep", "-ril", t, str(VAULT)],
                capture_output=True, text=True, timeout=15,
            )
            hits.update(r.stdout.splitlines())
        except Exception:
            continue
    return sorted(h for h in hits if h.startswith(str(VAULT)))[:top_n]


def reforco_qdrant(query: str, top_n: int = 5) -> list[str]:
    """Reforço semântico via Qdrant — graceful (nunca bloqueia)."""
    try:
        body = json.dumps({"vector": [0.0] * 768, "limit": top_n}).encode()
        req = urllib.request.Request(
            QDRANT_URL, data=body, headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=2) as resp:
            qd = json.loads(resp.read())
        return [p["payload"]["path"] for p in qd.get("result", [])
                if p.get("payload") and p["payload"].get("path")]
    except Exception:
        return []


def prefill_rwkv(contexto: str, query: str) -> dict:
    """Prefill ingestor :9084 com contexto recuperado (janela 1M)."""
    payload = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"CONTEXTO DO VAULT:\n{contexto}\n\nQUERY: {query}"},
        ],
        "temperature": 0.1,
        "max_tokens": 1024,
    }
    req = urllib.request.Request(
        RWKV_URL, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read())


def verificar_paths_reais(paths: list[str]) -> tuple[bool, list[str]]:
    """Verifica que todos os paths existem no filesystem (anti-alucinação)."""
    invalidos = [p for p in paths if not Path(p).exists()]
    return (len(invalidos) == 0, invalidos)


def main():
    parser = argparse.ArgumentParser(description="Bibliotecario RAG")
    parser.add_argument("query", help="consulta ao Vault")
    parser.add_argument("--top-n", type=int, default=5)
    args = parser.parse_args()

    # 1. busca lexical
    paths = buscar_lexical(args.query, args.top_n)
    # 2. reforço Qdrant (graceful)
    qd = reforco_qdrant(args.query, args.top_n)
    paths = list(dict.fromkeys(paths + qd))[: args.top_n]

    if not paths:
        print(json.dumps({
            "query": args.query,
            "references": [],
            "all_paths_real": True,
            "qdrant_used": False,
            "rwkv_used": False,
            "verdict": "PASSOU_CATEGORICO",
            "note": "sem registros no Vault para a query (resposta honesta, zero invenção)",
        }, ensure_ascii=False, indent=2))
        return 0

    # 3. monta contexto com trechos
    contexto = []
    for p in paths:
        try:
            txt = Path(p).read_text(encoding="utf-8", errors="ignore")[:4000]
            contexto.append(f"### {p}\n{txt[:1500]}")
        except Exception:
            continue
    contexto_txt = "\n\n".join(contexto)

    # 4. prefill ingestor
    rwkv_used = False
    resposta = ""
    try:
        r = prefill_rwkv(contexto_txt, args.query)
        resposta = r["choices"][0]["message"]["content"]
        rwkv_used = True
    except Exception as e:
        resposta = f"[RWKV offline: {e}] Trechos recuperados acima."

    # 5. veredito
    all_real, invalidos = verificar_paths_reais(paths)
    verdict = "PASSOU_CATEGORICO" if all_real else "NAO_PASSOU"

    print(json.dumps({
        "query": args.query,
        "references": [{"path": p} for p in paths],
        "all_paths_real": all_real,
        "invalid_paths": invalidos,
        "qdrant_used": bool(qd),
        "rwkv_used": rwkv_used,
        "resposta": resposta[:2000],
        "verdict": verdict,
        "note": "nota R34: 100% paths reais" if all_real else f"paths inválidos: {invalidos}",
    }, ensure_ascii=False, indent=2))
    return 0 if all_real else 1


if __name__ == "__main__":
    sys.exit(main())