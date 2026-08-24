#!/usr/bin/env python3
"""LLM Benchmark — Bateria Gran-Mestre helenizada (T1/T2/T3 + R55 + matriz).

Uso:
  python3 bench.py --model <arquivo.gguf|nome-ollama> [flags]
  Ver SKILL.md para flags completas.
"""
import argparse, json, os, re, subprocess, sys, time, urllib.request

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = "/mnt/dados/Assistente Pessoal/modelos LLM/"
LLAMA_GPU = "/home/johncoffee/llama.cpp/build/bin/llama-server"
LLAMA_CPU = "/mnt/dados/llama.cpp-master/build-cpu/bin/llama-server"
RESULTS_DIR = os.path.join(SKILL_DIR, "results")

def run(cmd, timeout=60, check=True):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if check and r.returncode != 0:
        raise RuntimeError(f"cmd falhou ({r.returncode}): {cmd}\n{r.stderr[:400]}")
    return r

def drop_caches(sudo_pass):
    """R55: derruba caches do kernel (requer root)."""
    if sudo_pass:
        run(f'echo "{sudo_pass}" | sudo -S sh -c \'sync && echo 3 > /proc/sys/vm/drop_caches\' 2>/dev/null')
    else:
        run("sudo -n sh -c 'sync && echo 3 > /proc/sys/vm/drop_caches'", check=False)

def telemetry():
    """RAM + VRAM atuais."""
    ram = subprocess.run("free -g | awk 'NR==2{print $3\"/\"$2}'", shell=True,
                         capture_output=True, text=True).stdout.strip()
    vram = ""
    r = subprocess.run("rocm-smi --showmeminfo vram 2>/dev/null | grep Used", shell=True,
                       capture_output=True, text=True)
    if r.returncode == 0:
        for line in r.stdout.splitlines():
            if "VRAM Total Used Memory" in line:
                vram = f"{int(line.split(':')[-1].strip()) / 1e9:.1f}GB"
    return ram, vram

