"""Parser CSR (Compressed Sparse Row) para o grafo de adjacência do conectoma.

Converte um dump de adjacência (lista de sinapses) em CSR, seguindo a
spec-parser-csr.md. Pipeline de 2 passes:

  1. Pass 1 (contagem): grau de saída por neurônio → row_ptr (prefix sum).
  2. Pass 2 (preenchimento): popular col_idx/weight, agregando multiedges.

Invariantes (proteína do conectoma):
  - grafo dirigido (pré → pós, sem aresta reversa implícita);
  - multiedge por peso (sinapses poliádicas agregadas somando pesos);
  - comentários e campos extras ignorados (tolerância a schema FlyEM real).

Anti-padrões evitados (spec §8): sem matriz densa, sem hash de pares.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Csr:
    """Grafo de adjacência em CSR — produzido pelo parser.

    - row_ptr: tamanho N+1; row_ptr[i..i+1] = intervalo em col_idx/weight.
    - col_idx: tamanho E_agregado; pós-sinápticos ordenados por (pre, post).
    - weight:  tamanho E_agregado; peso por aresta agregada.
    """

    row_ptr: list[int]
    col_idx: list[int]
    weight: list[int]
    n: int = field(default=0)

    def __post_init__(self) -> None:
        self.n = len(self.row_ptr) - 1

    def out_neighbors(self, pre: int):
        """Itera os vizinhos pós-sinápticos de `pre` como (post, weight)."""
        start, end = self.row_ptr[pre], self.row_ptr[pre + 1]
        for i in range(start, end):
            yield self.col_idx[i], self.weight[i]


def parse_csr(lines, n: int) -> Csr:
    """Parseia um dump de sinapses em CSR.

    Args:
        lines: iterável de linhas do dump (formato canônico da spec §2).
        n: número de neurônios (índices 0..n-1).

    Returns:
        Csr com row_ptr/col_idx/weight consistentes.
    """
    # Pass 0: normalizar linhas em arestas dirigidas (pre, post, weight).
    edges: list[tuple[int, int, int]] = []
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue  # comentário / linha vazia → ignorado.
        parts = line.split(",")
        pre = int(parts[0].strip())
        post = int(parts[1].strip())
        weight = int(parts[2].strip())
        # Campos extras (parts[3:]) ignorados pelo parser core.
        edges.append((pre, post, weight))

    # Pass 1 (contagem): grau de saída por neurônio, contando ARESTAS ÚNICAS
    # (multiedges agregam — não contam como grau extra). E_agregado ≤ E.
    unique_edges: set[tuple[int, int]] = set()
    for pre, post, _w in edges:
        unique_edges.add((pre, post))

    out_degree = [0] * n
    for pre, post in unique_edges:
        out_degree[pre] += 1

    # row_ptr via prefix sum.
    row_ptr = [0] * (n + 1)
    for i in range(n):
        row_ptr[i + 1] = row_ptr[i] + out_degree[i]

    # Pass 2 (preenchimento): cursor por linha + agregação de multiedges.
    cursor = row_ptr[:-1]  # cópia do início de cada linha.
    e_agregado = len(unique_edges)
    col_idx = [0] * e_agregado
    weight = [0] * e_agregado

    # Agregação de multiedges: somar pesos de arestas (pre, post) repetidas.
    # Usa dict (pre, post) -> posição no col_idx para somar no lugar.
    pos_of: dict[tuple[int, int], int] = {}
    for pre, post, w in edges:
        key = (pre, post)
        if key in pos_of:
            weight[pos_of[key]] += w  # multiedge → soma peso.
        else:
            idx = cursor[pre]
            cursor[pre] += 1
            col_idx[idx] = post
            weight[idx] = w
            pos_of[key] = idx

    # Ordenar col_idx/weight por (pre, post) dentro de cada linha (spec §4).
    for pre in range(n):
        start, end = row_ptr[pre], row_ptr[pre + 1]
        if end - start > 1:
            pairs = sorted(zip(col_idx[start:end], weight[start:end]))
            col_idx[start:end] = [p for p, _ in pairs]
            weight[start:end] = [w for _, w in pairs]

    return Csr(row_ptr=row_ptr, col_idx=col_idx, weight=weight)


def parse_csv_to_csr(path: str):
    """Lê um dump CSV de adjacência e devolve (row_ptr, col_idx, weight).

    Formato de linha: `<pre_id> <post_id> <weight>` (espaços/vírgulas),
    comentários iniciados por `#` são ignorados. Multiedges entre o mesmo par
    (pre, post) são agregados somando pesos. O número de neurônios `n` é
    inferido do maior índice presente (índices 0..n-1).
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

    csr = parse_csr(
        (f"{pre},{post},{w}" for (pre, post), w in edges.items()),
        n=n,
    )
    return csr.row_ptr, csr.col_idx, csr.weight