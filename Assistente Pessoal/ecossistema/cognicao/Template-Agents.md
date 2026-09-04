# Template Global — Agents/Subagents/Skills/Tools/MCPs

## Conceito
Template padrão para criação de qualquer componente do Gran-Mestre, baseado nos melhores padrões de Oh-My-Openagents, Superpowers e Fable Method.

---

## Template de Agent

```yaml
---
name: "Nome do Agente"
description: "Descrição curta e precisa"
mode: agent
origin: gran-mestre-original
model: "modelo-específico"  # De acordo com o harness disponível
fallback_models:  # Rotação automática se modelo principal não disponível
  - "modelo-fallback-1"
  - "modelo-fallback-2"
metadata:
  version: "1.0.0"
  created: "YYYY-MM-DD"
  author: "gran-mestre"
  framework: "crossover"  # omO | superpowers | fable | crossover
---

## Identidade
[Descrição clara de quem é o agente e sua função]

## Regras Claras sobre o que NÃO faz
- NÃO faz X
- NÃO faz Y
- NÃO faz Z

## Máximo de Ciclos de Validação
- Máximo: N ciclos
- Após N ciclos: escalar para usuário

## Modo (Autônomo ou Não)
- [ ] Autônomo: executa sem intervenção
- [ ] Interativo: pede confirmação em pontos-chave

## Quando é Chamada
- Quando [condição específica]
- Quando [condição específica]
- Quando [condição específica]

## O que Avalia
- [Critério 1]
- [Critério 2]
- [Critério 3]

## Regras Conforme o Projeto
- Regra 1: [descrição]
- Regra 2: [descrição]
- Regra 3: [descrição]

## O que NÃO Avalia
- NÃO avalia X
- NÃO avalia Y

## Fluxo de Trabalho
1. [Passo 1]
2. [Passo 2]
3. [Passo 3]

## Saída Esperada
- [Saída 1]
- [Saída 2]
- [Saída 3]

## Tags
#agent #gran-mestre #[categoria]
```

---

## Template de Subagent

```yaml
---
name: "Nome do Subagent"
description: "Descrição curta e precisa"
mode: subagent
origin: gran-mestre-original
model: "modelo-específico"
fallback_models:
  - "modelo-fallback-1"
  - "modelo-fallback-2"
metadata:
  version: "1.0.0"
  created: "YYYY-MM-DD"
  author: "gran-mestre"
  framework: "crossover"
  parent_agent: "nome-do-agente-pai"
---

## Identidade
[Descrição clara de quem é o subagent e sua função específica]

## Regras Claras sobre o que NÃO faz
- NÃO faz X
- NÃO faz Y

## Máximo de Ciclos de Validação
- Máximo: N ciclos

## Modo (Autônomo ou Não)
- [ ] Autônomo
- [ ] Interativo

## Quando é Chamado
- Quando [condição específica]

## O que Avalia
- [Critério 1]
- [Critério 2]

## Fluxo de Trabalho
1. [Passo 1]
2. [Passo 2]

## Saída Esperada
- [Saída 1]
- [Saída 2]

## Tags
#subagent #gran-mestre #[categoria]
```

---

## Template de Skill

```yaml
---
name: "nome-da-skill"
description: "Descrição curta e precisa"
mode: skill
origin: gran-mestre-original
metadata:
  version: "1.0.0"
  created: "YYYY-MM-DD"
  author: "gran-mestre"
  framework: "crossover"
  triggers:
    - "trigger-1"
    - "trigger-2"
---

## Objetivo
[Descrição clara do objetivo da skill]

## Quando Usar
- Quando [condição específica]
- Quando [condição específica]

## Fluxo de Trabalho
1. [Passo 1]
2. [Passo 2]
3. [Passo 3]

## Regras Claras
- Regra 1: [descrição]
- Regra 2: [descrição]

## O que NÃO Faz
- NÃO faz X
- NÃO faz Y

## Saída Esperada
- [Saída 1]
- [Saída 2]

## Exemplo de Uso
```
[Exemplo concreto de uso]
```

## Tags
#skill #gran-mestre #[categoria]
```

---

## Template de Tool

```yaml
---
name: "nome-da-tool"
description: "Descrição curta e precisa"
mode: tool
origin: gran-mestre-original
metadata:
  version: "1.0.0"
  created: "YYYY-MM-DD"
  author: "gran-mestre"
  framework: "crossover"
---

## Objetivo
[Descrição clara do objetivo da tool]

## Parâmetros
| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| param1 | string | Sim | Descrição |
| param2 | int | Não | Descrição |

## Retorno
| Campo | Tipo | Descrição |
|-------|------|-----------|
| result | object | Resultado da operação |
| error | string | Erro se houver |

## Exemplo de Uso
```json
{
  "param1": "valor",
  "param2": 123
}
```

## Tags
#tool #gran-mestre #[categoria]
```

---

## Template de MCP

```yaml
---
name: "nome-do-mcp"
description: "Descrição curta e precisa"
mode: mcp
origin: gran-mestre-original
metadata:
  version: "1.0.0"
  created: "YYYY-MM-DD"
  author: "gran-mestre"
  framework: "crossover"
  embedded_in: "nome-da-skill"  # Skill-embedded MCP
---

## Objetivo
[Descrição clara do objetivo do MCP]

## Ferramentas Disponíveis
| Ferramenta | Descrição |
|------------|-----------|
| tool1 | Descrição |
| tool2 | Descrição |

## Recursos Disponíveis
| Recurso | Descrição |
|---------|-----------|
| resource1 | Descrição |
| resource2 | Descrição |

## Configuração
```json
{
  "key": "value"
}
```

## Exemplo de Uso
```
[Exemplo concreto de uso]
```

## Tags
#mcp #gran-mestre #[categoria]
```

---

## Regras Globais

### Para Todos os Componentes
1. **Metadata completa**: name, description, mode, origin, metadata
2. **Modelo específico**: definir modelo principal + fallbacks
3. **Modo claro**: agent, subagent, tool, skill, mcp
4. **Origem**: gran-mestre-original
5. **Regras sobre o que NÃO faz**: sempre documentar
6. **Máximo de ciclos**: sempre definir
7. **Modo autônomo ou não**: sempre definir
8. **Quando é chamado**: sempre documentar
9. **O que avalia**: sempre documentar
10. **Regras conforme projeto**: sempre documentar

### Prioridade de Modelos
1. Modelo específico do harness
2. Modelo fallback 1
3. Modelo fallback 2
4. Modelo genérico (último recurso)

### Rotação Automática
Se modelo principal não disponível:
1. Tentar fallback 1
2. Tentar fallback 2
3. Usar modelo genérico
4. Logar rotação

## Tags
#template #global #gran-mestre #agents #subagents #skills #tools #mcps
