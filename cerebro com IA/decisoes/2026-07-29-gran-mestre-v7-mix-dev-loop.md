---
tags: [gran-mestre, decisao, MIX, dinâmico, dev-loop, pipeline]
date: 2026-07-29
pipeline: MIX
rota: MIX (COMPLEX + CRITICAL + FEATURE)
modelo: omniroute/auto/best-free
---

# Decisão: Gran-Mestre v7 — Delegação Dinâmica + Modo MIX + Dev Loop

## Contexto
O Gran-Mestre v6 tinha agents hardcoded por fase do pipeline. Cada modo
(TRIVIAL, SIMPLE, MEDIUM, COMPLEX, CRITICAL, FEATURE) especificava agentes
fixos. Isso criava rigidez: qualquer mudança exigia editar PIPELINE_MODES.md,
SKILL.md, MIX_MODE.md, etc. Além disso, não havia um sistema de iteração
estruturada — o modelo ficava "tentando de novo" sem critério.

## Decisão
Três mudanças arquiteturais simultâneas:

### 1. Delegação Dinâmica via Registry
- **Antes:** `Fase 4: Atlas → Fable Loop → Implementer → Code Reviewer`
- **Depois:** `Fase 4: consulta Registry por tags → compõe equipe → delega`
- Cada fase consulta `REGISTRY_SUBAGENTS.md` por **tags de capacidade**
- Pipeline vira líquido — plasticidade neural

### 2. Modo MIX como default
- **Antes:** 6 modos (TRIVIAL/SIMPLE/MEDIUM/COMPLEX/CRITICAL/FEATURE)
- **Depois:** 4 modos (MIX/FEATURE/COMPLEX/CRITICAL)
- **MIX = COMPLEX + CRITICAL + FEATURE** — ativa tudo simultaneamente
- TRIVIAL e SIMPLE foram absorvidos pelo Dev Loop N1 (ReAct)
- MEDIUM foi absorvido pelo pipeline MIX

### 3. Dev Loop de 3 Níveis
- **N1 — ReAct:** think → act → observe → repeat (reflexo neural)
- **N2 — Mini Loop:** spec → TDD → implementa → merge (hábito)
- **N3 — Human Loop:** decide → métricas → PR → decide (consciência)
- Escalonamento automático entre níveis

## Rationale
1. **Plasticidade** — Pipeline se adapta a qualquer task sem editar config
2. **Resiliência** — Nenhum subagent hardcoded = nenhum ponto único de falha
3. **Iteração** — Dev Loop estrutura a repetição com critérios de parada
4. **Economia** — Menos modos para lembrar (de 6 para 1 default)
5. **Evolução** — Métricas de acerto/erro alimentam o Registry

## Neurônios Afetados
- [[entities/gran-mestre]] — orquestrador atualizado para v7
- [[concepts/delegacao-dinamica]] — novo conceito
- [[concepts/dev-loop]] — novo conceito

## Sinapses Criadas
- `delegação-dinâmica` ⟷ `antropofagia-tecnologica`
- `delegacao-dinamica` ⟷ `gran-mestre`
- `dev-loop` ⟷ `gran-mestre`
- `dev-loop` ⟷ `delegacao-dinamica`

## Referências
- [[REGISTRY_SUBAGENTS.md]] — 61 subagents com tags
- [[PIPELINE_MODES.md]] — v8.0.0 delegação dinâmica
- [[MIX_MODE.md]] — v5.0.0
- [[GLOBAL_POLICY.md]] — v2.0.0
- [[2026-07-25-gran-mestre-v7-obsidian]] — decisão anterior

---

*Neurônio criado em: 2026-07-29*
*Sinapses: [[entities/gran-mestre]] [[concepts/delegacao-dinamica]] [[concepts/dev-loop]]*
