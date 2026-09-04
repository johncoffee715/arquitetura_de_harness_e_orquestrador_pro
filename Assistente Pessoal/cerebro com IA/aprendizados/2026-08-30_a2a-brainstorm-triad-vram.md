# 2026-08-30 — A2A Brainstorm: Loop com Tríade VRAM (Propositor/Refutador/Árbitro)

## O que foi feito (build real — via doutrina Hefesto R77)
- **Skill `a2a-brainstorm`** (3 camadas R77): conceito.md (A Ágora) + gabarito.json (firewall) + mecanica.md (ignição) + SKILL.md.
- **`a2a_brainstorm.py`**: loop A2A com tríade fixa na VRAM:
  - 🛠️ Propositor: Qwen3.8-4B (:9088) — gera/reescreve proposta
  - 🧠 Refutador: Ternary-8B (:9090) — ataca com evidência
  - ⚖️ Árbitro: LLMJudge-3B (:9085) — decide emparelhado A/B
  - 🏛️ Escalação: Ornith-35B (:8083 CPU) — Suprema Corte assíncrona
- Regras de engajamento: max 3 rodadas (R18), convergência R34, impressão R40.

## Evidência real (teste de fogo)
- TDD: 13/13 verdes (suíte features: 59/59).
- Teste real: "Melhor arquitetura RAG do Bibliotecário" → 3 rodadas de debate real (Qwen propôs, Ternary refutou, Judge decidiu refutação procedia 3x) → ESCALADO → **Ornith-35B decidiu: "INDEFERIDO — Contradições intrínsecas não resolvidas"** com análise estrutural.
- A proposta final do Qwen evoluiu a cada rodada (arquitetura com embeddings 8-bit ONNX, chunking 256) — a tensão cognitiva FUNCIONOU.

## Lições de engenharia (R46 dissecação)
1. **Judge-3B não emite JSON** — é treinado para avaliação emparelhada (`winner_model_a/b`). Adaptar o prompt à vocação real do modelo, não forçar formato.
2. **Ornith-35B CPU é inviável síncrono no loop** (~73s/50tok, bandwidth-bound) — escalação deve ser ASSÍNCRONA: loop salva histórico, `--escalar` consulta depois.
3. **Tríade com diversidade real**: Qwen (tool calling) × Ternary (profundidade) × Judge (emparelhado) — o debate não converge preguiçosamente; impasse real escala à Suprema Corte.
4. **Peneira grossa RWKV→Qwen já existia** (hooks kronjob/sdd-talamus + plugin preflight) — o GAP era o loop A2A, não o filtro.

## Pendência conhecida (pré-existente)
- `test_llm_inventory.py` desatualizado vs inventário R75 (7 failures da auditoria 30/08 — categorias novas sem affinity). Fora do escopo; registrar para próxima manutenção.

## Estado
- Commit: fc34b2f06.
- Registrado: opencode.jsonc (skills 13).