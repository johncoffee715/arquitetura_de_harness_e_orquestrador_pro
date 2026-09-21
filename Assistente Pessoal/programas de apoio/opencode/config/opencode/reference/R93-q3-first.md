# R93 — Q3-First: priorizar Q3, Q4 só pós-falha-quant (promulgada 2026-09-07)

> Status: FORJADA (ordem do usuário) · incorporação no AGENTS.md pendente.
> Vale desde o registro no decision-log.

## Regra

Em todo crivo/auditoria de LLM (R83/R84/R91), a quantização de teste é **Q3 primeiro**
(Q3_K_M preferido; IQ3_XS/IQ3_M conforme disponibilidade):

1. Crivo roda em Q3. PASSOU → canoniza em Q3 (menor VRAM/RAM/disquete, mesma rota).
2. Q4 entra SOMENTE pós-falha identificada como causada pela quantização, i.e.:
   veredito NAO_PASSOU + evidência de degradação típica de quant (gagueira
   morfológica, colapso de formato, perda factual vs baseline maior) → re-testa
   o MESMO crivo em Q4 antes de descontinuar o modelo.
3. Falha por arquitetura/papel (ctx, tokenizer, vocação, guarda) NÃO aciona Q4 —
   descontinua direto (Q4 não cura arquitetura).
4. Downloads seguem seriais (1 por vez — lição storm) e Q3 é menor = chega antes.

## Precedente

- OLMoE crivado em Q4_0 antes da regra: veredito Mantido (passou; sem falha =
  sem gatilho p/ re-teste).
- Qwen1.5-MoE: download Q4_K_M abortado mid-flight e trocado por Q3_K_M
  (tensorblock, 6.93G) na promulgação — primeira aplicação.
