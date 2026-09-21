#!/usr/bin/env python3
"""propor.py — proposal-queue HITL anti nota-podre (bibliotecario 2.1.0).

Cria proposta em pending_review/ — conteúdo factual novo NUNCA entra direto no vault.

Uso:
  python3 propor.py --titulo "Síntese X" --origem video:ae92ibehs4Q --self L-e \
      --evidencia "textos, pdf e esquemas/ae92ibehs4Q-transcricao-pt.md" \
      --arquivo-corpo /tmp/corpo.md
  # ou corpo via stdin:
  echo "conteúdo" | python3 propor.py --titulo "..." --origem a2a --self S-ca \
      --evidencia decisoes/2026-09-18.md
  python3 propor.py --listar

Exit: 0 ok | 2 args inválidos
"""
import argparse, hashlib, pathlib, sys, datetime

VAULT = pathlib.Path("/mnt/dados/Assistente Pessoal/cerebro com IA")
PENDING = VAULT / "pending_review"
SELFS = {"S-ca", "H-e", "L-e", "A-m"}

def criar(titulo: str, origem: str, self_: str, evidencia: str, corpo: str) -> pathlib.Path:
    assert self_ in SELFS, f"self inválido: {self_} (válidos: {sorted(SELFS)})"
    slug = "".join(c if c.isalnum() else "-" for c in titulo.lower())[:48].strip("-")
    hoje = datetime.date.today().isoformat()
    fp = hashlib.sha256(corpo.encode()).hexdigest()[:12]
    path = PENDING / f"{hoje}_{slug}_{fp}.md"
    if path.exists():
        print(f"DUPLICATA (fingerprint {fp}): {path}", file=sys.stderr)
        return path
    path.write_text(f"""---
tipo: proposta
status: pendente_gate
titulo: "{titulo}"
proposta_de: "{origem}"
self: "{self_}"
evidencia: "{evidencia}"
fingerprint: {fp}
data: {hoje}
---

# PROPOSTA PENDENTE — aguarda gate humano (ou GM autônomo R34)

{corpo}
""", encoding="utf-8")
    return path

def listar() -> None:
    props = sorted(PENDING.glob("*.md"))
    if not props:
        print("fila vazia")
        return
    for p in props:
        head = [l for l in p.read_text(encoding="utf-8").splitlines()[1:8] if l.startswith(("titulo:", "self:", "status:"))]
        print(f"{p.name}  |  {' | '.join(head)}")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--titulo"); ap.add_argument("--origem"); ap.add_argument("--self", dest="self_")
    ap.add_argument("--evidencia"); ap.add_argument("--arquivo-corpo")
    ap.add_argument("--listar", action="store_true")
    a = ap.parse_args()
    if a.listar:
        listar(); return 0
    if not all([a.titulo, a.origem, a.self_, a.evidencia]):
        ap.error("--titulo --origem --self --evidencia são obrigatórios")
    corpo = pathlib.Path(a.arquivo_corpo).read_text(encoding="utf-8") if a.arquivo_corpo else sys.stdin.read()
    if not corpo.strip():
        ap.error("corpo vazio")
    p = criar(a.titulo, a.origem, a.self_, a.evidencia, corpo)
    print(f"OK {p}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
