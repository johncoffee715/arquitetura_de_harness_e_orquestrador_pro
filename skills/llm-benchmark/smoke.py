#!/usr/bin/env python3
"""LLM Smoke Tests — TIER A (spec 'benchmark llms2.md' §3.1) helenizado 2026-08-20.

5 testes rápidos e binários que revelam problemas GRAVES de quantização ou template
antes de baterias longas (TIER B/C/D):

  A1 Pelican SVG   — quantizações agressivas (2-bit) falham primeiro em criativo estruturado
  A2 Strawberry    — contagem de caracteres + chain-of-thought coerente
  A3 JSON Extract  — aderência estrita a formato (parser de structured output)
  A4 Tool Call     — emissão de <tool_call> parseável (agentes quebram sem isso)
  A5 Halluc Guard  — modelo SEM ferramentas não inventa dado em tempo real

Aplica-se a QUALQUER backend OpenAI-compatível (llama.cpp, Ollama, vLLM, LM Studio).
Integra telemetria do watcher (llm-usage-<port>.jsonl) quando disponível.

Uso:
  python3 smoke.py --port 8090 --name qwen27b-iq2xxs [--base-url http://127.0.0.1]
                   [--watcher-jsonl /mnt/dados/harness/logs/llm-usage-8090.jsonl]
                   [--output-dir results] [--temp 0.0]

Saída: results/smoke-<name>.json + tabela na tela + markdown results/smoke-<name>.md
"""
import argparse, json, os, re, sys, time, urllib.request

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RESULTS = os.path.join(SKILL_DIR, "results")

# -----------------------------------------------------------------------------
# Cliente OpenAI-compatível (mínimo, sem deps externas)
# -----------------------------------------------------------------------------

def query(base_url, port, messages, temperature=0.0, max_tokens=1024, timeout=180):
    url = f"{base_url}:{port}/v1/chat/completions"
    payload = {
        "model": "local",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode())
        dt = time.time() - t0
        _msg = data["choices"][0]["message"]
        content = _msg.get("content") or ""
        if not content.strip():
            content = ((_msg.get("reasoning_content") or "") + "\n" + content).strip()
        usage = data.get("usage", {})
        c_tok = usage.get("completion_tokens", 0)
        tps = round(c_tok / dt, 2) if dt > 0 and c_tok > 0 else 0.0
        return {"ok": True, "content": content, "dur": round(dt, 2),
                "tps": tps, "prompt_tok": usage.get("prompt_tokens", 0)}
    except Exception as e:
        return {"ok": False, "content": "", "dur": round(time.time() - t0, 2),
                "tps": 0.0, "prompt_tok": 0, "error": str(e)[:200]}

# -----------------------------------------------------------------------------
# TIER A — 5 smoke tests (spec §3.1, prompts fixos, temp 0, critério binário)
# -----------------------------------------------------------------------------

def a1_pelican_svg(res):
    """A.1 — Pelican SVG: SVG válido + pelicano + bicicleta."""
    r = query(res["base"], res["port"], [
        {"role": "user", "content": "Generate a valid SVG of a pelican riding a bicycle. The output must be an XML file with <svg> and </svg> tags only, and must contain keywords like \"pelican\", \"bird\", \"beak\", \"wing\", \"bicycle\", \"bike\", \"wheel\", \"pedal\", or \"frame\". No markdown fences or other formatting."},
    ], temperature=0.0, max_tokens=1024)
    if not r["ok"]:
        return _result("A1_Pelican_SVG", False, r, reason="request_failed")
    raw = r["content"].strip()
    has_svg = "<svg" in raw.lower() and "</svg>" in raw.lower()
    has_pelican = any(k in raw.lower() for k in ["pelican", "bird", "beak", "wing"])
    has_bike = any(k in raw.lower() for k in ["bicycle", "bike", "wheel", "pedal", "frame"])
    passed = has_svg and has_pelican and has_bike
    return _result("A1_Pelican_SVG", passed, r,
                   details={"svg_valid": has_svg, "pelican": has_pelican, "bike": has_bike})

def a2_strawberry(res):
    """A.2 — Contagem de 'r' em strawberry + reasoning coerente."""
    r = query(res["base"], res["port"], [
        {"role": "user",
         "content": 'Count the number of \'r\'s in the word "strawberry". Explain your reasoning step by step.'},
    ], temperature=0.0, max_tokens=512)
    if not r["ok"]:
        return _result("A2_Strawberry", False, r, reason="request_failed")
    raw = r["content"].strip()
    correct = bool(re.search(r"\b3\b", raw))
    has_reasoning = any(k in raw.lower() for k in ["strawberr", "step", "s-t-r", "letter", "third"])
    passed = correct and has_reasoning
    return _result("A2_Strawberry", passed, r,
                   details={"count_3": correct, "reasoning": has_reasoning})

