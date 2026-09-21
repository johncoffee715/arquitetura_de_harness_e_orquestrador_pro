---
regra: R101
titulo: "SETOR DE REGRAS NA BIBLIOTECA + SYNCLINKS VIA TOOL CALL AO BIBLIOTECÁRIO (REDUÇÃO DO SYSTEM PROMPT + PREFILL OTIMIZADO)"
fonte: AGENTS.md (linha 1574)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R101 — SETOR DE REGRAS NA BIBLIOTECA + SYNCLINKS VIA TOOL CALL AO BIBLIOTECÁRIO (REDUÇÃO DO SYSTEM PROMPT + PREFILL OTIMIZADO) — promulgado 2026-09-11 ═══

**Regra**: criar, via os 4 quartetos, um setor APENAS para regras dentro da biblioteca
(`cerebro com IA/regras/`), e as regras carregadas no orquestrador via os 4 quartetos DEVEM ser
auditadas com **synclinks** via tool call ao Bibliotecário — reduzindo o system prompt inicial,
otimizando o prefill do orquestrador e convertendo-o para tool call ultra-fast, aproveitando as
características ultrafast do Bibliotecário (RWKV7 0.4B, 1M ctx, ~143 t/s) para entregar ao
orquestrador SÓ o "puro suco" (regras relevantes ao contexto), entregando ao usuário um workflow
mais fluido e corrigindo as debilidades iniciais do LLM de precisão crítica (janela cara, prefill pesado).

<Princípio>
- A constituição (AGENTS.md, ~150KB) NÃO deve ser carregada integral no system prompt do
  orquestrador — ela vive no setor `regras/` da biblioteca e é recuperada sob demanda.
- O orquestrador consulta o Bibliotecário (tool call ultra-fast) para obter SÓ a regra relevante
  ao contexto corrente — nunca o dump inteiro.
- Synclink = vínculo de sincronização auditável entre a regra no vault e a regra carregada no
  orquestrador (fonte única + verificação de drift).

<Procedimento obrigatório>
1. Setor `cerebro com IA/regras/` — uma nota por regra (R1..R101) + `index.md` (mapa vivo).
2. Synclink audit: tool call ao Bibliotecário verifica que a regra no vault == regra carregada
   (SHA/versão), antes de qualquer decisão que dependa dela.
3. Retrieval on-demand: o orquestrador pede a regra específica (não o bloco inteiro) — o
   Bibliotecário devolve o "puro suco" (trecho exato + referência).
4. Prefill otimizado: system prompt enxuto (só o núcleo irredutível) + regras sob demanda.

<Enforcement>
- Regra carregada sem synclink auditado = GAP (R8/R94/R100 violados por omissão).
- Regra fabricada (sem path real no vault) = fraude (R28) — `NAO_PASSOU_CATEGORICO`.
- O Bibliotecário NUNCA sai do vault (R94); o orquestrador NUNCA carrega o dump inteiro (R70).

<Exemplo canônico (2026-09-11)>
- Orquestrador precisa da R93 (preservação) → tool call ao Bibliotecário → devolve só a R93
  (trecho + path `regras/R93-preservacao-orquestrador.md`) → prefill economizado ~150KB → workflow fluido.

## Ingestão por upgrade (R108-canônica — input de regra nova)

**Gatilho**: sempre que o user gerar input de nova regra universal guardrail, o orquestrador
da session DEVE varrer TODAS as regras coexistentes (via `index.md` + search do Bibliotecário,
R100) ANTES de criar qualquer nota nova.

**Decisão**: fazer **UPGRADE** na regra mais próxima e coerente (score mais alto) — nunca
criar arquivo novo por default. Criar nota nova SÓ se nenhuma candidata passar de 60 (escala
R34) e com justificativa de gap explícita registrada.

**Objetivo**: otimizar a biblioteca (espaço + tempo), ganhar t/s (prefill menor ao
orquestrador), aperfeiçoar o ecossistema e a mente coletiva no Obsidian.

**Procedimento**:
1. Buscar (lexical + semântico) em `regras/` — `index.md` + `regras.py search`.
2. Ranquear top-3 candidatas com scores (R34).
3. Enxertar o delta na TOP-1 (append cirúrgico, sem remoção de conteúdo existente).
4. Auditar synclink em `index.md` + `nucleo-irredutivel.md` (drift = GAP).

**Anti-reinvenção**: instanciação concreta de R8 (catálogo primeiro) para o setor de regras —
regra sem synclink = GAP (conforme R101 existente).
