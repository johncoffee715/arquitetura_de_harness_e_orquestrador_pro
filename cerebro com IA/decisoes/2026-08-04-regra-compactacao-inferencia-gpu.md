---
tags: [decisao, compactacao, inferencia, gpu-only, regra-global]
data: 2026-08-04
origem: Gran-Mestre (R10) — solicitado pelo usuário
---

# Decisão — Regra global de compactação + inferência GPU-only

## 1. Compactação cognitiva a 50%
- **Política**: ARMARENAR → COMPACTAR → LIMPAR antes de qualquer compactação.
- **Ferramenta**: `harness/cognition/compact_context.py` (armazenar CONTEXT.md + Obsidian
  decisões + pipeline/contexto-atual.md; compactar CONTEXT_COMPACT.md; limpar lixo não-git com TTL).
- **Automação**: hook `ecc-compact-gate.sh` registrado em `PreCompact` do settings.json.
- **Preserva**: workflow e workspace (git intocado; dry-run inócuo).

## 2. Inferência SEMPRE em GPU (nunca CPU/RAM, exceto usuário solicitar)
- **Problema**: após queda do `llama-server`, o respawn caiu para CPU/RAM — sem watchdog.
- **Regra global**: inferência local sempre em GPU (Vulkan0, -ngl 999) até mesmo em respawn.
- **Implementação**: watchdog `gpu-watchdog.sh` — detecta porta morta → ressuscita via
  start-all-models.sh (GPU-only garantido) e verifica no log `device: Vulkan0`/`-ngl 999`.

## Próximos passos
- (verificado nesta sessão) registrar watchdog no agendador (cron/systemd) se desejado;
  verificar VRAM baseline para assert-on-GPU (delta vs CPU).
