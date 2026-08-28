#!/usr/bin/env python3
"""
SDD Tálamos Filter Hook — Córtex Sensorial Primário (R71)
Córtex Sensorial Primário para pré-filtragem de inputs via slot rápido
(rwkv7-g1d-0.4b-instruct :9084, ctx 1M ~14.4 t/s), espelhado no protocolo
Kronjob Tálamos.

Input: JSON OpenCode session.start em stdin ({"session_id","directory","prompt"}).
Output: {"context": {"__KRONJOB_TALAMUS__": {...}}} — injeção no contexto.
Fail-open: nunca bloqueia session.start (cortex down -> prompt original).
"""

import sys
import json
import re
import importlib.util
import unicodedata
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

HOOK_NAME = "sdd-talamus-filter"
LOG_PATH = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode/logs/sdd-hook.log")
KRONJOB_HOOK = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode/hooks/kronjob-talamus-filter.py")

CORTEX_BASE = "http://127.0.0.1:9084/v1"
CORTEX_MODEL = "rwkv7-g1d-0.4b-instruct"
CORTEX_TIMEOUT = 10
CORTEX_MAX_TOKENS = 128
CORTEX_SYSTEM = (
    "Você é o Córtex Sensorial Primário. Execute APENAS a tarefa mecânica "
    "pedida e retorne apenas o resultado limpo (IDs, JSON ou texto). "
    "Nunca raciocine."
)

FAST_SLOT = {"id": "rwkv7-g1d-0.4b-instruct", "port": 9084}
ORCH_SLOT = {"id": "ornith-1.5-9b-q5", "port": 8083}

TOKEN_RE = re.compile(r"[a-z0-9]+")

KEYWORDS = {
    "PRIMITIVE_HELLO_OR_THANKYOU": [
        "ola", "oi", "bom dia", "boa tarde", "boa noite", "eae", "hey", "hi",
        "hello", "thanks", "obrigado", "thank you", "tchau", "bye", "ok",
    ],
    "RAG_DOCUMENTS": [
        "documento", "rag", "contexto", "paragrafo", "relevant", "rerank",
        "busca em docs",
    ],
    "LONG_CHAT_HISTORY": [
        "historico", "history", "conversa anterior", "chat anterior", "thread",
    ],
    "RAW_LOGS": [
        "log", "erro", "error", "critical", "stack trace", "exception", "crash",
    ],
    "WEB_SCRAPING": [
        "web", "scrap", "html", "scrape", "site", "pagina", "markdown",
    ],
    "NEEDLE_EXACT_SEARCH_TRIGGER": [
        "buscar exato", "exact search", "needle", "busca exata", "hash",
    ],
}

CORTEX_TASKS = {
    "RAG_DOCUMENTS": (
        "Liste APENAS os IDs (JSON array) dos 3 parágrafos mais relevantes "
        "para a consulta. Consulta: "
    ),
    "LONG_CHAT_HISTORY": (
        "Produza um resumo executivo de 1 parágrafo que condense o histórico. "
        "Histórico: "
    ),
    "RAW_LOGS": (
        "Filtre apenas as linhas ERROR/CRITICAL, deduplique e remova "
        "timestamps repetidos. Logs: "
    ),
    "WEB_SCRAPING": (
        "Extraia apenas o texto corrido do artigo, removendo scripts, tags e "
        "menus. Conteúdo: "
    ),
}


def log(msg):
    """Log simples com path seguro."""
    ts = datetime.now().isoformat()
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] [{HOOK_NAME}] {msg}\n")
    except Exception:
        pass


def _norm(text: str) -> str:
    """Minúsculas + remoção de acentos (matching pt-BR/en robusto)."""
    text = text.lower()
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


def _has_keyword(text: str, keywords) -> bool:
    """Match por token (palavra) — evita falso positivo de substrings curtos."""
    norm = _norm(text)
    toks = set(TOKEN_RE.findall(norm))
    for kw in keywords:
        if " " in kw:
            if kw in norm:
                return True
            continue
        klen = len(kw)
        if klen < 3:
            if kw in toks:
                return True
        elif klen == 3:
            if kw in toks or (kw == "log" and "logs" in toks):
                return True
        else:
            for t in toks:
                if t.startswith(kw):
                    return True
    return False


def classify_intent(prompt: str) -> str:
    """Classifica intent do prompt (pt-BR + en) per R71."""
    if not prompt or not prompt.strip():
        return "GENERAL"
    for intent in (
        "PRIMITIVE_HELLO_OR_THANKYOU",
        "NEEDLE_EXACT_SEARCH_TRIGGER",
        "RAG_DOCUMENTS",
        "LONG_CHAT_HISTORY",
        "RAW_LOGS",
        "WEB_SCRAPING",
    ):
        if _has_keyword(prompt, KEYWORDS[intent]):
            return intent
    return "GENERAL"


def estimate_tokens(prompt: str) -> int:
    """Estimativa aproximada de tokens do prompt."""
    return len([t for t in TOKEN_RE.findall(_norm(prompt)) if t])


