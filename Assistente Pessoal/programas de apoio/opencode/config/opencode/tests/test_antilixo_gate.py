"""test_antilixo_gate.py — TDD do detector determinístico anti-lixo/anti-alucinação de entrega.

Contexto: subagentes (ex.: hefesto :9088) retornaram (a) linhas gigantes de separadores
sem conteúdo útil, (b) afirmações "8/8 PASS / OK / concluído" SEM ter escrito nada
(sha de arquivo-alvo inalterado). Este detector roda no GATE DE ENTREGA do orquestrador
(R28/R53/R70) — zero LLM, custo ~0.

Rota: escopo governança — criado por execução supervisionada direta (R6/R11: o executor
designado era o próprio fonte da alucinação; exceção documentada no decision-log).
"""
import hashlib
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
try:
    from antilixo_gate import (
        afirmar_sucesso,
        classificar,
        sinais_lixo,
        tem_exit_status,
        verificar_entrega,
    )
except ImportError as e:
    raise SystemExit(f"não carregou antilixo_gate: {e}")


def _tmp_file(content: str) -> Path:
    fd, path = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(content)
    return Path(path)


def _sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TestSinaisLixo(unittest.TestCase):
    def test_separador_gigante_detectado(self):
        r = sinais_lixo("─" * 300 + "\nretorno ok")
        self.assertTrue(r["lixo"], r)

    def test_linha_igual_repetida(self):
        r = sinais_lixo("=" * 500)
        self.assertTrue(r["lixo"], r)

    def test_conteudo_normal_nao_falso_positivo(self):
        txt = "# Relatório\n\n## Mudanças\n- a: b\n- c: d\n\n## Verificações\nunittest 8/8 PASS\n"
        r = sinais_lixo(txt)
        self.assertFalse(r["lixo"], r.get("motivos"))

    def test_repeticao_90_porcento(self):
        txt = ("─" * 200 + "\n") * 5 + "fim"
        r = sinais_lixo(txt)
        self.assertTrue(r["lixo"], r)

    def test_vazio_ou_minimo(self):
        r = sinais_lixo("ok")
        self.assertTrue(r["lixo"])  # mínimo demais = sem evidência


class TestVerificarEntrega(unittest.TestCase):
    def setUp(self):
        self.txt_ok = "# feito\nexit_status: ok\nmudancas em SKILL.md\n"
        self.txt_alu = "Tudo pronto! 8/8 PASS ✅ OK, concluído com sucesso.\n"
        self.baseline_f = _tmp_file("BASELINE conteudo")
        self.baseline_sha = _sha_file(self.baseline_f)

    def tearDown(self):
        try:
            os.unlink(self.baseline_f)
        except FileNotFoundError:
            pass

    def test_sucesso_sem_escrita_alucinacao(self):
        r = verificar_entrega(self.txt_alu, [self.baseline_f], {str(self.baseline_f): self.baseline_sha})
        self.assertTrue(r["alucinacao_entrega"], r)

    def test_sucesso_com_escrita_pass(self):
        self.baseline_f.write_text("MUDOU conteudo", encoding="utf-8")  # arquivo alterado
        r = verificar_entrega(self.txt_ok, [self.baseline_f], {str(self.baseline_f): self.baseline_sha})
        self.assertFalse(r["alucinacao_entrega"])
        self.assertEqual(r["status"], "ok")

    def test_sem_exit_status_incompleto(self):
        txt = "Concluído com sucesso, tudo certinho."
        r = verificar_entrega(txt, [self.baseline_f], {str(self.baseline_f): self.baseline_sha}, exigir_exit_status=True)
        self.assertTrue(r["incompleto"], r)

    def test_classificacao_ordeira(self):
        ver = classificar(self.txt_alu, [self.baseline_f], {str(self.baseline_f): self.baseline_sha}, exigir_exit_status=True)
        self.assertEqual(ver["status"], "NAO_PASSOU_CATEGORICO")
        motivos = " ".join(ver["motivos"])
        self.assertTrue("escrita" in motivos or "lixo" in motivos, ver)


if __name__ == "__main__":
    unittest.main()