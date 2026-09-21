#!/usr/bin/env python3
"""
Backfill total do vault no Qdrant (F6) — Bibliotecario gerente (R94).

Payloads 100% REAIS (path, conteudo, mtime, tags). Vetor: PLACEBO flagado
(`vetor_placebo: true`) ate o desbloqueio R96 (Qwen3-Embedding-0.6B) — NUNCA
mascarado, NUNCA usado p/ ranking por similaridade (consultar.py usa scroll
por payload, que e real). ids estaveis via md5 (corrige o hash() salgado do
watcher legado, que duplicava a cada restart).

Correcao 2026-09-10 (R95/R96): NENHUM dos modelos em "modelos LLM/" e embedder
dedicado — Llama-3.2-1B em :9094 e provisório (instruct em modo --embedding,
2k ctx, 2048-d real mas qualidade de retrieval NAO avaliada) e fica em
colecao separada 2048-d; a colecao canonica 768-d segue placebo honesto ate
Qwen3-Embedding-0.6B. Esta ferramenta serve ambas (dim/collection parametrizáveis).

Uso: backfill.py [--limit N] [--vault PATH]
"""

import argparse
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from catalogar import extrair_tags  # noqa: E402

VAULT_PADRAO = Path("/mnt/dados/Assistente Pessoal/cerebro com IA")
COLLECTION = "gran_mestre_docs"
QDRANT = "http://localhost:6333"
DIM = 768
EXCLUIR = {".obsidian", ".trash", "quarentena", ".git", "node_modules"}


def id_estavel(path):
    return int(hashlib.md5(path.encode()).hexdigest(), 16) % (2**63)


def iterar_notas(vault):
    for p in sorted(vault.rglob("*.md")):
        rel = p.relative_to(vault)
        if any(part in EXCLUIR or part.startswith(".") for part in rel.parts):
            continue
        yield p


def ponto(p, max_chars):
    try:
        texto = p.read_text(encoding="utf-8", errors="ignore")
        mtime = p.stat().st_mtime
    except Exception:
        return None
    spath = str(p)
    return ({
        "id": id_estavel(spath),
        "vector": None,  # preenchido por embed_lotes; None -> placebo
        "payload": {
            "path": spath,
            "content": texto[:2000],
            "mtime": mtime,
            "tags": extrair_tags(spath),
            "vetor_placebo": True,
            "indexado_em": time.time(),
        },
    }, texto[:max_chars])


def embed_lotes(itens, url, batch, dim):
    """Preenche vetores via /v1/embeddings em lotes; falha -> divide e tenta; placebo honesto."""
    if not url:
        for pt, _t in itens:
            pt["vector"] = [0.0] * dim
        return {"reais": 0, "placebo": len(itens)}
    import time as _time

    def _embed_slice(fatia):
        body = json.dumps({"input": [t for _p, t in fatia]}).encode()
        req = urllib.request.Request(url, data=body,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=600) as resp:
            data = json.loads(resp.read())
        return [d["embedding"] for d in sorted(data["data"], key=lambda d: d["index"])]

    reais = 0
    # fila com backoff: falha em lote grande -> metade
    fila = [itens[i:i + batch] for i in range(0, len(itens), batch)]
    while fila:
        fatia = fila.pop(0)
        try:
            vecs = _embed_slice(fatia)
            for (pt, _t), v in zip(fatia, vecs):
                if len(v) == dim:
                    pt["vector"] = v
                    pt["payload"]["vetor_placebo"] = False
                    reais += 1
                else:
                    pt["vector"] = [0.0] * dim
            _time.sleep(0.35)
        except Exception as e:
            if len(fatia) > 1:
                m = len(fatia) // 2
                fila.insert(0, fatia[m:])
                fila.insert(0, fatia[:m])
                _time.sleep(0.5)
            else:
                fatia[0][0]["vector"] = [0.0] * dim
                print(json.dumps({"lote_unitario_falhou": fatia[0][0]["payload"]["path"][-60:], "erro": str(e)[:140]}))
                _time.sleep(0.4)
    placebo = sum(1 for pt, _ in itens if pt["vector"] is None or pt["payload"].get("vetor_placebo"))
    for pt, _ in itens:
        if pt["vector"] is None:
            pt["vector"] = [0.0] * dim
    return {"reais": reais, "placebo": placebo}


def upsert_lote(pontos, collection):
    body = json.dumps({"points": pontos}).encode()
    req = urllib.request.Request(
        f"{QDRANT}/collections/{collection}/points",
        data=body, headers={"Content-Type": "application/json"}, method="PUT",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def caminhos_placebo(collection):
    """Paths com vetor_placebo=true (scroll sem vetor)."""
    try:
        body = json.dumps({"limit": 2000, "with_payload": True,
                           "with_vector": False}).encode()
        req = urllib.request.Request(
            f"{QDRANT}/collections/{collection}/points/scroll",
            data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
        pts = data.get("result", {}).get("points", [])
        return [p["payload"]["path"] for p in pts
                if p.get("payload", {}).get("vetor_placebo")]
    except Exception:
        return []


def main():
    ap = argparse.ArgumentParser(description="Backfill vault -> Qdrant")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--vault", default=str(VAULT_PADRAO))
    ap.add_argument("--collection", default=COLLECTION)
    ap.add_argument("--dim", type=int, default=DIM)
    ap.add_argument("--embed-url", default="http://127.0.0.1:9097/v1/embeddings")
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--max-chars", type=int, default=600)
    ap.add_argument("--so-placebo", action="store_true",
                    help="re-embebe SOMENTE pontos com vetor_placebo=true")
    args = ap.parse_args()
    vault = Path(args.vault)
    if args.so_placebo:
        notas = [Path(p) for p in caminhos_placebo(args.collection)
                 if Path(p).exists() and str(p).endswith(".md")]
    else:
        notas = list(iterar_notas(vault))
    if args.limit:
        notas = notas[: args.limit]
    itens, falhas = [], 0
    for p in notas:
        r = ponto(p, args.max_chars)
        if r:
            itens.append(r)
        else:
            falhas += 1
    emb = embed_lotes(itens, args.embed_url or None, args.batch, args.dim)
    ok = 0
    for i in range(0, len(itens), 64):
        upsert_lote([pt for pt, _t in itens[i:i + 64]], args.collection)
        ok += min(64, len(itens) - i)
    print(json.dumps({"notas": len(notas), "indexadas": ok, "falhas": falhas,
                      "vetores_reais": emb["reais"], "vetor_placebo": emb["placebo"],
                      "collection": args.collection, "dim": args.dim}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
