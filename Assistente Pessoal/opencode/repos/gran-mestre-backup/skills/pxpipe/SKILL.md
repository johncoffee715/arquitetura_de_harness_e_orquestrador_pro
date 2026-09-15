---
name: pxpipe
description: "Proxy local que reduz tokens de entrada do Claude Code renderizando contexto volumoso como imagens PNG. Economia de 59-70% em tokens de entrada."
model: opencode/gpt-5-nano
mode: skill
origin: gran-mestre-original
metadata:
  category: optimization
  version: 1.0.0
  author: Gran-Mestre
  source: https://github.com/teamchong/pxpipe
---

# pxpipe — Redutor de Tokens de Entrada

## Quando usar

1. **Sessões longas** — Quando o contexto acumula muitas tool calls e history
2. **System prompts grandes** — Quando há muitas skills e tools documentadas
3. **Custo elevado** — Quando o custo de tokens está alto

## Comandos

```
/pxpipe start              - Inicia o proxy na porta 47821
/pxpipe stop               - Para o proxy
/pxpipe status             - Mostra status e economia
/pxpipe export <dir>       - Exporta diretório como PNGs (sem proxy)
```

## Como usar

```bash
# Iniciar proxy
npx pxpipe-proxy

# Apontar Claude Code
ANTHROPIC_BASE_URL=http://127.0.0.1:47821 claude
```

## Token Economics

| Conteúdo | Como Texto | Como Imagem | Redução |
|----------|------------|-------------|---------|
| System prompt (48k chars) | ~25k tokens | ~2.7k tokens | 89% |
| Tool docs | ~10k tokens | ~1.5k tokens | 85% |
| History | ~20k tokens | ~3k tokens | 85% |

## Limitações

- **É lossy** — Strings hex de 12 chars podem ser perdidas
- **Escape hatch** — Subagents em modelos não-allowlisted passam como texto
- **Dependente do cliente** — Savings dependem do cliente reenviar como texto