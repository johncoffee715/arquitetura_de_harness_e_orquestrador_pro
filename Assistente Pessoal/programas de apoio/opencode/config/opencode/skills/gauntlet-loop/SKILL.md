---
title: "Gauntlet Loop - Dev Loop em Diamante"
description: "Refatorar Dev Loop → Grafo em Diamante (Gauntlet Loop) com 6 fases, referencia path/SHA, criticador granite :9088, ondas aninhadas"
author: "local-forge/proposer"
category: "dev-loop"
version: "1.0"
tags: ["dev-loop", "gauntlet", "diamante", "dev-loop-refatoracao"]
---

# Gauntlet Loop - Dev Loop em Diamante

Refatorar o Dev Loop para Grafo em Diamante (Gauntlet Loop) conforme R25, R40, R84, R84 quarteto, Dev Loop N3, Hefesto MIX.

## Objetivo
Implementar o Gauntlet Loop como um loop de desenvolvimento em diamante com 6 fases:
1. Segmentação inicial (bite-sized)
2. Execução paralela dos subtasks
3. Críticos cegos avaliação
4. Refutação incansável (R40) até impressão genuína
5. Loop até impressão genuína
6. Validação final e diagrama diamante

## Referência
- Path: /dev/loop/diamante/path/SHA (referência de estado)
- Criticador: granite :9088 (granite 9088)
- Onda aninhada: ondas aninhadas (nested waves)

## Diagrama Diamante (no SKILL.md)

```
    [Phase 1: Segmentação]
      ↓
    [Phase 2: Execução paralela]
      ↓
    [Phase 3: Críticos cegos]
      ↓
    [Phase 4: Refutação incansável]
      ↓
    [Phase 5: Loop até impressão genuina]
      ↓
    [Phase 6: Validação final]
```

## Estrutura de arquivos
- conceito.md: 50-100 linhas de conceito (50-100 linhas conforme requisito)
- gabarito.json: esquema JSON válido
- mecanica.md: descrição da mecânica de ignição e fluxo
- mecanica.py: Pydantic model para validação
- schema.gbnf: GBNF para geração restrita
