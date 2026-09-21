---
tipo: spec
feature: cientista
versao: 2.0
data: 2026-09-17
atualizado: 2026-09-18
estado: APROVADA-G1 (user) · aguardando forja (B1)
autor: gran-mestre (escrita in-house após 4 falhas de transporte SSE — circuit-breaker por forma de task)
---

# SPEC — Feature "Cientista" (estudo observacional + experimental, semanal)

## 1. Visão e persona

O **Cientista** é a skill que pratica método científico SOBRE o próprio ecossistema (harness + vault + sessões): estudo **observacional** (coleta padrões/frequências/associações sem intervir) e estudo **experimental** (manipula UMA variável em ambiente controlado, com critério de refutação pré-declarado). Meta declarada pelo usuário: o ecossistema tornar-se **mente coletiva** dos LLMs e sessions — topologia inspirada no conectoma da mosca-de-fruta (ver skill `snn-conectoma`), com os **4 selfs** `[S-ca] scaffolding · [H-e] healing · [L-e] learning · [A-m] ameliorative` permeados pelo **quarteto** `.md/.json/.py/.gbnf`.

**Persona do motor**: sádica-no-sentido-refutadora, perfeccionista, pragmática, sistemática. "Executor cego" de protocolo: não precisa ser sábia; precisa ser implacável **com o método**. O Cientista PROPÕE; o **usuário audita, refuta e dispõe** (gate humano semanal obrigatório — nada irreversível sem ele).

## 2. FASE 0 (antes de qualquer operação)

1. **Refresh do inventário**: `modelos LLM/manifesto_llm.json` está desatualizado (3 inventários stale detectados em 24h — lição registrada). Ferramenta `llm-inventory.py` hoje NÃO tem modo refresh (só --all/--probe/--register/--validate — evidência crivo C1 2026-09-18) ⇒ **GAP: criar modo refresh** (delega ao Hefesto depois).
2. **Diagnóstico da falha sistêmica de agendamento**: `skills/secretario/tooling/agenda.py` registra `due` mas NADA consome/dispara os dus vencidos automaticamente. Hipóteses verificáveis: (h1) não existe loop/daemon que chame `due`; (h2) check-in do secretario não é invocado sem sessão ativa; (h3) nenhum hook consulta agenda. Validar lendo agenda.py + hooks/ na forja.
3. **Onboarding R76** dos modelos novos já segue o crivo-padrão (R103/R104) — evidência: `benchmarks/2026-09-18-crivo-noema-2b.md` (Noema: NAO_PASSOU condicional — reasoning_content trava >9k tok).

## 3. Arquitetura — 5 camadas

```
L0 COLETA (existe — só consumir)
   features-watcher.py (R48, ciclo 30s) → relatório diário SEM consumidor (GAP-SL1)
   plugin tracer → trajectory.jsonl · decision-log canônico (vault) · gari pérolas/sessão
        │
L1 TRIAGEM (categoria vaga até crivo)
   motor pequeno canonizado (candidato primário: Noema-2B.Q4_K_S — status: NAO_PASSOU
   condicional no crivo 2026-09-18; re-teste com entradas ≤4k tok). Determinístico
   fallback: log_summarizer.py + grep puro (funciona com ZERO slot vivo).
        │
L2 MÉTODO (a feature — skill `cientista`, quarteto R85)
   Lê L0+L1 → observacional (padrões/associações) → esboça experimentos.
        │
L3 REFUTAÇÃO (já existe — scripts/a2a_brainstorm.py)
   Hipóteses do relatório passam pelo quarteto A2A (:9088/:9090/:9092).
   Slots down ⇒ fallback :9084 OU marca NAO_REFUTADO (ressalva explícita no gate).
        │
L4 GATE HUMANO SEMANAL (obrigatório)
   Relatório executivo → user audita/refuta/aprova → só aí mutações acontecem.
   Trilha: decision-log canônico + decisoes/.
```

## 4. Quarteto R85 da skill `cientista` (L2 — detalhe arquivo a arquivo)

Path: `skills/cientista/` (árvore canônica programas de apoio; live via symlink).

