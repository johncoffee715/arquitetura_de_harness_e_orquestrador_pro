"""Teste de contrato do parser CSR (RED→GREEN).

Valida os invariantes da spec-parser-csr.md contra a fixture sintética:
  - row_ptr monotônico não-decrescente, row_ptr[N] == len(col_idx) == len(weight);
  - col_idx em [0, N); weight > 0;
  - agregação de multiedges (peso somado);
  - grafo dirigido (sem aresta reversa implícita);
  - tolerância a comentários e campos extras (schema FlyEM real).
"""

from __future__ import annotations

import pytest

import fixture
from parser import parse_csr


def test_parse_csr_matches_fixture():
    """Parser lê o dump e emite CSR idêntico ao ground truth da fixture."""
    csr = parse_csr(fixture.dump_lines(), n=fixture.N)

    assert csr.row_ptr == fixture.EXPECTED_ROW_PTR
    assert csr.col_idx == fixture.EXPECTED_COL_IDX
    assert csr.weight == fixture.EXPECTED_WEIGHT


def test_csr_invariants():
    """Invariantes byte-level da spec (row_ptr/col_idx/weight consistentes)."""
    csr = parse_csr(fixture.dump_lines(), n=fixture.N)

    # row_ptr monotônico não-decrescente.
    assert all(a <= b for a, b in zip(csr.row_ptr, csr.row_ptr[1:]))
    # row_ptr[0] == 0 e row_ptr[N] == E_agregado == len(col_idx) == len(weight).
    assert csr.row_ptr[0] == 0
    assert csr.row_ptr[-1] == len(csr.col_idx) == len(csr.weight)
    assert csr.row_ptr[-1] == fixture.EXPECTED_E_AGGREGADO
    # col_idx em [0, N); weight > 0.
    assert all(0 <= c < fixture.N for c in csr.col_idx)
    assert all(w > 0 for w in csr.weight)


def test_multiedge_aggregation():
    """Sinapses poliádicas (0,1) com pesos 3 e 2 agregam em peso 5."""
    csr = parse_csr(fixture.dump_lines(), n=fixture.N)

    # Vizinhos pós-sinápticos do neurônio 0: (1, peso 5) e (2, peso 1).
    start, end = csr.row_ptr[0], csr.row_ptr[1]
    neighbors = dict(zip(csr.col_idx[start:end], csr.weight[start:end]))
    assert neighbors == {1: 5, 2: 1}


def test_directed_graph():
    """Grafo dirigido: (2,3) existe, mas (3,2) NÃO (sem aresta reversa)."""
    csr = parse_csr(fixture.dump_lines(), n=fixture.N)

    def has_edge(pre: int, post: int) -> bool:
        start, end = csr.row_ptr[pre], csr.row_ptr[pre + 1]
        return post in csr.col_idx[start:end]

    assert has_edge(2, 3) is True
    assert has_edge(3, 2) is False


def test_tolerates_extra_fields_and_comments():
    """Comentários e campos extras (neurotransmissor) são ignorados."""
    # A fixture já contém comentário + campo extra; se o parse acima passou,
    # a tolerância está garantida. Reforço com um dump mínimo com ruído.
    noisy = [
        "# comentário",
        "0,1,2,acetylcholine,extra,ignorado",
        "  1,2,3   ",  # espaços em branco tolerados
    ]
    csr = parse_csr(noisy, n=3)
    assert csr.row_ptr == [0, 1, 2, 2]
    assert csr.col_idx == [1, 2]
    assert csr.weight == [2, 3]