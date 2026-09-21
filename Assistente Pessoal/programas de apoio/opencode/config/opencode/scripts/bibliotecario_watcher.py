#!/usr/bin/env python3
"""
BIBLIOTECARIO WATCHER — Gatilho orientado a eventos (inotify via ctypes).

Monitora o Vault Obsidian; em CLOSE_WRITE de .md → reindexa (Qdrant) + log.
Sem dependência externa (inotify nativo Linux). Idempotente (lock).

Origin: helenizado:hefesto-v1 (R77 3 camadas — skill bibliotecario)
"""

import ctypes
import ctypes.util
import json
import logging
import os
import sys
import time
import urllib.request
from pathlib import Path

VAULT = Path("/mnt/dados/Assistente Pessoal/cerebro com IA")
LOG = Path("/tmp/opencode/bibliotecario-watcher.log")
LOCK = Path("/tmp/bibliotecario-watcher.lock")
QDRANT_URL = "http://localhost:6333/collections/gran_mestre_docs/points"
EXCLUDE = (".obsidian", ".swp", ".kate-swp", ".git", "node_modules", ".trash")

# inotify constants
IN_CLOSE_WRITE = 0x00000008
IN_CREATE = 0x00000100
IN_MOVED_TO = 0x00000080
IN_ISDIR = 0x40000000
IN_NONBLOCK = 0x00000800


def setup_logger() -> logging.Logger:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    l = logging.getLogger("BibliotecarioWatcher")
    l.setLevel(logging.INFO)
    if not l.handlers:
        h = logging.FileHandler(LOG)
        h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        l.addHandler(h)
    return l


def reindexar(path: str, logger: logging.Logger) -> None:
    """Reindexa a nota alterada no Qdrant (graceful — nunca bloqueia)."""
    try:
        content = Path(path).read_text(encoding="utf-8", errors="ignore")[:8000]
        body = json.dumps({
            "points": [{
                "id": abs(hash(path)) % (2**63),
                "vector": [0.0] * 768,  # dim 768 (collection gran_mestre_docs) — embedding real via modelo dedicado
                "payload": {"path": path, "content": content[:2000], "ts": time.time()},
            }]
        }).encode()
        req = urllib.request.Request(
            QDRANT_URL, data=body, headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            logger.info(f"reindexado: {path} → {resp.status}")
    except Exception as e:
        logger.warning(f"reindex falhou (graceful): {path} — {e}")


def watch(logger: logging.Logger) -> None:
    """Loop inotify via ctypes — recursivo sobre o Vault."""
    libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
    fd = libc.inotify_init1(IN_NONBLOCK)
    if fd < 0:
        raise OSError("inotify_init1 falhou")

    wds = {}
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE and not d.startswith(".")]
        wd = libc.inotify_add_watch(fd, root.encode(), IN_CLOSE_WRITE | IN_CREATE | IN_MOVED_TO)
        if wd >= 0:
            wds[wd] = root
    logger.info(f"monitorando {len(wds)} diretórios do Vault (inotify)")

    # struct inotify_event: wd(int) mask(uint32) cookie(uint32) len(uint32) name[]
    buf = ctypes.create_string_buffer(4096)
    while True:
        n = libc.read(fd, buf, 4096)
        if n <= 0:
            time.sleep(0.5)
            continue
        off = 0
        while off < n:
            wd = ctypes.c_int.from_buffer(buf, off).value
            mask = ctypes.c_uint32.from_buffer(buf, off + 4).value
            length = ctypes.c_uint32.from_buffer(buf, off + 12).value
            name = buf.raw[off + 16: off + 16 + length].split(b"\0")[0].decode(errors="ignore")
            off += 16 + length
            if not name or mask & IN_ISDIR:
                continue
            base = wds.get(wd, str(VAULT))
            fpath = os.path.join(base, name)
            if fpath.endswith(".md") and not any(x in fpath for x in EXCLUDE):
                logger.info(f"CLOSE_WRITE: {fpath}")
                reindexar(fpath, logger)


def main() -> int:
    if LOCK.exists():
        print("watcher já rodando (lock existe)")
        return 1
    LOCK.touch()
    logger = setup_logger()
    try:
        logger.info("bibliotecario-watcher iniciado")
        watch(logger)
    except KeyboardInterrupt:
        logger.info("encerrado")
    finally:
        LOCK.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())