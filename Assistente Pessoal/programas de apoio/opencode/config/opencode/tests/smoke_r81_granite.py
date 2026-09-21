"""Smoke de integração R81 contra o granite-4.2-3b :9088 (prova real, R29)."""
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills/hefesto/tooling"))

from pydantic import BaseModel, Field
from hefesto_llama_bridge import PydanticToGbnf, ConstrainedGenerate, llama_cpp_completions

BASE = "http://127.0.0.1:9088"


class Comando(BaseModel):
    comando_bash: str = Field(description="comando puro")
    risco_execucao: int = Field(ge=0, le=5)


def test_completion_with_grammar():
    """llama.cpp nativo /completion aceita grammar — barreira física real."""
    gbnf = PydanticToGbnf(Comando).to_gbnf()
    payload = {
        "prompt": "Json com comando bash para listar diretórios e risco (0-5).",
        "grammar": gbnf,
        "temperature": 0.0,
        "max_tokens": 120,
        "stop": ["\n\n"],
    }
    req = urllib.request.Request(
        BASE + "/completion",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as r:
        body = json.loads(r.read().decode("utf-8"))
    content = body.get("content", "")
    print("RAW COMPLETION:", repr(content[:200]))
    obj = Comando.model_validate_json(content)
    print("OK conforme:", obj.model_dump())


def test_chat_validation_only():
    """/v1 sem grammar: validação Pydantic + retry (pipeline anti-loop com o modelo real)."""
    fn = llama_cpp_completions(BASE + "/v1/chat/completions")
    cg = ConstrainedGenerate(fn, Comando, grammar="", temperature=0.0, max_tokens=120, max_retries=3)
    obj, meta = cg.run('Responda APENAS JSON: {"comando_bash": "...", "risco_execucao": N} — liste diretórios.')
    print("CHAT OK:", meta)
    print("conforme:", obj.model_dump())


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    if which in ("both", "grammar"):
        try:
            test_completion_with_grammar()
        except Exception as e:
            print("GRAMMAR FALHOU:", type(e).__name__, str(e)[:300])
    if which in ("both", "chat"):
        try:
            test_chat_validation_only()
        except Exception as e:
            print("CHAT FALHOU:", type(e).__name__, str(e)[:300])