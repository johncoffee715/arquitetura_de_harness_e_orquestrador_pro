---
name: gemini-mcp-tool
description: "MCP server que dá ao agente acesso ao Gemini CLI / Antigravity CLI (agy) — janela massiva para análise de arquivos/codebases grandes e brainstorm em 3 vozes. (absorvido de jamubc/gemini-mcp-tool). Aviso: Gemini CLI foi aposentado em 2026-06-18; backend padrão agora é agy."
user-invocable: true
allowed-tools: "Read Bash"
metadata:
  version: "1.0.0"
  origin: "https://github.com/jamubc/gemini-mcp-tool (MIT — not.assertion)"
  absorbed_at: "2026-08-05"
  antropofagia: "Devorada a ponte MCP→Gemini/agy para dialetos massivos de contexto, absorvida para o harness OpenCode como camada de deep-context externa opcional — complemento à memória Obsidian e aos modelos locais Nanbeige/LFM."
---

# ✨ gemini-mcp-tool — Skill de Deep-Context Externo

## Origem (Antropofagia Tecnológica)

Esta skill é o resultado da **antropofagia tecnológica** do repositório
[`jamubc/gemini-mcp-tool`](https://github.com/jamubc/gemini-mcp-tool) (2.269★, MIT declarado):

| Componente Original | O que absorvemos | Como adaptamos |
|--------------------|-----------------|----------------|
| MCP server (stdio) | Ponte Cliente IA ⇄ Gemini CLI | Servidor MCP opcional do harness |
| Gemini CLI backend | Token window massiva (1M+) | Análise de arquivos/codebase grandes |
| `@` syntax direction | Direcionar arquivos p/ Gemini | Passagem de arquivos por contexto |
| 3-person party | Brainstorm multi-IA | Alternativa ao Dev Loop brainstorm |
| Antigravity CLI (agy) | Sucessor pós-2026-06-18 | Backend padrão (migration automática) |

## O Que Esta Skill Faz

- 📄 **Análise de arquivos grandes**: jogar um arquivo/codebase todo em Gemini/agy via `@caminho`
- 🧠 **Brainstorming em 3 vozes**: Cliente IA + Gemini (+ opcional mais um) 
- 🔍 **Perguntas naturais**: "por que x é lento?" direto ao Gemini CLI
- 🧾 **Economia de contexto**: delega para a nuvem grandes leituras, economizando a janela do orquestrador

## Pré-requisitos

1. Node.js ≥ 16
2. **Antigravity CLI** (`agy`), instalando se ausente:

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
agy  # rodar uma vez para login
```

3. (Opcional) manter Gemini CLI para users enterprise: `export GEMINI_MCP_BACKEND=gemini`

## Instalação (OpenCode)

Adicione ao `opencode.json`:

```json
{
  "mcpServers": {
    "gemini-cli": {
      "command": "npx",
      "args": ["-y", "gemini-mcp-tool"]
    }
  }
}
```

Verificar: `/mcp` (OpenCode: `mcpServers` listado e ativo).

## Playbook de Uso

```bash
# EXEMPLO 1 — analisar arquivo grande (via a IA + @caminho)
# no cliente do agente, chame a tool gemini-cli perguntando:
#   "Analise src/core/harness.py e me diga o que me parece 'circuit_breaker' — @src/core/harness.py"

# EXEMPLO 2 — brainstorm de arquitetura (3 vozes)
#   "Faça um brainstorm em 3 vozes sobre melhor estratégia para hot-swap assíncrono de modelos com foco em VRAM engajante"
```

## Integração com o Harness

- **Quando usar**: tasks com arquivos/codebase grandes, hardware local com janela pequena,
  documentação extensa (ex: ∫ão de arquitetura), ou brainstorm multi-vozes.
- **Quando NÃO usar**: tasks triviais (R1/R2) — é overhead. Local/knowledge: para isso existem
  agent-reach/webfetch/firecrawl.
- **Recurso local vs MCP**: MCP/CLI Gemini é **recomendado opcional** — não substitui a
  espinha local Ornith/Nanbeige/LFM; é camada de deep-context sob demanda (padrão Model Provider).

## Avisos

- **Gemini CLI aposentado 2026-06-18** — para free/AI Pro/AI Ultra, o backend agora é `agy`
  automaticamente; `GEMINI_MCP_BACKEND=gemini` só para licença pagante enterprise/Standard.
- `agy` backend é experimental (Flash-only print mode, transcript fallback, tool-run não-sandbox).
- Não instalar se não houver CLI Gemini/agy no host (degrade silencioso).