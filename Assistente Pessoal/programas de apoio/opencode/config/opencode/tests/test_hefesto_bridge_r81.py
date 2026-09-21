"""test_hefesto_bridge_r81.py — TDD do núcleo R81/R82 (Constrained Decoding).

Cobre: transpilação Pydantic/JSON Schema -> GBNF válido; validação determinística
com retry + reinjeção de erro; anti-loop (3 falhas = exceção/fallback, nunca loop).
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills/hefesto/tooling"))

try:
    from pydantic import BaseModel, Field
    HAS_PYDANTIC = True
except Exception:
    HAS_PYDANTIC = False

from hefesto_llama_bridge import PydanticToGbnf, ConstrainedGenerate  # noqa: E402


if HAS_PYDANTIC:

    class RespostaSistema(BaseModel):
        comando_bash: str = Field(description="Comando puro, sem markdown")
        risco_execucao: int = Field(ge=0, le=5)

    class AjusteKernel(BaseModel):
        governador_cpu: str = Field(pattern="^(performance|schedutil|powersave)$")
        frequencia_max_mhz: int = Field(gt=800, le=5000)
        flag_systemd_boot: bool
        parametros_adicionais: list = Field(default_factory=list, max_items=3)


class TestPydanticToGbnf(unittest.TestCase):
    def test_gramatica_gbnf_valida(self):
        g = PydanticToGbnf(RespostaSistema).to_gbnf()
        self.assertTrue(g.startswith("root ::= "))
        self.assertIn("ws ::= ", g)
        self.assertIn('"comando_bash"', g)
        self.assertIn('"risco_execucao"', g)

    def test_enum_alternancia(self):
        schema = {"type": "object", "properties": {"estado": {"enum": ["ok", "failed"]}}, "required": ["estado"]}
        g = PydanticToGbnf(schema).to_gbnf()
        # enum de strings: aspas literais GBNF ("\"" "ok" "\"") — JSON *com* aspas
        self.assertIn('"\\"" "ok" "\\""', g)
        self.assertIn('"\\"" "failed" "\\""', g)

    def test_pattern_vira_alternancia(self):
        g = PydanticToGbnf(AjusteKernel).to_gbnf() if HAS_PYDANTIC else ""
        if HAS_PYDANTIC:
            self.assertIn('"performance" | "schedutil" | "powersave"', g)

    def test_bool_array_object(self):
        schema = {
            "type": "object",
            "properties": {
                "flag": {"type": "boolean"},
                "tags": {"type": "array", "items": {"type": "string"}, "maxItems": 2},
                "inner": {"type": "object", "properties": {"x": {"type": "integer"}}, "required": ["x"]},
            },
            "required": ["flag"],
        }
        g = PydanticToGbnf(schema).to_gbnf()
        self.assertIn('("true" | "false")', g)
        self.assertIn('"tags"', g)
        self.assertIn('"x"', g)


class TestConstrainedGenerate(unittest.TestCase):
    def _mk(self, sequence, response_model=None, fallback=None):
        """completions_fn que retorna a próxima resposta da lista."""
        self._calls = 0

        def fn(**kwargs):
            self._calls += 1
            idx = self._calls - 1
            if idx < len(sequence):
                return sequence[idx]
            raise RuntimeError("muitas chamadas")

        return fn, response_model, fallback

    def _ok_model(self):
        if not HAS_PYDANTIC:
            return None  # sem pydantic: usa mode None
        return RespostaSistema

    def test_primeira_tentativa_valida(self):
        if HAS_PYDANTIC:
            model = RespostaSistema
            seq = ['{"comando_bash": "ls", "risco_execucao": 2}']
        else:
            model = None
            seq = ["ls"]
        fn, _, _ = self._mk(seq, model)
        cg = ConstrainedGenerate(fn, model, grammar="", max_retries=2)
        obj, meta = cg.run("tarefa")
        self.assertTrue(meta["ok"])
        if HAS_PYDANTIC:
            self.assertEqual(obj.comando_bash, "ls")
            self.assertEqual(obj.risco_execucao, 2)

    def test_retry_reinjeta_erro(self):
        if HAS_PYDANTIC:
            model = RespostaSistema
            seq = ["{JSON INVÁLIDO", '{"comando_bash": "ls", "risco_execucao": 3}']
        else:
            model = None
            seq = ["", "ls"]
        fn, _, _ = self._mk(seq, model)
        cg = ConstrainedGenerate(fn, model, max_retries=3)
        obj, meta = cg.run("tarefa")
        self.assertTrue(meta["ok"])
        self.assertEqual(meta["attempts"], 2)

    def test_anti_loop_falha_3_vezes_estoura(self):
        if HAS_PYDANTIC:
            model = RespostaSistema
            seq = ["x", "x", "x", "x"]
        else:
            model = None
            seq = ["", "", "", ""]
        fn, _, _ = self._mk(seq, model)
        cg = ConstrainedGenerate(fn, model, max_retries=3)
        with self.assertRaises(RuntimeError) as ctx:
            cg.run("tarefa")
        self.assertIn("3 falhas", str(ctx.exception))

    def test_ant_loop_falback(self):
        model = RespostaSistema if HAS_PYDANTIC else None
        fb = {"comando_bash": "", "risco_execucao": 0}
        fn, _, _ = self._mk(["x", "x", "x"], model)
        cg = ConstrainedGenerate(fn, model, max_retries=3, fallback=fb)
        obj, meta = cg.run("tarefa")
        self.assertEqual(meta["ok"], False)
        self.assertEqual(obj["risco_execucao"], 0)




class TestR81Itens345(unittest.TestCase):
    """Itens 3-4-5: gabarito-fonte, FORJA byte-level, config estrita."""

    def test_gabarito_to_schema(self):
        from hefesto_llama_bridge import gabarito_to_schema
        gab = {"schema": {"type": "object", "properties": {"a": {"type": "string"}}, "required": ["a"]}}
        s = gabarito_to_schema(gab)
        self.assertEqual(s["properties"]["a"]["type"], "string")

    def test_gabarito_to_schema_invalido(self):
        from hefesto_llama_bridge import gabarito_to_schema
        with self.assertRaises(ValueError):
            gabarito_to_schema({"sem_schema": True})

    def test_validate_byte_level_rejeita_fence(self):
        from hefesto_llama_bridge import validate_byte_level
        ok, det = validate_byte_level('```json\n{"a": 1}\n```')
        self.assertFalse(ok)
        self.assertIn("fence_markdown", det["erros"])

    def test_validate_byte_level_aceita_json_puro(self):
        from hefesto_llama_bridge import validate_byte_level
        ok, det = validate_byte_level('{"a": 1}')
        self.assertTrue(ok, det)

    def test_validate_byte_level_schema_conformidade(self):
        if not HAS_PYDANTIC:
            self.skipTest("sem pydantic")
        from hefesto_llama_bridge import validate_byte_level
        class M(BaseModel):
            a: int
        ok, det = validate_byte_level('{"a": "texto"}', M)
        self.assertFalse(ok)  # tipo errado
        self.assertTrue(any("schema" in e for e in det["erros"]))

    def test_forja_byte_level_persiste_manifest(self):
        import tempfile, os
        from hefesto_llama_bridge import forja_byte_level, PydanticToGbnf
        # modelo de teste
        schema = {"type": "object", "properties": {"a": {"type": "integer"}}, "required": ["a"]}
        seq = ['{"a": 7}']
        calls = {"n": 0}

        def fn(**kw):
            calls["n"] += 1
            return seq[min(calls["n"] - 1, len(seq) - 1)]

        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "art.json")
            res = forja_byte_level(schema, "gere", fn, response_model=None, output_path=out)
            self.assertEqual(res["status"], "ok", res)
            self.assertTrue(os.path.exists(out))
            self.assertTrue(os.path.exists(out.replace(".json", ".manifest.json")))
            import json as _json
            self.assertEqual(_json.load(open(out))["a"], 7)

    def test_forja_motor_sampling_estrito(self):
        from hefesto_llama_bridge import ForjaMotor
        m = ForjaMotor()
        self.assertEqual(m.sampling["temperature"], 0.0)
        self.assertIn("```", m.sampling["stop"])
        schema = {"properties": {"x": {"type": "string"}, "y": {"type": "integer"}}, "type": "object"}
        n = m.max_tokens_para_schema(schema)
        self.assertGreaterEqual(n, 64)
        self.assertLessEqual(n, 2048)


if __name__ == "__main__":
    unittest.main()