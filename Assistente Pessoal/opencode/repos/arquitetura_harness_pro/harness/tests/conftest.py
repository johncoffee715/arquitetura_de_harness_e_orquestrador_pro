"""Garante que `harness/` está no sys.path p/ imports `models.*` nos testes."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
