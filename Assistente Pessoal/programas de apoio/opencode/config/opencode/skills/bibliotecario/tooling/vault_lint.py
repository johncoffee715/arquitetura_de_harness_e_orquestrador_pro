#!/usr/bin/env python3
"""vault_lint.py — Guardrail funcional do vault (anti-'estético sem função').

Verifica DETERMINISTICAMENTE (zero LLM):
  1. Todo [[wikilink]] do wiki/index.md resolve para arquivo .md real.
  2. Toda nota em wiki/summaries/ tem frontmatter com chaves obrigatórias.
  3. Todo 'asset_fonte' citado em summaries existe no disco.
  4. Orfãs: summaries/conceitos existentes mas não listadas no index.md.

Uso: python3 vault_lint.py [--vault DIR]
Exit 0 = tudo íntegro; Exit 1 = falhas (listadas).
"""
import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_FM = ["source", "date", "type", "tags"]
WIKILINK = re.compile(r"\[\[([^\]|]+?)(?:\|[^\]]*)?\]\]")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--vault",
        default="/mnt/dados/Assistente Pessoal/cerebro com IA",
    )
    args = ap.parse_args()
    vault = Path(args.vault)
    wiki = vault / "wiki"
    index = wiki / "index.md"

    falhas: list[str] = []
    avisos: list[str] = []
    checagens = 0

    # 1. links do index resolvem
    if not index.exists():
        falhas.append("wiki/index.md ausente")
        links_ok = []
    else:
        conteudo = index.read_text(encoding="utf-8")
        conteudo = re.sub(r"`[^`]*`", "", conteudo)  # ignora código inline
        conteudo = re.sub(r"\*[^*\n]+\*", "", conteudo)  # ignora itálico (rodapé métricas)
        links = set(WIKILINK.findall(conteudo))
        links_ok = []
        for link in sorted(links):
            cand = [
                vault / f"{link}.md",
                wiki / f"{link}.md",
                vault / link,
                wiki / link,
                wiki / link.rstrip("/") / "index.md",
            ]
            checagens += 1
            if any(p.is_file() or p.is_dir() for p in cand):
                links_ok.append(link)
            else:
                falhas.append(f"[index] link quebrado: [[{link}]]")

    # 2+3. frontmatter + asset_fonte
    summaries = sorted((wiki / "summaries").glob("*.md")) if (wiki / "summaries").exists() else []
    for nota in summaries:
        checagens += 1
        txt = nota.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
        if not m:
            falhas.append(f"[fm] {nota.name}: sem frontmatter")
            continue
        bloco = m.group(1)
        for chave in REQUIRED_FM:
            if not re.search(rf"^{chave}\s*:", bloco, re.M):
                falhas.append(f"[fm] {nota.name}: falta chave '{chave}'")
        m_asset = re.search(r'^asset_fonte:\s*"?(.*?)"?\s*$', bloco, re.M)
        if m_asset:
            checagens += 1
            alvo = vault / m_asset.group(1)
            if not alvo.exists():
                falhas.append(f"[asset] {nota.name}: fonte inexistente -> {m_asset.group(1)}")

    # 4. orfãs
    if index.exists():
        texto_idx = index.read_text(encoding="utf-8")
        for sub in ("summaries", "concepts"):
            for nota in sorted((wiki / sub).glob("*.md")):
                checagens += 1
                if nota.stem not in texto_idx:
                    avisos.append(f"[orfa] {sub}/{nota.name} não consta no index.md")

    relatorio = {
        "vault": str(vault),
        "checagens": checagens,
        "falhas": falhas,
        "avisos": avisos,
        "ok": not falhas,
    }
    print(json.dumps(relatorio, ensure_ascii=False, indent=2))
    return 0 if not falhas else 1


if __name__ == "__main__":
    sys.exit(main())
