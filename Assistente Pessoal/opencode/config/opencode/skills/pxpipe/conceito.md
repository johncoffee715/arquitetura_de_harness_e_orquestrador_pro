# pxpipe — Ontologia de Persona

## Conceito

pxpipe é um proxy local que reduz tokens de entrada do Claude Code. Ele:
- Reduz tokens de entrada por meio de renderização de contexto volumoso como imagens PNG
- Economiza tokens através de conversão de texto para imagens
- É ideal para sessões longas, prompts grandes e custos elevados de tokens

## Persona

- **Nome**: pxpipe-agent
- **Tipo**: Proxy/Tool
- **Função**: Reduz tokens de entrada via imagens
- **Capacidades**: 
  - Inicia proxy na porta 47821
  - Para o proxy
  - Mostra status e economia
  - Exporta diretório como PNGs (sem proxy)
- **Limitações**:
  - É lossy (perde strings hex de 12 chars)
  - Escape hatch (subagents em modelos não-allowlisted passam como texto)
  - Dependente do cliente (savings dependem do cliente reenviar como texto)

## Exemplo de uso

```bash
# Iniciar proxy
npx pxpipe-proxy

# Apontar Claude Code
ANTHROPIC_BASE_URL=http://127.0.0.1:47821 claude
```
