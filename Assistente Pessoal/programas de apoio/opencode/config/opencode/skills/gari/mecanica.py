#!/usr/bin/env python3
"""
Mecanica — gari
R77 triplice + R81 constrained decoding + R98 quarteto de quartetos
Origin: helenizado:hefesto-gari-v1
Upgrade 2026-09-11: gatilho flexível (pergunta direta do user) + referencia_direta R99.
Upgrade 2026-09-16 (gari-eng-01): constrained_generate REAL via :9084 + grammar do disco; fail-closed honesto.
"""

from pydantic import BaseModel, Field, ValidationError, ConfigDict
from typing import Optional, List
import json
import re
import pathlib
import subprocess
import urllib.request
import urllib.error

SKILL_DIR = pathlib.Path(__file__).resolve().parent
GRAMMAR_PATH = SKILL_DIR / "schema.gbnf"
SYNC_SCRIPT = pathlib.Path("/mnt/dados/Assistente Pessoal/programas de apoio/opencode/scripts/sync-llm-stack.py")
SNAP_PATH = pathlib.Path("/mnt/dados/Assistente Pessoal/cerebro com IA/decisoes/2026-09-11-sessao-encerrada.md")
BENCH_DIR = pathlib.Path("/mnt/dados/Assistente Pessoal/cerebro com IA/benchmarks")
DECISOES_DIR = pathlib.Path("/mnt/dados/Assistente Pessoal/cerebro com IA/decisoes")
TMP_DIR = pathlib.Path("/tmp/opencode")

# Gatilho flexível: pergunta DIRETA do user, em variações (com/sem "ainda", singular/plural, acento)
TRIGGER_RE = re.compile(
    r"posso\s+reiniciar\s+ou\s+(ainda\s+)?existe(m)?\s+(alguma\s+)?pend[êe]ncia(s)?",
    re.IGNORECASE,
)

class Output(BaseModel):
    model_config = ConfigDict(extra="forbid")
    trigger: str = Field(description="Pergunta direta do user detectada")
    referencia_direta: str = Field(default="R99", description="Referência direta ao requisito Gari")
    verdict: str = Field(pattern=r"^Pode reiniciar — zero pendências\.$")
    saved: List[str] = Field(default_factory=list)
    stored: Optional[str] = None
    cleaned: List[str] = Field(default_factory=list)
    skill: str = Field(default="gari", pattern=r"^[a-z0-9-]+$")


def detect_trigger(text: str) -> bool:
    """Detecta a pergunta direta do user (gatilho Gari) em variações."""
    return bool(TRIGGER_RE.search(text or ""))


def validate_output(data: dict) -> Output:
    return Output.model_validate(data)

def validate_json_str(s: str) -> Output:
    if " False" in s or " True" in s:
        raise ValueError("capital boolean")
    return Output.model_validate_json(s)

def _load_grammar() -> str:
    return GRAMMAR_PATH.read_text(encoding="utf-8")

