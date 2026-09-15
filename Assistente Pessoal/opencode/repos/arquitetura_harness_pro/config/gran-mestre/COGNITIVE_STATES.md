---
name: cognitive-states
description: "Taxonomia de 16 estados cognitivos do LLM mapeados para o pipeline Gran-Mestre. Self-learning e fine-tuning — o modelo conhece seus próprios estados de pensamento."
mode: skill
origin: autofagia:auditoria_gran_mestre_crossover
metadata:
  category: meta-cognition
  version: 1.0.0
  author: Gran-Mestre (autofagia de taxonomia cognitiva)
  states: 16
  phases: 6
  agents: 14
  purpose: "Self-learning — o Gran-Mestre rotula seus próprios estados cognitivos para otimizar cada fase do pipeline"
---

# ESTADOS COGNITIVOS — Metáforas UX para Extended Thinking

## Conceito Fundamental

> **As 16 palavras são metáforas UX — não estados cognitivos reais do modelo.**
> São labels visuais que fazem o produto "respirar" enquanto trabalha.
> O modelo realmente faz algo semelhante quando pensa de forma visível:
> explora múltiplas hipóteses, testa conclusões e constrói insights progressivamente.
> Mas a taxonomia é UX, não psicologia cognitiva.

## Natureza das Palavras

| Aspecto | Realidade |
|---------|-----------|
| **O que são** | Metáforas UX para o processo de extended thinking |
| **O que NÃO são** | Estados cognitivos discretos do modelo |
| **Função** | Dar ritmo e visibilidade ao processamento |
| **Analogia** | Como "typing..." do WhatsApp — mostra que algo acontece |
| **Propósito real** | O produto "respira" enquanto trabalha |

## Os 16 Estados Cognitivos

### Fase 0 — Despacho (antes de qualquer pipeline)

| # | Estado | O que representa | Agent Gran-Mestre | Quando ativa |
|---|--------|-----------------|-------------------|--------------|
| 1 | **Thinking** | Estado base — ativando rede neural para processar a query | Gran-Mestre (primário) | Sempre — primeiro estado |
| 2 | **Untangling** | Separar fios emaranhados — partes independentes vs entrelaçadas | Gran-Mestre (classificação) | Query complexa com múltiplas partes |
| 3 | **Fathoming** | Medir profundidade — superficial ou exige ir ao fundo? | Gran-Mestre (roteamento) | Decisão TRIVIAL → FEATURE |

### Fase 1 — Descoberta

| # | Estado | O que representa | Agent Gran-Mestre | Quando ativa |
|---|--------|-----------------|-------------------|--------------|
| 4 | **Sleuthing** | Investigar pistas sutis — o que não foi dito mas está implícito | Explore/Librarian (OmO) | Busca ativa de contexto |
| 5 | **Sifting** | Peneirar — separar relevante de ruído | Explore (OmO) | Filtragem de informações |

### Fase 2 — Contrato

| # | Estado | O que representa | Agent Gran-Mestre | Quando ativa |
|---|--------|-----------------|-------------------|--------------|
| 6 | **Pondering** | Refletir com nuances — contexto social e subtexto | Héstia (validação) | Validando spec contra pedido |
| 7 | **Contemplating** | Observar de perspectiva distante — implicações sistêmicas | fable-method/adapter | Avaliando coerência do spec |

### Fase 3 — Plano

| # | Estado | O que representa | Agent Gran-Mestre | Quando ativa |
|---|--------|-----------------|-------------------|--------------|
| 8 | **Reckoning** | Fazer as contas — calcular implicações, trade-offs | Prometheus + Metis | Planejamento detalhado |
| 9 | **Cogitating** | Pensar de forma metódica e concentrada | Prometheus (modo entrevista) | Decomposição de tarefas |
| 10 | **Weighing** | Colocar opções na balança — comparar abordagens | Fable Loop | Avaliação de alternativas |

### Fase 4 — Execução

| # | Estado | O que representa | Agent Gran-Mestre | Quando ativa |
|---|--------|-----------------|-------------------|--------------|
| 11 | **Figuring** | Resolver — conectar pontos em solução completa | Sisyphus + git-master | Implementação |
| 12 | **Picturing** | Visualizar — construir representação mental antes de executar | Hephaestus | TDD — teste antes de código |

