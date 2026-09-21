#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inject-regras.py — Hook session.start (R101): injeta o índice vivo de regras (R1-R101).

Reduz o system prompt do orquestrador: em vez de carregar ~150KB da constituição,
o GM recebe o núcleo irredutível (via instructions) + o índice vivo (via este hook)
e busca a regra completa sob demanda via `regras.py get <R-id>`.

Protocolo hook OpenCode (session.start):
    stdin:  JSON {"session_id": ..., "directory": ..., "prompt": ...}
    stdout: JSON {"context": {"__REGRA_INDEX__": {...}}} — injeção de contexto.
    Fail-open: qualquer exceção -> log + "{}" (nunca bloqueia session.start).
"""
import json
import logging
import sys
from pathlib import Path

INDEX = Path("/mnt/dados/Assistente Pessoal/cerebro com IA/regras/index.md")
NUCLEO = Path("/mnt/dados/Assistente Pessoal/cerebro com IA/regras/nucleo-irredutivel.md")
LOG_PATH = Path("/tmp/opencode/inject-regras.log")


def setup_logger():
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    l = logging.getLogger("InjectRegras")
    l.setLevel(logging.INFO)
    if not l.handlers:
        h = logging.FileHandler(LOG_PATH)
        h.setFormatter(logging.Formatter('%(asctime)s [INJECT-REGRAS] %(message)s'))
        l.addHandler(h)
    return l


logger = setup_logger()


def run() -> dict:
    if not INDEX.exists():
        logger.warning("index.md ausente: %s", INDEX)
        return {"index_loaded": False, "path": str(INDEX)}
    text = INDEX.read_text(encoding="utf-8")
    return {
        "index_loaded": True,
        "path": str(INDEX),
        "nucleo": str(NUCLEO),
        "tokens_approx": len(text) // 4,
        "mapa_vivo": text,
    }


def main():
    try:
        if not sys.stdin.isatty():
            sys.stdin.read()
    except Exception:
        pass
    try:
        result = run()
        emission = {"context": {"__REGRA_INDEX__": result}}
    except Exception as e:
        logger.error("erro=%s", e)
        print("{}")
        return 0
    print(json.dumps(emission, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())