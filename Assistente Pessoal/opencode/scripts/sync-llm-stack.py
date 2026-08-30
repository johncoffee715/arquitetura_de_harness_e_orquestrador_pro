#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync-llm-stack.py — Gerador canônico da configuração da stack LLM local (R27/R71).

FONTE ÚNICA DE VERDADE:
    /mnt/dados/Assistente Pessoal/modelos LLM/manifesto_llm.json

ALVOS REGENERADOS (espelhos derivados — NUNCA editar à mão):
    1. config/opencode/opencode.jsonc          → providers + models + model/small_model + hook
    2. config/opencode/harness/llm-inventory.json → models[] canônicos (merge preserva curadoria)
    3. config/opencode/manifest_llm.json       → cópia operacional (cortex_sensorial + models dict)
    4. scripts/ctx-cost.py                     → STACK_CPU dinâmico (leitura do manifesto)
    5. scripts/start-stack.sh                  → seção de launches
    6. scripts/stop-all-models.sh              → PORTS=(...)
    7. scripts/stack-guard.sh                  → loop "for p in ..."
    8. scripts/stack-toggle.sh                 → local ports=(...)
    9. scripts/obsidian-sync.sh                → loop "for p in ..."

O manifesto FONTE é enriquecido com sync_state {last_sync, generator_version, health}
e reescrito (idempotente: last_sync só muda na 1ª escrita ou troca de versão).

Uso:
    sync-llm-stack.py --check    → verifica divergências (exit 0 = sincronizado, 1 = divergências; não modifica)
    sync-llm-stack.py --apply    → regenera TODOS os alvos + enriquece o manifesto
    sync-llm-stack.py --health   → sonda /health de cada slot em paralelo e atualiza sync_state.health
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

VERSION = "1.0.0"
BASE = Path("/mnt/dados/Assistente Pessoal/opencode")
CONFIG = BASE / "config" / "opencode"
SCRIPTS = BASE / "scripts"
MODELS_DIR = Path("/mnt/dados/Assistente Pessoal/modelos LLM")
MANIFEST_SRC = MODELS_DIR / "manifesto_llm.json"

T_OPENCODE = CONFIG / "opencode.jsonc"
T_INVENTORY = CONFIG / "harness" / "llm-inventory.json"
T_MANIFEST = CONFIG / "manifest_llm.json"
T_CTXCOST = SCRIPTS / "ctx-cost.py"
T_START = SCRIPTS / "start-stack.sh"
T_STOP = SCRIPTS / "stop-all-models.sh"
T_GUARD = SCRIPTS / "stack-guard.sh"
T_TOGGLE = SCRIPTS / "stack-toggle.sh"
T_OBSIDIAN = SCRIPTS / "obsidian-sync.sh"

TARGETS = [
    T_CTXCOST,
    T_START,
    T_STOP,
    T_GUARD,
    T_TOGGLE,
    T_OBSIDIAN,
    T_INVENTORY,
    T_MANIFEST,
    T_OPENCODE,
]

BACKUP_DIR = Path("/tmp/opencode/sync-llm-stack-backups")
LOG_FILE = Path("/tmp/opencode/sync-llm-stack.log")

HOOK_CMD = "python3 /mnt/dados/Assistente Pessoal/opencode/config/opencode/hooks/sync-llm-stack.py"

PROVIDER_KEYS = {
    "orquestrador": "local-orchestrator",
    "talamus-cortex": "local-thalamus",
    "judge": "local-judge",
    "reflexo": "local-reflexo",
    "executor": "local-executor",
    "contrato-plano": "local-forge",
    "tool-leve": "local-tool",
    "prosa": "local-prose",
    "refutacao": "local-ternary",
    "descoberta": "local-descoberta",
}

# R75 — ROLES FUNCIONAIS (inversão de dependência): agentes .md acoplam a roles abstratos,
# nunca a instâncias/GGUF. Troca de LLM no slot = editar manifesto + --apply; bindings intactos.
ROLE_KEYS = {
    "orquestrador": "orchestrator",   # síntese macro, supervisão do grafo, decisão final
    "talamus-cortex": "ingestor",     # processamento rápido, fatiamento/compressão (Filtro Talâmico)
    "judge": "judge",                 # validação neutra, arbitrar refutações
    "reflexo": "reflexo",             # refutação de alta velocidade (acerto-e-erro R42)
    "contrato-plano": "proposer",     # sintaxe precisa, tool calling, código pragmático
    "refutacao": "refuter",           # base conceitual profunda, auditar/refutar com dados
    "forja": "forja",                   # validação de schema byte-level + tool calling (Needle-2)
    "executor": "proposer",           # (legado) mesmo role do contrato-plano
    "tool-leve": "ingestor",          # (legado) mesmo role do talamus-cortex
    "prosa": "refuter",               # (legado) mesmo role da refutacao
    "descoberta": "ingestor",         # (legado) mesmo role do talamus-cortex
}


