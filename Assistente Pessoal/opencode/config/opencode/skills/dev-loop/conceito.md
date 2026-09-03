# Dev Loop — 3 Níveis de Iteração

## Propósito
Evitar que o modelo fique "tentando de novo" sem estrutura. Cada nível tem critérios de entrada, ciclo definido e condição de término (morte). O escalonamento entre níveis é **automático** — se N1 falha, sobe para N2. Se N2 encontra incerteza, sobe para N3 (humano decide).

## Nível 1: ReAct (Think → Act → Observe → Repeat)

### Quando usar
- Tasks pequenas e isoladas (1-3 arquivos)
- Debug rápido, ajuste simples
- Exploração de código
- Tasks que cabem em 1-3 tool calls

### Ciclo
```
1. [THINK]  Analisa o problema e formula hipótese
2. [ACT]    Executa ação (edita código, roda comando, busca info)
3. [OBSERVE] Verifica resultado (teste, diff, erro, saída)
4. [REPEAT] Se falhou → volta ao passo 1 com novo insight
5. [DONE]    Se passou → commit atômico e encerra
```

### Escalonamento para N2
- 3 falhas consecutivas
- Task cresceu além de 3 arquivos
- Precisou de rollback
- Modelo não conseguiu formular hipótese clara

### Morte
- Task completa e commitada

## Nível 2: Mini Loop (Spec-Driven)

### Quando usar
- Features locais e bem definidas (1 módulo)
- Tasks que escalonaram do N1
- Features com requisitos claros (até 5 tasks)
- Refatorações de escopo médio

### Ciclo
```
FASE 0: [SETUP]
  ├── Cria branch nova: `feature/<slug>`
  ├── Define spec da feature (1-3 sentenças de aceite)
  └── Decompõe em 3-5 tasks atômicas

FASE 1: [TDD LOOP] Para cada task:
  ├── [TEST]  Escreve teste que falha (RED)
  ├── [CODE]  Implementa mínimo para passar (GREEN)
  ├── [REFACTOR] Limpa código (REFACTOR)
  └── [COMMIT] Commit atômico: `task-N: <descrição>`

FASE 2: [VERIFY]
  ├── Roda todos os testes
  ├── Verifica lint/type-check
  └── Se falhou → volta ao TDD LOOP

FASE 3: [DONE]
  ├── Roda testes integrados
  ├── QA básico (fumaça)
  ├── Merge branch
  └── Encerra
```

### Escalonamento para N3
- Spec mudou durante o ciclo
- Feature afeta múltiplos módulos
- Incerteza arquitetural detectada
- 2 ciclos de TDD LOOP sem completar
- Precisou de rollback

### Morte
- Feature completa e mergeada
- Branch deletada
