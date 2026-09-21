#!/usr/bin/env python3
"""Bench de custo de contexto empirico (R55): VRAM real com 2 ctx -> KV por token.

Para cada modelo: sobe com ctx A (8192) e ctx B (16384), mede VRAM pos-load.
KV real por token = (VRAM_B - VRAM_A) / (ctx_B - ctx_A).
Projeta ctx max na MI50 (16368 MiB) com folga 0.45 GB.

Uso: python3 ctx-cost.py --models "a.gguf,b.gguf" [--ctx-a 8192] [--ctx-b 16384]
"""
import argparse, json, os, re, subprocess, sys, time, urllib.request

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = "/mnt/dados/Assistente Pessoal/modelos LLM"
LLAMA_GPU = "/home/johncoffee/llama.cpp/build/bin/llama-server"

def run(cmd, timeout=120):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip()

def drop_caches(sudo_pass):
    if sudo_pass:
        run(f'echo "{sudo_pass}" | sudo -S sh -c \'sync && echo 3 > /proc/sys/vm/drop_caches\' 2>/dev/null')
    else:
        run("sudo -n sh -c 'sync && echo 3 > /proc/sys/vm/drop_caches'", check=False)

def vram_used():
    r = run("rocm-smi --showmeminfo vram 2>/dev/null | grep -i 'Total Used'")
    m = re.search(r":\s*(\d+)", r)
    return round(int(m.group(1)) / 1e9, 2) if m else 0.0

def wait_health(port, tries=50, delay=5):
    for _ in range(tries):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=2) as h:
                if '"status":"ok"' in h.read().decode():
                    return True
        except Exception:
            pass
        time.sleep(delay)
    return False

def stop():
    """R55/R19: derruba backend COMPLETAMENTE e verifica a morte (zero absoluto)."""
    run("pkill -x llama-server")
    time.sleep(5)
    for _ in range(6):
        if not run("pgrep -x llama-server"):
            return True
        run("pkill -9 -x llama-server")  # SIGKILL residual (emergência R19)
        time.sleep(3)
    return False

def baseline(sudo_pass):
    """Zero absoluto: backend morto + drop_caches + telemetria de partida."""
    stop()
    drop_caches(sudo_pass)
    ram = run("free -g | awk 'NR==2{print $3\"/\"$2}'")
    vram = vram_used()
    return ram, vram

def load_vram(model, ctx, mtp, port=8089):
    """Sobe o modelo e retorna a VRAM usada pos-load."""
    path = os.path.join(MODELS_DIR, model)
    cmd = [LLAMA_GPU, "-m", path, "--port", str(port), "--host", "127.0.0.1",
           "--no-webui", "-c", str(ctx), "-t", "18", "-ngl", "99",
           "--cache-type-k", "q4_0", "--cache-type-v", "q4_0", "-np", "1"]
    if mtp:
        cmd += ["--spec-type", "draft-mtp", "--spec-draft-n-max", "3"]
    log = open(os.path.join(SKILL_DIR, "results", f"ctxcost-{model.split('.')[0]}-{ctx}.log"), "w")
    subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    if not wait_health(port, tries=50):
        print(f"  [ERRO] {model} ctx={ctx}: health falhou")
        return None
    time.sleep(3)
    v = vram_used()
    return v

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", required=True, help="lista separada por virgula")
    ap.add_argument("--ctx-a", type=int, default=8192)
    ap.add_argument("--ctx-b", type=int, default=16384)
    ap.add_argument("--sudo-pass", default=None)
    args = ap.parse_args()

    models = [m.strip() for m in args.models.split(",")]
    out = []
    print(f"[R55] bench custo de contexto — ctx {args.ctx_a} vs {args.ctx_b}, MI50 17.2GB\n")
    for model in models:
        wgb = round(os.path.getsize(os.path.join(MODELS_DIR, model)) / 1e9, 2)
        mtp = model.startswith("Qwen3.8-")
        print(f"[{model}]")
        ram0, vram0 = baseline(args.sudo_pass)
        print(f"  [R55 baseline] RAM {ram0} | VRAM {vram0} GB (zero absoluto)")
        va = load_vram(model, args.ctx_a, mtp)
        if va is None:
            out.append({"file": model, "erro": "load falhou"})
            continue
        ram0, vram0 = baseline(args.sudo_pass)
        print(f"  [R55 baseline] RAM {ram0} | VRAM {vram0} GB (zero absoluto)")
        vb = load_vram(model, args.ctx_b, mtp)
        if vb is None:
            out.append({"file": model, "erro": "load falhou"})
            continue
        dctx = args.ctx_b - args.ctx_a
        dv = vb - va
        kv_per_tok = dv * 1e9 / dctx
        mb1k = round(kv_per_tok * 1024 / 1e6, 2)
        overhead = round(va - (wgb + kv_per_tok * args.ctx_a / 1e9), 2)
        ctx_max = int((15.98 - wgb - 0.45) * 1e9 / kv_per_tok) if kv_per_tok > 0 else 0
        print(f"  ctx {args.ctx_a}: VRAM {va} GB | ctx {args.ctx_b}: VRAM {vb} GB")
        print(f"  KV real: {mb1k} MB/1k tok | overhead fixo: {overhead} GB | pesos: {wgb} GB")
        print(f"  ctx MAX MI50: {ctx_max} | projecao 32K: {round(wgb + kv_per_tok*32768/1e9 + overhead, 2)} GB")
        out.append({"file": model, "weights_gb": wgb, "vram_8k": va, "vram_16k": vb,
                    "kv_mb_per_1k_empirico": mb1k, "overhead_gb": overhead,
                    "ctx_max_mi50": ctx_max})
        stop()
    os.makedirs(os.path.join(SKILL_DIR, "results"), exist_ok=True)
    json.dump(out, open(os.path.join(SKILL_DIR, "results", "ctx-cost.json"), "w"), indent=2)
    print(f"\n[save] results/ctx-cost.json")

if __name__ == "__main__":
    main()
