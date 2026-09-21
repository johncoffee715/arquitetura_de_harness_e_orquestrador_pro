"""Motor determinístico do modo-autonomo (R77/R85/R89). Fail-closed, idempotente, zero LLM."""
import json
import re
import sys

DENY = ("rm -rf", "trash --empty", "git reset --hard", "matar :8083",
        "matar o :8083", "sudo", "senha")
TRIGGER_RE = re.compile(r"(modo\s*aut[ôo]nomo|autonomous mode|dev\s*loop|cloud-direct)",
                        re.IGNORECASE)
VERDICT_OK = "Pode reiniciar \u2014 zero pend\u00eancias."


def decide(state_ativo: bool, texto: str, comando: str = "") -> dict:
    """Uma função focada: valida trigger + deny byte-level. Retorna veredito."""
    cmd = (comando or "").strip()
    for d in DENY:
        if d in cmd or d in (texto or ""):
            return {"verdict": "NAO_PASSOU_CATEGORICO",
                    "motivo": f"deny irreversivel: {d}"}
    if not state_ativo:
        return {"verdict": "NAO_PASSOU_CATEGORICO",
                "motivo": "estado OFF (fail-closed)"}
    if not TRIGGER_RE.search(texto or ""):
        return {"verdict": "NAO_PASSOU_CATEGORICO",
                "motivo": "trigger sem match byte-level"}
    return {"verdict": "PASSOU_CATEGORICO",
            "motivo": "trigger ON + sem deny; rotear cloud-direct"}


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception as exc:
        print(json.dumps({"verdict": "NAO_PASSOU_CATEGORICO",
                          "motivo": f"stdin invalido: {exc}"}))
        return 2
    out = decide(bool(payload.get("state_ativo", False)),
                 str(payload.get("texto", "")),
                 str(payload.get("comando", "")))
    print(json.dumps(out, ensure_ascii=False))
    return 0 if out["verdict"] == "PASSOU_CATEGORICO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
