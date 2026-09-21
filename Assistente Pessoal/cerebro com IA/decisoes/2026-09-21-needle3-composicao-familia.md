---
setor: decisoes
tipo: veredito-categorico
data: 2026-09-21
run: hefesto-needle3-absorcao (pipeline completo R74)
tags: "needle3, cactus, needle2, l0, engine, porta-engine, composicao"
---

# 2026-09-21 — Needle 3 (cactus-compute): COMPÕE a família L0

**VEREDITO CATEGÓRICO: COMPÕE** (não substitui às cegas; sucessão compatível com caminho de
promoção staged). O Needle 3 é a 3ª geração da MESMA linhagem L0 Syntactic Enforcer — a própria
Cactus mantém a geração 2 embutida no package `cactus-needle` 3.0.1 (`generation=2`), engines
versionadas por geração (needle2 v2.0.4 / needle3 v3.0.1), mesmo formato .cact (tags
`0x05E12A83`=gen2 / `0x05E12A84`=gen3), mesma API C (`needle_init/complete/reset/load`), mesmo
protocolo `POST /complete`, mesmos invariantes (refusal-not-guess, grammar byte-level, top-5
tools com tool_index_path). Tools JSON de produção (:8097/:9091) carregam sem mudança.

## Tabela comparativa (feature-a-feature)

| Feature | Needle 2 (produção local) | Needle 3 (avaliado) |
|---|---|---|
| Janela | 256 tokens (sliding) | max_seq_len 4096 (sliding 1024 + 4 camadas globais) |
| Params | 45M | 29-121M ladder depth 2-20 (rung por papel) |
| Quantização | .cact gen2 | Cactus Quants 2.125 bits/weight |
| RAM | 28 MB | 8-29 MB por rung (35 MB full 20L) |
| Throughput | 146.6 t/s (:9091) · 160.1 t/s (:8097) — provado local | decode 850 t/s · prefill 4300 t/s (vendor, RPi5 4000 prefill) — NÃO provado no nosso hardware |
| Confidence | ausente (refusal binário) | head calibrada + suppressed_calls <0.1 + validation.ungrounded |
| Embeddings | não (SQLite externo p/ retrieval) | nativo `needle_embed` 128-d |
| Extração | via tools | `needle.extract()` first-class + Pydantic + strict grounding |
| Repair args | não | determinístico (datas/números/enums/polaridade) |
| Fine-tune | não | LoRA local 4-bit JAX (derruba confidence head) / platform 2-bit (mantém, envia dados a terceiro) |
| Telemetria | binário local 2.0.4 limpo (sha256 d5e86d62, zero markers) | ON por default (Supabase + anon_id persistido) — exige NEEDLE_TELEMETRY=0 |

## Decisão operacional

- **Produção NÃO muda hoje**: Needle 2 :8097/:9091 segue como L0 (integração viva, provada,
  start-stack idempotente, manifesto sincronizado — nota 2026-09-15-needle-sync).
- **Needle 3 entra como candidato em fitragem** (guardrail-llm-fitragem): download pinado,
  telemetria OFF, promoção só via skill **porta-engine** (S0-S5: fitragem → pin/telemetria →
  smoke porta descartável → crivo t/s ≥1.5× baseline → paridade schema → promoção manifesto).
- Ganhos que motivam a promoção futura: janela 16× (torna needle-pytest-filter opcional, não
  obrigatório), confidence calibrada (fortalece gate R65/R28), embeddings nativos (dispensa
  SQLite surrogate p/ tool retrieval), decode ~5× mais rápido (vendor — crivar local).

## Evidências

- Repo: github.com/cactus-compute/needle (main, 315 commits, 11.9k stars, Apache-2.0, SEM
  releases GitHub — versioning via pip `cactus-needle` 3.0.1 + HF Cactus-Compute/needle3).
- Código: `__init__.py` (`__version__="3.0.1"`, `_CACT_GENERATIONS`, `generation or 3`) ·
  `architecture.py` (TransformerConfig: max_seq_len 4096, sliding 1024, GQA 12/2, engram 18432
  slots, mhc_lanes 4) · `fetch.py` (ENGINE_VERSIONS {2:"2.0.4", 3:"3.0.1"}) · `_telemetry.py`
  (endpoint Supabase, opt-out env) · `pyproject.toml` (descrição "14MB" desatualizada —
  evidência de repo reaproveitado da gen 2).
- Vídeo (R107, yt-dlp auto-subs): youtube.com/watch?v=1TN992VH-00 — demo CPU extração+tool
  calling, 96% confidence, RPi5 28MB/4000 t/s prefill; canal entusiasta (benchmarks não
  independentes → PROBABLE).
- Local: `programas de apoio/opencode/tools/needle2/` (binário 14.8MB + libneedle.a +
  needle.h sem needle_embed) · manifesto `needle2` :8097/:9091 POST /complete.
- Skill nova: `~/.config/opencode/skills/porta-engine/` (SKILL.md, conceito.md, gabarito.json,
  mecanica.md, mecanica.py, schema.gbnf) — GAP real: catálogo não cobria onboarding de engines
  binárias (porta-modelo = pesos ComfyUI).

## Riscos registrados

Telemetria 3.x (opt-out é lei) · engine não descarrega pesos (isolar por porta/processo) ·
LoRA local derruba confidence head · auto-download HF no 1º uso (fetch prévio + HF_HUB_OFFLINE)
· benchmarks self-reported (crivo local R83/R97 antes de promover) · contexto efetivo de
raciocínio ainda limitado (sliding 1024) — Needle 3 continua L0/L0.5, nunca F1/F2.
