#!/usr/bin/env python3
"""
Catalogacao tematica (F1) — Bibliotecario gerente (R94).

tags(nota) = frontmatter `tags:` + TF com stopwords PT.
Deterministico, zero LLM, zero rede. Importado por backfill.py e watcher.py.
"""

import re
from collections import Counter
from pathlib import Path

STOP = set(
    "a ao aos aquela aquelas aquele aqueles aquilo as ate com como da das de "
    "do dos e ela elas ele eles em entre era eram essa essas esse esses esta "
    "estas este estes eu foi foram ha isso isto ja lhe lhes mais mas me mesmo "
    "minha minhas meu meus muito na nas nao nem no nos nossa nossas nosso "
    "nossos nunca o os ou para pela pelas pelo pelos por qual quando que quem "
    "se sem ser seu seus sua suas talvez tambem te tem temos tendo tenha "
    "tenham teve tive tiveram um uma uns umas vai vao ser sao sobre sob "
    "entre onde como qual quais cujo cuja quanto desta deste disso desse "
    "dessa daquele daquela disto nisto nota notas arquivo vault obsidian "
    "the and for with from that this these those are was were been has have "
    "had will would can could should may might must shall their there their "
    "then than them they them its into over after before between under over".split()
)
TOK = re.compile(r"[a-zà-ú0-9][a-zà-ú0-9\-]{3,}")


def tags_frontmatter(texto):
    """Extrai tags: do bloco YAML inicial (tags: [a,b] | lista com '- ')."""
    tags = []
    if texto.startswith("---"):
        fim = texto.find("---", 3)
        head = texto[: fim if fim > 0 else 1500]
        m = re.search(r"^tags:\s*\[(.*?)\]", head, re.M | re.S)
        if m:
            tags += [t.strip().strip("'\"") for t in m.group(1).split(",")]
        tags += re.findall(r"^\s*-\s*([a-zA-Z0-9à-ú_\-/ ]{2,40})\s*$", head, re.M)[:12]
    return [t.strip().lower() for t in tags if t and t.strip()]


def tags_tf(texto, top=5):
    """Top termos por frequencia (STOP PT+EN, len>=4, freq>=2)."""
    toks = [t.lower() for t in TOK.findall(texto.lower())]
    freq = Counter(t for t in toks if t not in STOP)
    return [w for w, c in freq.most_common(top) if c >= 2]


def extrair_tags(path):
    """Tags unidas e dedupadas de uma nota. Nunca joga excecao."""
    try:
        texto = Path(path).read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    tags = tags_frontmatter(texto) + tags_tf(texto)
    vistas, unicas = set(), []
    for t in tags:
        if t not in vistas:
            vistas.add(t)
            unicas.append(t)
    return unicas[:10]


if __name__ == "__main__":
    import sys

    for arg in sys.argv[1:]:
        print(arg, "=>", extrair_tags(arg))
