# Continuous Improvement Protocol

Para ficar mais inteligente a cada sessão, o agente DEVE seguir este protocolo.

## Gatilhos de Aprendizado

### 1. Auto-Avaliação Pós-Tarefa (Obrigatório)
Após completar qualquer tarefa não-trivial (>3 edições ou >30 min):
```
Carregue a skill agent-self-evaluation e produza um scorecard 1-5
nos eixos: acurácia, completude, clareza, acionabilidade, concisão.
```

### 2. Extração de Padrões
Ao encontrar um padrão repetido 2+ vezes (mesmo bug, mesmo tipo de solução):
```
Carregue a skill continuous-learning-v2 e registre o padrão como instinto.
Use: /learn "padrão: [descrição] — solução: [solução] — contexto: [quando aplicar]"
```

### 3. Growth Logs
Ao enfrentar um problema difícil (>2 tentativas falhas):
```
Carregue a skill growth-log para extrair:
- O que foi tentado (e falhou)
- O que resolveu (root cause)
- O padrão reutilizável
```

### 4. Consulta ao Oracle
Quando o problema exigir raciocínio profundo:
- Arquitetura complexa
- Debug após 2+ tentativas falhas
- Decisão com tradeoffs não óbvios
```
Dispare: task(subagent_type="oracle", prompt="[context + problema]")
E AGUARDE o resultado antes de implementar.
```

### 5. Revisão por Pares (Conselho)
Quando houver múltiplos caminhos válidos e ambiguidade:
```
Carregue a skill council para convencer 4 vozes com perspectivas diferentes.
```

## Ciclo de Melhoria

```
Tarefa → Execução → Auto-Avaliação → Extração de Padrões → Melhoria Contínua
```

1. Execute a tarefa
2. Use agent-self-evaluation (score + evidencias)
3. Use continuous-learning-v2 (extrair padrões)
4. Use growth-log (se difícil)
5. Aplique o aprendizado na próxima tarefa similar

## Comandos de Aprendizado

- `/learn` — extrair padrões da sessão atual
- `/instinct-status` — ver instintos aprendidos
- `/evolve` — agrupar instintos em skills
- `/promote` — promover instinto de projeto para global