def log(msg):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] {msg}"
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass
    print(line, file=sys.stderr)


# ─────────────────────────── utilidades ───────────────────────────

def _now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _strip_jsonc_comments(text):
    out = []
    i, n = 0, len(text)
    in_str = esc = False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True
            out.append(c)
            i += 1
            continue
        if c == "/" and i + 1 < n and text[i + 1] == "/":
            while i < n and text[i] != "\n":
                i += 1
            out.append("\n")
            i += 1
            continue
        if c == "/" and i + 1 < n and text[i + 1] == "*":
            i += 2
            while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i += 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


def load_json_any(path):
    raw = path.read_text(encoding="utf-8")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return json.loads(_strip_jsonc_comments(raw))


def _strip_ignored(obj, ignore):
    if isinstance(obj, dict):
        return {k: _strip_ignored(v, ignore) for k, v in obj.items() if k not in ignore}
    if isinstance(obj, list):
        return [_strip_ignored(v, ignore) for v in obj]
    return obj


IGNORED_KEYS = ("last_updated", "last_sync", "updated")


def _backup(path):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = BACKUP_DIR / f"{path.name}.{ts}"
    if not dest.exists():
        shutil.copy2(path, dest)
        log(f"backup: {path.name} → {dest}")


def _validate_bash(content, name):
    with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False, encoding="utf-8") as tf:
        tf.write(content)
        tmp = tf.name
    try:
        r = subprocess.run(["bash", "-n", tmp], capture_output=True, text=True)
        if r.returncode != 0:
            raise ValueError(f"{name}: bash -n falhou: {r.stderr.strip()}")
    finally:
        Path(tmp).unlink(missing_ok=True)


def _validate_python(content, name):
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tf:
        tf.write(content)
        tmp = tf.name
    try:
        r = subprocess.run([sys.executable, "-m", "py_compile", tmp], capture_output=True, text=True)
        if r.returncode != 0:
            raise ValueError(f"{name}: py_compile falhou: {r.stderr.strip()}")
    finally:
        Path(tmp).unlink(missing_ok=True)


def write_text_target(path, content, validate=None):
    """Compara byte a byte; backup + escrita atômica só se mudou."""
    newb = content.encode("utf-8") if isinstance(content, str) else content
    cur = path.read_bytes() if path.exists() else b""
    if cur == newb:
        log(f"inalterado: {path.name}")
        return False
    if validate:
        validate(content, path.name)
    _backup(path)
    path.write_bytes(newb)
    log(f"escrito: {path.name} ({len(newb)} bytes)")
    return True


def write_json_target(path, obj, ignore=IGNORED_KEYS):
    """Compara semanticamente (ignorando chaves voláteis); só escreve se diferir."""
    cur = None
    if path.exists():
        try:
            cur = load_json_any(path)
        except Exception:
            cur = None
    if _strip_ignored(cur, ignore) == _strip_ignored(obj, ignore):
        log(f"inalterado: {path.name}")
        return False
    s = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
    json.loads(s)  # validação de parse (JSON válido)
    _backup(path)
    path.write_text(s, encoding="utf-8")
    log(f"escrito: {path.name} ({len(s)} bytes)")
    return True


def _norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def find_gguf(model_id):
    files = sorted(p.name for p in MODELS_DIR.glob("*.gguf") if p.is_file())
    if not files:
        log(f"AVISO: {MODELS_DIR} não tem .gguf — arquivo inferido {model_id}.gguf")
        return model_id + ".gguf"
    tgt = _norm(model_id)
    for f in files:
        if _norm(f[:-5]) == tgt:
            return f
    for f in files:
        b = _norm(f[:-5])
        if b.startswith(tgt) or tgt.startswith(b):
            return f
    log(f"AVISO: nenhum .gguf corresponde a '{model_id}' — usados: {files}")
    return model_id + ".gguf"


