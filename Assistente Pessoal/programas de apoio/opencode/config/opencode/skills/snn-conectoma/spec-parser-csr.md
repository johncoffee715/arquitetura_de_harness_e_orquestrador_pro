---
name: snn-conectoma-parser-csr
description: "Spec do parser CSR (Compressed Sparse Row) para o grafo de adjacência do conectoma Drosophila MaleCNS v1.0 (166K neurônios, 312M sinapses, sinapses poliádicas). Define formato de entrada, invariantes, contrato de saída e validação byte-level."
mode: spec
tags: "snn, csr, parser, conectoma, sparse-matrix, malecns"
origin: helenizado:male-cns-v1.0
metadata:
  category: spec
  version: 1.0.0
  date: 2026-09-13
  author: Hefesto (dispatcher snn-hefesto-absorb)
  motor: contrato-plano
---

# Spec — Parser CSR do Conectoma MaleCNS

## 1. Objetivo

Converter um dump de adjacência do conectoma (lista de sinapses) em **CSR**
(Compressed Sparse Row) para consumo eficiente pelo event-loop SNN.

## 2. Formato de entrada (dump)

Formato canônico assumido (linha por sinapse ou multiedge agregado):

```text
# comentário (ignorado)
<pre_id> <post_id> <weight> [<extra>...]
```

- `pre_id`, `post_id`: índices de neurônio (u32), 0-based, < N (N = nº neurônios).
- `weight`: contagem de sinapses (u32) — sinapse poliádica (1 T-bar → n PSDs) vira
  multiedge `pre → post` com peso = nº de sinapses.
- Campos extras opcionais (neurotransmissor, região) ignorados pelo parser core.

## 3. Invariantes (proteína — do conectoma)

1. **Grafo dirigido**: sinapse é direcional (pré → pós). Sem aresta reversa implícita.
2. **Multiedge por peso**: múltiplas sinapses entre mesmo par ≠ arestas duplicadas —
   agregar somando pesos.
3. **Só sinapses químicas** no dataset: gap junctions / neuromodulação FORA do grafo.
4. **N e E conhecidos a priori**: N=166_000 (aprox), E=312M — alocar com capacidade exata.

## 4. Estrutura CSR de saída

```text
row_ptr:  Vec<u64>  // tamanho N+1; row_ptr[i..i+1] = intervalo em col_idx
col_idx:  Vec<u32>  // tamanho E_agregado; pós-sinápticos ordenados por (pre, post)
weight:   Vec<u32>  // tamanho E_agregado; peso por aresta agregada
```

- `row_ptr[0] = 0`; `row_ptr[N] = E_agregado`.
- `col_idx` ordenado por `(pre, post)` para permitir busca binária por vizinho.
- `E_agregado ≤ E` (agregação de multiedges).

## 5. Pipeline de parse (2 passes)

1. **Pass 1 (contagem)**: contar grau de saída por neurônio → `row_ptr` (prefix sum).
2. **Pass 2 (preenchimento)**: popular `col_idx`/`weight`; agregar multiedges.

## 6. Contrato de validação (byte-level)

- `row_ptr` monotônico não-decrescente, `row_ptr[N] == col_idx.len() == weight.len()`.
- `col_idx` em `[0, N)`; `weight > 0`.
- Grau de saída total == soma dos graus (consistência prefix-sum).
- Overflow: N×N < u32::MAX não é exigido — usar u64 em row_ptr.

## 7. Complexidade

- Memória: O(N + E_agregado) — sem matriz densa (166K² = 27.5B células é inviável).
- Tempo: O(E log E) no sort, ou O(E) com counting sort por bucket de grau.

## 8. Anti-padrões (proibido)

- Matriz densa `Vec<Vec<u32>>` (27.5B células — OOM).
- Hash de pares (pre,post) para agregação (alocação por aresta — lento).
- Assumir undirected (perde direção sináptica).

## 9. Evidências (ground truth)

- N=166K, E=312M, sinapses poliádicas: https://en.wikipedia.org/wiki/Drosophila_connectome
- Berg et al. 2025, bioRxiv `10.1101/2025.10.09.680999`.