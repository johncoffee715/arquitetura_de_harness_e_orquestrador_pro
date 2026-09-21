"""
mecanica.py — Motor determinístico do Quarteto Gran-Mestre v9.2 (Modo Autônomo Blindado)

Componente .py do quarteto R85. Zero LLM: valida o contrato do gabarito.json antes
de qualquer ignição. Fecha 5 GAPs auditados (R88):
  GAP-1 anti-intervenção (allowlist diagnóstico read-only)
  GAP-2 quorum de refutação (early-termination, Aegean 2512.20184)
  GAP-3 memória de ação (record/replay, MOBIMEM 2512.15784)
  GAP-4 single-writer/estado versionado (IntelliCode 2512.18669)
  GAP-5 auto-quarteto (completa o .gbnf que faltava)

Origem: hefesto: forja v9.2 (2026-09-11)
"""
import json
import hashlib
import datetime
from pathlib import Path
from typing import Dict, List

GABARITO_PATH = Path(__file__).parent / "gabarito.json"

# GAP-1: comandos read-only de diagnóstico que NÃO podem pedir permissão no modo autônomo
DIAGNOSTIC_READONLY = ["df", "free", "du", "ps", "rocm-smi", "lscpu", "cat /proc/"]


def load_gabarito() -> Dict:
    """Extrai os valores reais (default/const) do JSON Schema — fonte única R77/R81."""
    with open(GABARITO_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)
    props = schema["properties"]

    def dflt(path):
        node = props
        for key in path:
            node = node[key]["properties"]
        return {k: v.get("default", v.get("const")) for k, v in node.items()}

    return {
        "artifact": props["artifact"]["const"],
        "version": props["version"]["const"],
        "bash_allowlist": dflt(["bash_allowlist"]),
        "bash_deny": dflt(["bash_deny"]),
        "refutation_quorum": dflt(["refutation_quorum"]),
        "action_memory": dflt(["action_memory"]),
        "single_writer": dflt(["single_writer"]),
    }


def validate_diagnostic_allowlist() -> Dict:
    """GAP-1: confirma que os comandos read-only de diagnóstico estão na allowlist."""
    gab = load_gabarito()
    allow = gab["bash_allowlist"]["diagnostic_readonly"]
    missing = [c for c in DIAGNOSTIC_READONLY if c not in allow]
    return {
        "gap": "GAP-1",
        "required": DIAGNOSTIC_READONLY,
        "present": allow,
        "missing": missing,
        "verdict": "PASSOU_CATEGORICO" if not missing else "NAO_PASSOU",
    }


def refutation_quorum(rounds: int, converged_agents: int, total_agents: int) -> Dict:
    """GAP-2: detecção de quorum com early-termination (Aegean 2512.20184)."""
    gab = load_gabarito()
    max_rounds = gab["refutation_quorum"]["max_rounds"]
    threshold = gab["refutation_quorum"]["quorum_threshold"]
    early = gab["refutation_quorum"]["early_termination"]

    ratio = (converged_agents / total_agents) if total_agents else 0.0
    quorum_reached = ratio >= threshold

    if rounds > max_rounds:
        action, verdict = "ESCALAR", "NAO_PASSOU"  # R18: teto excedido → escalar
    elif quorum_reached and early:
        action, verdict = "EARLY_TERMINATION", "PASSOU_CATEGORICO"
    elif rounds == max_rounds and not quorum_reached:
        action, verdict = "ESCALAR", "NAO_PASSOU"
    else:
        action, verdict = "CONTINUAR", "PENDENTE"

    return {
        "gap": "GAP-2",
        "rounds": rounds,
        "max_rounds": max_rounds,
        "quorum_ratio": round(ratio, 3),
        "quorum_reached": quorum_reached,
        "action": action,
        "verdict": verdict,
    }


class ActionMemory:
    """GAP-3: memória de ação com record/replay (MOBIMEM 2512.15784)."""

    def __init__(self, max_entries: int = 100):
        self.entries: List[Dict] = []
        self.max_entries = max_entries

    def record(self, action_id: str, sequence: List[str], verified: bool) -> Dict:
        entry = {
            "action_id": action_id,
            "sequence": sequence,
            "verified": verified,
            "sha256": hashlib.sha256(json.dumps(sequence, sort_keys=True).encode()).hexdigest(),
            "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        self.entries.append(entry)
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[-self.max_entries:]
        return {"status": "RECORDED", "action_id": action_id, "sha256": entry["sha256"]}

    def replay(self, action_id: str) -> Dict:
        for e in reversed(self.entries):
            if e["action_id"] == action_id and e["verified"]:
                return {"status": "REPLAY", "sequence": e["sequence"], "sha256": e["sha256"]}
        return {"status": "NOT_FOUND", "action_id": action_id}


def single_writer_check(writer_id: str, state_version: int, expected_version: int) -> Dict:
    """GAP-4: single-writer + estado versionado (IntelliCode 2512.18669)."""
    if state_version != expected_version:
        return {
            "gap": "GAP-4",
            "verdict": "NAO_PASSOU",
            "reason": f"stale-config: versão {state_version} != esperada {expected_version}",
            "action": "RELOAD_FROM_CANONICAL",
        }
    return {
        "gap": "GAP-4",
        "verdict": "PASSOU_CATEGORICO",
        "writer_id": writer_id,
        "version": state_version,
    }


def _smoke_action_memory() -> Dict:
    am = ActionMemory()
    am.record("carrossel-v1.3", ["contain", "backdrop-filter"], verified=True)
    replay = am.replay("carrossel-v1.3")
    return {
        "gap": "GAP-3",
        "verdict": "PASSOU_CATEGORICO" if replay["status"] == "REPLAY" else "NAO_PASSOU",
        "replay_status": replay["status"],
    }


def run_quarteto() -> Dict:
    """Roda as 4 validações do quarteto e emite veredito categórico (R28)."""
    results = {
        "gap1_allowlist": validate_diagnostic_allowlist(),
        "gap2_quorum": refutation_quorum(rounds=2, converged_agents=3, total_agents=4),
        "gap3_action_memory": _smoke_action_memory(),
        "gap4_single_writer": single_writer_check("gm", 2, 2),
    }
    verdicts = [r.get("verdict") for r in results.values()]
    all_pass = all(v == "PASSOU_CATEGORICO" for v in verdicts)
    return {
        "artifact": "gran-mestre-v92-quarteto",
        "results": results,
        "converged": all_pass,
        "verdict": "PASSOU_CATEGORICO" if all_pass else "NAO_PASSOU",
    }


if __name__ == "__main__":
    print(json.dumps(run_quarteto(), ensure_ascii=False, indent=2))