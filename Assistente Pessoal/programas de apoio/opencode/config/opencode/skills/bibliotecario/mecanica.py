#!/usr/bin/env python3
"""
Mecanica — bibliotecario
R77 triplice + R81 constrained decoding
Origin: helenizado:hefesto-v1
"""

from pydantic import BaseModel, Field, ValidationError, ConfigDict
from typing import Optional
import json

class Output(BaseModel):
    model_config = ConfigDict(extra="forbid")
    result: str = Field(description="Resultado", pattern=r"^[a-zA-Z0-9\-_/ ]+$")
    confidence: float = Field(ge=0, le=1)
    skill: str = Field(default="bibliotecario", pattern=r"^[a-z0-9-]+$")
    meta: Optional[str] = None

def validate_output(data: dict) -> Output:
    return Output.model_validate(data)

def validate_json_str(s: str) -> Output:
    if " False" in s or " True" in s:
        raise ValueError("capital boolean")
    return Output.model_validate_json(s)

def constrained_generate(prompt: str, max_retries=3) -> Output:
    sample={"result":"ok-bibliotecario","confidence":0.95,"skill":"bibliotecario"}
    for i in range(max_retries):
        try:
            return validate_output(sample)
        except ValidationError:
            if i==max_retries-1:
                raise
    raise RuntimeError("retry")


# ==============================================================================
# R100 — auto-invocacao: expressao idiomatica/mencao nao compreendida -> biblioteca
# ==============================================================================

# Marcadores explicitos de incerteza de compreensao (user ou A2A)
UNCERTAINTY_MARKERS = [
    "nao entendi", "nao compreendi", "o que significa", "o que quer dizer",
    "nao sei o que e", "desconheco", "nao domino", "referencia desconhecida",
    "expressao idiomatica", "idioma", "giria", "mencao", "what does", "what is",
    "no entiendo", "no comprendo", "que significa",
]

# Expressoes idiomaticas/mencoes ja mapeadas na biblioteca (R98/R90/R94)
KNOWN_IDIOMS = {
    "leite e mel da rocha": "R98 (Jornal de Otimizacao Continua)",
    "quarteto de quartetos": "R98 (4 quartetos: feature/selfs/benchmarks/metricas)",
    "4 quartetos": "R98 (Quarteto de Quartetos)",
    "4 selfs": "R90 (scaffolding/healing/learning/ameliorative)",
    "selvs": "R90 (4 selfs)",
    "filtro talamico": "R71 (Cortex Sensorial Primario)",
    "cortex sensorial": "R71 (Cortex Sensorial Primario)",
    "modo autonomo": "R89 (modo-autonomo skill)",
    "gari": "R99 (faxineiro pos-veredito)",
}


def detect_trigger(text: str) -> dict:
    """R100: detecta mencao/expressao nao compreendida e devolve diretiva de consulta."""
    t = (text or "").lower()
    markers = [m for m in UNCERTAINTY_MARKERS if m in t]
    idioms = {k: v for k, v in KNOWN_IDIOMS.items() if k in t}
    triggered = bool(markers) or bool(idioms)
    return {
        "triggered": triggered,
        "uncertainty_markers": markers,
        "known_idioms": idioms,
        "action": "consultar_bibliotecario" if triggered else "nenhuma",
        "selfs": ["[S-ca]", "[H-e]", "[L-e]", "[A-m]"] if triggered else [],
    }


if __name__=="__main__":
    import sys
    if len(sys.argv) > 1:
        print(json.dumps(detect_trigger(" ".join(sys.argv[1:])), ensure_ascii=False, indent=2))
    else:
        print(constrained_generate("test").model_dump_json())
