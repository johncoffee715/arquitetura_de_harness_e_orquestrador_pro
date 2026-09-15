# Task Plan: Autofagia do Gran-Mestre

## Goal
Aplicar a metodologia `planning-with-files` (OthmanAdi, v3.7.0) ao próprio Gran-Mestre — identificar gaps, implementar melhorias e fechar o ciclo de autofagia (dogfooding).

## Current Phase
Phase 4 — Documentar Protocolos

## Phases

### Phase 1: Pesquisa e Análise Comparativa ✅
- [x] Fetch README, SKILL.md, templates, quickstart do planning-with-files
- [x] Fetch template task_plan.md, findings.md, progress.md
- [x] Extrair lista de inovações vs GSD atual
- [x] Documentar gaps no findings.md
- **Status:** complete

### Phase 2: Criar Estrutura de Autofagia ✅
- [x] Criar .planning/autofagia/ com task_plan.md, findings.md, progress.md
- [x] Documentar comparação GSD vs PWF
- [x] Instalar skill planning-with-files oficialmente (se compatível)
- [x] Mapear quais inovações implementar vs quais ignorar
- **Status:** complete

### Phase 3: Implementar Gaps Prioritários ✅
- [x] **Criar SKILL.md do Gran-Mestre** (gap crítico — arquivo ausente)
- [x] **Implementar Attestation** (SHA-256 nos PLAN.md + verificação em hooks)
- [x] **Implementar Completion Gate** (verificar plano completo no Stop hook)
- [x] **Criar findings.md dedicado** para cada fase
- [x] **Implementar Ledger** (JSONL append-only para rastreamento)
- **Status:** complete

### Phase 4: Documentar Protocolos ✅
- [x] Atualizar agent/gran-mestre.md com novos protocolos
- [x] Adicionar 2-Action Rule e 3-Strike Protocol
- [x] Atualizar SKILL.md com referências a attestation/completion gate
- [x] Criar docs/autofagia.md com documentação completa
- **Status:** complete

### Phase 5: Testar Ciclo Completo
- [ ] Rodar `/gran-mestre` com uma tarefa real usando a nova estrutura
- [ ] Verificar completion gate funcionando
- [ ] Verificar attestation
- [ ] Verificar findings.md sendo populado
- **Status:** pending

### Phase 6: Reportar Resultados ✅
- [x] Relatório final da autofagia
- [ ] Recomendações de follow-up
- **Status:** complete

## Key Questions
1. Quais inovações do planning-with-files são aplicáveis ao Gran-Mestre?
2. Quais já existem no GSD mas com nomes diferentes?
3. O completion gate é compatível com o modelo de hooks do OpenCode?
4. Vale a pena instalar o planning-with-files como skill separada ou incorporar as ideias?

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| Usar diretório .planning/ autofagia/ | Isolado do .planning/ GSD existente, segue padrão PWF de planos escoped |
| Priorizar SKILL.md, attestation, completion gate | São os 3 maiores gaps; os outros são incrementais |
| Incorporar ideias vs instalar skill separada | Incorporar é mais limpo para o Gran-Mestre; instalar PWF adicionaria hooks conflitantes |
| Integrar conceitos do AAS | Agent-first control plane, specialized plugins, stack validation |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|

## Notes
- planning-with-files v3.7.0: 25.6k stars, benchmark 96.7% pass rate
- SKILL.md do Gran-Mestre criado em `~/.opencode/skills/gran-mestre/SKILL.md`
- Scripts attestation e completion gate criados em `/home/johncoffee/scripts/`
- GSD já tem PLAN.md, CONTEXT.md, ROADMAP.md — evoluído com novos protocolos