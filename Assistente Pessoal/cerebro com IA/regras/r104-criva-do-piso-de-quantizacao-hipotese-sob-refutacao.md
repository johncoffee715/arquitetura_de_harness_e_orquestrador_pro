---
regra: R104
titulo: "GUARDRAIL UNIVERSAL — CRIVA DO PISO DE QUANTIZAÇÃO: hipótese sob refutação empírica A/B"
fonte: user session 2026-09-15
data: 2026-09-15
---

# ═══ REGRA GLOBAL R104 — CRIVA DO PISO DE QUANTIZAÇÃO (hipótese "≥4B → Q1 é o limite real" sob refutação) — promulgado 2026-09-15 ═══

**Regra**: nenhum piso de quantização é verdade por apriorismo ("IQ1 é lixo", "Q2 é o mínimo usável").
Hipótese de piso (ex.: "≥4B aguenta Q1 como limite real com quartetos") entra como **conjectura sob
refutação** e só se prova no crivo A/B (R103) com a **evidência empírica da pérola sistêmica**:
quartetos somam +2.6~3.7 pts em 4B+ (e custam em micros ≤1.7B) — `benchmarks/2026-09-15-crivo-AB-consolidado-27b.md`.
Se o piso agressivo + quartetos **resiste** ao rival (ΔB ≤ 0.5 pts vs incumbent/quant-irmão), o piso
**desce** e a otimização **propaga no grafo** (cada nó re-avalia seu próprio piso — cadeia de VRAM).

<Workflow (fail-closed)>
1. Enunciar a conjectura do piso (quant alvo + faixa de params) + rival de referência (irmão de quant mais conservador) + incumbent do slot alvo.
2. Baixar o quant no piso → **filtragem/** (R-guardrail fitragem) — nunca direto na stack.
3. Crivo A/B do quant-piso vs rival-irmão E vs incumbent do slot (mesma bateria, rubrica única vigente).
4. Critério de refutação da conjectura: B(piso) < B(rival) − 0.5 pts  ⇒ piso inviabilizado NESTA família; conjectura rebaixada a "refutada com evidência" (canoniza o fracasso também — aprendizado).
5. Se resiste: piso validado → atualizar manifesto/tabela da verdade → **disparar a mesma criva nos demais nós do grafo** (propagação: nó a nó, nunca em lote cego).

<Enforcement>
- Sem par A/B com evidência jsonl + rubrica vigente registrada = piso não desce, ponto.
- Percepção comunitária ("IQ1_S não presta") NÃO é prova — só o crivo decide.
- Queda de t/s ou KV fora do envelope do slot também conta como refutação (régua é multidimensional: placar + t/s + VRAM).

<Exemplo canônico em curso (2026-09-15)>
- Conjectura: "Qwen3.8-27B ≥4B aceita Q1" → quant-piso: `unsloth/UD-IQ1_S` (6.19 GB) vs irmão `GSQ-RCO-IQ2_XS` (A 2.5 / B 6.2, 7.84 GiB) vs incumbent 8083 (A 3.5 / B 6.2). Se IQ1_S-B ≥ 5.7, piso desce p/ IQ1_S e dispara criva do piso nos demais nós.

---
