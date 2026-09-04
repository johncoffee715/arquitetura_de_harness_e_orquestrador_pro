---
tags: [gran-mestre, v8.4, hefesto, R52, R53, GAP-P5, enforcement]
date: 2026-08-26
---

# Gran-Mestre v8.4 — Refatoração Hefesto + Regras R52/R53 + GAP-P5 fechado

## Contexto
Sessão de amadurecimento do Gran-Mestre (agent primário), com pipeline hefesto
(DECOMPILAÇÃO → AUTOFAGIA → HELENIZAÇÃO → FORJA), pesquisa MIX multi-idioma (2 rodadas
paralelas: arquitetura/orquestração + enforcement de permissões), normas PCA de calibração.

## Entregas desta sessão
1. **Gran-Mestre v8.4.0** (refatoração maior):
   - `agent/gran-mestre.md` — frontmatter com **permission nativo** (edit deny global + allow
     só governança; bash ask + allowlist read-only; external_directory p/ vault/config).
     Contrato de 10 itens + segurança 2 níveis + observabilidade mínima + encerramento.
   - `skills/gran-mestre/SKILL.md` (236 linhas) — 4 pilares helenizados, modelos de orquestração
     (mesh RECUSADO com [DIVERGE DO SOURCE]), composição (5 verbos), Task Packet com run-id
     two-phase + `nao_fazer` + contrato de retorno determinístico (exit_status, erro bruto,
     evidência lockada, artefato+ref), recuperação em 2 níveis (task/pipeline), 3 camadas de
     estado (working/session/log + toxicidade), snapshot SHA do harness (anti-drift),
     política como código com gates HITL/HOTL/HOOTL, zero-trust (ABAC conceitual), lineage
     causal (derivation), MELT nativo (schema ts/dur_ms), budget zones + context-anxiety,
     gate de entrega categórico (R28/R53), trajectory eval + shadow cost, escopo por modo
     (esforço dinâmico), anti-padrões (auditoria de valor R51).
2. **R52 — Inventário Global de LLMs Locais** (regra global, pedido do usuário):
   - `harness/llm-inventory.json` (9 modelos: categoria/setor/prós-contras/bench
     CONFIRMED|INFERRED|UNKNOWN/amálgama 0–5) + `scripts/llm-inventory.py` (--all/--resolve/
     --probe/--show/--register/--validate, autocatálogo pós-registro) + `harness/INVENTARIO.md`.
   - Descoberta crítica: Qwen3.8-2B/4B/9B são distillas comunitárias (OFC: só 27B oficial);
     Ornith-1.5-9B é modelo real (ornith.ai, base Qwen3.5-9B RL: GPQA-D 86.4, SWE 70.6).
3. **R53 — Calibração Ancorada (PCA) como norma** (regra global): escala continua R34 mas
   julgamento por bandas comportamentais ancoradas; "impressão real" = banda ≥20 +
   PASSOU_CATEGORICO + zero bugs bloqueantes; anti-inflação (raciocínio antes da nota, contagem
   de evidências, UNKNOWN→piso). Notas 90+ antigas = viés de fluência (Zylos 2026, arXiv 2601.03444).
4. **GAP-P5 FECHADO** (enforcement mecânico de escrita do orquestrador):
   - Camada 1: permission nativo no frontmatter (last-match-wins; edit cobre write/edit/patch).
   - Camada 2: `plugins/guard-gap-p5.ts` — fail-closed de bash-destrutivo via regex no comando
     inteiro (rm -rf, git clean, tee p/ código, sed -i, shell -c bypass, truncate, dd), exceção
     auditável `git reset --hard` (rollback R18), auditoria JSONL em state/watcher; typecheck
     tsc 5.9 aprovado 0 erros.
   - Nota honesta: proteção contra prompt-injection de nível SO exige sandbox (fora do escopo).

## Descoberta operacional (por que o switch não via o Gran-Mestre)
Agentes são descobertos no boot da sessão; `agent/gran-mestre.md` foi criado durante sessão
ativa → invisível até restart. XDG_CONFIG_HOME confirma dir canônico. Solução: reiniciar.

