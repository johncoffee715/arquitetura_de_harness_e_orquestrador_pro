# MAPA MESTRE — MELHOR MODELO POR FUNÇÃO NO GRAFO 0-6
*(2026-08-23 · fonte: GM-oficial full + pernas E/F/A/B + smokes corrigidos + model cards oficiais + medições locais Xeon E5-2699v3/MI50)*

| Função no Grafo | 🏆 Melhor | Evidência numérica | Reserva | ❌ Refutado p/ esta função |
|---|---|---|---|---|
| **F0 Triagem L0** (entrada→rota) | **Needle 2** | ~1500 t/s dispatch · confidence dual-signal · falha=escalão | Ternary-1.7B :9089 (207 t/s texto) | LLMs grandes p/ triagem (desperdício de VRAM) |
| **F0 Watchdog ultra-rápido** | Ternary-Bonsai-1.7B | 207.47 t/s medido vivo · quality duplo ✅ | LFM230m 228 t/s (refutação pura) | Ternary-8B (**8.97 t/s medido** — upcast refuta o "sweet spot" teórico nesta stack) |
| **F1 Ideação criativa** | **Bonsai-27B-1bit** (CPU pesada) ou Ornith (GPU) | Bonsai: único A1 SVG nativo 5/5 · massa paramétrica quebra viés (tese usuário ✓) | Qwen27B ≥96K | IQ1_S (D=50 fraco p/ premissas ricas) |
| **F2 Contrato/spec.md** | **Qwen27B-XXS** (GPU ≥96K) | B-full **8.0/10** 🏆 · estrutura impecável | Qwen38-2b CPU (t=0.3, 155 t/s) | Qwen9B (G crítico em doc formal) |
| **F3 Plano + validação de assinaturas** | **Qwen27B planeja + Needle valida** | B-full 8.0 · Needle: grammar byte-a-byte, unselected=inalcançável | Ornith (B=66.7) | Ternary pequenos (densidade insuficiente p/ plano) |
| **F4 Execução CÓDIGO** | **Qwen9B + verificador obrigatório (§9)** | **D-full 90.0/100 🏆** melhor executor do quarteto | qwen38-2b (t=0.3) | Ornith (D=60) · Qwen27B (D=50) |
| **F4 Dispatch mecânico de tools** | **Needle 2** | ~1500 t/s · tool_index persistente · off-topic=[] ⇒ escalão | — | Qualquer LLM grande (custa VRAM p/ trabalho mecânico) |
| **F5 Revisão MACRO (diff total)** | **Ornith-1.5 @128K** (yarn→262K sob demanda) | F=100 · honesto · janela real medida | Qwen27B @96K (B=100 compensa) | Bonsai/IQ1_S (needle-fail/F❌) · Needle (256 tok) |
| **F6 Veredito/Judge** | **LLMJudge-3b t=0.15** + Ornith sela | Judge dedicado 139 t/s determinístico · G ornith=100 | Qwen27B | Qwen9B (G=0 — jamais julga) |
| **Respostas curtas/exploração rápida** | **Ternary-Bonsai-1.7B :9089** | 207.47 t/s vivo · quality duplo ✅ | LFM230m 228 (refutação) | Ternary-8B |

## LEIS EMPÍRICAS EXTRAÍDAS (refutáveis por nova medição)
1. **Nenhum modelo passa 80 sozinho no full** (ornith 77.9 é o teto) ⇒ ENSEMBLE é a única config que os dados sustentam.
2. **Cada fraqueza de um slot é a força do vizinho**: Qwen9B executa (D=90) mas não julga (G=0); Qwen27B planeja (B=100) mas não executa (D=50); Ornith revisa longos (F=100) mas tropeça em código difícil (D=60).
3. **Quantização ternária em CPU segue curva U-invertida**: 1.7B=163⚡ · 4B=21.7 · 8B=8.97 — upcast aniquila o ganho teórico (caveat AVX2 do model card confirmado localmente).
4. **Reasoning-models exigem dual-field parsing + reasoning-preserve** — sem isso, subnotação sistêmica (caso A1).
5. **RoPE-scale runtime > re-export**: 262K alcançado sem tocar no GGUF.

## COMANDOS DE ATIVAÇÃO POR MODO (registrados)
- Padrão: `start-all-models.sh` (8 slots, sampling por responsabilidade)
- Janela-extrema :8083: `-c 262144 --rope-scaling yarn --rope-scale 2.0` (98% VRAM — health-monitor vigia)
- F4 dispatch: `echo task | harness/needle-dispatch.py` (índice persistente `needle_tool_index.bin`)
