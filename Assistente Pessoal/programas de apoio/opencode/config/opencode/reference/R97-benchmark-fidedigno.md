# R97 — Guardrail Universal de Fidedignidade em Benchmarks (promulgada 2026-09-09)

> Status: FORJADA (ordem do usuário) · incorporação no AGENTS.md pendente.
> Vale desde o registro no decision-log. Nasce de falha própria admitida
> (duelos CPU×GPU assimétricos 06-08/09) — regra que conserta o autor.

## Regra

Para que todo teste seja fidedigno, todo LLM testado DEVE ser submetido às
MESMAS métricas que seus atuais rivais da stack local correspondente, e também
às MESMAS variáveis de temperatura e quarteto, simulando o uso real na stack
durante os benchmarks. Violação = veredito VOID.

## Checklist obrigatório por duelo (ambos os lados, mesma janela)

1. **Métricas idênticas**: decode (n≥32, temp 0.0) · prefill (~1-2K prompt) ·
   determinismo (×2 temp 0) · GBNF-conformance (mesmas gramáticas) ·
   factual/PT · duelo de qualidade cego (mesmo prompt).
2. **Temperatura idêntica**: temp/top_p/top_k/modelos de sampling iguais.
   Diferença de sampling invalida comparação de qualidade.
3. **Quarteto idêntico**: .md (mesmo prompt de papel) · .json (mesmos critérios
   de aceite) · .py (mesmo driver/validação) · .gbnf (mesma gramática onde couber).
4. **Otimizações de ambiente idênticas**: mesmo device (-ngl/-dev), batch (-b/-ub),
   KV types, FA on/off, threads e carga do sistema anotada. Diferença de ambiente
   invalida tanto quanto diferença de temperatura (update 2026-09-09).
4. **Slot neutro quando possível**: :9096 octógono (rivais medidos lá, sem tocar
   produção); mesma janela temporal (load anotado); re-probe em contaminação.
5. **Ctx honesto**: mesma -c salvo disjuntor de papel em teste (registrar divergência).

## Efeito retroativo

Vereditos anteriores fora deste padrão viram PARCIAIS pendentes de re-duelo
(ex.: OLMoE/Qwen0.5/Gemma/Qwen2.5-3B/Gemma3-4B vs rivais GPU) — foi o que
motivou o programa GPU 09/09. Exceções registradas com motivo (ex.: big-3 sem
VRAM: aritmética prova a impossibilidade).
