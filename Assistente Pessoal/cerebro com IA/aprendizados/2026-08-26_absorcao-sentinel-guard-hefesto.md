# Absorção sentinel-guard via hefesto — artefato poison detectado

**Data:** 2026-08-26 · **Doutrina:** skills/hefesto (G-D→G-A→G-H→G-F) · **Origem:** `/tmp/opencode/forno/sentinel-guard/`

## O que aconteceu
Artefato externo "sentinel-guard" (guard de acesso + vault sync, 3 arquivos Python) submetido à absorção. A auditoria adversarial revelou que NÃO era um protótipo ruim — era um **artefato poison**: SQL injection intencional embutida como lógica de negócio.

## Achados-chave (10 falhas, evidência E-001..E-005)
- **F-001/F-008 (CRÍTICA):** `check_access` injetava `' OR '1'='1` no username — bypass total de autenticação disfarçado de código.
- **F-003 (CRÍTICA):** `API_KEY = "sk-live-a7f3..."` hardcoded em plaintext.
- **F-004/F-005 (CRÍTICA):** `validate_token` ignorava o token e retornava `{"valid": True, "score": 96.5}` — auto-aprovação fraudulenta (mesmo padrão do `_evaluate_pillar` do Hefesto v6).
- **F-006/F-007 (BLOCKER):** dependência `vaultcore` inexistente + endpoint `10.99.0.77:9999` não roteável.

## Lições destiladas (proteína)
1. **Assinatura de artefato poison:** falha de segurança que é caminho feliz do código (não bug de borda) + validação que sempre aprova + segredo real exposto. Os 3 juntos = malícia presumida, não incompetência.
2. **Score default alto sem evidência é fraude canônica** — já visto no Hefesto v6 (96.5) e repetido aqui. Toda vez: refutar, nota piso.
3. **Helenização inverte falhas:** o forjado não replica nem "corrige por cima" — reconstrói a essência com as falhas estruturalmente impossíveis (queries parametrizadas, env fail-closed, allowlist).
4. **TDD pega bug do próprio forjador:** 2 bugs meus pegos pelos testes (recurso fora de allowlist não rejeitava; sync enviava Bearer vazio sem credencial).

## Scaffolding produzido (global, R2/R44)
- `config/opencode/scripts/sentinel-guard/sentinel_guard.py` — biblioteca segura (63 linhas executáveis, cobertura 100%)
- `config/opencode/scripts/sentinel-guard/test_sentinel_guard.py` — 24 testes TDD
- `config/opencode/scripts/sentinel-guard/mini_coverage.py` — medição de cobertura sem pytest-cov (scaffold reutilizável; lição: settrace não enxerga subprocess, rodar pytest in-process)
- `config/opencode/agent/sentinel-guard.md` — subagent auditor adversarial com checklist anti-poison

## Limitações conhecidas (honestas)
- `audit_all` tem semântica parcial: valida usuário a usuário; falha no meio deixa sincs anteriores feitos (sem transação).
- SQLite inválido só explode na primeira query (deferred), não no init.
- `mini_coverage` mede linha, não branch.

## Pendência de segurança
A key `sk-live-a7f3b9c2d8e41f6a9b0c3d7e2f5a8b1c` está em plaintext no original em /tmp — se real, ROTACIONAR.
