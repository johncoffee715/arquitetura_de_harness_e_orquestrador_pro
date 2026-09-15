# Lição — Hefesto universal cloud-direct (2026-09-12)

> Quando o transporte local morre, o motor muda, a doutrina fica.

## Fatos (com evidência)
1. Llama-3.2-1B (:9088) e qwen2.5-coder-3b falham tool-calling multi-tool (`peg-native format`, reproduzível via curl); Llama-3.2-3B passa 1–7 tools **só no build 0.18.0** — o build 0.3.0-dev tem gramática PEG mais estrita e quebra com 3+ tools.
2. `libggml-vulkan.so.0.18.0` foi deletada do bin do old-build: nenhum processo novo sobe nele (só os já residentes). Build novo é CPU-only.
3. `granite-4.2-3b` (o tool-caller original) foi deletado em 2026-09-04 — a capacidade se perdeu ali.
4. Agent configs valem pós-restart; opencode.jsonc `local-forge` foi revertida por mecanismo desconhecido (suspeita sync-hook) — routing por agent-file prevalece, provider nunca.
5. 35 skills forjadas via cloud-direct, sweep final 35/35 PASS; 2 com clone real + SHA (grok-build 3794978, testsprite 125872f).

## Regras novas
- **R-transporte**: transporte morto 1× = cloud-direct imediato, sem retry cego (R6 aplicado a slot, não só a task).
- **R-build**: antes de trocar modelo de slot, testar multi-tool (1, 2, 7 tools) — single-tool verde não prova nada.
- **R-staging**: mudança de config mid-session NÃO pega (runtime cacheia); documentar `vale pós-restart` + caminho de revert no CONTEXT.
- **R-forja**: intake webfetch basta p/ pattern-skills; frameworks/huge repos pedem clone real (SHA + fonte lida) — o usuário cobra ("como hefesto").

## Revert (quando a stack local voltar)
- agent/*.md: bibliotecario+cortex → local-thalamus/ingestor; executor-f4+general+hefesto+planejador+prosa-f2+sentinel → local-forge/proposer; juiz+refutador-limbico → local-ternary/refuter; explorador+explore+reflexo-r42 → local-reflexo/reflexo.
- Skills novas: `git add opencode/config/opencode/skills/<35 nomes>` (lista no CONTEXT) + limpar `__pycache__/`.
