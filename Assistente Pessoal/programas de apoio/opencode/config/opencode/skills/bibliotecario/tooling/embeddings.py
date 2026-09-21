#!/usr/bin/env python3
"""
Cliente do motor de embeddings dedicado (R96) — Bibliotecario + Split Dinâmico asyncio (2026-09-11).

Motor canonico: Qwen3-Embedding-0.6B-GGUF Q8_0 (Apache-2.0, 1024-d, PT, 32k)
  CPU :9094  -ngl 0          — 0.52s/b1, 14.7k tok/s b32, +0 VRAM, 809M RAM (tempo-real)
  GPU :9097  -ngl 99 Vulkan  — 0.12s/b1, 91k tok/s b32, +1 047M VRAM, 326M RAM (lote)

Arquitetura: produtor GM → fila asyncio → consumidor GPU b=16/32 (isolamento de código, não só roteamento).
- Query (b=1-2, prefer=auto) → CPU direto (0.52s, 0 VRAM, sem fila) — GM nunca espera lote.
- Lote (b>=3 ou prefer=gpu) → enfileira 1 texto/future por vez, consumidor drena até 32 ou 50ms e dispara 1 POST GPU → 90k tok/s, paga Vulkan 1×.

Fallback cruzado: se CPU falhar → GPU; se GPU falhar → CPU. Sem motor → None (graceful, flag vetor_placebo).
Stdlib only (asyncio + urllib + to_thread), sem aiohttp.
"""

import asyncio
import json
import urllib.request
import time

EMBED_URL_CPU = "http://127.0.0.1:9094/v1/embeddings"
EMBED_URL_GPU = "http://127.0.0.1:9097/v1/embeddings"
MODEL = "qwen3-embedding-0.6b"
DIM_ESPERADA = 1024

# --- sync low-level (usado por to_thread) ---
def _post_sync(url, texts, timeout=15):
    """POST /v1/embeddings síncrono, retorna list[vec] ou None se dim errada."""
    if isinstance(texts, str):
        texts = [texts]
    body = json.dumps({"model": MODEL, "input": texts}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read())
    vecs = [d["embedding"] for d in sorted(data["data"], key=lambda d: d["index"])]
    if any(len(v) != DIM_ESPERADA for v in vecs):
        return None
    return vecs

# --- queue GPU b=16/32 ---
_gpu_queue: asyncio.Queue = None
_gpu_worker_task = None
_FLUSH_MS = 0.05
_MAX_BATCH = 32

def _ensure_queue():
    global _gpu_queue, _gpu_worker_task
    if _gpu_queue is None:
        _gpu_queue = asyncio.Queue()
    if _gpu_worker_task is None or _gpu_worker_task.done():
        try:
            loop = asyncio.get_running_loop()
            _gpu_worker_task = loop.create_task(_gpu_consumer())
        except RuntimeError:
            pass  # sem loop -> worker sobe no próximo async
    return _gpu_queue

async def _gpu_consumer():
    """Consome 1..32 itens da fila, flush 50ms, 1 POST GPU para o lote."""
    while True:
        batch_texts = []
        batch_futs = []
        try:
            # espera primeiro item até 50ms
            text, fut = await asyncio.wait_for(_gpu_queue.get(), timeout=_FLUSH_MS)
            batch_texts.append(text)
            batch_futs.append(fut)
            # drena sem esperar até encher
            while len(batch_texts) < _MAX_BATCH:
                try:
                    t2, f2 = _gpu_queue.get_nowait()
                    batch_texts.append(t2)
                    batch_futs.append(f2)
                except asyncio.QueueEmpty:
                    break
                # pequena janela para coalescer chegadas quase simultâneas
                if len(batch_texts) >= 16:
                    await asyncio.sleep(0.01)
                    while len(batch_texts) < _MAX_BATCH:
                        try:
                            t2, f2 = _gpu_queue.get_nowait()
                            batch_texts.append(t2)
                            batch_futs.append(f2)
                        except asyncio.QueueEmpty:
                            break
                    break
        except asyncio.TimeoutError:
            continue

        # dispara lote (thread para não bloquear loop)
        try:
            vecs = await asyncio.to_thread(_post_sync, EMBED_URL_GPU, batch_texts, 15)
            if vecs is None:
                raise RuntimeError("dim errada GPU")
            for fut, vec in zip(batch_futs, vecs):
                if not fut.done():
                    fut.set_result(vec)
        except Exception as e:
            # fallback 1 a 1 na CPU se GPU falhar
            for text, fut in zip(batch_texts, batch_futs):
                if fut.done():
                    continue
                try:
                    vec = await asyncio.to_thread(_post_sync, EMBED_URL_CPU, [text], 15)
                    fut.set_result(vec[0] if vec else None)
                except Exception as e2:
                    fut.set_exception(e2)
        finally:
            for _ in batch_texts:
                _gpu_queue.task_done()

