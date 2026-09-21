---
data: 2026-09-18
task_id: CRIVO-C3-lfm-thinking
run_id: crivo-c3-20260918
modelo: LFM2.5-1.2B-Thinking-ToMoE-Q4_K_M.gguf
quant: Q4_K_M
hardware: CPU-only (8 threads, -ngl 0, GPU proibida)
ctx: 16384
servidor: llama-server /mnt/dados/Assistente Pessoal/llama.cpp/build/bin/llama-server, porta 9194 (8083 intocada)
evidencia_bruta: /tmp/opencode/crivo-lfm.log, crivo-lfm-bateria.json, crivo-lfm-native.json, bateria_lfm.py, bateria_lfm.out, r57_probe.py
---

# Crivo C3 — LFM2.5-1.2B-Thinking-ToMoE (candidato a motor da skill Cientista)

## Perfil do modelo
**Raciocinante**: emite `reasoning_content` antes de `content` — patologia think-only do C1 confirmada em budget baixo (400 tok → content vazio + `finish:length`). **R57 aplicada SEMPRE**: `chat_template_kwargs:{"enable_thinking":false}` é **aceita pelo servidor mas IGNORADA** — o template do GGUF tem `preserve_thinking` mas nenhum toggle `enable_thinking` (verificado via /props). Com budget ≥3000 tok, o thinking completa e o content É entregue (`finish:stop`) — diferente do Noema C1, que mesmo com 3000 tok manteve content vazio no prompt longo.

## Tabela de métricas

| # | Métrica | Resultado | Detalhe |
|---|---|---|---|
| a1 | Factual — capital do Brasil | ✅ | "Brasília", 690 tok (300 thinking), 19,1 t/s |
| a2 | Fatorial — fev. bissexto | ✅ | "29", 318 tok, 20,7 t/s |
| a3 | Factual — 7×8 | ✅ | "56", 127 tok, 15,0 t/s |
| b | Lógica 2 passos (trem 15:00 + 2h30 + parada 45min) | ✅ | "18:15" correto, MAS 2644 tok de thinking, 166s wall, e resposta suja: `\boxed{18:15}` anexado |
| c | JSON estrito Cientista sobre 30 linhas reais do decision-log (9.772 tok prompt) | ✅ PASSOU_CATEGORICO | 3/3 reproduções: JSON válido, schema-exato (3/3 chaves), **sem fence**, ENTREGUE em content, 3/3 byte-idênticos (determinismo total). Grounded: `decisionlog.convergencia` (1 ocorrência real no log) e `KV-spill` (1 real); porém `premissa_ou_vies` = filler vago ("A decisão A é o ponto central") |
| d1 | Anti-alucinação — arquivo inexistente | ❌ INVENTOU | "O arquivo contém instruções para o funcionamento do Assistente Pessoal com IA." — fabricou conteúdo de arquivo que não existe (C1 e C2 recusaram corretamente) |
| d2 | Anti-alucinação — extração 4 campos | ⚠️ substância OK / formato FALHA | 4/4 valores corretos, 0 invenções, MAS emitiu markdown k-v (`data: 2026-09-17`) em vez de JSON apesar de instrução "SOMENTE um JSON" → parse falhou |
| e | Anti-loop (n=3, temp 0) | ✅ PASSOU_CATEGORICO | Determinismo 100% (3/3 idênticos), loop 0%, vazio 0%, latência média 26,8s |

## R57 — endless-think ⇒ no-think (documentada)
1. `chat_template_kwargs:{"enable_thinking":false}`: aceita, **sem efeito** (template sem toggle; /props confirma só `preserve_thinking`).
2. Budget 400 tok: content vazio, tudo em reasoning (1712 chars), `finish:length` — patologia C1.
3. Budget ≥3000: thinking completa → content entregue. **Custo**: 127–2644 tok de thinking por chamada; latência 8–166s.

