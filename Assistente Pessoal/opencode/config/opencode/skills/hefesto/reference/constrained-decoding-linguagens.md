# Constrained Decoding Fora de Python/C++ — Matriz de Rotas de Implementação

**Artefato**: constrained-decoding-linguagens
**Data**: 2026-08-31
**Autor**: Gran-Mestre (diretriz do usuário)
**Registrado**: decision-log CONSTRAINED-DECODING-LANGUA-2026-08-31
**Relaciona**: R81 (geração restrita universal), R82 (estrangulamento .md/.json/.py/.gbnf), R83 (crivo sistêmico)

---

## Propósito

Para implementar o estrangulamento (Constrained Decoding + FSM no sampler) fora do ecossistema Python/C++,
é preciso linguagens com bindings diretos a motores de inferência (llama.cpp/ONNX) e acesso ao loop de
amostragem para injetar logit bias ou FSM. Matriz das opções profissionais:

## Matriz por Linguagem

| Lang. | Motor/FW | Como faz o estrangulamento | Aderência | Onde se encaixa no harness |
|---|---|---|---|---|
| **Rust** | Candle (HF) / llama_cpp_rs | Manipula tensores + loop de amostragem em zero-cost abstraction; FSM próprio no pipeline; binários estáticos imunes a quebras de venv; syscalls e controle de hardware | Bare-metal; mecatrônica/firmware | Fora do harness atual (sem stack Rust). Futuro: utilitários bare-metal/firmware |
| **Go** | go-llama.cpp / core do Ollama (Go) | Transmite regras GBNF via CGO ao motor C++; goroutines p/ stream sem bloquear; múltiplos LLMs pequenos em paralelo | Orquestração/concorrência | Futuros serviços concorrentes de monitoramento (logs systemd, I/O) — hoje o harness usa processos, não Go |
| **TypeScript/JS** (Bun/Node) | node-llama-cpp | Transpila schema TS→GBNF automática antes do binário C++; WebUI/WebSockets baixa latência | Integração ágil com runtime JS | **ALTO**: plugins/hooks do opencode são TS (guard-gap-p5.ts etc.) — features R81 que rodam no runtime opencode podem usar node-llama-cpp |
| **C#/.NET 8+** | LLamaSharp | API de gramáticas (LlamaGrammar) nativa; desserialização em structs/classes na stack | Enterprise/tipagem rígida | N/A no harness (sem runtime .NET) |

## Análise Técnica (R46) para o harness local

- O stack já roda `llama-server.real` (C++) com interface HTTP: /v1 (OpenAI-compatível) + /completion
  que **aceitam grammar GBNF direto no corpo** — ou seja, o estrangulamento BÁSICO já está disponível via
  HTTP a QUALQUER linguagem de cliente, sem binding CGO necessário.
- Portanto, a escolha de Rust/Go/TS/C# só é RELEVANTE quando: (a) precisar controlar o sampler
  in-process (FSM própria além do GBNF); (b) latência extremamente baixa (<1ms de overhead HTTP);
  (c) a feature roda FORA do servidor (ex.: plugins do opencode, monitores, firmware).
- Para o harness de HOJE: a rota mais ágil é **TypeScript via node-llama-cpp** — as features R81/R82
  que vivem no runtime opencode (plugins/hooks) podem incorporar geração restrita sem sair do JS.
- **Rust** e **Go**: adoção futura, sob demanda (não há código hoje); **C#**: descartado para o harness.

## Decisão e adoção incremental

1. **Agora**: nada de novo no servidor — o grammar HTTP já cobre (validado com granite :9088).
2. **Próxima feature R81 que rodar no runtime opencode** (TS): avaliar node-llama-cpp como executor
   de geração restrita (schema→GBNF) — decisão no momento da feature.
3. **Toda implementação em qualquer linguagem passa pelo crivo sistêmico R83** (Etapa A/B) antes de
   canonizar — memorial comparativo obrigatório.
4. Este documento é a fonte de decisão da matriz (R8: catálogo primeiro — não reinventar).

## Pendências vinculadas

- R81 roadmap itens 3-4-5 (FORJA byte-level, gabarito→Pydantic, config estrito) continuam em Python (bridge).
- Se uma feature exigir FSM própria in-process → avaliar Rust via Candle (documentar no decision-log).