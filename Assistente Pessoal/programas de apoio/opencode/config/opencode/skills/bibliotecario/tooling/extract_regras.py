#!/usr/bin/env python3
"""
extract_regras.py — R101: extrai as regras do AGENTS.md para notas individuais em regras/

Determinístico (zero LLM): parseia os headers de regra (2 formatos: `## RXX` e
`# ═══ REGRA GLOBAL RXX`), divide em blocos e escreve uma nota por regra em
`cerebro com IA/regras/`. Duplicatas (R35/R46-R50) ganham sufixo -vN.

Origem: hefesto: forja R101 (2026-09-11)
"""
import re
from pathlib import Path

AGENTS_MD = Path("/mnt/dados/Assistente Pessoal/programas de apoio/opencode/config/opencode/AGENTS.md")
REGRAS_DIR = Path("/mnt/dados/Assistente Pessoal/cerebro com IA/regras")

HEADER_RE = re.compile(
    r"^(?P<prefix>##\s+|#\s+═══\s+REGRA GLOBAL\s+)(?P<rid>R\d+(?:/R\d+)?)\s*[—-]\s*(?P<title>.+?)\s*$",
    re.MULTILINE,
)


def clean_title(t: str) -> str:
    t = t.strip()
    t = re.sub(r"\s*═══\s*$", "", t)
    t = re.sub(r"\s*[—-]\s*promulgado.*$", "", t)
    return t.strip()


def slugify(t: str) -> str:
    s = re.sub(r"[^a-z0-9à-ú]+", "-", t.lower())
    return re.sub(r"-+", "-", s).strip("-")[:60] or "regra"


def main():
    text = AGENTS_MD.read_text(encoding="utf-8")
    ms = list(HEADER_RE.finditer(text))
    REGRAS_DIR.mkdir(parents=True, exist_ok=True)
    seen = {}
    written = []
    for i, m in enumerate(ms):
        rid = m.group("rid")
        title = clean_title(m.group("title"))
        start = m.start()
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        block = text[start:end].strip()
        seen[rid] = seen.get(rid, 0) + 1
        slug = slugify(title)
        if seen[rid] > 1:
            slug = f"{slug}-v{seen[rid]}"
        fname = f"{rid.lower().replace('/', '-')}-{slug}.md"
        line = text[:start].count("\n") + 1
        note = (
            f"---\nregra: {rid}\ntitulo: \"{title}\"\n"
            f"fonte: AGENTS.md (linha {line})\ndata: 2026-09-11\n---\n\n{block}\n"
        )
        (REGRAS_DIR / fname).write_text(note, encoding="utf-8")
        written.append(fname)
    print(f"Extraídas {len(written)} regras para {REGRAS_DIR}")
    for f in written:
        print(f"  {f}")


if __name__ == "__main__":
    main()