## Throughput real (CPU-only, medido via print_timing do servidor)
- **Decode: 14,6 t/s** (com KV de prompt 10k carregado) **– 22,8 t/s** (curto; média 20,1 em 26 amostras)
- **Prefill: 127,5 t/s** (9.772 tok / 76,6s)
- Boot: ~5s; KV: ctx 16384, n_slots 4

## Veredito R28 — papel motor-cientista: **NAO_PASSOU** (condicional)

**Entrega exemplar, evidência contaminada.** O critério central (log 10k → JSON estrito consumível) é o MELHOR dos 3 candidatos: JSON válido, schema-exato, sem fence, em content, determinístico 3/3. Porém:
1. **Anti-alucinação é eliminatório para um motor-cientista**: fabricou conteúdo de arquivo inexistente (d1) — a skill Cientista produz micro-inferências grounded; um motor que inventa evidência contamina o produto na origem.
2. **Instruction-following de formato instável**: d2 ignorou "SOMENTE um JSON" (markdown k-v) — 3/4 emissões JSON no total.
3. **Overhead thinking estrutural**: sem toggle R57 funcional, toda chamada paga 127–2644 tok de raciocínio (latência 2–6× o C2; budget <3000 = content vazio).

**Recuperação viável (re-teste C4 sugerido)**: (a) GBNF grammar forçando JSON no content; (b) system prompt anti-fabulação + pergunta d1 re-testada; (c) consumer com budget ≥4000. Se d1 passar com system prompt, o modelo assume a liderança técnica do papel.

## Comparação 3-modelos — motor-cientista (bateria idêntica, CPU-only)

| Dimensão | Noema-2B (C1) | qwen2.5-coder-3b (C2) | LFM2.5-1.2B-Thinking (C3) | Melhor |
|---|---|---|---|---|
| Factual (3×) | 3/3 ✅ | 3/3 ✅ | 3/3 ✅ | Empate |
| Lógica 2 passos | ✅ 18:15 | ❌ 17:45 | ✅ 18:15 (sujo: \boxed) | **Noema/LFM** |
| JSON 10k tok | ❌ content VAZIO 3× (preso em reasoning) | ⚠️ content ✓, válido, com fence | ✅ content ✓, válido, schema-exato, SEM fence, 3/3 idêntico | **LFM** |
| Anti-alucinação | ✅ 0 invenções | ✅ 0 invenções | ❌ INVENTOU conteúdo (d1); d2 formato não-JSON | **C1/C2** |
| Determinismo | ✅ 100% | ✅ 100% | ✅ 100% | Empate |
| Decode t/s | 12,0–13,5 | 5,6–9,7 | 14,6–22,8 | **LFM** |
| Prefill t/s | 144,9 | 55,0–61,5 | 127,5 | **Noema** |
| Latência/chamada | 3,8s média | 2,1s média | 8–166s (thinking obrigatório) | **C2** |
| Veredito R28 | **NAO_PASSOU** | **PASSOU (condicional)** | **NAO_PASSOU (condicional)** | **C2** |

**Conclusão**: C2 (coder-3b) permanece o único aprovado — único que combina entrega em content + zero invenções. C3 (LFM) tem o melhor formato de JSON e o decode mais rápido, mas o thinking sem toggle (R57 morta) e a fabricação de evidência (d1) eliminam-no para o papel de motor-cientista; seria forte candidato a papéis onde alucinação é filtrada downstream (ex: hipóteses passando por gate humano R85). C1 (Noema) segue inutilizável sem fallback frágil.

## Evidência
- Bateria: 13 chamadas (/tmp/opencode/bateria_lfm.py → crivo-lfm-bateria.json), R57 kwargs em 100% das chamadas.
- R57 probe: r57_probe.py (3 chamadas: off/on/baseline — todas idênticas, kwarg ignorada).
- Timings: print_timing do servidor (prefill 9772 tok/76,6s; decode 800 tok/54,8s c/ KV 10k).
- Guards respeitados: porta 8083 intocada (viva ao fim); kill só no PID capturado (3104705, morto); -ngl 0 (zero GPU); porta 9194 livre ao fim (`ss -ltn` vazio).
