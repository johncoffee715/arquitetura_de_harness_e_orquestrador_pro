---
template: modulo-canonical
versao: 1.0
origem: spec-camada-autopoietica-v1 (SS-M1)
tags: [template, scaffolding]
---
# <NOME DO MÓDULO>

> Todo skill/subagent/hook/plugin/script NOVO nasce deste template. Sem exceção (G-AUD1).

```yaml
id: <id-curto-hifen>
tipo: plugin|hook|skill|subagent|script|mcp|lsp
versao: 0.1.0
data: YYYY-MM-DD
origem: absorvido:<owner/repo> | autoral | helenizado-de:<fonte>
modelo: <llm recomendado> + fallback: <llm alternativo|nenhum>
autonomia: auto | supervisionado
fase_grafo: F0|F1|F2|F3|F4|F5|F6|transversal
path: <caminho relativo na árvore portátil>
```

## Papel
<uma frase: o que este módulo faz>

## O que NÃO faz
- <fronteira explícita 1>
- <fronteira explícita 2>

## Ciclo de validação
1. <teste/verificação obrigatória antes de registrar>
2. <critério de trânsito R28: PASSOU_CATEGORICO com evidência>

## Interface
<como é invocado: comando, trigger, API>

## Histórico
- 0.1.0 — <data> — criação
```
