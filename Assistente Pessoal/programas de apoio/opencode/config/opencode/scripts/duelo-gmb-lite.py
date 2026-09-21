#!/usr/bin/env python3
"""Duelo GMB-lite adiado: espera acalmar e roda bateria 6+6 (Ornith :9096 x Qwen :8083).
Gatilho: load1 < 6.0 E tiny-probe no 8083 < 25s. Teto: 4h (depois parqueia).
Saída: /tmp/opencode/duelo-gmb-lite.jsonl + DONE marker. Sem julgamento (scoring posterior).
Forja: Gran-Mestre 2026-09-07, modo autonomo ON. R91: 2 amostras só na faixa cinza
(aqui 1 amostra por task por slot; re-challenge sob disputa).
"""
import json
import subprocess
import time
import os

TASKS = [
    ("T1-logica", "Se todos os Zorks sao Blips e alguns Blips voam, o que se pode concluir com certeza? Responda em 2 frases."),
    ("T2-falha", "Point out the flaw in one sentence: All cats are mammals, Whiskers is a mammal, therefore Whiskers is a cat."),
    ("T4-mat", "Um trem a 120km/h parte as 14h; outro a 80km/h parte as 15h, trajeto 400km. Quem chega primeiro e com que diferenca? Mostre contas."),
    ("T6-toolcall", 'Extract JSON with keys capital and country from: Paris is the capital of France. Reply ONLY with the JSON.'),
    ("T8-plano", "Write a 4-step test plan (headers only) for: login com OAuth2 quebrou apos deploy. Seja especifico."),
    ("T10-refuta", "Refute em 2 frases: 'Modelo maior sempre vence porque tem mais parametros.'"),
]
PAY = {"n_predict": 250, "temperature": 0.6, "top_p": 0.95, "top_k": 20}
OUT = "/tmp/opencode/duelo-gmb-lite.jsonl"
DONE = "/tmp/opencode/duelo-gmb-lite.done"


def load1():
    with open("/proc/loadavg") as f:
        return float(f.read().split()[0])


def probe(port, prompt, timeout=120):
    body = dict(PAY, prompt=prompt)
    t0 = time.time()
    try:
        r = subprocess.run(
            ["curl", "-s", "-m", str(timeout), "-X", "POST",
             f"http://127.0.0.1:{port}/completion",
             "-H", "Content-Type: application/json",
             "-d", json.dumps(body)],
            capture_output=True, text=True, timeout=timeout + 10)
        wall = (time.time() - t0) * 1000
        d = json.loads(r.stdout)
        return {"wall_ms": round(wall), "timings": d.get("timings", {}),
                "content": d.get("content", ""), "ok": True}
    except Exception as e:  # noqa: BLE001
        return {"wall_ms": -1, "error": str(e)[:100], "ok": False}


def calm():
    try:
        if load1() >= 6.0:
            return False
        r = probe(8083, "hi", timeout=25)
        return r["ok"] and r["wall_ms"] < 25000
    except Exception:  # noqa: BLE001
        return False


def main():
    t_end = time.time() + 4 * 3600
    while time.time() < t_end:
        if calm():
            break
        time.sleep(60)
    else:
        open(DONE, "w").write("PARKED-sem-janela-calma")
        return
    if os.path.exists(OUT):
        os.remove(OUT)
    with open(OUT, "w") as fh:
        for tid, prompt in TASKS:
            for slot in (9096, 8083):
                r = probe(slot, prompt)
                fh.write(json.dumps({"task": tid, "slot": slot,
                                     "prompt": prompt, **r},
                                    ensure_ascii=False) + "\n")
                fh.flush()
    open(DONE, "w").write("DONE")


if __name__ == "__main__":
    main()
