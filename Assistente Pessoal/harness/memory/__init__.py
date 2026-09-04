"""Collective Memory + Agentic RAG module for the Gran-Mestre harness.

The module persists a collective memory database (``context_memory.db``)
and provides retrieval for agentic RAG across pipeline phases.
"""

from harness.memory.context_memory import CollectiveMemory

__all__ = ["CollectiveMemory"]
