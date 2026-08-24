# /refute-a2a — Ciclo adversarial R40/R41 entre LLMs locais

Executa o ciclo de refutação incansável (R40/R41) entre dois LLMs locais,
gerando scaffolding e self-learning (decision-log).

## Uso

```
/refute-a2a --proponente qwen --refutador qwen-coder --tema "descrição"
/refute-a2a --proponente orchestrator --refutador bonsai --tema "..." --rodadas 3 --log
```

## Argumentos

| Flag | Descrição | Default |
|------|-----------|---------|
| `--proponente` | Modelo que propõe (orchestrator, bonsai, qwen, deepseek, lfm, qwen-coder) | obrigatório |
| `--refutador` | Modelo que refuta (mesmos) | obrigatório |
| `--tema` | Objeto da proposta | obrigatório |
| `--rodadas` | Máx de rodadas adversarial | 3 |
| `--log` | Registra veredito no decision-log | off |

## Mecânica (R40/R41)

1. **Proponente** propõe solução para o tema.
2. **Refutador** avalia com contrato de saída obrigatório (R28/R34):
   `NOTA_R34`, `BUGS_CONCRETOS`, `ELOGIOS_CONCRETOS`, `CORRECOES`,
   terminando com `REFUTADO` ou `IMPRESSIONADO`. Nota nua é proibida.
3. **Parada**: nota ≥ 90 **e** sem falso-positivo (anti-aprovação-burocrática:
   refutação genérica sem ancoragem na proposta é rejeitada — R40).
4. **Ciclo concluído** → veredito registrado no decision-log (self-learning).
5. **Rodadas esgotadas** → escalar (R18) ou revisar tema.

## Aprendizados empíricos embutidos (ciclo 2026-08-16)

- `qwen` (:9084) entra em loop infinito de `reasoning_content` sem
  `chat_template_kwargs: {"enable_thinking": false}` — o script já envia.
- Refutador sem contrato de saída gera texto repetitivo/genérico — o script
  impõe o contrato e detecta repetição ≥3x e falta de ancoragem lexical.

## Backends (ctx-catalog R27)

| Modelo | Porta | Janela |
|--------|-------|--------|
| orchestrator | :8083 | 65.536 |
| bonsai | :9083 | 16.384 |
| qwen | :9084 | 262.144 |
| deepseek | :9085 | 32.768 |
| lfm | :9086 | 128.000 |
| qwen-coder | :9087 | 131.072 |

## Script

`/mnt/dados/harness/safety/refutation_a2a.py`