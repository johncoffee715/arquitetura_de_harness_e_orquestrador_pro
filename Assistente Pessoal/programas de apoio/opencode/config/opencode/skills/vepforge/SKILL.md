---
name: vepforge
description: >
  Verifiable Experience Pipeline (VEP) — loop analyze→code→execute→reflect com evidência
  VERIFICADA antes de entrar no Experience (helenizado de huzjie/vepforge, inspirado no Atria
  Dawn 744B). Verificadores: exit_code==0, hash 64-hex, http 2xx, schema JSON, test failed==0,
  stdout não-vazio. Use ao desenhar execução long-horizon autônoma (R16/R37/R49/R89), gates de
  evidência fresca (R29), trânsito categórico (R28) ou pipelines com replay/trajetória.
---

# vepforge — Verifiable Experience Pipeline

## Origem
`github.com/huzjie/vepforge` (inspirado no Atria Dawn Preview 744B). Plataforma de agente
autônomo long-horizon que ancora o loop analyze-code-execute-reflect em ambientes executáveis
reais com trajetória, artefatos e evidência rastreáveis.

## Padrão (o que absorver)

1. **Quatro entidades linkadas**: `Experience` agrega `Task + Trajectory + Artifacts + Evidences`;
   um `Linker` mantém o mapa passo → artefato/evidência (rastreabilidade total).
2. **Evidência verificada ANTES de entrar no store**: resultado de tool passa pelo `Verifier`
   (exit_code/hash/http/schema/test/nonempty) e só então vira `Evidence.verified=true` —
   **impossível falsificar sucesso** (anti-"fake done").
3. **Zero-dependência core**: o motor não depende de LLM/rede; `MockLLM` + tools vazias rodam
   o pipeline end-to-end (testável em CI).
4. **Multi-backend LLM**: `OpenAICompatLLM`/`AnthropicCompatLLM` — troca de modelo sem tocar
   no negócio (nosso R84/R78).

## Verificadores (régua de evidência)

| Verifier | Passa quando |
|---|---|
| ExitCode | exit_code == 0 |
| Hash | 64-hex ou match expected |
| HttpStatus | 2xx |
| Schema | JSON válido na estrutura |
| TestResult | failed == 0 |
| NonEmpty | stdout não-vazio |

## Como usar no harness

- **Gates de entrega (R28/R29)**: antes de um subagente reportar "done", a evidência passa pela
  cadeia de verificadores — exit_code + schema + test_result. Sem `verified=true`, sem veredito.
- **Pipeline long-horizon (R16/R37/R49)**: o loop analyze→code→execute→reflect com trajetória
  persistida = nosso Dev Loop com checkpoint (R10 do modo-autonomo).
- **Replay/recuperação**: Trajectory versionada permite retomar de qualquer passo (R18/R22).
- **Benchmarks**: os 5 tipos de benchmark (automationbench, bfcl, browsecomp, cybergym,
  deepsearchqa) são baterias prontas para avaliar agentes — complementam crivo-padrao (R97/R103).

## Quarteto
- `gabarito.json` — firewall (allow/deny) do pipeline.
- `mecanica.py` — motor determinístico: Verifier chain + Experience/Linker (sem depender do repo).
- `schema.gbnf` — gramática do estado/evidência.
- Este SKILL.md — ontologia.

## Limitações (autofagia)
- O repo é Python; o harness é TS/Node + Python — absorver só o PADRÃO (verificadores + linker),
  não o código inteiro.
- Sandbox Docker do repo é pesado; no harness o sandbox é `/tmp/opencode` + guard-gap-p5.
- Docs em chinês — traduzir conceitos, não copiar.