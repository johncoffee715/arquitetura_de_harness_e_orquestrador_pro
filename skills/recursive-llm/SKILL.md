---
name: recursive-llm
description: "RLM (Recursive Language Model) p/ contexto longo eficiente: contexto vive em REPL Python, modelo explora/particiona recursivamente — 1M+ tokens com menos tokens de LLM e sem context rot. (absorvido de grishahq/recursive-llm)"
origin: absorvido:grishahq/recursive-llm
metadata:
  autofagia: grishahq/recursive-llm (2026-08-10)
  prioridade: 8
  linguagem: Python
  topics: rlm, long-context, repl, token-reduction, context-rot, recursive
  artefatos: skill
  padroes_absorvidos: 6
---
# Recursive LLM (RLM)

Helenizado de [`grishahq/recursive-llm`](https://github.com/grishahq/recursive-llm) — implementação do paper [RLM (arXiv 2512.24601)](https://arxiv.org/abs/2512.24601) por Alex L. Zhang, Tim Kraska e Omar Khattab.

## Propósito
Processamento **eficiente de contexto longo (100k+ até 1M tokens)**: o contexto fica em uma variável Python dentro de um REPL (em vez do prompt), permitindo ao modelo inspecionar partes relevantes, explorar/particionar recursivamente e reduzir o uso de tokens em tasks de contexto grande — evitando **context rot** (degradação de performance com contexto longo).

## Padrões absorvidos (núcleo canônico do repo)
- **Contexto como variável, não prompt**: `rlm.complete(query=..., context=huge_document)` armazena o documento como variável — o modelo faz peek/search/processamento recursivo adaptativo.
- **Recursão e particionamento**: o modelo explora e particiona o contexto recursivamente; busca local + computação substituem re-encode total.
- **Redução de tokens**: usa menos tokens do LLM em tasks adequadas (long-doc → sumarização/extração com busca direcionada).
- **Anti-context-rot**: evita a degradação de performance de prompts monolíticos gigantes.
- **Provider-agnostic**: OpenAI, Anthropic, Ollama, llama.cpp (qualquer endpoint compatível com OpenAI).
- **Benchmarks**: fluxo MedRAG + resultados de benchmark no repo (`BENCHMARK_RESULTS.md`) — medição reproduzível.

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar task de contexto grande (>100k tokens): sumarização/extrato de docs longos, auditoria de logs, análise de repositório inteiro em 1 sessão.
2. Carregar skill (`skill(name="recursive-llm")`).
3. Aplicar: contexto em variável de REPL; deixar o modelo explorar/particionar recursivamente; medir tokens economizados vs. baseline.
4. Caso com ollama/llama.cpp local — alinha com R23 (janela 11776): RLM permite *processar* contexto maior que a janela do servidor.

## Fonte
https://github.com/grishahq/recursive-llm