# SECRETARIO — Mecânica de Ignição

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: embeddings dedicados — Qwen3-Embedding-0.6B-Q8_0
  (1024-d, PT multilíngue, Apache-2.0).
  - `:9097` GPU Vulkan (lote 3+, fila b=16/32, ~91k tok/s) — caminho de lote.
  - `:9094` CPU (1-2 textos, ~0.52s, 0 VRAM, 809M RAM) — caminho tempo-real.
- **Refutação do catálogo**: embedding não raciocina — só classifica por
  cosseno. Qualquer síntese/prosa/curadoria → escalar `bibliotecario`
  (RWKV7 :9084, 1M ctx). Extração estrutural pesada futura → Needle2 :9091
  como acelerador; hoje a execução é determinística local (Python puro).
- **Fallback**: GPU → CPU (cruzado, automático no cliente canônico
  `bibliotecario/tooling/embeddings.py`) → lexical+`vetor_placebo: true`
  flagado (registro vetorial BLOQUEADO neste modo).
- **Execução**: Needle2 :9099 (`secretario-tools.json`) como acelerador —
  SUGERE a function call, quem executa é o Python determinístico
  (`mecanica.py` valida basename do alvo real; inválido → ignora e segue
  determinístico; diário marca `acelerador: needle|deterministico`).
  Needle offline/timeout → determinístico silencioso.

## 2. Parâmetros de ignição (sampling R61)

- **Classificação**: cosseno puro, zero-LLM — sem sampling envolvido.
- **Estruturação** (quando um LLM for compor campos/despacho):
  `temperature 0.0 · top_k 10 · top_p 0.9 · repeat_penalty 1.1 ·
  max_tokens 512`, GBNF travada (`schema.gbnf`, R81/R85).
- Alteração de sampling sem novo crivo = proibida (R62/R66).

## 3. Sequência de ignição

1. Validar gabarito (deny) — nenhuma ação antes.
2. Triagem: `embed(texto)` + cosseno contra centróides dos protótipos
   (cache em `tooling/data/protos_cache.json`) → intent + scores.
3. Desempate: margem entre top-1 e top-2 ≥ 0.05, senão `intent = "ambiguo"`.
4. Despacho pela `rota` do intent (`mecanica.py` orquestra).
5. Ação crítica? Exigir `hitl: true` — sem ele, exit 2 blocked.
6. Toda mutação: quarentena/backup antes + append no diário JSONL.

## 4. Anti-loop (R18/R42)

- `max_retries = 3` por operação de rede (embedding, Qdrant, RWKV7).
- 3 falhas → exceção + `exit_status: blocked|failed` + motivo de 1 linha;
  nunca loop infinito, nunca retry silencioso adicional.
- 3 rodadas de refutação sem convergência → escalar ao orquestrador.

## 5. Enforcement

- Motor recusa ignição se a ação violar o deny do gabarito (camada 2 é lei).
- Registro vetorial com `vetor_placebo: true` = fraude (R28) — o código
  retorna exit 2 e NÃO faz upsert.
