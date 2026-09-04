---
name: self-learning-auditoria
description: "Autofagia da auditoria_gran_mestre_crossover.md — extração completa de padrões, correções, anti-padrões e aprendizados para self-learning e fine-tuning do Gran-Mestre."
mode: skill
origin: autofagia:auditoria_gran_mestre_crossover
metadata:
  category: meta-learning
  version: 1.0.0
  author: Gran-Mestre (pipeline MIX — autofagia completa)
  source: /home/johncoffee/Downloads/auditoria_gran_mestre_crossover.md
  patterns: 22
  corrections: 7
  anti_patterns: 12
  meta_learnings: 8
  purpose: "Self-learning — cada auditoria gera aprendizados que melhoram o pipeline"
---

# SELF-LEARNING — Autofagia da Auditoria

## Conceito Fundamental

> **Cada auditoria é uma oportunidade de fine-tuning.**
> Não basta corrigir — é preciso aprender o padrão para nunca mais repetir.

## Fase 0 — Classificação

| Aspecto | Valor |
|---------|-------|
| Classificação | Escopo aberto (Pipeline Cascata) |
| Profundidade | Fathoming → fundo (meta-auditoria) |
| Estado cognitivo | Untangling → Sifting → Crystallizing |
| Fases percorridas | 6 completas |

---

## Fase 1 — Descoberta: 22 Padrões Extraídos

### Padrões de Arquitetura (7)

| # | Padrão | Descrição | Aprendizado |
|---|--------|-----------|-------------|
| 1 | **Auditar por mecanismo** | Não por analogia de papel — "parece um juiz" ≠ "é um juiz" | Sempre verificar o que a ferramenta realmente observa e produz |
| 2 | **Fase errada = desperdício** | Prometheus na Fase 1 gasta tokens para trabalho barato | Mapear agente → fase pelo mecanismo real, não pelo nome |
| 3 | **Redundância = custo sem ganho** | Héstia + Fable Judge na mesma fase = mesmo trabalho em dobro | Cada fase: uma camada por função |
| 4 | **Alias > invenção** | Atlas = Sisyphus+git-master, não agente novo | Preferir composição sobre criação do zero |
| 5 | **Composição > standalone** | Atena = Oracle + prompt adicional | Herda updates do upstream |
| 6 | **Despacho antes do pipeline** | fable-method Step 0 decide Padrão/Cascata antes de Fase 1 | Classificar antes de rotear |
| 7 | **Pipeline Padrão ≠ Cascata** | Requisitos claros não pagam custo de 6 fases | Definir explicitamente cada pipeline |

### Padrões de Segurança (5)

| # | Padrão | Descrição | Aprendizado |
|---|--------|-----------|-------------|
| 8 | **Injeção via interpolação** | `$msg` em código Python = execução arbitrária | Sempre usar `jq --arg` ou `printf` com sanitize |
| 9 | **Allowlist > blacklist** | Regex `^[a-zA-Z0-9_-]+$` rejeita tudo que não é permitido | Whitelist é mais seguro que tentar limpar |
| 10 | **SHA de scripts próprios** | Safety protocol sem attestation = sem garantia | Calcular SHA dos próprios scripts |
| 11 | **Separador frágil** | Dois espaços falham com nomes contendo espaços | Usar tabulação ou JSON |
| 12 | **Regex injection** | `grep "$FILE"` interpreta `.` como wildcard | Usar `grep -F` (fixed string) |

### Padrões de Auditoria (5)

| # | Padrão | Descrição | Aprendizado |
|---|--------|-----------|-------------|
| 13 | **Evidência antes de afirmação** | Nunca especular — sempre consultar a fonte | Documentar o que não foi verificado |
| 14 | **Causa raiz, não sintoma** | "Por que o problema existe?" vs "O que ele causa?" | Mapear efeito cascata |
| 15 | **Correções independentes** | Cada correção aplicável isoladamente | Não criar dependências entre correções |
| 16 | **Prós/contras/risco** | Toda correção precisa dos três | Não omitir contras |
| 17 | **Plug-and-play** | Entregar artefatos prontos para uso | Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+S |