- **SKILL.md** — ontologia (observacional vs experimental), persona, os 4 selfs como eixos de classificação de TODO achado, fronteiras (§10), anti-padrões (divagar, refutar sem dados, estudar a si sem marcação).
- **gabarito.json** — fonte única: `allowlist_leitura` (vault, trajectory.jsonl, decision-log, benchmarks/, logs /tmp/opencode), `paths` canônicos, `exclusion_list` (quarentena/, archive/, ImagensFundo/, binários), `max_recursao: 1`, `iso_week_runid: true`, thresholds do critério de morte, ports usadas.
- **mecanica.py** — DETERMINÍSTICO, ZERO LLM: (a) agrega os sinais da semana (conta eventos do decision-log, decisoes/, aprendizados/, watcher); (b) dedupe anti-eco (mesmo sinal N semanas ⇒ sobe severidade, não novo item); (c) detecta autorreferência (`origem: cientista`) e classifica separado; (d) classifica cada achado num dos 4 selfs (regras por keyword/regex do gabarito); (e) emite esqueleto do relatório JSON validado contra schema.gbnf; (f) idempotência ISO-week (`experimentos/.runs/YYYY-Www.done` → 2ª execução no-op); (g) exit_status explícito. Smoke: `python3 mecanica.py --semana atual --dry-run`.
- **schema.gbnf** — gramática ESTRITA do relatório (fonte única; mecanica valida por parser equivalente): campos `fenomeno_observado`, `hipotese_refutacao_vies`, `variavel_e_controle`, `protocolo_teste`, `confianca` (alta|media|baixa), `risco` (nenhum|baixo|medio|alto), `self` (S-ca|H-e|L-e|A-m), `origem` (livre regex).

## 5. Pipeline de micro-inferências (quando motor crivado existir)

Nunca mega-prompt. Cadeia de 3 prompts curtos por item observado:

1. **Observacional**: `Dado o log abaixo, identifique a ação principal em <=20 tokens:`
2. **Analítica**: `Qual premissa ou viés o usuário assumiu nessa ação? Responda em 1 frase.`
3. **Experimental**: `Proponha UMA variável a alterar na próxima semana e o protocolo de teste (<=5 linhas).`

System prompt cirúrgico (algorítmico): `Você é auditor científico. Duvide de toda correlação. Exija variável de controle. Curto, ríspido, exato. Sem empatia, sem floreio.` Saída por item validada pelo schema.gbnf. Entrada SEMPRE pré-mastigada por mecanica.py (máx ~3k tokens/item — lição do crivo C1: prompts >9k travam modelos 2B reasoning).

## 6. Autorreferência (desejada) — 4 guards

1. Todo artefato do cientista carrega `origem: cientista` no frontmatter.
2. Recursão capada: cientista NÃO agenda cientista (mecanica ignora `due` que criaria a si próprio).
3. Anti-eco: fingerprint (hash do sinal normalizado) repetido entre semanas ⇒ severidade sobe (info→atencao→acao), item único evolui, nunca duplica.
4. Todo achado é classificado em exatamente 1 self (S-ca/H-e/L-e/A-m) — relatório sem classificação = schema inválido.

## 7. Gatilho semanal — 3 camadas fechadas

1. **agenda.py**: `due` semanal "cientista:rodada" registrado na instalação; check-in do secretario dispara.
2. **Regra candidata R106** (rascunho COMPLETO abaixo).
3. **Wrapper real** `scripts/cientista-weekly.sh` + systemd --user timer (conteúdo especificado abaixo; instalação na forja).

### 7a. Rascunho REGRA R106 (candidata — pendente ratificação do usuário)

> **R106 — Kronjob semanal do Cientista (dentro→dentro).** Toda semana ISO, o Cientista agrega os sinais do ecossistema (R48 watcher, decision-log, decisionlog gari, vault decisoes/aprendizados), classifica nos 4 selfs, propõe no MÁXIMO 3 experimentos (sandbox/fitragem, critério de refutação pré-declarado) e entrega relatório em `benchmarks/YYYY-MM-DD-cientista-semanal.md` + entrada em `experimentos/`. O relatório passa pelo gate humano semanal: **o usuário audita, refuta e aprova; sem gate, nada se aplica**. Semana sem relatório = NAO_PASSOU_CATEGORICO (exemption disciplinada: slots de execução down documentados ⇒ relatório determinístico-mínimo ainda é exigido). Fronteira: R98 é diário e fora→dentro; R106 é semanal e dentro→dentro. Colisão proibida.

