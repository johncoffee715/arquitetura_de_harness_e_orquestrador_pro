# AUDITORIA JANELA × RAM — por slot (2026-08-24)

## ⚠️ METODOLOGIA (lição desta auditoria)
Fórmula genérica `L×kv_dim×ctx×bytes` sobre metadados declarados PRODUZIU LIXO
(ex.: 1648 "GiB" para janela 16K do Bonsai — kv_dims declarados heterogêneos/inflados por export).
**Padrão adotado**: valores MEDIDOS quando existem · lacunas marcadas ⚠️ com protocolo de bancada
(`smaps_rollup Anonymous` do processo sob carga real).

## TABELA DE AUDITORIA
| Slot | Modelo | Janela operacional | RAM medida (fonte) | Veredito hardware |
|---|---|---|---|---|
| :8083 GPU | Ornith-1.5-9B-Q4_K_M | **262144 NATIVO** (yarn×2.0) | 16GB total rocm-smi (76%→98% conforme fill) | ✅ validado Adenda 12 · zero-folga em 262K |
| :9083 | Bonsai-27B-1bit | 16384 | ⚠️ pendente smaps-anon sob carga | mede em bancada |
| :9084 | Qwen3.5-0.8b | 131072 | ⚠️ idem · decode 123 t/s medido | mede em bancada |
| :9085 | LLMJudge-3b | 32768 | ⚠️ idem · decode 139 t/s | mede em bancada |
| :9086 | LFM2.5-230m | 128000 | ⚠️ idem · decode 228 t/s 🏆CPU | mede em bancada |
| :9087 | Qwen38-2b | 262144 nat | ⚠️ idem · decode 155 t/s warm | mede em bancada |
| :9088 | Qwen3-1.7B | 32768 | ⚠️ idem · decode 182.88 pós-cura | mede em bancada |
| :9089 | Ternary-Bonsai-1.7B | 8192 | ⚠️ idem · decode 137-207 t/s | mede em bancada |
| :9090 | Ternary-Bonsai-8B | 4096 | ⚠️ idem · decode 44.5 estabilizado · coerência 🏆 warm 125 | mede em bancada |

## LEIS DA AUDITORIA
1. **Metadado declarado ≠ custo real**: geometrias GQA variam por export; só smaps/bancada vale.
2. **KV é lazy**: `-c` define TETO, não alocação upfront — OOM efetivo = preenchimento real + buffers.
3. **Ornith @262K**: única configuração com VRAM medida em ambos os regimes (76% idle-fill / 98% cheio).
