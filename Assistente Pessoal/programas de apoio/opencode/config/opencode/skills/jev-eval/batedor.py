#!/usr/bin/env python3
"""batedor.py — motor determinístico do Serviço Batedor (jev-eval, 2026-09-18).

Recebe a decisão tipada emitida por um LLM barato (ex.: :9086) e devolve o veredito
de roteamento. O LLM NUNCA fala com o usuário; só este motor decide o destino.

Uso:
  echo '{"rota":"tecnico","topicos":["llm"],"urgente":false,"confianca":0.83,"needs_dense":false}' \
    | python3 batedor.py
  python3 batedor.py --file decisao.json
  python3 batedor.py --demo

Exit codes: 0 ok | 2 schema inválido | 3 gated (confiança < 0.6)
"""
import json, sys, hashlib, datetime

GATE_CONFIANCA = 0.6
ROTAS_VALIDAS = {"tecnico", "financeiro", "comercial", "geral", "vault", "codigo", "conversa"}

def validar(d: dict) -> list[str]:
    erros = []
    if not isinstance(d.get("rota"), str) or d["rota"] not in ROTAS_VALIDAS:
        erros.append(f"rota inválida: {d.get('rota')!r} (válidas: {sorted(ROTAS_VALIDAS)})")
    t = d.get("topicos", [])
    if not isinstance(t, list) or len(t) > 3 or not all(isinstance(x, str) for x in t):
        erros.append("topicos deve ser lista de ≤3 strings")
    if not isinstance(d.get("urgente"), bool):
        erros.append("urgente deve ser bool")
    c = d.get("confianca")
    if not isinstance(c, (int, float)) or not (0.0 <= c <= 1.0):
        erros.append("confianca deve ser float 0.0-1.0")
    if not isinstance(d.get("needs_dense"), bool):
        erros.append("needs_dense deve ser bool")
    return erros

def processar(d: dict) -> dict:
    erros = validar(d)
    if erros:
        return {"exit_status": "failed", "motivo": "schema_invalido", "erros": erros}
    gated = d["confianca"] < GATE_CONFIANCA
    fp = hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()[:12]
    destino = "revisao" if gated else ("denso" if d["needs_dense"] else "barato")
    return {
        "exit_status": "ok",
        "batedor": {
            "destino": destino,             # barato | denso | revisao
            "gated": gated,                 # True => turno marcado p/ revisão (nunca silencia)
            "gate_confianca": GATE_CONFIANCA,
            "rota": d["rota"],
            "needs_dense": d["needs_dense"],
            "fingerprint": fp,
            "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        },
    }

def main() -> int:
    argv = sys.argv[1:]
    if "--demo" in argv:
        demo = {"rota": "tecnico", "topicos": ["llm", "quantizacao"], "urgente": False,
                "confianca": 0.83, "needs_dense": False}
        print(json.dumps(processar(demo), ensure_ascii=False, indent=2)); return 0
    if "--file" in argv:
        d = json.load(open(argv[argv.index("--file") + 1]))
    else:
        raw = sys.stdin.read().strip()
        if not raw:
            print("uso: echo '<json>' | batedor.py | --file F | --demo", file=sys.stderr); return 2
        d = json.loads(raw)
    out = processar(d)
    print(json.dumps(out, ensure_ascii=False))
    if out["exit_status"] == "failed": return 2
    return 3 if out["batedor"]["gated"] else 0

if __name__ == "__main__":
    sys.exit(main())
