#!/usr/bin/env python3
"""
Watcher gerente (F5) — Bibliotecario (R94). Substitui o watcher legado parado.

inotify via ctypes (sem deps): CLOSE_WRITE/CREATE/MOVED_TO de .md -> upsert com
payloads REAIS (conteudo, mtime, tags via catalogar) + flag vetor_placebo (R96).
ids estaveis md5 (sem duplicata entre restarts). Lock unico, log em /tmp.

Uso: setsid nohup python3 watcher.py > /tmp/opencode/bibliotecario-watcher.out 2>&1 < /dev/null & disown
"""

import ctypes
import ctypes.util
import hashlib
import json
import logging
import os
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from catalogar import extrair_tags  # noqa: E402

VAULT = Path("/mnt/dados/Assistente Pessoal/cerebro com IA")
LOG = Path("/tmp/opencode/bibliotecario-watcher.log")
LOCK = Path("/tmp/bibliotecario-watcher.lock")
QDRANT = "http://localhost:6333/collections/gran_mestre_docs/points"
DIM = 768
EXCLUDE = (".obsidian", ".swp", ".kate-swp", ".git", "node_modules", ".trash", "quarentena")

IN_CLOSE_WRITE = 0x00000008
IN_CREATE = 0x00000100
IN_MOVED_TO = 0x00000080
IN_ISDIR = 0x40000000
IN_NONBLOCK = 0x00000800


def setup_logger():
    LOG.parent.mkdir(parents=True, exist_ok=True)
    l = logging.getLogger("BibliotecarioWatcher2")
    l.setLevel(logging.INFO)
    if not l.handlers:
        h = logging.FileHandler(LOG)
        h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        l.addHandler(h)
    return l


def upsert(path, logger):
    try:
        p = Path(path)
        texto = p.read_text(encoding="utf-8", errors="ignore")
        pid = int(hashlib.md5(path.encode()).hexdigest(), 16) % (2**63)
        body = json.dumps({"points": [{
            "id": pid,
            "vector": [0.0] * DIM,  # PLACEBO (R96) — ver docstring
            "payload": {"path": path, "content": texto[:2000],
                        "mtime": p.stat().st_mtime,
                        "tags": extrair_tags(path),
                        "vetor_placebo": True, "indexado_em": time.time()},
        }]}).encode()
        req = urllib.request.Request(QDRANT, data=body,
                                     headers={"Content-Type": "application/json"},
                                     method="PUT")
        with urllib.request.urlopen(req, timeout=5) as resp:
            logger.info(f"reindexado: {path} -> {resp.status}")
    except Exception as e:
        logger.warning(f"reindex falhou (graceful): {path} — {e}")


def watch(logger):
    libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
    fd = libc.inotify_init1(IN_NONBLOCK)
    if fd < 0:
        raise OSError("inotify_init1 falhou")
    wds = {}
    for root, dirs, _files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE and not d.startswith(".")]
        wd = libc.inotify_add_watch(fd, root.encode(),
                                    IN_CLOSE_WRITE | IN_CREATE | IN_MOVED_TO)
        if wd >= 0:
            wds[wd] = root
    logger.info(f"monitorando {len(wds)} diretorios (inotify, payloads reais)")
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
            fpath = os.path.join(wds.get(wd, str(VAULT)), name)
            if fpath.endswith(".md") and not any(x in fpath for x in EXCLUDE):
                logger.info(f"evento: {fpath}")
                upsert(fpath, logger)


def main():
    if LOCK.exists():
        print("watcher ja rodando (lock existe)")
        return 1
    LOCK.touch()
    logger = setup_logger()
    try:
        logger.info("bibliotecario-watcher v2 iniciado (R94)")
        watch(logger)
    except KeyboardInterrupt:
        logger.info("encerrado")
    finally:
        LOCK.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
