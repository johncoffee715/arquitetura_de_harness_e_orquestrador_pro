# Spec — Botão On/Off ALL LLM (stack-toggle) — 2026-08-31

## Pedido do usuário (item 4 da revisão de pendências)
"Tornar on/off all LLM button" — o `stack-toggle.sh` deve funcionar como um botão
que liga/desliga TODOS os LLMs da stack (não apenas essenciais).

## Spec
- `stack-toggle.sh` (sem args) = botão on/off de TODA a stack:
  - Se TODOS os slots (ALL_PORTS: 8083 9084 9086 9088 9090 9092 9093 9095 + needles 8097 9091)
    estiverem UP → desliga TUDO (stop-all-models.sh sem args).
  - Senão → liga TUDO (start-stack.sh all).
- `is_stack_up()` deve checar ALL_PORTS (não só 8083/9084) — inverso da correção WARM
  (que limitava a essenciais). O botão é "all", o start padrão é WARM.
- Preservar: graceful-first (SIGTERM→10s→SIGKILL), lock cooperativo, idempotência,
  execução desanexada (R19).
- ⚠️ Dependência: `stop-all-models.sh` precisa estar corrigido (remover
  `pkill -f "llama-server"` global) ANTES de usar o botão — senão derruba o GM junto.

## Estado
- Pendente de implementação (aguardando autorização/outra sessão).
- Instruções base: `decisoes/2026-08-31-stack-warm-instrucoes.md` (passos 2-3).