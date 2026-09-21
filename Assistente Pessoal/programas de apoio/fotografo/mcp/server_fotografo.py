"""Servidor MCP stdio da feature Fotógrafo — Academy of Eletronic.

6 tools (contrato canônico):
  search_references | draft_generate | analyze_reference |
  display_locally | render_final | status_job

Regras: config por env, LOG MELT append-only em logs/mcp.jsonl,
erros nunca silenciados (msg bruta), nenhum subprocess bloqueante
além do poll de history, paths retornados absolutos.
Sem torch/CUDA aqui — só httpx + stdlib + pillow (base64).
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import random
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------- base paths
BASE_DIR = Path(__file__).resolve().parent.parent  # fotografo/
WORKFLOWS_DIR = BASE_DIR / "workflows"
REFS_DIR = BASE_DIR / "refs"
REFS_WEB = REFS_DIR / "web"
REFS_DRAFT = REFS_DIR / "draft"
REFS_VIDEO = REFS_DIR / "video"
LOGS_DIR = BASE_DIR / "logs"
SCHEMAS_DIR = BASE_DIR / "schemas"

for _d in (REFS_WEB, REFS_DRAFT, REFS_VIDEO, LOGS_DIR, SCHEMAS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

MELT_LOG = LOGS_DIR / "mcp.jsonl"

# ---------------------------------------------------------------- config (env)
COMFY_URL = os.environ.get("COMFY_URL", "http://127.0.0.1:8188").rstrip("/")
FOTOGRAFO_LLM = os.environ.get("FOTOGRAFO_LLM", "http://127.0.0.1:9188/v1").rstrip("/")
DISPLAY_CMD = os.environ.get("DISPLAY_CMD", "xdg-open")

# ---------------------------------------------------------------- persona DoP
PERSONA_FOTODESIGNER = (
    "Tu és o FOTODESIGNER, diretor de fotografia técnico-industrial da "
    "Academy of Eletronic. Composição planejada, hierarquia visual clara, "
    "pesos visuais equilibrados, direção de arte precisa, paleta ouro "
    "canônico #A3A44A sobre preto #0A0C0C, mascote ciborgue quando couber. "
    "Pós-produção alinhada à marca. Responde APENAS com JSON válido contendo "
    "EXATAMENTE as chaves: camera_angle, lighting_and_style, "
    "technical_subjects (todas string). Sem markdown, sem comentário."
)

DOP_KEYS = ("camera_angle", "lighting_and_style", "technical_subjects")

mcp = FastMCP("fotografo")


# ---------------------------------------------------------------- MELT log
def _args_hash(args: dict) -> str:
    bruto = json.dumps(args, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(bruto.encode("utf-8")).hexdigest()[:12]


def _melt(tool: str, args: dict, dur_ms: int, exit_status: str, ref: str = "") -> None:
    linha = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "tool": tool,
        "args_hash": _args_hash(args),
        "dur_ms": dur_ms,
        "exit_status": exit_status,
        "ref": ref,
    }
    try:
        with open(MELT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(linha, ensure_ascii=False) + "\n")
    except OSError:
        pass  # log nunca pode quebrar a tool


def _slug(texto: str) -> str:
    s = texto.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s[:40] or "ref"


def _ler_schema_gbnf() -> str:
    p = SCHEMAS_DIR / "dop_schema.gbnf"
    if p.exists():
        return p.read_text(encoding="utf-8")
    return ""


# ---------------------------------------------------------------- ComfyUI HTTP
def _post_prompt(workflow: dict) -> str:
    """POST /prompt -> prompt_id. Erro bruto, nunca silenciado."""
    url = f"{COMFY_URL}/prompt"
    try:
        r = httpx.post(url, json={"prompt": workflow}, timeout=30.0)
        r.raise_for_status()
    except Exception as e:
        raise RuntimeError(f"ComfyUI offline ou POST /prompt falhou ({url}): {e}") from e
    try:
        dado = r.json()
    except Exception as e:
        raise RuntimeError(f"ComfyUI retornou corpo não-JSON em /prompt: {e} :: {r.text[:500]}") from e
    pid = dado.get("prompt_id")
    if not pid:
        raise RuntimeError(f"ComfyUI /prompt sem prompt_id: {dado}")
    return str(pid)


def _get_history(prompt_id: str) -> dict:
    url = f"{COMFY_URL}/history/{prompt_id}"
    try:
        r = httpx.get(url, timeout=30.0)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        raise RuntimeError(f"ComfyUI GET /history/{prompt_id} falhou ({url}): {e}") from e


def _baixar_view(filename: str, subfolder: str, ftype: str, destino: Path) -> Path:
    url = f"{COMFY_URL}/view"
    params = {"filename": filename, "subfolder": subfolder, "type": ftype}
    try:
        r = httpx.get(url, params=params, timeout=120.0)
        r.raise_for_status()
    except Exception as e:
        raise RuntimeError(f"ComfyUI GET /view falhou ({filename}): {e}") from e
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(r.content)
    return destino.resolve()


def _template(nome: str, trocas: dict[str, str]) -> dict:
    """Carrega workflow API e substitui placeholders {{X}} (texto antes do parse)."""
    arq = WORKFLOWS_DIR / nome
    if not arq.exists():
        raise RuntimeError(f"Template de workflow ausente: {arq}")
    bruto = arq.read_text(encoding="utf-8")
    for k, v in trocas.items():
        bruto = bruto.replace("{{" + k + "}}", v)
    try:
        return json.loads(bruto)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Template {nome} inválido após substituição: {e}") from e


def _aguardar(prompt_id: str, timeout: int = 300, intervalo: int = 2) -> dict:
    """Poll /history até concluir. Único bloqueio permitido."""
    fim = time.time() + timeout
    while time.time() < fim:
        hist = _get_history(prompt_id)
        bloco = hist.get(prompt_id)
        if bloco and bloco.get("status", {}).get("completed", False):
            return hist
        time.sleep(intervalo)
    raise TimeoutError(f"ComfyUI não concluiu prompt_id={prompt_id} em {timeout}s")


def _extrair_outputs(hist: dict, prompt_id: str) -> list[dict]:
    bloco = hist.get(prompt_id, {})
    saidas: list[dict] = []
    for _node, res in (bloco.get("outputs") or {}).items():
        for img in res.get("images", []) + res.get("gifs", []):
            saidas.append(
                {
                    "filename": img.get("filename", ""),
                    "subfolder": img.get("subfolder", ""),
                    "type": img.get("type", "output"),
                }
            )
    return saidas


# ================================================================ TOOLS
@mcp.tool()
def search_references(query: str, limit: int = 3) -> dict:
    """Busca imagens (DuckDuckGo Images, fallback Bing), baixa p/ refs/web/."""
    t0 = time.time()
    args = {"query": query, "limit": limit}
    try:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as e:
            raise RuntimeError(
                "playwright ausente. Ação: "
                "fotografo/.venv/bin/python -m playwright install firefox "
                f"(erro bruto: {e})"
            ) from e

        slug = _slug(query)
        ts = int(time.time())
        REFS_WEB.mkdir(parents=True, exist_ok=True)
        urls: list[str] = []

        with sync_playwright() as pw:
            nav = pw.firefox.launch(headless=True)
            try:
                pag = nav.new_page()
                # tentativa 1: DuckDuckGo Images
                try:
                    pag.goto(
                        "https://duckduckgo.com/?q="
                        + query.replace(" ", "+")
                        + "&iax=images&ia=images",
                        timeout=30000,
                    )
                    pag.wait_for_timeout(3000)
                    imgs = pag.query_selector_all("img.tile--img__img")[: int(limit) * 3]
                    for el in imgs:
                        src = el.get_attribute("src") or el.get_attribute("data-src") or ""
                        if src.startswith("http"):
                            urls.append(src)
                        if len(urls) >= limit:
                            break
                except Exception:
                    urls = []
                # fallback: Bing Images
                if len(urls) < 1:
                    pag.goto(
                        "https://www.bing.com/images/search?q=" + query.replace(" ", "+"),
                        timeout=30000,
                    )
                    pag.wait_for_timeout(3000)
                    imgs = pag.query_selector_all("img.mimg")[: int(limit) * 3]
                    for el in imgs:
                        src = el.get_attribute("src") or ""
                        if src.startswith("http") and "data:image" not in src:
                            urls.append(src)
                        if len(urls) >= limit:
                            break
            finally:
                nav.close()

        if not urls:
            raise RuntimeError("Nenhuma imagem encontrada (DDG + Bing falharam ou vazio)")

        salvos: list[str] = []
        with httpx.Client(timeout=30.0, follow_redirects=True) as cli:
            for i, u in enumerate(urls[: int(limit)]):
                try:
                    r = cli.get(u)
                    r.raise_for_status()
                    if len(r.content) < 10 * 1024:
                        continue  # filtra <10KB
                    dest = (REFS_WEB / f"ref_{slug}_{ts}_{i}.jpg").resolve()
                    dest.write_bytes(r.content)
                    salvos.append(str(dest))
                except Exception:
                    continue

        if not salvos:
            raise RuntimeError("Downloads falharam ou todas <10KB — nada salvo")

        # índice append
        idx = REFS_WEB / "index.json"
        reg = []
        if idx.exists():
            try:
                reg = json.loads(idx.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                reg = []
        for i, p in enumerate(salvos):
            reg.append({"url_fonte": urls[i], "query": query, "ts": ts, "path": p})
        idx.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")

        _melt("search_references", args, int((time.time() - t0) * 1000), "ok", salvos[0])
        return {"paths": salvos}
    except Exception as e:
        _melt("search_references", args, int((time.time() - t0) * 1000), "error", str(e)[:200])
        raise


@mcp.tool()
def draft_generate(prompt: str, negative: str = "", seed: int = -1, steps: int = 12) -> dict:
    """Gera draft SDXL via workflows/draft_sdxl.json; salva refs/draft/."""
    t0 = time.time()
    args = {"prompt": prompt, "negative": negative, "seed": seed, "steps": steps}
    try:
        if seed is None or int(seed) == -1:
            seed_uso = random.randint(0, 2**31 - 1)
        else:
            seed_uso = int(seed)
        wf = _template(
            "draft_sdxl.json",
            {
                "PROMPT": prompt.replace('"', "'"),
                "NEGATIVE": (negative or "").replace('"', "'"),
                "SEED": str(seed_uso),
                "STEPS": str(int(steps)),
            },
        )
        pid = _post_prompt(wf)
        hist = _aguardar(pid, timeout=300, intervalo=2)
        outs = _extrair_outputs(hist, pid)
        if not outs:
            raise RuntimeError(f"ComfyUI concluiu {pid} mas sem outputs em history")
        ts = int(time.time())
        dest = (REFS_DRAFT / f"draft_{ts}.png").resolve()
        o = outs[0]
        _baixar_view(o["filename"], o["subfolder"], o["type"], dest)
        _melt("draft_generate", args, int((time.time() - t0) * 1000), "ok", str(dest))
        return {"prompt_id": pid, "path": str(dest)}
    except Exception as e:
        _melt("draft_generate", args, int((time.time() - t0) * 1000), "error", str(e)[:200])
        raise


@mcp.tool()
def analyze_reference(image_path: str, hint: str = "") -> dict:
    """Analisa imagem via LLM-Fotógrafo; retorna DoP {3 chaves exatas}."""
    t0 = time.time()
    args = {"image_path": image_path, "hint": hint}
    try:
        p = Path(image_path)
        if not p.exists():
            raise RuntimeError(f"Imagem inexistente: {image_path} (nunca inventar path)")
        b64 = base64.b64encode(p.read_bytes()).decode("ascii")
        gbnf = _ler_schema_gbnf()
        sistema = PERSONA_FOTODESIGNER + (f" Contexto do usuário: {hint}" if hint else "")

        def _chamar(instrucao_extra: str = "") -> str:
            corpo: dict = {
                "model": "fotografo",
                "temperature": 0.0,
                "max_tokens": 512,
                "messages": [
                    {"role": "system", "content": sistema + instrucao_extra},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Analisa esta imagem. APENAS JSON válido."},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{b64}"},
                            },
                        ],
                    },
                ],
            }
            # response_format JSON; grammar GBNF se suportado (llama.cpp)
            if gbnf:
                corpo["response_format"] = {"type": "json_object"}
            else:
                corpo["response_format"] = {"type": "json_object"}
            url = f"{FOTOGRAFO_LLM}/chat/completions"
            try:
                r = httpx.post(url, json=corpo, timeout=120.0)
                r.raise_for_status()
            except Exception as e:
                raise RuntimeError(f"LLM-Fotógrafo offline ou falhou ({url}): {e}") from e
            try:
                dado = r.json()
            except Exception as e:
                raise RuntimeError(f"LLM retornou corpo não-JSON: {e} :: bruto={r.text[:500]}") from e
            try:
                return dado["choices"][0]["message"]["content"]
            except (KeyError, IndexError) as e:
                raise RuntimeError(f"LLM resposta sem choices/message: {e} :: bruto={dado}") from e

        def _parse(bruto: str) -> dict:
            try:
                obj = json.loads(bruto)
            except json.JSONDecodeError as e:
                raise RuntimeError(f"Parse DoP falhou: {e} :: bruto={bruto[:800]}") from e
            if not isinstance(obj, dict) or tuple(sorted(obj.keys())) != tuple(sorted(DOP_KEYS)):
                raise RuntimeError(
                    f"DoP chaves inválidas (esperado {list(DOP_KEYS)}): {obj} :: bruto={bruto[:800]}"
                )
            for k in DOP_KEYS:
                if not isinstance(obj[k], str):
                    raise RuntimeError(f"DoP chave {k} não-string: {obj}")
            return {k: obj[k] for k in DOP_KEYS}

        try:
            bruto1 = _chamar()
            dop = _parse(bruto1)
        except RuntimeError:
            bruto2 = _chamar(" APENAS JSON válido, sem markdown, sem explicação.")
            dop = _parse(bruto2)  # falha 2 => propaga com bruto

        _melt("analyze_reference", args, int((time.time() - t0) * 1000), "ok", image_path)
        return dop
    except Exception as e:
        _melt("analyze_reference", args, int((time.time() - t0) * 1000), "error", str(e)[:200])
        raise


@mcp.tool()
def display_locally(path: str) -> dict:
    """Abre arquivo local (xdg-open) de forma NÃO-bloqueante."""
    t0 = time.time()
    args = {"path": path}
    try:
        p = Path(path)
        if not p.exists():
            _melt("display_locally", args, int((time.time() - t0) * 1000), "error", "inexistente")
            return {"aberto": False, "path": str(path)}
        try:
            subprocess.Popen(
                [DISPLAY_CMD, str(p.resolve())],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            ok = True
        except Exception:
            ok = False
        _melt(
            "display_locally",
            args,
            int((time.time() - t0) * 1000),
            "ok" if ok else "error",
            str(p.resolve()),
        )
        return {"aberto": ok, "path": str(p.resolve())}
    except Exception as e:
        _melt("display_locally", args, int((time.time() - t0) * 1000), "error", str(e)[:200])
        raise


@mcp.tool()
def render_final(
    prompt: str,
    reference_image: str,
    mode: str = "img2img",
    strength: float = 0.6,
    motion_bucket_id: int = 60,
    frames: int = 25,
    seed: int = -1,
) -> dict:
    """Render final img2img (SDXL+ControlNet) ou img2vid (SVD)."""
    t0 = time.time()
    args = {
        "prompt": prompt,
        "reference_image": reference_image,
        "mode": mode,
        "strength": strength,
        "motion_bucket_id": motion_bucket_id,
        "frames": frames,
        "seed": seed,
    }
    try:
        pref = Path(reference_image)
        if not pref.exists():
            raise RuntimeError(f"reference_image inexistente: {reference_image}")
        if mode not in ("img2img", "img2vid"):
            raise RuntimeError(f"mode inválido: {mode} (use img2img|img2vid)")
        seed_uso = random.randint(0, 2**31 - 1) if seed is None or int(seed) == -1 else int(seed)

        if mode == "img2img":
            wf = _template(
                "img2img_cn.json",
                {
                    "PROMPT": prompt.replace('"', "'"),
                    "NEGATIVE": "borrado, baixa qualidade".replace('"', "'"),
                    "REFERENCE_IMAGE": str(pref.resolve()),
                    "STRENGTH": str(float(strength)),
                    "SEED": str(seed_uso),
                },
            )
        else:
            wf = _template(
                "svd_xt.json",
                {
                    "REFERENCE_IMAGE": str(pref.resolve()),
                    "MOTION_BUCKET_ID": str(int(motion_bucket_id)),
                    "FRAMES": str(int(frames)),
                    "SEED": str(seed_uso),
                },
            )
        pid = _post_prompt(wf)
        hist = _aguardar(pid, timeout=300, intervalo=2)
        outs = _extrair_outputs(hist, pid)
        if not outs:
            raise RuntimeError(f"ComfyUI concluiu {pid} mas sem outputs")
        ts = int(time.time())
        caminhos: list[str] = []
        for i, o in enumerate(outs):
            if mode == "img2img":
                dest = (REFS_DIR / f"final_{ts}_{i}.png").resolve()
            else:
                ext = ".webp" if o["filename"].endswith(".webp") else ".mp4"
                dest = (REFS_VIDEO / f"final_{ts}_{i}{ext}").resolve()
            _baixar_view(o["filename"], o["subfolder"], o["type"], dest)
            caminhos.append(str(dest))
        _melt("render_final", args, int((time.time() - t0) * 1000), "ok", caminhos[0])
        return {"prompt_id": pid, "outputs": caminhos}
    except Exception as e:
        _melt("render_final", args, int((time.time() - t0) * 1000), "error", str(e)[:200])
        raise


@mcp.tool()
def status_job(prompt_id: str) -> dict:
    """Normaliza /history/{prompt_id} em {state, message, outputs}."""
    t0 = time.time()
    args = {"prompt_id": prompt_id}
    try:
        hist = _get_history(prompt_id)
        bloco = hist.get(prompt_id)
        if bloco is None:
            estado = {"state": "queued", "message": "prompt_id na fila ou desconhecido", "outputs": []}
        else:
            status = bloco.get("status", {})
            outs = _extrair_outputs(hist, prompt_id)
            if status.get("completed", False):
                estado = {"state": "done", "message": "concluído", "outputs": outs}
            elif status.get("status_str") == "error" or "error" in status:
                estado = {
                    "state": "error",
                    "message": str(status.get("messages") or status.get("error") or "erro"),
                    "outputs": outs,
                }
            elif outs:
                estado = {"state": "running", "message": "parcialmente pronto", "outputs": outs}
            else:
                estado = {"state": "running", "message": "em execução", "outputs": []}
        _melt("status_job", args, int((time.time() - t0) * 1000), "ok", prompt_id)
        return estado
    except Exception as e:
        _melt("status_job", args, int((time.time() - t0) * 1000), "error", str(e)[:200])
        raise


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
