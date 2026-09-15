# Smoke Tests (TIER A) — ornith-1.5-9b-gmb1
**Data:** 2026-08-23 16:33:49 | **Endpoint:** http://127.0.0.1:8083

| Teste | Pass | TPS | Duração | Notas |
|-------|:----:|:---:|:-------:|-------|
| A1_Pelican_SVG | ❌ | 28.24 | 36.27s | svg_valid=False; pelican=False; bike=False |
| A2_Strawberry | ✅ | 28.81 | 17.77s | count_3=True; reasoning=True |
| A3_JSON_Extract | ✅ | 26.25 | 3.73s | parseable=True; values_correct=True; markdown_fence=False |
| A4_Tool_Call | ✅ | 21.28 | 2.16s | tool_call_count=1; json_valid=True; name_args_ok=True |
| A5_Halluc_Guard | ✅ | 28.68 | 8.75s | admits_no_access=True; invented_number=False |

**Total: 4/5**

**Veredito: ⚠️ PARCIAL — investigar testes falhos (quant/template/tool parser)**