### Padrões Cognitivos (5)

| # | Padrão | Descrição | Aprendizado |
|---|--------|-----------|-------------|
| 18 | **Releia como revisor hostil** | Qualquer afirmação não verificada = caveat | Verificar antes de afirmar |
| 19 | **Auditoria da auditoria** | Toda auditoria pode ter erros | Segundo grau pega inconsistências |
| 20 | **Contagens precisas** | "15 achados" vs 22 numerados = inconsistência | Reconciliar números |
| 21 | **Placeholders são dívidas** | "[a ser calculado]" = nunca feito | Completar antes de finalizar |
| 22 | **Proveniência importa** | Relatório sobre scripts ≠ leitura dos scripts | Declarar o que foi realmente verificado |

---

## Fase 2 — Contrato: 7 Correções Aplicadas

| # | Correção | Status | Arquivo |
|---|----------|--------|---------|
| 1 | Prometheus: Fase 1 → Fase 3 | ✅ | MIX_MODE.md |
| 2 | Héstia: escopo rastreabilidade | ✅ | HESTIA-SKILL.md |
| 3 | Atena: composição sobre Oracle | ✅ | ATHENA-SKILL.md |
| 4 | fable-method Step 0: despachante | ✅ | MIX_MODE.md |
| 5 | Pipeline Padrão: definido | ✅ | MIX_MODE.md |
| 6 | json_log(): jq --arg | ✅ | ecc-digest.sh |
| 7 | $type: allowlist regex | ✅ | ecc-digest.sh |

---

## Fase 3 — Plano: 12 Anti-Padrões Documentados

### Anti-Padrões de Pipeline

| Anti-Padrão | Consequência | Correção |
|-------------|-------------|----------|
| Auditar por analogia | Fase errada, ferramenta errada | Verificar mecanismo real |
| Redundância sem escopo diferenciado | Custo em dobro, ganho zero | Uma camada por função por fase |
| Pipeline Padrão não definido | Todo pedido paga 6 fases | Definir explicitamente |
| Despacho dentro da Fase 1 | Gasta fase inteira para classificar | fable-method Step 0 antes |

### Anti-Padrões de Segurança

| Anti-Padrão | Consequência | Correção |
|-------------|-------------|----------|
| Interpolação em código | Injeção de código | jq --arg |
| Separador frágil | Match incorreto | Tabulação ou JSON |
| Regex injection | Match incorreto | grep -F |
| Sem attestation de scripts | Sem garantia de integridade | SHA-256 |

### Anti-Padrões de Auditoria

| Anti-Padrão | Consequência | Correção |
|-------------|-------------|----------|
| Especulação sem evidência | Falso positivo | Consultar fonte |
| Placeholders não preenchidos | Dívida técnica | Completar antes de finalizar |
| Contagens inconsistentes | Confusão | Reconciliar números |
| Proveniência não declarada | Falso grau de certeza | Declarar o que foi verificado |

---

## Fase 4 — Execução: 8 Meta-Aprendizados

### Meta-Aprendizado 1: A Correção da Correção

**O que aconteceu:** A auditoria original propôs `printf` como fix para a injeção. A auditoria da auditoria apontou que `printf` não faz JSON-escaping — `jq --arg` é o correto.

**Lição:** Toda correção proposta deve ser testada com adversários (tentar injetar), não apenas lida.

**Aplicação:** Antes de aplicar qualquer fix de segurança, testar com:
- Aspas simples (`'`)
- Aspas duplas (`"`)
- Barra (`/`)
- Ponto-e-vírgula (`;`)
- Newline (`\n`)

### Meta-Aprendizado 2: O Achado que Desapareceu

**O que aconteceu:** Achado #5 (health check não verifica SHA) foi documentado mas sumiu das tabelas-resumo.

**Lição:** Toda auditoria deve reconciliar achados numerados com tabelas-resumo.

**Aplicação:** Checklist pós-auditoria:
- [ ] Todos os achados numerados aparecem nas tabelas?
- [ ] Contagens batem?
- [ ] Nenhum achado foi perdido?

