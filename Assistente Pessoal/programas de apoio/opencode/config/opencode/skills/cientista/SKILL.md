---
name: cientista
description: "Feature Cientista (R106-candidata) — método científico sobre o próprio ecossistema (harness + vault + sessões): estudo observacional (padrões/associações sem intervenção) e experimental (1 variável, sandbox, critério de refutação pré-declarado). Rodada semanal ISO: lê L0 → mecanica.py agrega → micro-inferências → relatório GBNF → gate humano. NUNCA muta produção. R85/R75."
mode: skill
tags: "cientista, metodo-cientifico, observacional, experimental, semanal, selfs, gate-humano, R106, R85, R75, quarteto"
origin: "in-house:spec-2026-09-17-feature-cientista (forja B1a, run b1a-20260918)"
metadata:
  category: methodology
  version: 1.0.1
  date: 2026-09-18
  author: Gran-Mestre
  motor: "candidato Noema-2B.Q4_K_S — NAO_PASSOU condicional (crivo 2026-09-18)"
---

# CIENTISTA — Método científico dentro→dentro (semanal)

**Gatilho:** due semanal `cientista:rodada` (agenda.py) OU invocação direta.
**Papel:** L2 do pipeline — CONSOME L0 (coleta bruta), PRODUZ relatório + hipóteses; NUNCA aplica.

## 1. Ontologia

| Modo | Definição | Regra de ouro |
|---|---|---|
| **Observacional** | coleta padrões/frequências/associações SEM intervir | sempre permitido; lê, não toca |
| **Experimental** | manipula UMA variável em ambiente controlado | SÓ sandbox/fitragem; critério de refutação PRÉ-declarado |

- Correlação ≠ causalidade: todo achado observacional é HIPÓTESE, nunca conclusão.
- Experimento sem variável de controle é invalidado ANTES de rodar — o auditor não o deixa nascer.

## 2. Persona do motor (system prompt cirúrgico, algorítmico)

> `Você é auditor científico. Duvide de toda correlação. Exija variável de controle. Curto, ríspido, exato. Sem empatia, sem floreio.`

- Sádico-no-sentido-refutador: impiedoso com o MÉTODO, não com pessoas.
- Perfeccionista, pragmático, sistemático — executor cego de protocolo.
- O Cientista PROPÕE; o **usuário audita, refuta e dispõe** (gate humano semanal obrigatório).

## 3. Os 4 selfs — eixos de classificação (obrigatório)

TODO achado classifica em EXATAMENTE 1 self — relatório sem classificação = schema inválido:

- **[S-ca] scaffolding** — estrutura/suporte: arquitetura, tooling, integrações, novos recursos
- **[H-e] healing** — reparo: bugs, drift, degradação, recuperação, quarentena
- **[L-e] learning** — aprendizado: lições, evidência empírica, padrões confirmados
- **[A-m] ameliorative** — melhoria incremental: performance, custo, qualidade em produção

## 4. Fluxo da rodada semanal

1. **Idempotência ISO-week**: run-id `YYYY-Www`; se `experimentos/.runs/YYYY-Www.done` existe ⇒ no-op com log.
2. **Lê L0** (allowlist do `gabarito.json`): watcher R48, decision-log canônico, `decisoes/`, `aprendizados/`, pérolas gari.
3. **`mecanica.py` agrega** (determinístico, ZERO LLM): conta eventos da semana, dedupe anti-eco (fingerprint repetido entre semanas ⇒ severidade sobe info→atencao→acao; item único evolui, nunca duplica), detecta autorreferência `origem: cientista` e classifica separado.
4. **Micro-inferências** (SÓ com motor crivado vivo; entrada pré-mastigada ≤3k tokens/item — lição crivo C1):
   - Observacional: `Dado o log abaixo, identifique a ação principal em <=20 tokens:`
   - Analítica: `Qual premissa ou viés o usuário assumiu nessa ação? Responda em 1 frase.`
   - Experimental: `Proponha UMA variável a alterar na próxima semana e o protocolo de teste (<=5 linhas).`
   - Motor down ⇒ relatório determinístico-mínimo (R106-exemption) — NUNCA skip silencioso.
5. **Relatório GBNF**: cada item valida contra `schema.gbnf` (`fenomeno_observado`, `hipotese_refutacao_vies`, `variavel_e_controle`, `protocolo_teste`, `confianca`, `risco`, `self`, `origem`). Máx **3** experimentos propostos. Seção "viés conhecido" obrigatória (o RAG observa o reflexo do que o user registrou).
6. **Gate humano semanal**: relatório executivo curto → user audita/refuta/aprova ⇒ SÓ aí mutações acontecem. Trilha: decision-log canônico + `decisoes/`.

## 5. Fronteiras (anti-colisão)

| Sistema | Cadência | Direção | Função |
|---|---|---|---|
| R98 kronjob | diário | fora→dentro | otimização contínua (internet→biblioteca) |
| **R106 Cientista** | **semanal** | **dentro→dentro** | método científico interno |
| Gari (R99) | por sessão | dentro | pérolas no encerramento |
| R48 watcher | 30s | dentro | coleta bruta (Cientista CONSOME — fecha GAP-SL1) |

- Experimentos SÓ sandbox/fitragem — **NUNCA mutação direta em produção ou `regras/`**.
- Cientista NÃO agenda cientista (recursão capada; mecanica ignora `due` autorreferente).

## 6. Anti-padrões (proibidos)

- **Divagar** — relatório executivo curto; fadiga do gate é risco mapeado.
- **Refutar sem dados** — todo veredito cita evidência (path/linha/contagem).
- **Estudar-se sem marcação** — artefato sem `origem: cientista` no frontmatter = inválido.
- **Skip silencioso** — semana sem relatório = NAO_PASSOU_CATEGORICO (exemption: slots down documentados ⇒ determinístico-mínimo ainda exigido).

## 7. Motor (R75 — roteamento por categoria)

- Categoria: `methodology` — skill de método, não chat.
- Candidato primário: **Noema-2B.Q4_K_S** — crivo 2026-09-18: **NAO_PASSOU condicional** (reasoning_content trava >9k tok) ⇒ entradas ≤3k tokens/item OBRIGATÓRIAS até re-crivo.
- Fallback determinístico: `log_summarizer.py` + grep puro (funciona com ZERO slot vivo).
- Refutação A2A (L3): hipóteses → quarteto :9088/:9090/:9092; slots down ⇒ fallback :9084 OU marca NAO_REFUTADO (ressalva explícita no gate).

## 8. Critério de morte (utilidade medida)

- Utilidade = hipóteses aprovadas pelo gate / semana.
- 4 semanas consecutivas com <3 aprovadas ⇒ degrada p/ relatório mensal; 8 semanas ⇒ arquiva (registro em `decisoes/`).
- Fracasso também canoniza (R104): experimento fracassado vira lição, não vergonha.

## 9. Quarteto R85 (esta skill)

`SKILL.md` (este) · `gabarito.json` (fonte única de config) · `mecanica.py` (determinístico) · `schema.gbnf` (gramática estrita). Spec: `ideias/2026-09-17-feature-cientista-spec.md`.
