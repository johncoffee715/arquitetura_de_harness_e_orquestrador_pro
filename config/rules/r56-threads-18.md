---
numero: R56
tema: Threads fixos -t 18 (núcleos físicos) — regra de ouro da stack
categoria: harness
setor: backend
escopo: global
vigencia: 2026-08-19 (pedido do usuário)
---

# R56 — Threads fixos -t 18 (núcleos físicos) para TODA a stack

## Regra
Todo backend llama-server da stack DEVE iniciar com `-t 18` (núcleos físicos da
X99 E5-2699v3, 18c/36t). Proibido `-t 36` (hyperthreads) e proibido `-t 12`/`-t -1`
nos modelos GPU sem justificativa documentada.

## Evidência empírica (2026-08-19, ornith-1.0-9B, MI50 Vulkan)
| threads | decode t/s | VRAM load | prefill t/s (prompt 3.5k) |
| :--- | :--- | :--- | :--- |
| 18 (físicos) | **69,5** | 8,5 GB | 662,9 |
| 36 (hyperthreads) | 63,9 (-8%) | 10,0 GB | 643,0 |

- Hyperthreading NÃO ajuda: GPU (Vulkan) faz o trabalho pesado; threads de CPU só
  alimentam dequantização/submissão → `-t 36` gera contenção + mais buffers Vulkan.
- `-t 12` já havia degradado 52→2,4 t/s (histórico, R46) — confirmado inferior.

## Aplicação (5 pontos de verdade, R27)
1. `harness/start-all-models.sh` — case de threads: TODOS os modelos `-t 18`.
2. `harness/ctx-catalog.json` — campo threads=18.
3. `llama_budget.py` — default threads=18.
4. `bench.py`/`throughput.py` (skill llm-benchmark) — default já 18 ✓.
5. `AGENTS.md` §13 — essência irredutível abaixo.

## Nota CPU (modelos concorrentes)
Modelos CPU paralelos com `-t 18` cada → oversubscription (5×18=90 > 36 lógicos).
Regra vale para TODA a stack por decisão do usuário; se houver thrashing em modelos
CPU concorrentes, escalar ao usuário (nunca mudar sozinho).
