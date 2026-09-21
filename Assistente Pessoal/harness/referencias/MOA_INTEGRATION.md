---
name: moa-integration
description: "Integração do padrão Mixture of Agents (MoA) ao Gran-Mestre. Execução paralela de múltiplos modelos com agregação crítica para máxima qualidade."
mode: subagent
origin: absorvido:togethercomputer/moa
metadata:
  category: orchestration
  version: 2.0.0
  author: Gran-Mestre (autofagia de MoA)
  source: https://github.com/togethercomputer/moa
  stars: 29300
  paper: https://arxiv.org/abs/2406.04692
  note: "MoA achieves 65.1% on AlpacaEval 2.0 vs GPT-4 Omni's 57.5%"
---

# MOA — Mixture of Agents Integration

## Conceito Fundamental

> **Múltiplos LLMs em camadas, cada camada refinando a anterior.**
> O modelo agregador sintetiza criticamente todas as respostas.

## Arquitetura MoA

```
┌─────────────────────────────────────────────────────────────┐
│                    MOA ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────┤
│  Layer 1: Reference Models (paralelo)                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ Model A  │ │ Model B  │ │ Model C  │ │ Model D  │       │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘       │
│       └─────────────┼─────────────┼─────────────┘           │
│                     ▼                                        │
│  Layer 2: Refinement (paralelo)                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ Model A  │ │ Model B  │ │ Model C  │ │ Model D  │       │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘       │
│       └─────────────┼─────────────┼─────────────┘           │
│                     ▼                                        │
│  Layer N: Aggregator (síntese)                              │
│  ┌──────────────────────────────────────────────────┐       │
│  │ Aggregator: sintetiza respostas em output final   │       │
│  └──────────────────────────────────────────────────┘       │
│       │                                                      │
│       ▼                                                      │
│  RESPOSTA FINAL (streaming)                                 │
└─────────────────────────────────────────────────────────────┘
```

## Código Fonte (50 linhas)

```python
# moa.py — Mixture-of-Agents em 50 linhas
import asyncio
import os
import together
from together import AsyncTogether, Together

client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))
async_client = AsyncTogether(api_key=os.environ.get("TOGETHER_API_KEY"))

reference_models = [
    "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    "Qwen/Qwen2.5-72B-Instruct-Turbo",
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "microsoft/WizardLM-2-8x22B"
]
aggregator_model = "Qwen/Qwen2.5-72B-Instruct-Turbo"

async def run_llm(model):
    """Run a single LLM call with a reference model."""
    for sleep_time in [1, 2, 4]:  # Exponential backoff
        try:
            response = await async_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": user_prompt}],
                temperature=0.7,
                max_tokens=512,
            )
            break
        except together.error.RateLimitError:
            await asyncio.sleep(sleep_time)
    return response.choices[0].message.content

async def main():
    # Fan-out: executar todos os modelos em paralelo
    results = await asyncio.gather(*[run_llm(model) for model in reference_models])
    
    # Fan-in: agregar com modelo síntese
    finalStream = client.chat.completions.create(
        model=aggregator_model,
        messages=[
            {"role": "system", "content": aggregator_prompt + "\n" + 
             "\n".join([f"{i+1}. {r}" for i, r in enumerate(results)])},
            {"role": "user", "content": user_prompt},
        ],
        stream=True,
    )
    for chunk in finalStream:
        print(chunk.choices[0].delta.content or "", end="", flush=True)
```

## Padrões Extraídos

### 1. Fan-Out (Execução Paralela)

```python
results = await asyncio.gather(*[run_llm(model) for model in reference_models])
```

**Absorção para Gran-Mestre:**
- Atlas pode delegar tasks em paralelo
- Héstia pode validar múltiplos specs em paralelo
- Atena pode revisar múltiplos diffs em paralelo

### 2. Fan-In (Agregação Crítica)

```python
aggregator_prompt = """You have been provided with a set of responses...
Your task is to synthesize these responses into a single, high-quality response.
It is crucial to critically evaluate the information provided...
some of it may be biased or incorrect."""
```

**Absorção para Gran-Mestre:**
- Agregador não apenas combina, mas **critica e refina**
- Modelo síntese avalia cada resposta individualmente
- Output final é de qualidade superior a qualquer resposta individual

### 3. Multi-Layer Refinement

```python
for _ in range(1, layers - 1):
    results = await asyncio.gather(
        *[run_llm(model, prev_response=results) for model in reference_models]
    )
```

**Absorção para Gran-Mestre:**
- Cada camada refina a anterior
- Output da camada i alimenta camada i+1
- Qualidade progressiva

### 4. Exponential Backoff

```python
for sleep_time in [1, 2, 4]:
    try:
        response = await async_client.chat.completions.create(...)
        break
    except RateLimitError:
        await asyncio.sleep(sleep_time)
```

**Absorção para Gran-Mestre:**
- Retry com backoff exponencial
- Resiliência contra rate limits
- Nunca falhar por falta de retry

### 5. Streaming Output

```python
for chunk in finalStream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
```

**Absorção para Gran-Mestre:**
- Output em streaming para UX
- Feedback em tempo real
- Não bloquear até completar

## Resultados (Paper)

| Benchmark | MoA | GPT-4 Omni | Melhoria |
|-----------|-----|------------|----------|
| AlpacaEval 2.0 | **65.1%** | 57.5% | +7.6pp |

## Integração com Gran-Mestre

### Fase 1 (Descoberta) — MoA Pattern

```
Prometheus → Reference Models (paralelo)
├── Model A: análise técnica
├── Model B: análise de requisitos
├── Model C: análise de riscos
└── Aggregator: síntese das análises
```

### Fase 4 (Execução) — MoA Pattern

```
Atlas → Reference Models (paralelo)
├── Task 1: Implementação A
├── Task 2: Implementação B
├── Task 3: Implementação C
└── Aggregator: Atena (macro-review)
```

### Fase 5 (Revisão Macro) — MoA Pattern

```
Atena → Reference Models (paralelo)
├── Reviewer 1: coerência
├── Reviewer 2: acoplamento
├── Reviewer 3: arquitetura
└── Aggregator: síntese das revisões
```

## Configuração para Gran-Mestre

```yaml
moa:
  enabled: true
  layers: 3
  reference_models:
    - github-copilot/claude-opus-4.7
    - github-copilot/gpt-5.5
    - opencode/gemini-3.1-pro
  aggregator_model: github-copilot/claude-opus-4.7
  parallel_execution: true
  rate_limit_retry: [1, 2, 4]
  streaming: true
```

## Regras

1. **Fan-out paralelo** — Todos os modelos rodam simultaneamente
2. **Fan-in crítico** — Agregador avalia criticamente cada resposta
3. **Multi-layer** — Refinamento progressivo entre camadas
4. **Backoff exponencial** — Retry com [1, 2, 4] segundos
5. **Streaming** — Output em tempo real

## O que NÃO faz

- Não força todos os modelos a concordar
- Não ignora respostas divergentes
- Não para por falta de um modelo (fallback)
- Não bloqueia até completar (streaming)

## Limitações

- **GPU única** — Modelos locais na mesma GPU enfileiram, não paralelizam de verdade
- **Custo** — Múltiplos modelos = múltiplos custos
- **Latência** — Camadas adicionais aumentam latência
- **Consistência** — Modelos diferentes podem dar respostas inconsistentes

---

**Versão:** 2.0.0
**Data:** 2026-07-25
**Fonte:** togethercomputer/moa (29.3k stars)
**Paper:** arxiv.org/abs/2406.04692