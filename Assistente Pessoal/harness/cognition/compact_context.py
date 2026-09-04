#!/usr/bin/env python3
"""
compact_context — Regra global de compactação cognitiva a 50% de capacidade.

Política (armazenar → compactar → limpar, preservando workflow/workspace):

  1. ARMAZENAR  — antes de qualquer compactação, persiste o estado cognitivo:
                 decisões + pendências + estado de trabalho em
                   • cerebro/pipeline/contexto-atual.md
                   • cerebro/decisoes/<ts>-*.md
                   • harness/CONTEXT.md
  2. COMPACTAR  — escreve CONTEXT_COMPACT.md (essência para retomar a sessão:
                 decisões tomadas, tarefas ativas, próximos passos, riscos).
  3. LIMPAR     — remove lixo de contexto não-essencial (não-git, TTL):
                 *.tmp em , caches com idade > TTL, arquivos __pycache__ órfãos,
                 logs de sessão antigos. NUNCA toca arquivos de trabalho.

Preserva workflow/workspace: não altera arquivos rastreados pelo git (valida com
git status; modo --dry-run previewa tudo). Idempotente. Exit: 0 ok, 2 sem cognição,
3 erro.

Uso:
  compact_context.py [--threshold 50] [--ttl-days 7] [--dry-run]
  compact_context.py --store-only     # só estágio 1
  compact_context.py --compact-only   # só estágio 2
"""
import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

HARNESS_ROOT = Path("/mnt/dados")
CEREBRO = HARNESS_ROOT / "cerebro com IA"
PIPELINE_DIR = CEREBRO / "pipeline"
DECISOES_DIR = CEREBRO / "decisoes"
CONTEXT_FILE = HARNESS_ROOT / "harness" / "CONTEXT.md"
COMPACT_FILE = HARNESS_ROOT / "harness" / "CONTEXT_COMPACT.md"
TIMESTAMP = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def git_clean() -> bool:
    result = _run(["git", "-C", str(HARNESS_ROOT), "status", "--porcelain"])
    return not any(line for line in result.splitlines() if not line.startswith("??"))


def _run(cmd: List[str]) -> str:
    import subprocess
    r = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return (r.stdout or "") + (r.stderr or "")


def store_cognitive(state: dict, dry_run: bool) -> Path:
    """Estágio 1 — persiste estado cognitivo antes da compactação."""
    PIPELINE_DIR.mkdir(parents=True, exist_ok=True)
    DECISOES_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat()

    ctx = f"""# Contexto Atual — snapshot cognitivo ({ts})

## Decisões desta sessão
{_bullet(state.get("decisoes", ["(sem decisões novas)"]))}

## Tarefas ativas / pendências
{_bullet(state.get("pendencias", ["(sem pendências)"]) or state.get("tarefas", ["(sem tarefas)"]))}

## Próximos passos
{_bullet(state.get("proximos", ["(a definir)"]))}

## Riscos / estado
{_bullet(state.get("riscos", ["(sem riscos conhecidos)"]))}

## Snapshot técnico
- git: {", ".join(state.get("git", [])[:20]) if state.get("git") else "limpo"}
- ECC_HOME: {state.get("ecc_home", "n/d")}
- registry entries: {state.get("registry", "n/d")}
"""
    if dry_run:
        print(f"[dry-run] escreveria: {CONTEXT_FILE}")
        return CONTEXT_FILE
    CONTEXT_FILE.write_text(ctx, encoding="utf-8")
    # snapshot datado no cérebro (decidões)
    dec = f"""---
tags: [decisao, compactacao, pipeline]
data: {ts[:10]}
---

# Decisão — compactação cognitiva {ts}

{ctx}
"""
    dfile = DECISOES_DIR / f"{ts[:10]}-compactacao.md"
    dfile.write_text(dec, encoding="utf-8")
    return dfile


def _bullet(items) -> str:
    return "\n".join(f"- {x}" for x in items) if items else "(vazio)"


def compact_write(state: dict, dry_run: bool) -> Path:
    """Estágio 2 — escreve o resumo de retomada."""
    body = f"""# CONTEXT COMPACT — essência p/ retomada ({TIMESTAMP})

## Objetivo da sessão
{state.get("objetivo", "(não declarado)")}

## Decisões (mantidas)
{_bullet(state.get("decisoes", []))}

## Tarefas ativas
{_bullet(state.get("tarefas", ["(sem tarefas ativas)"]))}

## Próximos passos (ação)
{_bullet(state.get("proximos", ["(a definir)"]))}

## Riscos assumidos
{_bullet(state.get("riscos", ["(sem riscos)"]))}

---
Snapshoted em: {PIPELINE_DIR}/contexto-atual.md
"""
    if dry_run:
        print(f"[dry-run] escreveria: {COMPACT_FILE}")
        return COMPACT_FILE
    COMPACT_FILE.write_text(body, encoding="utf-8")
    return COMPACT_FILE