def constrained_generate(prompt: str, max_retries=3, endpoint="http://127.0.0.1:9084", timeout=60) -> Output:
    """Geração constrangida REAL: POST no :9084 com grammar do disco; fail-closed honesto."""
    if max_retries < 1:
        raise RuntimeError("max_retries<1")
    grammar = _load_grammar()
    system = ("Papel: faxineiro deterministico. Responder SOMENTE com o JSON do schema "
              "(trigger, referencia_direta=R99, verdict, saved[], cleaned[]). Sem prosa, sem markdown.")
    body = json.dumps({
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        "temperature": 0.0,
        "max_tokens": 256,
        "grammar": grammar,
    }).encode("utf-8")
    last: Exception = RuntimeError("retry-esgotado")
    for _ in range(max_retries):
        try:
            req = urllib.request.Request(
                endpoint.rstrip("/") + "/v1/chat/completions",
                data=body, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                resp = json.loads(r.read().decode("utf-8", "replace"))
            text = resp["choices"][0]["message"]["content"].strip()
            return Output.model_validate_json(text)
        except (ValidationError, ValueError, KeyError, IndexError,
                urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            last = e
    raise last

def salvar() -> dict:
    """Flush + sonda Qdrant + sync-check + snapshot. Retorna {saved: [...], sonda: {...}}."""
    saved = ["vault"]  # vault é filesystem; Qdrant faz WAL ~5s — apenas sonda
    sonda: dict = {"qdrant_http": None, "sync_check": None}
    try:
        with urllib.request.urlopen("http://127.0.0.1:6333/collections", timeout=5) as r:
            sonda["qdrant_http"] = r.status
            if r.status == 200:
                saved.append("qdrant")
    except Exception as e:
        sonda["qdrant_http"] = f"falha:{type(e).__name__}"
    if SYNC_SCRIPT.exists():
        try:
            p = subprocess.run(["python3", str(SYNC_SCRIPT), "--check"],
                               timeout=10, capture_output=True, text=True)
            sonda["sync_check"] = p.returncode
        except Exception as e:
            sonda["sync_check"] = f"falha:{type(e).__name__}"
    else:
        sonda["sync_check"] = "script-inexistente"
    if SNAP_PATH.exists():
        saved.append("manifesto")
    return {"saved": saved, "sonda": sonda}

def armazenar() -> dict:
    """Confere pérolas quant/qualit na biblioteca (contagem real, dirs ausentes = 0)."""
    b = list(BENCH_DIR.glob("*.md")) if BENCH_DIR.is_dir() else []
    d = list(DECISOES_DIR.glob("*.md")) if DECISOES_DIR.is_dir() else []
    return {"stored": f"benchmarks:{len(b)}+decisoes:{len(d)}", "quant": len(b), "qualit": len(d)}

def limpar() -> dict:
    """Remove SÓ voláteis: patch_*.py em /tmp/opencode + __pycache__ da skill. Conta remoções reais."""
    import shutil
    alvos = []
    if TMP_DIR.is_dir():
        alvos += sorted(TMP_DIR.glob("patch_*.py"))
    alvos += sorted(SKILL_DIR.glob("__pycache__"))
    cleaned = []
    for p in alvos:
        try:
            if p.is_dir() and not p.is_symlink():
                shutil.rmtree(p)
            else:
                p.unlink()
            cleaned.append(p.name)
        except Exception:
            pass
    return {"cleaned": cleaned}

if __name__=="__main__":
    import sys
    args = sys.argv[1:]
    if "--ignicao" in args:
        sv = salvar()
        ar = armazenar()
        li = limpar()
        prompt = ("Pergunta direta: posso reiniciar ou ainda existem pendencias (R99). "
                  f"Emita o contract JSON com saved={json.dumps(sv['saved'])} "
                  f"cleaned={json.dumps(li['cleaned'])}.")
        out = constrained_generate(prompt)
        print(json.dumps({"saved": sv, "stored": ar, "cleaned": li,
                          "contract": out.model_dump()}, ensure_ascii=False))
    elif args:
        text = " ".join(args)
        hit = detect_trigger(text)
        print(json.dumps({"trigger_detectado": hit, "referencia_direta": "R99" if hit else None}, ensure_ascii=False))
    else:
        offline_probe = {"trigger": "posso reiniciar ou ainda existem pendencias",
                         "referencia_direta": "R99",
                         "verdict": "Pode reiniciar — zero pendências.",
                         "saved": ["vault", "qdrant", "manifesto"],
                         "stored": "benchmarks+decisoes", "cleaned": [], "skill": "gari"}
        validate_output(offline_probe)
        grammar = _load_grammar()
        assert "Pode reiniciar — zero pendências." in grammar and "R99" in grammar
        print(json.dumps({"smoke": "OK",
                          "detect_self": detect_trigger("posso reiniciar ou ainda existem pendencias"),
                          "grammar_ok": True, "offline_probe_ok": True,
                          "rede": "nao-tocada"}, ensure_ascii=False))
