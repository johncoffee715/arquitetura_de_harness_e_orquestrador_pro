"""Anatomia real body_id -> regiao (Wave 6, bug B2).

Substitui o ``i % 4`` fake de ``live_loop.simulate`` por regioes
anatomicas derivadas da tabela oficial FlyEM Male-CNS v1.0
``body-annotations-*-minconf-0.5.feather`` (211.577 linhas, 14.4MB,
colunas bodyId/type/hemibrainType/superclass entre outras).

Regras (ordens importam; prefixos sobre type + hemibrainType):
  MB     — corpo fungiforme: KC*, MBON*, DAN*, PPL*, MB-*
  CX     — complexo central: EPG, PEG, PEN*, PFN*, PFP*, PFL*, PFR*,
           FB*, EB*, PB*, NO*/LNO*, ExR*, hDelta*, EPGt*, PFGs*, SFS*
  OL     — lobo optico: superclass == 'ol_intrinsic' ou prefixos
           Tm*, Mi*, T4*, T5*, L1-L5, C2/C3, Dm*, Sm*, Lawf*, Am*, Pm*
  VNC    — cordao nervoso ventral: superclass vnc*/ascending/descending
           ou prefixos DN*, DNg*, DNp*, DNge*, DNpe*, DDN*, HS*, VS*
  CB     — cerebro central residual: superclass == 'cb_intrinsic'
  outros — sem anotacao ou sem prefixo conhecido

Sem o feather (download >20MB = fail-closed): region_of cai para o
fallback ``'outros'`` — reportado como blocked parcial, nunca inventado.
Carga unica (<15MB) com medida de RAM (resource.ru_maxrss delta).
"""

from __future__ import annotations

import os
import resource

ANNOT_FEATHER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "data", "body-annotations.feather")

MARKER = "<!-- snn-episode"

MB_PREFIXES = ("KC", "MBON", "DAN", "PPL", "MB-", "MB_")
CX_PREFIXES = ("EPG", "PEG", "PEN", "PFN", "PFP", "PFL", "PFR", "PFG",
               "FB", "EB", "PB", "LNO", "LCNO", "ExR", "hDelta",
               "EPGt", "SFS", "NO")
CX_EXACT = {"EPG", "PEG", "FB", "EB", "PB", "NO", "SFS"}
OL_PREFIXES = ("Tm", "Mi", "T4", "T5", "Dm", "Sm", "Lawf", "Am", "Pm",
               "L1", "L2", "L3", "L4", "L5", "C2", "C3")
VNC_PREFIXES = ("DN", "DDN", "HS", "VS", "VNC", "AN0", "AN1")

_CACHE: dict = {}          # body_id -> (type, hemi, superclass)
_META: dict = {}           # n_rows, n_mapped, cols, ram_mb, path


def _rss_mb() -> float:
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def _starts_any(s: str, prefixes) -> bool:
    return bool(s) and s.split("(")[0].split(",")[0].strip() != "" and \
        any(s.startswith(p) for p in prefixes)


def classify(type_s: str | None, hemi_s: str | None = None,
             superclass_s: str | None = None) -> str:
    """Classifica (type, hemibrainType, superclass) -> regiao. Pura."""
    t = (type_s or "").strip()
    h = (hemi_s or "").strip()
    first_hemi = h.split(",")[0].strip() if h else ""
    for cand in (t, first_hemi):
        if not cand:
            continue
        if _starts_any(cand, MB_PREFIXES):
            return "MB"
        if cand in CX_EXACT or _starts_any(cand, CX_PREFIXES):
            return "CX"
    sup = (superclass_s or "").strip()
    if sup == "ol_intrinsic" or _starts_any(t, OL_PREFIXES):
        return "OL"
    if sup.startswith(("vnc", "ascending", "descending", "sensory_ascending")) \
            or _starts_any(t, VNC_PREFIXES):
        return "VNC"
    if sup == "cb_intrinsic":
        return "CB"
    return "outros"


def load_annotations(path: str = ANNOT_FEATHER) -> dict:
    """Carga unica do feather de anotacoes; idempotente. Retorna _META."""
    if _CACHE and _META.get("path") == path:
        return _META
    _CACHE.clear()
    _META.clear()
    if not os.path.exists(path):
        _META.update({"path": path, "n_rows": 0, "n_mapped": 0,
                      "cols": [], "ram_mb": 0.0, "loaded": False})
        return _META
    import pyarrow.ipc as ipc  # import tardio: modulo puro sem pyarrow
    before = _rss_mb()
    reader = ipc.open_file(path)
    cols = reader.schema.names
    n_rows = 0
    for i in range(reader.num_record_batches):
        b = reader.get_batch(i)
        n_rows += b.num_rows
        bids = b.column("bodyId").to_pylist()
        ty = b.column("type").to_pylist() if "type" in cols else [None] * len(bids)
        hb = b.column("hemibrainType").to_pylist() if "hemibrainType" in cols else [None] * len(bids)
        sc = b.column("superclass").to_pylist() if "superclass" in cols else [None] * len(bids)
        for d, t, h, s in zip(bids, ty, hb, sc):
            try:
                _CACHE[int(d)] = (t, h, s)
            except (TypeError, ValueError):
                continue
    _META.update({"path": path, "n_rows": n_rows, "n_mapped": len(_CACHE),
                  "cols": cols, "ram_mb": round(_rss_mb() - before, 1),
                  "loaded": True})
    return _META


def region_of(body_id) -> str:
    """body_id (int|str) -> regiao anatomica. Desconhecido => 'outros'."""
    try:
        bid = int(body_id)
    except (TypeError, ValueError):
        return "outros"
    if not _CACHE:
        load_annotations()
    if not _CACHE:  # fail-closed: sem feather, sem invencao
        return "outros"
    rec = _CACHE.get(bid)
    if rec is None:
        return "outros"
    return classify(*rec)
