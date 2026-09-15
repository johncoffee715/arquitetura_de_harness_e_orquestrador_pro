# Autofagia: Fallow — MCP/LSP Reviewers

**Data:** 2026-08-03 (Rodada 8 — 26 alvos)
**Fonte:** https://github.com/fallow-rs/fallow (4.2k★, MIT)
**Objetivo:** Absorver **revisores por interface** (MCP + LSP) e padrões de codebase intelligence

---

## 1. O que é

Fallow é ferramenta de **codebase intelligence** para TypeScript/JavaScript (análise estática: código não usado, duplicado, etc.), entregue como **dois servidores**: um **LSP** e um **MCP** — para que agents (Claude Code, Cursor, Copilot) e editores interajam programaticamente. O repo leva `.agents/` com reviewers por interface + rules por crate.

## 2. Padrões absorvidos

- **Revisão de MCP por ergonomia de agente**:
  - naming verb-first descobrível (`analyze`, não `run_dead_code_analysis`)
  - parâmetros com defaults seguros; evitar explosão
  - resposta JSON com arrays `actions` (agente sabe o próximo passo sem re-consultar)
  - erros estruturados com orientação acionável; `_meta` explicativo; idempotência; resolução de binário (env → `.bin` → PATH)
  - **direito de veto (BLOCK)** em tools destrutivas sem approval gate
- **Revisão de LSP por contrato de dados**:
  - `Diagnostic.data` com `{changedSince}` para filtro verificável por ferramentas
  - `cycleId` estável (FNV-1a, rotation-independent) para dobrar squiggles por-arquivo em um ciclo; `edges.len()==files.len()`
  - merge em vez de clobber de `data`
- **Separação de protocolos**: revisor LSP ≠ revisor MCP

## 3. Helenização

- Instalados: `~/.config/opencode/agents/fallow-mcp-reviewer.md` e `fallow-lsp-reviewer.md` (subagents, origem `absorvido:fallow-rs/fallow`)
- Papel no Gran-Mestre: revisão de servidores MCP/LSP próprios e de terceiros antes de absorção

## 4. Aprendizado

O modelo "mesma ferramenta como LSP **e** MCP" é o padrão para expor inteligência de código ao harness: LSP para editores, MCP para agents. Valerá reabsorver o runtime fallow (Rust) como servidor MCP/LSP nativo se o harness passar a consumir análise estática no fluxo.
