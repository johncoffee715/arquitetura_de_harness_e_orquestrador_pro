# R98 — Benchmark Completo Universal + Tabela Comparativa Sempre (promulgada 2026-09-09)

> Status: FORJADA (ordem do usuário) · incorporação no AGENTS.md pendente.
> Estende R91 (sessão) + R97 (fidedignidade): todo LLM avaliado, sempre,
> termina com TABELA COMPARATIVA para auditoria do usuário.

## Regra

Toda avaliação de LLM (candidato OU incumbente em revalidação) executa o
BENCHMARK COMPLETO e entrega TABELA COMPARATIVA ao final, sem exceção:

1. **Colunas obrigatórias**: pesos GB · ctx max/atual · KV/tok + kB/1k ·
   decode GPU · decode CPU · prefill · GBNF-conformidade · determinismo ·
   factual/PT · duelo de qualidade cego · veredito.
2. **R97 integral**: mesmas métricas/rivais/temp/quarteto/ambiente; violação = VOID.
3. **`a medir` com motivo**: célula sem dado carrega motivo
   (ex.: "arquivo excluído", "sem VRAM p/ GPU", "re-medir em acalmia").
4. **Custo da medição declarado**: evicções, restarts, tempo, degradação
   transitória — antes ou junto, nunca depois.
5. **Comparativo inclui incumbentes re-medidos** (não só números históricos).
