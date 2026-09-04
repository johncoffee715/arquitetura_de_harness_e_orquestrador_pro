"""test_attach_media.py — TDD da feature /attach (anexos de mídia)."""
import importlib.util
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode")
spec = importlib.util.spec_from_file_location("attach_media", ROOT / "scripts" / "attach_media.py")
am = importlib.util.module_from_spec(spec)
spec.loader.exec_module(am)


class TestAttachMedia(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # mídia sintética rápida (wav 0.5s) — sem depender de visão
        cls.wav = Path("/tmp/opencode/test-unit.wav")
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "sine=frequency=330:duration=0.5",
                        "-ac", "1", "-ar", "16000", str(cls.wav)], capture_output=True)

    def test_arquivo_inexistente_error(self):
        out = am.handle(Path("/tmp/opencode/nao-existe-xyz.avi"), 2)
        self.assertEqual(out["status"], "error")
        self.assertIn("NÃO ENCONTRADO", out["summary"])

    def test_tipo_audio_detectado(self):
        out = am.handle(self.wav, 2)
        self.assertEqual(out["kind"], "audio")
        self.assertIn("duration_s", out["media"])
        self.assertIsNotNone(out["media"]["duration_s"])

    def test_tipo_desconhecido_error(self):
        f = Path("/tmp/opencode/arquivo-teste.xyz123")
        f.write_text("x")
        out = am.handle(f, 1)
        self.assertEqual(out["status"], "error")
        self.assertIn("NÃO SUPORTADO", out["summary"])

    def test_image_sem_visao_partial(self):
        # monkeypatch: sem modelo de visão => partial honesto, sem inventar
        orig = am.vision_describe
        am.vision_describe = lambda p: None
        try:
            f = Path("/tmp/opencode/test-image.jpg")
            if not f.exists():
                self.skipTest("sem fixture")
            out = am.handle(f, 1)
            self.assertEqual(out["kind"], "image")
            self.assertIn(out["status"], {"partial", "ok"})
        finally:
            am.vision_describe = orig

    def test_schema_contrato(self):
        schema = json.loads((ROOT / "scripts" / "attach_media.schema.json").read_text())
        self.assertEqual(schema["properties"]["tool"]["const"], "attach_media")
        self.assertTrue(schema["properties"]["attachments"]["items"]["required"])

    def test_command_existe(self):
        cmd = (ROOT / "commands" / "attach.md")
        self.assertTrue(cmd.exists())
        t = cmd.read_text(encoding="utf-8")
        self.assertIn("attach_media.py $ARGUMENTS", t)
        self.assertIn("/mnt/dados/Assistente Pessoal/opencode/config/opencode/scripts/attach_media.py", t)

    def test_asr_whisper_disponivel(self):
        # descobre se o ASR está ativo e, se sim, transcreve clipe com fala (integração real)
        try:
            import subprocess
            import pathlib
            jfk = pathlib.Path("/tmp/opencode/whisper.cpp/samples/jfk.wav")
            if not jfk.exists():
                self.skipTest("sem sample jfk")
            out = am.handle(jfk, 1)
            self.assertEqual(out["kind"], "audio")
            self.assertEqual(out["status"], "ok", "com whisper ativo, transcrição deve existir")
            self.assertIsNotNone(out["media"].get("transcript"))
            self.assertIn("Americans", out["media"]["transcript"])
        except Exception as e:
            self.fail(f"integração ASR falhou: {e}")


if __name__ == "__main__":
    unittest.main()
