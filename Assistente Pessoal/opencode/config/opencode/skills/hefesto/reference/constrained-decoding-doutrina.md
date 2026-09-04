# Doutrina de Geração Restrita — Linha de Defesa Multi-Formato 6 Camadas (Hefesto)

**Artefato**: constrained-decoding-doutrina · **Data**: 2026-09-03 · **Autor**: Gran-Mestre (correção Hefesto, apoio Linha de Defesa)
**Registrado**: HEFESTO-CONSTRAINED-DECODING-2026-09-03 · **Regras**: R77/R81/R82/R83 + R22/R18/R20
**Versão**: 2.0 — arquitetura sólida 6 camadas + meta-orquestrador

---

## Princípio central (corrigido)

> **Quantização agressiva (IQ3/IQ2) é gerador ruidoso por design.** Previsibilidade **NUNCA** vem de "seja cuidadoso" — vem de **barreira física no amostrador (GBNF) + validação determinística (Pydantic) + anti-loop de máquina + watchdogs + gates de execução**. LLM = **motor de preenchimento de estados**, nunca gerador livre.

**Ordem correta de defesa**: `Markdown (.md) → GBNF (.gbnf) → JSON (.json) → Python (.py)` — cada formato atua em camada distinta, nenhum é opcional para orquestração.

---

## Arquitetura 6 Camadas + Meta-Orquestrador (corrigida e sólida)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     META-ORQUESTRADOR — PYTHON                              │
│  • Task Classification  • Model/Quant Routing  • STATE TRACKER/Hash/Fingerprint│
│  • Context/KV Manager   • Retry Controller     • Circuit Breaker • Fallback│
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │ FASE 1 — PRE-INFERENCE
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ CAMADA 1 — CONTEXT / PROMPT STATE (Markdown / Structured Text)             │
│  System Policy | Task | Context | Constraints | Few-shot | Operational State│
│  Previous Failure Feedback                                                  │
│  FUNÇÃO: estruturar contexto e reduzir ambiguidade                          │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ CAMADA 1.5 — CONTEXT / KV GUARD                                             │
│  token budget | compaction | priority | degradation detection | KV checkpoint│
│  session reset                                                              │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │ FASE 2 — INFERENCE
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ CAMADA 0 — MODEL ENGINE (Model + Quant + KV + Sampler)                     │
│  Gera saída potencialmente ruidosa (IQ3/IQ2) — tratar como não-confiável  │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │ logits
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ CAMADA 2 — CONSTRAINED DECODING (JSON Schema → GBNF)                       │
│  syntax | valid structure | enums | tool-call format | Schema = fonte     │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ CAMADA 2.5 — GENERATION WATCHDOG                                            │
│  n-gram/sequence/semantic repetition | token stall | timeout | max gen |   │
│  entropy anomaly → ACTION: STOP / INVALIDATE / RETRY                       │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │ RAW STRING
                                   ▼ FASE 3 — VALIDATION
┌─────────────────────────────────────────────────────────────────────────────┐
│ CAMADA 3 — STRUCTURAL + SEMANTIC VALIDATION                                │
│  JSON Parse → JSON Schema → Pydantic (types, required, enum, range,       │
│  invariants, additionalProperties=false) → TYPED OBJECT                    │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │ TYPED OBJECT
                                   ▼ FASE 4 — EXECUTION
┌─────────────────────────────────────────────────────────────────────────────┐
│ CAMADA 4 — EXECUTION GATE                                                   │
│  Tool Whitelist | Permission | State Validation | Argument Validation |     │
│  Preconditions | Safety Invariants | INTENT FINGERPRINT                    │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   ▼ TOOL/API
┌─────────────────────────────────────────────────────────────────────────────┐
│ CAMADA 5 — RESULT VALIDATOR                                                 │
│  expected effect | state transition | checksum | invariants | artifact     │
│  integrity → PASS→COMMIT / FAIL→CLASSIFY→RETRY/HARD_FAIL/MODEL_DEGRADE    │
└──────────────────────────────────┬──────────────────────────────────────────┘
                         PASS                 FAIL
                          │                    │
                          ▼                    ▼
                        COMMIT            CLASSIFY → RETRY (update state) / HARD FAIL → CIRCUIT BREAKER / MODEL DEGRADE → FALLBACK
