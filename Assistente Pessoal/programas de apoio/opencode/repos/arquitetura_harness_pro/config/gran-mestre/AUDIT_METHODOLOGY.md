---
name: audit-methodology
description: "Metodologia de auditoria extraída por autofagia da auditoria_gran_mestre_crossover.md. Framework reutilizável para auditoria de qualquer sistema — self-learning e fine-tuning do Gran-Mestre."
mode: skill
origin: autofagia:auditoria_gran_mestre_crossover
metadata:
  category: meta-audit
  version: 1.0.0
  author: Gran-Mestre (autofagia de auditoria externa)
  source: /home/johncoffee/Downloads/auditoria_gran_mestre_crossover.md
  sections: 14
  patterns: 12
  reusable: true
  purpose: "Self-learning — o Gran-Mestre usa esta metodologia para auditar a si mesmo e qualquer framework"
---

# METODOLOGIA DE AUDITORIA — Framework Reutilizável

## Conceito Fundamental

> **Auditar por *mecanismo*, não por *analogia de papel*.**
> A pergunta não é "isso parece um juiz?" — é "o que essa ferramenta realmente observa e produz como evidência?"

## Origem

Esta metodologia foi extraída por autofagia da auditoria técnica `auditoria_gran_mestre_crossover.md` (2026-07-27). O documento original tinha 14 seções, 5 problemas identificados, 7 correções propostas, e 3 anexos plug-and-play.

A metodologia é **genérica** — funciona para auditar qualquer sistema, framework, ou workflow.

---

## As 14 Seções da Auditoria

### Seção 1 — Visão Geral da Arquitetura

**O que faz:** Descreve o estado atual do sistema de forma factual, sem juízo de valor.

**Padrão de execução:**
1. Listar dependências reais (verificadas na fonte, não por inferência)
2. Para cada dependência: o que realmente é + componentes confirmados
3. Sinalizar limitações de acesso (o que NÃO foi possível verificar)

**Anti-padrões:**
- ❌ Descrever por memória — sempre consultar a fonte
- ❌ Assumir que "parece X" significa "é X"
- ❌ Não sinalizar o que não foi verificado

**Template:**
```markdown
| Framework | O que realmente é | Componentes confirmados |
|-----------|-------------------|------------------------|
| X         | [descrição factual] | [lista verificada]    |

Limitação declarada: [o que não foi possível verificar]
```

---

### Seção 2 — Auditoria Técnica

**O que faz:** Identifica pontos fortes, fracos e redundâncias com evidência.

**Padrão de execução:**
1. **Pontos fortes** — o que está certo e por quê
2. **Pontos fracos** — cada um com evidência, nunca especulação
3. **Redundâncias confirmadas** — mapear sobreposições exatas

**Cada ponto fraco deve ter:**
- Evidência (onde viu)
- Impacto (o que causa)
- Risco (o que pode dar errado)

**Anti-padrões:**
- ❌ "Acho que pode ser melhor" — sem evidência, não é ponto fraco
- ❌ Listar problemas sem impacto — é reclamação, não auditoria
- ❌ Não diferenciar redundância real de redundância aparente

---

### Seção 3 — Engenharia Reversa

**O que faz:** Remapeia o fluxo real do sistema (o que *deveria* acontecer) vs o que está documentado.

**Padrão de execução:**
1. Identificar a camada de despacho oculta (o que deveria vir antes)
2. Criar tabela de remapeamento: nome no doc → motor real
3. Para cada fase/módulo: o que está escrito vs o que deveria invocar

**Anti-padrões:**
- ❌ Aceitar o diagrama como verdade sem verificar
- ❌ Não questionar posicionamento de componentes
- ❌ Não mapear nomes próprios para equivalentes reais

**Template:**
```markdown
| Fase | Nome no doc | Motor real recomendado |
|------|-------------|----------------------|
| 1    | Prometheus  | Explore/Librarian    |
```

---

### Seção 4 — Análise de Problemas

**O que faz:** Identifica causa raiz e efeito cascata dos problemas.

**Padrão de execução:**
1. **Causa raiz** — por que o problema existe (geralmente: analogia de papel vs mecanismo)
2. **Impacto** — o que acontece agora
3. **Risco** — o que pode dar errado no futuro
4. **Efeito cascata** — como o problema se propaga

**Anti-padrões:**
- ❌ Tratar sintomas, não causas
- ❌ Não mapear efeito cascata
- ❌ Não conectar problemas entre si

---

### Seção 5 — Predição

**O que faz:** Antecipa problemas futuros com base na análise.

**Padrão de execução:**
1. **Gargalo futuro** — onde o sistema vai travar
2. **Limitação** — o que o sistema não consegue fazer
3. **Escalabilidade** — onde vai quebrar com mais carga
4. **Ponto de falha** — onde vai falhar primeiro

