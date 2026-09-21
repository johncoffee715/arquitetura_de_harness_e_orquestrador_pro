# INVENTÁRIO GLOBAL DE LLMs LOCAIS (R52)

Fonte de verdade da escolha LLM×recurso do orquestrador. Instituído em 2026-08-26
(regra global guardrail, pedido do usuário).

## O que é

`config/opencode/harness/llm-inventory.json` registra TODO LLM da stack local com:

| Campo | O que é |
|---|---|
| `category` | papel no grafo: orquestrador · descoberta · executor · judge · reflexo · prosa · tool-leve · refutacao · contrato-plano |
| `sector` | GPU-MI50-Vulkan · CPU-threads · CPU-threads RAM-gated |
| `capabilities`/`weaknesses` | prós e contras EXPLÍCITOS |
| `benchmarks` | públicos via model cards/HF/leaderboards com **status CONFIRMED / INFERRED / UNKNOWN** — nunca valor inventado |
| `empirical` | evidência local (t/s, t/s-per-KV-GB, uso real por fase) |
| `affinity` | amálgama 0–5 por tipo de feature (R52) |

## Uso obrigatório pelo orquestrador

Antes de escolher LLM local para QUALQUER task/feature:

```bash
python3 config/opencode/scripts/llm-inventory.py --resolve skill-prosa
python3 config/opencode/scripts/llm-inventory.py --resolve subagent-executor
python3 config/opencode/scripts/llm-inventory.py --all      # visa geral
python3 config/opencode/scripts/llm-inventory.py --probe    # saude dos slots
```

O resultado cruza com roteamento R13/R23/R47 e dissecação R46. Amálgama baseado
em UNKNOWN → declarar e decidir por empiria local (nunca forçar rota).

## Alimentação automática pós-registro (R52 + R27)

1. Registrar LLM novo: `llm-inventory.py --register MODELO.gguf --slot PORTA --category PAPEL`
2. Preencher lacunas de benchmark: MIX R50 (≥2 rodadas, todas as línguas) ou benchmark empírico local
3. Atualizar afinidades após medição (t/s, uso por fase)

## Regras de integridade

- Bench CONFIRMED exige fonte citável; sem fonte → INFERRED ou UNKNOWN.
- Divergência inventário×realidade (tipo/quant ≠ header GGUF) → corrigir inventário com evidência.
- Health de slot é parte do resolve (--probe antes de confiar).
