# Autofagia: OpenWork — Executor-Deep

**Data:** 2026-08-03 (Rodada 8 — 26 alvos)
**Fonte:** https://github.com/different-ai/openwork (21k★) — `.opencode/agents/executor-deep.md`
**Objetivo:** Absorver **contrato orquestrador→executor** de raciocínio profundo (alt. de Claude Cowork, powered by opencode)

---

## 1. O que é

OpenWork é a alternativa open-source ao Claude Cowork, **construída sobre opencode** (usa `.opencode/agents/`). O `executor-deep` é o executor de raciocínio máximo (variant xhigh) invocado pelo orquestrador para features multi-arquivo, refactors ou após 2 reparos falhos do executor padrão.

## 2. Padrões absorvidos

- **Split orquestrador/executor inegociável**: orquestrador pensa + verifica; executor só implementa
- **Brief com contrato**: Goal · Files (path:line) · Constraints · Acceptance · Verify — com pointers, não colagens
- **Verificação estreita**: check mais rápido que cobre a mudança; nunca build repo-wide sem pedido
- **Relatório delta**: ≤30 linhas (files changed, comandos + exit codes, o que foi pulado/assumido)
- **Loop de reparo**: retomar `task_id` mesmo só com o output que falhou; máx. 2 rodadas, depois escalar e re-decompor (nunca ping-pong)
- **Paralelismo**: tasks independentes lançam múltiplos executors em paralelo sem sobrepor arquivos

## 3. Helenização

- Instalado: `~/.config/opencode/agents/executor-deep.md` (subagent, origem `absorvido:different-ai/openwork`)
- Papel no Gran-Mestre: reforça o split supervisor/worker (Atlas→Implementer) com o contrato de brief e o relatório delta

## 4. Aprendizado

O verbo "narração demo-driven" (worktree fresh + spec app-driving `testkit` + tape de evidência) é um padrão a considerar para o pipeline de execução de features.
