"""Parser de metadados GGUF sem carregar tensores (T4.1).

Estratégia: parser mínimo próprio sobre mmap — lê apenas os KV do cabeçalho
necessários ao discovery e PULA arrays (ex.: vocabulário) sem materializá-los,
garantindo varredura de todo o MODEL_LIBRARY em <30s (critério [1] da SPEC).
"""
from __future__ import annotations

import mmap
import struct
from pathlib import Path
from typing import Any, Dict

GGUF_MAGIC = b"GGUF"

# tipos escalares GGUF -> fmt struct (little-endian)
_SCALARS: Dict[int, str] = {
    0: "<B",   # u8
    1: "<b",   # i8
    2: "<H",   # u16
    3: "<h",   # i16
    4: "<I",   # u32
    5: "<i",   # i32
    6: "<f",   # f32
    7: "<?",   # bool
    10: "<Q",  # u64
    11: "<q",  # i64
    12: "<d",  # f64
}

# chaves exatas e sufixos por-arquitetura que interessam ao discovery
_KEYS_EXACT = {"general.architecture", "general.name", "general.size_label"}
_KEY_SUFFIXES = (
    ".context_length",
    ".block_count",
    ".embedding_length",
    ".attention.head_count_kv",
    ".attention.key_length",
    ".attention.value_length",
)


def _read_str(buf: mmap.mmap, off: int):
    """Lê string GGUF (u64 len + bytes). Retorna (str, novo_offset)."""
    (n,) = struct.unpack_from("<Q", buf, off)
    off += 8
    raw = bytes(buf[off : off + n])
    return raw.decode("utf-8", errors="replace"), off + n


def _read_value(buf: mmap.mmap, off: int, vtype: int):
    """Lê ou pula um valor conforme o tipo. Retorna (valor_ou_None, novo_offset).

    Arrays são sempre pulados (None): vocabulário não agrega ao routing e
    materializá-lo custaria segundos por arquivo.
    """
    if vtype == 8:  # string
        return _read_str(buf, off)
    if vtype == 9:  # array
        (etype,) = struct.unpack_from("<I", buf, off)
        off += 4
        (count,) = struct.unpack_from("<Q", buf, off)
        off += 8
        if etype == 8:  # array de strings: pula lendo cada tamanho
            for _ in range(count):
                _, off = _read_str(buf, off)
            return None, off
        if etype in _SCALARS:
            step = struct.calcsize(_SCALARS[etype])
            return None, off + count * step
        raise ValueError(f"tipo de elemento de array inválido: {etype}")
    if vtype in _SCALARS:
        fmt = _SCALARS[vtype]
        (val,) = struct.unpack_from(fmt, buf, off)
        if vtype == 7:
            val = bool(val)
        return val, off + struct.calcsize(fmt)
    raise ValueError(f"tipo GGUF desconhecido: {vtype}")


def read_gguf_metadata(path: str | Path) -> Dict[str, Any]:
    """Extrai os KVs relevantes do cabeçalho GGUF.

    Levanta ValueError (arquivo inválido/truncado) ou OSError — chamador deve
    tratar como metadata_unreadable. Nunca lê dados de tensores.
    """
    p = Path(path)
    size = p.stat().st_size
    if size < 24:
        raise ValueError(f"arquivo pequeno demais para GGUF ({size}B)")
    with open(p, "rb") as fh:
        if fh.read(4) != GGUF_MAGIC:
            raise ValueError("magic GGUF inválido")
        mm = mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            version, tensor_count, kv_count = struct.unpack_from("<IQQ", mm, 4)
            off = 24
            meta: Dict[str, Any] = {
                "_gguf_version": version,
                "_tensor_count": tensor_count,
                "_kv_count": kv_count,
                "file_size_bytes": size,
            }
            for _ in range(kv_count):
                key, off = _read_str(mm, off)
                if off + 4 > len(mm):
                    raise ValueError("KV truncado no cabeçalho")
                (vtype,) = struct.unpack_from("<I", mm, off)
                off += 4
                val, off = _read_value(mm, off, vtype)
                if val is None:
                    continue
                if key in _KEYS_EXACT or key.endswith(_KEY_SUFFIXES):
                    meta[key] = val
            return meta
        finally:
            mm.close()
