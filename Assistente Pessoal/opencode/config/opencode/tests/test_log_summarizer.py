#!/usr/bin/env python3
"""
Testes TDD para o Log Summarizer (R77/R28).

Cobre: determinismo, contagem de sinais (pytest/go/jest), compressão,
gabarito, 3 camadas R77.
"""

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, "/mnt/dados/Assistente Pessoal/opencode/config/opencode/scripts")

from log_summarizer import summarise_log, compress_result, extract_tail

SCRIPT = "/mnt/dados/Assistente Pessoal/opencode/config/opencode/scripts/log_summarizer.py"


class TestSummariseLog:
    def test_conta_linhas(self):
        s = summarise_log("a\nb\nc")
        assert s["totalLines"] == 3

    def test_conta_erros_warnings(self):
        s = summarise_log("ERROR: x\nwarning: y\nok\nFAILED: z")
        assert s["errorLines"] == 1
        assert s["warningLines"] == 1
        assert s["passCount"] == 1
        assert s["failCount"] == 1

    def test_pytest_padroes(self):
        s = summarise_log("tests/test_a.py::test_x PASSED\ntests/test_b.py::test_y FAILED")
        assert s["passCount"] == 1
        assert s["failCount"] == 1
        assert "test_y" in s["firstFailure"]

    def test_go_test_padroes(self):
        s = summarise_log("ok  github.com/x/pkg 0.5s\nFAIL  github.com/y/pkg 0.1s")
        assert s["passCount"] >= 1
        assert s["failCount"] >= 1

    def test_primeiro_erro_capturado(self):
        s = summarise_log("linha normal\nERROR: primeiro erro grave\nERROR: segundo")
        assert s["firstError"] == "ERROR: primeiro erro grave"

    def test_determinismo(self):
        log = "ERROR: a\nwarning: b\nPASSED\nFAILED\nok"
        assert summarise_log(log) == summarise_log(log)


class TestCompressResult:
    def test_tail_12_linhas(self):
        out = "\n".join(f"linha {i}" for i in range(30))
        c = compress_result(out)
        assert c["truncated"] is True
        assert "linha 29" in c["summary"]

    def test_assinatura(self):
        c = compress_result("PASSED\nFAILED\nERROR: x")
        assert "[1 pass | 1 fail | 1 err | 0 warn]" in c["signature"]

    def test_truncamento_400(self):
        out = "x" * 1000
        c = compress_result(out)
        assert len(c["summary"]) <= 400
        assert "truncated" in c["summary"]


class TestCLI:
    def test_summarise_cli(self):
        r = subprocess.run(
            [sys.executable, SCRIPT, "--summarise", "--json"],
            input="ERROR: a\nPASSED\nFAILED", capture_output=True, text=True, timeout=10,
        )
        assert r.returncode == 0
        d = json.loads(r.stdout)
        assert d["errorLines"] == 1
        assert d["passCount"] == 1
        assert d["failCount"] == 1

    def test_compress_cli(self):
        r = subprocess.run(
            [sys.executable, SCRIPT, "--compress", "--json"],
            input="ok\nFAIL", capture_output=True, text=True, timeout=10,
        )
        assert r.returncode == 0
        d = json.loads(r.stdout)
        assert "summary" in d
        assert "signature" in d


class TestGabarito:
    def test_tres_camadas(self):
        d = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode/skills/log-summarizer")
        assert (d / "conceito.md").exists()
        assert (d / "gabarito.json").exists()
        assert (d / "mecanica.md").exists()
        assert (d / "SKILL.md").exists()

    def test_gabarito_valido(self):
        g = json.loads(Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode/skills/log-summarizer/gabarito.json").read_text())
        assert g["feature"] == "log-summarizer"
        assert "chamar LLM para sumarizar" in g["deny"]["behaviors"]