## Pendências registradas para próxima sessão
- Panteão r6 (4 validadores PCA — D/A/H/F) sobre v8.4.0 — não executado nesta sessão.
- Empiria t/s por slot (llm-inventory `--bench`) e confirmação quant do qwen3.5-0.8B.
- Teste end-to-end do `--register` com GGUF real (fora da stack) e TDD do motor (R51).

## Adendo r6b2 — guard gov-aware + norma 95+
- R53 norma de impressão = NOTA ≥95 (correção do usuário; bandas PCA = calibração de qualidade).
- guard-gap-p5 v3: gov-aware (tee/cat/echo para destinos de governança permitidos; código bloqueado),
  vírgula/regressão corrigidas, tsc sem erros internos, teste funcional 7/7 + deny reais em runtime
  (jsonl: 138+ eventos; deny bash×3, deny edit×2, allow edit×6).
- Pendência p/ impressão REAL (≥95): doutrina ainda sem testes executáveis automatizados (TDD
  RED→GREEN da própria doutrina) e nem todos os mecanismos com prova de execução viva (R29).

## Feature /attach (anexo de mídia) — 2026-08-26
- commands/attach.md + scripts/attach_media.py + attach_media.schema.json (tripé R51).
- Imagem/vídeo/áudio: ffprobe metadata; vídeo→keyframes ffmpeg (max 6, /tmp/opencode/attach-frames);
  áudio→wav 16k; VISÃO via Ollama qwen3.5:0.8b (R31) — testado: imagem azul descrita corretamente e
  frames do vídeo reconhecidos (status ok). ÁUDIO: partial sem whisper instalado (pendência ASR).
- SHELL-QUEBRA: primeira execução pegou cold-start >60s → timeout 240s.
- EVIDÊNCIA EMPÍRICA: Ornith-1.5-9B :8083 NÃO aceita imagem (HTTP 500 — R31 mantida; base Qwen3.5
  sem vision embutido neste build). Usuário sugeriu ornith "enxerga" — teste refutou com evidência.
- Testes: tests/test_attach_media.py (6) — suíte total 45 verdes (26 py + 19 node).
- Uso: /attach /caminho/arquivo.mp4 (comandos/attach.md usa shell output; drag-and-drop do gerenciador
  cola o caminho no terminal; seleção via tab-completion).

## Pendências RESOLVIDAS (2026-08-26, rodada final)
1. ASR: whisper.cpp compilado (/tmp/opencode/whisper.cpp/build/bin/whisper-cli) + ggml-base.bin
   (148MB) — transcrição REAL verificada: jfk.wav perfeita; attach_media.py integrado (-nt -otxt,
   env ATTACH_WHISPER_MODEL). Áudio agora `ok`. Nota honesta: whisper alucina em ruído puro
   (sine 440Hz -> "(crickets chirping)").
2. t/s slots restantes: 8083 N/A (timeout 100s sob carga — 9 llama-servers, RAM 25/31G, swap ativo),
   9087 = 0.4 t/s, 9083 = 2.4 t/s (saturação) — 2º probe registrado honesto.
3. quant qwen3.5-0.8B: INFERIDO por tamanho (0.57GB ≈ Q4_K_M) + quant_status inferred-by-size.
4. --register e2e: LFM2.5-1.2B-Thinking-ToMoE-Q4_K_M.gguf registrado (slot none -> offline,
   unassigned, 0.73GB); motor aceita slot offline; validate OK p/ 10 modelos.
5. Testes: +test_asr (integração real jfk); probe dinâmico (10). Suíte final: 27 py + 19 node = 46 verdes.
6. Ornith "enxerga" REFUTADO com evidência (HTTP 500 imagem; R31 mantida); visão = ollama
   qwen3.5:0.8b ATIVA e verificada.
7. AVISO runtime: guard em execução usa engine pré-fix de aspas (bun cacheia módulos) — a versão
   nova (com quoted-path gov) só vale após RESTART do opencode; node --test já cobre a nova (19/19).