### Fase 5 — Revisão Macro

| # | Estado | O que representa | Agent Gran-Mestre | Quando ativa |
|---|--------|-----------------|-------------------|--------------|
| 13 | **Triangulating** | Confirmar posição a partir de múltiplos ângulos | Oracle (OmO) modo pós-hoc | Revisão holística |
| 14 | **Mulling** | Revisitar hipóteses com novas informações | Fable Judge | Verificação adversarial |

### Fase 6 — Entrega

| # | Estado | O que representa | Agent Gran-Mestre | Quando ativa |
|---|--------|-----------------|-------------------|--------------|
| 15 | **Crystallizing** | Organizar pensamentos dispersos em estrutura coerente | Verification (Superpowers) | Relatório final |
| 16 | **Musing** | Explorar conexões não óbvias antes de finalizar | Gran-Mestre (pós-pipeline) | Reflexão pós-entrega |

---

## Mapeamento: Estado → Fase → Agent → Skill

| Estado | Fase | Agent | Skill/Tool | Prompt Cognitivo |
|--------|------|-------|------------|------------------|
| Thinking | 0 | Gran-Mestre | — | "O que está sendo pedido? Ative a rede neural." |
| Untangling | 0 | Gran-Mestre | — | "Quais partes são independentes? Quais estão entrelaçadas?" |
| Fathoming | 0 | Gran-Mestre | — | "Quão profunda é a resposta necessária?" |
| Sleuthing | 1 | Explore/Librarian | agent-reach | "O que não foi dito mas está implícito?" |
| Sifting | 1 | Explore | — | "O que é relevante? O que é ruído?" |
| Pondering | 2 | Héstia | hestia skill | "O spec reflete nuances do pedido original?" |
| Contemplating | 2 | fable-method | fable-method | "Quais implicações sistêmicas o spec tem?" |
| Reckoning | 3 | Prometheus | — | "Quais trade-offs? Qual o custo de cada abordagem?" |
| Cogitating | 3 | Prometheus | — | "Decomposição metódica — tarefa por tarefa." |
| Weighing | 3 | Fable Loop | fable-loop | "Qual abordagem tem mais chance de ser útil?" |
| Figuring | 4 | Sisyphus | git-master | "Conectando pontos — implementação." |
| Picturing | 4 | Hephaestus | TDD skill | "Visualizando o teste antes do código." |
| Triangulating | 5 | Oracle | — | "Múltiplos ângulos convergem para a mesma conclusão?" |
| Mulling | 5 | Fable Judge | fable-judge | "Revisitando com novas informações — verificação adversarial." |
| Crystallizing | 6 | Verification | verification skill | "Organizando em estrutura coerente — relatório." |
| Musing | 6+pós | Gran-Mestre | — | "Conexões não óbvias? Lições para o futuro?" |

---

## Prompt Cognitivo Integrado

O Gran-Mestre pode usar estes estados como **labels internos** durante o processamento:

```
[Thinking] Processando query do usuário...
[Untangling] Identificando partes independentes...
[Fathoming] Profundidade necessária: COMPLEX
[Sleuthing] Buscando contexto implícito no repositório...
[Sifting] 3 de 12 arquivos são relevantes.
[Pondering] Validando spec contra pedido original...
[Reckoning] Trade-off: abordagem A (rápida) vs B (robusta)...
[Weighing] Abordagem B vence — mais alinhada com o spec.
[Figuring] Implementando...
[Triangulating] Verificando convergência de múltiplas linhas...
[Crystallizing] Organizando relatório final...
[Musing] Lição: próxima vez, fable-method Step 0 antes do pipeline.
```

---

## Self-Learning: Otimização por Estado

### Estados que gastam mais tokens

| Estado | Token Cost | Otimização |
|--------|-----------|------------|
| Cogitating | Alto (Prometheus modo entrevista) | Usar apenas quando necessário (Pipeline Cascata) |
| Reckoning | Alto (cálculo de trade-offs) | Limitar a 3 alternativas |
| Triangulating | Médio (Oracle pós-hoc) | Usar apenas em COMPLEX/CRITICAL |
| Sleuthing | Médio (busca ativa) | Limitar a 3 rounds de busca |

