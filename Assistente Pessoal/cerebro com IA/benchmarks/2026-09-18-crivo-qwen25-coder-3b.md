---
data: 2026-09-18
task_id: CRIVO-C2-coder3b
run_id: crivo-c2-20260918
modelo: qwen2.5-coder-3b-instruct-q4_0.gguf
quant: Q4_0
hardware: CPU-only (16 threads, -ngl 0, GPU proibida)
ctx: 16384
servidor: llama-server /mnt/dados/Assistente Pessoal/llama.cpp/build/bin/llama-server, porta 9192 (8083 intocada)
evidencia_bruta: /tmp/opencode/crivo-coder3b-bateria.json, crivo-coder3b-c-native.json, crivo-coder3b.log, crivo-coder3b-30linhas.jsonl
---

# Crivo C2 — qwen2.5-coder-3b-instruct (candidato a motor da skill Cientista)

## Perfil do modelo
**Não-raciocinante**: não emite `reasoning_content`; toda a resposta vem em `content` com `finish:stop`. Sem a patologia think-only do C1. Porém **sempre embrulha JSON em ```json fences** (3/3 emissões, mesmo com instrução explícita "sem markdown" no prompt) — strip determinístico no consumer resolve.

## Tabela de métricas

| # | Métrica | Resultado | Detalhe |
|---|---|---|---|
| a1 | Factual — capital do Brasil | ✅ | "Brasília", 4 tok |
| a2 | Fatorial — fev. bissexto | ✅ | "29", 3 tok |
| a3 | Factual — 7×8 | ✅ | "56", 3 tok |
| b | Lógica 2 passos (trem 15:00 + 2h30 + parada 45min) | ❌ | "17:45" (esperado 18:15) — falha determinística de aritmética temporal |
| c | JSON estrito Cientista sobre 30 linhas reais do decision-log (9.985 tok prompt) | ⚠️ SUBSTÂNCIA OK / FENCE | JSON válido, schema-exato (3/3 chaves), grounded no log (acao_principal = "Canonizar Qwen3.6-35B-A3B-UD-IQ3_XXS :8083 CPU" — real, 2 ocorrências no log), ENTREGUE em content (151 tok, finish:stop) — mas em ```json fence. Reproduzido 2× (chat + nativo) |
| d1 | Anti-alucinação — arquivo inexistente | ✅ | "O arquivo ... não existe." — não inventou conteúdo |
| d2 | Anti-alucinação — extração 4 campos | ✅ | 4/4 corretos, 0 campos inventados (com fence) |
| e | Anti-loop (n=3, temp 0) | ✅ PASSOU_CATEGORICO | Determinismo 100%, taxa loop 0%, vazio 0%, latência média 2,14s |

## Throughput real (CPU-only, medido via /completion nativo — usage.timings ausente no chat endpoint desta build)
- **Decode: 5,6 t/s** (com KV de prompt 10k carregado) **– 9,7 t/s** (prompt curto; 300 tok: 9,66 t/s)
- **Prefill: 55,0 t/s** (9.985 tok) – 61,5 t/s (curto)
- Boot: ~10s; KV: ctx 16384, n_slots 4

## Veredito R28 — papel motor-cientista: **PASSOU** (condicional)

O núcleo do motor-cientista — ingerir log longo (~10k tok) → emitir JSON estrito consumível — **funciona ponta a ponta**: content entregue (não preso em raciocínio), JSON válido, schema-exato, grounded no log real, determinístico. Diferente do Noema, a entrega existe.
**Condição inegociável**: consumer DEVE fazer strip de ```json fences antes do parse (comportamento 100% consistente, 1 linha de código resolve).
**Risco anotado**: falha de lógica 2-passos (b) indica raciocínio aritmético fraco — geração de hipóteses da skill Cientista pode sair rasa; mitigação: hipóteses passam pelo gate humano (R85) de qualquer forma.

## Comparação direta vs Noema-2B (C1, mesma bateria)

| Dimensão | Noema-2B (C1) | qwen2.5-coder-3b (C2) | Melhor |
|---|---|---|---|
| Factual (3×) | 3/3 ✅ | 3/3 ✅ | Empate |
| Lógica 2 passos | ✅ 18:15 | ❌ 17:45 | **Noema** |
| JSON 10k tok | ❌ content VAZIO (preso em reasoning, 3×, instrução não recuperou) | ⚠️ entregue em content, válido+grounded, com fence (strip resolve) | **Coder-3B** |
| Anti-alucinação | ✅ 0 invenções (fence na extração) | ✅ 0 invenções (fence idem) | Empate |
| Determinismo | ✅ 100% | ✅ 100% | Empate |
| Decode t/s | 12,0–13,5 | 5,6–9,7 | **Noema (~2× mais rápido)** |
| Prefill t/s | 144,9 | 55,0–61,5 | **Noema (~2,4× mais rápido)** |

**Conclusão**: para o papel motor-cientista, **coder-3b supera Noema no critério decisivo** (entrega do JSON em content) e perde em velocidade (~2×) e lógica. Noema é inutilizável como motor sem fallback frágil de reasoning; coder-3b é utilizável com 1 linha de strip.

## Evidência
- Bateria manual: 10 chamadas (/tmp/opencode/bateria_coder3b.py → crivo-coder3b-bateria.json), 3/3 factual ✓, 0/1 lógica, JSON grounded e entregue (fence), 0 invenções, determinismo 3/3.
- Timings nativos: crivo-coder3b-c-native.json (prompt_n 9985, prefill 55,0 t/s, decode 5,6 t/s).
- Guards respeitados: porta 8083 intocada; kill só no PID capturado (3075543); -ngl 0 (zero GPU); porta 9192 livre ao fim (`ss -ltn` vazio, PID morto).
