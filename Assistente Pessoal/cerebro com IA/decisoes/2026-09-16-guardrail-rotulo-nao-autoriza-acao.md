# Guardrail universal CANDIDATA — rótulo pequeno nunca autoriza ação (2026-09-16)

> Status: CANDIDATA (promoção a regra numerada exige G4 + ordem do usuário).
> Origem: saga SDD W6-class → few-shot → árbitro :9090 (fronteira chitchat×unknown).
> Precedentes vivos: executor recusou rollback que reintroduzia hazard (asdf→command 0.8)
> e recusou re-sondagem (outcome-shopping) — a cultura já opera assim; aqui se formaliza.

## A regra (3 cláusulas inseparáveis)

1. **Nenhum rótulo confiante de modelo pequeno autoriza ação de efeito.** Intent de
   execução (`command`/`agir`) exige árbitro maior; erro confiante (0.8–0.9) do 0.4B
   é o caso que a cláusula mira (evidência: gibberish→command 0.8, filosofia→vault.query 0.9).
2. **Fail-closed + degradação graciosa.** Árbitro down/lento → `unknown` 0.0, nunca o
   rótulo direto; timeout limitado; `last_path` observável (direct|arbitrated|fallback).
3. **Compensação que reintroduz hazard conhecido é PROIBIDA** — recusar com evidência
   e preservar o `.bak` como prova, não como plano (rollback cego inverte a seta da segurança).

## Refutação pelos 4 selfs (tentativas genuínas de matar a regra)

- **[S-ca] "A regra mata o bootstrap":** exigir :9090 impede scaffolding sem stack completa.
  → SOBREVIVE EMENDADA: arbitragem exigida só com árbitro saudável (health); sem ele,
  fail-closed. Gate de scaffolding (HMI+CSR ativos) independe do árbitro.
- **[H-e] "Hop extra dobra a superfície de crash":** timeout/OOM no :9090 (CPU) derruba o loop.
  → SOBREVIVE: hop com timeout 60s + fail-closed + `last_path`; crash contido vira `unknown`,
  nunca crash do loop. Evidência: smoke 10/10 schema-válidos mesmo com árbitro falhando.
- **[L-e] "Dois modelos = drift duplo + latência no roteamento":** árbitro em 9/10 calls
  encarece a ponte vault→LLM e pode divergir silenciosamente do triador.
  → SOBREVIVE EMENDADA: cláusula de vigilância — medir taxa de acordo triador×árbitro;
  divergência sustentada = alerta de drift, não execução.
- **[A-m] "Enforcement global prematuro bloqueia fluxos legítimos":** grudar a regra no
  guard-gap antes da métrica é melhoria sem gate.
  → SOBREVIVE CONDICIONAL: graduação em 3 degraus — (i) contrato em skill + testes,
  (ii) gate métrico (≥8/10 fronteira + zero gibberish→command), (iii) SÓ ENTÃO
  enforcement global. Hoje: degrau (i), com (ii) pendente (7/10).

## Veredito
Regra SOBREVIVE aos 4 selfs, emendada (degradação + timeout/fail-closed + drift-watch +
graduação). Não-casual = este arquivo + testes + gate métrico antes de qualquer enforcement.
Próximo: fechar gate (ii), aí propor número R + plugin de enforcement.

## Gate (ii) — PASSOU 2026-09-16 (ciclo sdd-gate-20260916-01, verificado GM)
Fix em nível de trigger (não de glossa): `symbol-bypass` (sem letra→unknown, sem arbitrar)
+ `factual-override` (wh-question sem léxico vault/ação/opinião→unknown). Medido: 8/10 no
smoke final do executor, 7/10 no re-run GM — banda estocástica 7–8/10 (temp 0.1 + 2 modelos).
Determinístico em todas as runs (~50+ calls): 100% schema-válidos + **zero gibberish→command**.
Gate passado pelas garantias duras + ≥8 observado; degrau (iii) — enforcement global
(plugin) — PARKED: mudança global de alto risco, modo autônomo pausa aqui por doutrina;
exige ordem explícita.

exit_status: ok
