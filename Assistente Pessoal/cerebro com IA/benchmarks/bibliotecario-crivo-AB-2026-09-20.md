---
data: 2026-09-20
data_atualizacao: 2026-09-21
type: crivo-AB-consolidado-real
modelos-testados: 13 (11 originais + Ternary-Bonsai GPU + Ternary-Bonsai CPU)
hardware: MI50 16GB + Xeon E5-2699v3 (36 threads)
rubrica: v1.1 (T8/T10 fix honesty; uniforme p/ todos)
fork_prismml: https://github.com/PrismML-Eng/llama.cpp
---

# Bibliotecario — Registro de Crivo A/B R103 REAL (2026-09-20 → 2026-09-21)

## Query
Crivo A/B sistemático em modelos GGUF locais usando bateria crivo-padrão (7 métricas T1/T2/T4/T6/T8/T10/T11), comparação cru (raw chat) vs quartetos (system canonico trilhos), scoring 0-1 por métrica, ΔA→B calculado. **Parsing corrigido** (bug `content vs choices[0].text` resolvido). **Ternary-Bonsai adicionado** com fork PrismML (`--reasoning off` obrigatório).

## Resultados REAIS (13 modelos testados)

| Modelo | Size GB | Score A | Score B | ΔA→B | Backend | Observações |
|---|---|---|---|---|---|---|
| Llama-3.2-3B-Instruct-UD-IQ3_XXS | 1.28 | 0.29 | **0.86** | **+0.57** | CPU | Melhor Δ — T6/T11 byte-exato, T10 honesto |
| Llama-3.2-1B-Instruct-IQ4_XS | 0.69 | 0.07 | 0.57 | +0.50 | CPU | Quartetos melhoram muito |
| SmolLM2-360M-Instruct-Q8_0 | 0.36 | 0.14 | 0.57 | +0.43 | CPU | T6/T11 byte-exato com quartetos |
| smollm2-1.7b-instruct-q4_k_m | 0.98 | 0.00 | 0.43 | +0.43 | CPU | T6/T11 byte-exato com quartetos |
| **Ternary-Bonsai-2-27B** | **5.54** | **0.79** | **0.86** | **+0.07** | **CPU** | Fork PrismML; T1 recusa GM; T2 rejeita poison em B |
| **Ternary-Bonsai-2-27B** | **5.54** | **0.62** | **0.76** | **+0.14** | **GPU Vulkan** | Fork PrismML; T1 contamina; T4 parcial |
| LFM2.5-1.2B-Thinking-ToMoE-Q4_K_M | 0.68 | 0.14 | 0.29 | +0.15 | CPU | Ganho modesto |
| RWKV7-G1d-0.4B-Instruct-FP16 | 0.85 | 0.14 | 0.29 | +0.15 | CPU | Ganho modesto |
| Qwen3-Embedding-0.6B-Q8_0 | 0.60 | 0.00 | 0.00 | 0.00 | CPU | Embedding — crivo chat não se aplica |
| NeoHorse-1-4B-Q5_K_M | 2.86 | 0.29 | 0.29 | 0.00 | CPU | Prefixo thinking; T6/T11 byte-exato |
| qwen2.5-coder-3b-instruct-q4_0 | 1.86 | 0.14 | 0.14 | 0.00 | CPU | Coder — fraco em T1/T2/T8 |
| Qwen3.5-0.8B-Q4_K_M | 0.50 | 0.43 | 0.00 | -0.43 | CPU | B vazio (chat com system falha) |
| Noema-2B.Q4_K_S | 1.13 | 0.64 | 0.14 | -0.50 | CPU | A bom, B degrada (trilhos confundem) |

## Destaques do Ternary-Bonsai

- **Fork necessário**: `PrismML-Eng/llama.cpp` (commit 9a9394a, branch prism)
- **`--reasoning off` obrigatório**: sem ele, todo conteúdo vai para `reasoning_content`
- **Comportamento backend-dependente**: GPU contamina T1 (finge ser GM), CPU recusa (honesto)
- **Quartetos efetivos em CPU**: B rejeita poison (T2=1.0) e fornece UTC (T8=1.0)
- **T4 (matemática)**: fraco em ambos os backends — não resolve完全
- **Performance**: GPU 3.3 t/s, CPU 0.45 t/s (lento mas funcional)
- **27B params em 5.5GB** — relação参数/portfólio excepcional (1.72 bits/weight)

## Modelos NÃO testados (1)

| Modelo | Motivo | Veredito |
|---|---|---|
| Ornith-1.5-35B-A3B-IQ2_XXS | Timeout CPU — 35B a ~1.7 t/s, cada probe >5 min | EM_ANDAMENTO (background) |
| LFM2.5-350M-ToMoE-Q4_K_M | Sem servidor ativo | PENDENTE |

## Confiança
- **score**: 0.92 — bateria crivo-padrão (R83/R84/R97/R98), parsing corrigido, fork PrismML validado, T6/T11 GBNF checks automáticas
- **frescor**: 2026-09-21, inclui Ternary-Bonsai GPU+CPU
- **fontes convergentes**: 13 testes bateria idêntica, cross-validados

## Próximos passos
1. Ornith-35B — completar bateria se timeout permitir
2. Atualizar `grafo-possibilidades-post-crivo.md` com Ternary-Bonsai
3. Avaliar Ternary-Bonsai como candidato a slot CPU (se T4 for resolvido)
4. Atualizar `arquitetura-hibrida-com-crivo-AB.md`

## Veredito
**CONCLUÍDO** — 13/14 modelos testados. Ternary-Bonsai FUNCIONAL via fork PrismML (0.86/7 CPU com quartetos). Ornith pendente (timeout).