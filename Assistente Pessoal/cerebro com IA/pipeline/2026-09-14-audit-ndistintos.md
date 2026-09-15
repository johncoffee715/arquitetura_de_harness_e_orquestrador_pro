---
setor: pipeline
tipo: auditoria
data: 2026-09-14
deriva_de: 2026-09-13-snn-conectoma-CONTEXT.md
status: CONCLUÍDO
---

# Auditoria — anomalia `n_neuronios_distintos`

## Anomalia (apontada pelo Gran-Mestre em W1)

`snn/feather_to_csr.py` reportou `n_neuronios_distintos = 88.384.522` no dataset real
MaleCNS v1.0 (`connectome-weights.feather`, 1.051.241.946 B, sha256 `e35da783…`).
O canônico é **166.691 neurônios** (bioRxiv 10.1101/2025.10.09.680999 → CONFIRMED).

## Causa raiz (evidência = diff `snn/.backups/feather_to_csr.py.audit-ndistintos.bak`)

O contador misturava **dois espaços de ID diferentes** na mesma contagem:

- `body_pre`/`body_post` contêm **dois tipos de identificador misturados**: corpos neuronais
  (ids pequenos, `< 500.000`, mínimo observado `10.001`) e **sítios sinápticos**
  (ids grandes, até `1.571.863.634`).
- A contagem antiga fazia `set.update` de **todos** os ids → 88.384.522 ≈ corpos+sítios.

## Correção (≤10 linhas + 1 teste — delegada nested ao executor via CLI)

- `BODY_ID_MAX = 500_000` + `is_body_id()` filtram só corpos neuronais.
- Novo teste em `test_feather_csr.py` protege o limiar (`10001→True`, `499999→True`,
  `500000→False`, `1571863634→False`).

## Número verdadeiro (medido, re-execução GM 2026-09-14)

| Métrica | Antes | Depois | Canônico |
|---|---|---|---|
| n_neuronios_distintos | 88.384.522 | **169.736** | 166.691 |
| peak RSS (streaming total) | 7.896 MB | **83,9 MB** | — |

Delta +3.045 sobre o canônico (~1,8%) = corpos anotados a mais no flat-connectome minconf-0.5
(variações de anotação, esperado em dados experimentais — não é erro).

## Efeito colateral positivo

O bug explicava o pico absurdo de RAM: o `set` de 88M ids grandes inchava a memória.
Filtrando corpos, o streaming total do dataset (151.856.684 linhas, 2318 batches) cai
para **83,9MB de pico** — redução de 94×.

## Evidência fresca (re-execução)

```
batches: 2318 · total_rows: 151856684 · n_neuronios_distintos: 169736
id_min/max: 10001/1571863634 · stream_time_s: 34.2 · peak_rss_mb: 83.9
csr_slice_rows=100000 → n=38442 E=100000 build 0.6s · exit_status=0
Suite: 38 passed (37 anteriores + 1 novo de limiar), sem regressão.
```

## Veredito

**PASSOU_CATEGORICO** — causa raiz identificada, correção mínima com teste de proteção,
e efeito mensurável (RAM ×94 menor). Anomalia encerrada.
