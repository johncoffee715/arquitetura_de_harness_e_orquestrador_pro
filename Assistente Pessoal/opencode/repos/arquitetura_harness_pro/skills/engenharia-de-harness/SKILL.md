---
name: engenharia-de-harness
description: "Canonização da engenharia de harness híbrido (arquivo local 'engenharia de harness.md'): arquitetura Gran-Mestre 6 fases, Model Provider, memória Obsidian, eventos LangGraph, hot-swap assíncrono, alocação de VRAM na MI50 (16GB), gramática GBNF estrita e regras de segurança — fonte viva p/ autofagia contínua do próprio harness."
---

# 🎛️ engenharia-de-harness — Skill de Arquitetura do Harness Híbrido

## Origem (Antropofagia sobre a própria casa)

Esta skill **canoniza o documento-mestre** do harness:
[`/mnt/win1/123 tranqueiras e projetos/engenharia de harness.md`](file:///mnt/win1/123%20tranqueiras%20e%20projetos/engenharia%20de%20harness.md)
(533 linhas). É a fonte de decisões do harness híbrido local/nuvem.

## Mapas-Chave (decididos no doc)

### Camadas de modelo

| Papel no harness | Modelo | Por quê |
|------------------|--------|---------|
| Gran-Mestre (orquestrador) | Ornith-1.0 9B (Q4) ~5.5GB | Self-scaffolding, tools ativas, sem código bruto |
| Auditoria de qualidade/TDD | Nanbeige 4.2 3B 4-bit | Como supervisão na F3/F4 (cobertura, contratos) |
| Checagens binárias | LFM 2.5 1.6B FP8 | Gate Match meio: commit regex, PASSA/FAIL |
| Reescrita de lógica pesada | Bonsai 27B 1-bit ~3.9GB | Quando 2 falhas seguidas de validação |
| Deep review final | MoE nuvem (sob demanda) | Fase 5/6 — auditoria holística p/ latência baixa |

Alocação VRAM: total modelos ~11.9GB; sobra ~4.1GB p/ KV cache.

| Regra prática | Aplicação |
|--------------|-----------|
| **Fases 1-3** não tocam código prod | Busca o SHA em F3 |
| **Fases 4-6** = execução + review + entrega | Commits atômos, evidência |
| **Gates**: usuário aprova 1/2/3 e relatório 4 | Himera humano no vapor |
| **Estado**: `.git_harness_sha` | `git rev-parse HEAD` + `git diff --quiet` |
| **Hot-swap** de modelos no backend é assíncrono | MI50/llama.cpp slots |
| **Memória**: Obsidian MCP server (não nativo do LLM) | "cérebro" do har sn |
| **Roundback**: erro → `git reset --hard $sha` | proteção (máx 1) |
| **Regras globais R1-R17+** | `harness/global-rules.md`; R18 circuit-breaker |

## Uso (para design decisions futuras)

1. Sempre que a task for **alterar o harness** (config, modelos, hooks, skills, MCP, LSP),
   consulte AQUI primeiro as decisões da engenharia original (fatividades em outras regras).
2. **Roteamento (F2)** deve respeitar a matriz acima: Gran-Mestre ≠ exe bruto, etc.
3. **Novas features** precisam ver se quebram as invariantes:
   - E1: Fases 1-3 nunca tocam produção.
   - E2: SHA salvo antes de F4.
   - E3: circuito R18 (disjuntos estagnados).
   - E4: memória cerebral (Obsidian) é MCP/tool, nunca envio de contexto gigante.
4. **É o doc fonte** da visão MIX (tornar todo arsenal compatível: hooks/plugins/skills/
   subagents/MCP/LSP/features conforme task).

## Referência rápida de arquivos do harness

- `harness/core/harness.py` — GranMestreHarness (6 fases/4 gates)
- `harness/harness-config.json` — modelos/rotas
- `harness/registry.json` — catálogo arsenal (hooks/skills/subagents/MCP/LSP/plugins/commands)
- `harness/global-rules.md` — regras globais R1-R18
- `harness/safety/*` — safety protocol + circuit_breaker (R18)
- `opencode/skills/<nome>` — skills helenizadas (padrão SKILL.md)
- `opencode/config/agents/<nome>.md` — subagent helenizado

## Limitações

- A skill é **referência de arquitetura/design**, não executa código.
- Template do doc original assume hardware MI50/HBM2 16GB; o roteador do harness
  degrada quando o hardware difere (não assumir VRAM fixa).