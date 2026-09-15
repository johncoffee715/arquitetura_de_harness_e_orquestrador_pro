# Análise do Padrão de Desenvolvimento (extraído do dashi-ppt-skill)

## Padrão de Validação Multi-Estágio (Extraído do dashi-ppt-skill)

Inspirado no padrão `validate:goal-spec → validate:swiss → validate:goal-copy` do dashi-ppt-skill, nosso pipeline de cascata usa validação em **3 camadas** por fase:

```
Camada 1 — Spec/Plano Validation (Héstia)
  → Valida contra o pedido original (requisitos, escopo, contratos)
  → Estado: APPROVED / NEEDS_CORRECTION / BLOCKED

Camada 2 — Implementation Validation (Code Reviewer micro)
  → Valida código contra o spec/plano (TDD, padrões, segurança)
  → Estado: PASS / FIX_NEEDED / REJECT

Camada 3 — Holistic Validation (Atena macro + Verification)
  → Valida coerência cross-task, integração, entrega final
  → Estado: DELIVERED / ROLLBACK / ESCALATE
```

**Estados explícitos de aceitação** (aplicáveis a qualquer fase):
- `APPROVED` / `NEEDS_CORRECTION` / `BLOCKED` — aceitação de camada 1
- `PASS` / `FIX_NEEDED` / `REJECT` — aceitação de camada 2
- `DELIVERED` / `ROLLBACK` / `ESCALATE` — aceitação de camada 3

## Padrão de Projeto (Extraído do dashi-ppt-skill)

### Filtros Mágicos (multifacetados e personalizados)

- `props:safe` — substitui modelos predefinidos por props geradas de um modelo específico, aplica qualquer regra de correção e lembra as propriedades editadas para a próxima renderização (máximo 2 travamentos por solicitação)
- `props:safe -- --goal <file> --write` — escreve as props geradas por `props:safe` no arquivo goal

- `validate:swiss` — plataforma do dashi-ppt-skill para validação de projeto. Lê o arquivo objetivo (`goal.json`) via `path-resolve` e executa fins `validate:goal-copy` (verifica se todos os requisitos atuais estão finalizados), `validate:goal-spec` (verifica se o objeto JSON se encaixa no schema)

- `goal:scaffold` — método usado antes da primeira renderização de um deck

- `goal:fill-plan` — método usado quando a edição de um deck já foi iniciada e `goal.json` original existe, apenas `goal.fillPlan.json` ainda não está finalizado.

## Padrão de Trabalho (Extraído do dashi-ppt-skill)

### Preservação Colaborativa de Ideias

O sistema de branch e worktree do OpenCode não aborda a separação de responsabilidades.

Um diagrama de rede mostra que nosso sistema é composto por vários nós de agentes, com níveis de confiança, baseado em mensagens, autenticadas por criptografia de chave pública, onde cada nó pode agir como um cliente e um servidor.

Ao comparar com um modelo mental, vemos um nível de abstração adicional: o *diretório do projeto*. Então, devemos decidir por um destes modelos mentais para o sistema embasado em nós:

- O modelo de arquivo do OpenCode (países dentro de um diretório)
- O modelo de rede (sub-redes interconectadas)
- O modelo de arvore do trabalho (árvore principal, worktree)

### Hiperlinks (Introdução)

O repositório, o diretório do projeto e o arquivo do agente estão no mesmo nível. Nós podemos mover um deles:

- De todas as sessões de agente: mover [session-manager](https://github.com/jongyeol/opencode-session-manager) para o horizonte (extensão)
- Oferecer a opção para o agente de todas as sessões de agente. Definir os limites. Possivelmente ter várias outras resoluções
- Fornecer um caminho mais claro para os usuários, mostrando a relevância do agente do projeto. Atalho de interface para os usuários. Permitir editor entre os nós do agente do projeto.

### Hiperlinks (Página de Introdução)

O repositório, o diretório do projeto e o arquivo do agente estão no mesmo nível.

O nível de abstração seguinte é um *conjunto de agente*. Ao invés de nós de agentes, temos conjuntos.