def slugify(model_id):
    s = model_id.lower()
    s = re.sub(r"[^a-z0-9.]+", "-", s).strip("-")
    return re.sub(r"-+", "-", s)


def _old_slug_by_slot():
    out = {}
    for path in (T_MANIFEST, T_INVENTORY):
        try:
            data = load_json_any(path)
        except Exception:
            continue
        if isinstance(data.get("models"), dict):
            for k, v in data["models"].items():
                out[str(v.get("slot"))] = k
        elif isinstance(data.get("models"), list):
            for m in data["models"]:
                out[str(m.get("slot"))] = m.get("id")
        if out:
            break
    return out


def categoria(voc):
    voc = (voc or "").lower()
    if "orquestrador" in voc:
        return "orquestrador"
    if any(t in voc for t in ("córtex", "cortex", "talam", "sensorial")):
        return "talamus-cortex"
    if "judge" in voc:
        return "judge"
    if "reflexo" in voc:
        return "reflexo"
    if "executor" in voc:
        return "executor"
    if "contrato" in voc:
        return "contrato-plano"
    if "tool" in voc:
        return "tool-leve"
    if "prosa" in voc:
        return "prosa"
    if "refuta" in voc:
        return "refutacao"
    if "descoberta" in voc:
        return "descoberta"
    return "descoberta"


def papel_curto(voc):
    voc = (voc or "").strip()
    return voc.split("·")[0].strip().split(";")[0].strip() or "—"


def params_of(model_id):
    m = re.search(r"(\d+(?:\.\d+)?)[Bb]", model_id)
    return (m.group(1) + "B") if m else "?"


def derived_models(src):
    olds = _old_slug_by_slot()
    rows, cortex = [], None
    for m in src.get("models", []):
        mid = m.get("model_id", "") or "?"
        slot = str(m.get("slot_port", 0))
        fi = m.get("fisica_inferencia", {}) or {}
        arch = m.get("topologia_arquitetura", {}) or {}
        ctx = fi.get("ctx_ativo") or arch.get("contexto_nativo") or 8192
        nativo = arch.get("contexto_nativo") or ctx
        voc = m.get("vocacao_grafo", "") or ""
        cat = categoria(voc)
        deriv = m.get("derivado") or {}
        slug = deriv.get("slug") or olds.get(slot) or slugify(mid)
        temp = fi.get("temp")
        kb = fi.get("kv_per_token_kb")
        kb = float(kb) if isinstance(kb, (int, float)) and kb > 0 else 12.0
        gpu = str(m.get("device", "CPU")).upper() == "GPU"
        row = {
            "mid": mid,
            "slot": slot,
            "file": find_gguf(mid),
            "ctx": int(ctx),
            "ctx_nativo": int(nativo) if nativo else None,
            "cat": cat,
            "slug": slug,
            "temp": temp,
            "temp_eff": temp if temp is not None else 0.6,
            "kb": kb,
            "gpu": gpu,
            "papel": papel_curto(voc),
            "quant": fi.get("quantizacao", ""),
            "arch": arch.get("arch_detail") or arch.get("tipo_fundacao", ""),
            "fundacao": arch.get("tipo_fundacao", ""),
            "tool_call": cat not in ("talamus-cortex", "refutacao"),
            "output": 4096 if cat == "talamus-cortex" else 8192,
            "tps": fi.get("tps_decode_empirical"),
        }
        if cat == "talamus-cortex":
            cortex = row
        rows.append(row)
    if cortex is None and rows:
        cortex = min(rows, key=lambda r: r["ctx"])
    return rows, cortex


# ─────────────────────────── construtores de alvos ───────────────────────────

def build_opencode(rows, cortex, current):
    import copy

    new = copy.deepcopy(current)
    prov = {}
    for r in rows:
        base = PROVIDER_KEYS.get(r["cat"], "local-" + r["slug"][:20])
        key = base
        if key in prov:
            key = f"{base}-{r['slug']}"
        mkey = ROLE_KEYS.get(r["cat"], r["slug"])
        prov[key] = {
            "api": "openai",
            "name": f"{r['papel']} :{r['slot']} — role:{mkey}",
            "options": {
                "baseURL": f"http://127.0.0.1:{r['slot']}/v1",
                "apiKey": "llamacpp",
            },
            "models": {
                mkey: {
                    "name": f"role:{mkey}",
                    "limit": {"context": r["ctx"], "output": r["output"]},
                    "tool_call": r["tool_call"],
                }
            },
        }
    new["provider"] = prov
    new["model"] = "local-orchestrator/orchestrator"
    new["small_model"] = "local-thalamus/ingestor"
    hooks = new.setdefault("hooks", {})
    sl = hooks.setdefault("session.start", [])
    if HOOK_CMD not in sl:
        sl.append(HOOK_CMD)
        log("opencode.jsonc: hook sync-llm-stack.py adicionado a hooks.session.start")
    return new


