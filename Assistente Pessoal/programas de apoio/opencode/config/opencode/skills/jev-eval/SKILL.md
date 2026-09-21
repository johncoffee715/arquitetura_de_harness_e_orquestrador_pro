---
name: jev-eval
description: >
  Roteador com gate de confiança + métricas de eficiência com distratores (helenizado de
  vinilana/jev-eval-agent, MIT). Padrão: um classificador escolhe a PRÓXIMA tool entre N opções
  (expondo só 1 tool ao LLM por passo) e um gate "done" bloqueia respostas prematuras.
  Métricas: completion, efficiency (completion × ideal/calls × 0.5 se distrator), distractorCalls,
  idealPath, custo estimado. Use ao desenhar roteamento de tools (R65), evals de agente (R97/R103)
  ou comparar "LLM escolhe tool" vs "classificador escolhe tool".
---

# jev-eval — Roteador com gate de confiança + eval com distratores

## Origem
`github.com/vinilana/jev-eval-agent` (MIT) — agente pessoal com 100 tools mock, servido via
OpenRouter; compara `llm-direct` (LLM vê 100 tools) vs `jev-classifier` (classificador escolhe a
tool, LLM só preenche args). 6 tasks PT-BR × 8 modelos × 2 modos, resultados versionados.

## Padrão de roteamento (o que absorver)

1. **Estado compacto** por passo: `{ user_request, actions_taken[], assistant_said[] }` derivado do
   histórico — clip de 600 chars por resultado, 300 por fala.
2. **Classificador escolhe** `next_tool` (choice sobre N tools + `respond_to_user`) e `done` (noul:
   "toda ação pedida já está em actions_taken?").
3. **Gate de confiança**: se `respond_to_user` mas `done < threshold` (default 0.5) → bloqueia a
   resposta e expõe a próxima melhor tool (top-1 não-respond). Toda decisão vira trace
   (choice, confidence, done, top-5, latency, gated).
4. **Exposição mínima**: no modo classificador, só a tool escolhida é exposta ao LLM por passo —
   o LLM preenche argumentos, não navega o catálogo.

## Métricas (o que medir)

- `completion` = famílias obrigatórias cobertas / total (família = conjunto de tools equivalentes).
- `efficiency` = completion × (ideal / calls) × (0.5 se chamou distrator).
- `distractorCalls` = chamadas a tools com nome parecido (flights_hold × flights_book, etc.).
- `idealPath` = completion==1 && extra==0 && distractor==0 && failed==0.
- `usage` = tokens in/out + custo estimado (preço público do provider).

## Como usar no harness

- Roteamento: aplicar o gate de confiança no nosso roteador híbrido (R65) — o classificador
  (RWKV :9084 / Needle) escolhe a tool, o LLM denso só argumenta.
- Eval: adaptar as 6 tasks PT-BR (p1-marina, p2-voo-sp, p3-orcamento, p4-viagem, p5-reuniao,
  p6-financas) como bateria de agente com distratores — complementa o crivo-padrao (R97/R103).
- Comparação: rodar `llm-direct` vs `classifier` nos nossos slots locais e registrar no
  benchmarks/ com a régua R103 (mesmas condições, mesmo prompt).

## Serviço Batedor (decisões tipadas com LLM barato — 2026-09-18)

Instanciação do padrão Jev validado em campo (vídeo ae92ibehs4Q, Hora de Codar): o batedor
**NUNCA gera texto, código ou explicação** — só devolve decisões tipadas (diretriz do usuário).
Em produção pode ser **LLM barato dedicado** (:9086 LFM-1.2B local 317 t/s; omniroute free como
HA — R20/R23), não o denso.

- **Contrato por mensagem** (GBNF-estrito, constrained decoding R81/R82 — schema, não prompt):
  `{rota: enum, topicos: [≤3], urgente: bool, confianca: 0.0-1.0, needs_dense: bool}`.
- **Gate de confiança 0.6** (evidência Jev: "confiança < 0.6 → revisar manualmente"):
  abaixo disso ⇒ marca o turno p/ revisão (log + flag), NUNCA silencia nem inventa.
- **needs_dense=false** ⇒ resolve na camada barata (L0 needle / L0.5 RWKV7); **true** ⇒ acorda
  LLMs densos (F1/F2) já com trabalho triado. Nenhuma prosa do batedor chega ao usuário.
- **Métricas**: as da própria skill (completion, efficiency, distractorCalls) + `gated_rate`
  (% turnos bloqueados pelo 0.6) — registrado em benchmarks/ para o cientista (R106).
- **Implementação**: PENDENTE A2A/executor (runtime 429 em 2026-09-18) — esta seção é o contrato.

## Quarteto
- `gabarito.json` — firewall (allow/deny) do roteador.
- `mecanica.py` — motor determinístico: buildState, gate, métricas (sem depender do SDK).
- `schema.gbnf` — gramática do estado/decisão.
- Este SKILL.md — ontologia.

## Limitações (autofagia)
- O SDK `@typesafe-ai/sdk` (TypeSafe/Jev) é serviço externo; no harness local o classificador é
  substituível (RWKV/Needle). O stub (`JEV_STUB=1`) mostra o contrato offline.
- 100 tools mock = mundo determinístico; adaptar o catálogo ao nosso arsenal real.
- Custo estimado usa preço público; recalibrar com nossos preços locais (R78).