### Meta-Aprendizado 3: O Placeholder que Nunca é Preenchido

**O que aconteceu:** Seção 5 (SHA dos scripts) tinha "[a ser calculado]" — literalmente um placeholder.

**Lição:** Placeholders são dívidas técnicas — se não preencher agora, nunca preenche.

**Aplicação:** Nenhum relatório é final com placeholders. Completar antes de commitar.

### Meta-Aprendizado 4: Relatório sobre ≠ Leitura de

**O que aconteceu:** A auditoria era "sobre" os scripts, não uma leitura linha por linha.

**Lição:** Declarar explicitamente o que foi realmente verificado vs o que foi inferido.

**Aplicação:** Toda auditoria deve ter seção "Limitações" declarando o que NÃO foi verificado.

### Meta-Aprendizado 5: A Allowlist que Faltava

**O que aconteceu:** `$type` era sanitizado por substituição (aceitava `/`, espaço, `;`) mas não por allowlist.

**Lição:** Allowlist (`^[a-zA-Z0-9_-]+$`) é mais seguro que blacklist (tentar limpar caracteres perigosos).

**Aplicação:** Para qualquer input que vira nome de arquivo ou path, usar allowlist.

### Meta-Aprendizado 6: O Separador que Quebra

**O que aconteceu:** Dois espaços como separador falham com nomes contendo espaços.

**Lição:** Para dados estruturados, usar formato robusto (JSON, tabulação) não separadores frágeis.

**Aplicação:** Nunca usar espaços como separador em dados que podem conter espaços.

### Meta-Aprendizado 7: A Regex que Não É Fixa

**O que aconteceu:** `grep "$FILE"` interpreta `.` como wildcard.

**Lição:** Para matching literal, sempre `grep -F` (fixed string).

**Aplicação:** Qualquer grep com input do usuário deve ser `grep -F`.

### Meta-Aprendizado 8: O SHA que Nunca Foi Calculado

**O que aconteceu:** Os scripts de safety protocol nunca tiveram sua integridade verificada.

**Lição:** O safety protocol precisa de safety protocol — os próprios scripts devem ser atestados.

**Aplicação:** Após criar/corrigir qualquer script de segurança, calcular e armazenar seu SHA.

---

## Fase 5 — Revisão: Checklist de Integridade

| Item | Status |
|------|--------|
| json_log(): jq --arg (não printf) | ✅ |
| $type: allowlist regex | ✅ |
| SHA-256 dos 6 scripts calculado | ✅ |
| Attestation salva em .ecc/autofagia/ | ✅ |
| Inconsistências numéricas documentadas | ✅ |
| auditoria_gran_mestre_crossover.md preservado | ✅ |
| Backup no repositório | ✅ |

---

## Fase 6 — Entrega: Template de Self-Learning

Para cada auditoria futura, extrair:

```markdown
## Padrões Extraídos (N)
| # | Padrão | Descrição | Aprendizado |

## Correções Aplicadas (N)
| # | Correção | Status | Arquivo |

## Anti-Padrões Documentados (N)
| Anti-Padrão | Consequência | Correção |

## Meta-Aprendizados (N)
### Meta-Aprendizado N: Título
**O que aconteceu:** ...
**Lição:** ...
**Aplicação:** ...
```

---

## Frequência de Auto-Auditoria

| Tipo | Frequência | Escopo |
|------|-----------|--------|
| Leve | A cada 10 pipelines | Anti-padrões e redundâncias |
| Completa | Mensal | 14 seções + reconciliação |
| Meta-auditoria | Após cada auditoria externa | Extrair meta-aprendizados |
| Fine-tuning | Após aplicar correções | Verificar se correção funciona |

---

**Versão:** 1.0.0
**Data:** 2026-07-27
**Origem:** autofagia completa de auditoria_gran_mestre_crossover.md
**Padrões:** 22 extraídos
**Correções:** 7 aplicadas
**Anti-padrões:** 12 documentados
**Meta-aprendizados:** 8 codificados
**Propósito:** Self-learning — cada auditoria melhora o pipeline
