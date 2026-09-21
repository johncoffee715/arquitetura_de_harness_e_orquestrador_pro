---
name: aprendiz
description: "Ciclo de aprendizado por ingesta contínua — transforma 4 fontes (vídeo, ebook/PDF, input do user, A2A) em DELTAS acionáveis com evidência e self obrigatório ([S-ca]/[H-e]/[L-e]/[A-m]). Orquestra (não duplica) bibliotecario/book-to-skill/gari/cientista/hefesto. LLM barato só devolve decisões tipadas (GBNF), nunca prosa. Spec: ideias/2026-09-18-aprendiz-ciclo-aprendizado-ingesta.md. R2/R8/R34/R94."
mode: skill
tags: "aprendiz, ingesta, aprendizado, deltas, 4selfs, destilacao, gate-evidencia, R98, R106, R107"
origin: "in-house:spec-2026-09-18 (diretriz usuário + validação 4 vídeos)"
metadata:
  category: methodology
  version: 1.0.0
  date: 2026-09-18
  author: Gran-Mestre (bypass autorizado — runtime tasks 429)
  motor: determinístico (LLM barato só tipifica via schema)
---

# APRENDIZ — ciclo de aprendizado por ingesta contínua

**Tese**: toda fonte que entra (vídeo, ebook/PDF, input do user, A2A) vira **deltas acionáveis
com evidência e self obrigatório** — nunca resumo decorativo. Os 4 selfs são a gramática;
a ingesta é a fonte (único pipeline que alimenta os 4 eixos).

## Pipeline (toda fonte, integralmente)

1. **captura** → raw preservado (vault/`raw/`, R107 p/ vídeo; book-to-skill p/ ebook)
2. **destilação** → extrai deltas (princípio / contra-exemplo / métrica / padrão) — NÃO resumo
3. **triagem** → gate de evidência (gari 1.0.3): sem evidência ⇒ `claim_sem_evidencia: true` visível
4. **classificação** → EXATAMENTE 1 self: `[S-ca]|[H-e]|[L-e]|[A-m]` (sem self = schema inválido)
5. **mapeamento** → catálogo R8 primeiro: qual skill/feature o delta toca (anti-duplicata)
6. **proposta** → `bibliotecario/tooling/propor.py` (proposal-queue, nunca escrita direta)
7. **gate** → humano (ou GM autônomo R34 ≥ limiar)
8. **aplicação + feedback** → Hefesto/executor; cientista mede utilidade semanal (R106)

## Fronteiras (R2/R8 — orquestra, não duplica)

| Skill | Faz | Aprendiz |
|---|---|---|
| bibliotecario | guarda/catálogo/retrieval | envia propostas p/ gate |
| book-to-skill | ebook→skill | consome como fonte |
| gari | pérolas fim-de-sessão | consome como fonte |
| cientista | mede (semanal) | produz hipóteses auditadas |
| hefesto | forja mutações aprovadas | nunca forja |

## Schema do delta (schema.gbnf — estrito)

```yaml
delta:
  id: "YYYY-MM-DD-<slug>"
  fonte: {tipo: video|ebook|user|a2a, ref: "<path/url>"}
  self: "S-ca|H-e|L-e|A-m"             # obrigatório, exatamente 1
  principio: "<1 frase>"
  contraexemplo: "<opcional>"
  evidencia: {path: "...", trecho: "..."}  # obrigatório (ou flag)
  afeta: [<skills>]
  proposta: "<diff conceitual>"
  confianca: 0.0-1.0
  claim_sem_evidencia: bool            # default false
```

## Cadência

- **gatilhos**: fim de sessão (gari), kronjob diário (R98), ingesta manual, fim de A2A
- **semanal**: cientista consome deltas da semana e mede utilidade por self

## Motor de decisão tipada (diretriz do usuário)

LLM barato (:9086 317 t/s) envolvido SÓ na classificação da fonte→self via **GBNF-estrito**
(schema, não prompt — R81/R82); nunca gera prosa. Se `confianca < 0.6` ⇒ delta marcado
`revisar` na fila (mesmo gate do batedor jev-eval).

## Critério de morte

utilidade = deltas aprovados no gate / semana, por self. 4 semanas <3 ⇒ mensal; 8 ⇒ arquiva.

## Anti-padrões

resumo sem delta · delta sem self · evidência ausente sem flag · duplicar book-to-skill/gari ·
escrita direta no vault sem gate · 2 selfs no mesmo delta ("pega o dominante ou rejeita").

## Quarteto R85

`SKILL.md` (este) · `gabarito.json` (fontes/limiares allowlist) · `mecanica.py` (valida delta,
dedupe, conta por self — zero LLM) · `schema.gbnf` (gramática fonte da validação).
