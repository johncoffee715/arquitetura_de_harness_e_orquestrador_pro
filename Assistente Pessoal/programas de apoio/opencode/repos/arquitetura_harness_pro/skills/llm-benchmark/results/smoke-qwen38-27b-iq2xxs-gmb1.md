# Smoke Tests (TIER A) — qwen38-27b-iq2xxs-gmb1
**Data:** 2026-08-23 16:53:11 | **Endpoint:** http://127.0.0.1:8083

| Teste | Pass | TPS | Duração | Notas |
|-------|:----:|:---:|:-------:|-------|
| A1_Pelican_SVG | ❌ | 20.91 | 48.97s | svg_valid=False; pelican=False; bike=False |
| A2_Strawberry | ✅ | 20.52 | 12.92s | count_3=True; reasoning=True |
| A3_JSON_Extract | ✅ | 17.5 | 6.06s | parseable=True; values_correct=True; markdown_fence=False |
| A4_Tool_Call | ✅ | 16.61 | 5.84s | tool_call_count=1; json_valid=True; name_args_ok=True |
| A5_Halluc_Guard | ✅ | 19.38 | 9.39s | admits_no_access=True; invented_number=False |

**Total: 4/5**

**Veredito: ⚠️ PARCIAL — investigar testes falhos (quant/template/tool parser)**