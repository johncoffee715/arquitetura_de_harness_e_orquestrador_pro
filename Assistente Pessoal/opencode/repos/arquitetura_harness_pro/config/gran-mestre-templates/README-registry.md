# Registry Canônico — Agents / Subagents / Tools / MCP / Skills

Três arquivos:

- **agent-registry.schema.json** — a definição (regras do que todo `entry` precisa ter)
- **agent-registry.example.json** — um exemplo real preenchido por tipo (agent, subagent, mcp, skill, tool)
- este README

## Como usar

1. Copie `agent-registry.example.json` para `agent-registry.json` (esse é o arquivo vivo).
2. Todo novo agent/subagent/tool/mcp/skill que você criar vira um `entry` nesse array — nunca um arquivo solto.
3. Antes de commitar um `entry`, valide contra o schema:

```bash
npx ajv-cli validate -s agent-registry.schema.json -d agent-registry.json
```

4. Campos que **não podem** ficar vazios em nenhum entry: `id`, `tipo`, `status`, `proposito`, `regras.nao_faz`, `autonomia.modo_autonomo`. Se você não consegue preencher `regras.nao_faz`, é sinal de que o escopo da entidade não está definido — pare e defina antes de registrar.

## Mapeamento pro seu sistema atual

| Campo do schema | Onde já existe no seu setup |
|---|---|
| `validacao.gates` | hooks do ECC Autofagia (Safety SHA, Attestation Gate, 2-Action Rule, 3-Strike Protocol, Completion Gate) |
| `categoria_roteamento` | degraus do Gran-Mestre v6.0 (TRIVIAL→CRITICAL/FEATURE) |
| `origem.framework` | oh-my-openagent, superpowers, fable-method, mixture-of-agents, archify |
| `modelo.fallback` | cadeia OmniRoute → OpenCode Go → OpenCode Zen |
| `status: legado` | os 43 agents `gsd-*` (sistema antigo) |
| `status: ativo` | os 27 agents do sistema `build`/ECC atual |

## Diferença deste template para o "template de construção" que você já tinha pedido

O template canônico anterior (metadata completa + modelo/fallback/regras/validação/autonomia) descreve **como construir uma entidade**. Este aqui descreve **como registrá-la depois de construída** — é o índice/banco de dados que o Gran-Mestre consulta em runtime para saber o que existe, o que cada coisa pode fazer e quais gates ela precisa passar. Um `entry` deste registry referencia o arquivo de definição da entidade; não o substitui.

## Próximos passos sugeridos

- **CRÍTICA**: migrar `agent-registry.json` real (Héstia/Atena já mencionadas) para este schema, senão o registry atual e este ficam divergentes.
- **IMPORTANTE**: adicionar validação automática (`ajv`) como pre-commit hook.
- **OPCIONAL**: gerar visualização (via Archify/graphify.js) das `dependencias` entre entries — vira um grafo do sistema inteiro de graça.
- **FUTURA**: expor este registry via MCP próprio, pra qualquer agent poder consultar "quem existe e o que faz" sem hardcode.
