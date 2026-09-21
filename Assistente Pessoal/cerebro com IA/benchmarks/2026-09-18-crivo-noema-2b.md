---
data: 2026-09-18
task_id: CRIVO-C1-noema
run_id: crivo-c1-20260918
modelo: Noema-2B.Q4_K_S.gguf
quant: Q4_K_S
hardware: CPU-only (16 threads, -ngl 0, GPU proibida)
ctx: 16384 (desvio: packet pedia 8192, mas 30 linhas reais do decision-log = 9611 tokens > 8192)
servidor: llama-server /mnt/dados/Assistente Pessoal/llama.cpp/build/bin/llama-server, porta 9191 (8083 intocada)
evidencia_bruta: /tmp/opencode/crivo-noema-bateria.json, crivo-noema-b-final.json, crivo-noema.log
memorial: harness/logs/llm-crivo-memorial.jsonl (llm_crivo.py R83)
---

# Crivo C1 — Noema-2B (candidato a motor da skill Cientista)

## Perfil do modelo
**Raciocinante**: emite `reasoning_content` (bloco de pensamento) antes de `content`. Com `max_tokens` baixo (40-60), o raciocínio consome todo o budget → content vazio + `finish:length`. Bateria refeita com 600-3000 tokens.

## Tabela de métricas

| # | Métrica | Resultado | Detalhe |
|---|---|---|---|
| a1 | Factual — capital do Brasil | ✅ | "Brasília", 47 tok, 13,1 t/s |
| a2 | Fatorial — fev. bissexto | ✅ | "29", 13 tok, 11,1 t/s |
| a3 | Factual — 7×8 | ✅ | "56", 90 tok, 13,4 t/s |
| b | JSON estrito Cientista sobre 30 linhas reais do decision-log (9.758 tok prompt) | ⚠️ SUBSTÂNCIA OK / ENTREGA FALHA | JSON schema-exato e grounded no log (R75, -ngl 0, KV-spill, VRAM 15GB — tudo real), porém emitido DENTRO de `reasoning_content`; `content` vazio + `finish:stop`. Reproduzido 3× (2 com instrução explícita p/ emitir fora do bloco — não obedeceu) |
| c | Lógica 2 passos (trem 15:00 + 2h30 + parada 45min) | ✅ | "18:15", 328 tok, 13,5 t/s |
| R83-A | Anti-alucinação (llm_crivo.py) | ❌ NAO_PASSOU | Fato ✓, arquivo inexistente ✓ (não inventou), extração com 0 invenções e 4/4 campos corretos, MAS envolveu JSON em ```json fences → parse pydantic falhou. Falha de FORMATAÇÃO, não de substância |
| R83-B | Anti-loop (n=3, temp 0) | ✅ PASSOU_CATEGORICO | Determinismo 100%, taxa loop 0%, vazio 0%, latência média 3,78s |

## Throughput real (CPU-only, medido)
- **Decode: 12,0-13,5 t/s** (metrics: 140 tok/11,67s = 12,0; curto: 13,1-13,5)
- **Prefill: 144,9 t/s** (9758 tok/67,34s, prompt longo)
- Boot: ~10s; KV: ctx 16384, n_slots 4

## Veredito R28 — papel motor-cientista: **NAO_PASSOU** (condicional)

**Substância aprovada, entrega reprovada.** O núcleo do motor-cientista é: ingerir log longo → emitir JSON estrito consumível. Noema-2B falha exatamente aí em duas modalidades:
1. **Prompt longo (~9,7k tok)**: resposta fica presa no bloco de raciocínio; `content` retorna VAZIO com `finish:stop` (patologia think-only, R57). Instrução explícita não recupera.
2. **Prompt curto**: JSON correto mas embrulhado em markdown fences (parse falha sem strip).

**Recuperação viável (re-teste C2 sugerido)**: (a) GBNF/grammar forçando JSON no content; (b) consumer com fallback `reasoning_content`; (c) template com toggle de thinking; (d) limitar input <9k tok. Sem nenhuma dessas, o motor não serve a skill Cientista.

## Evidência
- Bateria manual: 5 chamadas, 3/3 factual ✓, 1/1 lógica ✓, JSON grounded mas não entregue em content.
- llm_crivo.py R83: veredito global NAO_PASSOU (só pela fence da extração; 0 invenções, 0 loops).
- Guards respeitados: porta 8083 intocada; kill só nos PIDs capturados (3005096, 3007269, 3014159); -ngl 0 (zero GPU); porta 9191 livre ao fim (`ss -ltn` vazio, 0 processos).
