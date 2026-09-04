"""test_llm_inventory.py — TDD do motor R52 (llm-inventory.py)."""
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode")
spec = importlib.util.spec_from_file_location(
    "llm_inventory_motor", ROOT / "scripts" / "llm-inventory.py"
)
inv = importlib.util.module_from_spec(spec)
sys.modules["llm_inventory_motor"] = inv
spec.loader.exec_module(inv)


class TestInventoryMotor(unittest.TestCase):
    def test_load_valido(self):
        data = inv.load()
        self.assertEqual(data["schema_version"], 1)
        self.assertGreaterEqual(len(data["models"]), 9)
        ids = [m["id"] for m in data["models"]]
        self.assertEqual(len(ids), len(set(ids)), "ids duplicados")

    def test_campos_obrigatorios(self):
        data = inv.load()
        for m in data["models"]:
            for k in ("id", "slot", "file", "category", "sector", "status", "affinity", "benchmarks", "empirical"):
                self.assertIn(k, m, f"{m['id']} falta {k}")
            self.assertIn(m["benchmarks"]["status"], {"CONFIRMED", "INFERRED", "UNKNOWN"})

    def test_validate_estrutura(self):
        data = inv.load()
        for m in data["models"]:
            self.assertIn(m["category"], inv.CATEGORIES, f"{m['id']} categoria inválida")
            for feat in inv.FEATURES:
                if feat in m["affinity"]:
                    self.assertIsInstance(m["affinity"][feat], (int, float),
                                          f"{m['id']}.{feat} não-numérico")

    def test_amalgama_bounds(self):
        data = inv.load()
        for m in data["models"]:
            for feat in inv.FEATURES:
                v = m["affinity"].get(feat)
                if isinstance(v, (int, float)):
                    self.assertTrue(0 <= v <= 5, f"{m['id']}.{feat}={v} fora de 0-5")

    def test_bench_status_consistencia(self):
        data = inv.load()
        for m in data["models"]:
            st = m["benchmarks"]["status"]
            if st == "CONFIRMED":
                self.assertTrue(m["benchmarks"].get("items"), f"{m['id']} CONFIRMED sem itens")
            self.assertTrue(m["benchmarks"].get("source"), f"{m['id']} sem source declarado")

    def test_resolve_feature_invalida_rejeita(self):
        with self.assertRaises(SystemExit):
            inv.cmd_resolve("feature-inexistente")

    def test_show_por_id_e_por_slot(self):
        data = inv.load()
        m0 = data["models"][0]
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            inv.cmd_show(m0["id"])
        self.assertIn(m0["id"], buf.getvalue(), "--show por id deve resolver")
        buf2 = io.StringIO()
        with contextlib.redirect_stdout(buf2):
            inv.cmd_show(m0["slot"])
        self.assertIn(m0["id"], buf2.getvalue(), "--show por slot deve resolver")
        with self.assertRaises(SystemExit):
            inv.cmd_show("id-inexistente-xyz")

    def test_register_caminho_inexistente_rejeita(self):
        with self.assertRaises(SystemExit):
            inv.cmd_register("ArquivoFakeNaoExiste.gguf", "9999", "judge")

    def test_categories_fechadas(self):
        expected = {"orquestrador", "descoberta", "executor", "judge", "reflexo",
                    "prosa", "tool-leve", "refutacao", "contrato-plano"}
        self.assertEqual(inv.CATEGORIES, expected)

    def test_cmd_validate_ok(self):
        inv.cmd_validate()  # não deve levantar SystemExit

    def test_cmd_probe_com_mock(self):
        sinalizado = []

        def fake_probe(port, timeout=2):
            sinalizado.append(port)
            return True

        import io
        import contextlib
        original = inv.probe
        inv.probe = fake_probe
        try:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                inv.cmd_probe()
            self.assertIn("online", buf.getvalue())
        finally:
            inv.probe = original
        expected = len(inv.load()["models"])
        self.assertEqual(len(sinalizado), expected, "probe deve visitar todos os slots")

    def test_cmd_all_roda(self):
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            inv.cmd_all()
        out = buf.getvalue()
        self.assertIn("SLOT", out)
        self.assertIn("ornith", out)


if __name__ == "__main__":
    unittest.main()
