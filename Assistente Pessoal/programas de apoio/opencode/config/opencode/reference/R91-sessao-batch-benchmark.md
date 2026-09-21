# R91 — Sessão de Benchmark de Batch em Todos os LLMs (doutrina completa)

> Status: FORJADA 2026-09-06 (Hefesto, sessão cloud-direct) · incorporação no AGENTS.md
> pendente de escrita humana (AGENTS.md fora do allowlist de edição desta sessão).
> Vale como regra operacional a partir do registro no decision-log (`r91-promulgada`).

## Regra

TODO LLM da stack passa por **sessão de benchmark de batch** buscando otimização e
desempenho — não só no onboarding (R76), mas em toda mudança de device/ctx/quant (R27)
e em toda ordem de otimização. Batch maior NÃO é melhor por padrão (R76: b8192 colapsa
em bandwidth-bound); só o crivo decide, nunca o palpite.

## Procedimento (por slot, 1 por vez — R87)

1. **Escada**: atual vs `(1024/512)`, `(2048/512)`, `(4096/1024)` — pula config que estoure
   a guarda VRAM ≥1GB; slot de load lento (ex.: 35B CPU ~220s) usa escada reduzida
   (atual + 1 desafiante), salvo evidência em contrário.
2. **Métricas**: decode t/s aquecido (≥32 tokens gerados, temp 0.0, warmup descartado) +
   prefill t/s + tempo de load + delta VRAM. Amostra única lenta NÃO é veredito.
3. **Adoção**: média ≥+5% em 2 amostras (faixa ±5% = ruído) + zero regressão → ADOTA;
   senão MANTÉM (R62). Empate confirma o default por crivo, nunca por silêncio.
4. **Disciplina de transiente**: 1ª inferência pós-load é FRIA (compile Vulkan) — sempre
   descartar o warmup; re-probar antes de declarar degradação R63.
5. **Memorial**: resultado por config no decision-log + `llm-crivo-memorial.jsonl`;
   7/7 health antes e depois.

## Escada spec — draft + n-max por LLM (update universal 2026-09-07)

Métrica obrigatória da sessão em todo slot com suporte (`--spec-type` no binário),
hill-climbing com vencedor acumulado, sempre buscando a otimização máxima por LLM:

1. **Ordem de custo**: `ngram-simple` (1 restart, zero pesos) → `draft-simple` CPU
   (zero VRAM) → `draft-simple` GPU (mede DELTA VRAM!) → draft KV `q4_0`
   (corta ~4x o KV do draft) → escada `n-max` 2/4/6(/8).
2. **Draft elegível**: mesmo tokenizador (vocab ±100, checar no header ANTES de
   restartar) + menor da família; `p-min 0.75` default na pipeline 2026
   (default 0.0 é footgun — bisect b9235).
3. **n-max**: começa em 4; estende (6, 8) enquanto `mean_len ≥ 0.85 × n-max`
   (teto batido = espaço); adota por R91 (média +5% em 2 amostras, zero regressão).
4. **Métricas por degrau**: decode rep + decode estruturado (tool-call/JSON) +
   acceptance + mean len (log do servidor) + delta VRAM + tempo de load.
5. **Regra de guarda**: draft que estoura a guarda VRAM ≥1GB volta p/ CPU ou KV-q4;
   guarda violada = NAO_PASSOU mesmo com decode maior.
6. **Precedente canônico 06-07/09 (8083)**: plain 6.0 → ngram 5.9 → draft-CPU 9.2 →
   draft-GPU-F16 12.5 (guarda violada) → draft-GPU-q4KV 13.3 → n-max 6: 15.1
   (accept 1.0, len 5.45). Total: 2.5x com +0.7G VRAM.

## Refutação R88 (por que regra, não ad-hoc)

- Fatos: sweep 06/09 em 6 slots — 5 MANTER + 1 ADOTAR; sem a 2ª amostra, 9088 teria
  adotado ruído (+5.1%→+1.0%); sem warmup descartado, 9090 teria sido declarado
  degradado (28→129 t/s).
- Custo do ad-hoc: cada número acima exigiu restart + probes; sem protocolo, cada
  sessão futura repete o trabalho sem memorial comparável.
- Veredito: refutação do ad-hoc SUSTENTA → regra promulga; incorporação textual no
  AGENTS.md = 1 bloco humano (texto pronto acima).

## Exemplo canônico (2026-09-06)

- 9093 +1.7% MANTER · 9088 +3.1% (2 amostras) MANTER · 9090 −0.0% MANTER ·
  9092 +2.5% MANTER · 9086 +4.5% (2 amostras, sem regressão) ADOTAR b2048/ub512 ·
  9084 b1024 −1.0% MANTER. Batch maior atrasa o load (9090: 1:31→2:17).
  8083-CPU intocado (sweep 04/09 vigente).
