---
name: porta-engine
description: "Onboarding staged de engines de inferência binários de tool-calling (ex: Needle 2/3 da Cactus) no stack local — download pinado com sha256, telemetria OFF obrigatório (privacy-first), validação de geração .cact, smoke em porta descartável, bench t/s comparativo contra baseline e promoção de manifesto só após crivo. Caso canônico: promoção Needle 2 (:8097/:9091) → Needle 3 (COMPÕE a família, nunca substituição às cegas). Use ao adicionar qualquer engine LLM binário novo ao harness antes de acoplá-lo a :8097/:9091 ou ao start-stack."
mode: skill
tags: "engine, needle, needle3, cactus, onboarding, fitragem, telemetria, ladder, cact, tool-calling, promocao, crivo"
origin: helenizado: cactus-compute/needle @ 3.0.1 (2026-09-21) — proteína extraída da avaliação Needle 3 vs Needle 2 local
metadata:
  category: methodology
  version: 1.0.0
  date: 2026-09-21
  author: Hefesto (dispatcher v2)
  motor: nenhum (determinístico; bench via HTTP stdlib)
---

# PORTA-ENGINE — O Portão dos Engines

Toda engine LLM binária de tool-calling (API C própria, binário standalone, protocolo HTTP
próprio) entra no harness por esta porta. Engines ≠ modelos: `porta-modelo` cobre pesos de
checkpoint/LoRA/VAE em ComfyUI; **porta-engine** cobre binários de inferência com API de
tool-calling (caso canônico: família Needle da Cactus Compute — Needle 2 em produção
:8097/:9091, Needle 3 avaliado 2026-09-21).

## Doutrina (invariantes da família Needle, extraídos por autofagia)

1. **Refusal-not-guess**: entrada off-topic → `function_calls` vazia (lista vazia, nunca chute).
2. **Byte-level grammar**: gramática compilada do schema constrange cada token; payload 100%
   conforme o schema declarado.
3. **Top-5 tools**: catálogo >5 tools → retrieval head injeta só as 5 mais relevantes por
   turno; embeddings persistidos via `tool_index_path`.
4. **Gerações .cact**: tag de 4 bytes little-endian no arquivo — `0x05E12A83` = geração 2,
   `0x05E12A84` = geração 3. Engine por geração (libneedle2/libneedle3); backward compat
   embutida no package (`generation=2`).
5. **Ladder de rungs**: cada profundidade 2-20 layers é deployável; rung por papel —
   F0 triagem = 2-4L (ultra-rápido), F4 forja = 8L (equilíbrio). 20L em CPU de produção é
   desperdício.
6. **Telemetria é superfície de ataque**: engines 3.x telemetram por default (anon_id
   persistido + endpoint de terceiro). Opt-out é LEI: `NEEDLE_TELEMETRY=0` + `DO_NOT_TRACK=1`.
7. **Engine não descarrega pesos**: uma engine carregada num processo não pode trocar pesos —
   isolamento por porta/processo é obrigatório (o `--serve` por porta já nos isola).

## Pipeline de adoção (6 estágios, gates categóricos)

| Estágio | Gate | Comando de evidência |
|---|---|---|
| S0 FITRAGEM | engine nova NUNCA vai ao path principal direto (guardrail-llm-fitragem); fica em `fitragem/engines/<nome>-<versao>/` | `ls fitragem/engines/` |
| S1 PIN+TELEMETRIA | versão + sha256 pinados; env de opt-out exportado; strings do binário auditadas | `mecanica.py probe-strings <bin>` + `check-env` |
| S2 SMOKE | `--serve` em porta DESCARTÁVEL (nunca 9091/8097); tools JSON de produção carregam; refusal-not-guess OK | `mecanica.py smoke-check <port>` |
| S3 CRIVO t/s | bench decode vs baseline registrado (Needle 2: 146.6 t/s @:9091, 160.1 t/s @:8097); gate: ≥1.5× baseline OU mantém N2 | `mecanica.py bench <port> --baseline-tts 146.6` |
| S4 PARIDADE SCHEMA | tools de produção (validate_schema/write_artifact) N rodadas, 100% conformidade; confidence calibrada presente | `mecanica.py bench <port> --rounds 10` |
| S5 PROMOÇÃO | manifest_llm.json atualizado com fallback da geração anterior; start-stack idempotente preservado; nota no vault `decisoes/` | `python -m json.tool manifest_llm.json` |

Falhou qualquer gate → engine PERMANECE em fitragem; produção intocada (reversível).

## Regras de ferro

- PROIBIDO promover engine sem bench local no NOSSO hardware (benchmarks self-reported do
  vendor são `PROBABLE`, nunca `CONFIRMED` — crivo próprio R83/R97).
- PROIBIDO substituir Needle 2 em produção sem veredito registrado no vault (R26).
- PROIBIDO smoke na porta de produção (:9091/:8097) — porta descartável ≥9100.
- PROIBIDO auto-download HF no caminho crítico — `needle fetch` prévio + `HF_HUB_OFFLINE=1`
  para air-gapped.
- Fine-tune local LoRA derruba a confidence head (`confidence=None`) — se o gate de confiança
  (R65) depender dela, ou fine-tune via plataforma (envia dados a terceiro — avaliar) ou
  mantém o modelo base.

## Baseline local registrado (2026-09-15, needle-sync)

- :8097 graph-tools (triagem L0) — 160.1 t/s · :9091 forja-tools — 146.6 t/s
- Engine needle2 v2.0.4, binário 14.8 MB, sem strings de telemetria detectáveis
- Janela 256 tokens (sliding) — o needle-pytest-filter existe POR CAUSA dela; Needle 3
  (max_seq_len 4096) elimina a obrigatoriedade do filtro, mas ele continua como economia.

## Integração (API compatível entre gerações)

API C idêntica: `needle_init(system, tools_json, tool_index_path)` · `needle_complete(input,
max_new_tokens, out, capacity)` · `needle_reset()` · `needle_load(cact, n)` — geração 3
acrescenta `needle_embed(text, out, dim)`. HTTP: `POST /complete {"input":"..."}` +
`POST /reset`. Tools JSON de produção (graph-tools.json/forja-tools.json) carregam sem
mudança em ambas as gerações.
