# 2026-08-30 — Refatoração Hefesto: Dispatcher + 4 Skills Atômicas (R77)

## O que foi feito
- Hefesto monolítico → **dispatcher** que invoca a skill atômica certa por fase via skill-tool.
- 4 skills atômicas com **3 camadas R77** (conceito.md persona + gabarito.json firewall allow/deny + mecanica.md ignição):
  - `hefesto-decompilacao` (O Arqueólogo) → contrato-plano :9088
  - `hefesto-autofagia` (O Estômago) → refutacao :9090
  - `hefesto-helenizacao` (O Tradutor) → contrato-plano :9088 (anti-lazy R71)
  - `hefesto-forja` (O Selador) → forja :9091 (Needle 2, fb judge :9085)
- Template canônico `_template-feature/` para toda feature futura (R77).
- Motor v2.0.0: roteamento R75 por categoria + `validate_gabarito` (R77 camada 2 — deny é lei) + fallback.

## Needle 2 (Cactus Compute)
- **Já existia** como binário nativo x86-64 em `tools/needle2/needle` (14.8MB, ~29MB RAM, 184-222 t/s) — triagem L0 :8097.
- Novo papel **FORJA :9091** com tool-set dedicado (`forja-tools.json`: validate_schema, write_artifact, upsert_vault, emit_manifest).
- API própria `POST /complete` (não-OpenAI) — acesso via motor, não provider.

## Lições
1. **Catálogo-primeiro (R8)**: o Needle já existia no sistema — o GAP era tool-set + registro R75, não build do cactus (que é ARM-only e não compila em x86).
2. **Zero-trust (R28/R53)**: subagente hefesto retornou SUCCESS com árvore de arquivos INVENTADA (zero mudanças no disco) — self-healing #17. Verificação de filesystem é obrigatória antes de aceitar veredito.
3. **R77 funciona**: gabarito.json como firewall determinístico — o motor recusa ignição se a ação violar deny (testado: "modificar o original" → rejeitado).

## Estado
- Testes: 36/36 verdes (test_hefesto_motor.py v2 + test_hefesto_skills.py).
- Health: 6/6 llama + needle 8097/9091 respondendo.
- Commit: 2a61c4f3a.