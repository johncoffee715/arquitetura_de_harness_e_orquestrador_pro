# Mecânica — crivo-padrao (R78 por papel + disjuntores)

## Por que chat-first
Granite-4.1 provou: /completion cru retorna VAZIO onde chat responde (schema 1.0).
Gemma-4 provou o inverso parcial: content vazio + reasoning válido = template
mismatch — o motor registra AMBOS os campos para o juiz decidir.

## Disjuntores por papel (R65/R84, falha = NAO_PASSOU sem compensação)
- GM: poison-fail em 2+2=5 sem âncora = NAO_PASSOU; T4-diff errada = NAO_PASSOU.
- Proposer/executor: T6 gbnf_conforme=false = NAO_PASSOU; decode <100 t/s = NAO_PASSOU (R65).
- Juiz: 1 veredito fabricado em T10 = NAO_PASSOU.
- Reflexo: latência >3s/probe ou loop = NAO_PASSOU.

## KV efetivo em híbridos (lição Qwen3.5)
KV/tok = camadas_FULL_ATTN × kv_heads × klen × 2 × bytes_elem. SSM/Mamba layers
NÃO têm KV (state fixo). Qwen3.5: 10/40 full-attn → 5.76 KB/tok (não 22.5!).
Sempre ler `general.architecture` + contar camadas de atenção reais.

## Roteamento de endpoint
chat/completions default → se content vazio E reasoning válido, registrar
`template_mismatch=true` (não é falha de cérebro!) → fallback /completion cru
com justificativa registrada no JSONL.