# --- API pública ---
async def embed_async(texts, timeout=15, prefer="auto"):
    """
    Async: GM produtor → consumidor GPU b=16/32 isolado.
    - str ou list[str] → list[vec] ou None
    - prefer: auto|cpu|gpu (auto: 1-2→CPU direto, 3+→fila GPU)
    """
    if isinstance(texts, str):
        texts = [texts]
        single = True
    else:
        single = False

    # caminho rápido CPU para tempo-real (sem fila)
    if prefer == "cpu" or (prefer == "auto" and len(texts) < 3):
        try:
            vecs = await asyncio.to_thread(_post_sync, EMBED_URL_CPU, texts, timeout)
            if vecs is not None:
                return vecs[0] if single else vecs
        except Exception:
            pass
        # fallback GPU
        try:
            vecs = await asyncio.to_thread(_post_sync, EMBED_URL_GPU, texts, timeout)
            return vecs[0] if single else vecs if vecs else None
        except Exception:
            return None

    # caminho lote GPU via fila (produtor → consumidor)
    _ensure_queue()
    # enfileira 1 future por texto para coalescência
    futs = []
    for t in texts:
        fut = asyncio.get_running_loop().create_future()
        await _gpu_queue.put((t, fut))
        futs.append(fut)
    try:
        vecs = await asyncio.gather(*futs)
        if any(v is None for v in vecs):
            return None
        return vecs[0] if single else vecs
    except Exception:
        return None

def embed(texts, timeout=15, prefer="auto"):
    """Sync wrapper: se há loop, delega ao async; senão, POST direto (compat)."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # sem loop → sync direto (mantém backfill.py e consultar.py antigos funcionando)
        if isinstance(texts, str):
            texts = [texts]
            single = True
        else:
            single = False
        url = EMBED_URL_CPU if (prefer == "cpu" or (prefer == "auto" and len(texts) < 3)) else EMBED_URL_GPU
        try:
            vecs = _post_sync(url, texts, timeout)
            if vecs is not None:
                return vecs[0] if single else vecs
        except Exception:
            pass
        # fallback cruzado
        alt = EMBED_URL_GPU if url == EMBED_URL_CPU else EMBED_URL_CPU
        try:
            vecs = _post_sync(alt, texts, timeout)
            return vecs[0] if single else vecs if vecs else None
        except Exception:
            return None
    else:
        # com loop → precisa await; quem chama sync dentro de async recebe coroutine
        # para não quebrar, cria task e bloqueia só se for thread separada — aqui retorna None pedindo uso de embed_async
        return None  # sinaliza: use await embed_async() quando já em async

def motor_online(timeout=3):
    for url in (EMBED_URL_CPU, EMBED_URL_GPU):
        try:
            urllib.request.urlopen(url.replace("/v1/embeddings", "/health"), timeout=timeout)
            return True
        except Exception:
            continue
    return False

if __name__ == "__main__":
    import urllib.request as _u
    for n, u in [("cpu", EMBED_URL_CPU), ("gpu", EMBED_URL_GPU)]:
        try:
            _u.urlopen(u.replace("/v1/embeddings", "/health"), timeout=2)
            print(n, "ONLINE", end=" ")
        except Exception:
            print(n, "OFFLINE", end=" ")
    print()
    # smoke async queue
    async def _smoke():
        v1 = await embed_async("ola mundo", prefer="cpu")
        print("CPU_DIM", len(v1) if v1 else "FAIL")
        v2 = await embed_async(["a", "b", "c", "d"], prefer="gpu")
        print("GPU_BATCH", len(v2) if v2 else "FAIL", "DIM", len(v2[0]) if v2 and v2[0] else "?")
    try:
        asyncio.run(_smoke())
    except Exception as e:
        print("SMOKE_FAIL", e)
