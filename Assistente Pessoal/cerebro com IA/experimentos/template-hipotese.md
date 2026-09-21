---
data: YYYY-MM-DD
hipotese: >
  (Uma frase refutável no formato "Se X, então Y" — nunca vaga, nunca inquestionável.)
variavel: (A ÚNICA variável manipulada no experimento)
controle: (O que permanece congelado para isolar o efeito da variável)
criterios_refutacao: >
  (Condição PRÉ-DECLARADA, mensurável e binária que, se observada, mata a hipótese.
   Ex: "métrica M não melhora >= N% em S semanas" ou "regressão R aparece".)
self: S-ca            # [S-ca|H-e|L-e|A-m] — exatamente 1: S-ca scaffolding · H-e healing · L-e learning · A-m ameliorative
origem: cientista     # guard 1 (§6): todo artefato do cientista carrega origem: cientista
status: proposto      # [proposto|aprovado|rodando|concluido|fracassado-canonizado]
---

# Hipótese: <título-curto>

> **Fracasso também canoniza (R104).** Veredito "refutado" com método limpo é
> aprendizado registrado, não desperdício. Esconder resultado ruim é que é falha.

## Método
- Protocolo: (passos numerados, determinísticos, reprodutíveis)
- Janela: (semana ISO de execução — YYYY-Www)
- Sandbox: (fitragem/leitura controlada — v1 NÃO toca o path principal)
- Motor: (LLM crivado usado, ou "determinístico-mínimo" se slots down)

## Variáveis
- **Independente (manipulada)**: <variavel> — UMA só, nunca duas.
- **Controle**: <controle> — todo o resto congelado.
- **Dependente (medida)**: (métrica + instrumento + onde o dado fica registrado)

## Resultado
- (Dados brutos observados, sem interpretação. Se ainda não rodou: "—".)

## Veredito
- [ ] Refutado — critério de refutação disparou (canonizar a lição)
- [ ] Não-refutado — sobrevive; re-testar semana seguinte com severidade maior
- [ ] Inconclusivo — documentar por quê (NAO_REFUTADO exige ressalva explícita no gate)

- Lição canonizada: (o que o ecossistema aprende com ESTE resultado, qualquer que seja ele)
- Trilha: decision-log + decisoes/ — gate humano semanal obrigatório: sem gate, nada se aplica.
