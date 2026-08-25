---
description: "Dev Loop: 3 níveis — N1 ReAct (task isolada) · N2 Spec-Driven (feature) · N3 Human Loop (épico)"
agent: gran-mestre
---
DEV LOOP ATIVADO — selecione o nível pela complexidade da minha próxima instrução:

NÍVEL 1 — REACT (task isolada, 1 arquivo, sem dependências): execute direto com o executor F4 (qwen3.8-9b :9087). Ciclo: fazer → testar → corrigir → entregar. Sem spec, sem gates.
NÍVEL 2 — SPEC-DRIVEN (feature local, multi-arquivo): mini-spec (3-5 linhas: objetivo + critérios + arquivos tocados) → implementação por executor → validação → entrega. Um único gate: eu aprovo a mini-spec antes.
NÍVEL 3 — HUMAN LOOP (épico/multi-sistema): escala para o modo MIX (/mix) automaticamente.

REGRA: se a minha instrução seguinte for trivial → N1. Feature → N2. Épico → N3 (escala automática, me avise antes de escalar).
