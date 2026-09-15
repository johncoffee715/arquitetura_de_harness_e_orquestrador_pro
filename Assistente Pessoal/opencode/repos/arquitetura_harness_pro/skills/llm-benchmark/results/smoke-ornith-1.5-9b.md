# Smoke Tests (TIER A) — ornith-1.5-9b
**Data:** 2026-08-21 08:14:33 | **Endpoint:** http://127.0.0.1:8090

**Telemetria (watcher):** VRAM 11.12 GB | temp 38.0°C | prefill 0.0 t/s

| Teste | Pass | TPS | Duração | Notas |
|-------|:----:|:---:|:-------:|-------|
| A1_Pelican_SVG | ❌ | 71.75 | 14.27s | svg_valid=False; pelican=False; bike=False |
| A2_Strawberry | ✅ | 69.82 | 7.33s | count_3=True; reasoning=True |
| A3_JSON_Extract | ✅ | 57.87 | 1.69s | parseable=True; values_correct=True; markdown_fence=False |
| A4_Tool_Call | ✅ | 41.31 | 1.11s | tool_call_count=1; json_valid=True; name_args_ok=True |
| A5_Halluc_Guard | ✅ | 66.45 | 3.85s | admits_no_access=True; invented_number=False |

**Total: 4/5**

**Veredito: ⚠️ PARCIAL — investigar testes falhos (quant/template/tool parser)**