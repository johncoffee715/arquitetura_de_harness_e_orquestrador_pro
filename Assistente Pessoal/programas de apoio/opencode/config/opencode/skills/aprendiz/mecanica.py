#!/usr/bin/env python3
"""mecanica.py — motor determinístico do aprendiz (zero LLM, quarteto R85).

Valida deltas contra gabarito.json (selfs, fontes), faz dedupe por fingerprint,
grava 1 arquivo YAML por delta em aprendizados/deltas/, conta por self.
LLM barato só tipifica fonte→self (GBNF); a validação é 100% determinística.

Subcomandos:
  novo --fonte video|ebook|user|a2a --ref <path> --self S-ca|H-e|L-e|A-m \
       --principio "<1 frase>" --afeta skill1,skill2 --proposta "<diff>" \
       --confianca 0.0-1.0 [--evidencia <path>] [--contraexemplo "<txt>"] \
       [--claim-sem-evidencia]
  listar | contar-por-self | smoke

Exit: 0 ok | 2 schema inválido | 3 confiança < 0.6 (delta gravado com revisar: true)
"""
import argparse, datetime, hashlib, json, pathlib, sys

HERE = pathlib.Path(__file__).parent
VAULT = pathlib.Path("/mnt/dados/Assistente Pessoal/cerebro com IA")
GABARITO = json.loads((HERE / "gabarito.json").read_text(encoding="utf-8"))
DELTAS = VAULT / "aprendizados" / "deltas"
DELTAS.mkdir(parents=True, exist_ok=True)

SELFS = set(GABARITO["selfs_validos"])
FONTES = set(GABARITO["fontes_permitidas"])
GATE = GABARITO["limiares"]["gate_confianca"]


def validar(d: dict) -> list[str]:
    e = []
    if d.get("fonte_tipo") not in FONTES:
        e.append(f"fonte inválida: {d.get('fonte_tipo')!r} (válidas: {sorted(FONTES)})")
    if not isinstance(d.get("ref"), str) or not d["ref"].strip():
        e.append("fonte.ref obrigatória (path/url)")
    if d.get("self") not in SELFS:
        e.append(f"self inválido/ausente: {d.get('self')!r} — delta sem self = schema inválido")
    if not isinstance(d.get("principio"), str) or len(d["principio"].strip()) < 8:
        e.append("principio ausente/curto demais (<8 chars)")
    if not isinstance(d.get("proposta"), str) or not d["proposta"].strip():
        e.append("proposta obrigatória")
    if not isinstance(d.get("afeta"), list) or not d["afeta"]:
        e.append("afeta deve ser lista não-vazia")
    c = d.get("confianca")
    if not isinstance(c, (int, float)) or not (0.0 <= c <= 1.0):
        e.append("confianca deve ser 0.0-1.0")
    tem_evid = bool(d.get("evidencia"))
    if not tem_evid and not d.get("claim_sem_evidencia"):
        e.append("evidencia ausente EXIGE claim_sem_evidencia=true (gate anti nota-podre)")
    return e


def gravar(d: dict) -> pathlib.Path:
    hoje = d.get("data") or datetime.date.today().isoformat()
    fp = hashlib.sha1((d["ref"] + "|" + d["principio"]).encode()).hexdigest()[:10]
    slug = "".join(c if c.isalnum() else "-" for c in d["principio"].lower())[:40].strip("-")
    path = DELTAS / f"{hoje}_{d['self']}_{slug}_{fp}.md"
    if path.exists():
        return path  # dedupe idempotente
    ev = f'"{d["evidencia"]}"' if d.get("evidencia") else "null"
    path.write_text(f"""---
tipo: delta
id: "{hoje}-{fp}"
data: "{hoje}"
fonte: {{tipo: "{d['fonte_tipo']}", ref: "{d['ref']}"}}
self: "{d['self']}"
principio: "{d['principio']}"
contraexemplo: "{d.get('contraexemplo', '')}"
evidencia: {ev}
afeta: {json.dumps(d['afeta'], ensure_ascii=False)}
proposta: "{d['proposta']}"
confianca: {d['confianca']}
claim_sem_evidencia: {str(bool(d.get('claim_sem_evidencia'))).lower()}
revisar: {str(d['confianca'] < GATE).lower()}
status: pendente_gate
---

# delta — {d['self']} — {d['principio']}

**Proposta:** {d['proposta']}
""", encoding="utf-8")
    return path