def a3_json_extract(res):
    """A.3 — Aderência JSON: chaves exatas + parseável + sem fences."""
    r = query(res["base"], res["port"], [
        {"role": "user",
         "content": ('Extract the following information as valid JSON with keys: name, age, city.\n'
                     'Text: "Maria is 28 years old and lives in São Paulo."\n'
                     'Respond ONLY with the JSON object, no markdown fences.')},
    ], temperature=0.0, max_tokens=256)
    if not r["ok"]:
        return _result("A3_JSON_Extract", False, r, reason="request_failed")
    raw = r["content"].strip()
    has_fence = "```" in raw
    parsed = None
    try:
        m = re.search(r"\{.*\}", raw, re.DOTALL)
        parsed = json.loads(m.group(0)) if m else json.loads(raw)
    except Exception:
        parsed = None
    correct = bool(parsed and parsed.get("name") == "Maria"
                   and str(parsed.get("age")) in ("28", "28.0")
                   and parsed.get("city") == "São Paulo")
    passed = parsed is not None and correct and not has_fence
    return _result("A3_JSON_Extract", passed, r,
                   details={"parseable": parsed is not None, "values_correct": correct,
                            "markdown_fence": has_fence})

def a4_tool_call(res):
    """A.4 — Tool call parsing: exatamente um <tool_call> com JSON válido."""
    r = query(res["base"], res["port"], [
        {"role": "system",
         "content": 'You have access to a function `get_weather(city: str)`. '
                    'Respond with a tool call in the format: '
                    '<tool_call>{"name": "get_weather", "arguments": {"city": "Tokyo"}}</tool_call>'},
        {"role": "user", "content": "What's the weather in Tokyo?"},
    ], temperature=0.0, max_tokens=256)
    if not r["ok"]:
        return _result("A4_Tool_Call", False, r, reason="request_failed")
    raw = r["content"].strip()
    calls = re.findall(r"<tool_call>(.*?)</tool_call>", raw, re.DOTALL)
    parsed_ok = False
    name_ok = False
    if len(calls) == 1:
        try:
            obj = json.loads(calls[0].strip())
            parsed_ok = True
            name_ok = obj.get("name") == "get_weather" and "city" in obj.get("arguments", {})
        except Exception:
            parsed_ok = False
    passed = len(calls) == 1 and parsed_ok and name_ok
    return _result("A4_Tool_Call", passed, r,
                   details={"tool_call_count": len(calls), "json_valid": parsed_ok,
                            "name_args_ok": name_ok})

def a5_hallucination_guard(res):
    """A.5 — Sem ferramentas: modelo NÃO inventa dado em tempo real."""
    r = query(res["base"], res["port"], [
        {"role": "user", "content": "What is the current stock price of AAPL?"},
    ], temperature=0.0, max_tokens=256)
    if not r["ok"]:
        return _result("A5_Halluc_Guard", False, r, reason="request_failed")
    raw = r["content"].strip().lower()
    admits_no_access = any(k in raw for k in ["don't have", "do not have", "cannot provide",
                                               "can't provide", "no real-time", "not able",
                                               "unable to", "não tenho", "não posso",
                                               "sem acesso", "não consigo", "no access",
                                               "real-time data"])
    invented_number = bool(re.search(r"\$\s?\d+(\.\d+)?", raw))
    passed = admits_no_access and not invented_number
    return _result("A5_Halluc_Guard", passed, r,
                   details={"admits_no_access": admits_no_access, "invented_number": invented_number})

TESTS = [
    ("A1_Pelican_SVG", a1_pelican_svg),
    ("A2_Strawberry", a2_strawberry),
    ("A3_JSON_Extract", a3_json_extract),
    ("A4_Tool_Call", a4_tool_call),
    ("A5_Halluc_Guard", a5_hallucination_guard),
]

def _result(name, passed, r, details=None, reason=None):
    return {"test": name, "passed": passed, "ok": r["ok"], "dur": r["dur"], "tps": r["tps"],
            "details": details or {}, "reason": reason,
            "raw": r["content"][:300] if r["content"] else ""}

# -----------------------------------------------------------------------------
# Telemetria do watcher (integração llm-usage-<port>.jsonl)
# -----------------------------------------------------------------------------

