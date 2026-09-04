---
tags: [concept, antropofagia, helenizacao]
related: [[entities/open-notebook]] [[entities/oh-my-pi]] [[entities/gran-mestre]] [[entities/reverser]]
last_updated: 2026-07-29
---
# Antropofagia Tecnológica

## Definição
Adaptação crítica e transformação de tecnologias externas em soluções nativas para OpenCode. Inspirado no movimento Antropofágico de Oswald de Andrade (1928) — "devorar" o estrangeiro para criar algo genuinamente novo.

## Princípio Central
1. **Identificar** — Qual tecnologia estrangeira está sendo citada?
2. **Extrair** — Qual é a essência do componente?
3. **Refatorar** — Como isso funciona nativamente no OpenCode?
4. **Integrar** — Onde entra no workflow (skill, agent, hook, MCP)?

## Tecnologias Devoradas

| Fonte | Componente | Refatoração OpenCode |
|---|---|---|
| Open Notebook | Notebook/Source/Note hierarchy | MCP open-notebook |
| Open Notebook | MCP interface | opencode.json mcp section |
| Oh My Pi | Hashline patches | edit tool |
| Oh My Pi | Multi-provider router | oh-my-openagent.json |
| Oh My Pi | Hindsight memory | SQLite memory |
| LLM Wiki (Karpathy) | Persistent wiki | cerebral-wikia skill |
| Obsidian | Headless vault | /mnt/dados/Assistente Pessoal/cerebro com IA/ |

## Pattern: LLM Wiki
- **Raw sources** → `raw/` (imutável)
- **Wiki** → `wiki/` (persistência)
- **Schema** → `AGENTS.md` (convenções)

## Helenização (Metanoia)
Após devorar, CONVERTER para o padrão OpenCode:
- **Agentes externos** → subagents orquestrados pelo Gran-Mestre
- **Frameworks externos** → skills, MCPs, hooks
- **Protocolos externos** → etapas do pipeline
- **Ferramentas externas** → tools registradas no Registry

### Exemplos de Helenização
| Fonte Original | Helenizado para OpenCode |
|----------------|--------------------------|
| Oh My Pi (agentes multi-provider) | Gran-Mestre orquestra 61 subagents |
| Open Notebook (MCP + wiki) | cerebral-wikia + .manifest.json |
| Claude Code (agentes) | OpenCode subagents descartáveis |
| ChatGPT/Gemini (histórico) | Neurônios em `/aprendizados/` |
| Ghidra (eng. reversa) | reverser subagent |

## Workflow Obrigatório
Sempre que outro agente/ferramenta for citado, aplicar o fluxo de antropofagia + helenização:
1. **DEVORAR** — Extrair essência da tecnologia externa
2. **CONVERTER** — Refatorar para padrão OpenCode (subagent, skill, MCP, hook, tool)
3. **ORQUESTRAR** — Gran-Mestre passa a controlar via Registry
4. **ARQUIVAR** — Criar neurônio em `wiki/entities/` ou `wiki/concepts/`

## Sinapses Atualizadas
- [[entities/oh-my-pi]] — fonte devorada, links bidirecionais ✅
- [[entities/open-notebook]] — fonte devorada, links bidirecionais ✅
- [[entities/gran-mestre]] — orquestrador que aplica antropofagia+helenização
- [[entities/reverser]] — engenharia reversa como ferramenta de antropofagia
- [[concepts/delegacao-dinamica]] — delegação como resultado da helenização
- [[concepts/dev-loop]] — iteração para refinar absorção
- [[concepts/ppr-cascade]] — retrieval neural, absorvido de wiki frameworks
- [[decisoes/2026-07-29-otimizacao-neural-obsidian]] — otimizações como helenização aplicada

---
*Devorado em: 2026-07-16 | Helenização: 2026-07-29*