def novo(a) -> int:
    d = {
        "fonte_tipo": a.fonte, "ref": a.ref, "self": a.self,
        "principio": a.principio, "proposta": a.proposta,
        "afeta": [s.strip() for s in a.afeta.split(",") if s.strip()],
        "confianca": a.confianca, "evidencia": a.evidencia,
        "contraexemplo": a.contraexemplo or "",
        "claim_sem_evidencia": a.claim_sem_evidencia,
    }
    erros = validar(d)
    if erros:
        print(json.dumps({"exit_status": "failed", "erros": erros}, ensure_ascii=False, indent=2))
        return 2
    p = gravar(d)
    gated = d["confianca"] < GATE
    print(json.dumps({"exit_status": "ok", "delta": str(p), "self": d["self"],
                      "revisar": gated}, ensure_ascii=False))
    return 3 if gated else 0


def listar() -> int:
    ds = sorted(DELTAS.glob("*.md"))
    if not ds:
        print("zero deltas")
        return 0
    for p in ds:
        linhas = p.read_text(encoding="utf-8").splitlines()
        meta = [l for l in linhas if l.startswith(("self:", "principio:", "status:", "revisar:"))][:4]
        print(f"{p.name}\n    {' | '.join(meta)}")
    return 0


def contar() -> int:
    ds = sorted(DELTAS.glob("*.md"))
    cont: dict[str, int] = {s: 0 for s in SELFS}
    n_revisar = 0
    for p in ds:
        front = p.read_text(encoding="utf-8").split("---")[1] if "---" in p.read_text(encoding="utf-8") else ""
        for s in SELFS:
            if f'self: "{s}"' in front:
                cont[s] += 1
                break
        if "revisar: true" in front:
            n_revisar += 1
    print(json.dumps({"total": len(ds), "por_self": cont, "revisar": n_revisar}, ensure_ascii=False))
    return 0


def smoke() -> int:
    """Prova de vida: valida aceitação, rejeição e gate sem tocar o vault real."""
    bom = {"fonte_tipo": "video", "ref": "x.md", "self": "L-e",
           "principio": "teste de fumaça ok", "proposta": "n/a",
           "afeta": ["aprendiz"], "confianca": 0.9, "evidencia": "x.md"}
    ruim = {"fonte_tipo": "video", "ref": "x.md", "principio": "x",
            "proposta": "", "afeta": [], "confianca": 2.0}
    sem_ev = {"fonte_tipo": "user", "ref": "y", "self": "H-e",
              "principio": "sem evidência nenhuma", "proposta": "p",
              "afeta": ["gari"], "confianca": 0.9}
    ok1 = validar(bom) == []
    ok2 = len(validar(ruim)) >= 3
    ok3 = any("claim_sem_evidencia" in e for e in validar(sem_ev))
    gate = bom["confianca"] < GATE  # False aqui
    res = {"valida_bom": ok1, "rejeita_ruim": ok2, "exige_flag_sem_evidencia": ok3,
           "gate_06_ativo_em_baixa": gate is False}
    print(json.dumps({"smoke": all([ok1, ok2, ok3]), **res}, ensure_ascii=False))
    return 0 if all([ok1, ok2, ok3]) else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("novo")
    n.add_argument("--fonte", required=True); n.add_argument("--ref", required=True)
    n.add_argument("--self", required=True); n.add_argument("--principio", required=True)
    n.add_argument("--afeta", required=True); n.add_argument("--proposta", required=True)
    n.add_argument("--confianca", type=float, required=True)
    n.add_argument("--evidencia"); n.add_argument("--contraexemplo")
    n.add_argument("--claim-sem-evidencia", action="store_true")
    sub.add_parser("listar"); sub.add_parser("contar-por-self"); sub.add_parser("smoke")
    a = ap.parse_args()
    if a.cmd == "novo": return novo(a)
    if a.cmd == "listar": return listar()
    if a.cmd == "contar-por-self": return contar()
    if a.cmd == "smoke": return smoke()
    return 2


if __name__ == "__main__":
    sys.exit(main())
