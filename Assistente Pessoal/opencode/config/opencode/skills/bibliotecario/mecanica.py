#!/usr/bin/env python3
"""
Mecanica — bibliotecario
R77 triplice + R81 constrained decoding
Origin: helenizado:hefesto-v1
"""

from pydantic import BaseModel, Field, ValidationError
from typing import Optional
import json

class Output(BaseModel):
    result: str = Field(description="Resultado", pattern=r"^[a-zA-Z0-9\-_/ ]+$")
    confidence: float = Field(ge=0, le=1)
    skill: str = Field(default="bibliotecario", pattern=r"^[a-z0-9-]+$")
    meta: Optional[str] = None
    class Config:
        extra = "forbid"

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

if __name__=="__main__":
    print(constrained_generate("test").model_dump_json())
