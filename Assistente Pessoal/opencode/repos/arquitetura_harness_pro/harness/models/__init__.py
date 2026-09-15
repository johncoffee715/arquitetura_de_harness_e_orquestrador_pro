"""Pacote de gerenciamento de modelos do harness (discovery/profiler/router)."""
from .discovery import scan_models_dir, write_registry, MODELS_DIR
from .metadata import read_gguf_metadata

__all__ = ["scan_models_dir", "write_registry", "MODELS_DIR", "read_gguf_metadata"]
