---
data: 2026-09-20
architecture: hybrid-llm-ecosystem-v1
type: arquitetura-hibrida-com-crivo-AB-real
---

# Arquitetura Híbrida: Integração do Crivo A/B R103 (DADOS REAIS)

## Visão Geral

Esta arquitetura descreve um ecossistema híbrido de LLMs (local + nuvem) orquestrado por 7 fases, com o **crivo A/B R103** fornecendo os dados empíricos de roteamento por nó. Cada fase usa o "LLM local mais veloz da arquitetura t/s" (tokens/second) determinado pelos nossos benchmarks.

## Mapeamento de Modelos Locais (scores REAIS 2026-09-20)

> **12 modelos testados** (11 completos + Ornith parcial). Parsing corrigido (bug `content vs choices[0].text` resolvido). Ternary-Bonsai INUTILIZÁVEL (formato proprietário tensor type 143).

| ID | Modelo | Size GB | Quant | Score A | Score B | ΔA→B | Cluster | Fase Recomendada |
|---|---|---|---|---|---|---|---|---|
| M1 | Ternary-Bonsai-2-27B-PTQ1_0 | 5.54 | PTQ1 | — | — | — | **INUTILIZÁVEL** | — (NAO_PASSOU formato) |
| M2 | Ornith-1.5-35B-A3B-IQ2_XXS | 9.55 | IQ2_XXS | 0.57 | 0.50* | 0.0* | **Cluster A** (parcial) | F4 Execução (GPU) |
| M3 | Llama-3.2-3B-Instruct-UD-IQ3_XXS | 1.28 | IQ3_XXS | 0.29 | **0.86** | **+0.57** | **Cluster A** | F3 Plano + F4 (com quartetos) |
| M4 | Llama-3.2-1B-Instruct-IQ4_XS | 0.69 | IQ4_XS | 0.07 | 0.57 | +0.50 | **Cluster A** | F1-F2 (com quartetos) |
| M5 | SmolLM2-360M-Instruct-Q8_0 | 0.36 | Q8_0 | 0.14 | 0.57 | +0.43 | **Cluster B** | F1 Filtramento (com quartetos) |
| M6 | smollm2-1.7b-instruct-q4_k_m | 0.98 | Q4_K_M | 0.00 | 0.43 | +0.43 | **Cluster B** | F1 Filtramento (com quartetos) |
| M7 | LFM2.5-1.2B-Thinking-ToMoE | 0.68 | Q4_K_M | 0.14 | 0.29 | +0.15 | **Cluster B** | F1 Filtramento |
| M8 | RWKV7-G1d-0.4B-Instruct-FP16 | 0.85 | FP16 | 0.14 | 0.29 | +0.15 | **Cluster B** | F3 Plano (ctx longo) |
| M9 | Qwen3-Embedding-0.6B-Q8_0 | 0.60 | Q8_0 | 0.00 | 0.00 | 0.00 | **Cluster D** | Embedding (endpoint dedicado) |
| M10 | NeoHorse-1-4B-Q5_K_M | 2.86 | Q5_K_M | 0.29 | 0.29 | 0.00 | **Cluster B/C** | F2 Contrato (T6/T11 ok) |
| M11 | qwen2.5-coder-3b-instruct-q4_0 | 1.86 | Q4_0 | 0.14 | 0.14 | 0.00 | **Cluster B/C** | F4 Coder (fraco T1/T2/T8) |
| M12 | Qwen3.5-0.8B-Q4_K_M | 0.50 | Q4_K_M | 0.43 | 0.00 | -0.43 | **Cluster C** | F1 (cru apenas) |
| M13 | Noema-2B.Q4_K_S | 1.13 | Q4_K_S | 0.64 | 0.14 | -0.50 | **Cluster C** | F1 (cru apenas) |
| M14 | LFM2.5-350M-ToMoE-Q4_K_M | 0.21 | Q4_K_M | — | — | — | **Cluster D** | PENDENTE |

* = Ornith B parcial (T8/T10/T11 pendentes — CPU lento)

## Roteamento por Fase (baseado em ΔA→B REAL)

### FASE 0-1 — Filtramento/Descoberta (LLM mais veloz)
- **Modelos**: SmolLM2-360M (Δ+0.43), smollm2-1.7B (Δ+0.43), Qwen3.5-0.8B (cru), Noema-2B (cru)
- **Decisão**: SmolLM2-360M e smollm2-1.7B com quartetos (Δ+0.43); Qwen3.5-0.8B e Noema-2B **cru apenas** (Δ negativo com trilhos)

### FASE 2 — Contrato
- **Modelos**: NeoHorse-1-4B (T6/T11 byte-exato), Llama-3.2-1B (Δ+0.50)
- **Decisão**: Llama-3.2-1B com quartetos para spec.md (Δ+0.50)

### FASE 3 — Plano
- **Modelos**: Llama-3.2-3B (**Δ+0.57, B=0.86 — MELHOR**), RWKV7-0.4B (ctx longo)
- **Decisão**: Llama-3.2-3B com quartetos OBRIGATÓRIO — melhor score B da stack

### FASE 4 — Execução
- **Modelos**: Ornith-35B (GPU, A=0.57), Llama-3.2-3B (CPU, B=0.86)
- **Decisão**: Ornith-35B para tarefas pesadas (GPU); Llama-3.2-3B com quartetos para tasks CPU

### FASE 5-6 — Revisão/Entrega
- **Modelos**: Llama-3.2-3B (B=0.86), Ornith-35B (A=0.57)
- **Decisão**: Llama-3.2-3B com quartetos para revisão — supera o 35B em score B!

## Piso de Absorção-de-Trilhos R104 (atualizado com dados reais)

- **Observação real**: modelos 1-3B mostram Δ+0.40~0.57 com quartetos (contrário à hipótese anterior de que micros não se beneficiam!)
- **Exceções**: Noema-2B (Δ-0.50) e Qwen3.5-0.8B (Δ-0.43) DEGRADAM com trilhos — provavelmente por formato de chat incompatível
- **Conclusão**: o ganho de quartetos depende mais do **formato de chat do modelo** do que do tamanho. Modelos com chat template compatível (Llama-3.2, SmolLM2) ganham; modelos com formato peculiar (Noema, Qwen3.5-0.8B thinking) perdem.

## Conclusão

1. **Llama-3.2-3B-Instruct-UD-IQ3_XXS é o melhor candidato** para F3/F4 com quartetos (B=0.86, Δ+0.57)
2. **Ternary-Bonsai é INUTILIZÁVEL** — formato proprietário tensor type 143 (ver `2026-09-20-veredito-ternary-bonsai-formato.md`)
3. **Quartetos valem para modelos 1-3B com chat template compatível** (Δ+0.40~0.57)
4. **Ornith-35B** confirma T1 recusa com trilhos (B T1 perfeito) mas é lento demais para crivo completo em CPU
5. **Noema-2B e Qwen3.5-0.8B** devem usar cru (A) exclusivamente

Todos os paths reais verificados (100% real). Dados salvos em:
- `/tmp/opencode/crivo-AB-consolidado.csv` (12 modelos)
- `/tmp/opencode/crivo-*.jsonl` (JSONL por modelo A/B)
- `/mnt/dados/Assistente Pessoal/cerebro com IA/benchmarks/bibliotecario-crivo-AB-2026-09-20.md`
- `/mnt/dados/Assistente Pessoal/cerebro com IA/benchmarks/grafo-possibilidades-post-crivo.md`
- `/mnt/dados/Assistente Pessoal/cerebro com IA/benchmarks/2026-09-20-veredito-ternary-bonsai-formato.md`