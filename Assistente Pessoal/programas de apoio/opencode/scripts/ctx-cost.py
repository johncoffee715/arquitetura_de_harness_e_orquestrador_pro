#!/usr/bin/env python3
# ctx-cost.py — custo de KV cache por LLM (regra global: todo -c de slot nasce desta conta)
# Uso:
#   ctx-cost.py <gguf> [-c N] [--k q4_0] [--v q4_0]
#   ctx-cost.py --all            # tabela da stack CPU inteira
import argparse
import glob
import json
import struct
import sys

MODELS_DIR = "/mnt/dados/Assistente Pessoal/modelos LLM"

# bytes por elemento por quantização (llama.cpp)
BPW = {"f16": 2.0, "q8_0": 1.125, "q6_K": 0.82, "q5_1": 0.8125,
       "q5_0": 0.75, "q4_1": 0.6875, "q4_0": 0.625, "q4_K": 0.5625, "iq4_nl": 0.55}

# STACK_CPU: GERADO por sync-llm-stack.py · leitura DINÂMICA do manifesto (não editar à mão)

MANIFESTO_PATH = "/mnt/dados/Assistente Pessoal/modelos LLM/manifesto_llm.json"


def _load_stack_cpu():
    """Lê a stack CPU (device != GPU) dinamicamente do manifesto_llm.json (fonte única)."""
    try:
        with open(MANIFESTO_PATH, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:
        print(f"ctx-cost: manifesto ilegível ({exc}) — STACK_CPU vazio", file=sys.stderr)
        return []
    rows = []
    for m in data.get("models", []):
        if str(m.get("device", "CPU")).upper() == "GPU":
            continue  # slot GPU (8083) usa compute_ornith_ctx no start-stack.sh
        fi = m.get("fisica_inferencia", {}) or {}
        arch = m.get("topologia_arquitetura", {}) or {}
        ctx = fi.get("ctx_ativo") or arch.get("contexto_nativo") or 4096
        rows.append((str(m.get("slot_port", 0)), _gguf_for(m.get("model_id", "")),
                     int(ctx), _papel(m.get("vocacao_grafo", ""))))
    return rows


def _gguf_for(model_id):
    import glob as _glob
    import re as _re

    def _n(s):
        return _re.sub(r"[^a-z0-9]", "", s.lower())

    tgt = _n(model_id)
    for f in sorted(_glob.glob(f"{MODELS_DIR}/*.gguf")):
        base = f.rsplit("/", 1)[-1][:-5]
        if _n(base) == tgt or _n(base).startswith(tgt) or tgt.startswith(_n(base)):
            return base + ".gguf"
    return model_id + ".gguf"


def _papel(voc):
    voc = (voc or "").strip()
    return voc.split("·")[0].strip().split(";")[0].strip() or "—"


STACK_CPU = _load_stack_cpu()




def read_header(path):
    """Extrai topologia KV do header GGUF (arquiteturas qwen2/3/3.5, lfm2, bitnet)."""
    with open(path, "rb") as f:
        f.read(8)
        struct.unpack("<Q", f.read(8))
        n_kv = struct.unpack("<Q", f.read(8))[0]

        def rs():
            l = struct.unpack("<Q", f.read(8))[0]
            return f.read(l).decode(errors="replace")

        def rv(t):
            if t == 4: return struct.unpack("<I", f.read(4))[0]
            if t == 5: return struct.unpack("<i", f.read(4))[0]
            if t == 6: return struct.unpack("<f", f.read(4))[0]
            if t == 7: return struct.unpack("<?", f.read(1))[0]
            if t == 8: return rs()
            if t == 9:
                et = struct.unpack("<I", f.read(4))[0]
                n = struct.unpack("<Q", f.read(8))[0]
                return [rv(et) for _ in range(n)]
            if t == 10: return struct.unpack("<Q", f.read(8))[0]
            raise ValueError(f"tipo {t}")

        h = {}
        for _ in range(n_kv):
            k = rs()
            t = struct.unpack("<I", f.read(4))[0]
            h[k] = rv(t)

    def pick(*suffixes):
        for pref in ("qwen35", "qwen3", "qwen2", "lfm2", "bitnet", "granite", "rwkv7"):
            for s in suffixes:
                key = f"{pref}.{s}"
                if key in h:
                    return h[key]
        return None

    layers = pick("block_count")
    n_heads = pick("attention.head_count")
    kvh = pick("attention.head_count_kv")
    key_len = pick("attention.key_length")
    emb = None
    for k, v in h.items():
        if k.endswith("embedding_length") and isinstance(v, int):
            emb = v
            break
    ctx_native = pick("context_length")
    arch = next((p for p in ("qwen35", "qwen3", "qwen2", "lfm2", "bitnet", "granite") if f"{p}.block_count" in h), "?")

    # LFM2 híbrido: apenas camadas com kv_heads > 0 têm KV cache tradicional
    attn_layers = layers
    if isinstance(kvh, list):
        attn_layers = sum(1 for x in kvh if x > 0)
        kvh = max(kvh) if any(x > 0 for x in kvh) else 0

    if key_len is None and emb and n_heads:
        key_len = emb // n_heads
    kv_dim = (kvh or 0) * (key_len or 0)

    return {"arch": arch, "layers": layers, "attn_layers": attn_layers,
            "kv_dim": kv_dim, "ctx_native": ctx_native}


def cost(path, c, kq="q4_0", vq="q4_0"):
    h = read_header(path)
    bpw_k = BPW.get(kq, 2.0) * 1024  # B/el → KB/el base 1000? não: manter bytes
    kb_tok = h["attn_layers"] * h["kv_dim"] * (BPW[kq] + BPW[vq]) / 1024.0  # KB/tok
    gb = kb_tok * 1024 * c / 1e9
    return {**h, "kb_tok": round(kb_tok, 1), "gb_at_c": round(gb, 2), "c": c,
            "max_c_4gb": int(4 * 1e9 / (kb_tok * 1024)) if kb_tok > 0 else 0}  # state fixo (RWKV): custo não escala com ctx


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("gguf", nargs="?", help="caminho do GGUF ou nome no MODELS_DIR")
    ap.add_argument("-c", type=int, default=4096)
    ap.add_argument("--k", default="q4_0", choices=list(BPW))
    ap.add_argument("--v", default="q4_0", choices=list(BPW))
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()

    if a.all:
        print(f"{'slot':<6} {'modelo':<34} {'KB/tok':>7} {'-c':>7} {'KV GB':>7} {'papel'}")
        total = 0.0
        for slot, f, c, papel in STACK_CPU:
            r = cost(f"{MODELS_DIR}/{f}", c, a.k, a.v)
            total += r["gb_at_c"]
            print(f"{slot:<6} {f:<34} {r['kb_tok']:>7.1f} {c:>7} {r['gb_at_c']:>7.2f} {papel}")
        print(f"{'':<49}{'TOTAL':>7} {total:>7.2f}")
        return

    path = a.gguf if "/" in a.gguf else f"{MODELS_DIR}/{a.gguf}"
    r = cost(path, a.c, a.k, a.v)
    print(json.dumps(r, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
