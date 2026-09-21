#!/usr/bin/env python3
"""crivo_vlm.py — runner do crivo de candidatos VLM para o papel LLM-Fotógrafo.

Bateria:
  T1 (visão, 5 imgs): JSON DoP estrito via GBNF (chaves exatas do schema).
  T2 (texto, 10x):   JSON DoP sem imagem — conformidade de schema.
T3 (qualidade do prompt EN compilado) e T5 (HITL) ficam a cargo da avaliação
posterior usando os artefatos deste run; T4 (performance) sai das medições aqui.

Uso: crivo_vlm.py --name <id_candidato> [--url http://127.0.0.1:9188/v1]
Saída: benchmarks/result_<name>.json + resumo no stdout.
"""
import argparse
import base64
import datetime as dt
import json
import sys
import time
from pathlib import Path

import httpx

ROOT = Path("/mnt/dados/Assistente Pessoal/programas de apoio/fotografo")
SCHEMA_PATH = ROOT / "schemas" / "dop_schema.gbnf"
IMGS_DIR = ROOT / "benchmarks" / "imgs"
OUT_DIR = ROOT / "benchmarks"

KEYS = {"camera_angle", "lighting_and_style", "technical_subjects"}

SYSTEM = (
    "Você é um Diretor de Fotografia especializado em macrofotografia industrial e "
    "cibernética. Analise a imagem e responda APENAS com JSON válido contendo "
    "exatamente as chaves camera_angle, lighting_and_style, technical_subjects. "
    "Nenhuma palavra fora do JSON."
)

USER_VISAO = (
    "Extraia o enquadramento, a iluminação/estilo e os sujeitos técnicos desta imagem."
)

TEXTOS_T2 = [
    "macro de microsolda em chip BGA com fumaça de fluxo",
    "bancada de eletrônica vista de cima com multímetros",
    "retrato de robô biomêtrico de perfil com fundo preto",
    "circuito impresso com trilhas de cobre expostas",
    "placa de vídeo sobre mesa com pinças ESD",
    "soldagem ponto a ponto em conector HDMI",
    "estação de retrabalho de ar quente",
    "fonte de bancada ligada mostrando 12V",
    "mão robótica segurando ferro de solda",
    "close em capacitores SMD ao redor de um chipset",
]


def carregar_schema() -> str:
    txt = SCHEMA_PATH.read_text(encoding="utf-8")
    if not txt.strip().startswith("root"):
        raise SystemExit("GBNF inválido: não começa com 'root'")
    return txt


def chat(url: str, contents: list, grammar: str, timeout: int = 240) -> dict:
    payload = {
        "model": "local",
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": contents},
        ],
        "temperature": 0.2,
        "max_tokens": 300,
        "grammar": grammar,
    }
    with httpx.Client(timeout=timeout) as cli:
        r = cli.post(url.rstrip("/") + "/chat/completions", json=payload)
        r.raise_for_status()
        return r.json()


def validar(conteudo: str) -> dict:
    data = json.loads(conteudo)
    if not isinstance(data, dict):
        raise ValueError("não é objeto")
    if set(data.keys()) != KEYS:
        raise ValueError(f"chaves incorretas: {set(data.keys())}")
    if not all(isinstance(v, str) and v.strip() for v in data.values()):
        raise ValueError("valor não-string/vazio")
    return data


def imagem_b64(path: Path) -> str:
    return "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--url", default="http://127.0.0.1:9188/v1")
    ap.add_argument("--imgs", default=str(IMGS_DIR))
    args = ap.parse_args()

    grammar = carregar_schema()
    imgs = sorted(Path(args.imgs).glob("*.jpg"))
    if not imgs:
        raise SystemExit("sem imagens de teste")
    imgs = imgs[:5]

    res = {
        "name": args.name,
        "ts": dt.datetime.now().isoformat(timespec="seconds"),
        "t1": {"total": len(imgs), "ok": 0, "detalhes": []},
        "t2": {"total": len(TEXTOS_T2), "ok": 0},
        "raw_falhas": [],
        "_tok_s": [],
        "_latencias": [],
    }

    def registrar_metricas(resp: dict, wall: float) -> None:
        timings = resp.get("timings") or {}
        tok_s = timings.get("predicted_per_second")
        if not tok_s:
            usage = resp.get("usage") or {}
            comp = usage.get("completion_tokens")
            if comp and wall > 0:
                tok_s = comp / wall
            else:
                tok_s = None
        if tok_s:
            res["_tok_s"].append(round(float(tok_s), 2))
        res["_latencias"].append(round(wall, 2))

    # T1 — visão
    for img in imgs:
        t0 = time.monotonic()
        try:
            resp = chat(
                args.url,
                [
                    {"type": "text", "text": USER_VISAO},
                    {"type": "image_url", "image_url": {"url": imagem_b64(img)}},
                ],
                grammar,
            )
            wall = time.monotonic() - t0
            registrar_metricas(resp, wall)
            conteudo = resp["choices"][0]["message"]["content"]
            validar(conteudo)
            res["t1"]["ok"] += 1
            res["t1"]["detalhes"].append(
                {"img": img.name, "ok": True, "s": round(wall, 1)}
            )
        except Exception as e:  # noqa: BLE001 — registrar bruto e seguir
            wall = time.monotonic() - t0
            bruto = ""
            try:
                bruto = (resp["choices"][0]["message"]["content"])[:500]  # type: ignore
            except Exception:
                pass
            res["t1"]["detalhes"].append(
                {"img": img.name, "ok": False, "s": round(wall, 1), "erro": str(e)[:200]}
            )
            res["raw_falhas"].append(
                {"fase": "t1", "img": img.name, "erro": str(e)[:300], "bruto": bruto}
            )

    # T2 — texto puro
    for texto in TEXTOS_T2:
        t0 = time.monotonic()
        try:
            resp = chat(
                args.url,
                [{"type": "text", "text": f"Descreva (JSON DoP): {texto}"}],
                grammar,
                timeout=120,
            )
            wall = time.monotonic() - t0
            registrar_metricas(resp, wall)
            validar(resp["choices"][0]["message"]["content"])
            res["t2"]["ok"] += 1
        except Exception as e:  # noqa: BLE001
            res["raw_falhas"].append({"fase": "t2", "tema": texto, "erro": str(e)[:300]})

    tok_s = res.pop("_tok_s")
    lat = res.pop("_latencias")
    res["tok_s_media"] = round(sum(tok_s) / len(tok_s), 2) if tok_s else None
    res["lat_media_s"] = round(sum(lat) / len(lat), 2) if lat else None

    out = OUT_DIR / f"result_{args.name}.json"
    out.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"== CRIVO {args.name} ==")
    print(f"T1 visão : {res['t1']['ok']}/{res['t1']['total']}")
    print(f"T2 texto : {res['t2']['ok']}/{res['t2']['total']}")
    print(f"tok/s médio: {res['tok_s_media']} | lat média: {res['lat_media_s']}s")
    print(f"raw_falhas: {len(res['raw_falhas'])}")
    print(f"artefato: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
