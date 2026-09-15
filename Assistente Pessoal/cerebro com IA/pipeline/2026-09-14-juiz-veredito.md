---
setor: pipeline
tipo: veredito-juiz-final
data: 2026-09-14
task_id: snn-juiz-final-r28
run_id: juz-1789433036
papel: juiz-limbico (F5-F6)
suite: 44 passed (pytest snn/ -q, 2.22s, exit 0)
status: VEREDITO_EMITIDO
---

# Juiz final — Pipeline SNN motor-funcional (W0/C1/W1/W2/W3/W4/W5 + audit-ndistintos)

> Suite rodada pelo juiz: `snn/.venv/bin/python -m pytest snn/ -q` → **44 passed in 2.22s**.
> Re-runs independentes: E2E+daemon 7 passed; `stream_stats` full (32.8s, 83.3MB);
> probe reforço próprio r2 17→51. Código snn NÃO alterado; sem commit.

## Veredito por nível (R28 categórico)

| Nível | Critério | Veredito | Evidência (fresca, medida pelo juiz) |
|---|---|---|---|
| L1 | Topologia real MaleCNS | **PASSOU_CATEGORICO** | `stream_stats` full: 2318 batches, 151.856.684 rows, **n=169.736** corpos (<500k), id 10001/1571863634, 32.8s, 83.3MB — reproduz audit (169.736, 83.9MB). Delta +1,8% vs canônico 166.691 = variantes minconf-0.5, explicado e aceito. |
| L2 | Dinâmica viva vault→SNN→trio→vault | **PASSOU_CATEGORICO** | `test_e2e_real` GREEN; `live_state.json`: exit ok, **rwkv_http 200**, 85 spikes, embedding_dim 1024, decision_raw real RWKV. Mocks cobrem ler/agir/ignorar + falha-não-finge. |
| L3a | Reforço PPL101 (probe 17→51) | **PASSOU_CATEGORICO** | Probe próprio no fixture mini: r2 **17→34→51** após 2× reinforce(+1), eff 1.0→1.2→1.4 — reproduz exato o claim W4. Bounds [0.1,2.0], persistência roundtrip, rotas inativas intactas (4/4 testes). |
| L3b | Daemon W5 (idempotência) | **PASSOU_CATEGORICO** | `daemon_episodes.jsonl`: 2 episódios reais exit ok (spikes 68, 1072). `test_jsonl_contem_campos`: 2º run = 0 episódios, sem duplicar. Debounce/fila-max-5/SIGINT-flush testados (6/6 daemon tests). |

## Bugs / ressalvas reais (todos verificados, nenhum bloqueante)

- **B1 (dívida P3 parcial):** imports top-level restantes — `event_loop.py:19`, `feather_to_csr.py:28`, `live_loop.py:27,29`, `aggregate.py:23`. Suite só é verde com cwd=`snn/`. P3 quitou 3 arqs + `__init__.py`; estes 4 ficaram. Funciona, mas packaging frágil.
- **B2 (regiões sintéticas):** `live_loop.py:133,142` — "regiões" r0–r3 = `i % 4` sobre índice denso, NÃO macro-região anatômica (MB/CX/PPL101). O HMI/wiki fala em macro-regiões, mas o loop não mapeia neurônio→região real. Reforço atua em buckets arbitrários.
- **B3 (PPL101 é rótulo, não identidade):** o próprio wiki (`snn-ppl101-dopamina.md`) marca contagem de células PPL101 como UNKNOWN. O `reinforce()` é eligibility-trace genérico por rota (padrão doomfly, implementação própria) — mecanismo PROVADO, mapeamento anatômico PPL101→KC pendente.
- **B4 (classify keyword-frágil):** `live_loop.py:204-210` — RWKV real respondeu chatty ("Okay, let's see…", sem palavra de decisão) e caiu no default `ignorar`. Decisão segura, mas o parser de decisão é substring-match; resposta sem keyword sempre vira ignorar.
- **B5 (contagem por wrap):** `live_loop.py:109-117` — contagem de disparos via monkey-patch de `nr.receive` por instância. Correto (probe confirma), mas frágil a refactors do LIF.
- **B6 (daemon "reativo" = polling 2s + taxa 1 ep/10s):** por design anti-spam; reatividade real limitada, adequado ao uso atual (2 episódios gravados).

## Nota final R34

**92.5 / 100** — L1/L2/L3 todos reproduzidos de forma independente pelo juiz
(número 169.736, E2E HTTP 200, probe 17→51 exato, idempotência). Descontos:
B1 (−2.0, dívida packaging), B2+B3 (−3.0, honestidade anatômica: buckets ≠ regiões,
PPL101 = rótulo), B4+B5 (−1.5, fragilidades não-bloqueantes), B6 (−1.0, reatividade limitada).
Nenhum código que finge: falha de endpoint retorna `exit_status failed` com erro bruto
(`test_falha_endpoint_nao_finge` GREEN); métricas são medidas, não inventadas.

exit_status: ok
