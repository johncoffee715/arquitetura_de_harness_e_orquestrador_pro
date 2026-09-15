"""Daemon vault->cerebro (Wave 5): polling reativo sobre o vault.

Polling 2s por .md novos/editados via mtime em memoria (stdlib, sem deps).
Nao reutiliza watcher.py integralmente: debounce temporal (3s) + taxa
maxima (1 episodio/10s) + fila max 5 exigem camada propria; coupling com
live_loop.py restrito a consumir LiveLoop (lazy, <10 linhas).
Cada episodio roda LiveLoop existente e faz append em JSONL.
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import sys
import time
from pathlib import Path

SNN_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_VAULT = os.path.abspath(os.path.join(SNN_DIR, "..", "cerebro com IA"))
DEFAULT_JSONL = os.path.join(SNN_DIR, "data", "daemon_episodes.jsonl")

POLL_INTERVAL = 2.0
DEBOUNCE_S = 3.0
MIN_INTERVAL_S = 10.0
MAX_QUEUE = 5
MAX_NOTAS_POR_SCAN = 50
GRACE_S = 3600.0  # 1a varredura: ignora .md antigos (baseline); so' novos disparam


class DaemonVault:
    """Polling reativo vault->SNN com debounce, taxa maxima e fila limitada."""

    def __init__(self, vault_root=DEFAULT_VAULT, jsonl_path=DEFAULT_JSONL,
                 loop_factory=None, poll_interval=POLL_INTERVAL,
                 debounce_s=DEBOUNCE_S, min_interval_s=MIN_INTERVAL_S,
                 max_queue=MAX_QUEUE, max_notas_por_scan=MAX_NOTAS_POR_SCAN,
                 grace_s=GRACE_S, time_fn=None, sleep_fn=None, log_fn=None):
        self.vault_root = Path(vault_root)
        self.jsonl_path = str(jsonl_path)
        self.loop_factory = loop_factory
        self.poll_interval = poll_interval
        self.debounce_s = debounce_s
        self.min_interval_s = min_interval_s
        self.max_queue = max_queue
        self.max_notas_por_scan = max_notas_por_scan
        self.grace_s = grace_s
        self.time_fn = time_fn or time.monotonic
        self.sleep_fn = sleep_fn or time.sleep
        self.logs: list = []
        self.log_fn = log_fn or (lambda m: (self.logs.append(m), print(m)))
        self._seen: dict = {}       # path -> mtime (baseline em memoria)
        self._last_emit: dict = {}  # path -> monotonic ts do ultimo episodio
        self._pending: dict = {}    # path -> mtime mais recente colapsado
        self._queue: list = []
        self._last_run_ts = None
        self._stop = False
        self.dropped = 0
        self._loop = None
        self._boot_wall = time.time()
        self._load_seen_from_jsonl()

    # -- estado persistido (idempotencia) --
    def _load_seen_from_jsonl(self):
        try:
            if not os.path.exists(self.jsonl_path):
                return
            with open(self.jsonl_path, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        e = json.loads(line)
                    except Exception:
                        continue
                    nota, mt = e.get("nota"), e.get("mtime")
                    if isinstance(nota, str) and isinstance(mt, (int, float)):
                        if mt > self._seen.get(nota, -1):
                            self._seen[nota] = float(mt)
        except Exception:
            pass

    # -- scan --
    def _scan_files(self):
        found = []
        if not self.vault_root.exists():
            return found
        for p in self.vault_root.rglob("*"):
            if p.is_file() and p.name.endswith(".md"):
                try:
                    found.append((str(p), p.stat().st_mtime))
                except OSError:
                    continue
        found.sort(key=lambda t: t[1])
        return found

    @staticmethod
    def _is_self_episode_only(path: str) -> bool:
        """True se o diff recente da nota e' SO' bloco snn-episode (anti-loop).

        Stateless: compara o body_hash atual (conteudo SEM episodios) com o
        hash registrado no ultimo marcador '<!-- snn-episode body_hash=H'.
        Iguais => a unica mudanca foi o write-back do proprio cerebro.
        Edicao do usuario apos o bloco => hashes diferem => processa.
        """
        import re
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except OSError:
            return False
        if "<!-- snn-episode" not in text:
            return False
        try:
            sys.path.insert(0, SNN_DIR)
            from live_loop import LiveLoop
            cur = LiveLoop.body_hash(text)
        except Exception:
            import hashlib
            stripped = re.sub(r"^## Cérebro \(episódio.*?"
                              r"<!-- snn-episode[^\n]*\n?", text,
                              flags=re.M | re.S)
            cur = hashlib.sha1(stripped.strip().encode("utf-8")).hexdigest()
        tails = re.findall(r"<!-- snn-episode\s+body_hash=(\w+)", text)
        return bool(tails) and tails[-1] == cur

    def scan(self):
        """Uma varredura: devolve lista de notas novas/editadas pos-debounce."""
        now = self.time_fn()
        cand = []
        for path, mtime in self._scan_files():
            base = self._seen.get(path)
            if base is not None and mtime <= base:
                continue  # sem mudanca
            if base is not None and self._is_self_episode_only(path):
                self._seen[path] = mtime  # eco cerebelar: consome sem reentrar
                continue
            if base is None and mtime < self._boot_wall - self.grace_s:
                self._seen[path] = mtime  # baseline: .md antigo, nao dispara
                continue
            last = self._last_emit.get(path)
            if last is not None and (now - last) < self.debounce_s:
                self._pending[path] = mtime  # rajada colapsa: guarda o mais novo
                continue
            if path in self._pending and (now - last if last else 1e9) < self.debounce_s:
                continue
            cand.append((mtime, path))
        # promove pendentes cuja janela expirou (1 por path)
        for path, mtime in list(self._pending.items()):
            last = self._last_emit.get(path)
            if last is None or (now - last) >= self.debounce_s:
                if all(p != path for _, p in cand):
                    cand.append((mtime, path))
                del self._pending[path]
        cand.sort(key=lambda t: t[0])
        return [p for _, p in cand[:self.max_notas_por_scan]]

    # -- fila --
    def enqueue(self, paths):
        for p in paths:
            self._queue.append(p)
            if len(self._queue) > self.max_queue:
                drop = self._queue.pop(0)
                self.dropped += 1
                self.log_fn(f"daemon_vault: fila cheia, descartado {drop}")

    # -- episodio --
    def _get_loop(self):
        if self.loop_factory is not None:
            return self.loop_factory()
        if self._loop is None:
            sys.path.insert(0, SNN_DIR)
            from live_loop import LiveLoop  # consumo pontual (<10 linhas)
            self._loop = LiveLoop.from_feather(limit_rows=5000)
        return self._loop

    def _append(self, entry):
        d = os.path.dirname(self.jsonl_path)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(self.jsonl_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def flush(self):
        try:
            if os.path.exists(self.jsonl_path):
                with open(self.jsonl_path, "a", encoding="utf-8") as fh:
                    fh.flush()
                    try:
                        os.fsync(fh.fileno())
                    except Exception:
                        pass
        except Exception:
            pass

    def run_episode(self, note_path):
        now = self.time_fn()
        if self._last_run_ts is not None:
            wait = self.min_interval_s - (now - self._last_run_ts)
            if wait > 0:
                self.sleep_fn(wait)
                now = self.time_fn()
        try:
            mtime = os.stat(note_path).st_mtime
        except OSError:
            mtime = self._boot_wall
        try:
            out = self._get_loop().run(note_path)
        except Exception as exc:
            out = {"exit_status": "failed", "error": repr(exc)}
        entry = {"ts": time.time(), "nota": note_path, "mtime": mtime,
                 "decisao": out.get("decision", out.get("exit_status", "?")),
                 "spikes": ((out.get("activity") or {}).get("total_spikes", 0)
                            if isinstance(out.get("activity"), dict) else 0),
                 "exit_status": out.get("exit_status", "?")}
        self._append(entry)
        self._seen[note_path] = mtime
        self._last_emit[note_path] = self.time_fn()
        self._last_run_ts = self.time_fn()
        return entry

    def scan_and_run_once(self):
        new = self.scan()
        self.enqueue(new)
        n = 0
        while self._queue and not self._stop:
            self.run_episode(self._queue.pop(0))
            n += 1
        return n

    # -- sinais --
    def request_stop(self, signum=None, frame=None):
        self._stop = True
        self.flush()

    def run_forever(self):
        signal.signal(signal.SIGINT, self.request_stop)
        signal.signal(signal.SIGTERM, self.request_stop)
        while not self._stop:
            self.scan_and_run_once()
            if self._stop:
                break
            self.sleep_fn(self.poll_interval)
        self.flush()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--vault-root", default=DEFAULT_VAULT)
    ap.add_argument("--jsonl", default=DEFAULT_JSONL)
    a = ap.parse_args(argv)
    d = DaemonVault(vault_root=a.vault_root, jsonl_path=a.jsonl)
    if a.once:
        n = d.scan_and_run_once()
        print(f"daemon_vault --once: {n} episodio(s), exit_status ok")
        return 0
    d.run_forever()
    print("daemon_vault: parada limpa, exit_status ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
