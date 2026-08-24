# Contexto Atual — Pipeline State
**Data:** 2026-08-02
**Sessão:** Inventário do Ecossistema OpenCode

## Estado
- Inventário completo gerado e salvo em `/home/johncoffee/INVENTARIO_ECOSISTEMA.md`
- 61 subagents catalogados (Pipeline, Crossover, GSD, OpenCode)
- 13 skills + 50+ comandos GSD documentados
- 2 MCPs (Ghidra SSE com erro de conexão, Context7 OK)
- 5 LSPs instalados (typescript, basedpyright, rust, clangd, deno)
- 20 hooks GSD documentados

## Problemas Identificados
1. **Ghidra MCP** — Servidor não escuta na porta 8080. Extensão precisa ser ativada no Ghidra (File → Configure → GhidraMCP)
2. **OpenWork** — Precisa de token OAuth. Config atual tem `oauth: {}` vazio
3. **gopls** — Go não instalado no sistema

## Ações Realizadas
- [x] Inventário completo gerado e salvo
- [x] typescript-language-server instalado (v5.3.0)
- [x] basedpyright instalado (v1.39.9)
- [x] Decisões de instalação LSP registradas (typescript, basedpyright, gopls)

## Pendências
- [ ] Ativar GhidraMCP no Ghidra
- [ ] Configurar token OpenWork
- [ ] Instalar Go para gopls

## Contexto Relevante
- Usuário: John Coffee
- Projetos ativos: BIOS UEFI modding (Jingsha X99-D8), Inferência Local (MI50)
- Vault Obsidian: `/mnt/dados/cerebro com IA/`
