import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from csr import parse_csv_to_csr


def test_toy_consistency():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mini_edges.csv")
    row_ptr, col_idx, weight = parse_csv_to_csr(path)

    # N = 4 neurônios (0..3), E_agregado = 5 arestas
    assert len(row_ptr) == 5, f"row_ptr deve ter N+1=5, tem {len(row_ptr)}"
    assert row_ptr[0] == 0
    assert row_ptr[4] == len(col_idx) == len(weight) == 5

    # monotônico não-decrescente
    assert all(row_ptr[i] <= row_ptr[i + 1] for i in range(4))

    # col_idx em [0, N), weight > 0
    assert all(0 <= c < 4 for c in col_idx)
    assert all(w > 0 for w in weight)

    # grau de saída por neurônio: 0->2, 1->1, 2->2, 3->0
    assert row_ptr[1] - row_ptr[0] == 2
    assert row_ptr[2] - row_ptr[1] == 1
    assert row_ptr[3] - row_ptr[2] == 2
    assert row_ptr[4] - row_ptr[3] == 0

    # ordenação por (pre, post): vizinhos de 0 = [1, 2]
    assert col_idx[row_ptr[0]:row_ptr[1]] == [1, 2]
    assert weight[row_ptr[0]:row_ptr[1]] == [2, 1]