"""TDD do caminho feather -> CSR (slice de 100k linhas + parse_csr).

Consome parser.py sem modifica-lo; valida que o streaming por batches
gera CSR identico ao parse direto e respeita os invariantes da spec.
"""

from __future__ import annotations

import inspect

import feather_to_csr as f2c
from parser import parse_csr

FEATHER = "snn/data/connectome-weights.feather"
SLICE = 100_000


def test_iter_triples_is_streaming_generator():
    """iter_triples e generator: batches processados um a um, sem full-table."""
    assert inspect.isgeneratorfunction(f2c.iter_triples)
    reader = f2c.open_reader(FEATHER)
    assert reader.num_record_batches > 1  # 2318 batches reais


def test_slice_yields_first_100k_rows():
    """Amostra das primeiras 100k linhas tem exatamente 100k triplas."""
    triples = list(f2c.iter_triples(FEATHER, limit_rows=SLICE))
    assert len(triples) == SLICE
    assert all(len(t) == 3 and t[2] > 0 for t in triples[:1000])


def test_slice_csr_consistent_with_parse_csr():
    """CSR do slice == parse_csr direto sobre as mesmas linhas remapeadas."""
    triples = list(f2c.iter_triples(FEATHER, limit_rows=SLICE))
    agg = f2c.aggregate_triples(triples)
    ids: set[int] = set()
    for pre, post in agg:
        ids.add(pre)
        ids.add(post)
    id_map = f2c.remap_ids(ids)
    n = len(id_map)
    lines = [f"{id_map[a]},{id_map[b]},{w}" for (a, b), w in agg.items()]
    expected = parse_csr(lines, n=n)

    csr, _, stats = f2c.build_csr(FEATHER, limit_rows=SLICE)
    assert csr.row_ptr == expected.row_ptr
    assert csr.col_idx == expected.col_idx
    assert csr.weight == expected.weight
    assert stats["n_edges_agregadas"] == len(agg)


def test_slice_csr_invariants():
    """Invariantes byte-level da spec sobre o CSR do slice real."""
    csr, _, stats = f2c.build_csr(FEATHER, limit_rows=SLICE)
    assert all(a <= b for a, b in zip(csr.row_ptr, csr.row_ptr[1:]))
    assert csr.row_ptr[0] == 0
    assert csr.row_ptr[-1] == len(csr.col_idx) == len(csr.weight)
    assert all(0 <= c < stats["n_neuronios"] for c in csr.col_idx)
    assert all(w > 0 for w in csr.weight)
    for pre in range(min(50, stats["n_neuronios"])):
        s, e = csr.row_ptr[pre], csr.row_ptr[pre + 1]
        assert sorted(csr.col_idx[s:e]) == csr.col_idx[s:e]


def test_multiedge_aggregation_sums_weights():
    """Pares repetidos agregam somando pesos (proteina do conectoma)."""
    agg = f2c.aggregate_triples([(5, 7, 2), (5, 7, 3), (5, 8, 1)])
    assert agg == {(5, 7): 5, (5, 8): 1}
def test_body_id_threshold_separates_sites():
    """Limiar 500k separa corpos de sites; batch 0 real tem ambas populacoes."""
    assert f2c.is_body_id(10_001) is True
    assert f2c.is_body_id(499_999) is True
    assert f2c.is_body_id(500_000) is False
    assert f2c.is_body_id(1_571_863_634) is False
    batch = f2c.open_reader(FEATHER).get_batch(0)
    pre = batch.column("body_pre").to_pylist()
    assert any(f2c.is_body_id(int(x)) for x in pre)
    assert any(not f2c.is_body_id(int(x)) for x in pre)
