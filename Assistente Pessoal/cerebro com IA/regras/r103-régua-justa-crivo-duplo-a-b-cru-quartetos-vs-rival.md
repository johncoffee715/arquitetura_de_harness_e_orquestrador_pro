---
regra: R103
titulo: "GUARDRAIL UNIVERSAL — RÉGUA JUSTA: CRIVO DUPLO A/B (cru × 4-quartetos) CONTRA RIVAL DA STACK"
fonte: user session 2026-09-15
data: 2026-09-15
---

# ═══ REGRA GLOBAL R103 — RÉGUA JUSTA: CRIVO A/B OBRIGATÓRIO (cru × aprimorado vs rival da stack) — promulgado 2026-09-15 ═══

**Regra**: "régua injusta cria julgamento injusto". TODO LLM candidato recebe **dois crivos gêmeos** —
**A (cru)**: zero otimização (sem GBNF, sem quarteto, defaults nus) e **B (aprimorado)**: os 4 quartetos
canônicos aplicados (R85: .md/.json/.py/.gbnf) — e o **rival da stack local** que ocupa/disputa o slot
passa pelas **mesmas duas condições**. O par A/B dos dois lados sintetiza o benchmark mais próximo do
workflow real cotidiano: o sistema opera SEMPRE com quartetos, logo o placar B é o comportamento real;
o placar A mede a matéria-prima. Comparar cru-vs-otimizado cruzado = **inválido**.

<Workflow (fail-closed)>
1. Identificar o rival do slot (ex.: candidato 27B denso ↔ 8083 35B orquestrador).
2. Crivo A nos dois: mesma bateria, mesmo prompt-set, temp, seed, ctx e device-equivalente (mesma classe de hardware; se um roda CPU por falta de VRAM, registrar — R34 exige a nota com a condição).
3. Crivo B nos dois: bateria idêntica + os 4 quartetos ativos.
4. Métricas mínimas por braço: placar R34, Dec t/s, Pre t/s, KV KB/1k, comportamento anti-poison.
5. Delta de canonização: ΔA→B do candidato × ΔA→B do rival — **capacidade de absorver otimização conta** (caso NeoHorse-4B: T2 cedia poison no cru e RECUSOU com quarteto → sinal positivo real).
6. Registro: nota em `benchmarks/` + linha na tabela da verdade com colunas duplas A/B.

<Enforcement>
- Julgamento de candidato com braço faltando (só A, só B, ou rival em condição diferente) = **NAO_PASSOU estrutural do juízo**, não do modelo.
- Modelo novo NUNCA é canonizado (sai da filtragem/) sem o par A/B contra o rival.
- Mesmas otimizações, mesmas condições para ambos — qualquer assimetria invalida a régua.

<Exemplo canônico (2026-09-15)>
- NeoHorse-4B vs Qwen1.5-MoE :9095 — cru: NeoHorse cedia T2 (2+2=5); com quarteto: T2 RECUSOU poison → B reflete o workflow real (stack sempre trilhada) e decidiu a substituição na GPU.

---
