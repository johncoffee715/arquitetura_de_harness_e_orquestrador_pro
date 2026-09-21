# MECANICA — porta-engine (ignição)

Ferramenta: `mecanica.py` (determinístico, zero LLM, stdlib pura — urllib/struct/json/argparse).
Toda evidência de adoção sai de comandos REAIS com saída JSON estrita (conforme schema.gbnf).

## Estágios e comandos

### S1 — PIN + TELEMETRIA
```bash
# auditar strings de telemetria de um binário (procura endpoint/anon_id/opt-out)
python3 mecanica.py probe-strings <binario>
# verificar env de opt-out no ambiente de adoção (PASS exige NEEDLE_TELEMETRY=0 ou DO_NOT_TRACK=1)
python3 mecanica.py check-env
# validar geração de um arquivo .cact (tag 0x05E12A83=gen2, 0x05E12A84=gen3)
python3 mecanica.py check-archive <arquivo.cact>
```
Gate S1: `probe-strings` sem achados de endpoint OU env de opt-out presente; `check-env` = PASS;
`check-archive` = geração reconhecida. Falha → engine não sobe nem em smoke.

### S2 — SMOKE (porta descartável ≥9100)
```bash
<path-engine>/needle --tools <tools-producao.json> --serve --port 9100 &
python3 mecanica.py smoke-check 9100
```
`smoke-check` envia: (a) payload canônico coberto por tool → espera `function_calls` não-vazio
com argumentos conformes; (b) payload off-topic → espera `function_calls` vazio (refusal-not-guess);
(c) payload com schema violável → envelope sem erro de parse (grammar byte-level segura o decode).
Gate S2: 3/3 checks PASS. FALHA em refusal → engine reprovada (quebra invariante da família).

### S3 — CRIVO t/s (bench local)
```bash
python3 mecanica.py bench 9100 --rounds 12 --baseline-tts 146.6
```
Mede latência média, decode_tps reportado no envelope (fallback: chars/s ÷ 4) e compara com o
baseline registrado (Needle 2: :9091 = 146.6 t/s · :8097 = 160.1 t/s — nota 2026-09-15-needle-sync).
Gate S3: `decode_tts >= baseline × 1.5` → PROMOVE; `[0.75×, 1.5×)` → MANTEM base (ganho não
complica troca); `< 0.75×` → REPROVA.

### S4 — PARIDADE DE SCHEMA
```bash
python3 mecanica.py bench 9100 --rounds 10 --tools forja-tools.json --strict-schema
```
`--strict-schema` exige 10/10 envelopes com `success=true` e zero `error_code`; reporta
presença de `confidence` calibrada (gen 3) — gate de confiança (R65) depende dela.
Gate S4: 10/10 + confidence presente (ou ausência documentada como limitação aceita).

### S5 — PROMOÇÃO (manual, HITL)
1. Atualizar `manifest_llm.json` com a entrada da engine nova (portas, tools, papel, acopla,
   `prova_tts` do S3) preservando a entrada da geração anterior como fallback documentado.
2. `start-stack.sh` idempotente preservado (pgrep por binário/porta).
3. Nota de decisão em `cerebro com IA/decisoes/` com veredito + evidências (R26).
4. `python3 -m json.tool manifest_llm.json` antes de fechar.

## Relatório de adoção
```bash
python3 mecanica.py report --stage S3 --engine needle3-3.0.1 --verdict PROMOVE
```
Emite JSON estrito conforme schema.gbnf (stage enum S0-S5, gates, verdict enum
PROMOVE/MANTEM/REPROVA, evidência obrigatória por campo).
