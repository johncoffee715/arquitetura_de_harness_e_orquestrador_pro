---
data: 2026-09-15
tipo: checkpoint-sessao-autonoma
---

# Checkpoint — Sessão autônoma (modo ON desde 19:00, retorno user ~06:30)

## Resolvidos 2026-09-18 (turno pós-reinício)
- **ctx session 130k→262k**: `local-orchestrator/orchestrator` limit.context 65536 → **262144** (jsonc linha 33) — casa com o Ornith GM (ctx nativo 262k)
- **opencode update .31**: instalado **v1.18.31** (era 1.18.29, binário manual de 11/09 não auto-atualizava). Substituído no path R102.
- **CIVITAI_API_KEY**: configurada (bashrc + fish) e **validada** — MCP `civitai-orchestration` respondeu initialize (serverInfo "Civitai Orchestration MCP Server"). Pendência MCP anterior RESOLVIDA.

## 🏆 COROAÇÃO CONCLUÍDA (2026-09-17 ~22:00)
- **Novo GM**: Ornith-1.5-35B-A3B-IQ2_XXS no :8083 (manifesto atualizado + sync-llm-stack --apply)
- **Config**: CPU-knobs (b4096/ub1024, fa on, prio 2, mlock, t36) — dec **81.0** / pre **123.8** t/s
- **vs incumbent**: 26.5 → 81.0 = **3x mais rápido**; crivo B=6.0 (Δ0.2)
- Qwen3.5-35B-IQ3_XXS = **EXCLUÍDO TOTALMENTE** (sem fallback — limitação de hardware, user 17/09)
- **gemma-4-26B = DESCARTADO** (A=4.6/B=5.2 muito abaixo do padrão B=6.0 — falhas por dados inadmissíveis)
- MTP/DFlash: bloqueados por build (ggml_abort/mismatch) — não decisivos (user)
- **Régua de candidatos**: B ≥ ~5.7-6.0 para ser considerado; otimizações entregues potencializam cada LLM novo/canonizado

## Matriz final Ornith-IQ2_XXS (2026-09-17, dec/pre t/s medidos)

| Config | dec | pre |
|---|---|---|
| full-GPU ngl 99 | **79.4** 🏆 | 46.8 |
| GM-parity ngl 36 | 23.4 | 25.3 |
| híbrido experts-VRAM + draft 0.8B | 12.0 | 36.5 |
| cpu-moe | 11.9 | 8.0 |

→ Caminho de coroa: full-GPU ngl99. Draft heterogêneo não compensa.
→ Requisito físico: `--flash-attn on` quando KV=q4 (erro encontrado); v1 laners sem -ngl após VuIkan leak.

## PENDENTE (tese do user, 2026-09-17)
Acelerar Ornith em CPU com os MESMOS knobs do Qwen-35B: b4096/ub1024, fa on, prio 2, mlock, threads nativos — nunca aplicados ao Ornith em CPU puro (runner usava -t 18). Testar também MTP/DFlash da MESMA família (não o Abliterated).

## ✅ RESOLVIDO — CPU-KNOBS (2026-09-17 ~16:15)
Ornith-IQ2_XXS com knobs do Qwen-35B (b4096/ub1024, fa on, prio 2, mlock, t36):
- dec **44.5 t/s** (300 tok) · pre **103.4 t/s** — vs "CPU puro" 3.4 (era artefato do runner -t18 sem knobs)
- **13x de ganho em CPU** — tese do user CONFIRMADA
- full-GPU segue campeão (79.4 dec) mas CPU-knobs é o melhor sem VRAM dedicada

## MTP/DFlash — BLOQUEADO por incompatibilidade de build (2026-09-17 ~21:30)
- DFlash2 (Cobra91310 + jzinno): mismatch de tensores (96×69) — draft é para o base ornith-ai, não o IQ2_XXS bartowski
- MTP Q2_K (mradermacher): `ggml_abort` no load mesmo sem spec-type — formato de head MTP mais novo que nosso llama.cpp
- **Veredito**: MTP/DFlash são dead-end com o build atual. CPU-knobs (44.5 t/s) já supera o incumbent (26.5) em 1.7x. Fechado o crivo de aceleração.
- Pendência futura: atualizar llama.cpp p/ suportar MTP (risco: quebrar stack) OU usar main na família base p/ DFlash2.

## Feito (com evidência)
1. **R102** criada + índices sincronizados (vault + ~/.config/opencode/AGENTS.md).
2. **R103** criada (crivo A/B cru×quartetos vs rival) + índice AGENTS.md.
3. **Migração R102 efetivada**: opencode/ → programas de apoio/opencode/ (rename, refs sed 58+83 arq, guard-engine paths atualizados, testes 29/29 PASS, health 10/10 + 3 needles + sync-llm-stack ✔ sincronizado).
4. **Órfãos da raiz** canonizados via pkexec (opencode-standalone 179MB + tarball 59MB).
5. **fish**: fish_user_paths corrigido (universal); config.fish L111 PENDENTE (barreira de sessão — plugin velho em memória; próxima sessão edita livre via política 2026-09-15; comando pronto na seção abaixo).
6. **Links .local/bin**: code, pipx, node/npm/npx reparados; ocr-vision/opencli órfãos pré-migração (alvos inexistem).
7. **Crash-loops saneados** (disable --now, reversível): config-watcher, omniroute, ocr-auto-sync, llm-usage@8083/8090, iq2-8090. Benignos documentados: opencode-vacuum (falha por design com opencode ativo), ghidra-mcp (on-demand, ExecStart staled p/ /mnt/dados/opencode/tools/...).

## Em curso
- (vazio) — ver `benchmarks/2026-09-15-crivo-AB-consolidado-27b.md`: crivo A/B completo p/ stack toda + 27B. 27B = filtragem até slot GPU.

## Fila p/ retorno do user
- [ ] Fix L111 `~/.config/fish/config.fish`: `sed -i 's|/mnt/dados/Assistente Pessoal/opencode|/mnt/dados/Assistente Pessoal/programas de apoio/opencode|' ~/.config/fish/config.fish`
- [ ] Fusão harness/ + ecossistema/: recon feito (ZERO overlap de nomes; harness=ops, ecossistema=cognição) → fusão = anexação sem conflitos. Decidir destino final (sugerido: ecossistema/ vira subávore de harness/ ou de cerebro com IA — aguardar user.
- [ ] 9095 NeoHorse ctx: rodando 262k (KV caro); plano canônico era 8-32k — decidir.
- [ ] Stack completa restaurada após os testes (8083 GM já OK em `srv-gm-full`; demais slots **gerenciados pela session paralela** "confyui"/"refinando" — não interfiro)

## Lições
- `pkill -f` SEM colchete `[l]` mata o próprio shell (self-match) — 2 timeouts reais.
- systemd-run transient SEM --remain-after-exit cria SIGTERM nos filhos quando a unit termina (KillMode default) — cobrir SEMPRE com --remain-after-exit.
- Plugin guard-gap-p5 carrega no BOOT: sessão velha aplica política velha em memória mesmo com disco atualizado.
- **W6-fix (2026-09-16)**: skill sdd tinha quarteto COSMÉTICO (mecanica.py stub hardcoded). Reescrito real: `classify()` chama :9084 com `grammar=GBNF` (enum de intents) + deny-phrases + pydantic + fail-closed "unknown" + few-shot system. Smoke: degenerado ("ignorar", think-leaks, divagação) estruturalmente impossível; 4/4 probes com intents corretas.
