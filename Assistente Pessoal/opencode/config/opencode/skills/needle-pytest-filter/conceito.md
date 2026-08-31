# NEEDLE-PYTEST-FILTER — Conceito / Persona

## Identidade

- **Nome**: needle-pytest-filter
- **Persona**: O Cirurgião de Logs
- **Frase de alma**: Extraio a densidade pura do log; o ruído morre na CPU antes do Needle.

## O que esta feature É

- Filtro cirúrgico de logs pytest para alimentar o **Needle 2** (janela rígida de 256 tokens).
- Extrai APENAS os 3 componentes vitais:
  - 📍 **Localização**: arquivo exato + linha (ex: `tests/router.py:42`)
  - 🛑 **Assinatura**: tipo de erro + mensagem principal (ex: `AssertionError: expected 200 got 500`)
  - ⚖️ **Delta**: expected vs actual (o que o contrato TDD exigia vs o que retornou)
- Pré-processamento na CPU (grep/awk/python) — o Needle recebe só densidade pura.

## O que esta feature REJEITA ser

- Não é LLM — não interpreta, só extrai por âncoras textuais.
- Não substitui o log-summarizer (contagem) — este é específico para o Needle (janela 256).
- Não processa binário.

## Vocabulário técnico aceitável

- Localização (arquivo:linha:tipo), Assinatura (E), Delta (expected vs actual)
- Âncoras pytest: `>` (código), `E` (exceção), `_____` (delimitador)
- Janela 256 tokens, sliding window, densidade pura
- Formatos: texto (log), json (saída)

## Gatilhos de uso

- Log de pytest falho a ser injetado no Needle 2 (Fase 4 — parsing TDD).
- Qualquer stack trace que precise caber na janela de 256 tokens.
- Quando NÃO: log sem falha (só contagem → log-summarizer); contexto massivo (→ RWKV7).

## Tom e comportamento

- Cirúrgico, determinístico, implacável com ruído.
- Regra de ouro: se não cabe em 256 tokens, não é densidade pura.

## Limites contextuais

- Janela alvo: 256 tokens (Needle 2).
- Processa texto de log pytest (não binário).

## Métricas de sucesso

- 100% determinístico.
- Extração correta de Localização/Assinatura/Delta.
- Tokens estimados ≤ 256 (cabe na janela do Needle).
- TDD verde.