def build_inventory(rows, current):
    new = dict(current)
    old_by_id = {m.get("id"): m for m in (current.get("models") or [])}
    models = []
    for r in rows:
        canon = {
            "id": r["slug"],
            "slot": r["slot"],
            "file": r["file"],
            "params": params_of(r["mid"]),
            "quant": r["quant"] or "?",
            "arch": r["arch"] or "?",
            "n_ctx_train": r["ctx_nativo"],
            "ctx_allocated": r["ctx"],
            "kb_per_tok": r["kb"],
            "temp": r["temp_eff"],
            "category": r["cat"],
            "sector": "GPU-MI50-Vulkan" if r["gpu"] else "CPU-threads",
            "status": "online",
        }
        old = old_by_id.get(r["slug"], {})
        models.append({**old, **canon})
    new["models"] = models
    new["last_updated"] = _now_iso()
    new["description"] = (
        "Inventário Global de LLMs Locais (R52) — regenerado por sync-llm-stack.py "
        "a partir de modelos LLM/manifesto_llm.json (fonte única)."
    )
    return new


def build_manifest_copy(rows, cortex, current):
    new = dict(current)
    models = {}
    for r in rows:
        hp = r["cat"] != "talamus-cortex"
        entry = {
            "slot": r["slot"],
            "category": r["cat"],
            "high_precision": hp,
            "input_hygiene_required": hp,
            "cortex_sensorial": f"{cortex['slug']}:{cortex['slot']}" if hp else None,
            "safe_input_size": r["ctx"],
            "ctx_allocated": r["ctx"],
            "status": "online",
        }
        old = (current.get("models") or {}).get(r["slug"], {})
        for k, v in old.items():
            entry.setdefault(k, v)
        models[r["slug"]] = entry
    new["models"] = models
    new["cortex_sensorial"] = {
        "model": cortex["slug"],
        "slot": cortex["slot"],
        "role": "Córtex Sensorial Primário",
        "function": "Filtro ultraveloz de input context bruto (R71)",
    }
    new["last_updated"] = _now_iso()
    new["description"] = (
        "Manifesto de modelos LLM para o Grafo Híbrido v2 — regenerado por "
        "sync-llm-stack.py a partir de modelos LLM/manifesto_llm.json."
    )
    return new


CTX_COST_MARKER = "# STACK_CPU: GERADO por sync-llm-stack.py · leitura DINÂMICA do manifesto (não editar à mão)"
CTX_COST_BLOCK = CTX_COST_MARKER + """

MANIFESTO_PATH = "/mnt/dados/Assistente Pessoal/modelos LLM/manifesto_llm.json"


def _load_stack_cpu():
    \"\"\"Lê a stack CPU (device != GPU) dinamicamente do manifesto_llm.json (fonte única).\"\"\"
    try:
        with open(MANIFESTO_PATH, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:
        print(f"ctx-cost: manifesto ilegível ({exc}) — STACK_CPU vazio", file=sys.stderr)
        return []
    rows = []
    for m in data.get("models", []):
        if str(m.get("device", "CPU")).upper() == "GPU":
            continue  # slot GPU (8083) usa compute_ornith_ctx no start-stack.sh
        fi = m.get("fisica_inferencia", {}) or {}
        arch = m.get("topologia_arquitetura", {}) or {}
        ctx = fi.get("ctx_ativo") or arch.get("contexto_nativo") or 4096
        rows.append((str(m.get("slot_port", 0)), _gguf_for(m.get("model_id", "")),
                     int(ctx), _papel(m.get("vocacao_grafo", ""))))
    return rows


def _gguf_for(model_id):
    import glob as _glob
    import re as _re

    def _n(s):
        return _re.sub(r"[^a-z0-9]", "", s.lower())

    tgt = _n(model_id)
    for f in sorted(_glob.glob(f"{MODELS_DIR}/*.gguf")):
        base = f.rsplit("/", 1)[-1][:-5]
        if _n(base) == tgt or _n(base).startswith(tgt) or tgt.startswith(_n(base)):
            return base + ".gguf"
    return model_id + ".gguf"


def _papel(voc):
    voc = (voc or "").strip()
    return voc.split("·")[0].strip().split(";")[0].strip() or "—"


STACK_CPU = _load_stack_cpu()
"""

