# Função Real de Cada Papel no Grafo 0-6 (2026-09-16)

> Auditoria de otimizações/substituições — baseado em manifesto + crivo /7 + t/s medidos.

## Mapa Fase → Papel → Slot

| Fase | Papel | Slot | Modelo | Função REAL | Evidência |
|---|---|---|---|---|---|
| F0 | Córtex Talâmico | :9084 | RWKV7-0.4B | Filtra/compacta contexto 1M antes do orquestrador; roteamento semântico; ingestão logs longos O(1) | 143 t/s, KV=0, ctx 1M — insubstituível |
| F0 | Triagem L0 | :8097 | Needle-2 | Triagem confidence-gated de prompts (triage_route/run_shell) | 14MB, tool-calling puro |
| F1 | Descoberta | :9093 | SmolLM2-360M | Micro-classifier ultra-rápido p/ brainstorming em massa | 400 t/s GPU→CPU |
| F2/F3 | Proposer | :9088 | Llama-3.2-1B | Contrato/plano: spec.md, TDD bite-sized, formato estrito | 4.0/7, 240 t/s, GBNF |
| F4 | Executor F4 | :9095 | NeoHorse-4B | Motor de features: tool-calling, TDD, ctx 262k, raciocínio atômico | 5.1/7, 102 t/s GPU |
| F4 | Forja | :9091 | Needle-2 | Validação schema byte-level + escrita artefato | determinístico |
| F4 | Executor-cego | :9098 | Noema-Q4_K_S | Obediência estrita: ordens diretas, extração JSON, forja | 3.0/7, T6/T11 exatos |
| F1/F3/F5 | Refuter | :9090 | Llama-3.2-3B | Refutação A2A, extração GBNF 10/10 | 3.5/7 |
| F1/F3/F5 | Relay | :9092 | SmolLM2-1.7B | Roteamento intermediário + anti-poison | 3.5/7, único RESISTE |
| F5 | Orquestrador | :8083 | Qwen3.5-35B | Suprema corte: diff total, decisão final, síntese macro | 3.3/7, ctx 262k |
| F6 | Auto-ameliorativo | :8083+Hefesto | Qwen3.5-35B | Analisa telemetria, escreve regras no manifesto | — |
| F6 | Reflexo | :9086 | LFM-1.2B | Refutação alta velocidade (degradado thinking-burn) | N/A |
| RAG | Embedder | :9094 | Qwen3-Emb-CPU | Query tempo-real bibliotecário | 14.7k t/s |
| RAG | Embedder | :9097 | Qwen3-Emb-GPU | Backfill lote (WARM/toggle) | 91k t/s |

## Decisões de otimização (auditoria)

1. **Proposer (9088)**: MANTER Llama-1B — velocidade 2.4x vs NeoHorse, formato estrito. NeoHorse-4B fica executor F4.
2. **Embedders**: unificados — :9094 CPU canônico, :9097 GPU WARM (toggle).
3. **9093 → CPU**: micro-classifier não precisa GPU (liberou VRAM).
4. **NeoHorse-4B**: canonizado :9095 (substituiu Qwen1.5-MoE).
5. **Noema-Q4_K_S**: canonizado :9098 executor-cego (sweet spot sweep).
6. **Ornith-9B/35B, Q35-UD-IQ2XXS**: NAO_PASSOU, lixeira.

## Gargalos identificados

1. **8083 orquestrador**: 26.5 t/s CPU — gargalo assumido (R39, intocável)
2. **9086 LFM reflexo**: thinking-burn — cura R57 pendente (G4)
3. **9090 refuter**: 12.2 t/s CPU — lento mas funcional
4. **VRAM**: 92.3% — folga ~1.3GB, sem espaço p/ novos modelos GPU
