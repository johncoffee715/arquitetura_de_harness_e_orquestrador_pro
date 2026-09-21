# Smoke Tests (TIER A) — bonsai27b-1bit-gmb1
**Data:** 2026-08-23 18:56:50 | **Endpoint:** http://127.0.0.1:8083

| Teste | Pass | TPS | Duração | Notas |
|-------|:----:|:---:|:-------:|-------|
| A1_Pelican_SVG | ✅ | 27.64 | 37.05s | svg_valid=True; pelican=True; bike=True |
| A2_Strawberry | ✅ | 27.12 | 18.88s | count_3=True; reasoning=True |
| A3_JSON_Extract | ✅ | 25.75 | 9.94s | parseable=True; values_correct=True; markdown_fence=False |
| A4_Tool_Call | ✅ | 23.68 | 7.1s | tool_call_count=1; json_valid=True; name_args_ok=True |
| A5_Halluc_Guard | ✅ | 26.36 | 9.71s | admits_no_access=True; invented_number=False |

**Total: 5/5**

**Veredito: 🏆 APTO (sem regressão de quantização/template)**