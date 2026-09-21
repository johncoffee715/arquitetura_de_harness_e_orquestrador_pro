---
tipo: aprendizado
data: 2026-09-18
tags: [sessao, gari, perolas, cientista, governanca, a2a]
origem: gran-mestre
---

# Sessão 2026-09-17→18 — Feature Cientista (brainstorm/refutação) + faxina de governança

## O que foi feito

1. **F1 brainstorm Cientista**: refutação 4 vias (GM + 3 rodadas externas do user + ground truth bibliotecário). G1 fechado: arquitetura 5 camadas (cientista = metodologista, NÃO refutador-motor); crivo-first p/ todo modelo de screenshot; gatilho semanal 3 camadas (agenda.py + regra doutrinária + cron real).
2. **Correções de governança (A1/A2/A3/A5)**: transporte A2A curado (fallback :9084 + check_slots/REDFLAG), decision-log unificado no vault (Decisão A + 3 writers convergidos), meta_orchestrator.py confirmado existente (pendência morta), gabarito-raiz = no-op honesto.

## Evidência real

- a2a_brainstorm.py --help exit 0; check_slots presente; JSONL canônico 2/2 parse OK; sha256s registrados nos retornos A2/A3/A5.
- Slots 9086/9088/9090/9092 health=000 (4/5 do A2A down); único vivo :9084.

## Pérolas quantitativas

- decision-log legado: 423 registros históricos (231.640 bytes) preservados intocados; canônico nasce com 2 linhas; 3º log divergente (25 linhas) sem writers.
- hefesto/tooling: 5/5 arquivos da linha de defesa íntegros, byte-idênticos nas 2 árvores.
- gari mecanica --ignicao: qdrant_http 200, sync_check 0, biblioteca 14 benchmarks + 50 decisões.
- Repo /mnt/dados: 3992 linhas dirty (baseline declarado).

## Pérolas qualitativas (lições de engenharia R46)

1. **Inventário desatualizado morde 2× na mesma noite**: gabarito.json-raiz e manifesto_llm.json. Lição: claims de inventário exigem re-verificação no ato (evidência fresca > memória de inventário).
2. **3 coroações de modelo por screenshot em 1 sessão contradizem-se entre si** → prova viva da doutrina crivo-first (R103/R104). Noema-2B = candidato primário do user, mas papel por CATEGORIA até crivo.
3. **NO-OP honesto > evidência fabricada**: A2 recusou criar nota de quarentena p/ arquivo inexistente ("seria evidência falsa") — padrão a premiar.
4. **Symlink R102 descoberto na prática**: ~/.config/opencode ≡ programas de apoio (1 física) — drift de espelho nessa árvore é impossível; focar drift em hooks/scripts.
5. **User refutou o guard anti-autorreferência**: auto-estudo é o OBJETIVO (mente coletiva, topologia mosca-de-fruta). Guards viram: marcação de artefatos próprios + recursão capada + anti-eco/dedupe + eixo 4 selfs.
6. **Agendamento já existe e falha sistemicamente** (não é levado a rigor) → FASE 0 da spec cientista = diagnóstico dessa falha antes de criar qualquer wrapper novo.

## Estado

- Pipeline cientista: **CONCLUÍDO** (F2 spec in-house + B1 forja + crivo 3 candidatos + B2 drift + item 5 migração). Modo autônomo segue ON.

## Pérolas da 2ª metade da sessão (crivo + forja)

7. **R57 confirmada em produção**: Noema-2B com `enable_thinking:false` (campo chat_template_kwargs) virou PASSOU — mesma bateria que falhara com content vazio. Pensar nem sempre ajuda entrega estruturada.
8. **LFM-1.2B-Thinking: template sem toggle** — `enable_thinking:false` é ACEITO mas IGNORADO (só `preserve_thinking` existe). Budget <3k tok ⇒ content vazio; ≥3k funciona. Mas **alucina em anti-alucinação** ⇒ NAO_PASSOU p/ auditor (fabricar evidência é eliminatório).
9. **coder-3b**: único PASSOU de fábrica, com ressalva determinística: **100% fence ```json** — consumer deve strip. Lógica fraca (17:45 vs 18:15).
10. **Tasks longas de documento morrem em SSE timeout** (4 planejador + 1 executor, ~5 falhas); tasks curtas/read-only ou com escrita pequena passam. ⇒ GM escreve docs longos (governança); subagentes só escrita curta/código.
11. **wrapper systemd --user enable --now funciona** sem sudo: timer cientista-weekly ativo, próximo domingo 20h.
