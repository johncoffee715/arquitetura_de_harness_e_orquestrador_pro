"""Grafo cognitivo condicional 0-6 com gates e circuit-breaker (T4.5).

Rotas (SPEC F2 §2.1): FAST 0→4→6 · STANDARD 0→…→6 · FULL com nós de
brainstorm/audit/refutação. Gates exigidos ANTES de entrar no nó-alvo;
3 falhas no mesmo nó abrem o circuito (R18).
"""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Tuple

ROUTES: Dict[str, List[str]] = {
    "FAST": ["F0", "F4", "F6"],
    "STANDARD": ["F0", "F1", "F2", "F3", "F4", "F5", "F6"],
    "FULL": ["F0", "F1", "F1B_BRAINSTORM", "F2", "F2_AUDIT", "F3_REFUTATION",
             "F4", "F4_MICRO_REVIEW", "F5_MACRO_REFUTATION", "F6_INDEPENDENT"],
}

_BASE_GATES: Dict[str, List[str]] = {"F2": ["G1"], "F3": ["G2"], "F4": ["G3"], "F6": ["G4"]}
_ROUTE_GATES: Dict[str, Dict[str, List[str]]] = {
    "FAST": {"F4": ["G3"], "F6": ["G4"]},
    "STANDARD": _BASE_GATES,
    "FULL": _BASE_GATES,
}

CIRCUIT_OPEN = "CIRCUIT_OPEN"


def classify_route(complexity: str, risk: str, ambiguity: str) -> str:
    """any(high)→FULL · all(low)→FAST · caso contrário STANDARD."""
    dims = (complexity, risk, ambiguity)
    if any(d == "high" for d in dims):
        return "FULL"
    if all(d == "low" for d in dims):
        return "FAST"
    return "STANDARD"


def gates_for(route_name: str, node: str) -> List[str]:
    return list(_ROUTE_GATES.get(route_name, {}).get(node, []))


class GraphEngine:
    """Máquina de estados sequencial com gates por nó e breaker por nó."""

    def __init__(self, route_name: str, max_retries_per_node: int = 3):
        if route_name not in ROUTES:
            raise ValueError(f"rota desconhecida: {route_name}")
        self.route_name = route_name
        self.nodes: List[str] = list(ROUTES[route_name])
        self.pos = 0
        self.approved: Dict[str, str] = {}
        self._fails: Dict[str, int] = defaultdict(int)
        self.max_retries = max_retries_per_node
        self.open = False

    def try_next(self) -> Tuple[str, List[str]]:
        """Retorna (nó_atual, gates_pendentes). Nó vazio ⇒ aguardando gate."""
        if self.open:
            return CIRCUIT_OPEN, []
        node = self.nodes[self.pos]
        missing = [g for g in gates_for(self.route_name, node) if g not in self.approved]
        return node, missing

    def pending_gates(self) -> List[str]:
        _, missing = self.try_next()
        return missing

    def approve_gate(self, gate: str, verdict: str = "PASSOU_CATEGORICO") -> None:
        if verdict != "PASSOU_CATEGORICO":
            raise ValueError(f"gate {gate} sem trânsito categórico: {verdict}")
        self.approved[gate] = verdict

    def complete_node(self) -> bool:
        """Avança se o nó atual está liberado; retorna True ao concluir o grafo."""
        node, missing = self.try_next()
        if self.open or missing or node == CIRCUIT_OPEN:
            return False
        self.pos += 1
        return True

    def report_failure(self, node: str) -> bool:
        """Registra falha; True quando o circuito ABRIU (R18: máx 3 tentativas)."""
        self._fails[node] += 1
        if self._fails[node] >= self.max_retries:
            self.open = True
        return self.open

    @property
    def completed(self) -> bool:
        return self.pos >= len(self.nodes)

    def snapshot(self) -> Dict:
        return {"route": self.route_name, "pos": self.pos, "node": self.nodes[min(self.pos, len(self.nodes) - 1)],
                "approved": dict(self.approved), "open": self.open, "completed": self.completed}
