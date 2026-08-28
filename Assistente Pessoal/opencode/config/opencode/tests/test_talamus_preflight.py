#!/usr/bin/env python3
"""
Testes TDD para o ecossistema talâmico pré-LLM (T1-T5):
  - plugin/talamus-preflight.ts       (plugin pré-LLM, auto-load pasta plugin/)
  - modo --preflight dos hooks python (kronjob + sdd)

Caminhos canônicos globais (R27). Rodar: python3 -m pytest tests/test_talamus_preflight.py -v
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode")
PLUGIN = BASE / "plugin" / "talamus-preflight.ts"
KRONJOB = BASE / "hooks" / "kronjob-talamus-filter.py"
SDD = BASE / "hooks" / "sdd" / "sdd-talamus-filter.py"
WATCHER = Path("/mnt/dados/Assistente Pessoal/opencode/state/watcher")
PREFLIGHT_LOG = WATCHER / "talamus-preflight.jsonl"
NODE = Path("/usr/bin/node")
SMOKE_DIR = Path(tempfile.gettempdir()) / "opencode"

# --- heurística de intent do hook python (fonte de verdade) ---
_spec = importlib.util.spec_from_file_location("kronjob_talamus", KRONJOB)
kronjob = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(kronjob)


def _tmp_log() -> Path:
    fd, name = tempfile.mkstemp(prefix="talamus-preflight-", suffix=".jsonl")
    os.close(fd)
    return Path(name)


def _make_messages(n=12) -> list:
    msgs = []
    for i in range(n):
        role = "system" if i == 0 else ("user" if i % 2 == 1 else "assistant")
        text = ("parágrafo %d " % i) * 20
        msgs.append({"info": {"role": role}, "parts": [{"type": "text", "text": text}]})
    msgs[-1]["parts"][0]["text"] = "buscar exato no needle agora"  # última user = consulta
    return msgs


# ---------------------------------------------------------------------------
# 1) Classificação de intent (heurística do kronjob) — >=6 casos
# ---------------------------------------------------------------------------
def test_classify_intent_cases():
    cases = [
        ("olá", "PRIMITIVE_HELLO_OR_THANKYOU"),
        ("obrigado por tudo", "PRIMITIVE_HELLO_OR_THANKYOU"),
        ("buscar exato no needle agora", "NEEDLE_EXACT_SEARCH_TRIGGER"),
        ("extrair erros do log e stack trace", "RAW_LOGS"),
        ("rerank documentos relevantes do contexto", "RAG_DOCUMENTS"),
        ("resumo do histórico de conversa anterior", "LONG_CHAT_HISTORY"),
        ("scraping de página web em html", "WEB_SCRAPING"),
        ("implementar feature X", "GENERAL"),
    ]
    assert len(cases) >= 6, "precisa de >=6 casos"
    for prompt, expected in cases:
        got = kronjob.classify_intent(prompt)
        assert got == expected, f"'{prompt}' -> {got} (esperado {expected})"
    print(f"ok test_classify_intent_cases: {len(cases)} casos")


# ---------------------------------------------------------------------------
# 2) Plugin TS: existe + hooks registrados + smoke real via node
# ---------------------------------------------------------------------------
def test_plugin_file_exists_and_registers_hooks():
    assert PLUGIN.exists(), f"plugin ausente: {PLUGIN}"
    src = PLUGIN.read_text(encoding="utf-8")
    assert '"experimental.chat.messages.transform"' in src, "hook transform ausente"
    assert "talamus-preflight.jsonl" in src, "path do JSONL ausente"
    assert "catch" in src and "try {" in src, "fail-open ausente"
    assert 'import type { Plugin } from "@opencode-ai/plugin"' in src, "assinatura Plugin ausente"
    print("ok test_plugin_file_exists_and_registers_hooks")


def test_plugin_ts_smoke_execution():
    assert NODE.exists(), "node ausente"
    log_tmp = _tmp_log()
    driver = SMOKE_DIR / "talamus_smoke.mjs"
    SMOKE_DIR.mkdir(parents=True, exist_ok=True)

    driver_src = r"""
import { TalamusPreflight, classifyIntent, estimateTokens } from "__PLUGIN__"

const mk = (role, i) => ({
  info: { role },
  parts: [{ type: "text", text: ("parágrafo " + i + " ").repeat(20) }],
})
const messages = []
for (let i = 0; i < 12; i++) {
  const role = i === 0 ? "system" : i % 2 === 1 ? "user" : "assistant"
  messages.push(mk(role, i))
}
messages[11].parts[0].text = "buscar exato no needle agora"

if (classifyIntent("olá") !== "PRIMITIVE_HELLO_OR_THANKYOU") throw new Error("classifyIntent primitivo")
if (classifyIntent("buscar exato no needle") !== "NEEDLE_EXACT_SEARCH_TRIGGER") throw new Error("classifyIntent needle")
if (estimateTokens("x".repeat(400)) < 50) throw new Error("estimateTokens baixo")

const plugin = (await TalamusPreflight())
const hooks = plugin
const h = hooks["experimental.chat.messages.transform"]
if (typeof h !== "function") throw new Error("hook transform ausente")

// 1) sem TALAMUS_CONDENSE: observa e loga, NÃO transforma
process.env.TALAMUS_CONDENSE = "0"
const out1 = { messages: JSON.parse(JSON.stringify(messages)) }
await h({}, out1)
if (out1.messages.length !== 12) throw new Error("transformou sem condense")

