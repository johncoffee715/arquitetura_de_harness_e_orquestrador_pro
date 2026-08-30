#!/usr/bin/env python3
"""
Testes TDD para o Bibliotecário (R77/R28).

Cobre: busca lexical, verificação de paths reais (anti-alucinação),
veredito categórico, watcher (lock/idempotência), gabarito.
"""

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, "/mnt/dados/Assistente Pessoal/opencode/config/opencode/scripts")

from bibliotecario_rag import (
    buscar_lexical,
    verificar_paths_reais,
    VAULT,
)
from bibliotecario_watcher import LOCK, EXCLUDE


class TestBuscaLexical:
    def test_returns_real_paths(self):
        """Paths retornados devem existir no filesystem."""
        paths = buscar_lexical("hefesto refatoração", top_n=5)
        for p in paths:
            assert Path(p).exists(), f"path inventado: {p}"

    def test_paths_within_vault(self):
        """Paths devem estar dentro do Vault."""
        paths = buscar_lexical("aprendizados", top_n=5)
        for p in paths:
            assert p.startswith(str(VAULT)), f"fora do vault: {p}"

    def test_empty_query_ok(self):
        """Query vazia não deve quebrar."""
        paths = buscar_lexical("", top_n=3)
        assert isinstance(paths, list)


class TestVerificarPathsReais:
    def test_all_real(self):
        """Todos os paths reais → (True, [])."""
        ok, invalidos = verificar_paths_reais([str(VAULT / "log.md")])
        assert ok is True
        assert invalidos == []

    def test_invalid_detected(self):
        """Path inventado → (False, [path])."""
        ok, invalidos = verificar_paths_reais(["/mnt/dados/Assistente Pessoal/cerebro com IA/nao-existe.md"])
        assert ok is False
        assert len(invalidos) == 1


class TestWatcher:
    def test_lock_idempotente(self):
        """Lock deve existir como Path (idempotência)."""
        assert isinstance(LOCK, Path)
        assert LOCK.name == "bibliotecario-watcher.lock"

    def test_exclude_filters(self):
        """Filtros de ruído devem incluir .obsidian e .swp."""
        assert ".obsidian" in EXCLUDE
        assert ".swp" in EXCLUDE


class TestGabarito:
    def test_gabarito_valido(self):
        """Gabarito deve ser JSON válido com allow/deny."""
        gp = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode/skills/bibliotecario/gabarito.json")
        g = json.loads(gp.read_text(encoding="utf-8"))
        assert g["feature"] == "bibliotecario"
        assert "allow" in g and "deny" in g
        assert "inventar path" in g["deny"]["behaviors"]

    def test_tres_camadas(self):
        """Skill deve ter 3 camadas R77."""
        d = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode/skills/bibliotecario")
        assert (d / "conceito.md").exists()
        assert (d / "gabarito.json").exists()
        assert (d / "mecanica.md").exists()
        assert (d / "SKILL.md").exists()


class TestCLI:
    def test_rag_cli(self):
        """CLI do RAG deve retornar JSON com veredito."""
        r = subprocess.run(
            [sys.executable, "/mnt/dados/Assistente Pessoal/opencode/config/opencode/scripts/bibliotecario_rag.py",
             "hefesto", "--top-n", "3"],
            capture_output=True, text=True, timeout=30,
        )
        assert r.returncode == 0, r.stderr
        out = json.loads(r.stdout)
        assert "verdict" in out
        assert "references" in out