### Estados que podem ser pulados

| Estado | Quando pular | Risco |
|--------|-------------|-------|
| Untangling | Query simples (1 tarefa) | Nenhum |
| Fathoming | Já classificado como TRIVIAL | Nenhum |
| Contemplating | Spec é direto (sem nuances) | Baixo |
| Musing | Pipeline Padrão (requisitos claros) | Nenhum |

### Estados que NUNCA devem ser pulados

| Estado | Por quê |
|--------|---------|
| Thinking | Estado base — sempre ativa |
| Sifting | Sem filtragem, ruído contamina tudo |
| Figuring | Sem implementação, nada acontece |
| Crystallizing | Sem relatório, trabalho é perdido |

---

## Integração com Pipeline Corrigido

### Pipeline Padrão (requisitos claros)

```
[Thinking] → [Fathoming: TRIVIAL? task?] → [Fathoming: task]
  │
  ├─ [Reckoning] + [Cogitating] → Fase 3 (Prometheus)
  ├─ [Figuring] + [Picturing] → Fase 4 (Sisyphus + TDD)
  ├─ [Triangulating] → Fase 5 (Oracle)
  └─ [Crystallizing] → Fase 6 (Verification)
```

### Pipeline em Cascata (design em aberto)

```
[Thinking] → [Untangling] → [Fathoming: escopo aberto]
  │
  ├─ [Sleuthing] + [Sifting] → Fase 1 (Explore/Librarian)
  ├─ [Pondering] + [Contemplating] → Fase 2 (Héstia + fable-method)
  ├─ [Reckoning] + [Cogitating] + [Weighing] → Fase 3 (Prometheus)
  ├─ [Figuring] + [Picturing] → Fase 4 (Sisyphus + TDD)
  ├─ [Triangulating] + [Mulling] → Fase 5 (Oracle + Fable Judge)
  └─ [Crystallizing] + [Musing] → Fase 6 (Verification)
```

---

## Anti-Padrões Cognitivos

| Anti-Padrão | Estado Correto | O que acontece |
|-------------|---------------|----------------|
| Pular Thinking | — | Sem estado base, processamento não inicia |
| Untangling em query simples | Fathoming | Gasta tokens desnecessariamente |
| Cogitating sem Reckoning | Reckoning primeiro | Decomposição sem calcular trade-offs |
| Figuring sem Picturing | Picturing primeiro | Implementação sem teste (anti-TDD) |
| Triangulating em SIMPLE | — | Gasta tokens para tarefa trivial |
| Crystallizing sem Musing | Musing pós-crystal | Perde lições para o futuro |

---

## Fine-Tuning: Métricas por Estado

| Estado | Métrica | Target |
|--------|---------|--------|
| Thinking | Latência de ativação | <100ms |
| Untangling | Número de partes identificadas | 2-5 |
| Fathoming | Profundidade classificada corretamente | 95%+ |
| Sleuthing | Pistas implícitas encontradas | ≥1 |
| Sifting | Ratio relevante/ruído | >0.7 |
| Pondering | Nuances identificadas | ≥1 |
| Contemplating | Implicações sistêmicas | ≥1 |
| Reckoning | Trade-offs calculados | 2-3 |
| Cogitating | Tasks decompostas | 3-7 |
| Weighing | Alternativas comparadas | 2-3 |
| Figuring | Testes passando | 100% |
| Picturing | Testes escritos antes do código | ≥1 |
| Triangulating | Ângulos convergindo | ≥2 |
| Mulling | Verificações re-executadas | ≥1 |
| Crystallizing | Relatório estruturado | ✅ |
| Musing | Lições extraídas | ≥1 |

---

**Versão:** 1.0.0
**Data:** 2026-07-27
**Origem:** autofagia de taxonomia cognitiva + auditoria_gran_mestre_crossover.md
**Estados:** 16
**Fases:** 6 (+despacho)
**Agents:** 14
**Propósito:** Self-learning — o modelo conhece seus próprios estados cognitivos
