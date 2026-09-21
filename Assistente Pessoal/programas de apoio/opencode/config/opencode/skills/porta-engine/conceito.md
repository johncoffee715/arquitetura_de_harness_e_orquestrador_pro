# CONCEITO — porta-engine (ontologia)

## Engine ≠ Modelo

- **Modelo** (porta-modelo): pesos de checkpoint/LoRA/VAE renderizados por um runtime
  existente (ComfyUI). O que entra é um arquivo de pesos.
- **Engine** (porta-engine): binário de inferência standalone com API C própria
  (`needle_init`/`needle_complete`/`needle_load`), protocolo HTTP próprio (`POST /complete`),
  tokenizer e runtime embutidos. O que entra é um EXECUTÁVEL — superfície de ataque maior:
  telemetria, auto-download, chamadas de rede embutidas.

## Formato .cact (pesos da família Needle)

- Container: header `<48If` + codebook + records `<BBHIIIIQQII`; pesos quantizados
  (Cactus Quants, ~2.125 bits/weight na geração 3).
- **Tag de geração** (4 primeiros bytes, little-endian): `0x05E12A83` = gen 2 ·
  `0x05E12A84` = gen 3. A tag seleciona a engine compatível — gen 2 NÃO lê .cact de gen 3.
- Engines versionadas por geração: needle2 v2.0.4 (repo HF Cactus-Compute/needle2) ·
  needle3 v3.0.1 (repo Cactus-Compute/needle3). Package Python `cactus-needle` 3.0.1 carrega
  AMBAS (`generation=2` para a legada) — a própria Cactus trata as gerações como FAMÍLIA.

## Ladder de rungs (geração 3)

- Arquitetura Laddered Simple Attention Network: 29-121M params, depth 2-20 deployável.
- Config de referência (architecture.py): d_model 768 · 12 heads / 2 KV heads (GQA 6:1) ·
  qk_head_dim 48 / v_head_dim 64 · max_seq_len 4096 · sliding_window 1024 · camadas globais
  em (4, 9, 14, 19) · engram n-gram (18432 slots, orders 2-3) · mhc_lanes 4 · qkv_conv_taps 3.
- **Rung por papel** (invariante de adoção): F0 triagem = 2-4L (mínima latência) ·
  F4 forja = 8L (equilíbrio precisão/custo) · 20L reservado a avaliação, nunca a produção CPU.

## Invariantes comportamentais da família

1. **Refusal-not-guess**: sem cobertura de tool → `function_calls: []` (contrato, não erro).
2. **Grammar byte-level**: decode sempre parseable contra o schema declarado.
3. **Top-5 + tool_index_path**: retrieval head injeta ≤5 tools por turno; embeddings persistidos.
4. **Envelope JSON**: `{type, success, error, error_code, function_calls, reasoning,
   confidence, prefill_tps, decode_tps, suppressed_calls, validation}` (gen 3 completa a
   gen 2 com `confidence` calibrada, `suppressed_calls` e `validation.ungrounded`).

## Telemetria (auditoria 2026-09-21)

- Package `cactus-needle` e engines 3.x: telemetry ON por default → endpoint Supabase de
  terceiro (`vlqqczxwyaodtcdmdmlw.supabase.co`), envia event/anon_id (uuid persistido em
  `~/.cactus_needle/telemetry_id`)/version/engine/os/arch/python/props.
- Opt-out: `NEEDLE_TELEMETRY=0` OU `DO_NOT_TRACK=1` (env `CI` exclui automaticamente).
- Binário needle2 v2.0.4 local (25-ago-2026): SEM strings de telemetria detectáveis
  (`strings | grep -i "telemetry\|supabase\|do_not_track"` → vazio). Classificação PROBABLE
  limpo; engines novas = auditar sempre em S1.

## Riscos operacionais mapeados (lições do original)

- Engine não descarrega pesos → isolamento por porta/processo; NUNCA reusar processo entre
  pesos base e tuned.
- Fine-tune LoRA local (4-bit, JAX) derruba confidence head → `confidence=None`; platform
  fine-tune (2-bit) mantém a head mas envia dados de treino a terceiro.
- Primeiro uso com auto-download HF → rede no caminho crítico; usar `needle fetch` prévio +
  `HF_HUB_OFFLINE=1` + `NEEDLE3_LIB_PATH`.
- Benchmarks do vendor são self-reported (DroidCall/Mobile Actions) → crivo local obrigatório
  antes de qualquer promoção (R83/R97).

## Relação com regras do vault

- R8 catálogo-primeiro · R26 memória Obsidian · R28 trânsito categórico · R65 roteamento
  híbrido · R83/R97 crivo · guardrail-llm-fitragem (LLM novo só sai da fitragem ao canonizar).
