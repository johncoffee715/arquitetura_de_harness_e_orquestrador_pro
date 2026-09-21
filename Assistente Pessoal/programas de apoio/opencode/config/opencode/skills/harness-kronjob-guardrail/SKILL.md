---
name: harness-kronjob-guardrail
description: "Global guardrail specification for 10-element architecture (1x VRAM, 8x CPU, 1x C-LIB): Tálamos pre-filter via fast CPU slot, Protected Core model hierarchy, Intent routing. Helenizado de HARNESS KRONJOB GLOBAL GUARDRAIL.py (sha256 054754c86bacfcf0f6c595cec297856cfa6933f17ce53559b87202c5ddd5c5bd)."
mode: skill
tags: "kronjob, talamos, guardrail, arquitetura, 10-elementos, roteamento, intencao"
origin: "hefesto: HARNESS KRONJOB GLOBAL GUARDRAIL.py (sha256 054754c86bacfcf0f6c595cec297856cfa6933f17ce53559b87202c5ddd5c5bd)"
metadata:
  category: guardrail
  version: 1.0.0
  date: 2026-08-27
  author: Gran-Mestre
  source_file: "tranqueiras/autofagia e helenizaçao/HARNESS KRONJOB GLOBAL GUARDRAIL.py"
  source_sha256: "054754c86bacfcf0f6c595cec297856cfa6933f17ce53559b87202c5ddd5c5bd"
  pipeline: DECOMPILAÇÃO → AUTOFAGIA → HELENIZAÇÃO → FORJA
  panteao_score: 96.625
  status: OLYMPIAN_PERFECTION
---

# HARNESS KRONJOB GUARDRAIL — Skill Helenizada v1.0.0

Pipeline de guardrail para arquitetura 10-elementos (1x VRAM + 8x CPU + 1x C-LIB).
Origem: HARNESS KRONJOB GLOBAL GUARDRAIL.py — helenizado via HEFESTO v1.0.0.

## Arquitetura 10-Elementos

```
┌─────────────────────────────────────────────────────────────────┐
│                    HARNESS KRONJOB GUARDRAIL                    │
├─────────────────────────────────────────────────────────────────┤
│  [ENTRADA] ──→ [TÁLAMOS FILTER] ──→ [PROTECTED CORE]          │
│                    (CPU slot)              (VRAM slot)          │
├─────────────────────────────────────────────────────────────────┤
│  TÁLAMOS (CPU): intent pre-classification (108 t/s)            │
│  PROTECTED CORE: 4 modelos (ORCHESTRATOR, DEEP_REASONING,      │
│                  REFUTATION, PLANNER)                          │
│  C-LIB: libneedle.a native (L0 micro-router)                   │
└─────────────────────────────────────────────────────────────────┘
```

## Componentes

### 1. Tálamos Filter (CPU Slot Rápido)

Pré-filtro via slot CPU de alta velocidade (qwen3.5-0.8b @108 t/s) para:
- Classificar intent (PRIMITIVE_HELLO, NEEDLE_SEARCH, RAG, etc.)
- Destilar contexto (suco condensado)
- Roteamento inteligente antes do dispatch para VRAM

### 2. Protected Core (VRAM + CPU Hierarchy)

| Slot | Modelo | Device | Função |
|------|--------|--------|--------|
| ORCHESTRATOR | role:orchestrator | CPU (:8083) | Orquestração de alta precisão (Ornith-35B) |
| PROPOSER | role:proposer | GPU (:9088) | Raciocínio profundo / código pragmático |
| REFUTER | role:refuter | GPU (:9090) | Refutação adversarial |
| JUDGE | role:judge | GPU (:9085) | Validação neutra / arbitragem |
| INGESTOR | role:ingestor | GPU (:9084) | Filtro Talâmico / fatiamento |
| REFLEXO | role:reflexo | GPU (:9086) | Refutação de alta velocidade R42 |

### 3. C-LIB (libneedle.a Native)

Micro-router L0 em C nativo para busca exata em volume massivo.

## Intent Patterns

| Pattern | Ação |
|---------|------|
| `PRIMITIVE_HELLO_OR_THANKYOU` | Resposta direta (poupa 100% VRAM) |
| `NEEDLE_EXACT_SEARCH_TRIGGER` | Dispatch para C-LIB (libneedle.a) |
| `RAG_DOCUMENTS` | Reranking de contexto |
| `LONG_CHAT_HISTORY` | Sumarização para 1 parágrafo |
| `RAW_LOGS` | Extração de ERROR/CRITICAL |
| `WEB_SCRAPING` | Limpeza de ruído HTML/markdown |

## Uso

```python
from harness_kronjob_guardrail import KronjobGuardrail

guardrail = KronjobGuardrail()
result = guardrail.process_request(input_data)
```

## Correções vs Original

| Original | Helenizado |
|----------|-----------|
| Port 9090 hardcoded | Dynamic resolution via llm-inventory.json |
| Port 8083 hardcoded | Dynamic resolution via R47 |
| temperature: 0.0 fixed | Per-model R61 settings |
| HTTP needle2 URL | C-LIB concept (libneedle.a) |

## Slot Resolution (R35/R47)

Os slots são resolvidos dinamicamente do inventário real:

```bash
python3 scripts/hefesto_motor.py --resolve forja  # → ornith @8083
python3 scripts/hefesto_motor.py --resolve refutador  # → ternary @9090
python3 scripts/hefesto_motor.py --list-cpu  # → 8 slots CPU online
```

## Integração

- **Gran-Mestre**: usa como guardrail de entrada antes de dispatch
- **Tálamos hook**: injetado em `session.start`
- **Sentinel Guard**: complementa para auditoria adversarial

## Relacionamento com Regras

- **R1**: orquestrador delega, não executa
- **R8**: catálogo primeiro (GAP verificado)
- **R13**: modelo mais competente por caso de uso
- **R28**: critério de trânsito categórico
- **R34**: escala 0.0000001–100
- **R35/R47**: slot resolution dinâmico
- **R51**: Obsidian Sync Bridge
