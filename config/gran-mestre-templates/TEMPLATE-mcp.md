---
name: <slug-do-mcp>
# SEM campo `mode:` -- MCP nao e um agente do OpenCode, e uma conexao
# de servidor. Nao existe validacao subagent/primary/all pra isso.

type: remote                # remote | local
url: <endereco-se-remote>   # ex: http://127.0.0.1:8080/mcp
command: <comando-se-local> # ex: npx @some/mcp-server -- so um dos dois (url OU command)
timeout_ms: 300000

origin: gran-mestre-original
# ou: absorvido:<projeto-fonte>

requires: []
# dependencias de infraestrutura, ex: [docker], [ghidra-headless]
# Se requires nao estiver satisfeito, o CapabilityIndex nunca deve
# selecionar componentes que dependam deste MCP -- ver gap do
# open-notebook (dependia de Docker, falhava silenciosamente).

capabilities_exposed:
  - <tool-exposta-1>
  - <tool-exposta-2>

health_check:
  enabled: true
  on_failure: <acao -- ex: marcar unhealthy, tentar reconectar, bloquear chamada>
---

# MCP: <nome>

## O que expõe
<Lista objetiva das tools/capacidades que este MCP disponibiliza
 pro resto do sistema.>

## Dependências
<O que precisa estar rodando (Docker, processo headless, etc.)
 antes deste MCP funcionar. Seja explícito -- é exatamente a falta
 disso que causou o gap do open-notebook.>

## Comportamento em falha
<O que acontece se o MCP cair no meio de uma execução -- quem
 detecta (hook mcp-health-check), o que faz com tasks em andamento.>

## O que NÃO faz
- <limite explícito 1>
