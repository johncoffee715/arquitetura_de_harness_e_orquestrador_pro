"""A2A (Agent2Agent) protocol for the Gran-Mestre harness.

Implements the 2026 A2A standard (see "Orquestrador de IA de Forma
Profissional" §2.1): ``AgentCard`` discovery, ``Task`` state, and
OAuth-scoped skill authorization — over an in-memory transport with no
network dependency.
"""

from harness.a2a.protocol import A2AClient, AgentCard, Task
from harness.a2a.registry import A2ARegistry, AgentRegistry

__all__ = [
    "A2AClient",
    "A2ARegistry",
    "AgentCard",
    "AgentRegistry",
    "Task",
]

__version__ = "1.0.0"
