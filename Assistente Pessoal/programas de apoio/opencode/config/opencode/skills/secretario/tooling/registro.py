#!/usr/bin/env python3
"""
Registro vetorial do secretário — upsert real 1024-d no Qdrant (R96 honesto).

Uso:
    registro.py "texto" [--tipo decisao|nota|lembrete] [--tags a,b]

Coleção: bibliotecario_1024 (Cosine, 1024-d). Payload sempre com origem="secretario".
Se o embedding falhar: NÃO faz upsert de vetor zero — retorna exit 2 (blocked)
com vetor_placebo:true e motivo (norma R96/R28: placebo nunca operante).
Verificação de leitura: GET do ponto + count filtrado por origem=secretario.
"""

import argparse
import datetime
import hashlib
import json
import sys
import time
import urllib.request

sys.path.insert(0, "/home/johncoffee/.config/opencode/skills/bibliotecario/tooling")
try:
    from embeddings import embed  # noqa: E402
except Exception as e:  # pragma: no cover
    embed = None

QDRANT = "http://localhost:6333"
COLECAO = "bibliotecario_1024"
MAX_RETRIES = 3


def _http(method, url, body=None, timeout=10):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Content-Type": "application/json"})
    last = None
    for _ in range(MAX_RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read())
        except Exception as e:
            last = e
            time.sleep(0.3)
    raise RuntimeError(f"{method} {url} falhou 3x: {last}")


def registrar(texto, tipo="nota", tags=None):
    tags = tags or []
    if embed is None:
        return {"acao": "registro", "vetor_placebo": True,
                "motivo": "cliente de embeddings indisponível (import falhou)",
                "exit_status": "blocked"}, 2
    vec = embed(texto, timeout=15, prefer="auto")
    if vec is None:
        return {"acao": "registro", "vetor_placebo": True,
                "motivo": "motor :9094 indisponível — sem vetor real, upsert recusado (R96)",
                "exit_status": "blocked"}, 2
    if len(vec) != 1024:
        return {"acao": "registro", "vetor_placebo": True,
                "motivo": f"dimensão inesperada {len(vec)} (esperada 1024) — upsert recusado",
                "exit_status": "blocked"}, 2

    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    chave = (ts + texto[:64]).encode()
    ponto_id = int(hashlib.md5(chave).hexdigest()[:12], 16)
    payload = {"origem": "secretario", "tipo": tipo,
               "content": texto[:2000], "ts": ts, "tags": tags}
    _http("PUT", f"{QDRANT}/collections/{COLECAO}/points",
          {"points": [{"id": ponto_id, "vector": vec, "payload": payload}]},
          timeout=15)

    # verificação de leitura: o ponto existe + count de origem=secretario
    got = _http("GET", f"{QDRANT}/collections/{COLECAO}/points/{ponto_id}")
    verificado = bool(got.get("result")
                      and got["result"].get("payload", {}).get("origem") == "secretario")
    cnt = _http("POST", f"{QDRANT}/collections/{COLECAO}/points/count",
                {"filter": {"must": [{"key": "origem",
                                      "match": {"value": "secretario"}}]}})
    return {
        "acao": "registro", "destino": "registro_vetorial",
        "ponto_id": ponto_id, "tipo": tipo, "dim": len(vec),
        "verificado": verificado,
        "count_secretario": cnt.get("result", {}).get("count"),
        "vetor_placebo": False, "exit_status": "ok" if verificado else "failed",
    }, 0 if verificado else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="Registro vetorial do secretário")
    ap.add_argument("texto", help="conteúdo a registrar (≤2000 chars guardados)")
    ap.add_argument("--tipo", default="nota", choices=["decisao", "nota", "lembrete"])
    ap.add_argument("--tags", default="", help="tags separadas por vírgula")
    args = ap.parse_args(argv)
    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    try:
        out, code = registrar(args.texto, tipo=args.tipo, tags=tags)
    except Exception as e:
        print(json.dumps({"acao": "registro", "erro": str(e),
                          "vetor_placebo": True, "exit_status": "failed"},
                         ensure_ascii=False), flush=True)
        return 1
    print(json.dumps(out, ensure_ascii=False), flush=True)
    return code


if __name__ == "__main__":
    sys.exit(main())