**Classificação:**
- CRÍTICA — vai causar problema em breve
- IMPORTANTE — vai causar problema eventualmente
- FUTURA — pode causar problema em cenário específico

**Anti-padrões:**
- ❌ Predições vagas ("pode dar problema") — precisa ser específico
- ❌ Não classificar urgência
- ❌ Não conectar com causa raiz da Seção 4

---

### Seção 6 — Prevenção

**O que faz:** Propõe ações preventivas antes que os problemas aconteçam.

**Padrão de execução:**
1. Para cada predição da Seção 5: uma ação preventiva
2. Classificar urgência (CRÍTICA / IMPORTANTE / FUTURA)
3. Ser específico: o que fazer, quando, como

**Anti-padrões:**
- ❌ "Melhorar a documentação" — vago demais
- ❌ Não conectar com predição específica
- ❌ Não priorizar

---

### Seção 7 — Correção

**O que faz:** Propõe correções concretas com análise de prós/contras/risco.

**Padrão de execução:**
1. Tabela com: #, Mudança, Classificação, Prós, Contras, Risco, Impacto técnico
2. Cada correção é independente (pode ser aplicada isoladamente)
3. Classificação: CRÍTICA / IMPORTANTE / OPCIONAL / FUTURA

**Anti-padrões:**
- ❌ Correções acopladas (precisa aplicar todas ou nenhuma)
- ❌ Não analisar contras
- ❌ Não classificar impacto técnico

**Template:**
```markdown
| # | Mudança | Classificação | Prós | Contras | Risco | Impacto técnico |
|---|---------|---------------|------|---------|-------|-----------------|
| 1 | [ação]  | CRÍTICA       | [...] | [...]  | Baixo | [...]           |
```

---

### Seção 8 — Refatoração

**O que faz:** Propõe simplificações e melhorias arquiteturais.

**Padrão de execução:**
1. **Simplificação** — eliminar duplicações
2. **Modularização** — dar padrão de arquivo a componentes informais
3. **Redução de complexidade** — substituir numeração ad-hoc por nomes funcionais
4. **Melhoria arquitetural** — corrigir estruturas subespecificadas

**Anti-padrões:**
- ❌ Refatorar sem entender o que está fazendo
- ❌ Não manter compatibilidade com o que funciona
- ❌ Criar mais complexidade em vez de reduzir

---

### Seção 9 — Integração

**O que faz:** Avalia compatibilidade das correções com o sistema existente.

**Padrão de execução:**
1. **Compatibilidade** — as correções trocam componentes ou só remapeiam?
2. **Impacto nos módulos existentes** — o que muda de comportamento?
3. **Plano de migração** — passos concretos para aplicar

**Anti-padrões:**
- ❌ Propor correções que quebram o que funciona
- ❌ Não fornecer plano de migração
- ❌ Não avaliar impacto em módulos existentes

---

### Seção 10 — Comparação

**O que faz:** Tabela antes/depois mostrando o benefício obtido.

**Padrão de execução:**
1. Tabela com: Aspecto, Original, Corrigido, Benefício obtido
2. Cada linha mostra uma mudança concreta
3. Benefício é mensurável ou descritivo claro

**Template:**
```markdown
| Aspecto | Original | Corrigido | Benefício |
|---------|----------|-----------|-----------|
| Fase 1  | [antes]  | [depois]  | [ganho]   |
```

---

### Seção 11 — Melhorias Técnicas

**O que faz:** Prioriza melhorias em imediatas, médio prazo, longo prazo.

**Padrão de execução:**
1. **Imediatas** — o que fazer agora
2. **Médio prazo** — o que fazer em semanas
3. **Longo prazo** — o que fazer em meses

---

### Seção 12 — Roadmap

**O que faz:** Próxima evolução recomendada.

**Padrão de execução:**
1. Um parágrafo com o próximo passo natural
2. Conectar com as melhorias da Seção 11
3. Ser específico e acionável

---

### Seção 13 — Checklist

**O que faz:** Estado atual da implementação.

**Padrão de execução:**
1. ✔ **Implementado** — o que já existe
2. ✔ **Corrigido nesta auditoria** — o que foi mudado
3. ✔ **Pendente (seu lado)** — o que o usuário precisa fazer
4. ✔ **Futuro** — o que fazer depois

---

### Seção 14 — Entrega

**O que faz:** Artefato plug-and-play para o usuário.

**Padrão de execução:**
1. Anexos com código/config prontos para copiar e colar
2. Instruções claras: Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+S
3. Nenhuma outra mudança de código necessária

---

## Os 12 Padrões da Metodologia

