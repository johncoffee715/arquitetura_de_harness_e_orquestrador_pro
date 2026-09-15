# Sessão encerrada — 2026-09-14 (auditoria fair-crivo + guardrail universal)

## Pérolas quantitativas
- Crivo /7 (T6/T1/T2/T4/T8/T10/T11): topo geral AD-IQ3_S 3.4 (RAW) · stack: 8083 3.3 · 9088 3.2 · 9090/9095-mitigado 3.0 · 9092 2.7 · 9093 2.0 · coder-3b 1.7 · 9084 0.0 · 9086 N/A
- Candidatos lixeira: DT-IQ3_XXS 2.5 · bs-IQ3_S 2.2 (T10 fabricação) · neo4B-Q5-ret 2.7 · noemaQ8 1.0 · NH9B-Q5 2.7 pós-Fase B
- Fase B: extrator .py 6 recuperações wrapper · rerun GBNF T6/T11 **16/16 byte-exato** (incl. RWKV e LFM)
- Nenhum modelo ≥ GM 6.0, nem mitigado. Registry: 52 modelos. Decision-log: 332 entradas. Evidências: 103 arquivos (2026-09-13).

## Pérolas qualitativas (R28)
- Tese R85 confirmada ao vivo: grammar física salva qualquer modelo (coder-3b livre 1.2 → com trilho confiável).
- Fabricação (T10) desqualifica mais que placar baixo: bs-IQ3_S 2.2 descartado por inventar registry.
- Ground-check `17:20` é cego a `17h20` — T4 do 8083 perfeito marcou 0 no ground (verificação humana prevalece).
- Thinking-models (LFM) queimam budget em reasoning sem emitir content; cura R57 = G4, nunca mid-pipeline.
- Guardrail universal promulgado: Fase A base (chat template-correto) + Fase B quarteto-mitigação, mesmos artifícios p/ todos.
- Recovery stack: `harness/stack-recovery-2026-09-14.sh` (8 cmdlines exatas; :9094/:9097 embedders fora — DOWN pré-auditoria).
