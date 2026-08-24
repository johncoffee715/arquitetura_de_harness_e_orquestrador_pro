---
name: context-compaction
description: "Regra global de compactação cognitiva a 50% de capacidade: ARMARENAR → COMPACTAR → LIMPAR antes de qualquer compactação de contexto, preservando workflow e workspace e evitando alucinações por estouro de contexto. Acionar quando a sessão atingir ~50% da janela de contexto, em PreCompact, ou ao iniciar longa sessão de retomada."
---

# Context Compaction — Regra Global (50%)

## Política (3 estágios, sempre nesta ordem)

1. **ARMAZENAR** — persiste o estado cognitivo ANTES de perder contexto:
   - `harness/CONTEXT.md` — snapshot de decisões/pendências/git
   - `cerebro com IA/decisoes/<data>-compactacao.md` — decisão arquivada
   - `cerebro com IA/pipeline/contexto-atual.md` — continuidade entre sessões
2. **COMPACTAR** — escreve `harness/CONTEXT_COMPACT.md` (essência p/ retomada:
   objetivo, decisões, tarefas ativas, próximos passos, riscos)
3. **LIMPAR** — remove lixo não-essencial (não-git, TTL): `__pycache__` órfãos,
   `.tmp`, `.bak.*` antigos (>3) — NUNCA arquivos de trabalho nem git

## Disparos

- `PreCompact` / compactação automática da sessão (hook `ecc-compact-gate.sh`)
- Quando a janela de contexto do modelo chega a ~50% de capacidade
- Início de retomada de sessão longa (para garantir snapshot fresco)

## Uso

```bash
python3 /mnt/dados/harness/cognition/compact_context.py          # tudo
python3 .../compact_context.py --dry-run                         # preview
python3 .../compact_context.py --store-only                     # só armazenar
python3 .../compact_context.py --compact-only                   # só compactar
COMPACT_DRY=1 bash ~/.claude/hooks/ecc-compact-gate.sh          # via hook
```

## Garantias (preservação de workflow/workspace)

- Nunca altera arquivos rastreados pelo git (valida `git status`; avisa se sujo)
- `--dry-run` não escreve nada (idempotente)
- Exit codes: 0 ok · 3 erro
- A limpeza só remove lixo não-git com TTL — arquivos de trabalho intactos

## Relação com o harness

- Sincroniza o pipeline com a memória cognitiva (Obsidian/cerebro)
- Previne alucinações por estouro de contexto ao compactar com estado salvo
- Suporta `harness/CONTEXT.md` (consumido pelos checks de fase do Gran-Mestre)

## Fonte

Padrão absorvido de Ratel/Context-Engineering (context-selector) + prática
de memória Obsidian do harness — R10.
