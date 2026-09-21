# Smoke Tests (TIER A) — qwen38-27b-iq1s-gmb1
**Data:** 2026-08-24 04:59:09 | **Endpoint:** http://127.0.0.1:8083

| Teste | Pass | TPS | Duração | Notas |
|-------|:----:|:---:|:-------:|-------|
| A1_Pelican_SVG | ✅ | 24.32 | 42.11s | svg_valid=True; pelican=True; bike=True |
| A2_Strawberry | ✅ | 28.65 | 14.03s | count_3=True; reasoning=True |
| A3_JSON_Extract | ✅ | 27.07 | 7.54s | parseable=True; values_correct=True; markdown_fence=False |
| A4_Tool_Call | ❌ | 21.18 | 5.33s | tool_call_count=2; json_valid=False; name_args_ok=False |
| A5_Halluc_Guard | ✅ | 27.96 | 9.16s | admits_no_access=True; invented_number=False |

**Total: 4/5**

**Veredito: ⚠️ PARCIAL — investigar testes falhos (quant/template/tool parser)**