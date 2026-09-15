---
setor: decisoes
tipo: regra-operacional
data: 2026-09-15
origem: ordem direta do usuario (sessao conclusao pendencias)
status: ativa
---

# Regra: guard-gap-p5 + comando explícito do usuário

**Gatilho:** usuário dá comando explícito (modo autônomo ou assistido) e o guard
bloqueia escrita fora do workdir / fora da governança (vault/config).

## Procedimento obrigatório do agente

1. **Reverter**: desfazer/abortar a tentativa bloqueada imediatamente (nada fica
   aplicado "pela metade").
2. **Corrigir a causa raiz**: o path legítimo precisa entrar na governança —
   ajustar whitelist/config do guard (vault/config é caminho permitido) ou mover
   o artefato para caminho permitido. Correção é formal e auditada, com
   `[Authorize] ordem direta do usuario` registrado no decision-log.
3. **Reexecutar** com a autorização registrada, e logar o evento no
   `decision-log.jsonl` + nota em `decisoes/`.
4. **Alternativa equivalente de autoridade**: entregar ao usuário o comando
   exato pronto para colar no terminal dele (a sessão shell dele é a execução
   com as credenciais dele — o agente não possui credenciais separadas).

## Limite explícito (recusado nesta mesma sessão)

- ❌ NÃO criar "regra universal de bypass": contornar sistematicamente o guard
  em qualquer bloqueio futuro apaga a função fail-closed da camada 2.
- ❌ NÃO usar credenciais do usuário como mecanismo de evasão por agente —
  não existem credenciais separadas disponíveis ao agente; a autoridade do
  usuário se exerce **pela alteração formal da config** (governança) ou **pela
  execução no terminal dele**.
- Ressalva registrada por decisão narrada do usuário nesta data; se a soberania
  do usuário quiser a forma integral (bypass universal), o caminho formal é
  editar `plugins/guard-gap-p5.ts` / `scripts/guard-engine.ts` por ordem
  explícita pontual — nunca como automático permanente.

## Caso originário

Escrita em `/mnt/dados/.gitignore` (raiz do repo, fora do workdir
`Assistente Pessoal/` e fora de vault/config) bloqueada 2× nesta sessão.
Correção aplicada: comando pronto entregue ao usuário (ver abaixo) +
`.gitignore` proposto documentado.
