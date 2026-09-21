#!/usr/bin/env python3
"""
Mecanica — security-methodology
R77 tríplice + R81 constrained decoding + R82 estrangulamento
Skill: security-methodology — metodologia segurança
Origin: https://github.com/security-methodology
Model: local-thalamus/ingestor (R75 DIP)
"""

from pydantic import BaseModel, Field, ValidationError
from typing import Optional, List
import json

class Output(BaseModel):
    """Output estrito de security-methodology — validado via Pydantic + GBNF"""
    result: str = Field(description="Resultado principal", pattern=r"^[a-zA-Z0-9\-_/ ]+$")
    confidence: float = Field(ge=0.0, le=1.0, description="Confiança 0-1")
    skill: str = Field(default="security-methodology", pattern=r"^[a-z0-9-]+$")
    meta: Optional[str] = Field(default=None, description="Metadados opcionais")

    class Config:
        extra = "forbid"

def validate_output(data: dict) -> Output:
    """Validação determinística — 100% schema conforme (R81)"""
    return Output.model_validate(data)

def validate_json_str(json_str: str) -> Output:
    """Validação de string JSON com anti-lixo gate"""
    # gate: rejeita False/True capital (Python vs JSON)
    if " False" in json_str or " True" in json_str:
        raise ValueError("JSON contém True/False capital — use true/false")
    if " | " in json_str and "PASS" in json_str:
        raise ValueError("JSON contém 'PASS | FAIL' não JSON — use enum")
    return Output.model_validate_json(json_str)

def constrained_generate(prompt: str, max_retries: int = 3) -> Output:
    """Stub GBNF travado — em produção, chama llama_cpp com LlamaGrammar.from_json_schema"""
    # Exemplo determinístico para teste
    sample = {"result": "ok-security-methodology", "confidence": 0.95, "skill": "security-methodology"}
    for attempt in range(max_retries):
        try:
            return validate_output(sample)
        except ValidationError as e:
            if attempt == max_retries - 1:
                raise
            # re-inject error e retry (nunca loop infinito)
            sample["result"] = f"retry-{attempt}"
    raise RuntimeError("max_retries excedido — fallback")

if __name__ == "__main__":
    # sanity
    out = constrained_generate("test")
    print(out.model_dump_json())
    # test anti-lixo
    try:
        validate_json_str('{"result": "x", "confidence": 0.9, "skill": "security-methodology", "extra": "lixo"}')
    except Exception as e:
        print(f"gate ok: {e}")
