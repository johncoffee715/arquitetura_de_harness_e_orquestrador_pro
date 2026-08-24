---
name: memory-recall
description: >-
  Injeção/consulta rápida de memória Obsidian do harness, disponível para TODOS
  os modelos (regra global R26). Trigger: começar um turno com "memória: <tema>"
  ou quando o usuário perguntar "o que já fizemos?", "lembra de...", "contexto
  anterior". Preserva a janela: devolve apenas um bloco curto (<= 200 tokens)
  com o essencial do vault (/mnt/dados/cerebro com IA) — wiki, aprendizados,
  decisões, pipeline.
---
# Memory Recall (R26 — memória para todos os modelos)

## Trigger de uso
- Prefixo de turno: `memória: <tema>` — injeta o contexto Obsidian relevante.
- Perguntas de retomada: "o que já fizemos?", "onde paramos?", "lembra de X?".
- Início de sessão/task: consultar `wiki/index.md` + `pipeline/` para estado.

## Protocolo de consulta (preserva a janela)
1. **Resposta mínima obrigatória** — nunca despejar arquivos inteiros.
2. Formato do bloco injetado:
```
[MEMORIA] <tema>
- wiki: <1 linha por conceito/entidade relevante>
- aprendizados: <1 linha por item recente>
- decisoes: <1 linha por decisão arquivada>
- pipeline: <estado atual, se houver>
```
3. Máximo **200 tokens** no bloco. Se o contexto pedir mais, consultar o
   arquivo específico com Read (offset/limit).

## Fontes (ordem de consulta)
| Prioridade | Fonte | Conteúdo |
|------------|-------|----------|
| 1 | `wiki/index.md` | Índice do cérebro (entidades, conceitos, decisões, aprendizados) |
| 2 | `pipeline/contexto-atual` | Estado atual do pipeline |
| 3 | `aprendizados/` | Memória de longo prazo (nome tem data) |
| 4 | `decisoes/` | Decisões datadas |
| 5 | `wiki/concepts/`, `wiki/entities/` | Profundidade sob demanda |

## Regras (R26)
- **TODOS os modelos** têm acesso — não é privilégio do Gran-Mestre.
- **Sempre compacto** — a memória é referência de trigger, não dump.
- **Nunca escrever** sem necessidade — escrita via memory-keeper/Obsidian flow.
- Quando a consulta for vazia, responder `[MEMORIA] sem registros para "<tema>"` — nunca inventar.

## Anti-padrões
- NUNCA despejar arquivos inteiros do vault na janela.
- NUNCA inventar memórias que não existem no vault.
- NUNCA tratar este skill como substituto do context-compaction.
