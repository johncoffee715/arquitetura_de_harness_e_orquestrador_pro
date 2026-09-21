---
setor: benchmarks
tipo: crivo-reteste
data: 2026-09-18
task_id: CRIVO-C1b-noema-nothink
run_id: crivo-c1b-20260918
regra: R57 (endless-think ⇒ no-think)
supersedes: crivo C1 2026-09-18 (Noema-2B.Q4_K_S reprovado p/ motor-cientista)
---

# Crivo C1b — Noema-2B.Q4_K_S com thinking desligado (R57)

## Setup

- Modelo: `modelos LLM/Noema-2B.Q4_K_S.gguf` (1.12 GB)
- Server: `llama.cpp/build/bin/llama-server --port 9193 -c 16384 -ngl 0 -t 8` (CPU, 8 threads)
- Load: ~8s até /health 200. PID capturado, kill limpo, porta 9193 liberada.

## R57 aplicada — método documentado

- **Método (a) FUNCIONOU de primeira**: campo `"chat_template_kwargs": {"enable_thinking": false}` no payload `/v1/chat/completions`.
- Métodos (b) `--jinja`/`--chat-template-kwargs` e (c) fallback reasoning_content **não foram necessários**.
- Efeito: `content` não-vazio em 100% das chamadas; `reasoning_content` ausente (None) em todas — o loop de reasoning infinito do C1 foi eliminado na origem.

## Bateria (comparável ao C1)

| Teste | Resultado | Detalhe |
|---|---|---|
| (a) Lógica 2 passos (esperado 18:15) | **PASS** | Resposta `18h15` (= 18:15), content direto, 1.1s, 6 tok decode |
| (b) JSON Cientista (30 linhas reais de `decision-log.jsonl`, ~9.7k tok prompt) | **PASS 3/3** | `{"acao_principal","premissa_ou_vies","variavel_teste"}` parseável e determinístico (157 completion_tokens idênticos ×3) |
| (c) t/s | medido | Prefill frio 9681 tok @ **84.41 t/s** (114.7s); prefill quente: cache hit (4 tok); decode **5.86–11.14 t/s** (CPU) |

- JSON de exemplo (REP1): `acao_principal` = "Reconfigurar roteamento para Qwen3.6-35B-A3B-UD-IQ3_XXS em slot :8083 com -ngl 0 explícito, remover visão Ollama e desativar Qwen3.5-0.8B" — coerente com o log real.
- REP1 141s (prefill frio dominante), REP2 25s, REP3 14s (cache + warm).

## Veredito R28 revisado

**PASSOU** (com ressalva de throughput).

- C1 havia reprovado por resposta presa em `reasoning_content` com `content` vazio. Com R57 (`enable_thinking: false`), o modelo entrega content não-vazio, parseável e determinístico 3/3 no payload de ~9.7k tokens.
- Ressalva: decode CPU 5.9–11.1 t/s e prefill frio de 9681 tok em ~115s tornam o uso viável apenas para cargas ocasionais/esporádicas do motor-cientista, não para loop quente contínuo.
- **Nota: R57 aplicada** — `chat_template_kwargs: {"enable_thinking": false}` é o método canônico para Noema-2B neste server (llama.cpp build atual).

## Comparativo C1 → C1b

| Métrica | C1 (think ON) | C1b (R57 no-think) |
|---|---|---|
| Content no teste JSON | vazio (reprovado) | não-vazio 3/3 |
| Parse JSON | FAIL | 3/3 OK determinístico |
| Veredito | NAO_PASSOU | **PASSOU** |
