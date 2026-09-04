---
tipo: aprendizado
data: 2026-08-28
autor: Gran-Mestre
pipeline: hefesto
tema: cortex talamico rwkv7 ctx 1M
---

# Córtex Talâmico setado: RWKV7-G1d-0.4B ctx 1M + captura bruta pré-LLM

## Estado real (CONFIRMED)
- GGUF header: `rwkv7.context_length = 1048576` (nativo 1M — manifesto antigo dizia 8192, ERRADO).
- Servidor :9084 já rodava `-c 1048576` (start-stack.sh linha 54) — props n_ctx=1048576.
- RWKV7 state fixo por camada → custo NÃO escala com ctx (kv_total 0.064GB constante).

## Correções (R27 — 5 pontos de verdade)
1. `harness/llm-inventory.json`: n_ctx_train 8192→1048576; category→talamus-cortex; weaknesses corrigidas; capabilities Córtex.
2. `manifesto_llm.json`: contexto_nativo/ctx_ativo 1048576; vocacao→CÓRTEX SENSORIAL PRIMÁRIO; tps 180.
3. `opencode.jsonc`: provider local-qwen (desalinhado qwen-3.5-0.8b) → local-thalamus/thalamus-cortex (ID neutro R69), ctx 1048576; small_model atualizado.
4. `start-stack.sh`: já correto (-c 1048576) — sem mudança.
5. `plugin/talamus-preflight.ts`: TALAMUS_SLOT=9084 default + condensação SDD real via /v1/chat/completions com enable_thinking=false (R57).

## Descoberta técnica (R46)
- RWKV7 responde VAZIO em /completion cru; via /v1/chat/completions + chat_template_kwargs enable_thinking=false → suco condensado limpo e estruturado. NO-THINK obrigatório para tarefas mecânicas (R57).

## Lição
- Ponto de verdade errado (n_ctx_train 8192) persistia apesar do servidor rodar 1M — auditoria GGUF header é a fonte da verdade (R62: geometria declarada ≠ custo real; aqui: ctx declarado ≠ ctx real do GGUF).
