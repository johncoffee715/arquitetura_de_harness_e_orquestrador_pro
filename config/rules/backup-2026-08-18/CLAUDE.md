# CLAUDE.md — Preferências Globais do Usuário

## Idioma (REGRAS GLOBAIS)
- **Toda a comunicação deve ser 100% em português do Brasil (pt-BR)**, de forma global e consistente.
- Isso vale para: respostas, explicações, relatórios, mensagens de status, títulos e qualquer texto voltado ao usuário.
- O código-fonte, identificadores, comandos de terminal e nomes de arquivos permanecem em inglês quando esse for o padrão da tecnologia — mas os comentários e toda a comunicação em linguagem natural devem ser em pt-BR.
- Não misturar idiomas na mesma frase quando puder ser evitado; priorizar pt-BR claro e natural.

## Arquitetura Gran-Mestre (DECISÃO 2026-07-27)

> **O Gran-Mestre é o ÚNICO agent primário e meta-orquestrador.**
> **Todo o resto é subagent disponível para orquestração.**

### Hierarquia
```
GRAN-MESTRE (primário) — ponto de entrada único
  ├── Pipeline Subagents (6): prometheus, hestia, atlas, atena, atreus, code-reviewer
  ├── Crossover Subagents (16): oh-my-openagents, superpowers, fable-method
  ├── GSD Subagents (35): gsd-planner, gsd-executor, gsd-code-reviewer, etc.
  ├── OpenCode Subagents (3): memory-keeper, reverser, general
  └── External Subagents (4): agent-evaluator, build-error-resolver, contextscout, hookify
  TOTAL: 61 subagents
```

### Regras Fundamentais
1. **Gran-Mestre nunca executa direto** — sempre delega para subagent
2. **Subagents são descartáveis** — contexto isolado, sem estado entre invocações
3. **Hierarquia de roteamento** — exata→tipo→classificação→fallback→rejeição
4. **Safety protocol sempre ativo** — SHA→Héstia→Atena→Fable Judge→Rollback

## Projeto atual relevante
- Modding de BIOS UEFI (AMI Aptio) para placa Jingsha X99-D8 (LGA2011-3, C612), chip W25Q128BV (16 MB), programador EZP2019 (`/home/johncoffee/.local/bin/scriba`).
- Worktree principal: `/mnt/dados/projetos/bios e vbios modding/motherboard/mods/jingsha x99-d8/03_grafical_bios_refactor/`
