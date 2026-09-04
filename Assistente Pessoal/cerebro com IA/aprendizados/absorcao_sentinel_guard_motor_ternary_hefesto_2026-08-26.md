# Absorção sentinel-guard + Motor Ternary-8B do Hefesto (2026-08-26)

## Pipeline hefesto executado (4 estágios completos)
- **Artefato**: `/tmp/opencode/forno/sentinel-guard/` (guard.py, sync.py, README.md — ~1,1 KB)
- **Destino global**: `config/opencode/skills/sentinel-guard-security/` (SKILL.md + guard.py hardened + test_guard.py)
- **Resultado**: TDD 5/5 GREEN, cobertura 100% (stdlib trace), panteão convergiu (média ≈96.4 > 95)

## Falhas críticas encontradas NO ORIGINAL (auditoria adversarial)
| ID | Falha | Local | Confiança |
|---|---|---|---|
| E-001 | SQL injection por f-string em query | guard.py `find_user` | CONFIRMED |
| E-002 | Bypass de autorização injetado (`' OR '1'='1`) | guard.py `check_access` | CONFIRMED |
| E-003 | API key hardcoded em cleartext (`sk-live-...`) | guard.py:3 + README orienta editar | CONFIRMED |
| E-004 | Token auto-aprovado sem verificação (score default 96.5) | guard.py `validate_token` | CONFIRMED |
| E-005 | Sync HTTP sem auth para IP interno hardcode | sync.py | CONFIRMED |
| E-006 | Dependência interna inexistente (`vaultcore`) | sync.py import | HIGH_CONFIDENCE |

## Lições
1. **Score default alto = fraude** (padrão anti-fraude hefesto): `validate_token` retornava 96.5 fixo — mesmo antipadrão do Hefesto v6 `_evaluate_pillar`. Validador sem evidência → UNKNOWN + nota piso.
2. **/tmp é volátil**: a fonte foi removida entre sessões → hash sha256 do original ficou UNKNOWN. Registrar lacuna honestamente no provenance; nunca inventar.
3. **Instrumentação manual de cobertura com sys.settrace buga** (frames aninhados não rastreados sem handler 'call') → usar `python -m trace --count` stdlib.
4. **Capabilities antes de apontar motor** (R35/R9): GGUF pode existir no path mas não expor tool calling. Ternary-Bonsai-8B-Q2_0_g64 (:9090) = só "completion" → `tool_call: false` no provider.

## Mudança de motor do hefesto
- `agent/hefesto.md`: `local-forge/qwen3.8-4b` → `local-ternary/ternary-bonsai-8b`
- Novo provider `local-ternary` :9090 no opencode.jsonc (ctx 65536 nativo, Q2_0, 8.19B params)
- Tradeoff registrado: sem tool calling nativo; fallback para tools = local-forge/qwen3.8-4b
- Smoke test real: resposta "OK" ✓
