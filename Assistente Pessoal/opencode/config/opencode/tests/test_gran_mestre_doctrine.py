"""test_gran_mestre_doctrine.py — TDD da doutrina v8.4 (testes de contrato dos artefatos).

Valida: frontmatter parseável; versão consistente; norma de impressão R53 = nota >=95;
GAP-P5: permission presente no agent; plugin + engine existem; referencia sem stale;
inventário R52 íntegro; contagem de linhas dentro do teto (~250).
"""
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode")
SKILL = ROOT / "skills" / "gran-mestre" / "SKILL.md"
AGENT = ROOT / "agent" / "gran-mestre.md"
PLUGIN = ROOT / "plugins" / "guard-gap-p5.ts"
ENGINE = ROOT / "scripts" / "guard-engine.ts"
REFERENCE = ROOT / "skills" / "gran-mestre" / "reference" / "MIX-research-2026-08-26.md"
CONSTITUTION = ROOT / "AGENTS.md"


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---")[1])


class TestGranMestreDoctrine(unittest.TestCase):
    def test_frontmatters_parseam(self):
        sk = frontmatter(SKILL)
        ag = frontmatter(AGENT)
        self.assertEqual(sk["mode"], "skill")
        self.assertEqual(ag["mode"], "primary")
        self.assertIn("model", ag)

    def test_versao_consistente(self):
        sk = frontmatter(SKILL)
        self.assertEqual(sk["metadata"]["version"], "9.0.0")
        agent_txt = AGENT.read_text(encoding="utf-8")
        self.assertIn("v9.0.0", agent_txt)

    def test_norma_impressao_r53_95(self):
        skt = SKILL.read_text(encoding="utf-8")
        agt = AGENT.read_text(encoding="utf-8")
        self.assertIn("≥95", skt, "SKILL deve exigir nota >=95 (norma R53)")
        self.assertIn("≥95", agt)

    def test_gap_p5_permission_no_agent(self):
        ag = frontmatter(AGENT)
        perm = ag.get("permission")
        self.assertIsNotNone(perm, "agent deve ter permission (GAP-P5 camada 1)")
        self.assertEqual(perm["edit"]["*"], "deny", "edit catch-all deve ser deny")

    def test_gap_p5_plugin_e_engine_existem(self):
        self.assertTrue(PLUGIN.exists(), "guard-gap-p5.ts deve existir")
        self.assertTrue(ENGINE.exists(), "guard-engine.ts deve existir")
        plug = PLUGIN.read_text(encoding="utf-8")
        self.assertIn('import { verdict, isAllowedWritePath } from "../scripts/guard-engine"', plug)
        eng = ENGINE.read_text(encoding="utf-8")
        self.assertIn("export function isGovPath", eng)
        self.assertIn("export function isAllowedWritePath", eng)
        self.assertIn("export function unescapePath", eng)

    def test_reference_sem_stale(self):
        ref = REFERENCE.read_text(encoding="utf-8")
        self.assertNotIn("v8.3.1", ref, "reference não deve citar versão antiga como atual")
        self.assertIn("v8.4.0", ref)

    def test_inventario_presente_e_estruturado(self):
        data = json_load = __import__("json").loads(
            (ROOT / "harness" / "llm-inventory.json").read_text(encoding="utf-8")
        )
        self.assertEqual(data["schema_version"], 1)
        self.assertGreaterEqual(len(data["models"]), 5)
        self.assertIn("feature_types", data)
        self.assertIn("governance", data)

    def test_teto_linhas_skill(self):
        n = len(SKILL.read_text(encoding="utf-8").splitlines())
        self.assertLessEqual(n, 250, f"SKILL com {n} linhas (teto ~250)")


if __name__ == "__main__":
    unittest.main()
