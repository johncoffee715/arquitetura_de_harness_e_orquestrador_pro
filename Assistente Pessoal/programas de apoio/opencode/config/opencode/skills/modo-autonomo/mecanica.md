# Mecânica — modo-autonomo dev-loop cloud (R77 camada 3 · R89 · R93)

> Ignição, seleção e refutação de motores. A feature NÃO decide o que pode; o gabarito decide.

## 1. Ignição (quando liga)
- Trigger: `opencode/state/modo-autonomo.json` com `{"ativo": true}` + escopo + origem (ordem explícita).
- Nenhum subagente/hook/modelo ativa sozinho. Desliga: "desativa modo autônomo" / conclusão geral / ordem contrária → `{"ativo": false}` + linha de log.
- Ao ligar em sessão com transporte degradado: `cloud-direct` automático (R6/R10/R20/R89).

## 2. Seleção (sempre por CATEGORIA R75, nunca por nome de GGUF)
- Features/execução → categoria cloud (`omniroute`/LLM cloud atual, janela grande).
- `local-orchestrator/orchestrator` = DISJUNTOR ABSOLUTO p/ feature (R93). GM só: delegar, ignitar, julgar, supervisionar, sintetizar (R43/R70).
- Hefesto = executor padrão da forja (R74, 8 passos); retry com spec integral; binding `Model not found` → corrigir `model:` p/ ID neutro (R27) e retry.

## 3. Samplers & setup (por responsabilidade R61)
- Agentic/execução: `t0.6 tk20 tp0.95` · juiz: `≤0.15` · criativo: `t0.8-1.0` · exploração: `≥1.0`.
- Tool-call pesado (Executor-F4/Hefesto) carrega `grammar` do schema (R85); sem grammar = sem ignição. Exceção só :8083 com crivo 4/4.

## 4. Refutação pré-execução (R88, inclusive contra o usuário)
1. Fatos (timings/VRAM/vereditos/memorial) → 2. Dados lado a lado, mesma métrica → 3. Custo por extenso → 4. Veredito: SUSTENTA→não executa+registra; CAI→executa e carimba. Reiteração explícita pós-veredito → executa sob risco registrado (R39).
- Omissão de refutação em 1 ciclo = violação autodenunciada no decision-log.

## 5. Motor determinístico (`mecanica.py` + `schema.gbnf`)
- `mecanica.py` valida `trigger` + `verdict` byte-level via gramática; deny (irreversível/fora de escopo/sem estado ON) = `NAO_PASSOU_CATEGORICO` fail-closed.
- `gabarito.json` é FONTE ÚNICA (R77): Pydantic→JSON Schema→GBNF em runtime; `.gbnf` manual só legado/fallback.

## 6. Observabilidade
- Toda volta: `[Authorize] auto — modo autônomo (cloud)` + `[RunID]` + `[Budget]` + `[Derivation]` no CONTEXT e decision-log; relatórios carimbam `modo: autonomo ON (cloud)/OFF`.