### 7b. Wrapper + systemd (conteúdo especificado)

`scripts/cientista-weekly.sh`: checa ISO-week lock → chama `mecanica.py --semana atual` → se motor crivado vivo, roda micro-inferências → senão emite relatório determinístico-mínimo → escreve em benchmarks/ + log.
`~/.config/systemd/user/cientista-weekly.timer`: `OnCalendar=Sun *-*-* 20:00:00`, `Persistent=true`, unit chama o wrapper. Instalação: `systemctl --user daemon-reload && systemctl --user enable --now cientista-weekly.timer` (reversível: disable --now).

## 8. Setor `experimentos/` (novo, no vault)

- `experimentos/template-hipotese.md`: frontmatter (data, hipotese, variavel, controle, criterios_refutacao, self, origem, status[proposto|aprovado|rodando|concluido|fracassado-canonizado]) + corpo (método → variáveis → resultado → veredito). **Fracasso também canoniza** (R104).
- `experimentos/.runs/` guarda locks ISO-week (idempotência).

## 9. Critério de morte + idempotência + dedupe

- **Utilidade medida**: nº de hipóteses aprovadas pelo gate / semana. **Morte**: 4 semanas consecutivas com <3 aprovadas ⇒ feature degrada p/ relatório mensal; 8 semanas ⇒ arquiva (registro em decisoes/).
- **Idempotência**: run-id por ISO-week; reexecução = no-op com log.
- **Dedupe anti-eco**: fingerprint por sinal; repetição ⇒ severidade sobe.

## 10. Fronteiras (anti-colisão)

| Sistema | Cadência | Direção | Função |
|---|---|---|---|
| R98 kronjob | diário | fora→dentro (internet→biblioteca) | otimização contínua |
| **R106 Cientista** | semanal | dentro→dentro (ecossistema) | método científico interno |
| Gari (R99) | por sessão | dentro | pérolas no encerramento |
| R48 watcher | 30s | dentro | coleta bruta (Cientista CONSOME — fecha GAP-SL1) |

## 11. Riscos residuais

1. Slots down ⇒ relatório semanal sai determinístico-mínimo (aceitável por R106-exemption) ou NAO_REFUTADO — nunca skip silencioso.
2. Motor 2B reasoning trava em contexto grande (evidência crivo C1) ⇒ entradas ≤3k tok obrigatórias; re-crivo após ajuste.
3. Fadiga do usuário no gate semanal ⇒ mitigada por critério de morte e relatório executivo curto.
4. Viés de confirmação do vault (o RAG observa o reflexo do que o user registrou) ⇒ seção "viés conhecido" obrigatória no relatório.
5. Self-loop apesar dos guards ⇒ mecanica audita recursão (toda execução loga stack de origem).
6. Falha de agendamento não diagnosticada ⇒ FASE 0 item 2 é gate da forja.
7. Sandbox sem integração ⇒ experimentos v1 limitados a fitragem/leitura controlada até integração existir.

## 12. Checklist de implementação (F4 — forja)

1. skills/cientista/{SKILL.md, gabarito.json, mecanica.py, schema.gbnf} nas 2 árvores (canônica → live sync natural).
2. experimentos/ + template + .runs/
3. scripts/cientista-weekly.sh + systemd user timer (instalar+enable; reversível).
4. agenda.py: registrar due semanal "cientista:rodada".
5. Diagnóstico FASE 0 item 2 documentado em decisoes/.
6. Smoke: `mecanica.py --semana atual --dry-run` exit 0 + relatório esqueleto valida no schema.
7. Registro: decision-log + decisoes/log.md + lições.

## 13. Paths verificados (método)

| Path | Verificação |
|---|---|
| cerebro com IA/harness/decision-log.jsonl | criado+convergido 2026-09-18 (A2/A5), 427 linhas parse 100% |
| skills/a2a_brainstorm fallback :9084 | patch A1, --help exit 0 |
| cerebro com IA/benchmarks/2026-09-18-crivo-noema-2b.md | escrito pelo crivo C1 |
| experimentos/ | AUSENTE (criar na forja) |
| skills/secretario/tooling/agenda.py | existe (ground truth bibliotecário) |
| scripts/log_summarizer.py | existe (ground truth) |
