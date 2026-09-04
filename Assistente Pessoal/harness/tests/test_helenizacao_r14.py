#!/usr/bin/env python3
"""TDD write-first — R14: helenização de recursos externos.

Exigências (F3 plano):
  1. Skill caveman — compressão de saída (níveis, comandos de commit/review).
  2. Skill code-archaeologist — exploração profunda com relatório estruturado.
  3. Subagent metrology-scientist — metrologia GUM/VIM/ISO 17025.
  4. Hooks do padrão agent-scaffold — sensitive-data-check + trailer commit.

Os testes abaixo FALHAM antes da F4 (execução) e devem PASSAR depois.
"""

import os
import re
import sys
import json
import yaml
import unittest
from pathlib import Path

HARNESS = Path(__file__).resolve().parent.parent
REGISTRY = HARNESS / "registry.json"
CONFIG_DIR = Path.home() / ".config" / "opencode"

REQUIRED_FRONTMATTER = {"name", "description"}
REQUIRED_TAGS = {"tags"}
HOOKS_REQUIRED = {"sensitive-data-check.sh", "prepare-commit-msg.sh"}


def parse_frontmatter(path: Path) -> dict:
    """Parse YAML frontmatter between --- markers. Raises on malformed."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.DOTALL)
    if not m:
        raise AssertionError(f"{path}: frontmatter YAML ausente (--- obrigatório)")
    data = yaml.safe_load(m.group(1))
    if not isinstance(data, dict):
        raise AssertionError(f"{path}: frontmatter deve ser mapeamento YAML")
    return data


def registry_lists() -> dict:
    if not REGISTRY.exists():
        raise AssertionError("registry.json não existe — rode rebuild antes")
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return {
        "skills": {s.get("name") for s in data.get("skills", []) if isinstance(s, dict)},
        "subagents": {s.get("name") for s in data.get("subagents", []) if isinstance(s, dict)},
        "hooks": {s.get("name") for s in data.get("hooks", []) if isinstance(s, dict)},
    }


def tags_as_set(fm: dict) -> set:
    """tags no frontmatter é string CSV (padrão harness) — normaliza p/ set."""
    raw = fm.get("tags", [])
    if isinstance(raw, str):
        return {t.strip().lower() for t in raw.split(",") if t.strip()}
    if isinstance(raw, list):
        return {str(t).strip().lower() for t in raw if str(t).strip()}
    return set()


class TestCavemanSkill(unittest.TestCase):
    """Fonte: github.com/juliusbrussee/caveman — compressão de saída."""

    SKILL_DIR = CONFIG_DIR / "skills" / "caveman"

    def setUp(self):
        self.skill = self.SKILL_DIR / "SKILL.md"
        if not self.skill.exists():
            self.skipTest("caveman ainda não helenizado (F4 pendente)")

    def test_frontmatter_valido(self):
        fm = parse_frontmatter(self.skill)
        self.assertTrue(REQUIRED_FRONTMATTER.issubset(fm.keys()),
                        f"faltam campos {REQUIRED_FRONTMATTER - fm.keys()}")

    def test_descricao_cobre_compressao_saida(self):
        fm = parse_frontmatter(self.skill)
        desc = fm["description"].lower()
        self.assertTrue(any(w in desc for w in ("compress", "token", "saída", "saida")),
                        "description deve mencionar compressão de tokens/saída")

    def test_tags_rota_para_compressao(self):
        fm = parse_frontmatter(self.skill)
        tags = tags_as_set(fm)
        self.assertTrue(tags, "tags obrigatórias")
        self.assertTrue(any("compress" in t for t in tags),
                        "tags devem incluir compressão")

    def test_conteudo_tem_niveis_de_compressao(self):
        text = self.skill.read_text(encoding="utf-8").lower()
        self.assertIn("lite", text)
        self.assertIn("ultra", text)


class TestCodeArchaeologistSkill(unittest.TestCase):
    """Fonte: flyingwebie/claude-agents — exploração + relatório estruturado."""

    SKILL_DIR = CONFIG_DIR / "skills" / "code-archaeologist"

    def setUp(self):
        self.skill = self.SKILL_DIR / "SKILL.md"
        if not self.skill.exists():
            self.skipTest("code-archaeologist ainda não helenizado (F4 pendente)")

    def test_frontmatter_valido(self):
        fm = parse_frontmatter(self.skill)
        self.assertTrue(REQUIRED_FRONTMATTER.issubset(fm.keys()))

    def test_tags_cobrem_exploracao(self):
        fm = parse_frontmatter(self.skill)
        tags = tags_as_set(fm)
        self.assertTrue(any("explor" in t for t in tags),
                        "tags devem incluir exploração")

    def test_relatorio_tem_secoes_obrigatorias(self):
        text = self.skill.read_text(encoding="utf-8")
        for secao in ("resumo executivo", "saúde do código", "riscos", "arquitetura"):
            self.assertIn(secao, text.lower(),
                          f"relatório deve conter seção: {secao}")

    def test_workflow_survey_a_sintese(self):
        text = self.skill.read_text(encoding="utf-8").lower()
        for passo in ("survey", "map", "padrões", "síntese"):
            self.assertIn(passo, text, f"workflow deve conter passo: {passo}")


class TestMetrologyScientistAgent(unittest.TestCase):
    """Fonte: K-Dense-AI/scientific-agents — metrologia GUM/VIM/ISO 17025."""

    AGENT = CONFIG_DIR / "agents" / "metrology-scientist.md"

    def setUp(self):
        if not self.AGENT.exists():
            self.skipTest("metrology-scientist ainda não helenizado (F4 pendente)")

    def test_frontmatter_valido(self):
        fm = parse_frontmatter(self.AGENT)
        self.assertTrue(REQUIRED_FRONTMATTER.issubset(fm.keys()))
        self.assertIn("tools", fm, "subagent deve declarar tools")

    def test_descricao_cobre_metrologia(self):
        fm = parse_frontmatter(self.AGENT)
        desc = fm["description"].lower()
        self.assertTrue(any(w in desc for w in ("metrolog", "incerteza", "gum", "medição", "medicao")),
                        "description deve mencionar metrologia/incerteza")

    def test_conteudo_tem_principios_chave(self):
        text = self.AGENT.read_text(encoding="utf-8").lower()
        for princ in ("gum", "vim", "iso 17025", "incerteza"):
            self.assertIn(princ, text, f"conteúdo deve cobrir: {princ}")


class TestScaffoldHooks(unittest.TestCase):
    """Fonte: jeremyary/agent-scaffold — hooks de segurança/convenção."""

    HOOKS_DIR = CONFIG_DIR / "hooks"

    def setUp(self):
        if not self.HOOKS_DIR.exists():
            self.skipTest("diretório de hooks ausente")

    def test_hooks_obrigatorios_existem(self):
        for hook in HOOKS_REQUIRED:
            self.assertTrue((self.HOOKS_DIR / hook).exists(),
                            f"hook ausente: {hook}")

    def test_sensitive_data_check_e_executavel(self):
        path = self.HOOKS_DIR / "sensitive-data-check.sh"
        if not path.exists():
            self.skipTest("hook ainda não criado (F4 pendente)")
        self.assertTrue(os.access(path, os.X_OK),
                        "sensitive-data-check.sh deve ser executável")

    def test_sensitive_data_check_varre_segredos(self):
        path = self.HOOKS_DIR / "sensitive-data-check.sh"
        if not path.exists():
            self.skipTest("hook ainda não criado (F4 pendente)")
        text = path.read_text(encoding="utf-8")
        # literais presentes no PATTERNS (substring, não regex)
        for padrao in ("api[_-]?key", "senha", "password", "token", "secret"):
            self.assertIn(padrao, text, f"deve varrer padrão: {padrao}")
        # grep deve ser case-insensitive (pega AWS_SECRET_ACCESS_KEY)
        self.assertIn("grep -inE", text,
                      "varredura deve ser case-insensitive (-i)")

    def test_prepare_commit_msg_tem_trailer(self):
        path = self.HOOKS_DIR / "prepare-commit-msg.sh"
        if not path.exists():
            self.skipTest("hook ainda não criado (F4 pendente)")
        text = path.read_text(encoding="utf-8")
        self.assertIn("Assisted-by", text,
                      "deve anexar trailer 'Assisted-by' ao commit")


class TestRegistryDiscovery(unittest.TestCase):
    """Após F4, rebuild registry deve descobrir os recursos novos."""

    def test_registry_existe_e_cobre_categorias(self):
        if not REGISTRY.exists():
            self.skipTest("registry.json ausente — rode rebuild")
        lists = registry_lists()
        self.assertTrue(lists["skills"] and lists["subagents"] and lists["hooks"],
                        "registry deve ter skills, subagents e hooks")


if __name__ == "__main__":
    sys.path.insert(0, str(HARNESS))
    unittest.main(verbosity=2)
