# Smoke Tests (TIER A) — ornith-1.5-9b-8192
**Data:** 2026-08-21 09:19:42 | **Endpoint:** http://127.0.0.1:8090

**Telemetria (watcher):** VRAM 11.04 GB | temp 37.0°C | prefill 0.0 t/s

| Teste | Pass | TPS | Duração | Notas |
|-------|:----:|:---:|:-------:|-------|
| A1_Pelican_SVG | ❌ | 69.42 | 14.75s | svg_valid=False; pelican=False; bike=False |
| A2_Strawberry | ✅ | 68.61 | 7.46s | count_3=True; reasoning=True |
| A3_JSON_Extract | ✅ | 57.15 | 1.73s | parseable=True; values_correct=True; markdown_fence=False |
| A4_Tool_Call | ✅ | 41.62 | 1.15s | tool_call_count=1; json_valid=True; name_args_ok=True |
| A5_Halluc_Guard | ✅ | 64.28 | 3.28s | admits_no_access=True; invented_number=False |

**Total: 4/5**

**Veredito: ⚠️ PARCIAL — investigar testes falhos (quant/template/tool parser)**