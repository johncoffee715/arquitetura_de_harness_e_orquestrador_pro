# Diagnóstico 2026-08-24 — Config invalid + loop de tool calling

## Bug 1: Banner "config invalid - run doctor" (OpenCode 1.18.21)

**Sintoma:** TUI mostra paths `../../mnt/dados/openc...` ou `../../home/johncoffee...` dependendo do cwd de abertura (relativos ao project dir).

**Causa exata (medida):**
Na config *resolvida* (`opencode debug config`), as entradas MCP `obsidian` e `siz_delimiter` chegam como `{"enabled": true}` — SEM `type` — embora o opencode.json em disco esteja correto. O guard do core (`"type" in entry`, extraído do bundle) loga `Ignoring MCP config entry without type`.

**Workaround aplicado:** entradas removidas do `.mcp` → preservadas em `opencode/config/mcp-disabled-workaround-20260824.json`. Validado: 0 erros em processo fresco.

**Descartado com evidência:** JSON sintaxe · plugin npm OMO (bloqueado→idêntico) · duplicação global/project de fonte · mcp.json de skills (vazios) · opencode.db (histórico) · plugins file:// locais.
**Suspeito restante:** normalização do campo `enabled` no core 1.18.21.

## Bug 2: Loop infinito de tool calling
Modelo repetiu `ls "/mnt/dados/cerebro con IA/"` 27× após ENOENT idêntico (typo gerado, não copiado). Sem self-healing: modelo não lê stderr nem varia. Correção estrutural: circuit-breaker.ts (R18) — bloqueia 3ª tentativa idêntica.

## Ghidra :8080 — falso positivo
Porta CORRETA (ver ghidra_mcp_porta_8080_causa_raiz.md). WARN = serviço fechado.

Tags: gran-mestre, aprendizado, diagnostico, mcp, loop