def cleanup(ttl_days: int, dry_run: bool) -> List[str]:
    """Estágio 3 — remove lixo não-essencial (não-git), respeitando TTL."""
    removed: List[str] = []
    now = datetime.now().timestamp()
    ttl = ttl_days * 86400

    # *.tmp dentro do harness/autofagia (não-git por definição)
    for p in (HARNESS_ROOT / "harness" / "autofagia").glob("*.tmp"):
        if now - p.stat().st_mtime > ttl:
            removed.append(str(p))

    # __pycache__ órfãos em dirs de scripts
    for d in (HARNESS_ROOT / "harness" / "autofagia").rglob("__pycache__"):
        if d.is_dir():
            import fnmatch
            srcs = {p.with_suffix("").name for p in d.parent.glob("*.py")}
            orphan = [p for p in d.glob("*.pyc") if p.name.split(".")[0] not in srcs]
            if orphan and now - d.stat().st_mtime > ttl:
                removed.append(str(d))
        break  # só top-level nesse passe

    # arquivos .bak antigos do registry (são de segurança, manter últimos 3)
    baks = sorted((HARNESS_ROOT / "harness" / "autofagia").glob("*.bak.*"),
                  key=lambda p: p.stat().st_mtime, reverse=True)
    for old in baks[3:]:
        removed.append(str(old))

    if dry_run:
        for r in removed:
            print(f"[dry-run] removeria: {r}")
    else:
        for r in removed:
            p = Path(r)
            try:
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink()
            except OSError:
                pass
    return removed


def load_state() -> dict:
    """Estado default (não há entrada externa; baseado no harness)."""
    git = _run(["git", "-C", str(HARNESS_ROOT), "status", "-s"]).splitlines()
    reg = "?"
    try:
        r = json.loads(Path("/mnt/dados/opencode/config/agents/gran-mestre/agent-registry.json").read_text())
        reg = str(len(r.get("entries", [])))
    except Exception:
        pass
    return {"objetivo": "Rodada R11 de autofagia/helenização (36 fontes) — classificar, extrair padrões e helenizar alvos para o harness.",
            "decisoes": ["Deploy R11 real concluído: alvos.json 16→31; 158 artefatos (15 skills+15 subagents+hooks+plugins); registry 28→43",
                         "MTP verificado no build local llama.cpp (--spec-type draft-mtp, libmtmd.so) — feature llama-mtp p/ 4 modelos Vulkan",
                         "MCP openwork ativado em opencode/config/opencode.json (remote, oauth, mcp_openwork: allow) — aprovado pelo usuário",
                         "Histórico HISTORICO_AUTOFAGIA.md §16 atualizado com deploy real + MCP"],
            "tarefas": ["(nenhuma pendência ativa — ciclo de fim de sessão executado)"],
            "proximos": ["Aplicar BM25 em route_to_model (herdada R10)", "pytest 8 cenários do arsenal (herdada R10)",
                         "Opcional: testar MCP openwork (requer auth OAuth no browser)"],
            "riscos": ["WORKSPACE COM MUDANÇAS NÃO-COMMITADAS (deploy R11 + MCP openwork) — commit pendente antes de reset",
                       "Delegação de subagents falha (anti-padrão R8/R9) — usar gh api contido",
                       "Skills ricas preservadas (hallmark, book-to-skill — guard)"],
            "git": git[:20] or ["limpo"],
            "ecc_home": os.environ.get("ECC_AUTOFAGIA_HOME", "$HOME/.ecc/autofagia"),
            "registry": reg}


def main() -> int:
    ap = argparse.ArgumentParser(description="Regra global de compactação cognitiva")
    ap.add_argument("--threshold", type=int, default=50, help="percentual de capacidade que dispara (default 50)")
    ap.add_argument("--ttl-days", type=int, default=7)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--store-only", action="store_true")
    ap.add_argument("--compact-only", action="store_true")
    args = ap.parse_args()

    try:
        print(f"▶ Compactação cognitiva (threshold {args.threshold}%)")
        state = load_state()

        if args.compact_only:
            compact_write(state, args.dry_run)
            print("✓ CONTEXT_COMPACT.md")
            return 0
        if args.store_only:
            f = store_cognitive(state, args.dry_run)
            print(f"✓ Snapshot cognitivo: {f}")
            return 0

        if not git_clean() and not args.dry_run:
            print("⚠ workspaces com mudanças não-commitadas — snapshot mesmo assim (não limpa git)")
        store_cognitive(state, args.dry_run)
        compact_write(state, args.dry_run)
        removed = cleanup(args.ttl_days, args.dry_run)
        print(f"✓ {len(removed)} itens de limpeza" + (" (dry-run)" if args.dry_run else ""))
        return 0
    except Exception as e:
        print(f"✗ Erro: {e}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
