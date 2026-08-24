---
tags: [entity, framework]
domain: ai
status: active
source: https://github.com/can1357/oh-my-pi
---
# Oh My Pi

## Tipo
Framework multi-agent Rust com MCP nativo

## Descrição
Sistema de agentes para Raspberry Pi com:
- Hashline patches (edição confiável)
- Hindsight memory (persistência)
- Multi-provider router
- Stream rules (reinforcement)
- ACP protocol (editor integration)

## Componentes Devorados

### Hashline Patches
- Edição por content-hash
- Evita conflitos de edição
- Refatorado para: edit tool + SHA tracking

### Hindsight Memory
- SQLite persistente
- Project-scoped
- Refatorado para: cerebral-wikia + SQLite

### Multi-Provider Router
- Fallback chains automáticos
- Refatorado para: oh-my-openagent.json

### Stream Rules
- Reinforcement em tempo real
- Refatorado para: hooks do OpenCode

### ACP Protocol
- Integração com editores
- Refatorado para: opencode.json editor integration

## Sinapses
- [[concepts/antropofagia-tecnologica]] — fonte devorada
- [[concepts/delegacao-dinamica]] — multi-provider router → delegação dinâmica
- [[concepts/dev-loop]] — hindsight memory → iteração neural
- [[concepts/ppr-cascade]] — hashline patches → content-hash tracking
- [[decisoes/2026-07-29-otimizacao-neural-obsidian]] — otimizações neurais
- [[decisoes/2026-07-25-gran-mestre-v7-obsidian]] — cérebro neural
- [[entities/gran-mestre]] — orquestrador que absorveu os padrões

## Status
- ✅ Analisado: referências/*.md lidos
- ✅ Refatorado: antropofagia concluída
- ✅ Integração: cerebral-wikia skill
- ✅ Sinapses: 7 links bidirecionais estabelecidos