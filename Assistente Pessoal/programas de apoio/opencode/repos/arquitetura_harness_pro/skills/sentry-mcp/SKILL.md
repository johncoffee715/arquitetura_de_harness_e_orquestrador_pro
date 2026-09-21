---
name: sentry-mcp
description: "MCP remoto do Sentry (mcp.sentry.dev) — debugging orientado a anotadores de código: erros, issues, traces, performance. absorvido de getsentry/sentry-mcp; middleware remoto p/ o fluxo dev workflow (human-in-the-loop)."
---

# 🐞 sentry-mcp — Skill de Erros de Produção para OpenCode

## Origem (Antropofagia Tecnológica)

Esta skill é o resultado da **antropofagia tecnológica** do serviço/repo
[`getsentry/sentry-mcp`](https://github.com/getsentry/sentry-mcp) (805★)
e o endpoint remote [`https://mcp.sentry.dev/mcp`](https://mcp.sentry.dev/mcp):

| Componente Original | O que absorvemos | Como adaptamos |
|--------------------|-----------------|----------------|
| Remote MCP (Cloudflare) | MCP como middleware no endpoint central | Card MCP remoto no registry do harness |
| Issues/Trace/Perf tools | Debug de erros/eventos | Review/QA de erros de produção |
| Human-in-the-loop | Priorização DX | Uso em F5/F6 com supervisão humana |
| AI search tools | `search_events`/`search_issues` | Requer provider LLM (opcional) |

## O Que Esta Skill Faz

- 🐞 **Localizar erro**: consultar um erro específico num projeto Sentry
- 🔍 **Search por issues/events**: traduz perguntas em not lógico (requer LLM provider, senão tools base data)
- 📖 **Leitura de stacktrace/trace**: contexto de trace spans para debug
- 📈 **Performance**: busca de perf/anomalias

## Configuração (OpenCode)

Obs.: substituir `***` pelo token do usuário (org:read etc.) e project scope.

```json
{
  "mcpServers": {
    "sentry": {
      "type": "remote",
      "url": "https://mcp.sentry.dev/mcp"
    }
  }
}
```

Ou stdio (self-hosted):

```bash
npx @sentry/mcp-server@latest --access-token=sentry-user-token
# Scopes: org:read project:read project:write team:read team:write event:write
# --host para Sentry self-hosted (ex.: --host=sentry.example.com)
```

## Playbook

1. **Contexto**: veja como o erro aparece no projeto Sentry (issue title, fingerprint).
2. **Consulte via MCP**: tool `get_issue`/`search_issues`/`search_events` (conforme cards ativos).
3. **Trace → mapa**: se houver trace, siga o span problemático e acrescente ao diagnóstico.
4. **Loop de correção**: volte ao harness com a evidência (R14 ciclo de reparo).

## Integração com o Harness

- **Fase 5 (Revisão macro)**: quando o diff causa erro de produção (bug report), use sentry-mcp
  para localizar o erro do novo merge.
- **Gate de qualidade**: "existe erro novo no Sentry? aumenta? p99?" — evidência de impacta a
  verofisto de conformidade (Fase 6).
- **Ops/QA contínuo**: rodada de checagem de erros no release.

## Avisos

- Tools de IA (`search_events`, `search_issues`) exigem LLM provider configurado
  (OpenAI/Azure/Anthropic/OpenRouter) — sem isto, só dados (read/get).
- **Requer token/org**, não há modo anônimo.
- A importação de cartão + hates sem credencial real é um jumper — first run sem token irá
  marcar `enabled:false` no diagnóstico.