// 2) com TALAMUS_CONDENSE=1 + budget baixo: condensa preservando system + cauda quente
process.env.TALAMUS_CONDENSE = "1"
process.env.TALAMUS_BUDGET = "150"
const out2 = { messages: JSON.parse(JSON.stringify(messages)) }
await h({}, out2)
if (out2.messages.length >= 12) throw new Error("não condensou")
if (out2.messages[0].info.role !== "system") throw new Error("system perdida")
const roles2 = out2.messages.map((m) => m.info.role)
if (roles2.length < 8) throw new Error("cauda quente perdida")

// 3) JSONL apendado e completo
const fs = await import("fs")
if (!fs.existsSync("__LOG__")) throw new Error("JSONL ausente")
const lines = fs.readFileSync("__LOG__", "utf-8").trim().split("\n")
if (!lines.length) throw new Error("JSONL vazio")
const last = JSON.parse(lines[lines.length - 1])
if (!last.ts || !last.intent || !last.action || !Array.isArray(last.roles)) throw new Error("entry incompleto")
if (typeof last.tokens_estimated !== "number") throw new Error("tokens inválido")

console.log("SMOKE_OK", JSON.stringify({ len: out2.messages.length, intent: last.intent, action: last.action, entries: lines.length }))
"""
    driver.write_text(driver_src.replace("__PLUGIN__", PLUGIN.as_uri()).replace("__LOG__", str(log_tmp)))
    try:
        env = {
            **os.environ,
            "TALAMUS_PREFLIGHT_LOG": str(log_tmp),
            "TALAMUS_CONDENSE": "1",
            "TALAMUS_BUDGET": "150",
        }
        run = subprocess.run([str(NODE), str(driver)], capture_output=True, text=True, timeout=60, env=env)
        assert run.returncode == 0, f"smoke falhou rc={run.returncode}\nstdout: {run.stdout[-500:]}\nstderr: {run.stderr[-800:]}"
        assert "SMOKE_OK" in run.stdout, run.stdout[-500:]
        print(f"ok test_plugin_ts_smoke_execution: {run.stdout.strip()}")
    finally:
        if driver.exists():
            driver.unlink()
        if log_tmp.exists():
            log_tmp.unlink()


# ---------------------------------------------------------------------------
# 3) Modo --preflight dos hooks python (pipe JSON -> JSONL append)
# ---------------------------------------------------------------------------
def test_preflight_mode_kronjob():
    log_tmp = _tmp_log()
    data = {
        "sessionID": "tst-kronjob-001",
        "request": {
            "messages": [
                {"role": "system", "parts": [{"type": "text", "text": "sys prompt"}]},
                {"role": "user", "parts": [{"type": "text", "text": "resumo do histórico de conversa"}]},
            ]
        },
    }
    try:
        env = {**os.environ, "TALAMUS_PREFLIGHT_LOG": str(log_tmp)}
        run = subprocess.run(["python3", str(KRONJOB), "--preflight"],
                             input=json.dumps(data), text=True, capture_output=True, timeout=30, env=env)
        assert run.returncode == 0, run.stderr[:500]
        entry = json.loads(run.stdout)
        assert entry["intent"] == "LONG_CHAT_HISTORY", entry["intent"]
        assert entry["action"] in ("DIRECT_RESPONSE", "DISPATCH_VRAM", "CONDENSE")
        assert entry["messages"] == 2 and entry["roles"] == ["system", "user"]
        assert log_tmp.exists() and log_tmp.stat().st_size > 0
        line = json.loads(log_tmp.read_text(encoding="utf-8").strip().splitlines()[-1])
        assert line["intent"] == entry["intent"] and line["sessionID"] == "tst-kronjob-001"
        print("ok test_preflight_mode_kronjob: JSONL apendado")
    finally:
        if log_tmp.exists():
            log_tmp.unlink()


def test_preflight_mode_sdd():
    log_tmp = _tmp_log()
    data = {
        "sessionID": "tst-sdd-001",
        "request": {"messages": [{"role": "user", "parts": [{"type": "text", "text": "olá"}]}]},
    }
    try:
        env = {**os.environ, "TALAMUS_PREFLIGHT_LOG": str(log_tmp)}
        run = subprocess.run(["python3", str(SDD), "--preflight"],
                             input=json.dumps(data), text=True, capture_output=True, timeout=30, env=env)
        assert run.returncode == 0, run.stderr[:500]
        entry = json.loads(run.stdout)
        assert entry["intent"] == "PRIMITIVE_HELLO_OR_THANKYOU", entry["intent"]
        assert entry["action"] == "DIRECT_RESPONSE", entry["action"]
        assert log_tmp.exists() and log_tmp.stat().st_size > 0
        print("ok test_preflight_mode_sdd: JSONL apendado")
    finally:
        if log_tmp.exists():
            log_tmp.unlink()


# ---------------------------------------------------------------------------
# 4) Config continua JSON válido (T2 não pode quebrar)
# ---------------------------------------------------------------------------
def test_opencode_jsonc_valid():
    cfg = BASE / "opencode.jsonc"
    assert cfg.exists()
    try:
        json.loads(cfg.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise AssertionError(f"opencode.jsonc inválido: {e}")
    print("ok test_opencode_jsonc_valid")


if __name__ == "__main__":
    tests = [
        test_classify_intent_cases,
        test_plugin_file_exists_and_registers_hooks,
        test_plugin_ts_smoke_execution,
        test_preflight_mode_kronjob,
        test_preflight_mode_sdd,
        test_opencode_jsonc_valid,
    ]
    passed = failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            print(f"❌ {t.__name__}: {e}")
            failed += 1
    print("=" * 60)
    print(f"RESULTADO: {passed}/{len(tests)} passed, {failed} failed")
    print("=" * 60)
    sys.exit(0 if failed == 0 else 1)