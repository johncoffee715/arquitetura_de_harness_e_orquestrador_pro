---
name: dev-loop
description: "Loop de desenvolvimento de 3 níveis para iterar tasks rapidamente. Nível 1 (ReAct) para tasks isoladas. Nível 2 (Mini Loop Spec-Driven) para features locais. Nível 3 (Human Loop) para épicos e ciclos longos. Escalonamento automático entre níveis."
model: omniroute/auto/best-free
---

# Dev Loop — 3 Níveis de Iteração

## Propósito

Evitar que o modelo fique "tentando de novo" sem estrutura. Cada nível tem critérios de entrada, ciclo definido e condição de término (morte). O escalonamento entre níveis é **automático** — se N1 falha, sobe para N2. Se N2 encontra incerteza, sobe para N3 (humano decide).

---

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
5. [DONE]   Se passou → commit atômico e encerra
```

### Regras
- Máximo 3 iterações antes de escalonar para N2
- Cada iteração = 1 tool call de escrita + 1 de verificação
- Se erro novo aparecer na iteração 3, escala
- Commit só no passo 5

### Critério de Escalonamento para N2
```
- 3 falhas consecutivas
- Task cresceu além de 3 arquivos
- Precisou de rollback
- Modelo não conseguiu formular hipótese clara
```

### Critério de Morte
```
- Task completa e commitada
```

---

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

### Regras
- Branch morre com a feature (merge e deleta)
- Spec é congelada durante o ciclo
- Se spec precisar mudar → escala para N3
- Máximo 2 ciclos de TDD LOOP antes de escalar

### Critério de Escalonamento para N3
```
- Spec mudou durante o ciclo
- Feature afeta múltiplos módulos
- Incerteza arquitetural detectada
- 2 ciclos de TDD LOOP sem completar
- Precisou de rollback
```

### Critério de Morte
```
- Feature completa e mergeada
- Branch deletada
```

---

## Nível 3: Human Loop (Decide → Métricas → Triagem → Planeja → PR → Decide)

### Quando usar
- Épicos e features complexas
- Tasks que escalonaram do N2
- Decisões arquiteturais importantes
- Múltiplos módulos afetados
- Incerteza alta sobre direção

### Ciclo
```
ITERAÇÃO:
  ├── [DECIDE]   Humano diz: "faz X" ou "continua na direção Y"
  ├── [CONSULTA] Gran-Mestre busca métricas:
  │   ├── Execuções anteriores similares
  │   ├── Duração média, erros comuns
  │   ├── Padrões de sucesso/falha
  │   └── Dependências afetadas
  ├── [TRIAGEM]  Analisa:
  │   ├── Backlog atual
  │   ├── Prioridades do projeto
  │   ├── Blockers conhecidos
  │   └── Riscos identificados
  ├── [PLANEJA]  Cria épico com:
  │   ├── 1 spec clara
  │   ├── 5-15 tasks atômicas
  │   ├── Dependências mapeadas
  │   └── Critérios de aceite
  ├── [EXECUTA]  Executa via N1/N2 (delega para subagents)
  │   ├── ReAct para tasks pequenas
  │   └── Mini Loop para features locais
  └── [PR]       Abre Pull Request com:
      ├── Evidências de teste
      ├── Screenshots (se UI)
      ├── Decisões tomadas
      └── Pendências conhecidas

FIM? Humano decide:
  ├── CONTINUAR → próxima iteração
  ├── AJUSTAR → muda direção e repete
  └── ENCERRAR → merge final e arquiva
```

### Regras
- Humano **sempre** decide o próximo passo
- Gran-Mestre nunca toma decisão arquitetural sozinho
- Cada iteração produz um PR (não commit)
- Métricas alimentam o Shared Brain
- Máximo 10 iterações por épico (repete "ajustar" ilimitado)

### Critério de Morte
```
- Decisão humana explícita de encerrar
- Épico completo e mergeado
```

---

## Máquina de Estados do Dev Loop

```
                    ┌─────────────────────────────┐
                    │         TASK ENTRADA        │
                    └─────────────┬───────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │       CLASSIFICADOR         │
                    │   (1-3 arquivos? Spec OK?)  │
                    └──────┬──────────────┬───────┘
                           │              │
                      sim  │              │  não
                           ▼              ▼
                ┌──────────────────┐  ┌──────────────────┐
                │   NÍVEL 1 - ReAct│  │   NÍVEL 2 - Mini │
                │  (Think→Act→Obs) │  │  (Spec→TDD→Done) │
                └────────┬─────────┘  └────────┬─────────┘
                         │                     │
                   3 falhas?               spec mudou?
                         │                     │
                         └──────┬──────────────┘
                                │
                                ▼
                   ┌──────────────────────────┐
                   │    NÍVEL 3 - Human Loop   │
                   │ (Decide→Métricas→PR→Loop) │
                   └────────────┬─────────────┘
                                │
                          humano decide?
                          ├── CONTINUAR
                          ├── AJUSTAR
                          └── ENCERRAR
```

---

## Exemplos de Uso

### Exemplo 1: Debug de tipo TypeScript (N1)
```
Task: "arrumar erro de tipo em utils.ts"
Entrada: 1 arquivo, erro claro
Nível: N1 (ReAct)
Ciclo: [THINK] erro de tipo na linha 42 → [ACT] edita tipo → [OBSERVE] tsc passa → [DONE] commit
```

### Exemplo 2: Adicionar modal de confirmação (N2)
```
Task: "adicionar modal de confirmação antes de deletar"
Entrada: 1 módulo, spec clara
Nível: N2 (Mini Loop)
Ciclo: spec → branch → task1 (componente) → task2 (estado) → task3 (testes) → merge
```

### Exemplo 3: Implementar sistema de notificações (N3)
```
Task: "implementar sistema de notificações push"
Entrada: múltiplos módulos, incerteza alta
Nível: N3 (Human Loop)
Ciclo: humano decide "começar pelo backend" → métricas → triagem → planeja épico → executa → PR → humano decide "agora frontend" → repete
```

---

## Integração com Gran-Mestre

O Gran-Mestre:
1. Ao receber task, **classifica** o nível do Dev Loop
2. Se level=1: delega para subagent com skill dev-loop N1
3. Se level=2: delega para subagent com skill dev-loop N2
4. Se level=3: Gran-Mestre gerencia pessoalmente (coordena humano)
5. Registra métricas de cada iteração

---

## Observabilidade

Cada iteração registra:
```
[DevLoop] Level: {1|2|3}
[DevLoop] Iteration: {N}
[DevLoop] Action: {think|act|observe|done|escalate}
[DevLoop] Duration: {segundos}
[DevLoop] Files: {arquivos_afetados}
[DevLoop] Status: {success|failed|escalated}
```