def watcher_telemetry(jsonl_path):
    """Lê o jsonl do watcher e devolve última VRAM/temp/prefill_tps (se disponível)."""
    if not jsonl_path or not os.path.exists(jsonl_path):
        return None
    try:
        with open(jsonl_path) as f:
            lines = f.readlines()
        last = None
        for line in lines[-50:]:
            try:
                last = json.loads(line)
            except Exception:
                continue
        if not last:
            return None
        return {"vram_gb": last.get("vram_gb"), "temp_edge_c": last.get("temp_edge_c"),
                "prefill_tps": last.get("prefill_tps"), "ts": last.get("ts")}
    except Exception:
        return None

# -----------------------------------------------------------------------------
# Relatório
# -----------------------------------------------------------------------------

def build_markdown(name, results, tele, base, port):
    lines = [f"# Smoke Tests (TIER A) — {name}",
             f"**Data:** {time.strftime('%Y-%m-%d %H:%M:%S')} | **Endpoint:** {base}:{port}\n"]
    if tele:
        lines.append(f"**Telemetria (watcher):** VRAM {tele.get('vram_gb')} GB | "
                     f"temp {tele.get('temp_edge_c')}°C | prefill {tele.get('prefill_tps')} t/s\n")
    lines.append("| Teste | Pass | TPS | Duração | Notas |")
    lines.append("|-------|:----:|:---:|:-------:|-------|")
    passed = 0
    for r in results:
        status = "✅" if r["passed"] else "❌"
        if r["passed"]:
            passed += 1
        notes = "; ".join(f"{k}={v}" for k, v in (r.get("details") or {}).items()) if r.get("details") else ""
        if r.get("reason"):
            notes += f" reason={r['reason']}"
        lines.append(f"| {r['test']} | {status} | {r['tps']} | {r['dur']}s | {notes} |")
    lines.append(f"\n**Total: {passed}/{len(results)}**")
    if passed == len(results):
        lines.append("\n**Veredito: 🏆 APTO (sem regressão de quantização/template)**")
    elif passed >= 3:
        lines.append("\n**Veredito: ⚠️ PARCIAL — investigar testes falhos (quant/template/tool parser)**")
    else:
        lines.append("\n**Veredito: ❌ INVIÁVEL para papel agentic neste quant**")
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser(description="Smoke Tests TIER A (spec llms2.md §3.1)")
    ap.add_argument("--port", type=int, default=8090)
    ap.add_argument("--base-url", default="http://127.0.0.1")
    ap.add_argument("--name", default=None, help="Rótulo (default: modelo do /v1/models)")
    ap.add_argument("--watcher-jsonl", default=None,
                    help="Path do llm-usage-<port>.jsonl p/ telemetria (default: auto por porta)")
    ap.add_argument("--output-dir", default=DEFAULT_RESULTS)
    ap.add_argument("--temp", type=float, default=0.0)
    args = ap.parse_args()

    res = {"base": args.base_url, "port": args.port}

    # Nome padrão: consulta /v1/models
    name = args.name
    if not name:
        try:
            req = urllib.request.Request(f"{args.base_url}:{args.port}/v1/models")
            data = json.loads(urllib.request.urlopen(req, timeout=5).read().decode())
            name = data["data"][0]["id"].split("/")[-1].replace(".gguf", "")
        except Exception:
            name = f"port{args.port}"

    if not args.watcher_jsonl:
        args.watcher_jsonl = f"/mnt/dados/harness/logs/llm-usage-{args.port}.jsonl"

    print("=" * 60)
    print(f" 🚀 SMOKE TESTS (TIER A) — {name} @ {args.base_url}:{args.port}")
    print("=" * 60)

    tele = watcher_telemetry(args.watcher_jsonl)
    if tele:
        print(f" [telemetria watcher] VRAM {tele['vram_gb']}GB | temp {tele['temp_edge_c']}°C "
              f"| prefill {tele['prefill_tps']} t/s")

    results = []
    for label, fn in TESTS:
        print(f"  [{label}] executando...", end="", flush=True)
        r = fn(res)
        print(f" -> {'✅ PASS' if r['passed'] else '❌ FAIL'} ({r['tps']} t/s, {r['dur']}s)")
        results.append(r)

    os.makedirs(args.output_dir, exist_ok=True)
    md = build_markdown(name, results, tele, args.base_url, args.port)
    md_path = os.path.join(args.output_dir, f"smoke-{name}.md")
    json_path = os.path.join(args.output_dir, f"smoke-{name}.json")
    with open(md_path, "w") as f:
        f.write(md)
    with open(json_path, "w") as f:
        json.dump({"name": name, "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "endpoint": f"{args.base_url}:{args.port}", "telemetry": tele,
                   "tests": results, "passed": sum(1 for r in results if r["passed"]),
                   "total": len(results)}, f, indent=2, ensure_ascii=False)
    print(f"\n[✓] Relatório: {md_path}")
    print(f"[✓] JSON: {json_path}")

if __name__ == "__main__":
    main()