CTX_COST_RE = re.compile(r"(?ms)^STACK_CPU = \[.*?^\][ \t]*\n")


def build_ctx_cost(current, rows=None):
    if "STACK_CPU = _load_stack_cpu()" in current:
        return current  # já é a forma gerada (idempotente — 2ª aplicação é no-op)
    if not CTX_COST_RE.search(current):
        raise ValueError("ctx-cost.py: bloco STACK_CPU não encontrado (padrão PORTS/STACK_CPU alterado)")
    return CTX_COST_RE.sub(CTX_COST_BLOCK + "\n\n", current)


START_MARKER = "# ══ SEÇÃO GERADA por sync-llm-stack.py · FONTE: manifesto_llm.json (não editar à mão) ══"


def build_start_section(rows):
    lines = [START_MARKER]
    for r in sorted(rows, key=lambda x: int(x["slot"])):
        if r["slot"] == "8083" and r["gpu"]:
            # ORQUESTRADOR — template GPU do Ornith (único que usa ORNITH_CTX)
            lines.append(f'# GPU {r["slot"]} · {r["cat"]} · {r["mid"]} · -c dinâmico via compute_ornith_ctx (R60)')
            lines.append(f'launch {r["slot"]} "{r["file"]}" \\')
            lines.append('  -c "$ORNITH_CTX" -np 1 -b 2048 -ub 1024 \\')
            lines.append("  -ngl 999 -dev Vulkan0 \\")
            lines.append("  --cache-type-k q4_0 --cache-type-v q4_0 \\")
            lines.append("  --spec-type none \\")
            lines.append("  --jinja --temp 0.6 --top-p 0.95 --top-k 20 \\")
            lines.append('  --chat-template-kwargs \'{"enable_thinking": false}\'')
        elif r["slot"] == "8083":
            # ORQUESTRADOR CPU — 35B MoE (não cabe na VRAM; ctx fixo por RAM)
            # threads AUTO (18 físicos) — t36 degrada decode 7.9→2.8 t/s (bandwidth-bound, R72 empírico 30/08)
            lines.append(f'# CPU {r["slot"]} · {r["cat"]} · {r["mid"]} · ORQUESTRADOR (CPU, ctx fixo, threads auto)')
            lines.append(f'launch {r["slot"]} "{r["file"]}" \\')
            lines.append(f"  -c {r['ctx']} -np 1 -b 2048 -ub 512 -ngl 0 \\")
            lines.append("  --cache-type-k q4_0 --cache-type-v q4_0 \\")
            lines.append("  --jinja --temp 0.6 --top-p 0.95 --top-k 20 \\")
            lines.append('  --chat-template-kwargs \'{"enable_thinking": false}\'')
        elif r["fundacao"] == "rwkv" or "rwkv" in r["slug"]:
            # RWKV (CPU ou GPU) — state fixo, ctx nativo, sem thinking
            if r["gpu"]:
                lines.append(f'# GPU {r["slot"]} · {r["cat"]} · {r["mid"]} (RWKV — state fixo, ctx nativo)')
                lines.append(f'launch {r["slot"]} "{r["file"]}" \\')
                lines.append(f"  -c {r['ctx']} -np 1 -b 512 -ngl 999 -dev Vulkan0 \\")
                lines.append("  --cache-type-k q4_0 --cache-type-v q4_0 --jinja")
            else:
                lines.append(f'# CPU {r["slot"]} · {r["cat"]} · {r["mid"]} (RWKV — state fixo, ctx não escala)')
                lines.append(f'launch {r["slot"]} "{r["file"]}" \\')
                lines.append(f"  -c {r['ctx']} -np 1 -ngl 0")
        elif r["gpu"]:
            # GPU comum (não-8083, não-RWKV) — Flash Attention ON (economiza buffers de attention na VRAM)
            t = f" --temp {r['temp']}" if r["temp"] is not None else ""
            lines.append(f'# GPU {r["slot"]} · {r["cat"]} · {r["mid"]} (FA on)')
            lines.append(f'launch {r["slot"]} "{r["file"]}" \\')
            lines.append(f"  -c {r['ctx']} -np 1 --flash-attn on -b 512 -ngl 999 -dev Vulkan0 \\")
            lines.append(f"  --cache-type-k q4_0 --cache-type-v q4_0 --jinja{t}")
        else:
            # CPU comum
            t = f" --temp {r['temp']}" if r["temp"] is not None else ""
            lines.append(f'# CPU {r["slot"]} · {r["cat"]} · {r["mid"]}')
            lines.append(f'launch {r["slot"]} "{r["file"]}" \\')
            lines.append(f"  -c {r['ctx']} -np 1 --flash-attn on -b 512 -ngl 0 \\")
            lines.append(f"  --cache-type-k q4_0 --cache-type-v q4_0{t}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n\n"


def _start_section_span(current):
    """(início, fim) da seção de launches: do marcador gerado (ou launch 8083) até o
    texto do comentário 'F0 TRIAGEM' (sem whitespace residual — span determinístico)."""
    f0 = re.search(r"(?m)^\s*# ── CPU · F0 TRIAGEM", current)
    if not f0:
        raise ValueError("start-stack.sh: marcador 'F0 TRIAGEM' não encontrado")
    end = f0.end() - len(f0.group().lstrip())
    m = re.search(r"(?m)^" + re.escape(START_MARKER), current)
    if m is not None and m.start() < end:
        return m.start(), end
    m2 = re.search(r"(?m)^launch 8083 ", current)
    if m2 is None or m2.start() >= end:
        raise ValueError("start-stack.sh: 'launch 8083' não encontrado antes de F0 TRIAGEM")
    return m2.start(), end


def build_start_script(current, rows):
    start, end = _start_section_span(current)
    return current[:start] + build_start_section(rows) + current[end:]


def ports_sorted(rows):
    return sorted(str(r["slot"]) for r in rows)


STOP_RE = re.compile(r"(?m)^PORTS=\([^)]*\)")
TOGGLE_RE = re.compile(r"(?m)^(\s*)local ports=\([^)]*\)")
GUARD_RE = re.compile(r"(?m)^(\s*)for p in [0-9 ]+; do[ \t]*$")
OBS_RE = re.compile(r"(?m)^(\s*\$\(\s*)for p in [0-9 ]+; do[ \t]*$")


def build_stop(current, rows, ports=None):
    ports = ports or ports_sorted(rows)
    if not STOP_RE.search(current):
        raise ValueError("stop-all-models.sh: PORTS=(...) não encontrado")
    return STOP_RE.sub(f"PORTS=({' '.join(ports)})", current, count=1)


def build_toggle(current, rows, ports=None):
    ports = ports or ports_sorted(rows)
    if not TOGGLE_RE.search(current):
        raise ValueError("stack-toggle.sh: 'local ports=(...)' não encontrado")
    return TOGGLE_RE.sub(lambda m: f"{m.group(1)}local ports=({' '.join(ports)})", current, count=1)


def build_guard(current, rows, ports=None):
    ports = ports or ports_sorted(rows)
    if not GUARD_RE.search(current):
        raise ValueError("stack-guard.sh: loop 'for p in ...; do' não encontrado")
    return GUARD_RE.sub(lambda m: f"{m.group(1)}for p in {' '.join(ports)}; do", current, count=1)


def build_obsidian(current, rows, ports=None):
    ports = ports or ports_sorted(rows)
    if not OBS_RE.search(current):
        raise ValueError("obsidian-sync.sh: loop 'for p in ...; do' não encontrado")
    return OBS_RE.sub(
        lambda m: f"{m.group(1)}for p in {' '.join(ports)} 8097; do", current, count=1
    )


# ─────────────────────────── enriquecimento do manifesto ───────────────────────────

def enrich_source(src, rows):
    now = _now_iso()
    changed = False
    st = src.get("sync_state")
    if not isinstance(st, dict):
        src["sync_state"] = {"generator_version": VERSION, "last_sync": now, "health": {}}
        changed = True
    else:
        if st.get("generator_version") != VERSION:
            st["generator_version"] = VERSION
            st["last_sync"] = now
            changed = True
        st.setdefault("health", {})
    src.setdefault("version", "1.2")
    for m, r in zip(src.get("models", []), rows):
        if "derivado" not in m:
            m["derivado"] = {
                "file": r["file"],
                "slug": r["slug"],
                "category": r["cat"],
                "papel": r["papel"],
                "ctx_ativo_efetivo": r["ctx"],
                "generator_version": VERSION,
            }
            changed = True
    return changed


# ─────────────────────────── --check ───────────────────────────

def _extract_ports(content, regex):
    m = re.search(regex, content)
    if not m:
        return None
    return re.findall(r"\d+", m.group(0))


def cmd_check(src):
    rows, cortex = derived_models(src)
    ports = ports_sorted(rows)
    divs = []

    if "sync_state" not in src:
        divs.append(f"{MANIFEST_SRC.name}: manifesto FONTE ainda não enriquecido (falta sync_state) — rode --apply")

    for path in TARGETS:
        if not path.exists():
            divs.append(f"{path}: AUSENTE (esperado — alvo do gerador)")
            continue
        cur = path.read_text(encoding="utf-8")
        if path == T_CTXCOST:
            if "STACK_CPU = _load_stack_cpu()" not in cur:
                divs.append(f"{path.name}: seção STACK_CPU não é a gerada (leitura dinâmica ausente)")
        elif path == T_START:
            if START_MARKER not in cur:
                divs.append(f"{path.name}: seção gerada ausente (marcador não encontrado)")
            else:
                try:
                    start, end = _start_section_span(cur)
                    got = cur[start:end]
                except ValueError:
                    got = None
                want = build_start_section(rows)
                norm = lambda t: [l.strip() for l in t.splitlines() if l.strip()]
                if got is None or norm(got) != norm(want):
                    divs.append(f"{path.name}: seção de launches difere do manifesto")
        elif path == T_STOP:
            got = _extract_ports(cur, STOP_RE)
            if got is None or sorted(got) != sorted(ports):
                divs.append(f"{path.name}: PORTS difere do manifesto (tem {got}, esperado {ports})")
        elif path == T_TOGGLE:
            got = _extract_ports(cur, TOGGLE_RE)
            if got is None or sorted(got) != sorted(ports):
                divs.append(f"{path.name}: local ports difere do manifesto (tem {got}, esperado {ports})")
        elif path == T_GUARD:
            got = _extract_ports(cur, GUARD_RE)
            if got is None or sorted(got) != sorted(ports):
                divs.append(f"{path.name}: loop for p difere do manifesto (tem {got}, esperado {ports})")
        elif path == T_OBSIDIAN:
            got = _extract_ports(cur, OBS_RE)
            if got is None or sorted(got) != sorted(ports + ["8097"]):
                divs.append(f"{path.name}: loop for p difere do manifesto (tem {got}, esperado {ports + ['8097']})")
        elif path == T_INVENTORY:
            try:
                inv = load_json_any(path)
            except Exception as e:
                divs.append(f"{path.name}: JSON inválido ({e})")
                continue
            want = build_inventory(rows, inv)
            if _strip_ignored(inv, IGNORED_KEYS) != _strip_ignored(want, IGNORED_KEYS):
                ids_inv = {m.get("id") for m in inv.get("models", [])}
                ids_want = {m.get("id") for m in want.get("models", [])}
                divs.append(f"{path.name}: difere do manifesto (ids {ids_inv} vs esperado {ids_want}) — rode --apply")
        elif path == T_MANIFEST:
            try:
                mc = load_json_any(path)
            except Exception as e:
                divs.append(f"{path.name}: JSON inválido ({e})")
                continue
            want = build_manifest_copy(rows, cortex, mc)
            if _strip_ignored(mc, IGNORED_KEYS) != _strip_ignored(want, IGNORED_KEYS):
                divs.append(f"{path.name}: difere do manifesto (modelos {set(mc.get('models', {}))} vs {set(want.get('models', {}))})")
        elif path == T_OPENCODE:
            try:
                cfg = load_json_any(path)
            except Exception as e:
                divs.append(f"{path.name}: JSON/JSONC inválido ({e})")
                continue
            want = build_opencode(rows, cortex, cfg)
            if _strip_ignored(cfg, IGNORED_KEYS) != _strip_ignored(want, IGNORED_KEYS):
                divs.append(f"{path.name}: providers/models diferem do manifesto")

    if not divs:
        print("✔ tudo sincronizado (todos os 9 alvos + manifesto fonte)")
        log("check: sincronizado")
        return 0
    for d in divs:
        print(f"[DIVERGÊNCIA] {d}")
    log(f"check: {len(divs)} divergência(s)")
    return 1


# ─────────────────────────── --apply ───────────────────────────

def cmd_apply(src):
    rows, cortex = derived_models(src)
    ports = ports_sorted(rows)
    failures = []

    def w(target, builder, validator=None, text=True):
        try:
            cur = target.read_text(encoding="utf-8") if text else ""
            return write_text_target(target, builder(cur, rows), validate=validator)
        except Exception as e:
            failures.append(f"{target.name}: {e}")
            log(f"ERRO {target.name}: {e}")
            return False

    w(T_CTXCOST, build_ctx_cost, validator=_validate_python)
    w(T_START, build_start_script, validator=_validate_bash)
    w(T_STOP, build_stop, validator=_validate_bash)
    w(T_GUARD, build_guard, validator=_validate_bash)
    w(T_TOGGLE, build_toggle, validator=_validate_bash)
    w(T_OBSIDIAN, build_obsidian, validator=_validate_bash)

    cur_inv = load_json_any(T_INVENTORY) if T_INVENTORY.exists() else {}
    write_json_target(T_INVENTORY, build_inventory(rows, cur_inv))
    cur_mc = load_json_any(T_MANIFEST) if T_MANIFEST.exists() else {}
    write_json_target(T_MANIFEST, build_manifest_copy(rows, cortex, cur_mc))
    cur_cfg = load_json_any(T_OPENCODE) if T_OPENCODE.exists() else {}
    write_json_target(T_OPENCODE, build_opencode(rows, cortex, cur_cfg))

    if enrich_source(src, rows):
        s = json.dumps(src, ensure_ascii=False, indent=2) + "\n"
        json.loads(s)
        _backup(MANIFEST_SRC)
        MANIFEST_SRC.write_text(s, encoding="utf-8")
        log(f"escrito: {MANIFEST_SRC.name} (enriquecido com sync_state + derivado)")
    else:
        log(f"inalterado: {MANIFEST_SRC.name} (já enriquecido)")

    if failures:
        print("ERROS durante --apply:")
        for f in failures:
            print(f"  - {f}")
        log(f"apply: {len(failures)} erro(s) — exit 1")
        return 1
    log("apply: concluído")
    return 0


# ─────────────────────────── --health ───────────────────────────

def _probe(port):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=2) as r:
            return port, "online" if r.status == 200 else "offline"
    except Exception:
        return port, "offline"


