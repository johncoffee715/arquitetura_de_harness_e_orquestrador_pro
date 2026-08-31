#!/usr/bin/env python3
"""attach_media.py — anexa mídia (imagem/vídeo/áudio) ao contexto do orquestrador.

Fluxo (hefesto 2026-08-26, tripé .py/.md/.json — R51):
  1. Detecta tipo por extensão/mime.
  2. IMAGEM: metadata (ffprobe) + tentativa de descrição/OCR via modelo de visão local
     (Ollama qwen3.5:0.8b — R31/R35). Sem visão disponível -> status partial, summary
     declara "sem modelo de visão (ollama vazio)" — honesto, nunca inventa descrição.
     ⚠️ DESCONTINUADO 2026-08-28 (decisão usuário): backend de visão qwen3.5:0.8b/Ollama
     removido do roteamento; VISION_MODEL fica "" (desativado) por padrão. Para reativar,
     setar ATTACH_VISION_MODEL com um modelo oficialmente canonizado no inventário (R35 novo).
  3. VÍDEO: ffprobe (duração/resolução/fps/codec) + ffmpeg extrai N keyframes para
     /tmp/opencode/attach-frames/ (sandbox tmp permitido pelo guard) + tentativa de
     visão nos frames. Flag --frames N controla quantidade (default 3, máx 6).
  4. ÁUDIO: ffprobe + transcodifica p/ wav 16k mono (ffmpeg) + transcrição se whisper
     estiver disponível (binário "whisper" ou "whisper-cli"); senão partial honesto.
  5. Saída: JSON conforme attach_media.schema.json (contrato estrito, additionalProperties
     false) — o orquestrador cola o resumo no contexto e referencia os caminhos.
  Execução viva: ffmpeg/ffprobe obrigatórios; tudo em /tmp/opencode (área pré-aprovada).
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

VERSION = "1.0.1"
TMP = Path("/tmp/opencode")
FRAMES_DIR = TMP / "attach-frames"
VISION_API = "http://127.0.0.1:11434/api/generate"
# DESCONTINUADO 2026-08-28: qwen3.5:0.8b/Ollama removido do roteamento (decisão usuário).
# Vazio = visão desativada; para reativar, canonizar modelo de visão no inventário e setar ATTACH_VISION_MODEL.
VISION_MODEL = os.environ.get("ATTACH_VISION_MODEL", "")
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff"}
VIDEO_EXTS = {".mp4", ".mov", ".webm", ".mkv", ".avi", ".m4v"}
AUDIO_EXTS = {".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac", ".opus", ".wma"}
WHISPER_BIN = (
    shutil.which("whisper")
    or shutil.which("whisper-cli")
    or "/tmp/opencode/whisper.cpp/build/bin/whisper-cli"
)
WHISPER_MODEL = os.environ.get(
    "ATTACH_WHISPER_MODEL", "/tmp/opencode/whisper.cpp/models/ggml-base.bin"
)


def run(cmd, timeout=120):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout + p.stderr


def ffprobe_meta(path: Path) -> dict:
    meta = {"json": None, "raw": ""}
    ok, out = run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)])
    if ok != 0:
        return meta
    try:
        meta["json"] = json.loads(out)
    except Exception:
        meta["raw"] = out[:200]
    return meta


def summarize_media(meta: dict) -> dict:
    m = {"duration_s": None, "width": None, "height": None, "fps": None, "codec": None, "format": None}
    j = meta.get("json") or {}
    fmt = j.get("format") or {}
    m["duration_s"] = fmt.get("duration") and float(fmt["duration"])
    m["format"] = fmt.get("format_name")
    streams = j.get("streams") or []
    for s in streams:
        if s.get("codec_type") == "video":
            m["width"] = s.get("width")
            m["height"] = s.get("height")
            m["fps"] = _parse_fps(s.get("avg_frame_rate") or s.get("r_frame_rate"))
            m["codec"] = s.get("codec_name")
            break
        if s.get("codec_type") == "audio" and not m["codec"]:
            m["codec"] = s.get("codec_name")
    return m


def _parse_fps(rate: str | None) -> float | None:
    if not rate or "/" not in rate:
        return None
    a, b = rate.split("/")
    try:
        v = float(a) / float(b)
        return round(v, 2) if 0 < v < 1000 else None
    except Exception:
        return None


def vision_available() -> bool:
    """Visão descontinuada: só disponível se ATTACH_VISION_MODEL for explicitamente setado
    (modelo canonizado no inventário) E o Ollama responder. Decisão usuário 2026-08-28."""
    if not VISION_MODEL:
        return False
    try:
        urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=5)
        return True
    except Exception:
        return False


def vision_describe(image_path: Path) -> str | None:
    """Tenta descrição via Ollama (multiimodal, R31/R35). Sem modelo => None (honesto).

    Cold-start do modelo de visão pode levar >60s na 1ª chamada — timeout 240s.
    """
    if not vision_available():
        return None
    import base64
    data = base64.b64encode(image_path.read_bytes()).decode()
    payload = json.dumps({
        "model": VISION_MODEL,
        "prompt": "Descreva em português o conteúdo desta imagem em 1-2 frases (objetos, texto visível OCR).",
        "images": [data],
        "stream": False,
    }).encode()
    try:
        req = urllib.request.Request(VISION_API, data=payload, headers={"Content-Type": "application/json"})
        resp = json.loads(urllib.request.urlopen(req, timeout=240).read())
        return resp.get("response") or None
    except Exception:
        return None


def extract_frames(video: Path, n: int) -> list[str]:
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    stem = video.stem.replace(" ", "_")[:40]
    out_root = FRAMES_DIR / stem
    out_root.mkdir(exist_ok=True)
    ok, _ = run([
        "ffmpeg", "-y", "-i", str(video), "-vf", f"fps=1/2,scale=800:-1",
        "-frames:v", str(n), str(out_root / "f%02d.jpg"),
    ], timeout=180)
    if ok != 0 or not list(out_root.glob("*.jpg")):
        # fallback: 1 frame no meio
        run(["ffmpeg", "-y", "-i", str(video), "-frames:v", "1", "-vf", "scale=800:-1",
             str(out_root / "f01.jpg")], timeout=180)
    return [str(p) for p in sorted(out_root.glob("*.jpg"))]


def transcript_audio(wav: Path) -> str | None:
    if not WHISPER_BIN or not Path(WHISPER_BIN).exists():
        return None
    if not Path(WHISPER_MODEL).exists():
        return None
    out_txt = wav.with_suffix(".txt")
    try:
        run([WHISPER_BIN, "-m", WHISPER_MODEL, "-f", str(wav), "-nt", "-otxt",
             "-of", str(wav.with_suffix(""))], timeout=600)
    except Exception:
        return None
    if out_txt.exists():
        text = out_txt.read_text(encoding="utf-8", errors="replace").strip()
        return text if text else None
    return None


def handle(path: Path, frames: int) -> dict:
    base = {"path": str(path), "media": {}}
    if not path.exists():
        return {**base, "kind": "unknown", "status": "error", "summary": f"ARQUIVO NÃO ENCONTRADO: {path}", "media": {"error": "not found"}}
    size = path.stat().st_size
    ext = path.suffix.lower()
    kind = "image" if ext in IMAGE_EXTS else "video" if ext in VIDEO_EXTS else "audio" if ext in AUDIO_EXTS else "unknown"
    m = summarize_media(ffprobe_meta(path)); m["size_bytes"] = size
    m.setdefault("frames", []); m.setdefault("transcript", None)
    base["media"] = m
    if kind == "image":
        desc = vision_describe(path)
        if desc:
            m["transcript"] = desc
            return {**base, "kind": kind, "status": "ok",
                    "summary": f"IMAGEM {path.name} ({size//1024} KB): {desc}"}
        return {**base, "kind": kind, "status": "partial",
                "summary": f"IMAGEM {path.name} ({size//1024} KB) — anexada estruturalmente; SEM modelo de visão ativo (Ollama vazio), não consigo descrever o conteúdo. Para descrição: `ollama pull qwen3.5:0.8b` (R31)."}
    if kind == "video":
        fr = extract_frames(path, frames)
        m["frames"] = fr
        if fr:
            desc = vision_describe(Path(fr[0])) if vision_available() else None
            if desc:
                m["transcript"] = desc
                return {**base, "kind": kind, "status": "ok",
                        "summary": f"VÍDEO {path.name}: {m.get('duration_s', '?')}s, {m.get('width')}x{m.get('height')}, {m.get('fps')}fps, {m.get('codec')}. {len(fr)} frames: {', '.join(fr)}. 1ª cena: {desc}"}
            return {**base, "kind": kind, "status": "partial",
                    "summary": f"VÍDEO {path.name}: {m.get('duration_s', '?')}s, {m.get('width')}x{m.get('height')}, {m.get('fps')}fps, {m.get('codec')}. {len(fr)} frames extraídos: {', '.join(fr)} — sem visão ativa; frames disponíveis para leitura."}
        return {**base, "kind": kind, "status": "error",
                "summary": f"VÍDEO {path.name}: ffmpeg falhou ao extrair frames — {path}"}
    if kind == "audio":
        wav = TMP / (path.stem.replace(" ", "_")[:40] + ".wav")
        run(["ffmpeg", "-y", "-i", str(path), "-ac", "1", "-ar", "16000", str(wav)], timeout=180)
        tr = transcript_audio(wav) if wav.exists() else None
        if tr:
            m["transcript"] = tr
            return {**base, "kind": kind, "status": "ok",
                    "summary": f"ÁUDIO {path.name}: {m.get('duration_s', '?')}s, {m.get('codec')}. TRANSCRIÇÃO: {tr[:600]}"}
        return {**base, "kind": kind, "status": "partial",
                "summary": f"ÁUDIO {path.name}: {m.get('duration_s', '?')}s — Sem fala detectada ou ASR indisponível; wav 16k em {wav}. (whisper ativo: {Path(WHISPER_BIN).exists()})"}
    return {**base, "kind": "unknown", "status": "error", "summary": f"TIPO NÃO SUPORTADO: {path} (ext {ext})"}


def main(argv: list[str]) -> int:
    if not argv:
        print(json.dumps({"tool": "attach_media", "version": VERSION, "generated_at": datetime.now(timezone.utc).isoformat(),
                          "attachments": [],
                          "error": "Uso: attach_media.py [--frames N] <arquivo...>"}, ensure_ascii=False, indent=2))
        return 1
    frames = 3
    paths = list(argv)
    if argv[0] == "--frames":
        frames = min(int(argv[1]), 6); paths = argv[2:]
    out = {"tool": "attach_media", "version": VERSION,
           "generated_at": datetime.now(timezone.utc).isoformat(),
           "attachments": [handle(Path(p), frames) for p in paths]}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:])) 