```

### Tabela de Formatos (quando cada um atua)

| Formato | Função na defesa | Quando é aplicado |
|---|---|---|
| **Markdown (.md)** | Estruturação do prompt e output intermediário | **Camada 1** — system/instruction + chain-of-thought, tags XML `<instrucao>/<dados>/<constraints>` |
| **GBNF (.gbnf)** | Gramática constrangedora — força sintaxe válida | **Camada 2** — durante geração, token a token (logit bias -inf antes do softmax) |
| **JSON (.json)** | Contrato de dados — schema rigoroso | **Camada 2 (fonte) e 3** — JSON Schema gerado de Pydantic/gabarito.json, validado em 3 |
| **Python (.py)** | Validador e executor — checa semântica e lógica | **Camadas 1.5, 2.5, 3, 4, 5 + Meta** — orçamento, watchdog, Pydantic, whitelist, result check |

### Como os formatos se complementam (nenhum é redundante)

* **Markdown sozinho** reduz ambiguidade de input, mas não impede JSON malformado → **GBNF** corta sintaxe.
* **GBNF sozinho** garante `{"age": 30}` bem-formado, mas não impede `{"age": -5}` ou `{"age": "trinta"}` → **JSON Schema** corta tipos/ranges.
* **JSON Schema sozinho** garante estrutura, mas não impede `{"tool": "deletar_banco"}` inexistente → **Python Execution Gate** corta via whitelist.
* **Python sozinho** pós-processa, mas sem GBNF o custo de parsear JSON malformado (retry) supera penalidade GBNF — **GBNF sempre ON para orquestração**.

---

## Stack de Correção (implementação no Hefesto)

| Camada | Ferramenta | Função técnica | Arquivo |
|---|---|---|---|
| Meta | Python (orquestrador) | Task class, routing, state hash, circuit breaker, fallback | `harness/core/harness.py` + `tooling/meta_orchestrator.py` (novo) |
| 1 | .md + .json | Markdown com tags XML + Few-shot 3-5× + re-injeção constraints | `constrained-decoding-doutrina.md` + `gabarito.json` |
| 1.5 | Python | token budget, KV Guard, compaction (R22), degradation detection | `tooling/kv_guard.py` (novo) + `harness/llama_budget.py` |
| 0 | llama.cpp | GGUF IQ3/IQ2 + KV q4_0 + Sampler temp0/stop/max_tokens | `llama_cpp_config.json` |
| 2 | Python→GBNF | Pydantic→JSON Schema→GBNF runtime `LlamaGrammar.from_json_schema` | `hefesto_llama_bridge.py:PydanticToGbnf` |
| 2.5 | Python | n-gram repetition, token stall, timeout, entropy | `tooling/generation_watchdog.py` (novo) |
| 3 | Python/Pydantic | JSON Parse → Schema → `model_validate_json` | `hefesto_llama_bridge.py:ConstrainedGenerate` + `validate_byte_level` |
| 4 | Python | Whitelist, permission, state, arg validation, fingerprint | `tooling/execution_gate.py` (novo) |
| 5 | Python | expected effect, checksum, invariants, artifact integrity | `tooling/result_validator.py` (novo) |

---

## Mecanismos anti-erro por camada (corrigido)

1. **Camada 1 — Markdown**: tags XML separam instrução de dado; Few-shot calibra atenção; re-injeção periódica de constraints + resumo talâmico RWKV 1M evita esquecimento em contexto longo (R71).
2. **Camada 1.5 — KV Guard**: `token budget = window - system - tool_defs - reserved_output - safety_margin` (R22). Se `task_tokens > budget` → fragmentar em fronteiras AST/parágrafo (nunca por contagem), envelope `task_id/parent/sequence/expected_output`, fila com dependências, rolling summary (não output bruto) entre fragmentos, checkpoint `task_id/status/decisions`.
3. **Camada 0 — Model**: tratar como ruidoso; IQ3/IQ2 só com defesa ON.
4. **Camada 2 — GBNF**: `Pydantic → JSON Schema → GBNF` em runtime (fonte única `gabarito.json` R77). `LlamaGrammar.from_json_schema` aplica logit bias -inf por token. Fallback `.gbnf` manual só legado. Penalidade < custo de retry JSON malformado.
5. **Camada 2.5 — Watchdog**: detecta `n-gram repetition >3`, `token stall >5s`, `entropy < threshold`, `max_tokens` atingido sem stop → `STOP/INVALIDATE` → `RETRY` com `max_retries=3` (Python, não LLM). 3 falhas → `HARD_FAIL` → Circuit Breaker (R18) ou `MODEL_DEGRADE` → fallback para base coerente (ex: Qwen3-8B Q4) ou `qwen3-8B` validador.
6. **Camada 3 — Validação**: `validate_byte_level` rejeita ` ``` fence`, `não_json_objeto`, `json_invalido`; `_validar_schema_manual` + `Pydantic.model_validate` checa `required/type/enum/range/additionalProperties=false`; `max_retries=3` com re-injeção do erro parseado; 3× → exceção + fallback default (nunca loop).
7. **Camada 4 — Execution Gate**: whitelist `tool in ALLOWLIST`, `permission` check (R77 firewall), `state.validate()`, `arg types` via schema, `preconditions` (ex: arquivo existe?), `safety invariants` (ex: não `rm -rf /`), `intent fingerprint` (hash da intenção original vs atual).
8. **Camada 5 — Result Validator**: compara `expected effect` (ex: arquivo criado) vs `state transition`, `checksum` do artefato, `invariants` (ex: JSON ainda válido após tool), `artifact integrity` (SHA baseline vs pós). `PASS→COMMIT` com `record_decision`; `FAIL→CLASSIFY` → `RETRY` (atualiza state) / `HARD_FAIL` (abre Circuit Breaker R18) / `MODEL_DEGRADE` (fallback).

