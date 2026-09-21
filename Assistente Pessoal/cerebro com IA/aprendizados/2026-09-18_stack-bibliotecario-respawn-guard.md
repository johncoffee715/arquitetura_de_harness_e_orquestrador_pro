---
tags: [aprendizado, stack, watchdog, respawn, vram, pkill, reasoning]
data: 2026-09-18
sessao: stack-bibliotecario-respawn-guard
---

# Pérolas empíricas — stack bibliotecário + guarda-VRAM (2026-09-18)

## P1. `q4_0` V-cache EXIGE `--flash-attn on` neste build
- Lançar `:9086` (LFM2.5-1.2B) com `--flash-attn off` + `--cache-type-v q4_0` = fatal:
  `llama_init_from_model: V cache quantization requires flash_attn`.
- Manifesto dizia "flash false" p/ 9086/9092 — **REFUTADO por evidência**.
- Regra: todo slot com KV `q4_0` sobe com `--flash-attn on` (CPU ou GPU).

## P2. LFM thinking-only: `--reasoning off --reasoning-budget 0`
- `--chat-template-kwargs '{"enable_thinking": false}'` está **DEPRECATED** no build
  (log: "Use --reasoning on / --reasoning off instead") — e mesmo `--reasoning off`
  sozinho NÃO bastou (reasoning 230 chars, content vazio, finish=length).
- Combinação que funciona p/ content direto (relay/GBNF): `--reasoning off --reasoning-budget 0`.
- Vale p/ qualquer modelo thinking-only da família (mesmo sintoma do NeoHorse).

## P3. `pkill -f "port XXXX"` dentro de `bash -c` mata o próprio shell
- O padrão aparece na cmdline do próprio `bash -c` → self-match → shell morre, timeout sem saída.
- Truque canônico: colchetes no padrão — `pkill -f "port 908[6]"` (regex casa `9086` no alvo, mas não o literal `908[6]` do próprio comando).

## P4. Shell tool: comandos longos com loop estouram timeout e a saída bufferizada se perde
- Padrão seguro: lançar (comando curto) → checar em comandos curtos separados (`sleep 12` + 1 curl por chamada).

## P5. Política CPU-only p/ embeddings (ordem usuário 2026-09-18)
- `:9097` GPU descontinuado (processo morto, fora do respawn/watchdog, manifesto = DESCONTINUADO). `:9094` CPU é o único embedder.
- `embeddings.py` continua `graceful`: GPU_BATCH cai p/ CPU 1-a-1 automaticamente.

## P6. Guarda-VRAM no `respawn.sh` (ComfyUI da outra sessão)
- `vram_free_mb()` via `rocm-smi` (`awk '/Total Memory/{print $NF}'` — `$7` quebra; usar `$NF`).
- Slots GPU (ngl!=0) só sobem com livre >= 1500MB; senão ADIADO com log + retry próximo ciclo. Slots CPU voltam sempre.
- `wd.sh`/`respawn.sh` jamais matam processo (zero kills); `slots.json` agora vigia 8083/9084/9086/9088/9090/9092/9093/9094.

## P7. Blanket `pkill -f llama-server` eliminado do harness ativo
- `validate-models.sh` (2×) e `start-llama.sh` (1×) → escopo por porta. `start-llama.sh` ainda tinha binário inexistente (`llama.cpp-master`) → apontado ao canônico.

## P8 (adendo). `sync_check 1` → `status` no manifesto NÃO basta
- O gari acusou `sync_check: 1` (8 divergências): o gerador `sync-llm-stack.py` ignora o campo `status` — entrada presente = slot esperado nos 9 alvos.
- Descontinuar de verdade = REMOVER a entrada do manifesto fonte (+`--apply` regenera; backups automáticos em `/tmp/opencode/sync-llm-stack-backups/`).
- `--check` final: `✔ tudo sincronizado (9 alvos + fonte)`. `.gguf` mantido no disco; backup fonte `manifesto_llm.json.bak-pre9097rm-20260918`.
