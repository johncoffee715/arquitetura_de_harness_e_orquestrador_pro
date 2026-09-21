# LOG-SUMMARIZER — Conceito / Persona

## Identidade

- **Nome**: log-summarizer
- **Persona**: O Contador (determinístico, sem LLM)
- **Frase de alma**: Compacto logs de teste em uma linha de verdade; zero gasto de inferência.

## O que esta feature É

- Sumarizador **heurístico determinístico** de logs de ferramentas (pytest, go test, jest, grep, stack traces).
- Conta linhas de erro/warning, PASSED/FAILED, captura primeiro erro/falha.
- Comprime output verboso em resumo compacto (tail N linhas + assinatura + truncamento).
- **Sem chamada LLM** — complementa o RWKV7 cortex (que é para contexto massivo; este é para tool output rotineiro).

## O que esta feature REJEITA ser

- Não é LLM — não raciocina, não interpreta semântica.
- Não substitui o cortex RWKV7 (1M ctx) — é a camada determinística barata.
- Não inventa resumo — só conta e extrai o que existe.

## Vocabulário técnico aceitável

- totalLines, errorLines, warningLines, passCount, failCount
- firstError, firstFailure, tail, signature, truncated
- Padrões: pytest PASSED/FAILED, go test ok/FAIL, jest PASS/FAIL
- Formatos: texto (log), json (saída)

## Gatilhos de uso

- Output de pytest/go test/jest/grep/stack trace para compactar antes de injetar no contexto.
- Qualquer tool output verboso que precise virar resumo de 1 linha.
- Quando NÃO: contexto massivo (1M) → RWKV7 cortex; interpretação semântica → LLM.

## Tom e comportamento

- Determinístico: mesma entrada → mesma saída (testável).
- Regra de ouro: nunca gasta token de LLM para contar linhas.

## Limites contextuais

- maxSummaryLength 400 chars, maxTailLines 12 (defaults).
- Processa texto, não binário.

## Métricas de sucesso

- 100% determinístico (mesma entrada → mesma saída).
- Zero chamada LLM.
- Cobertura de padrões: pytest, go test, jest, error/warning genérico.
- TDD verde.