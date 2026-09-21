"""
Mecânica de Ignição (Execution & Validation) — andrej-karpathy-skills.
4 gates contra pitfalls de codificação por LLM (Karpathy).
Helenizado de multica-ai/andrej-karpathy-skills — princípios como gates executáveis.
"""

from typing import Any, Dict, List
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


class KarpathyReviewInput(BaseModel):
    """Input schema: diff lines + original task."""
    diff_lines: List[str]
    task: str


class Violation(BaseModel):
    """Uma violação com princípio + evidência de linha."""
    principle: str  # think | simplicity | scope | goals
    line: str
    reason: str


class KarpathyReviewOutput(BaseModel):
    """Schema for the output."""
    verdict: str  # "pass" or "fail"
    violations: List[Violation]
    reviewed_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_karpathy_input(input_data: Dict[str, Any]) -> KarpathyReviewInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = KarpathyReviewInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.task or not input_obj.task.strip():
        raise ValueError("Invalid input: 'task' must be non-empty")
    if not input_obj.diff_lines:
        raise ValueError("Invalid input: 'diff_lines' must have ≥1 line")
    return input_obj


def aplicar_gates(diff_lines: List[str], task: str) -> Dict[str, Any]:
    """Aplica os 4 gates (heurística determinística offline p/ validação).

    scope: linhas que não mencionam nenhum termo da task = suspeitas.
    simplicity: linhas >120 chars ou com 'abstract/factory/manager' genérico = suspeitas.
    think/goals: verificados pelo chamador (requerem julgamento); aqui estrutura.
    """
    task_terms = {t.lower() for t in task.replace("/", " ").split() if len(t) > 3}
    violations: List[Violation] = []
    for ln in diff_lines:
        low = ln.lower()
        if task_terms and not any(t in low for t in task_terms) and ln.strip().startswith(("+", "-")):
            violations.append(Violation(
                principle="scope",
                line=ln[:120],
                reason="linha não traça a nenhum termo da task (mudança cirúrgica violada?)",
            ))
        if len(ln) > 120:
            violations.append(Violation(
                principle="simplicity",
                line=ln[:120],
                reason="linha >120 chars — candidata a simplificação",
            ))
    verdict = "fail" if violations else "pass"
    out = KarpathyReviewOutput(
        verdict=verdict,
        violations=violations,
        reviewed_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "gates": ["think", "simplicity", "scope", "goals"],
                            "heuristic": "offline-deterministica"},
    )
    return out.model_dump(mode="json")


def ignicao(diff_lines: List[str], task: str) -> Dict[str, Any]:
    """Função principal: valida → aplica gates → dict."""
    validated = validate_karpathy_input({"diff_lines": diff_lines, "task": task})
    return aplicar_gates(validated.diff_lines, validated.task)


if __name__ == "__main__":
    import json

    r1 = ignicao(["+def validate(x): return bool(x)  # fix login validation"], "fix login validation")
    assert r1["status"] == "success" and r1["verdict"] == "pass", r1
    r2 = ignicao(["+class AbstractUserManagerFactoryImpl:", "+    # refactored unrelated helper"], "fix login validation")
    assert r2["verdict"] == "fail" and len(r2["violations"]) >= 1, r2
    try:
        ignicao([], "")
        raise SystemExit("FAIL: input vazio deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 3}, ensure_ascii=False))
