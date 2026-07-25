# /gran-mestre — Executa pipeline completo de orquestração

Executa o pipeline Gran-Mestre. A rota é detectada automaticamente:

## Pipeline Padrão (requisito claro: fix, refactor, escopo fechado)
1. **Prometheus** — Planejar (PLAN.md)
2. **Héstia** — Validar plano
3. **Atlas** — Executar
4. **Atena** — Revisar código
5. **Héstia** — Validar entrega
6. **Relatório final** ao usuário
## Pipeline em Cascata — rota FEATURE (feature nova, design em aberto)

Gran-Mestre ⚡ Superpowers intercalados em zíper, dupla validação por estágio:

1. **DESCOBERTA** — Prometheus (decomposição leve) >>> Brainstorming (diálogo, 2-3 abordagens) — ⏸️ GATE 1
2. **CONTRATO** — Spec Writer >>> Héstia valida (filtro 1) — ⏸️ GATE 2
3. **PLANO** — Plan Writer (TDD, bite-sized) >>> Héstia valida — ⏸️ GATE 3 + 💾 SHA salvo
4. **EXECUÇÃO** — Atlas (supervisor: git/sequenciamento) >>> Implementer (operário: TDD/task) → Code Reviewer (micro/task) — ⚡ sem gates
5. **REVISÃO MACRO** — Atena (diff total, coerência cross-task)
6. **ENTREGA** — Verification (evidência de ferro) >>> Héstia (filtro 1) — ⏸️ GATE 4 + relatório

## Modos de Gate (rota FEATURE)

| Modo | Comportamento |
|---|---|
| `A` interativo (default) | 4 gates: direção → spec → plano → entrega |
| `C` autonomo | Héstia é proxy de aprovação; só escala ao usuário se reprovar 2x. Ativar com: "autônomo", "sem gates", "modo noturno" |

## Uso

```
/gran-mestre [descrição da tarefa]
/gran-mestre autônomo [descrição da feature]   ← cascata modo C
```

## Regras

- **Safety protocol**: SHA salvo antes de execução (fim da Fase 3 na cascata)
- **Rollback**: automático se pipeline falhar; máximo 1 por pipeline
  - Na cascata: rollback só se o pipeline INTEIRO falhar — falha de task individual é corrigida no loop Implementer
- **Escalonamento**: CRITICAL/FEATURE com 2 falhas locais → nuvem (oc/tllm → opencode-go/kimi-k3 → opencode-zen), sempre registrado
- **Divisão inegociável**: Atlas nunca escreve código na cascata; Implementer nunca gerencia a branch
- **Relatório final**: o que foi feito, arquivos alterados, testes, avisos, follow-ups

## Padrão de Análise (extraído do dashi-ppt-skill)

O pipeline de validação multi-estágio:

- **Camada 1 (Héstia)**: Valida contra pedido original (especificações, escopo, contratos)
- **Camada 2 (Code Reviewer micro)**: Valida código contra spec/plano (TDD, padrões, segurança)
- **Camada 3 (Atena/Verification)**: Valida coerência cross-task, integração, entrega final

Explicitação de `Approval State`: 
  `APPROVED` / `NEEDS_CORRECTION` / `BLOCKED` / `DELIVERED` / `ROLLBACK`

## Observação

Antes de delegar ao Atlas, verificar:
1. PLAN.md existe? Se não → criar via Prometheus primeiro
2. PLAN.md tem ≥1 fase com acceptance criteria?
3. PLAN.md tem ≥1 task por fase?
4. Dependências listadas (se houver)?
5. Attestation SHA-256 confere?
6. Se plano incompleto → voltar ao Prometheus

Veja também:
- `GRAN_MESTRE.md` no registry — manifesto completo (cascata, modelos, escalonamento)
