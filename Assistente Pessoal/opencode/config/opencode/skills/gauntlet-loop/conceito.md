# Gauntlet Loop - Conceito em Diamante

## Objetivo
Implementar o Gauntlet Loop como um loop de desenvolvimento em diamante com 6 fases conforme R25, R40, R84 quarteto, Dev Loop N3, Hefesto MIX.

## Fases do Gauntlet Loop (Dev Loop em Diamante)

1. **Segmentação inicial** (Bite-sized)
   - Divide a tarefa principal em subtasks gerenciáveis (≤ 200 tokens cada).
   - Cada subtask carrega seu envelope mínimo (YAML/JSON) com estado de progresso.
   - Verifica se cada subtask cabe na janela de contexto da tarefa principal.

2. **Execução paralela**
   - Executa os subtasks em paralelo usando workers separados.
   - Cada worker carrega o envelope mínimo do subtask.
   - Monitora progresso com checkpoints após cada subtask.
   - Usa TDD write-first para cada subtask.

3. **Críticos cegos** (Cegos Criticador)
   - Avalia os resultados dos subtasks contra critérios de críticos cegos.
   - Identifica falhas que não são visíveis na tarefa principal.
   - Registra evidência de falhas e correções.
   - Se falha crítico, reinicia o subtask com ajuste de parâmetros.

4. **Refutação incansável (R40)**
   - Inicia uma refutação incansável contra o criticador (granite :9088).
   - Loop de refutação até impressionar genuína (R40) — não para até que o veredito categórico seja PASSOU_CATEGORICO.
   - Cada iteração: critico refuta → resposta da subtask → refutador avalia → ciclo até impressão genuína.
   - Loop de refutação: 3 rodadas sem impressão genuína = escalar para fallback nuvem.

5. **Loop até impressão genuína**
   - Repete o loop de refutação incansável até obter impressão genuína (nota ≥ 90 na escala R34).
   - Verifica se a impressão é genuína (verificação de qualidade, coesão, sem acertos irrelevantes).
   - Se após 3 rodadas ainda não é genuína → escalar para fallback nuvem (omirute) ou rerefatorar.
   - Se for nuvem, retorna com evidência de progresso.

6. **Validação final**
   - Executa validação final completa: TDD write-first, testes reais, validação de contrato.
   - Verifica se o diagrama diamante está construído corretamente.
   - Salva artefato final com evidência fresca (hash do output).
   - Registra score e log de debug para retroalimentação.

## Referência (path/SHA)
- Referência de estado: /dev/loop/diamante/path/SHA
- Criticador: granite :9088 (criticador = granite 9088)
- Onda aninhada: ondas aninhadas (nested waves)

## Diagrama Diamante (em SKILL.md já presente)

```
    [Phase 1: Segmentação]
      ↓
    [Phase 2: Execução paralela]
      ↓
    [Phase 3: Críticos cegos]
      ↓
    [Phase 4: Refutação incansável]
      ↓
    [Phase 5: Loop até impressão genuína]
      ↓
    [Phase 6: Validação final]
```
