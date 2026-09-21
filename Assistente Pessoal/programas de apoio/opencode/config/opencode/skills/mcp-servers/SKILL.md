---
name: mcp-servers
description: MCP reference catalog — Everything/Fetch/Filesystem/Git/Memory/Sequential-Thinking/Time + safe client-config contract.
category: skill
model: local-forge/proposer
---

# mcp-servers

Catálogo de referência dos MCP servers oficiais (steering group): o que cada um faz,
quando usar, como configurar o client com segurança. Helenizado de
`modelcontextprotocol/servers` (origem: https://github.com/modelcontextprotocol/servers).

> Irmãs no catálogo: `sentry-mcp`, `gemini-mcp-tool`, `openwork-mcp`, `firecrawl`.
> Aqui o FOCO é o catálogo de referência + contrato de config segura.

## Quando usar

- Precisar de filesystem/git/memory/fetch/time/sequential-thinking via MCP
- Configurar um client MCP (Claude Desktop e afins) sem adivinhar comandos
- Avaliar se um server serve (referência educacional, NÃO produção sem hardening)

## Catálogo (7 ativos)

| Server | Uso | Start |
|---|---|---|
| Everything | referência/teste (prompts+resources+tools) | npx -y @modelcontextprotocol/server-everything |
| Fetch | fetch web p/ LLM | npx -y @modelcontextprotocol/server-fetch |
| Filesystem | arquivos com access control | npx -y @modelcontextprotocol/server-filesystem /allowed/dir |
| Git | ler/buscar/manipular repos | uvx mcp-server-git |
| Memory | knowledge-graph persistente | npx -y @modelcontextprotocol/server-memory |
| Sequential-Thinking | problem-solving reflexivo | npx -y @modelcontextprotocol/server-sequential-thinking |
| Time | timezone/conversão | npx -y @modelcontextprotocol/server-time |

Arquivados (fora do core, buscar no `servers-archived`): postgres, redis, sqlite, sentry, slack, github, gitlab, gdrive, maps, puppeteer, brave-search, everart.

## Princípio

Referência ≠ produção: avaliar threat model próprio antes de expor. Secrets sempre via `env`, nunca no comando.
