"""
Testes TDD do gerador canônico sync-llm-stack.py (espelhos da stack LLM local).

Contrato (R29 — evidência fresca):
 1. --check limpo após --apply (exit 0, zero divergências)
 2. --apply idempotente (2ª rodada não altera nenhum arquivo)
 3. opencode.jsonc: JSON válido; cada slot do manifesto presente como provider;
    limit.context == ctx_ativo; model/small_model corretos; hook registrado
 4. llm-inventory.json: nº models == manifesto; campos obrigatórios presentes
 5. start-stack.sh: launch por slot; -c == ctx_ativo (GPU = ORNITH_CTX dinâmico)
 6. scripts de porta (stop/toggle/guard/obsidian): todos os slots nas listas
 7. manifesto artificial (mock) → apply no real → estado restaurado (roundtrip)
"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

BASE = Path(__file__).resolve().parent.parent
SCRIPTS = BASE / "scripts"
CONFIG = BASE / "config" / "opencode"
SRC_MANIFEST = Path("/mnt/dados/Assistente Pessoal/modelos LLM/manifesto_llm.json")
SYNC = SCRIPTS / "sync-llm-stack.py"

TARGETS = [
    CONFIG / "opencode.jsonc",
    CONFIG / "harness" / "llm-inventory.json",
    CONFIG / "manifest_llm.json",
    SCRIPTS / "ctx-cost.py",
    SCRIPTS / "start-stack.sh",
    SCRIPTS / "stop-all-models.sh",
    SCRIPTS / "stack-guard.sh",
    SCRIPTS / "stack-toggle.sh",
    SCRIPTS / "obsidian-sync.sh",
]


def run_sync(*args):
    return subprocess.run(
        [sys.executable, str(SYNC), *args], capture_output=True, text=True
    )


def load_manifest():
    with open(SRC_MANIFEST, encoding="utf-8") as f:
        return json.load(f)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


@pytest.fixture(scope="module", autouse=True)
def aplicar_uma_vez():
    r = run_sync("--apply")
    assert r.returncode == 0, f"--apply falhou:\n{r.stdout}\n{r.stderr}"
    yield


def test_1_check_limpo_apos_apply():
    r = run_sync("--check")
    assert r.returncode == 0, f"divergências remanescentes:\n{r.stdout}\n{r.stderr}"


def test_2_apply_idempotente():
    antes = {str(p): sha(p) for p in TARGETS}
    antes_manifesto = sha(SRC_MANIFEST)
    r = run_sync("--apply")
    assert r.returncode == 0, f"{r.stdout}\n{r.stderr}"
    for p in TARGETS:
        assert antes[str(p)] == sha(p), f"{p.name} mudou na 2ª aplicação"
    assert antes_manifesto == sha(SRC_MANIFEST), "manifesto fonte mudou na 2ª aplicação"


def test_3_opencode_jsonc_espelha_manifesto():
    cfg = json.loads((CONFIG / "opencode.jsonc").read_text(encoding="utf-8"))
    src = load_manifest()
    provs = cfg["provider"]
    for m in src["models"]:
        slot = str(m["slot_port"])
        ctx = m["fisica_inferencia"]["ctx_ativo"]
        found = [
            p
            for p in provs.values()
            if p.get("options", {}).get("baseURL") == f"http://127.0.0.1:{slot}/v1"
        ]
        assert found, f"provider do slot {slot} ausente no opencode.jsonc"
        for mod in found[0]["models"].values():
            assert mod["limit"]["context"] == ctx, (
                f"slot {slot}: limit.context {mod['limit']['context']} != ctx_ativo {ctx}"
            )
    assert cfg["model"] == "local-orchestrator/orchestrator"
    assert cfg["small_model"] == "local-thalamus/thalamus-cortex"
    hooks = cfg.get("hooks", {}).get("session.start", [])
    assert any("hooks/sync-llm-stack.py" in h for h in hooks), "hook de sync não registrado"


def test_4_inventory_espelha_manifesto():
    inv = json.loads((CONFIG / "harness" / "llm-inventory.json").read_text(encoding="utf-8"))
    src = load_manifest()
    assert len(inv["models"]) == len(src["models"]), "nº de models difere do manifesto"
    campos = {
        "id", "slot", "file", "params", "quant", "arch", "n_ctx_train",
        "ctx_allocated", "kb_per_tok", "temp", "category", "sector", "status",
    }
    for model in inv["models"]:
        assert campos <= set(model), f"faltam campos em {model.get('id')}: {campos - set(model)}"


def test_5_start_stack_espelha_manifesto():
    content = (SCRIPTS / "start-stack.sh").read_text(encoding="utf-8")
    src = load_manifest()
    for m in src["models"]:
        slot = str(m["slot_port"])
        assert re.search(rf"(?m)^launch {slot} ", content), f"launch {slot} ausente"
        ctx = m["fisica_inferencia"]["ctx_ativo"]
        if m.get("device", "CPU") == "GPU":
            assert '-c "$ORNITH_CTX"' in content, "GPU deve usar ORNITH_CTX dinâmico (R60)"
        else:
            assert re.search(
                rf"(?m)^launch {slot} .*\n  -c {ctx} ", content
            ), f"slot {slot}: -c != ctx_ativo {ctx}"


def test_6_scripts_porta_contem_todos_slots():
    src = load_manifest()
    slots = {str(m["slot_port"]) for m in src["models"]}
    stop = (SCRIPTS / "stop-all-models.sh").read_text(encoding="utf-8")
    m = re.search(r"(?m)^PORTS=\(([^)]*)\)", stop)
    assert m, "PORTS=(...) ausente em stop-all-models.sh"
    assert set(m.group(1).split()) == slots
    toggle = (SCRIPTS / "stack-toggle.sh").read_text(encoding="utf-8")
    m = re.search(r"(?m)^\s*local ports=\(([^)]*)\)", toggle)
    assert m, "local ports=(...) ausente em stack-toggle.sh"
    assert set(m.group(1).split()) == slots
    guard = (SCRIPTS / "stack-guard.sh").read_text(encoding="utf-8")
    m = re.search(r"(?m)^\s*for p in ([0-9 ]+); do", guard)
    assert m, "loop for p ausente em stack-guard.sh"
    assert set(m.group(1).split()) == slots
    obs = (SCRIPTS / "obsidian-sync.sh").read_text(encoding="utf-8")
    m = re.search(r"(?m)^\s*\$\(\s*for p in ([0-9 ]+); do", obs)
    assert m, "loop for p ausente em obsidian-sync.sh"
    assert set(m.group(1).split()) == slots | {"8097"}


@pytest.fixture()
def manifesto_temporario(tmp_path):
    """Backup do manifesto real; restaura ao final do teste (roundtrip seguro)."""
    backup = tmp_path / "manifesto_llm.json.bak"
    shutil.copy2(SRC_MANIFEST, backup)
    yield
    shutil.copy2(backup, SRC_MANIFEST)
    r = run_sync("--apply")
    assert r.returncode == 0, "restauração pós-teste falhou"
    inv = json.loads((CONFIG / "harness" / "llm-inventory.json").read_text(encoding="utf-8"))
    slugs_src = {m["derivado"]["slug"] for m in load_manifest()["models"]}
    assert slugs_src <= {x["id"] for x in inv["models"]}, (
        "slugs canônicos perdidos após roundtrip artificial (derivado.slug do manifesto fonte)"
    )


def test_7_manifesto_artificial_roundtrip(manifesto_temporario):
    artificial = {
        "version": "teste",
        "updated": "2026-08-28T00:00:00Z",
        "models": [
            {
                "model_id": "Fake-Modelo-1B-Q4_K_M",
                "slot_port": 7001,
                "device": "CPU",
                "topologia_arquitetura": {
                    "tipo_fundacao": "qwen2",
                    "contexto_nativo": 32768,
                },
                "fisica_inferencia": {
                    "quantizacao": "Q4_K_M",
                    "ctx_ativo": 32768,
                    "kv_per_token_kb": 5.0,
                    "temp": 0.5,
                },
                "vocacao_grafo": "F1 DESCOBERTA",
            },
            {
                "model_id": "Fake-Cortex-0.3B-FP16",
                "slot_port": 7002,
                "device": "CPU",
                "topologia_arquitetura": {
                    "tipo_fundacao": "rwkv",
                    "contexto_nativo": 1048576,
                },
                "fisica_inferencia": {"quantizacao": "FP16", "ctx_ativo": 1048576},
                "vocacao_grafo": "CÓRTEX SENSORIAL PRIMÁRIO",
            },
        ],
    }
    SRC_MANIFEST.write_text(json.dumps(artificial, ensure_ascii=False), encoding="utf-8")
    r = run_sync("--apply")
    assert r.returncode == 0, f"--apply com manifesto artificial falhou:\n{r.stdout}\n{r.stderr}"
    stop = (SCRIPTS / "stop-all-models.sh").read_text(encoding="utf-8")
    m = re.search(r"(?m)^PORTS=\(([^)]*)\)", stop)
    assert m, "PORTS ausente"
    assert {"7001", "7002"} <= set(m.group(1).split()) and "9089" not in m.group(1)
    start = (SCRIPTS / "start-stack.sh").read_text(encoding="utf-8")
    assert "launch 7001" in start and "launch 7002" in start
    inv = json.loads((CONFIG / "harness" / "llm-inventory.json").read_text(encoding="utf-8"))
    assert {x["slot"] for x in inv["models"]} == {"7001", "7002"}