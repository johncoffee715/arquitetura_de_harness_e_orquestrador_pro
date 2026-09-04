---
name: context-mode
description: >-
  >- Gestão de contexto longo para agentes via sandboxing de saída de ferramentas, retenção FTS5 e recuperação pós-compactação (helenizada de kujohnson/context-mode). Use quando tool outputs volumosos estourarem a janela, quando a sessão se aproximar de PreCompact, ou para recuperar contexto perdido a
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/context-mode
helenized: true
r84: true
r77_triple: true
---
# context-mode — modo contexto

Helenizado de [`https://github.com/context-mode`](https://github.com/context-mode) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
>- Gestão de contexto longo para agentes via sandboxing de saída de ferramentas, retenção FTS5 e recuperação pós-compactação (helenizada de kujohnson/context-mode). Use quando tool outputs volumosos estourarem a janela, quando a sessão se aproximar de PreCompact, ou para recuperar contexto perdido a

## Padrões absorvidos
- gerenciamento: contexto, modo, seleção
- Origem: https://github.com/context-mode
- Domínio: modo contexto

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `context-mode` (tags: contexto, modo).
2. `skill(name="context-mode")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/context-mode