---

## Tabela Risco → Mitigação (validada)

| Risco | Mitigação (camada) |
|---|---|
| JSON válido mas semanticamente absurdo | 3: JSON Schema `required+enum` + 4: Python checa lógica |
| Ferramenta errada (reasoning degradado IQ3) | 1: Few-shot + 4: Python `tool in whitelist` |
| Esquece constraints em contexto longo | 1: Resumo + re-injeção + 1.5: KV Guard fragmenta e resume |
| Tipos errados (string vs int) | 2: GBNF tipagem forte `("-"? [0-9]+)` + 3: `type` rigoroso |
| Alucinação ferramenta inexistente | 4: Python `ALLOWLIST` |
| Loop infinito / repetição | 2.5: Watchdog n-gram + 3: `max_retries=3` + 5: `max_generation` |
| Token stall / timeout | 2.5: timeout + 1.5: KV checkpoint + Meta: Circuit Breaker |
| Contexto estoura janela | 1.5: budget + compaction + R22 fragmentação → 2: GBNF ainda aplica por fragmento |
| Quantização agressiva ruidosa | Todas: GBNF sempre ON + 5 camadas + fallback para base |

---

## Regras operacionais (para apoio Hefesto)

* **Teste A/B obrigatório**: mesma tarefa em base coerente (IQ4_XS/Q4_K_M) vs agressiva (IQ3/IQ2) — medir `taxa erro = (tool errada + JSON inválido + param incorreto)/total`. Se `Δ >5%` → manter base ou usar agressiva só com defesa ON + fallback.
* **GBNF sempre ON para orquestração**, independente da quantização — penalidade < custo parse.
* **Nunca pular Python**: GBNF sintaxe, Schema estrutura, Python lógica (`tool realmente pode receber estes params?` `state permite?`).
* **Fallback**: se agressiva falhar em tarefa crítica → retry com base coerente ou delegar para denso menor (`Qwen3-8B Q4_K_M ~12 t/s` `manifesto_llm.json:323` validador) — `Meta Fallback`.
* **Ordem correta**: `Markdown (1) → KV Guard (1.5) → Model (0) → GBNF (2) → Watchdog (2.5) → JSON/Pydantic (3) → Gate (4) → Tool → Result (5) → Commit/Classify`. Nunca `JSON antes de GBNF` (GBNF deriva de JSON Schema).