def call_cortex(task_prefix: str, prompt: str):
    """Chama o Córtex (rwkv7 :9084) via chat completion OpenAI-compatível.

    Timeout 10s; falha -> (None, "DOWN") — fail-open, nunca bloqueia.
    """
    payload = {
        "model": CORTEX_MODEL,
        "messages": [
            {"role": "system", "content": CORTEX_SYSTEM},
            {"role": "user", "content": task_prefix + prompt[:20000]},
        ],
        "max_tokens": CORTEX_MAX_TOKENS,
        "temperature": 0.1,
    }
    req = urllib.request.Request(
        CORTEX_BASE + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=CORTEX_TIMEOUT) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        content = body["choices"][0]["message"]["content"].strip()
        return content[:4000], "UP"
    except Exception as e:
        log(f"Cortex indisponível: {e}")
        return None, "DOWN"


def route_intent(prompt: str, intent: str):
    """Roteia a task conforme intent. Retorna (distilled, action, needle, cortex_status)."""
    if intent == "PRIMITIVE_HELLO_OR_THANKYOU":
        # Early-exit: NON-BLOCKING, sem cortex call, sem GPU wake (R71.3)
        return prompt, "DIRECT_RESPONSE", False, "SKIPPED"
    if intent == "NEEDLE_EXACT_SEARCH_TRIGGER":
        # Apenas flag para dispatch do needle 2 — hook NUNCA chama needle (R71.3)
        return prompt, "NEEDLE_FLAG", True, "SKIPPED"
    if intent == "GENERAL":
        return prompt, "PASS_THROUGH", False, "SKIPPED"
    distilled, status = call_cortex(CORTEX_TASKS[intent], prompt)
    if distilled is not None:
        return distilled, "CORTEX_DISTILLED", False, status
    return prompt, "CORTEX_DOWN_FAILOPEN", False, status


def build_emission(prompt: str) -> dict:
    """Classifica, roteia e monta o JSON de injeção de contexto do hook."""
    intent = classify_intent(prompt)
    tokens = estimate_tokens(prompt)
    distilled, action, needle, cortex_status = route_intent(prompt, intent)

    emission = {
        "context": {
            "__KRONJOB_TALAMUS__": {
                "active": True,
                "intent": intent,
                "distilled": distilled,
                "action": action,
                "fast_slot": dict(FAST_SLOT),
                "orchestrator_slot": dict(ORCH_SLOT),
                "needle_required": needle,
            }
        }
    }
    log(f"intent={intent} action={action} tokens={tokens} cortex={cortex_status}")
    return emission


def read_stdin_payload(argv) -> str:
    """Lê JSON do stdin (session.start). Fallbacks: argv join | prompt vazio."""
    raw = ""
    try:
        if not sys.stdin.isatty():
            raw = sys.stdin.read()
    except Exception:
        raw = ""
    if raw.strip():
        try:
            data = json.loads(raw)
            if isinstance(data, dict):
                return data.get("prompt", "") or ""
            return raw.strip()
        except json.JSONDecodeError:
            return raw.strip()
    return " ".join(argv)


def run_tests():
    """Testes manuais de intent classification (sem chamadas de rede)."""
    test_prompts = [
        "olá",
        "obrigado",
        "buscar exato no needle",
        "rerank documentos relevantes",
        "resumo do histórico de conversa",
        "extrair erros do log",
        "scraping de página web",
        "implementar feature X",
    ]
    print("=" * 60)
    print("SDD TALAMUS — TESTES DE INTENT CLASSIFICATION")
    print("=" * 60)
    for p in test_prompts:
        result = build_emission(p)
        t = result["context"]["__KRONJOB_TALAMUS__"]
        print(f"\nPrompt: {p}")
        print(f"  Intent: {t['intent']}")
        print(f"  Action: {t['action']}")
        print(f"  Needle: {t['needle_required']}")
    print("\n" + "=" * 60)
    print("SDD Tálamos filter: OK")
    print("=" * 60)


def run_preflight(data: dict) -> dict:
    """Modo --preflight SDD: mesmo pipeline talâmico do kronjob (DRY), source SDD.

    Carrega o kronjob via importlib (pai do path) para reusar a heurística
    R71 classificando e logando no mesmo JSONL de state/watcher.
    """
    spec = importlib.util.spec_from_file_location("kronjob_talamus", KRONJOB_HOOK)
    kj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kj)
    return kj.run_preflight(data, source="sdd-talamus-filter.py --preflight")


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    if "--test" in argv:
        run_tests()
        return 0

    if "--preflight" in argv:
        try:
            raw = sys.stdin.read()
            data = json.loads(raw) if raw.strip() else {}
        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"input_invalido: {e}"}))
            return 1
        entry = run_preflight(data)
        print(json.dumps(entry, ensure_ascii=False))
        return 0

    if "--slots" in argv:
        print(json.dumps({"fast_slot": FAST_SLOT, "orchestrator_slot": ORCH_SLOT},
                         indent=2, ensure_ascii=False))
        return 0

    prompt = read_stdin_payload(argv)
    try:
        emission = build_emission(prompt)
    except Exception as e:
        # Fail-open absoluto: nunca bloqueia session.start
        log(f"ERROR: falha no filtro Tálamos: {e}")
        emission = {
            "context": {
                "__KRONJOB_TALAMUS__": {
                    "active": True,
                    "intent": "GENERAL",
                    "distilled": prompt,
                    "action": "FAILOPEN",
                    "fast_slot": dict(FAST_SLOT),
                    "orchestrator_slot": dict(ORCH_SLOT),
                    "needle_required": False,
                }
            }
        }
    print(json.dumps(emission, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())