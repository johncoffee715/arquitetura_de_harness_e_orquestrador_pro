# Matriz QUEM/COMO/QUANDO/PORQUÊ/ONDE — grafo F0–F6 × roster × hardware (v3.0 2026-09-08: GAPs resolvidos com bateria)

> Hardware: Xeon E5-2699v3 · X99 · 4x8GB DDR4 · MI50 16GB HBM2 · SSD 128GB SATA3
> (harness idempotente). Features ignitam VIA QUARTETO (.md persona → .json
> contrato → .py validação → .gbnf gramática). Swap é inimigo: guardas abaixo.

## Lei do hardware (medido)

| Recurso | Papel | Guarda |
|---|---|---|
| VRAM HBM2 16G (rápida, escassa) | decode GPU: 6 smalls + draft (13-14G) | ≥1G livre (violar = OOM/NAO_PASSOU) |
| DDR RAM 31G (lenta, vasta) | pesos 35B (12.3G) + KV-CPU + :9095 + page cache | ≥4G livres (35B nunca pagina) |
| SSD SATA3 (bulk) | GGUFs, slots/logs, trash, fitragem, restart idempotente | downloads 1-a-1 (lição storm) |

## Standing roles — QUEM/COMO/QUANDO/PORQUÊ/ONDE

| Papel | QUEM | COMO (quarteto) | QUANDO | PORQUÊ | ONDE |
|---|---|---|---|---|---|
| Orquestrador | Qwen3.6-35B :8083 | R43: julga, ignita, nunca bruto | sempre | 262K + GBNF 4/4; deb 7 solo/15 draft | DDR (12.3G) |
| Proposer | Llama-1B :9088 | contrato/plano na janela | F2/F3 | ctx 131K + 228 t/s | VRAM 1.88G |
| Supervisor F4 | GM (+proposer apoia) | sequencia tasks, Git atômico | F4 | juízo + latência | DDR/GM |
| Executor F4 | executor→:9088 (grammar) | TDD por task | F4 | tps≥100 (R65) | VRAM |
| Refuter leve | Qwen1.5 :9095 | bursts A2A curtos | F1/F3/F5 | MT-7.17; deb 12.7 + ctx 8K | DDR (~7G) |
| Relay | Llama-3B :9090, Smol1.7B :9092 | extração GBNF | F4 | 129/200; semântica Llama | VRAM 5.1G |
| Micro | Smol360M :9093 | early-exit, classify | F0/eventos | 258; deb instrução | VRAM 0.43G |
| Ingestor | RWKV7 :9084 | logs 1M O(1) | F0/F4 | único 1M; deb raciocínio | VRAM 1.42G |
| Avaliador F5 | VAGO→GM acumula (+Atena) | diff holístico | F5 | sem juiz neutro no inventário | DDR/GM |
| Draft | Qwen3.5-0.8B (em :8083) | spec n-max 8, vocab 248320 | decode GM | +100% por 0.7G VRAM | VRAM |

## Funções velozes por fase (resolvidas por demanda + hardware)

| Fase | Função | QUEM | PORQUÊ (t/s + HW) |
|---|---|---|---|
| F0 massa | filtrar logs/hist/ctx | RWKV7 | único 1M; VRAM 1.42G |
| F0 micro | phatics/intent | Smol360M | 258 t/s; VRAM 0.43G |
| F1 consolidador | limpar refutações | Smol1.7B :9092 (GBNF+BOOL) | dedupe mecânico; GM valida |
| F2 spec-cache | cache semântico | script spec_cache.py (SEM LLM) | hash/sha por seção; LLM fora do juízo (BOOL falhou) |
| F3 compressão | resumir p/ A2A (cap RAM!) | LFM parcial | 291 t/s; history-cap anti-swap |
| F4 schema-router | schemas mínimos executor | Smol360M :9093 (SOMENTE enum-GBNF) | enum físico impede invenção; com validação |
| F5a extract | entidades do diff (files/funcs) | Llama-3B :9090 (GBNF) | exato byte-level medido |
| F5b judge | sumário + desvios (juízo) | GM (+Atena) | síntese-livre proibida em ≤4B (loop+invenção medidos) |
| F6 scaffold | telemetria→regras Hefesto | GM+Hefesto+vault | só GM julga; SSD persiste |

## Disjuntores (v3.0: +2)

F4 tps≥100 · refutação ≥180 · proposer ctx≥131072 · ingestor ≥1M ·
VRAM≥1G · RAM≥4G · juiz 0-erros (VAGO=GM) ·
router-SOMENTE-enum-GBNF (string-livre=false) · sintese-livre-vetada-≤4B.
