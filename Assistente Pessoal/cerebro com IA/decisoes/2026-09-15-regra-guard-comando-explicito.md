---
setor: decisoes
tipo: regra-operacional
data: 2026-09-15
origem: ordem direta do usuario (sessao conclusao pendencias)
status: ativa
---

# Regra: guard-gap-p5 + comando explícito do usuário

**Gatilho:** usuário dá comando explícito (modo autônomo ou assistido). Invariante
revogada pela soberania do usuário: **é permitida escrita fora do workdir e
fora da governança (vault/config) sempre que o user solicitar.** O guard
NÃO deve proibir essa escrita; defasagem entre essa regra e o código do
plugin é defeito do plugin, a corrigir — nunca tratada como proibição.

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

## Soberania do usuário (cláusula suprema)

- **O usuário é a ÚNICA exceção a qualquer regra do harness.** Nenhuma regra,
  guard, doutrina ou convenção pode ser usada pelo agente para barrar a
  autonomia do usuário quando ele der uma ordem explícita.
- **Só o usuário revoga** esta cláusula — a qualquer momento, sem condição.
- Fundamento já registrado no decision-log: "[Authorize] SOBERANIA-USUARIO
  reiterada" (2026-09-09).

### Consequência operacional obrigatória do agente

Quando o guard bloquear fisicamente a tool call de uma ordem explícita do
usuário, o agente deve, NESTA ORDEM e sem sermão, sem adiamento:

1. Declarar o bloqueio em 1 linha (fato, não pedido de permissão).
2. Entregar IMEDIATAMENTE o comando exato pronto para o terminal do usuário
   (o terminal dele = as credenciais dele = a autonomia dele sem barreira).
3. OU, se o usuário preferir persistência, executar a mudança formal na
   governança (vault/config) que absolve o caso — com `[Authorize]
   SOBERANIA-USUARIO` registrado no decision-log.
4. Nunca reinterpretar a ordem como "pedido negado" e nunca propor alternativa
   que preserve o bloqueio como resposta final.

### Limite físico (não é exceção de regra, é arquitetura)

O plugin guard-gap-p5 bloqueia a tool call DO AGENTE; o agente não possui
credenciais separadas das do usuário. Portanto a autonomia soberana do usuário
se executa pelos canais 2 e 3 acima — nunca por "o agente ignora o plugin"
(tecnicamente inexistente). Isso não limita a soberania: é o meio pelo qual
ela flui.

### Consequência para o código do guard

A política canônica passa a ser: **permitir escrita fora do workdir/governança
sempre que o user solicitar**. O plugin `guard-gap-p5.ts` (e `guard-engine.ts`)
deve ser alinhado: bloqueio → auditoria (log + allow). Nota técnica registrada:
o plugin não distingue "ordem do user" de "iniciativa do agente" dentro da
sessão — portanto, na prática, essa classe de escrita vira allow-com-auditoria
(a trilha JSONL permanece como accountability). Deny real mantido apenas para
destrutivo sem ordem (rm -rf alheio, kill :8083, git reset --hard sem SHA).

## Caso originário

Escrita em `/mnt/dados/.gitignore` (raiz do repo, fora do workdir
`Assistente Pessoal/` e fora de vault/config) bloqueada 2× nesta sessão.
Correção aplicada: comando pronto entregue ao usuário (ver abaixo) +
`.gitignore` proposto documentado.
