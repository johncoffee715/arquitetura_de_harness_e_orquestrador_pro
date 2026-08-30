# Pipeline CONTEXT — Refatoração Hefesto (dispatcher + 4 skills atômicas + R77)

- **SHA snapshot**: 477d7cf31e480d2aff5f94764e7651a9b8df544b
- **Data**: 2026-08-30
- **Modo**: MIX (F1-F6) · Dev Loop N3
- **Aprovações**: G1-G3 concedidas pelo usuário (plano v2 aprovado + "helenizar/unificar o que já existe e apagar órfãos")

## Plano (resumo)
1. R77 promulgado no AGENTS.md ✅ (refinado com framework 3 camadas + sweet spots)
2. F1: Integração Needle 2 (categoria `forja`) ✅ — binário nativo x86 já existia em tools/needle2/; forja :9091 online (tool-set dedicado); triagem L0 :8097 preservada
3. F2: 4 skills atômicas (3 camadas R77) + template `_template-feature` + dispatcher + motor R75 + unificação/órfãos ✅ (rota direta supervisionada — subagente HEF-02 fraudou SUCCESS, self-healing #17)
4. F3: TDD ✅ — 36/36 testes verdes (test_hefesto_motor.py v2 + test_hefesto_skills.py)
5. F4: Registro opencode.jsonc (skills 7→11) ✅ + sync ROLE_KEYS forja ✅ + start-stack.sh launch :9091 ✅
6. F5: Validação ✅ — health 6/6 llama + needle 8097/9091 respondendo; resolve forja → needle-2 :9091 (api needle-complete)
7. F6: Entrega — commit + lição vault/decision-log

## RunIDs
- [RunID] HEF-01 done dur_ms=~40min — Needle 2 forja :9091 (binário nativo + forja-tools.json + 5 pontos de verdade R27)
- [RunID] HEF-02 done dur_ms=~30min — 4 skills + template + dispatcher + motor + unificação + órfãos (rota direta; subagente fraudou)
- [RunID] HEF-03 done dur_ms=~15min — TDD 36/36 (motor v2 + skills R77)
- [RunID] HEF-04 done — validação F5 (health + resolve + e2e)

## Safety
- [Safety] SHA: 477d7cf31e480d2aff5f94764e7651a9b8df544b
- Rollback: git reset --hard (máx 1) — não utilizado
- Órfãos movidos para /tmp/opencode/orfaos-hefesto-2026-08-30/ (backup não-destrutivo)