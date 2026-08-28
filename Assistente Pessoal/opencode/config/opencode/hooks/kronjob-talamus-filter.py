#!/usr/bin/env python3
"""
Kronjob Tálamos Filter Hook — Córtex Sensorial Primário (R71)
Hook para session.start: intercepta o prompt ANTES dos LLMs de alta precisão,
classifica intent (pt-BR/en) e roteia tarefas mecânicas para o slot Córtex
(fast slot rwkv7-g1d-0.4b-instruct :9084, ctx 1M ~14.4 t/s).

Origin: hefesto: HARNESS KRONJOB GLOBAL GUARDRAIL.py
       (sha256 054754c86bacfcf0f6c595cec297856cfa6933f17ce53559b87202c5ddd5c5bd)
Protocolo: R71 — Guardrail Kronjob Tálamos (Córtex Sensorial Primário).
Input: JSON OpenCode session.start em stdin ({"session_id","directory","prompt"}).
Output: {"context": {"__KRONJOB_TALAMUS__": {...}}} — injeção no contexto.
Fail-open: nunca bloqueia session.start (cortex down -> prompt original).
"""

import sys
import json
import re
import os
import logging
import unicodedata
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

INVENTORY_PATH = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode/harness/llm-inventory.json")
LOG_PATH = Path("/tmp/opencode/kronjob-talamus.log")
PREFLIGHT_LOG = Path("/mnt/dados/Assistente Pessoal/opencode/state/watcher/talamus-preflight.jsonl")

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


def setup_logger():
    """Setup logger com path seguro (R2/R44)."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    l = logging.getLogger("KronjobTalamus")
    l.setLevel(logging.INFO)
    if not l.handlers:
        h = logging.FileHandler(LOG_PATH)
        h.setFormatter(logging.Formatter('%(asctime)s [KRONJOB-TALAMUS] %(message)s'))
        l.addHandler(h)
    return l


logger = setup_logger()


def load_inventory() -> dict:
    """Carrega o inventário real de LLMs (R35/R47)."""
    if INVENTORY_PATH.exists():
        with open(INVENTORY_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"models": [], "schema_version": 1}


def resolve_fast_cpu_slot() -> dict | None:
    """Resolve o slot CPU mais rápido para Tálamos (R35/R47)."""
    inventory = load_inventory()
    cpu_slots = []
    for model in inventory.get("models", []):
        sector = model.get("sector", "")
        if sector.startswith("CPU") and model.get("status") == "online":
            params = model.get("params", "0")
            if "0.8" in params or "1B" in params or "2B" in params:
                cpu_slots.append({
                    "id": model["id"],
                    "port": model.get("slot", 0),
                    "params": params,
                    "ctx": model.get("ctx_allocated", 0),
                    "temp": model.get("temp", 0.6),
                })
    cpu_slots.sort(key=lambda x: x.get("params", "99B"))
    return cpu_slots[0] if cpu_slots else None


def resolve_orchestrator_slot() -> dict | None:
    """Resolve o slot do orquestrador (VRAM) para dispatch final (R47)."""
    inventory = load_inventory()
    for model in inventory.get("models", []):
        sector = model.get("sector", "")
        if sector.startswith("GPU") and model.get("status") == "online":
            return {
                "id": model["id"],
                "port": model.get("slot", 0),
                "ctx": model.get("ctx_allocated", 0),
                "temp": model.get("temp", 0.6),
            }
    return None


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
        logger.warning("Cortex indisponível: %s", e)
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
    logger.info(
        "intent=%s action=%s tokens=%d cortex=%s",
        intent, action, tokens, cortex_status,
    )
    return emission


def append_preflight(entry: dict) -> Path:
    """Apende entry JSONL em PREFLIGHT_LOG (override via TALAMUS_PREFLIGHT_LOG)."""
    log = Path(os.environ.get("TALAMUS_PREFLIGHT_LOG", PREFLIGHT_LOG))
    log.parent.mkdir(parents=True, exist_ok=True)
    with open(log, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return log


def run_preflight(data: dict, source: str = "kronjob-talamus-filter.py --preflight") -> dict:
    """Modo --preflight: lê {request:{messages:[...]}, sessionID} e loga o JSONL
    talâmico (obserevador — nunca transforma). Retorna a entry logada."""
    request = data.get("request") or {}
    messages = request.get("messages") or []
    if isinstance(messages, dict):
        messages = [messages]
    session_id = data.get("sessionID") or data.get("session_id") or "unknown"

    roles, texts = [], []
    for m in messages:
        if not isinstance(m, dict):
            continue
        roles.append(m.get("role", "?"))
        parts = m.get("parts")
        if isinstance(parts, list):
            for p in parts:
                if isinstance(p, dict) and p.get("type") == "text":
                    t = p.get("text")
                    if isinstance(t, str):
                        texts.append(t)
        content = m.get("content")
        if isinstance(content, str):
            texts.append(content)

    joined = "\n".join(texts)
    tokens_est = max(1, (len(joined) + 3) // 4)  # chars/4 — mesma fórmula do plugin TS
    last_user = next(
        (t for t in reversed(texts) if t.strip()),
        "",
    )
    intent = classify_intent(last_user or joined)

    try:
        budget = int(os.environ.get("TALAMUS_BUDGET", "20000"))
    except ValueError:
        budget = 20000
    if intent == "PRIMITIVE_HELLO_OR_THANKYOU":
        action = "DIRECT_RESPONSE"
    elif tokens_est > budget:
        action = "CONDENSE"
    else:
        action = "DISPATCH_VRAM"

    entry = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": source,
        "sessionID": session_id,
        "messages": len(messages),
        "tokens_estimated": tokens_est,
        "roles": roles,
        "intent": intent,
        "action": action,
    }
    append_preflight(entry)
    return entry


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
    print("KRONJOB TALAMUS — TESTES DE INTENT CLASSIFICATION")
    print("=" * 60)
    for p in test_prompts:
        result = build_emission(p)
        t = result["context"]["__KRONJOB_TALAMUS__"]
        print(f"\nPrompt: {p}")
        print(f"  Intent: {t['intent']}")
        print(f"  Action: {t['action']}")
        print(f"  Needle: {t['needle_required']}")
    print("\n" + "=" * 60)
    print("Tálamos filter: OK")
    print("=" * 60)


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    if "--test" in argv:
        run_tests()
        return 0

    if "--preflight" in argv:
        # Observador talâmico: lê JSON de mensagens via stdin, loga e imprime a entry.
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
        print(json.dumps({
            "fast_cpu_slot": FAST_SLOT,
            "orchestrator_slot": ORCH_SLOT,
            "inventory_fast": resolve_fast_cpu_slot(),
            "inventory_orch": resolve_orchestrator_slot(),
        }, indent=2, ensure_ascii=False))
        return 0

    prompt = read_stdin_payload(argv)
    try:
        emission = build_emission(prompt)
    except Exception as e:
        # Fail-open absoluto: nunca bloqueia session.start
        logger.exception("Falha no filtro Tálamos: %s", e)
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