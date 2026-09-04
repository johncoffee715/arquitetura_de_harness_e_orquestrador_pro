---
tags: [autofagia, omo-slim, opencode, multi-agente, orquestração, bun, alvinunreal]
categoria: aprendizado
status: absorvido
data: 2026-07-29
fonte: https://github.com/alvinunreal/oh-my-opencode-slim
fonte2: YouTube - "oh-my-opencode-slim é INSANO: 7 IAs se dividindo sozinhas"
fonte3: YouTube - "Spec Driven em 2026: Testei SpecKit, Superpowers, TLC e OpenSpec"
---

# Autofagia — oh-my-opencode-slim

## O que é

Framework de delegação multi-agente para OpenCode por Boring Dystopia Development (alvinunreal). 7 agentes especializados + Council (síntese multi-model), background orchestration, Companion visual opcional.

## Agentes (Panteão)

1. **Orchestrator** (Order) — planeja, roteia, escala, reconcilia resultados. Model: openai/gpt-5.6-terra
2. **Explorer** (Wanderer) — reconhecimento de codebase, arquivo por arquivo. Model: openai/gpt-5.6-luna
3. **Oracle** (Guardian) — arquitetura, trade-offs, debug avançado. Model: openai/gpt-5.6-sol
4. **Council** (Chorus) — roda N modelos em paralelo, sintetiza consenso. Model: config-driver
5. **Librarian** (Weaver) — busca documentação externa via MCPs (websearch, context7, gh_grep). Model: openai/gpt-5.6-luna
6. **Designer** (Guardian of Beauty) — UI/UX, visual excellence. Model: openai/gpt-5.6-luna
7. **Fixer** (Last Builder) — implementação rápida, escopo bem definido. Model: openai/gpt-5.6-luna
8. **Observer** (Silent Witness) — (opcional) multimodal / visual analysis. Model: mimo-v2.5

## Complementaridade com Superpowers

| Superpowers | Omo-Slim | Análise |
|---|---|---|
| Framework de workflow | Framework de delegação | Compatíveis (superpowers Manda & omo-slim executa) |
| brainstorms → plan → SDD | Dispatch paralelo especializado | Superpowers define o plano; omo-slim executa com especialistas |
| Zero dependências | bun + TypeScript + React (Companion) | Superpowers é mais independente; omo-slim mais visual |
| Context guard (ledger disk) | Background task scheduling | Ledger complementa scheduling log; junta autonomia |
| 14 skills de processo | 8 skills (codemap, deepwork, simplify, worktrees, reflect) | Complement em algumas (simplify vs writing-skills) |

## Vantagens Técnicas Absorvíveis

1. **Background orchestration**: dispachar sub-agentes como FG tasks (não bloqueantes) — OpenCode com ACP
2. **Councils**: M obrigatório no processo de decisão (matcha o documento do Orquestrador)
3. **Preset switching**: `/preset openai → /preset opencode-go` runtime — bind this to our config model
4. **Companion window**: GUI: via terminal back (refina experiência visual)
5. **Multiplexer**: Tmux/Zellij integration — observar sub-agentes

## Decisão

**POSITIVO** — será integrado como camada de execução pós-plano (Superpowers define plano e delega a Omo-slim para execução), não como substituto do Orquestrador primário. Potencial de absorção: 75% (a maioria das features são valiosas; council e background tasks especialmente).

## Riscos Rastreáveis

1. **Bun runtime dependency** — omo-slim precisa de bun; mas o opencode.real já bundla bun internamente, então plataforma está pronta
2. **Versão EXCLUSIVA de agentes fixos** — omo-slim define 7 papéis (não permite criar novos sem config, mas isso é ok)
3. **Custo de Council**: executar 3-5 modelos ao mesmo tempo. Usar presets com models free (opencode-go)

## Instalação (futura)

```bash
# OpenCode via bunx (bun incluído no opencode)
bunx oh-my-opencode-slim@latest install --preset=opencode-go

# Update / remote-config management
# Omo-slim já modifica ~/.config/opencode/oh-my-opencode-slim.json
# Isso é compatível com o /run/media/liveuser/Ventoy/opencode/config/ path
```

## Próximos Passos em Autofagia

1. [ ] Instalar o omo-slim lado a lado com superpowers (testar conflito)
2. [ ] Testar delegando planos do superpowers para fixer/designer
3. [ ] Comparar **Council vs single Oracle** no nosso workflow
4. [ ] Criar preset opencode-go com DeepSeek/Kimi/mini previsto do Harness
5. [ ] Documentar flux´ão "Superpowers → Omo-slim" no meta-orquestrador