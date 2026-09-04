# Gran-Mestre — Protocolo COMPLEX/FEATURE com Internet

## Conceito
Em modos COMPLEX e FEATURE, o acesso à internet é **obrigatório** como reforço cognitivo. Toda task deve passar por pesquisa na internet antes de implementação.

## Modo COMPLEX (7+ passos)

### Fase 1: Pesquisa (Obrigatória)
1. **Web Search**: Buscar contexto geral do problema
2. **Context7**: Buscar documentação de APIs/frameworks
3. **Librarian**: Buscar código de exemplo em repositórios
4. **Agent Reach**: Buscar em fóruns e comunidades
5. **Web Fetch**: Buscar documentação específica

### Fase 2: Planejamento
6. **Prometheus**: Criar plano baseado na pesquisa
7. **Héstia**: Validar plano com fontes externas

### Fase 3: Execução
8. **Atlas**: Executar plano com referências da internet
9. **Hephaestus**: Revisar código com melhores práticas

### Fase 4: Validação
10. **Atena**: Validar com documentação oficial
11. **Fable Judge**: Verificar com fontes externas

### Fase 5: Documentação
12. **Obsidian**: Salvar pesquisa e descobertas
13. **Memória**: Atualizar referências

## Modo FEATURE (Design em aberto)

### Fase 1: Requisitos
1. **Web Search**: Buscar melhores práticas do mercado
2. **Context7**: Buscar padrões de design
3. **Librarian**: Buscar implementações similares

### Fase 2: Design
4. **Prometheus**: Criar design baseado na pesquisa
5. **Héstia**: Validar design com fontes externas

### Fase 3: Especificação
6. **Spec Writer**: Criar spec com referências da internet
7. **Héstia**: Validar spec com documentação oficial

### Fase 4: Implementação
8. **Atlas**: Implementar com código de exemplo
9. **Hephaestus**: Revisar com melhores práticas

### Fase 5: Validação
10. **Atena**: Validar com documentação oficial
11. **Fable Judge**: Verificar com fontes externas

### Fase 6: Documentação
12. **Obsidian**: Salvar design e implementação
13. **Memória**: Atualizar referências

## Ferramentas por Fase

### Pesquisa (Fases 1-3)
| Ferramenta | Uso | Exemplo |
|------------|-----|---------|
| `websearch` | Contexto geral | `websearch(query="Vega 20 overclock")` |
| `context7` | Documentação API | `context7_resolve-library-id(libraryName="amdgpu")` |
| `librarian` | Código de exemplo | `task(subagent_type="librarian", prompt="Find code")` |
| `agent-reach` | Fóruns/comunidades | `skill(name="agent-reach", user_message="research")` |
| `webfetch` | URLs específicas | `webfetch(url="https://...")` |

### Planejamento (Fases 4-5)
| Ferramenta | Uso | Exemplo |
|------------|-----|---------|
| `websearch` | Melhores práticas | `websearch(query="best practices")` |
| `context7` | Padrões de design | `context7_query-docs(libraryId="/org/lib", query="patterns")` |
| `librarian` | Implementações | `task(subagent_type="librarian", prompt="Find implementations")` |

### Execução (Fases 6-8)
| Ferramenta | Uso | Exemplo |
|------------|-----|---------|
| `librarian` | Código de referência | `task(subagent_type="librarian", prompt="Find reference code")` |
| `webfetch` | Documentação | `webfetch(url="https://docs...")` |

### Validação (Fases 9-11)
| Ferramenta | Uso | Exemplo |
|------------|-----|---------|
| `webfetch` | Documentação oficial | `webfetch(url="https://official-docs...")` |
| `websearch` | Múltiplas fontes | `websearch(query="validation")` |

### Documentação (Fases 12-13)
| Ferramenta | Uso | Exemplo |
|------------|-----|---------|
| `Obsidian` | Salvar pesquisa | `obsidian-session-saver.sh save <id>` |
| `memória` | Atualizar referências | `cat >> vault/referencias/...` |

## Regras de Pesquisa em COMPLEX/FEATURE

### Regra 1: Pesquisar Obrigatoriamente
> **ANTES de qualquer implementação, pesquisar na internet.**
> Isso garante uso de melhores práticas e evita erros conhecidos.

### Regra 2: Documentar Todas as Fontes
> **TODA informação da internet deve ter fonte documentada.**
> Isso permite verificação e atualização futura.

### Regra 3: Validar com Múltiplas Fontes
> **INFORMAÇÕES críticas devem ser validadas com 2+ fontes.**
> Isso reduz risco de informações erradas.

### Regra 4: Atualizar Memória Persistente
> **DESCOBERTAS relevantes devem ser salvas no Obsidian.**
> Isso mantém o conhecimento atualizado.

### Regra 5: Citar Sempre
> **SEMPRE citar fontes ao usar informação da internet.**
> Isso dá crédito e permite verificação.

## Exemplo de Fluxo COMPLEX

### Task: Implementar overclock seguro para Vega 20

#### Fase 1: Pesquisa
```bash
# Buscar contexto geral
websearch(query="Vega 20 safe overclock settings 2026")

# Buscar documentação do driver
context7_resolve-library-id(libraryName="amdgpu", query="power management")

# Buscar código de exemplo
task(subagent_type="librarian", prompt="Find amdgpu power management code")

# Buscar em fóruns
skill(name="agent-reach", user_message="research Vega 20 overclock Reddit")

# Buscar documentação específica
webfetch(url="https://www.amd.com/en/support/graphics/amd-radeon-vii")
```

#### Fase 2: Planejamento
```bash
# Criar plano baseado na pesquisa
task(category="deep", prompt="Create overclock plan based on research")

# Validar plano com fontes externas
task(subagent_type="oracle", prompt="Validate overclock plan")
```

#### Fase 3: Execução
```bash
# Executar plano
task(category="unspecified-high", prompt="Execute overclock plan")

# Revisar código
task(subagent_type="code-reviewer", prompt="Review overclock code")
```

#### Fase 4: Validação
```bash
# Validar com documentação oficial
webfetch(url="https://www.amd.com/en/support/graphics/amd-radeon-vii")

# Verificar com fontes externas
task(subagent_type="fable-judge", prompt="Verify overclock implementation")
```

#### Fase 5: Documentação
```bash
# Salvar no Obsidian
cat > ~/ObsidianGranMestre/referencias/vega20-overclock-$(date +%Y-%m-%d).md << EOF
# Vega 20 Overclock — $(date +%Y-%m-%d)

## Pesquisa
- (Fonte 1 — URL: ...)
- (Fonte 2 — URL: ...)

## Implementação
- (Código implementado)

## Validação
- (Validação com fontes oficiais)

## Tags
#vega20 #overclock #pesquisa #$(date +%Y-%m-%d)
EOF
```

## Conclusão

Em modos COMPLEX e FEATURE, o acesso à internet é **obrigatório** como reforço cognitivo. Ao usar todas as ferramentas disponíveis (`websearch`, `webfetch`, `context7`, `librarian`, `agent-reach`), o Gran-Mestre pode:

1. **Pesquisar** documentação atualizada
2. **Validar** decisões com fontes externas
3. **Aprender** com exemplos reais
4. **Atualizar** a memória persistente
5. **Documentar** todas as fontes

**Usar a internet como reforço cognitivo é essencial para o Gran-Mestre funcionar como um sistema de conhecimento completo em modos COMPLEX e FEATURE.**
