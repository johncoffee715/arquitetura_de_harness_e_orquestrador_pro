# Execução da auditoria exaustiva opencode-dev (2026-08-25)

**Fonte:** `AUDITORIA-opencode-dev-2026-08-25.md` (pasta do projeto) · 6 frentes paralelas + correções

## O que foi feito
Fase 0 (topologia: sem .git próprio, repo macro /mnt/dados; bun instalado; typecheck baseline limpo) → frentes A–F → 4 correções implementadas + higiene, todas com evidência de teste.

## Correções aplicadas (97 testes verdes)
1. **CRÍTICA**: expansão `` !`cmd` `` de slash commands executava shell FORA do Permission.ask (`prompt.ts`) → gate `command_shell` default "ask" + regras do agente + rejeição limpa. Padrão Effect v4: operador é `Effect.catch` (não catchAll); throw em gen = defect.
2. move-session agora reseta Context Epoch (contrato CONTEXT.md:118) — função reset existia sem callers.
3. Storage failure do tool-output = lossy success (CONTEXT.md:194), não falha da tool.
4. Teto MAX_AUTO_COMPACTION_TRANSITIONS=5 na recursão pós-compaction (evita loop de custo infinito via defect-goto).

## Achados estruturais mais valiosos (para decisões futuras)
- **Tarball vendado client@1.17.13-v2** consumido por app/session-ui (46 pontos) contra repo 1.18.23 — CI valida o artefato errado. Migração = maior dívida ativa.
- Patch fff-bun morto (0.9.3 declarado × 0.9.4 no lock) prova que patches sobre dist/ caem silenciosamente → prevenir com CI de validação de patches.
- Lint não roda em nenhum workflow; 9 packages fora do turbo test.
- Plugins sem timeout = vetor de stall silencioso (sinergia com R9/R18 do harness).
- Veredito segurança .opencode/: CONDICIONAL-SIM (comando shell era o elo fraco — corrigido).

## Lições meta
- Testes upstream quebrados por correção de segurança = atualizar o teste para expressar o NOVO contrato (permission allow explícito no config do teste), nunca enfraquecer a correção.
- Sempre checar se a Interface tipada do serviço declara o canal de erro antes de adicionar effects que falham (Image.Error vs Permission Error conflitaram).
- Auditoria por frentes paralelas com retorno estruturado (fortes/fracos/causa raiz/cascata + arquivo:linha) produziu síntese direta sem retrabalho.
