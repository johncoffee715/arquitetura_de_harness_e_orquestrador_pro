# Smoke Tests (TIER A) — ornith10-gmb1
**Data:** 2026-08-24 05:30:21 | **Endpoint:** http://127.0.0.1:8083

| Teste | Pass | TPS | Duração | Notas |
|-------|:----:|:---:|:-------:|-------|
| A1_Pelican_SVG | ✅ | 68.34 | 14.98s | svg_valid=True; pelican=True; bike=True |
| A2_Strawberry | ✅ | 70.72 | 7.24s | count_3=True; reasoning=True |
| A3_JSON_Extract | ❌ | 66.81 | 3.83s | parseable=False; values_correct=False; markdown_fence=False |
| A4_Tool_Call | ✅ | 44.34 | 1.31s | tool_call_count=1; json_valid=True; name_args_ok=True |
| A5_Halluc_Guard | ✅ | 64.95 | 2.91s | admits_no_access=True; invented_number=False |

**Total: 4/5**

**Veredito: ⚠️ PARCIAL — investigar testes falhos (quant/template/tool parser)**