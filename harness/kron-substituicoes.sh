#!/bin/bash
# KRON-SUBSTITUIÇÕES — ciclo 15 dias (guardrail usuário 2026-08-24)
# Coleta intel multilíngue sobre LLMs candidatos p/ o grafo e registra p/ conflito c/ benchmarks.
OUT="/mnt/dados/cerebro com IA/aprendizados/kron-scouts/kron-$(date +%Y%m%d-%H%M).md"
mkdir -p "$(dirname "$OUT")"
{
echo "# KRON-SCOUT $(date -Is)"
echo
echo "## QUERY SET MULTILÍNGUE (executar com skills websearch/firecrawl/agent-reach)"
cat <<'Q'
- 🇧🇷 pt: "melhor LLM pequeno CPU 2026 criativo raciocínio benchmark" · "LLM ternário bitnet CPU"
- 🇺🇸 en: "best small CPU LLM 2026 agentic creative benchmark" · "BitNet b1.58 native kernels speed"
- 🇪🇸 es: "mejor LLM local pequeño 2026 CPU creativo"
- 🇨🇳 zh: "小模型 CPU 推理 2026 基准"
- 🇯🇵 ja: "ローカルLLM CPU 2026 比較"
- 🇩🇪 de: "bestes lokales LLM 2026 CPU kreativ"
- 🇷🇺 ru: "локальная LLM 2026 CPU бенчмарк"
- Fóruns: r/LocalLLaMA · Hacker News · HF discussions · fóruns BitNet
- YouTube: "small LLM CPU benchmark 2026" · "ternary inference" · "BitNet llama.cpp"
Q
echo
echo "## BASELINES LOCAIS (conflitar TODO achado contra — régua conjunta)"
echo "| slot | modelo | decode t/s medido |"
echo "|---|---|---|"
echo "| GPU :8083 | Ornith-1.5-9B | GM-oficial 76.3 rank#1 |"
echo "| :9086 | lfm2.5-230m | 228 |"
echo "| 🆕:9089 | Ternary-Bonsai-1.7B | 137-207 |"
echo "| :9088 | Qwen3-1.7B | 182.88 (pós-cura) |"
echo "| :9087 | Qwen38-2b | 155 |"
echo "| :9085 | LLMJudge-3b t0.15 | 139 |"
echo "| :9084 | qwen3.5-0.8b | 123 |"
echo "| WARM | Ternary-Bonsai-8B | 125 warm · 44.5 ctx4k · 8.97 frio |"
echo "| WARM :9083 | Bonsai-27B-1bit | 15.72 (F1 criativo eleito) |"
echo
echo "## REGRA DE CONFLITO (filosofia de enxame)"
echo "1 abelha não derruba elefante — ENXAME PROPORCIONAL derruba."
echo "Candidato só entra se bater o ruler da sua função EM NOSSA BANCADA (não vale número de paper)."
echo
echo "## PENDENTES DE INVESTIGAÇÃO (da sessão 2026-08-23/24)"
echo "- bitnet.cpp nativo: realizaria 28-40 t/s teóricos do Ternary-8B? (clang≥18 req.)"
echo "- Qwen38-4B endless-think: testar enable_thinking:false / export oficial"
echo "- Ornith 262K yarn: probe de qualidade além dos 78k chars já validados"
} > "$OUT"
echo "[kron] intel coletada → $OUT"