def cmd_health(src):
    ports = sorted(str(m.get("slot_port")) for m in src.get("models", []))
    with ThreadPoolExecutor(max_workers=min(8, len(ports) or 1)) as pool:
        results = dict(pool.map(_probe, ports))
    st = src.get("sync_state")
    if not isinstance(st, dict):
        st = src["sync_state"] = {"generator_version": VERSION, "last_sync": None, "health": {}}
    st["health"] = {"ts": _now_iso(), "slots": {p: results[p] for p in sorted(results)}}
    s = json.dumps(src, ensure_ascii=False, indent=2) + "\n"
    json.loads(s)
    _backup(MANIFEST_SRC)
    MANIFEST_SRC.write_text(s, encoding="utf-8")
    print(f"{'slot':<8} {'status'}")
    for p in sorted(results):
        print(f"{p:<8} {results[p]}")
    online = sum(1 for v in results.values() if v == "online")
    print(f"online {online}/{len(results)}")
    log(f"health: {online}/{len(results)} slots online; manifesto atualizado")
    return 0


# ─────────────────────────── CLI ───────────────────────────

def main(argv=None):
    ap = argparse.ArgumentParser(description="Gerador canônico da stack LLM local (R27)")
    ap.add_argument("--check", action="store_true", help="verifica divergências (exit 0/1, não modifica)")
    ap.add_argument("--apply", action="store_true", help="regenera todos os alvos + enriquece o manifesto")
    ap.add_argument("--health", action="store_true", help="sonda /health dos slots e atualiza sync_state.health")
    a = ap.parse_args(argv)

    try:
        src = json.loads(MANIFEST_SRC.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"ERRO: manifesto fonte ilegível ({MANIFEST_SRC}): {e}", file=sys.stderr)
        return 2

    if a.health:
        return cmd_health(src)
    if a.apply:
        return cmd_apply(src)
    return cmd_check(src)


if __name__ == "__main__":
    sys.exit(main())