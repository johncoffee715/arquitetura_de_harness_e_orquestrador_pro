---
name: code-review-graph
description: "Local-first code intelligence graph for MCP and CLI. Persistent map of codebase so AI tools read only what matters. (absorvido de tirth8205/code-review-graph)"
---
# Code Review Graph

Helenizado de [`tirth8205/code-review-graph`](https://github.com/tirth8205/code-review-graph).

## Propósito
Local-first code intelligence graph for MCP and CLI. Builds a persistent map of your codebase so AI coding tools read only what matters, with benchmarked context reductions on reviews and large-repo workflows.

## Padrões absorvidos (núcleo canônico do repo)
- Small single-file changes:** Graph context can exceed naive file reads for trivial edits (see express results above). The overhead is the structural metadata that enables multi-file analysis.
- Search quality (MRR 0.35):** Keyword search finds the right result in the top-4 for most queries, but ranking needs improvement. Express queries return 0 hits due to module-pattern naming.
- Flow detection (33% recall):** Framework and conventional entry patterns are strongest for Python and PHP/Laravel. JavaScript and Go flow detection needs work.
- Precision vs recall trade-off:** Impact analysis is deliberately conservative. It flags files that *might* be affected, which means some false positives in large dependency graphs.
- [vs RAG / embeddings](docs/FAQ.md#isnt-this-just-rag) — structural edges parsed from the AST, not similarity chunks; embeddings are optional and only assist search.
- [vs grep / agentic search](docs/FAQ.md#why-not-just-grep) — grep wins on one-hop lookups; the graph wins on multi-hop questions (impact radius, callers-of-callers, tests-for, affected flows).
- [vs Serena, codegraph, claude-context, repomix](docs/FAQ.md#how-does-it-compare-to-serena-codegraph-claude-context-and-repomix) — factual comparison table.
- [When NOT to use it](docs/FAQ.md#when-should-i-not-use-it) — small repos, trivial single-file diffs, one-off questions.

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade que casa com este padrão.
2. Carregar skill (`skill(name="code-review-graph")`) ou subagent (`task(subagent_type="...")`).
3. Aplicar o padrão helenizado ao contexto atual.

## Fonte
https://github.com/tirth8205/code-review-graph
