---
data: 2026-09-17
tipo: absorção Hefesto (MIX) — jev-eval-agent + vepforge (Atria Dawn)
---

# Absorções 2026-09-17 — roteador com gate + pipeline de evidência verificável

## 1. jev-eval-agent (vinilana, MIT) → skill `jev-eval`
- **Padrão**: classificador escolhe a próxima tool entre N opções (expõe só 1 tool ao LLM por passo) + gate `done` (noul) que bloqueia resposta prematura quando `done < 0.5`.
- **Métricas**: completion, efficiency = completion × ideal/calls × (0.5 se distrator), distractorCalls, idealPath, custo estimado.
- **6 tasks PT-BR** com distratores (flights_hold×book, calendar_block×create, etc.) — bateria pronta p/ avaliar agente.
- **Uso no harness**: aplicar o gate de confiança no roteador híbrido (R65); adaptar tasks como bateria complementar ao crivo-padrao (R97/R103).

## 2. vepforge (huzjie, inspirado Atria Dawn 744B) → skill `vepforge`
- **Padrão**: Verifiable Experience Pipeline — analyze→code→execute→reflect; Experience agrega Task+Trajectory+Artifacts+Evidences via Linker.
- **Evidência verificada ANTES do store**: exit_code==0, hash 64-hex, http 2xx, schema JSON, test failed==0, stdout não-vazio → `verified=true` só após passar. Anti-fake-done.
- **Zero-dependência core** (MockLLM roda pipeline em CI) + multi-backend LLM.
- **Uso no harness**: gates de entrega R28/R29 (evidência fresca), pipeline long-horizon R16/R37/R49, replay R18/R22, benchmarks R97.
- **mecanica.py** implementado e smoke-tested: cadeia de verificadores + Experience/Linker.

## Estado
- Skills criadas com quarteto completo (SKILL.md + gabarito.json + mecanica.py + schema.gbnf).
- Repos clonados em /tmp/opencode/ (jev-eval-agent, vepforge) — referência local.
- Nenhum código produtivo alterado; só padrões helenizados (R14/R74/R77/R85).