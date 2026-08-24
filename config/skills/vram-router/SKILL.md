---
name: vram-router
description: "Escolhe o melhor LLM local para uma task via MODEL_SCORE ponderado com escada de contexto 64K→96K→128K→192K, residency HOT/WARM/COLD, curvas VRAM medidas e cost de escassez (VRAM+prefill+superdimensionamento). Use sempre que for delegar execução a um modelo local."
---

<objective>
Roteamento BEST-FOR-THIS-TASK com guardrails físicos: nada acima de 192K sem
override; SAFE_LOAD contra teto medido; fallback PRIMARY→SECONDARY→TERTIARY→DEGRADED.
</objective>

<usage>
python3 ~/.config/opencode/skills/vram-router/run.py --role coder --ctx 32000 [--gpu-used 14.2] [--top 3]
# roles: orchestrator|planner|coder|critic|reviewer|judge
</usage>

<notes>
- Registry consumido: benchmark/runs/registry.json (gere antes via skill model-discovery).
- Task >192K ⇒ UNSCHEDULABLE (escada progressiva — diretriz 2026-08-23).
- Curvas medidas embutem overhead: comparação direta vs física, sem reserva dupla.
- Código: /mnt/dados/opencode/harness/models/router.py · testes: harness/tests/test_router.py (14 ✅).
</notes>

<referencia-completa>
Parâmetros run.py: `--registry` · `--role` {orchestrator|planner|coder|critic|reviewer|judge} OBRIGATÓRIO · `--ctx` needed_ctx_tokens (escada até 192K) · `--gpu-used` GiB ocupados · `--top` N.
Exit codes: 0 = rankeado · 1 = UNSCHEDULABLE (ctx >192K, sem SAFE_LOAD, ou registry ausente).
Constantes: PHYSICAL=16GiB · RESERVE=2GiB (só no fallback linear) · REF_CTX=32768 · TIERS=[65536,98304,131072,196608].
MODEL_SCORE: 0.30 cap +0.25 task +0.15 ctx +0.15 res(HOT1.0/WARM0.9/COLD0.75) +0.10 hist(neutro 0.5) +0.05 verif −0.10 cost(VRAM½+prefill³⁄₁₀+overprov²⁄₁₀) −0.05 risk(YELLOW).
Níveis: PRIMARY≥0.80 · SECONDARY≥0.65 · TERTIARY≥0.50 · senão DEGRADED.
Curvas VRAM medidas embutidas: ornith(14.2@32K→13.69@131K) · iq2-xxs(15.7) · -9b-q4(14.9) — curva medida dispensa reserva adicional.
PENDÊNCIA registrada: subtrair SYSTEM_PROMPT_OVERHEAD (~86k tokens observados: ~40k regras + ~46k scaffold) do ctx útil antes do ctx_fit/tier — ver RELATÓRIO COMPLETO §5.
</referencia-completa>
</notes>
