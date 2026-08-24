"""Testes TDD do Discovery Engine (T4.1/T4.2) — parser, profiler, scan, registry."""
from __future__ import annotations

import json
import struct

import pytest

from models.discovery import scan_models_dir, write_registry
from models.metadata import read_gguf_metadata
from models.profiler import (
    QUANT_PENALTY,
    confidence,
    detect_family,
    detect_quant_tag,
    estimate_vram_gib,
    param_scale,
    params_billion,
)

T_STR, T_U32, T_F32, T_ARR_STR = 8, 4, 6, 9


def _s(value: str) -> bytes:
    raw = value.encode()
    return struct.pack("<Q", len(raw)) + raw


def make_gguf(kvs):
    """Monta bytes GGUF sintéticos válidos (header + KVs, zero tensores)."""
    out = b"GGUF" + struct.pack("<IQQ", 3, 0, len(kvs))
    for key, t, v in kvs:
        out += _s(key) + struct.pack("<I", t)
        if t == T_STR:
            out += _s(str(v))
        elif t == T_U32:
            out += struct.pack("<I", v)
        elif t == T_F32:
            out += struct.pack("<f", v)
        elif t == T_ARR_STR:
            out += struct.pack("<IQ", T_STR, len(v)) + b"".join(_s(x) for x in v)
        else:
            raise AssertionError(f"tipo não suportado no fixture: {t}")
    return out


VALID_KVS = [
    ("general.architecture", T_STR, "qwen"),
    ("general.name", T_STR, "FakeQwen 9B"),
    ("general.size_label", T_STR, "9B"),
    ("qwen.context_length", T_U32, 131072),
    ("qwen.block_count", T_U32, 28),
    ("qwen.attention.head_count_kv", T_U32, 8),
    ("qwen.attention.key_length", T_U32, 128),
    ("tokenizer.ggml.tokens", T_ARR_STR, ["a", "bb", "ccc"]),
]


def test_parser_reads_scalars_and_skips_vocab(tmp_path):
    p = tmp_path / "m.gguf"
    p.write_bytes(make_gguf(VALID_KVS))
    meta = read_gguf_metadata(p)
    assert meta["general.architecture"] == "qwen"
    assert meta["qwen.context_length"] == 131072
    assert meta["qwen.attention.head_count_kv"] == 8
    assert "tokenizer.ggml.tokens" not in meta
    assert meta["file_size_bytes"] == p.stat().st_size


@pytest.mark.parametrize("bad", [b"", b"NOTG", b"GGUF\x03"])
def test_parser_rejects_invalid(tmp_path, bad):
    p = tmp_path / "bad.gguf"
    p.write_bytes(bad)
    with pytest.raises((ValueError, struct.error)):
        read_gguf_metadata(p)


def test_detect_quant_and_family():
    assert detect_quant_tag("Modelo-X-27B-UD-IQ2_XXS.gguf") == "IQ2_XXS"
    assert detect_quant_tag("sem-tag.gguf") == "Q4_K_M"
    assert detect_family("Ornith-1.5-9B", None) == "ornith"
    assert detect_family("qq qualquer", "llama") == "llama"
    assert detect_family("zzz", None) == "desconhecida"


def test_param_math_bounds():
    assert params_billion({"general.size_label": "27B"}, 0, "Q4_K_M") == 27.0
    assert 22.0 <= params_billion({}, 8.4, "IQ2_XXS") <= 30.0
    s9, s27 = param_scale(9.0), param_scale(27.0)
    assert 0.95 <= s9 <= 1.05 and s27 == pytest.approx(1.08)
    assert confidence(0) == 0.0 and confidence(90) == 0.9


def test_vram_monotonic_and_override():
    meta = {}
    for k, t, v in VALID_KVS:
        if t == T_U32 and k.endswith(("block_count", "head_count_kv", "key_length")):
            meta[k] = v
        elif k == "general.size_label":
            meta[k] = v
    meta["file_size_bytes"] = 5_300_000_000
    lo = estimate_vram_gib(meta, "fake-x", 8192)
    hi = estimate_vram_gib(meta, "fake-x", 131072)
    assert 0 < lo < hi
    assert estimate_vram_gib({}, "ornith-1-5-9b-q4-k-m", 32768) == 14.2
    assert estimate_vram_gib({}, "qwen38-9b-q4-k-m", 32768) == 14.9


def test_scan_excludes_corrupted(tmp_path):
    (tmp_path / "quebrado-Q4_K_M.gguf").write_bytes(b"\x00trash")
    reg = scan_models_dir(tmp_path)
    m = reg["models"]["quebrado-q4-k-m"]
    assert m["status"]["excluded"]
    assert m["status"]["exclusion_reason"].startswith("metadata_unreadable")


