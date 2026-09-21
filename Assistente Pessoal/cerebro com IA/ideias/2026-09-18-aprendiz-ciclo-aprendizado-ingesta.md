---
tipo: spec-candidata
status: proposta
data: 2026-09-18
origem: gerado pelo GM sob bypass autorizado (runtime de tasks 429/SSE-timeout; A2A pendente)
diretriz_usuario: "ensina ele a aprender através da ingesta com vídeos, ebooks, PDFs, input do user, A2A — LLM só devolve decisões tipadas, pode usar LLM barato; os 4 selfs são a base"
fundamento: os 4 selfs são a gramática; a ingesta é a fonte (único pipeline que alimenta os 4 eixos)
referencias:
  - cerebro com IA/aprendizados/2026-09-18_a2a-plano-mutacoes-4videos.md
  - textos/HahjBkz-0eY/LqpRNhAP09U/_bieksxg6oY/ae92ibehs4Q (transcrições R107)
---

# APRENDIZ — ciclo de aprendizado por ingesta contínua (spec-candidata)

## 0. Tese em 1 linha
Toda fonte que entra (vídeo, ebook/PDF, input do user, A2A) vira **deltas acionáveis com evidência e self obrigatório**, que alimentam vault/cientista/skills — nunca resumo decorativo.

## 1. Ontologia — 4 fontes × 8 estágios

| Fonte | Captura (quem) | Exemplo desta sessão |
|---|---|---|
| vídeo | R107 yt-dlp → `textos, pdf e esquemas/*-transcricao-*` | 4 transcrições de hoje |
| ebook/PDF | book-to-skill (existente) | — |
| input do user | gari (pérolas c/ gate de evidência) + decision-log | diretrizes desta sessão |
| A2A | loops refutação → `aprendizados/` | plano 4 vídeos |

Pipeline (toda fonte passa integralmente):
1. **captura** — raw preservado (vault/`raw/`); nunca sobrescreve.
2. **destilação** — extrai deltas (princípio, contra-exemplo, métrica, padrão) — NÃO resumo.
3. **triagem** — gate de evidência (gari 1.0.3): sem evidência ⇒ `claim_sem_evidencia: true` visível.
4. **classificação** — EXATAMENTE 1 self: `[S-ca]|[H-e]|[L-e]|[A-m]` (delta sem self = schema inválido).
5. **mapeamento** — qual feature/skill o delta toca (catálogo R8 primeiro — anti-duplicata).
6. **proposta** — diff conceitual por skill afetada (proposal, nunca escrita direta — fronteira bibliotecario 2.1.0).
7. **gate** — humano (ou GM autônomo R34 ≥ limiar).
8. **aplicação + feedback** — Hefesto/executor aplica; cientista mede utilidade na rodada semanal.

## 2. Fronteiras (anti-colisão, R2/R8)
- bibliotecario: GUARDA (vault, catálogo, retrieval). aprendiz: TRANSFORMA ingesta em propostas.
- book-to-skill: converte ebook/PDF → skill. aprendiz: consome o resultado como fonte.
- gari: fecha sessão (pérolas). aprendiz: consome pérolas como fonte.
- cientista: MEDE (semanal). aprendiz: produz hipóteses/deltas que o cientista audita.
- hefesto: FORJA mutações aprovadas. aprendiz: nunca forja.

## 3. Schema do delta acionável (GBNF-strict)
```yaml
delta:
  id: "YYYY-MM-DD-<slug>"
  fonte: {tipo: video|ebook|user|a2a, ref: "<path/url>"}
  self: "S-ca | H-e | L-e | A-m"            # obrigatório
  principio: "<1 frase>"
  contraexemplo: "<opcional — evidência negativa>"
  evidencia: {path: "...", trecho: "...", comando: "..."}  # obrigatório
  afeta: [<skills/features>]
  proposta: "<diff conceitual>"
  confianca: 0.0-1.0
  claim_sem_evidencia: bool                # default false; true ⟹ visível
```

## 4. Cadência
- gatilhos: fim de sessão (gari), kronjob diário (R98), ingesta manual (vídeo/ebook entregue), fim de A2A.
- semanal: cientista consome os deltas da semana e mede utilidade por self.

## 5. Quarteto R85
- `SKILL.md` — esta ontologia.
- `gabarito.json` — fontes permitidas, limiares (confiança gate 0.6), allowlist de paths.
- `mecanica.py` — determinístico: valida schema do delta, dedupe por fingerprint, conta por self.
- `schema.gbnf` — gramática do delta (fonte da validação).

## 6. Critério de morte
- utilidade = deltas aprovados no gate / semana, por self.
- 4 semanas <3 aprovados ⇒ degrada p/ mensal; 8 ⇒ arquiva (espelha cientista R106).

## 7. Anti-padrões
- resumo sem delta acionável · delta sem self · delta sem evidência sem flag · duplicar book-to-skill/gari/bibliotecario · escrever direto no vault sem gate · classificar em 2 selfs ("pega o dominante ou rejeita").

## 8. Estado de forja
PENDENTE: A2A (proposer×refuter×juiz) + executor-f4 — bloqueado por runtime de tasks (429/SSE) em 2026-09-18. Spec pronta para forja quando liberar.
