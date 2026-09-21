# Task Plan: Autofagia do ECC (affaan-m/ECC)

## Goal
Aplicar autofagia (self-digestion/self-improvement) ao repositório ECC — identificar gaps na arquitetura de hooks, agents e skills comparando com Gran-Mestre + planning-with-files + Claude-Mem, propondo melhorias e implementando integração cross-harness.

## Metadata
- **Repo:** https://github.com/affaan-m/ECC
- **Stars:** 230K
- **License:** MIT
- **Linguagem:** JavaScript (54%) / TypeScript (43%) / Shell (3%)
- **Último release:** v2.0.0
- **Agentes:** 67 especializados
- **Skills:** 261+ workflows
- **Hooks:** 30+ lifecycle hooks (SessionStart, PreToolUse, PostToolUse, Stop)
- **Harnesses suportados:** Claude Code, Codex, Cursor, OpenCode, Gemini, Zed, GitHub Copilot

## Current Phase
COMPLETE — Todas as 6 fases concluidas

## Phases

### Phase 1: Pesquisa e Análise Comparativa ✅
- [x] Mapear estrutura completa do ECC (agents/, skills/, hooks/, rules/, commands/)
- [x] Identificar arquitetura cross-harness e adapters
- [x] Extrair inovações do ECC vs Gran-Mestre vs planning-with-files
- [x] Documentar gaps no findings.md
- **Status:** complete

### Phase 2: Mapear Gaps de Autofagia ✅
- [x] Identificar falta de Attestation (SHA-256 para planos)
- [x] Identificar falta de Completion Gate
- [x] Identificar falta de 2-Action Rule e 3-Strike Protocol
- [x] Identificar lacunas no continuous-learning v2 vs Claude-Mem
- [x] Mapear oportunidades de integração cross-harness
- **Status:** complete

### Phase 3: Propor Melhorias ✅
- [x] Desenhar sistema de Attestation para ECC plans
- [x] Desenhar Completion Gate para ECC hooks
- [x] Propor 2-Action Rule para session-start hooks
- [x] Propor integração com Claude-Mem como memória cross-harness
- **Status:** complete

### Phase 4: Implementar Scripts de Autofagia ✅
- [x] Criar `ecc-attest.sh` — integridade de planos
- [x] Criar `ecc-complete.sh` — gate de completude
- [x] Criar `ecc-digest.sh` — digestão de descobertas
- [x] Criar `ecc-autofagia.sh` — ciclo completo de autofagia
- **Status:** complete

### Phase 5: Documentar Protocolos ✅
- [x] Documentar protocolo de integração ECC ↔ Gran-Mestre
- [x] Documentar padrão de hooks autofágicos
- [x] Atualizar documentação de cross-harness
- **Status:** complete

### Phase 6: Testar e Reportar ✅
- [x] Testar scripts de autofagia
- [x] Testar modelo local com OpenCode
- [x] Verificar integração com hooks existentes
- [x] Relatório final com recomendações
- **Status:** complete

## Key Questions
1. Como o ECC pode se beneficiar do padrão de Attestation do Gran-Mestre?
2. O continuous-learning v2 do ECC substitui o Claude-Mem ou complementa?
3. Como adaptar o 3-Strike Protocol aos hooks do ECC?
4. Vale a pena criar um plugin ECC específico para autofagia?

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| Autofagia do ECC como análise conceitual + scripts | Não é possível modificar o repo remoto, mas podemos criar scripts de autofagia locais |
| Foco em integração cross-harness | ECC já é multi-harness; autofagia deve seguir mesma filosofia |
| Priorizar Attestation + Completion Gate | Mesmos gaps críticos identificados no Gran-Mestre |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|

## Notes
- ECC tem 2x mais estrelas que planning-with-files (230K vs 25.6K)
- Continuous-learning v2 usa observação + instinto com thresholds de confiança
- Claude-Mem é complementar (memória persistente) vs ECC (otimização de harness)
- Gran-Mestre é orquestrador — os três sistemas são complementares
