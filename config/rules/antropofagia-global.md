# Antropofagia Tecnologica — Regra Global

## Princípio

Quando um agente de IA **não-OpenCode** for mencionado ou sua solução for apresentada, **devorar criticamente** o componente e **refatorar para OpenCode**.

## Fluxo Obrigatório

1. **Identificar** → Qual agente/ferramenta não-OpenCode está sendo citado?
2. **Extrair** → Qual é a **essência** do componente (não a implementação)?
3. **Refatorar** → Como isso funciona nativamente no OpenCode?
4. **Integrar** → Onde entra no workflow (skill, agent, hook, MCP)?

## Agentes de Referência → Refatoração OpenCode

| Agente/Ferramenta | Componente Devorado | Refatoração OpenCode |
|---|---|---|
| **Claude Code** (Anthropic) | Hooks, Skills, CLAUDE.md | `~/.opencode/skills/`, `~/.opencode/agent/`, `opencode.json` |
| **Cursor** | Rules (.cursorrules), @-commands | `~/.opencode/rules/`, `/commands` |
| **Windsurf** | Memories (.windsurfrules) | `~/.opencode/memory/`, MEMORY.md |
| **Aider** | .aider.conf.yml, repo-map | opencode.json config, `~/.opencode/skills/` |
| **Roo Code** | .roo/rules/, mode switching | `~/.opencode/agent/`, categories |
| **Continue** | .continue/config.json | opencode.json provider config |
| **OpenClaw** | Multi-agent orchestration | oh-my-openagent.json, Sisyphus pipeline |
| **Open Notebook** | Notebook/Source/Note hierarchy | MCP open-notebook, SQLite memory |
| **Oh My Pi** | Hashline patches, hindsight memory | edit tool, persistent context |
| **Cline** | .clinerules, custom instructions | `~/.opencode/rules/`, SKILL.md |
| **Gemini CLI** | GEMINI.md, .gemini/ | AGENTS.md, opencode.json |

## Regras de Implementação

### Sempre que citarem outro agente:

```
1. Perguntar: "Qual é a essência deste componente?"
2. Verificar: "Isso já existe no OpenCode?"
3. Se NÃO existe: Criar skill/agent/rule que faça o mesmo
4. Se PARECE mas é diferente: Criar variante OpenCode
5. Se é IDÊNTICO: Documentar que OpenCode já tem isso
```

### Formato de Entrega

Cada refatoração deve ser:
- **Plug-and-play**: Ctrl+A, Ctrl+C, Ctrl+S
- **Compatível**: Não quebrar config existente
- **Incremental**: Adicionar, não substituir
- **Documentado**: Incluir triggers e exemplos

## Exemplos de Devoração

### Devorando Claude Code:
- **Hooks** → OpenCode hooks (stop-hook, start-hook)
- **Skills** → OpenCode skills (SKILL.md + agent.md)
- **CLAUDE.md** → AGENTS.md + MEMORY.md
- **MCP servers** → opencode.json `mcp` section

### Devorando Cursor:
- **.cursorrules** → `~/.opencode/rules/`
- **@-commands** → `/commands` no opencode
- **Codebase indexing** → graphify skill

### Devorando Open Notebook:
- **Notebook hierarchy** → MCP open-notebook
- **Source management** → SQLite memory engine
- **Dual search** → Full-text + vectorial search

### Devorando Oh My Pi:
- **Hashline patches** → edit tool com content-hash
- **Hindsight memory** → SQLite persistent context
- **Multi-provider router** → oh-my-openagent.json fallback
- **Stream rules** → Real-time reinforcement hooks

## Anti-Padrões

- **NUNCA**: Copiar implementação literal (devorar a essência)
- **NUNCA**: Criar dependência do agente original
- **NUNCA**: Pular a refatoração para OpenCode
- **SEMPRE**: Testar compatibilidade com config existente
- **SEMPRE**: Documentar triggers e casos de uso
