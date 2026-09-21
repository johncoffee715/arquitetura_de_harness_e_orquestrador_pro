> [ARQUIVO FRI extraido de AGENTS.md em 2026-09-10 — regra R81/R82 integral aqui. AGENTS.md carrega apenas o stub de 3 linhas.]

# ═══ REGRA GLOBAL R81 — PADRÃO DE GERAÇÃO RESTRITA UNIVERSAL (CONSTRAINED DECODING) PARA TODO LLM — promulgado 2026-08-31 ═══

**Regra**: o padrão de **Geração Restrita + Pipeline de Validação Determinístico** é EXIGIDO para
**QUALQUER LLM do ecossistema, independentemente das capacidades cognitivas** (pequeno OU grande):
todo output estruturado (JSON, tool call, schema, extração) produzido por LLM local deve ser envelopado
em arquitetura de controle — o LLM é **motor de preenchimento de estados**, nunca gerador livre de sintaxe.

<Stack de controle obrigatório (5 camadas)>
1. **Definição de Tipos** — Python/Pydantic (ou JSON Schema): esquema rígido; o modelo só pode responder o que está tipado.
2. **Geração Restrita** — GBNF no motor (llama.cpp) ou FSM (Outlines/Instructor): tokens fora da regra = probabilidade zero (logit bias infinito negativo) ANTES do softmax; o modelo é FISICAMENTE impedido de alucinar sintaxe. Fonte única: gabarito.json (R77) → Pydantic → JSON Schema → GBNF em runtime (`LlamaGrammar.from_json_schema`); .gbnf manual = legado/fallback, nunca fonte nova.
3. **Controle de Estado** — .md (system prompts com tags XML separando instrução de dado) + .json (few-shot perfeito 3–5 interações Input→Output).
4. **Motor de Inferência estrito** — temp=0.0 para determinismo (f(x)=y), stop_tokens brutos (ex.: `["\n\n","```","<|eot_id|>"]`), max_tokens calculado do schema (trava física — modelo bate no muro rápido, economiza VRAM/tempo).
5. **Validação e Correção anti-loop** — Pydantic `model_validate_json` + retry com parse do erro re-injetado; `max_retries=3` (3 falhas = exceção no Python, NUNCA loop no LLM); fallback default obrigatório (JSON vazio/log), jamais realimentar falha em loop.

<Aplicação>
- Vale para TODOS os slots e TODAS as features (hefesto/forja, roteador-hibrido, needle, sdd, extractors, tool calling de qualquer subagente) — independente do modelo (Ornith-35B, granite-4.2-3b, ternary-8B, gemma-2B, lfm, rwkv).
- O gabarito R77 (.json) é a FONTE ÚNICA que transpila para Pydantic e GBNF — sem camadas duplicadas.
- Ferramental de referência: `skills/hefesto/tooling/hefesto_llama_bridge.py` (bridge + GBNF runtime) · `skills/hefesto/reference/constrained-decoding-doutrina.md` (doutrina completa) · `llama_cpp_config.json` (flags estritas).
- Exceção documentada: respostas livres/criativas (F1/F2 brainstorm, prosa R61 criativo) NÃO exigem GBNF — mas qualquer output que será consumido por máquina (JSON/tool call/schema) SIM.
- **Previsibilidade de LLM não vem do prompt ("seja cuidadoso") — vem da barreira física no amostrador + validação determinística + anti-loop de máquina (R43: scaffolding estrutural em vez de pedido).**

<Exemplo canônico (2026-08-31)>
- Hefesto upgrade: doutrina registrada em skills/hefesto/reference/constrained-decoding-doutrina.md + decision-log HEFESTO-CONSTRAINED-DECODING-2026-08-31; bridge já existente (hefesto_llama_bridge.py + hefesto_deep_spec.gbnf + hefesto_feature.gbnf) recebe o stack como motor padrão; pipeline FORJA passa a usar tool calling estruturado byte-level com schema 100% conforme (R29/R28).

---

# ═══ REGRA GLOBAL R82 — ESTRANGULAMENTO DE FEATURES VIA TRÍPLICE (.md .json .py .gbnf) — promulgado 2026-08-31 ═══

**Regra**: TODA feature gerada ou helenizada através do Hefesto (skill, subagent, hook, plugin, MCP, LSP,
script, watcher, gabarito, motor) **DEVE ser estrangulada via a tríplice/quadrúplice como estratégia
anti-loop, anti-alucinação e coesão ativa**:
- **.md** — ontologia/persona/instrução (system prompt imutável; tags XML separando instrução de dado).
- **.json** — gabarito/firewall (definição-fonte R77; esquema rígido; allow/deny; transpilável para Pydantic/GBNF).
- **.py** — mecânica de ignição/validação (motor determinístico; Pydantic `model_validate_json`; anti-loop max_retries=3 + fallback).
- **.gbnf** — barreira física no amostrador (gerada em runtime de Pydantic/JSON Schema; nunca fonte nova manual).

<Aplicação>
- Vale para QUALQUER feature nova ou helenizada (R74/R77/R81) — independente do modelo que a executa.
- Estrangulamento = o LLM da feature é envelopado: não gera livre, preenche estados dentro do contrato
  da tríplice; qualquer desvio é cortado na camada física (GBNF) ou determinística (Python).
- Coesão ativa: os 4 artefatos referenciam-se (fonte única no .json); mudança no contrato propaga para
  Pydantic e GBNF sem duplicação.
- Anti-loop: 3 falhas de validação = exceção Python + fallback default (nunca realimentar erro no LLM).
- Anti-alucinação: schemas rígidos + stop_tokens + max_tokens calculado (a feature não pode "inventar"
  campos nem se perder em justificativas).

<Exemplo canônico (2026-08-31)>
- Roadmap R81 implementado: `hefesto_llama_bridge.py` com `PydanticToGbnf` (transpilador runtime) +
  `constrained_generate` (retry/re-inject/fallback) + TDD (test_hefesto_bridge_r81.py); FORJA passa a
  consumir schema byte-level via bridge; gabarito.json → Pydantic → GBNF.

---

