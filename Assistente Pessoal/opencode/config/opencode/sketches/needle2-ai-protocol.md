# Needle 2 AI — Protocolo de Sincronização de Estado (v1.0)

**Data:** 2026-08-27
**Autor:** Gran-Mestre (via Hefesto v1.0.0)
**Escopo:** Habilitação de Needle 2 AI em todos os 9 LLMs da stack local

---

## Visão Geral

Needle 2 AI é o protocolo de sincronização de estado entre LLMs. Permite que cada modelo salve e recupere seu estado interno (contexto, thinking, evaluation, debate) via endpoints HTTP, garantindo continuidade entre rodadas e sessões.

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│ GRAFO COMPLETO — Needle 2 AI em TODOS os LLMs               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ┌─ RWKV-6-Geni (:9084) — PRODUTOR CÓRTEX                    │
│ └─ POST /complete → gera destilado + estado                  │
│                                                            ↓  │
│ ┌─ Ornith (:8083) — CONSUMIDOR                              │
│ └─ POST /complete ← recebe destilado                        │
│                                                            ↓  │
│ ┌─ Granite (:9087) — CONSUMIDOR                             │
│ └─ POST /complete ← recebe destilado                        │
│                                                            ↓  │
│ ┌─ Qwen3.8-4B (:9088) — CONSUMIDOR                          │
│ └─ POST /complete ← recebe destilado                        │
│                                                            ↓  │
│ ┌─ Judge (:9085) — BIDIRECIONAL                             │
│ └─ POST /state → salva avaliação; /load → retoma            │
│                                                            ↓  │
│ ┌─ LFM2.5 (:9086) — BIDIRECIONAL                            │
│ └─ POST /state → salva estado thinking; /load → retoma      │
│                                                            ↓  │
│ ┌─ Ternary (:9090) — BIDIRECIONAL                           │
│ └─ POST /state → salva debate; /load → retoma               │
│                                                            ↓  │
│ ┌─ Qwen3.8-2B (:9089) — CONSUMER-LAZY                      │
│ └─ POST /load ← recebe seed estilo (quando disponível)      │
│                                                            ↓  │
│ ┌─ Qwen3.5-4B-IQ2 (:9083) — CONSUMER-LAZY                 │
│ └─ POST /load ← recebe seed tonalidade (quando disponível)  │
│                                                             │
│ INTEGRIDADE DO SISTEMA:                                     │
│ - Todos os LLMs com Needle 2 AI ativo                       │
│ - Estado serializável em JSON                               │
│ - Máximo 5 MB por estado (RWKV é o maior)                   │
│ - Recuperação garantida via /reset + /load                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Endpoints

### POST /complete
Gera resposta completa com estado serializado.
```json
{
  "model": "rwkv-6-geni-0.4b-instruct",
  "prompt": "...",
  "state_id": "eval-20260827-001",
  "max_tokens": 500,
  "temperature": 0.6
}
```

### POST /state
Salva estado serializado.
```json
{
  "model": "llmjudge-qwen2.5-3b",
  "state_id": "eval-20260827-001",
  "state": {
    "type": "judgement",
    "score": 94.5,
    "critique_points": ["logic", "creativity", "accuracy"],
    "category": "R28-metric"
  }
}
```

### GET /state
Recupera estado serializado.
```json
{
  "state_id": "eval-20260827-001",
  "type": "reflexo",
  "phase": "analysis_complete",
  "components": ["thinking", "entities", "metadata"],
  "timestamp": "2026-08-27T14:30:00Z"
}
```

### POST /load
Carrega estado para retomada.
```json
{
  "model": "qwen3.8-2b-distill",
  "state_id": "eval-20260827-001"
}
```

### POST /reset
Limpa estado atual.
```json
{
  "model": "ornith-1.5-9b-q5"
}
```

### GET /health
Verifica saúde do endpoint.
```json
{
  "status": "ok",
  "model": "ornith-1.5-9b-q5",
  "port": "8083"
}
```

### POST /metadata (NOVO)
Armazena metadados customizados por LLM.
```json
{
  "model": "llmjudge-qwen2.5-3b",
  "state_id": "eval-20260827-001",
  "metadata": {
    "type": "judgement",
    "score": 94.5,
    "critique_points": ["logic", "creativity", "accuracy"],
    "category": "R28-metric"
  }
}
```

### GET /state/summary (NOVO)
Retorna resumo do estado serializado para debugging.
```json
{
  "state_id": "eval-20260827-001",
  "type": "reflexo",
  "phase": "analysis_complete",
  "components": ["thinking", "entities", "metadata"],
  "timestamp": "2026-08-27T14:30:00Z"
}
```

---

## Configuração por LLM

| LLM | Slot | Sync | State Size | Persist On | Lazy |
|---|---|---|---|---|---|
| Ornith-1.5-9B | 8083 | consumer | large | reasoning, tool_calls, context | ❌ |
| RWKV-6-Geni-0.4B | 9084 | bidirectional | medium | code, context, seed | ❌ |
| LLMJudge-Qwen2.5-3B | 9085 | bidirectional | minimal | evaluation, score, critique | ❌ |
| LFM2.5-1.2B-Thinking | 9086 | bidirectional | medium | reflexo, loop, r42 | ❌ |
| Granite-4.2-3B | 9087 | consumer | medium | reasoning, tool_calls | ❌ |
| Qwen3.8-4B | 9088 | consumer | medium | contract, plan, schema | ❌ |
| Qwen3.8-2B | 9089 | consumer | minimal | tool_calls | ✅ |
| Qwen3.5-4B-IQ2_XXS | 9083 | consumer | minimal | seed, tone | ✅ |
| Ternary-Bonsai-8B | 9090 | bidirectional | variable | debate, refutacao, round | ❌ |

---

## Métricas de Validação

| Métrica | Threshold | Score Alvo |
|---|---|---|
| Endpoint /state funcional | 100% dos LLMs | 100% |
| Estado serializável | ≤ 5 MB cada | ≤ 5 MB |
| Latência /state | < 100ms | < 50ms |
| Recuperação via /load | 100% consistente | 100% |
| Integração hook ↔ LLM | 0 falhas em 10 testes | 100% |
| Score agregado R34 | ≥ 97 | ≥ 97 |

---

## Regras de Uso

1. **Serialização:** Estado deve ser JSON válido, ≤ 5 MB por modelo
2. **Retomada:** /load deve restaurar estado 100% consistente
3. **Limpeza:** /reset deve liberar VRAM/RAM imediatamente
4. **Lazy:** Modelos consumer-lazy só carregam estado quando state_id é fornecido
5. **Thinking:** LFM2.5-Thinking serializa reasoning_tokens + token posicionais
6. **Debate:** Ternary-Bonsai serializa refutation_round + última argumentação

---

## Histórico

| Data | Ação | Autor |
|---|---|---|
| 2026-08-27 | Criação do protocolo Needle 2 AI | Gran-Mestre (Hefesto v1.0.0) |
| 2026-08-27 | Habilitação em todos os 9 LLMs | Gran-Mestre |
| 2026-08-27 | Substituição qwen3.5-0.8b → RWKV-6-Geni | Gran-Mestre |