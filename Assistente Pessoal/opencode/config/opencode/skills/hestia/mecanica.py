from pydantic import BaseModel, Field
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass
import tempfile
import filelock

@dataclass
class HestiaOntology:
    """Ontologia do Hestia - conceito de persona e sistema do skill."""
    persona: str
    system_prompt: str

@dataclass
class HestiaFirewall:
    """Firewall (gabarito) - regras de segurança e categorias."""
    rules: Dict[str, Any]
    allowed_categories: List[str]
    allowed_models: List[str]
    deny: List[str]

@dataclass
class HestiaMecanica:
    """Mecânica - etapas de execução e refutação."""
    ignition: str
    selection_criteria: str
    refutation_strategy: str

class HestiaSkill(HestiaOntology, HestiaFirewall, HestiaMecanica):
    """Hestia skill dispatcher with helenization R77/R75."""
    # SKILL.md já contém as seções, esta classe é para o mecanica.py
    pass

# Schema para validação (usado em mecanica.py)
# A forma mais simples: usar Pydantic no mecanica.py

def load_skill_schema() -> Dict[str, Any]:
    """Return schema from SKILL.md or ontologia.md."""
    return {
        "ontology": {
            "persona": "Orquestrador principal (Gran-Mestre) - supervisão de tarefas, decisão de rota, validação de veredito.",
            "system_prompt": "You are the Hestia skill dispatcher. You apply helenization R77/R75. Use global bindings by category (R75) and catalog-first (R8)."
        },
        "firewall": {
            "rules": [
                "Only execute within runtime constraints",
                "Never modify paths outside allowed directories",
                "Use global bindings by category"
            ],
            "allowed_categories": ["forge", "judge", "proposer", "ingestor", "reflexo"],
            "allowed_models": [
                "local-forge/forge",
                "local-judge/judge",
                "local-proposer/proposer",
                "local-ingestor/ingestor",
                "local-reflexo/reflexo"
            ],
            "deny": [
                "any external model beyond the stack",
                "Any model outside the stack"
            ]
        },
        "mechanica": {
            "ignition": "Ignite the hestia skill based on the dispatched task and runtime context.",
            "selection_criteria": "Select appropriate helenized skill based on task requirements and category.",
            "refutation_strategy": "Refute against invalid patterns using firewall rules and task constraints."
        }
    }