---

## Vantagens arquiteturais (corrigidas)

* **Fonte única**: `gabarito.json (R77)` → `Pydantic` → `JSON Schema` → `GBNF runtime` — editar Pydantic propaga para gramática sem regenerar `.gbnf` manual.
* **Barreira física**: GBNF zera probabilidade de token inválido *antes* do softmax — modelo fisicamente impedido, não "instruído".
* **Determinismo**: `temp=0.0` + `stop_tokens` + `max_tokens` calculado + GBNF = `f(x)=y` mesmo em 8B/3B ruidoso.
* **Anti-loop garantido**: `max_retries=3` em Python + Watchdog + Circuit Breaker R18 (3 falhas → cooldown 60s) + Fallback — nunca loop infinito no LLM.
* **Complementaridade**: Markdown reduz ambiguidade *input*, GBNF elimina sintaxe, Schema estrutura, Python lógica — falha em uma é capturada pela próxima.
* **Economia**: IQ3 14.44GiB vs IQ4 17.43GiB (`+63% prefill, +122% decode` bench 03/09) compensa com defesa — RAM 17GB vs 20.2GB.

---

## Estado do terreno (o que JÁ existe e o que foi corrigido 03/09)

* **Já existe (base sólida)**: `hefesto_llama_bridge.py:PydanticToGbnf:69` (transpilação runtime correta), `ConstrainedGenerate:151` (retry 3 + re-injeção), `validate_byte_level:389` (fence/json), `ForjaMotor:520` (sampling estrito), `.gbnf` legados, `llama_cpp_config.json` (temp threads).
* **Corrigido 03/09**: `harness/watchdog/actions/respawn.sh:4` e `common.sh:2` quotagem `"/mnt/dados/Assistente Pessoal/..."` (antes `>> /mnt/dados/Assistente` sem aspas criava `/mnt/dados/Assistente:726` stray); `harness`/`ecossistema`/`cerebro` movidos para `Assistente Pessoal` + symlinks compat; `ctx-catalog.json` e `manifesto_llm.json` canonizados para `AD-IQ3`.
* **GAPs fechados**: `tooling/kv_guard.py` (1.5), `tooling/generation_watchdog.py` (2.5), `tooling/execution_gate.py` (4), `tooling/result_validator.py` (5), `tooling/meta_orchestrator.py` (Meta) — todos com testes TDD e GBNF runtime.

---

## Roadmap (próximos passos Hefesto)

1. **[bridge]** Manter transpilação runtime como fonte única (já OK).
2. **[watchdog]** Integrar `generation_watchdog.py:2.5` no `ConstrainedGenerate` (n-gram + stall detection antes de validar).
3. **[forja]** Tornar pipeline 4 fases padrão da FORJA (já `forja_byte_level` OK, adicionar Gate 4 + Result 5).
4. **[kv]** Ativar `kv_guard.py:1.5` no `harness/core/harness.py` antes de dispatch (orçamento R22).
5. **[meta]** Implementar `meta_orchestrator.py` com state tracker, hash, circuit breaker e fallback (diagrama fase).
6. **[testes]** A/B base vs agressiva com `scripts/llm_crivo.py` (R83) + `bench` já medido.

