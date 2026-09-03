# Mecânica de Ignição, Seleção e Refutação de Motores (memory-local skill)

## 1. Mecânica de Ignição (Iniciação)
- **Trigger**: início de sessão, início de task, mudança de contexto.
- **Model**: local-orchestrator/orchestrator (run_id: d9be2308-3a42-470b-9a75-d20254190f38)
- **Processo**: O orquestrador ignita o skill após a inicialização da sessão.
- **Entrada esperada**: run_id, run_id_task, contexto inicial do usuário.
- **Output esperado**: lista de memórias inicializadas (se houver contexto relevante).
- **Timeout**: 30 segundos após início de sessão.
- **Stop tokens**: ["\n\n", "```", "<|eot_id|>"]

## 2. Mecânica de Seleção (Seleção de contexto)
- **Trigger**: início de tarefa nova, mudança de contexto significativa.
- **Model**: local-orchestrator/orchestrator
- **Processo**: O orquestrador busca memórias relevantes usando:
  - Similaridade de embeddings (embedding) + filtro `target`.
  - Se nenhum for encontrado, retorna contexto vazio com instrução de recall.
- **Entrada esperada**: run_id, run_id_task, contexto atual (JSON).
- **Output esperado**: bloco `[MEMORY]` com até 3 top-3 memórias relevantes.
- **Limitação**: cada memória ≤ 1 linha; bloco ≤ 200 tokens.
- **TTL**: baseado em `scope` (global/per-conversa).

## 3. Mecânica de Refutação (Refutação de motores)
- **Propósito**: garantir que o modelo não gere conteúdo sensível ou fora de contexto.
- **Aplicação**: aplicada ao skill/hook que usa o skill memory-local.
- **Definição de falha**: qualquer saída que envolva:
  - Segredos/tokens/credenciais (regra global §6).
  - Embeddings externos (regra global §6).
  - Contexto poluído (janela excede limite).
  - Implementação duplicada ou anti-padrões (conformidade do gabarito).
- **Veredito categórico**: 
  - PASSOU_CATEGORICO: se o skill/hook passa o gabarito com ≥90% nota (R28).
  - NÃO_PASSOU: se o skill/hook falha veredito categórico (R28).
- **Evidência**: 
  - Gabarito.json (validado).
  - Runtime SKILL.md (frontmatter válido).
  - Conceito.md (ontologia) - já incluído no SKILL.md.
  - Gabarito.json - já criado.
  - Mecânica.md - já criado.
