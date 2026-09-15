"""Feather -> CSR do conectoma real (streaming, sem tabela inteira em RAM).

Caminho: connectome-weights.feather (Arrow IPC, magic ARROW1,
colunas body_pre/body_post/weight) --lido por record-batches-->
triples -> agregacao multiedge (soma por par) -> remap denso ->
``parser.parse_csr`` (consumido, NAO modificado).

RAM limitada a O(pares_unicos_do_slice + neuronios_distintos):
o arquivo NUNCA e carregado inteiro; cada batch (~65k linhas) e
processado e descartado. IDs body_* sao esparsos (ex.: ate 1.5B),
por isso ha remap para indices densos 0..N-1 antes do parse_csr.

Uso:
    snn/.venv/bin/python snn/feather_to_csr.py [PATH] [--build-rows K]
"""

from __future__ import annotations

import argparse
import inspect
import resource
import sys
import time

import pyarrow.compute as pc
import pyarrow.ipc as ipc

from parser import parse_csr

COLUMNS = ("body_pre", "body_post", "weight")

# Auditoria 2026-09-14: corpos <500k (uniao 169.736 ~= canonico 166.691); sites ate 1.57B.
BODY_ID_MAX = 500_000


def is_body_id(i: int) -> bool:
    return i < BODY_ID_MAX


def open_reader(path: str):
    """Abre o feather como RecordBatchFileReader (streaming por batches)."""
    return ipc.open_file(path)


def iter_triples(path: str, limit_rows: int | None = None):
    """Gera (pre, post, weight) batch a batch; nunca monta a tabela inteira.

    Generator function: cada batch e convertido, iterado e descartado.
    """
    reader = open_reader(path)
    yielded = 0
    for i in range(reader.num_record_batches):
        batch = reader.get_batch(i)
        pre = batch.column("body_pre").to_pylist()
        post = batch.column("body_post").to_pylist()
        w = batch.column("weight").to_pylist()
        for a, b, c in zip(pre, post, w):
            if limit_rows is not None and yielded >= limit_rows:
                return
            yield (int(a), int(b), int(c))
            yielded += 1


def aggregate_triples(triples) -> dict[tuple[int, int], int]:
    """Agrega multiedges somando pesos por par (pre, post). Funcao pura."""
    agg: dict[tuple[int, int], int] = {}
    for pre, post, w in triples:
        key = (pre, post)
        agg[key] = agg.get(key, 0) + w
    return agg


def remap_ids(ids) -> dict[int, int]:
    """Mapeia IDs esparsos body_* -> indices densos 0..N-1 (ordem crescente)."""
    return {body_id: idx for idx, body_id in enumerate(sorted(ids))}


def build_csr(path: str, limit_rows: int = 100_000):
    """Constroi Csr via parser existente sobre um slice limitado (streaming).

    Returns:
        (csr, id_map, stats) onde stats tem total_rows, n_neuronios,
        n_edges_agregadas.
    """
    agg = aggregate_triples(iter_triples(path, limit_rows=limit_rows))
    ids: set[int] = set()
    for pre, post in agg:
        ids.add(pre)
        ids.add(post)
    id_map = remap_ids(ids)
    n = len(id_map)
    lines = (
        f"{id_map[pre]},{id_map[post]},{w}" for (pre, post), w in agg.items()
    )
    csr = parse_csr(lines, n=n)
    stats = {
        "total_rows": limit_rows,
        "n_neuronios": n,
        "n_edges_agregadas": len(agg),
    }
    return csr, id_map, stats


def stream_stats(path: str) -> dict:
    """Passada streaming COMPLETA (todos os batches) com RAM limitada.

    Usa kernels C++ (pyarrow.compute) por batch; o Python so acumula o
    conjunto de neuronios distintos (~1e5) e escalares. Retorna metricas.
    """
    reader = open_reader(path)
    t0 = time.perf_counter()
    total_rows = 0
    weight_sum = 0
    gmin: int | None = None
    gmax = 0
    neurons: set[int] = set()
    for i in range(reader.num_record_batches):
        batch = reader.get_batch(i)
        total_rows += batch.num_rows
        c_pre = batch.column("body_pre")
        c_post = batch.column("body_post")
        mm_pre = pc.min_max(c_pre).as_py()
        mm_post = pc.min_max(c_post).as_py()
        lo = min(mm_pre["min"], mm_post["min"])
        hi = max(mm_pre["max"], mm_post["max"])
        gmin = lo if gmin is None else min(gmin, lo)
        gmax = max(gmax, hi)
        weight_sum += pc.sum(batch.column("weight")).as_py()
        neurons.update(x for x in pc.unique(c_pre).to_pylist() if is_body_id(x))
        neurons.update(x for x in pc.unique(c_post).to_pylist() if is_body_id(x))
    elapsed = time.perf_counter() - t0
    peak_mb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    return {
        "num_batches": reader.num_record_batches,
        "total_rows": total_rows,
        "n_neuronios": len(neurons),
        "id_min": gmin,
        "id_max": gmax,
        "weight_sum": weight_sum,
        "elapsed_s": round(elapsed, 1),
        "peak_rss_mb": round(peak_mb, 1),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Feather -> CSR streaming.")
    ap.add_argument("path", nargs="?",
                    default="snn/data/connectome-weights.feather")
    ap.add_argument("--build-rows", type=int, default=100_000,
                    help="linhas p/ construir CSR demo via parse_csr")
    args = ap.parse_args(argv)

    stats = stream_stats(args.path)
    print(f"dataset: {args.path}")
    print(f"batches: {stats['num_batches']}")
    print(f"total_rows: {stats['total_rows']}")
    print(f"n_neuronios_distintos: {stats['n_neuronios']}")
    print(f"id_min/max: {stats['id_min']}/{stats['id_max']}")
    print(f"stream_time_s: {stats['elapsed_s']}")
    print(f"peak_rss_mb: {stats['peak_rss_mb']}")

    t0 = time.perf_counter()
    csr, _, bstats = build_csr(args.path, limit_rows=args.build_rows)
    dt = time.perf_counter() - t0
    assert csr.row_ptr[-1] == len(csr.col_idx) == len(csr.weight)
    print(f"csr_slice_rows={args.build_rows} "
          f"n={bstats['n_neuronios']} E_agreg={bstats['n_edges_agregadas']} "
          f"build_s={dt:.1f}")
    print("exit_status=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
