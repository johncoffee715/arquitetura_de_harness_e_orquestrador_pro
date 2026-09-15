#!/usr/bin/env python3
"""Throughput isolado (t/s) para qualquer LLM local — llama.cpp (GPU/CPU) ou Ollama.

Mede prefill t/s e decode t/s via endpoint nativo /completion (timings do llama-server).
R55 integrado: derruba backend + drop_caches antes de cada modelo.

Uso:
  python3 throughput.py --model X.gguf --name rotulo [--ctx N] [--gpu] [--mtp N]
                        [--cache-k q4_0] [--cache-v q4_0] [--np 1] [--threads 18]
                        [--sudo-pass 0000] [--backend llama|ollama] [--prompt-tokens 512]

Saída: tabela + JSON em results/throughput-<name>.json
"""
import argparse, json, os, re, subprocess, sys, time, urllib.request

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = "/mnt/dados/Assistente Pessoal/modelos LLM"
LLAMA_GPU = "/home/johncoffee/llama.cpp/build/bin/llama-server"
LLAMA_CPU = "/mnt/dados/llama.cpp-master/build-cpu/bin/llama-server"

def run(cmd, timeout=120):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip()

def drop_caches(sudo_pass):
    if sudo_pass:
        run(f'echo "{sudo_pass}" | sudo -S sh -c \'sync && echo 3 > /proc/sys/vm/drop_caches\' 2>/dev/null')
    else:
        run("sudo -n sh -c 'sync && echo 3 > /proc/sys/vm/drop_caches'")

def get_telemetry():
    ram = run("free -g | awk 'NR==2{print $3\"/\"$2}'")
    vram = run("rocm-smi --showmeminfo vram 2>/dev/null | grep Used")
    vram_gb = "?"
    m = re.search(r"Used.*?(\d+\.?\d*)", vram)
    if m:
        vram_gb = round(float(m.group(1)) / 1e9, 1)
    return ram, vram_gb

def wait_health(port, tries=40, delay=5):
    for _ in range(tries):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=2) as h:
                if '"status":"ok"' in h.read().decode():
                    return True
        except Exception:
            pass
        time.sleep(delay)
    return False

def stop_backend(backend):
    """R55: derruba backend COMPLETAMENTE (SIGTERM -> verifica -> SIGKILL residual)."""
    if backend == "llama":
        run("pkill -x llama-server")
    else:
        run("ollama stop --all 2>/dev/null || true")
    time.sleep(5)
    for _ in range(6):
        if not run("pgrep -x llama-server"):
            return True
        run("pkill -9 -x llama-server")
        time.sleep(3)
    return False

def start_llama(args, port):
    model_path = os.path.join(MODELS_DIR, args.model)
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"modelo não encontrado: {model_path}")
    bin_path = LLAMA_GPU if args.gpu else LLAMA_CPU
    cmd = [bin_path, "-m", model_path, "--port", str(port), "--host", "127.0.0.1",
           "--no-webui", "-c", str(args.ctx), "-t", str(args.threads)]
    if args.gpu:
        cmd += ["-ngl", "99"]
    cmd += ["--cache-type-k", args.cache_k, "--cache-type-v", args.cache_v, "-np", str(args.np)]
    if args.mtp and args.mtp > 0:
        cmd += ["--spec-type", "draft-mtp", "--spec-draft-n-max", str(args.mtp)]
    if args.reason_budget:
        cmd += ["--reasoning-budget", str(args.reason_budget), "--jinja"]
    log = open(os.path.join(SKILL_DIR, "results", f"tp-{args.name}.server.log"), "w")
    subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    return wait_health(port)

def completion_timings(port, prompt, max_tokens=256, temp=0.3, timeout=900):
    """Usa /completion nativo — retorna timings (prompt_per_second, predicted_per_second)."""
    req = urllib.request.Request(f"http://127.0.0.1:{port}/completion",
        data=json.dumps({"prompt": prompt, "n_predict": max_tokens,
                         "temperature": temp, "cache_prompt": False}).encode(),
        headers={"Content-Type": "application/json"})
    t0 = time.time()
    r = json.load(urllib.request.urlopen(req, timeout=timeout))
    dt = time.time() - t0
    t = r.get("timings", {})
    return {
        "wall_s": round(dt, 1),
        "prompt_n": t.get("prompt_n", 0),
        "predicted_n": t.get("predicted_n", 0),
        "prompt_per_second": round(t.get("prompt_per_second", 0), 1),
        "predicted_per_second": round(t.get("predicted_per_second", 0), 1),
    }

