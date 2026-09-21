# Auditoria n_distintos — snn/feather_to_csr.py (2026-09-14)

task_id: snn-audit-ndistintos | run_id: aud-1789421001. Read-only sobre o dataset; sem commit; sem /tmp; sem downloads.

## Veredito

**CAUSA:** `stream_stats` contava a união crua de `body_pre ∪ body_post` sobre todas as
151.856.684 linhas como "neurônios" → **88.384.522**. Esse número = corpos + sites
sinápticos, não neurônios. As colunas misturam duas populações: IDs pequenos de corpos
(<500k) e IDs grandes de sites sinápticos (até 1.571.863.634).

**NÚMERO-VERDADEIRO:** canônico 166.691 corpos (referência MaleCNS v1.0). Melhor proxy
medido no arquivo: união de IDs <500k = **169.736** (+1,8%). A lista exata de 166.691
exige a tabela oficial de corpos — não é derivável do feather por aritmética pura
(varredura de limiares 100k→2M não apresenta platô no canônico; inter pre∩post <500k =
146.647 < canônico).

## Evidências medidas (snn/.venv/bin/python, pyarrow, sem full-table em RAM)

- Schema: `body_pre int64, body_post int64, weight int64`; 2318 batches; total_rows
  **151.856.684**; id_min **10001**; id_max **1.571.863.634**; weight_sum **311.833.243**.
- Amostras: batch 0/1 ordenados por peso desc (2591…92), ~60% IDs <500k, união ~28–38k por
  65k linhas; batch 1159: pre concentrado (187 únicos, 29k–82k = corpos), post BIG
  (só 14,5% <500k), weight=1 em tudo; batch 2317: pre e post BIG (1,5B).
- Categorias (limiar 2M, kernels C++): ambos pequenos **26.443.741**; pre-pequeno/post-BIG
  **113.405.119** (sinapses individuais peso 1, dominante); pre-BIG/post-pequeno
  **4.467.474**; ambos BIG **7.540.350**.
- União IDs pequenos por limiar: 100k→77.102; 200k→124.964; 300k→143.354; 400k→156.988;
  **500k→169.736**; 600k→207.320; 1M/2M→284.568 (sem platô no canônico).
- TH=500k: pre=151.943, post=164.440, interseção=146.647, união=169.736
  (só-pre=5.296, só-post=17.793).

## Correção aplicada: SIM (backup + teste)

- Backup: `snn/.backups/feather_to_csr.py.audit-ndistintos.bak` (pré-fix, md5 8b70d180…).
- Diff backup→atual (só `snn/feather_to_csr.py`): constante `BODY_ID_MAX = 500_000`,
  helper puro `is_body_id`, 2 linhas de `stream_stats` filtradas; `build_csr` intacto
  (semântica CSR preservada). Extra junto: import tolerante pacote/top-level (B1).
- Teste novo: `test_body_id_threshold_separates_sites` — GREEN.
- Suite: `pytest snn/` → **63 passed** (inclui 6/6 em test_feather_csr.py).
  Nota: invocar o arquivo direto sem PYTHONPATH dá ModuleNotFoundError pré-existente de
  sys.path — comportamento do harness, não regressão (canônico `pytest snn/` verde).

exit_status=0
