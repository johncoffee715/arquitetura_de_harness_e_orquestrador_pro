---
name: scheduler-admission
description: "Admissão FIFO com backfill protegido (epoch/donor proofs), cost-model de transferência/prefill e resolução de sampling em camadas — padrões absorvidos do NInfer para agendar trabalho sob capacidade fixa. Use ao dimensionar filas, decidir backfill sem starvation, precificar restore-vs-recompute ou resolver defaults de sampling."
mode: skill
tags: "scheduler, fifo, backfill, admission, anti-starvation, cost-model, kv-cache, sampling-defaults, capacidade, serving"
origin: absorvido:https://github.com/Neroued/ninfer
metadata:
  category: contrato-plano
  version: 1.0.0
  date: 2026-09-17
  author: Hefesto (dispatcher)
  source_sha: f76e19c0fbd026c86f46005acf2c80c54084bade
  license: Apache-2.0 (upstream); padrões reescritos, sem código literal
---

# SCHEDULER-ADMISSION — Fila com Backfill Protegido

Padrões de **scheduling sob capacidade fixa** absorvidos do NInfer
(motor C++/CUDA single-GPU; aqui só a lógica, em Python stdlib puro —
nenhuma dependência do framework original, nenhum código literal copiado).

## 1. Quando usar

- Dimensionar fila com concorrência fixa de startup (`max_concurrency 1..8`).
- Decidir **backfill**: admitir requisição pequena atrás do head bloqueado
  sem causar starvation do head.
- Precificar **restore-vs-recompute** de prefixos/checkpoints.
- Resolver parâmetros de sampling em camadas (preset → override → request).

## 2. Regras (contrato)

1. **Scheduler escolhe, recurso projeta.** Quem ordena a fila NUNCA lê
   placement físico; quem executa sela um plano contra a revisão atual.
2. **Head primeiro.** Se o head couber (tokens + slot livre), ele entra.
   Só se bloqueado, escanear backfill.
3. **Proteção por prova.** Congelar doadores (epoch + head id + revisão de
   recursos). Revisão divergente ⇒ **negar**. Doador morto ⇒ remover no
   `rebind`. Borrower persistente da **epoch corrente nunca vira doador**
   (impede a fronteira do head de andar para trás em backfill repetido).
4. **Backfill autorizado sse** cabe no livre AGORA **e** o head continua
   executável após doadores liberarem.
5. **Ativo é intocável.** Capacidade reservada de request ativo nunca é
   emprestada à política de cache inativo.
6. **Custo = `max(batch + ops·op, bytes·ns/byte)`** (transferência) e
   `chunk + tokens·t + pares·a` (prefill). Defaults genéricos sempre
   existem; presets de hardware fazem override; calibração atualiza **um**
   componente por vez, preservando os demais.
7. **Sampling em camadas:** preset do modelo/modo fornece todo campo omitido;
   overrides de processo ficam no meio; campos do request vencem; seed omitido
   ⇒ seed fresco por request; `--greedy` força `temperature 0`.
8. **Capacidade `auto` mantém headroom** (ex.: 1 GiB / N tokens) fora do pool
   utilizável, pelo tempo de vida do processo. Sem preempção de ativos,
   sem QoS/prioridade — FIFO limitado é o produto.

## 3. Origem → conceito (rastreabilidade)

| Arquivo / seção upstream | Conceito absorvido |
|---|---|
| `src/runtime/engine/admission_policy.h:24-54` | `AdmissionProtection` (epoch/head/revisão/doadores), `rebind`, `persistent_backfill_is_authorized` |
| `src/runtime/engine/context_cache/context_cost.h:58-136` | `transfer_ns`/`prefill_ns`, presets por `hardware_class`, upsert atômico de calibração |
| `src/runtime/engine/context_cache/resource_manager.h:59-61` | separação Scheduler × ResourceManager × Program; owner-edge vs snapshot |
| `src/runtime/contract/sampling.h:7-11`, `serve_options.h` (overrides + `greedy`) | preset cobre omitidos; camadas; seed fresco; greedy = argmax |
| `serve_options.h` (capacidades) + `README.md:242-256` | contrato startup-fixed, FIFO limitado, tool calls parseadas-não-executadas |
| `docs/maintainer/logging.md:§1-3` | 4 classes de saída (operacional × resultado × medição × emergência); sem mutar logger global |
| `tools/bench/run_serve_ttft.py` + `tools/bench/ttft/` | grafo auditado de TTFT (hot reuse, resume, evicção, prefixos compartilhados) — metodologia citada, não forjada (crivo-padrao cobre bench) |

## 4. Uso

```bash
python3 tooling/smoke_admission.py   # 13 checks, determinístico
```

```python
from tooling.admission import *
cap = CapacityContract(kv_capacity=10000, max_concurrency=3, headroom_tokens=1000)
admitidos = schedule_fifo_with_backfill(cap, ativos, pendentes, revision=5, epoch=7)
amostra = resolve_sampling(defaults, "thinking", overrides, greedy=False, fresh_seed=42)
ns = resolve_cost_model(presets).transfer_ns(bytes_n, ops_n)
```

## 5. Não-objetivos (rejeitados com motivo)

- Port do motor CUDA/inferência (sem GPU no harness; `nvidia-smi` ausente).
- Preempção, QoS/prioridade, multi-GPU, offload (fora do produto; AGENTS.md upstream).
- Contrato de tool-call (já coberto pela doutrina constrained-decoding do harness).
- Bench TTFT completo (crivo-padrao cobre metodologia de benchmark).
- Pre-router MoE/offload SSD (pesquisa Edge Zero, não feature operacional).
