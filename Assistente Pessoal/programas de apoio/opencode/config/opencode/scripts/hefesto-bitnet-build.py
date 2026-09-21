#!/usr/bin/env python3
"""Fila de build bitnet.cpp: espera acalmar -> cmake build throttled -> smoke.
Gate: load1 < 8.0 em 3 checagens seguidas (60s). Teto: 6h (parqueia).
Build: cmake -B build + --build -j8 sob nice -n 19 (limita impacto na produção).
Smokes: binário existe + --version roda. Resultado: DONE marker + log.
NÃO serve modelo nem baixa nada (downloads fora). Modo autonomo ON.
Forja: Gran-Mestre/Hefesto 2026-09-07.
"""
import os
import subprocess
import time

SRC = "/tmp/opencode/hefesto/bitnet.cpp"
LOG = "/tmp/opencode/hefesto-build.log"
DONE = "/tmp/opencode/hefesto-build.done"


def log(m):
    with open(LOG, "a") as f:
        f.write(f"{time.strftime('%FT%TZ', time.gmtime())} {m}\n")


def load1():
    with open("/proc/loadavg") as f:
        return float(f.read().split()[0])


def main():
    t_end = time.time() + 6 * 3600
    while time.time() < t_end:
        try:
            ok = all((lambda: (time.sleep(60), load1() < 8.0)[1])() for _ in range(3))
        except Exception:  # noqa: BLE001
            ok = False
        if ok:
            break
        time.sleep(60)
    else:
        open(DONE, "w").write("PARKED-sem-janela")
        return
    log("JANELA-CALMA: iniciando cmake configure+build -j8 nice19")
    r1 = subprocess.run(
        ["nice", "-n", "19", "cmake", "-S", SRC, "-B", SRC + "/build",
         "-DCMAKE_BUILD_TYPE=Release"],
        capture_output=True, text=True, timeout=1800)
    log(f"configure exit={r1.returncode} tail={r1.stderr[-300:]}")
    if r1.returncode != 0:
        open(DONE, "w").write("FAIL-configure")
        return
    r2 = subprocess.run(
        ["nice", "-n", "19", "cmake", "--build", SRC + "/build", "-j", "8"],
        capture_output=True, text=True, timeout=5 * 3600)
    log(f"build exit={r2.returncode} tail={r2.stderr[-300:]}")
    if r2.returncode != 0:
        open(DONE, "w").write("FAIL-build")
        return
    srv = SRC + "/build/bin/llama-server"
    ok = os.path.exists(srv)
    if ok:
        r3 = subprocess.run([srv, "--version"], capture_output=True,
                            text=True, timeout=120)
        ok = r3.returncode == 0
        log(f"smoke version exit={r3.returncode} out={r3.stdout[:150]}")
    open(DONE, "w").write("DONE" if ok else "FAIL-smoke")


if __name__ == "__main__":
    main()
