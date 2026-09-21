"""Parser CSR (Compressed Sparse Row) — CSV -> row_ptr/col_idx/weight.

Sem dependências externas (stdlib apenas). Implementa o pipeline de 2 passes
da spec-parser-csr.md: contagem de grau de saída (pass 1) e preenchimento com
agregação de multiedges (pass 2).
"""

from __future__ import annotations


def parse_csv_to_csr(path: str):
    """Lê um dump CSV de adjacência e devolve (row_ptr, col_idx, weight).

    Formato de linha: `<pre_id> <post_id> <weight>` (espaços/vírgulas),
    comentários iniciados por `#` são ignorados. Multiedges entre o mesmo par
    (pre, post) são agregados somando pesos.
    """
    edges: dict[tuple[int, int], int] = {}

    with open(path, "r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.replace(",", " ").split()
            if len(parts) < 3:
                continue
            pre = int(parts[0])
            post = int(parts[1])
            w = int(parts[2])
            key = (pre, post)
            edges[key] = edges.get(key, 0) + w

    if not edges:
        return [0], [], []

    n = max(max(pre, post) for pre, post in edges) + 1

    # Pass 1: grau de saída por neurônio -> row_ptr (prefix sum)
    degree = [0] * n
    for pre, _post in edges:
        degree[pre] += 1

    row_ptr = [0] * (n + 1)
    for i in range(n):
        row_ptr[i + 1] = row_ptr[i] + degree[i]

    # Pass 2: preenchimento ordenado por (pre, post)
    col_idx = [0] * len(edges)
    weight = [0] * len(edges)
    cursor = row_ptr[:]  # cópia para cursor de escrita por linha
    for (pre, post), w in sorted(edges.items()):
        pos = cursor[pre]
        col_idx[pos] = post
        weight[pos] = w
        cursor[pre] += 1

    return row_ptr, col_idx, weight