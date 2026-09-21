#!/usr/bin/env python3
"""
Diário do secretário — log JSONL reversível de mutações + quarentena.

Uso:
    diario.py --tail N
    (append é feito via Python: from diario import logar, mover_para_quarentena)

Toda ação destrutiva (mover) passa por mover_para_quarentena(), que copia o
arquivo para <vault>/quarentena/secretario/<ts>-<nome> ANTES de mover, e loga
{ts, acao, alvo, resultado, reversao:{tipo, path_backup}}.
"""

import argparse
import datetime
import json
import os
import shutil
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
DIARIO = os.path.join(BASE, "data", "diario.jsonl")
VAULT = "/mnt/dados/Assistente Pessoal/cerebro com IA"
QUARENTENA = os.path.join(VAULT, "quarentena", "secretario")


def _agora():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def logar(acao, alvo, resultado, reversao=None):
    os.makedirs(os.path.dirname(DIARIO), exist_ok=True)
    entry = {"ts": _agora(), "acao": acao, "alvo": alvo,
             "resultado": resultado, "reversao": reversao or {}}
    with open(DIARIO, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def mover_para_quarentena(path, motivo):
    """Move path para quarentena com backup prévio. Retorna entry do diário."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"alvo inexistente: {path}")
    ts = _agora().replace(":", "-")
    nome = os.path.basename(path)
    os.makedirs(QUARENTENA, exist_ok=True)
    backup = os.path.join(QUARENTENA, f"{ts}-{nome}.bak")
    if os.path.isdir(path):
        shutil.copytree(path, backup)
        shutil.rmtree(path)
    else:
        shutil.copy2(path, backup)
        os.remove(path)
    dest = os.path.join(QUARENTENA, f"{ts}-{nome}")
    os.rename(backup, dest)
    return logar("mover_quarentena", path, f"ok ({motivo})",
                 {"tipo": "restaurar_via_copia", "path_backup": dest})


def ler_ultimos(n=10):
    if not os.path.exists(DIARIO):
        return []
    with open(DIARIO, encoding="utf-8") as f:
        linhas = [ln for ln in f if ln.strip()]
    return [json.loads(ln) for ln in linhas[-n:]]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Diário do secretário")
    ap.add_argument("--tail", type=int, default=10)
    args = ap.parse_args(argv)
    out = {"acao": "diario_tail", "total_lidos": args.tail,
           "entries": ler_ultimos(args.tail), "exit_status": "ok"}
    print(json.dumps(out, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