def make_prompt(n_chars):
    base = ("Explique em detalhe técnico como funciona inferência de LLM com KV cache "
            "quantizado em GPU AMD, incluindo prefill, decode e speculative decoding. ")
    return (base * (n_chars // len(base) + 1))[:n_chars]

def main():
    ap = argparse.ArgumentParser(description="Throughput isolado (t/s) de LLMs locais")
    ap.add_argument("--model", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--port", type=int, default=8083)
    ap.add_argument("--ctx", type=int, default=32768)
    ap.add_argument("--gpu", action="store_true")
    ap.add_argument("--mtp", type=int, default=0)
    ap.add_argument("--cache-k", default="q4_0")
    ap.add_argument("--cache-v", default="q4_0")
    ap.add_argument("--np", type=int, default=1)
    ap.add_argument("--threads", type=int, default=18)
    ap.add_argument("--reason-budget", type=int, default=1024)
    ap.add_argument("--sudo-pass", default=None)
    ap.add_argument("--backend", choices=["llama", "ollama"], default="llama")
    ap.add_argument("--prompt-chars", type=int, default=1024, help="tamanho do prompt de teste (~4 chars/token)")
    args = ap.parse_args()

    print("[R55] derrubando backend + drop_caches...")
    stop_backend(args.backend)
    drop_caches(args.sudo_pass)
    ram0, vram0 = get_telemetry()
    print(f"[R55] baseline: RAM {ram0} | VRAM {vram0}GB")

    print(f"[start] subindo {args.model} (ctx={args.ctx}, gpu={args.gpu}, mtp={args.mtp})...")
    if args.backend == "llama":
        ok = start_llama(args, args.port)
    else:
        run(f"ollama run {args.model} --keepalive 60m >/dev/null 2>&1 &", check=False)
        time.sleep(8)
        ok = wait_health(args.port)
    if not ok:
        print("[ERRO] health falhou — backend não subiu")
        sys.exit(1)
    ram1, vram1 = get_telemetry()
    print(f"[load] RAM {ram1} | VRAM {vram1}GB")

    prompt = make_prompt(args.prompt_chars)
    # 2 rodadas: prefill+decode curto e prefill grande (decode 256 tok)
    r1 = completion_timings(args.port, prompt, max_tokens=256)
    r2 = completion_timings(args.port, prompt * 8, max_tokens=256)  # prefill ~8x maior

    print(f"\n## Throughput isolado — {args.name}")
    print(f"| Métrica | Rodada 1 (prompt {r1['prompt_n']} tok) | Rodada 2 (prompt {r2['prompt_n']} tok) |")
    print("| :--- | :--- | :--- |")
    print(f"| **Prefill t/s** | {r1['prompt_per_second']} | {r2['prompt_per_second']} |")
    print(f"| **Decode t/s** | {r1['predicted_per_second']} | {r2['predicted_per_second']} |")
    print(f"| **Output tok** | {r1['predicted_n']} | {r2['predicted_n']} |")
    print(f"| **Wall s** | {r1['wall_s']} | {r2['wall_s']} |")
    print(f"| **VRAM load** | {vram1}GB | |")
    print(f"| **RAM** | {ram1} | |")

    out = {
        "name": args.name, "model": args.model, "ctx": args.ctx, "mtp": args.mtp,
        "cache_k": args.cache_k, "cache_v": args.cache_v, "np": args.np, "threads": args.threads,
        "telemetria": {"ram": ram1, "vram_gb": vram1},
        "rodada1": r1, "rodada2": r2,
    }
    os.makedirs(os.path.join(SKILL_DIR, "results"), exist_ok=True)
    with open(os.path.join(SKILL_DIR, "results", f"throughput-{args.name}.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n[save] results/throughput-{args.name}.json")
    print("[R55] backend derrubado (limpeza p/ próximo modelo)")
    stop_backend(args.backend)
    drop_caches(args.sudo_pass)

if __name__ == "__main__":
    main()