| # | Padrão | Descrição |
|---|--------|-----------|
| 1 | **Auditar por mecanismo** | Não por analogia de papel — o que a ferramenta realmente faz? |
| 2 | **Evidência antes de afirmação** | Nunca especular — sempre consultar a fonte |
| 3 | **Sinalizar limitações** | O que não foi verificado é tão importante quanto o que foi |
| 4 | **Causa raiz, não sintoma** | Entender por que o problema existe, não apenas o que ele causa |
| 5 | **Efeito cascata** | Mapear como problemas se propagam pelo sistema |
| 6 | **Predição com classificação** | CRÍTICA / IMPORTANTE / FUTURA |
| 7 | **Correções independentes** | Cada correção pode ser aplicada isoladamente |
| 8 | **Prós/contras/risco** | Toda correção precisa dos três |
| 9 | **Comparação antes/depois** | Mostrar o benefício concreto |
| 10 | **Plug-and-play** | Entregar artefatos prontos para uso |
| 11 | **Escopo diferenciado** | Quando duas ferramentas fazem "a mesma coisa", verificar se realmente fazem |
| 12 | **Alias vs invenção** | Preferir composição/alias sobre invenção do zero |

---

## Anti-Padrões de Auditoria

| Anti-Padrão | Por que é ruim | Correção |
|-------------|---------------|----------|
| Auditar por analogia | "Parece um juiz" ≠ "É um juiz" | Verificar mecanismo real |
| Especulação sem evidência | "Acho que pode dar problema" | Consultar fonte, documentar evidência |
| Não sinalizar limitações | Falso positivo de segurança | Declarar o que não foi verificado |
| Tratar sintomas | Problema volta | Identificar causa raiz |
| Correções acopladas | Tudo ou nada | Tornar cada correção independente |
| Não classificar urgência | Tudo parece importante | CRÍTICA / IMPORTANTE / FUTURA |
| Não fornecer plano de migração | Usuário não sabe como aplicar | Passos concretos |
| Não mapear efeito cascata | Problema se propaga silenciosamente | Conectar problemas entre si |

---

## Template de Auditoria (14 seções)

```markdown
# Auditoria Técnica — [Sistema Alvo]

**Escopo:** [o que está sendo auditado]
**Fontes consultadas:** [lista de fontes diretas]
**Limitação declarada:** [o que não foi possível verificar]

---

## 1. Visão Geral da Arquitetura
[Estado atual + dependências reais + limitações]

## 2. Auditoria Técnica
[Pontos fortes + fracos (com evidência) + redundâncias]

## 3. Engenharia Reversa
[Remapeamento: nome no doc → motor real]

## 4. Análise de Problemas
[Causa raiz + impacto + risco + efeito cascata]

## 5. Predição
[Gargalo futuro + limitação + escalabilidade + ponto de falha]

## 6. Prevenção
[Ações preventivas por urgência]

## 7. Correção
[Tabela de correções com prós/contras/risco]

## 8. Refatoração
[Simplificação + modularização + redução de complexidade]

## 9. Integração
[Compatibilidade + impacto + plano de migração]

## 10. Comparação
[Tabela antes/depois]

## 11. Melhorias Técnicas
[Imediatas / médio prazo / longo prazo]

## 12. Roadmap
[Próxima evolução]

## 13. Checklist
[Implementado / corrigido / pendente / futuro]

## 14. Entrega
[Anexos plug-and-play]
```

---

## Uso pelo Gran-Mestre

### Auto-Auditoria (self-learning)

O Gran-Mestre pode usar esta metodologia para auditar a si mesmo:

1. Rodar a Seção 1 sobre seu próprio harness
2. Identificar pontos fracos com evidência
3. Propor correções independentes
4. Comparar antes/depois
5. Entregar plug-and-play

### Fine-Tuning

Cada auditoria gera aprendizados que alimentam o fine-tuning:

1. **Padrão identificado** → registrar em MIX_MODE.md
2. **Anti-padrão detectado** → adicionar aos anti-padrões
3. **Correção aplicada** → verificar se funciona, documentar resultado
4. **Nova predição** → conectar com predições anteriores

### Frequência Recomendada

| Tipo | Frequência | Escopo |
|------|-----------|--------|
| Auto-auditoria leve | A cada 10 pipelines | Anti-padrões e redundâncias |
| Auto-auditoria completa | Mensal | 14 seções completas |
| Auditoria de framework externo | Ao absorver novo framework | Foco em Seções 1-4 |
| Fine-tuning de correções | Após aplicar correções | Foco em Seção 10 (antes/depois) |

---

**Versão:** 1.0.0
**Data:** 2026-07-27
**Origem:** autofagia de auditoria_gran_mestre_crossover.md
**Seções:** 14
**Padrões:** 12
**Anti-padrões:** 8
**Reutilizável:** Sim — para qualquer sistema
