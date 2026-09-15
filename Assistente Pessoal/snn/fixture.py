"""Fixture sintética mínima para o parser CSR do conectoma.

Ground truth até o Hefesto absorver o dado real (MaleCNS). NÃO é o dataset
completo (125M/312M sinapses) — é uma amostra pequena, determinística, que
exercita todos os invariantes do parser (spec-parser-csr.md):

  - grafo dirigido (pré → pós, sem aresta reversa implícita);
  - multiedge por peso (sinapses poliádicas agregadas somando pesos);
  - comentários e campos extras ignorados (tolerância a schema FlyEM real).

Formato canônico do dump (uma linha por sinapse):
    <pre_id> <post_id> <weight> [<extra>...]
"""

from __future__ import annotations

# N = número de neurônios na fixture (índices 0..N-1).
N = 6

# Dump CSV sintético. Inclui:
#   - comentário (linha 1) — deve ser ignorado;
#   - multiedge: (0,1) aparece 2x com pesos 3 e 2 → agregado em peso 5;
#   - campo extra (neurotransmissor) — deve ser ignorado pelo parser core;
#   - aresta dirigida: (2,3) existe, mas (3,2) NÃO (direção preservada).
DUMP_CSV = """\
# conectoma sintético — fixture mínima
0,1,3,acetylcholine
0,1,2,acetylcholine
0,2,1,glutamate
1,3,4,acetylcholine
2,3,2,glutamate
2,4,1,glutamate
4,5,7,octopamine
"""

# CSR esperado após parse (agregação de multiedges, ordenado por (pre, post)).
# Arestas únicas (E_agregado = 6):
#   (0,1)w5  (0,2)w1  (1,3)w4  (2,3)w2  (2,4)w1  (4,5)w7
# Graus de saída: 0→2, 1→1, 2→2, 3→0, 4→1, 5→0.
EXPECTED_ROW_PTR = [0, 2, 3, 5, 5, 6, 6]
EXPECTED_COL_IDX = [1, 2, 3, 3, 4, 5]
EXPECTED_WEIGHT = [5, 1, 4, 2, 1, 7]
EXPECTED_E_AGGREGADO = 6  # == len(col_idx) == len(weight) == row_ptr[N]


def dump_lines() -> list[str]:
    """Retorna as linhas do dump (sem o newline final), para o parser consumir."""
    return DUMP_CSV.strip("\n").split("\n")