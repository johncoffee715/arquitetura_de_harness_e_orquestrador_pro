---
name: context7-skill
description: Up-to-date library docs via Context7 REST (no MCP overhead) — resolve library ID, then fetch docs with topic focus.
category: skill
model: local-thalamus/ingestor
---

# context7-skill

Fetch live library documentation through the Context7 REST API without persistent MCP context cost.
Helenizado de `netresearch/context7-skill` (origem: https://github.com/netresearch/context7-skill).

## Quando usar

- "how do I use [library]?" / "[library] documentation" / "show me [library] patterns"
- Antes de gerar código contra lib com API volátil (React, Next.js, Vue, Express, Prisma, +50)
- Quando o MCP Context7 não estiver configurado ou o custo de contexto precisar ficar ~100 tokens sob demanda

## Como usar

1. **Resolver o ID**: `scripts/context7.sh search "prisma"` → `/prisma/prisma`
2. **Buscar docs com tópico**: `scripts/context7.sh docs "/prisma/prisma" "queries"`
3. Foco via tópico (hooks, routing, middleware) para reduzir ruído

## Princípio

REST direto, sem schemas de tool no contexto. MCP Context7 custa ~500–2000 tokens sempre;
esta skill custa ~100 tokens somente quando invocada. `CONTEXT7_API_KEY` opcional (rate limits maiores).
