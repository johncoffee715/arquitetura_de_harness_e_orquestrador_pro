---
tags: [decisao, harness, reinstalacao, opencode, autofagia]
data: 2026-08-25
---

# Decisão — Reinstalação limpa do harness OpenCode (2026-08-25)

## Contexto
A instalação antiga quebrou em cascata quando `/mnt/dados/opencode/` foi apagado: o
`PORTABLE_BOOTSTRAP.sh` criava 10 symlinks de `$HOME` para essa pasta (config, cache,
data, state, .opencode, .claude, .omo, .bun, mem). Além disso, `/usr/local/bin/opencode`
era um symlink morto para `/mnt/usb/` que sombrava o PATH, e o `opencode.jsonc` do
Ventoy tinha caminhos hardcoded com `/run/media/liveuser/`.

## Auditoria (resumo)
- 12 vestígios eliminados: pacote pacman `local/opencode`, symlink fantasma do PATH,
  8 symlinks mortos em `$HOME`, 2 dirs reais (`~/.local/share/opencode`,
  `~/.local/state/opencode`), 54MB de cache órfão, entradas mortas no fish.
- Regras globais canônicas (R1–R50) RECUPERADAS do repo público
  `johncoffee715/arquitetura_de_harness_e_orquestrador_pro` → `config/rules/AGENTS.md`.
- `data/auth.json` estava exposto em repo PÚBLICO no GitHub → decisão: rotacionar chaves.

## Decisões tomadas
1. **Nova arquitetura**: instalação autônoma em `/mnt/dados/Assistente Pessoal/opencode/`
   com wrapper que calcula ROOT dinamicamente e redireciona XDG (config/data/state/cache).
   Zero symlinks no `$HOME`, zero caminhos hardcoded — imune ao modo de falha antigo.
2. **Binário v1.18.23** (upstream, SHA-256 verificado contra a release) também aplicado
   ao portátil do Ventoy (backup v1.18.9 preservado como `.bak-v1.18.9`).
3. **AGENTS.md global restaurado** de `config/rules/AGENTS.md` com paths corrigidos
   (vault agora em `Assistente Pessoal/cerebro com IA`) + nota de STATUS DE ATIVAÇÃO:
   arsenal de orquestração (registry, GSD, hooks, skills helenizadas) fica ARQUIVADO
   nos sparse-clones `repos/arquitetura_harness_pro/` e `repos/gran-mestre-backup/`
   até a Fase 2 do harness.
4. **Guardrails de permissão** no opencode.jsonc: sudo/push/shutdown pedem aprovação;
   rm -rf /, mkfs, dd of=/dev/, force-push NEGADOS; auth.json/.env/pem/key negados p/ leitura.
5. superpowers / agent-skills / agent-reach NÃO entram na nova instalação — servem só
   de apoio durante sessões de trabalho (decisão explícita do usuário).

## Pendências registradas
- [ ] Usuário: rotacionar as chaves API expostas (`data/auth.json` público)
- [ ] Purgar `auth.json` do histórico git do repo público (requer force-push)
- [ ] Corrigir caminhos desatualizados dentro do vault (AGENTS.md do vault, hot.md congelado em 27 dias)
- [ ] VSCode: extensão `sst-dev.opencode-0.0.13` é publisher antigo — atualizar
- [ ] `gh auth login` + `opencode auth login` (credenciais do zero)

## Referências
- [[../projeto opencode/harness/AUDITORIA-MIGRACAO-2026-08-25]] (relatório completo fora do vault)
- Backup da migração: `Assistente Pessoal/projeto opencode/harness/backup-2026-08-25/`