def call_llm(port, payload, timeout=600):
    req = urllib.request.Request(f"http://127.0.0.1:{port}/v1/chat/completions",
        data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    t0 = time.time()
    r = json.load(urllib.request.urlopen(req, timeout=timeout))
    dt = time.time() - t0
    c = r["choices"][0]["message"]["content"]
    u = r.get("usage", {})
    return c, dt, u

def wait_health(port, tries=40, delay=5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=2) as h:
                if '"status":"ok"' in h.read().decode():
                    return True
        except Exception:
            pass
        time.sleep(delay)
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
    log = open(os.path.join(SKILL_DIR, "results", f"{args.name}.server.log"), "w")
    subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    return wait_health(port)

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

# ---------- TESTES ----------

def _load_codigo_ctx(ctx):
    """Carrega o fixture truncando para caber no ctx (preserva a invariante)."""
    codigo = open(os.path.join(SKILL_DIR, "fixtures", "codigo_12k.txt")).read()
    linhas = codigo.split("\n")
    idx = next((i for i, l in enumerate(linhas) if "INVARIANTE_CRITICA_R52" in l), 0)
    if ctx >= 16384 or len(linhas) <= 400:
        return codigo  # completo (ctx grande)
    tok_linha = len(codigo) / len(linhas) / 2.1  # ~2.1 chars/token em C
    max_linhas = int((ctx * 0.85) / tok_linha)  # deixa folga p/ instrução + output
    if max_linhas >= len(linhas):
        return codigo
    if max_linhas > idx + 1:
        # cabe até a invariante: corta só o pós-invariante
        return "\n".join(linhas[:max_linhas])
    # ctx pequeno: mantém a invariante, corta pré (invariante ~70% preservada)
    start = max(0, idx - (max_linhas - 1))
    return "\n".join(linhas[start:idx + 1])

def t1_kv_stress(port, name, ctx=32768):
    """T1: injeta 12k tokens de código com invariante oculta; exige só o valor."""
    codigo = _load_codigo_ctx(ctx)
    payload = {
        "messages": [{"role": "user", "content":
            "Analise este repositório massivo. Responda apenas com o valor da variável "
            f"de invariante crítica (INVARIANTE_CRITICA_R52) definida no meio do código. Sem introduções.\n\n{codigo}"}],
        "max_tokens": 30, "temperature": 0.3,
        "chat_template_kwargs": {"enable_thinking": False}}
    c, dt, u = call_llm(port, payload, timeout=600)
    alucinou = "true" not in c.lower() and "soberano" not in c.lower()
    return {"resposta": c.strip()[:120], "tempo_s": round(dt, 1),
            "prompt_tokens": u.get("prompt_tokens"), "out_tokens": u.get("completion_tokens"),
            "alucinou": alucinou}

def t2_aderencia(port, grammar=None):
    """T2: resposta estritamente JSON, sem markdown, sem tags de pensamento."""
    payload = json.load(open(os.path.join(SKILL_DIR, "fixtures", "t2_prompt.json")))
    if grammar:
        payload["grammar"] = open(os.path.join(SKILL_DIR, "fixtures", grammar)).read()
    c, dt, u = call_llm(port, payload, timeout=180)
    json_puro = bool(re.match(r'^\s*\{.*\}\s*$', c, re.S)) and '"veredito"' in c
    has_thinking = "thinking" in c.lower()
    return {"resposta": c.strip()[:200], "tempo_s": round(dt, 1),
            "json_puro": json_puro, "has_thinking_tag": has_thinking}

def t3_auditoria(port):
    """T3: julga código C com volatile; gabarito: leituras consecutivas podem divergir."""
    payload = json.load(open(os.path.join(SKILL_DIR, "fixtures", "t3_prompt.json")))
    c, dt, u = call_llm(port, payload, timeout=180)
    acertou_volatile = "volatile" in c.lower() and ("diverg" in c.lower() or "diferent" in c.lower()
        or "mudar" in c.lower() or "alterar" in c.lower() or "ler" in c.lower() and "duas" in c.lower())
    nota_match = re.search(r'(\d{1,3})\s*[/.]?\s*100', c)
    nota = int(nota_match.group(1)) if nota_match else None
    return {"resposta": c.strip()[:300], "tempo_s": round(dt, 1),
            "acertou_volatile": acertou_volatile, "nota_impressao": nota}

# ---------- MATRIZ ----------

def build_matrix(name, results, tele, cache_k="q8_0", cache_v="q8_0"):
    m = [
        f"## Matriz de Veredito — {name}",
        "",
        "| Métrica | Valor |",
        "| :--- | :--- |",
        f"| **KV cache** | K={cache_k} / V={cache_v} |",
        f"| **VRAM pós-load** | {tele['vram_pos']} |",
        f"| **VRAM pós-T1** | {tele['vram_t1']} |",
        f"| **RAM pós-load** | {tele['ram_pos']} |",
        f"| **Throughput T1** | {results['t1']['prompt_tokens']} tok / {results['t1']['tempo_s']}s |",
        f"| **T1 (KV stress)** | {'PASSOU' if not results['t1']['alucinou'] else 'FALHOU'} — {results['t1']['resposta']!r} |",
        f"| **T2 (JSON puro)** | {'Pass' if results['t2']['json_puro'] else 'Fail'} — thinking: {'Sim' if results['t2']['has_thinking_tag'] else 'Não'} |",
        f"| **T3 (volatile)** | {'Acertou' if results['t3']['acertou_volatile'] else 'Errou'} — nota {results['t3']['nota_impressao']} |",
        f"| **T3 resposta** | {results['t3']['resposta']!r} |",
        "",
    ]
    return "\n".join(m)

def main():
    ap = argparse.ArgumentParser(description="LLM Benchmark Gran-Mestre (helenizado)")
    ap.add_argument("--model", required=True)
    ap.add_argument("--backend", default="llama", choices=["llama", "ollama"])
    ap.add_argument("--port", type=int, default=8083)
    ap.add_argument("--ctx", type=int, default=32768)
    ap.add_argument("--gpu", action="store_true", default=True)
    ap.add_argument("--cpu", action="store_true")
    ap.add_argument("--threads", type=int, default=18)
    ap.add_argument("--grammar-t2", default="json-strict.gbnf", help="GBNF p/ blindar T2 (default json-strict.gbnf; vazio = sem gramática)")
    ap.add_argument("--np", type=int, default=1, help="slots paralelos (vídeo: 1 — sem paralelismo; -np 4 quadruplica KV)")
    ap.add_argument("--mtp", type=int, default=0, help="MTP Nmax (vídeo: 3)")
    ap.add_argument("--cache-k", default="q8_0", help="tipo KV K (default q8_0 — quantizado)")
    ap.add_argument("--cache-v", default="q4_0", help="tipo KV V (default q4_0 — quantizado; V tolera mais)")
    ap.add_argument("--temp", type=float, default=0.3)
    ap.add_argument("--reason-budget", type=int, default=1024)
    ap.add_argument("--skip-t1", action="store_true")
    ap.add_argument("--skip-t2", action="store_true")
    ap.add_argument("--skip-t3", action="store_true")
    ap.add_argument("--name", default=None)
    ap.add_argument("--sudo-pass", default=None)
    ap.add_argument("--keep-up", action="store_true")
    args = ap.parse_args()
    if args.cpu: args.gpu = False
    args.name = args.name or os.path.basename(args.model).replace(".gguf", "")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    print(f"[R55] derrubando backend + drop_caches...")
    stop_backend(args.backend)
    drop_caches(args.sudo_pass)
    ram0, vram0 = telemetry()
    print(f"[R55] baseline: RAM {ram0} | VRAM {vram0}")

    print(f"[start] subindo {args.model} (ctx={args.ctx}, gpu={args.gpu}, mtp={args.mtp})...")
    ok = start_llama(args, args.port) if args.backend == "llama" else wait_health(args.port)
    if not ok:
        print("FALHA: modelo não subiu"); sys.exit(1)
    ram1, vram1 = telemetry()
    print(f"[load] RAM {ram1} | VRAM {vram1}")

    results = {}
    if not args.skip_t1:
        print("[T1] KV stress...")
        results["t1"] = t1_kv_stress(args.port, args.name, args.ctx)
        _, vram_t1 = telemetry()
    else:
        results["t1"] = {"alucinou": None}
        vram_t1 = vram1
    if not args.skip_t2:
        print("[T2] aderência JSON...")
        results["t2"] = t2_aderencia(args.port, args.grammar_t2)
    if not args.skip_t3:
        print("[T3] auditoria A2A...")
        results["t3"] = t3_auditoria(args.port)

    tele = {"ram_pos": ram1, "vram_pos": vram1, "vram_t1": vram_t1}
    matrix = build_matrix(args.name, results, tele, args.cache_k, args.cache_v)
    print(matrix)

    out = {"name": args.name, "model": args.model, "ctx": args.ctx, "gpu": args.gpu,
           "mtp": args.mtp, "temp": args.temp, "cache_k": args.cache_k, "cache_v": args.cache_v,
           "telemetria": tele, "results": results}
    with open(os.path.join(RESULTS_DIR, f"{args.name}.json"), "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"[save] results/{args.name}.json")

    if not args.keep_up:
        stop_backend(args.backend)
        print("[R55] backend derrubado (limpeza p/ próximo modelo)")

if __name__ == "__main__":
    main()