"""Teste da ponte inotify→LLM — Task 4.3 (RED→GREEN).

Cobre os três critérios categóricos do plano (R28):
  1. Debounce: rajada de N eventos colapsa em 1 evento pós-debounce.
  2. Backpressure: fila limitada não estoura; descarte-mais-antigo é contabilizado.
  3. Roteamento: mudança de .md roteia à categoria certa (mock, sem socket/HTTP).

Sem chamadas reais a endpoints/sockets. Sem dependências externas.
"""

from __future__ import annotations

import os
import time
from pathlib import Path

from router import Router, route_event
from watcher import VaultWatcher


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _touch(path: Path, content: str = "x") -> None:
    """Escreve `content` em `path`, garantindo mtime novo (polling por mtime)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    # força mtime estritamente maior que o snapshot anterior
    os.utime(path, (time.time() + 0.01, time.time() + 0.01))


# ---------------------------------------------------------------------------
# 1) Debounce: rajada colapsa em 1 evento
# ---------------------------------------------------------------------------

def test_rajada_colapsa_em_um_evento(tmp_path):
    """N mudanças rápidas no mesmo .md → 1 evento pós-debounce."""
    target = tmp_path / "nota.md"
    _touch(target, "v0")

    watcher = VaultWatcher(root=tmp_path, debounce_s=0.15, max_queue=16)
    watcher.snapshot()  # baseline

    # rajada: N escritas rápidas no mesmo arquivo
    for i in range(1, 6):
        _touch(target, f"v{i}")

    events = watcher.poll()
    # pós-debounce, a rajada inteira colapsa em exatamente 1 evento
    assert len(events) == 1, f"esperado 1 evento, veio {len(events)}"
    assert events[0].path == str(target)


# ---------------------------------------------------------------------------
# 2) Backpressure: fila limitada não estoura, descarte contabilizado
# ---------------------------------------------------------------------------

def test_fila_limitada_descarta_mais_antigo_com_contador(tmp_path):
    """Fila com max_queue pequeno descarta o mais antigo e conta o descarte."""
    watcher = VaultWatcher(root=tmp_path, debounce_s=0.0, max_queue=3)
    watcher.snapshot()

    # 5 arquivos distintos mudam → 5 eventos brutos, fila só comporta 3
    for i in range(5):
        _touch(tmp_path / f"n{i}.md", f"c{i}")

    events = watcher.poll()
    assert len(events) == 3, f"fila deveria reter 3, reteve {len(events)}"
    assert watcher.dropped == 2, f"esperado 2 descartes, veio {watcher.dropped}"
    # descarta-mais-antigo: os 2 primeiros (n0, n1) saem, os 3 últimos ficam
    kept = {Path(e.path).name for e in events}
    assert kept == {"n2.md", "n3.md", "n4.md"}, f"mantidos errados: {kept}"


# ---------------------------------------------------------------------------
# 3) Roteamento por categoria (mock, sem chamada real)
# ---------------------------------------------------------------------------

def test_roteamento_nota_md_para_categoria_correta():
    """Mudança de .md roteia à categoria certa via descritor (sem HTTP)."""
    router = Router()

    # nota markdown → retrieval/validação (Needle :9091)
    d = router.route("nota.md")
    assert d["endpoint"] == "http://127.0.0.1:9091"
    assert d["categoria"] == "retrieval"

    # arquivo de regras → filtro/síntese (RWKV7 :9084)
    d = router.route("regras/R17.md")
    assert d["endpoint"] == "http://127.0.0.1:9084"
    assert d["categoria"] == "sintese"

    # arquivo de pipeline/plano → orquestração (Qwen :8083)
    d = router.route("pipeline/plano.md")
    assert d["endpoint"] == "http://127.0.0.1:8083"
    assert d["categoria"] == "orquestracao"

    # descritor carrega motivo (R75: categoria > nome)
    assert d["motivo"]


def test_route_event_aceita_evento_do_watcher(tmp_path):
    """Integração watcher→router: evento do watcher roteia sem chamada real."""
    target = tmp_path / "nota.md"
    _touch(target, "x")

    watcher = VaultWatcher(root=tmp_path, debounce_s=0.0, max_queue=8)
    watcher.snapshot()
    _touch(target, "y")

    events = watcher.poll()
    assert len(events) == 1

    desc = route_event(events[0])
    assert desc["endpoint"] == "http://127.0.0.1:9091"
    assert desc["categoria"] == "retrieval"