# Corpo do OpenCode — Arquitetura

Este documento descreve a arquitetura geral do sistema OpenCode e seus componentes.

## Componentes

- **ECS** (Enhanced Claude Code) — sistema de instalação e gerenciamento de configuração
- **Skills** — módulos de conhecimento especializado carregados sob demanda
- **Agents** — agentes especializados para tarefas específicas
- **Registry** — registro central de capacidades e agentes
- **MCP** — Model Context Protocol para integração com ferramentas externas

## Hierarquia de Configuração

```
~/.opencode/           → Raiz do OpenCode
  skills/              → Skills instalados
  agents/              → Definições de agentes
  commands/            → Comandos customizados
  architecture/        → Documentação arquitetural
  config/              → Configurações
    registry/          → Registro de agentes
    agents/            → Definições de agentes do sistema
```

## Gran-Mestre

O Gran-Mestre é o meta-orquestrador que gerencia o pipeline de desenvolvimento:

1. Prometheus (planejamento)
2. Héstia (validação)
3. Atlas (execução)
4. Atena/Hephaestus (revisão)