def test_scan_includes_valid_synthetic(tmp_path):
    (tmp_path / "FakeQwen-9B-Q4_K_M.gguf").write_bytes(make_gguf(VALID_KVS))
    reg = scan_models_dir(tmp_path)
    assert reg["total_models"] == 1 and reg["available_models"] == 1
    m = reg["models"]["fakeqwen-9b-q4-k-m"]
    assert m["architecture"]["family"] == "qwen"
    assert m["architecture"]["context_length"] == 131072
    assert m["capabilities"]["estimated"]["coding"] > 0.5
    assert m["capabilities"]["confidence"] == 0.0
    assert m["roles_suitability"]["planner"] > 0.5
    assert m["backend"] == {"format": "gguf", "compatible": ["llama.cpp"]}
    assert reg["reference_ctx"] == 32768


def test_scan_blacklist_and_vram_rule(tmp_path):
    (tmp_path / "Bloqueado-Q4_K_M.gguf").write_bytes(make_gguf(VALID_KVS))
    reg = scan_models_dir(tmp_path, blacklist={"bloqueado"})
    assert reg["models"]["bloqueado-q4-k-m"]["status"]["exclusion_reason"] == "user_blacklist"

    huge = lambda meta, mid, ctx: 99.0
    (tmp_path / "Gigante-Q4_K_M.gguf").write_bytes(make_gguf(VALID_KVS))
    reg2 = scan_models_dir(tmp_path, blacklist=set(), vram_estimator=huge)
    assert "vram_insufficient" in reg2["models"]["gigante-q4-k-m"]["status"]["exclusion_reason"]


def test_scan_yellow_zone(tmp_path):
    (tmp_path / "Apertado-Q4_K_M.gguf").write_bytes(make_gguf(VALID_KVS))
    reg = scan_models_dir(tmp_path, vram_available_gib=16.0, vram_estimator=lambda m, i, c: 15.0)
    m = reg["models"]["apertado-q4-k-m"]
    assert m["status"]["available"] and m["health"]["status"] == "YELLOW"
    assert m["resources"]["vram_warning"] is True

    reg2 = scan_models_dir(tmp_path, vram_available_gib=16.0, vram_estimator=lambda m, i, c: 16.5)
    excluido = reg2["models"]["apertado-q4-k-m"]
    assert not excluido["status"]["available"]
    assert "vram_insufficient" in excluido["status"]["exclusion_reason"]


def test_family_by_filename_beats_internal_arch(tmp_path):
    # finetune Ornith carrega arquitetura interna qwen: o arquivo deve vencer
    (tmp_path / "Ornith-Mix-Q4_K_M.gguf").write_bytes(make_gguf(VALID_KVS))
    reg = scan_models_dir(tmp_path)
    m = reg["models"]["ornith-mix-q4-k-m"]
    assert m["architecture"]["family"] == "ornith"
    assert m["capabilities"]["estimated"]["coding"] < 0.85


def test_measured_trio_not_hard_excluded(tmp_path):
    # âncora GMB-1: a tríade medida CARREGOU na MI50 física de 16GiB
    for name in (
        "Ornith-1.5-9B-Q4_K_M.gguf",
        "Qwen3.8-9B-Q4_K_M.gguf",
        "Qwen3.8-27B-UD-IQ2_XXS.gguf",
    ):
        (tmp_path / name).write_bytes(make_gguf(VALID_KVS))
    reg = scan_models_dir(tmp_path)
    for gid, expect in (
        ("ornith-1-5-9b-q4-k-m", 14.2),
        ("qwen3-8-9b-q4-k-m", 14.9),
        ("qwen3-8-27b-ud-iq2-xxs", 15.7),
    ):
        m = reg["models"][gid]
        assert m["status"]["available"], (gid, m["status"])
        assert m["resources"]["estimated_vram_gib"] == expect
        assert m["health"]["status"] == "YELLOW"
        assert m["resources"]["vram_warning"] is True


def test_registry_roundtrip(tmp_path):
    (tmp_path / "A-Q4_K_M.gguf").write_bytes(make_gguf(VALID_KVS))
    reg = scan_models_dir(tmp_path)
    out = write_registry(reg, tmp_path / "registry.json")
    loaded = json.loads(out.read_text(encoding="utf-8"))
    assert set(loaded["models"]) == set(reg["models"])
    assert loaded["total_models"] == reg["total_models"]
