# Gran-Mestre — Acesso à Internet como Reforço Cognitivo

## Conceito
A internet é uma **fonte externa de conhecimento** que complementa a memória persistente do Gran-Mestre. Em modos COMPLEX e FEATURE, o acesso à internet é essencial para:
- Pesquisar documentação atualizada
- Verificar melhores práticas
- Buscar soluções para problemas específicos
- Validar decisões com fontes externas

## Ferramentas Disponíveis

### Web Search
```bash
# Busca geral na web
websearch(query="Vega 20 overclock settings 2026")
```

### Web Fetch
```bash
# Buscar conteúdo de URLs específicas
webfetch(url="https://example.com/docs", format="markdown")
```

### Context7
```bash
# Buscar documentação de bibliotecas/frameworks
context7_resolve-library-id(libraryName="amdgpu", query="power management")
context7_query-docs(libraryId="/org/amdgpu", query="DPM levels")
```

### Agent Reach
```bash
# Buscar em plataformas específicas
skill(name="agent-reach", user_message="research Vega 20 overclock Reddit")
```

### Librarian
```bash
# Buscar em repositórios remotos
task(subagent_type="librarian", prompt="Find Vega 20 power management code in Linux kernel")
```

## Modos de Uso

### Modo COMPLEX (7+ passos)
1. **Pesquisa Inicial**: Usar `websearch` para contexto geral
2. **Documentação**: Usar `context7` para APIs/frameworks
3. **Código**: Usar `librarian` para exemplos reais
4. **Validação**: Usar `webfetch` para fontes específicas
5. **Integração**: Salvar descobertas no Obsidian

### Modo FEATURE (Design em aberto)
1. **Requisitos**: Usar `websearch` para melhores práticas
2. **Arquitetura**: Usar `context7` para padrões
3. **Implementação**: Usar `librarian` para referências
4. **Validação**: Usar `webfetch` para documentação oficial
5. **Documentação**: Salvar no Obsidian como referência

## Integração com Cognição

### Fluxo Cognitivo com Internet

```
┌─────────────────────────────────────────────────────────┐
│                    GRAN-MESTRE                          │
│                    (Cérebro Cognitivo)                  │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  Atenção    │  │  Percepção  │  │   Memória   │     │
│  │  (Foco)     │  │  (Contexto) │  │  (Obsidian) │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │             │
│         └────────────────┼────────────────┘             │
│                          │                              │
│                    ┌─────▼─────┐                        │
│                    │ Raciocínio│                        │
│                    │ (Pipeline)│                        │
│                    └─────┬─────┘                        │
│                          │                              │
│                    ┌─────▼─────┐                        │
│                    │ Linguagem │                        │
│                    │ (Output)  │                        │
│                    └─────┬─────┘                        │
│                          │                              │
│                    ┌─────▼─────┐                        │
│                    │ Internet  │                        │
│                    │ (Reflexo) │                        │
│                    └───────────┘                        │
└─────────────────────────────────────────────────────────┘
```

## Protocolo de Pesquisa

### 1. Atenção (Foco)
- Identificar o que precisa ser pesquisado
- Definir query específica
- Escolher ferramenta apropriada

### 2. Percepção (Contexto)
- Analisar resultados da pesquisa
- Identificar informações relevantes
- Filtrar ruído

### 3. Memória (Armazenamento)
- Salvar descobertas no Obsidian
- Atualizar referências
- Documentar fontes

### 4. Linguagem (Comunicação)
- Sintetizar informações
- Documentar em Markdown
- Citar fontes

### 5. Raciocínio (Decisão)
- Aplicar conhecimento à task
- Validar decisões
- Atualizar memória

## Exemplos de Uso

### Exemplo 1: Pesquisa de Hardware
```bash
# Buscar informações sobre Vega 20
websearch(query="AMD Vega 20 power management Linux 2026")

# Buscar documentação do driver
context7_resolve-library-id(libraryName="amdgpu", query="power management")

# Buscar código de exemplo
task(subagent_type="librarian", prompt="Find amdgpu power management code in Linux kernel")
```

### Exemplo 2: Pesquisa de Overclock
```bash
# Buscar melhores práticas
websearch(query="Vega 20 overclock safe settings 2026")

# Buscar em fóruns
skill(name="agent-reach", user_message="research Vega 20 overclock Reddit")

# Buscar documentação oficial
webfetch(url="https://www.amd.com/en/support/graphics/amd-radeon-vii", format="markdown")
```

### Exemplo 3: Pesquisa de Software
```bash
# Buscar documentação de biblioteca
context7_resolve-library-id(libraryName="Obsidian", query="API documentation")

# Buscar exemplos de uso
task(subagent_type="librarian", prompt="Find Obsidian API usage examples")

# Buscar tutoriais
websearch(query="Obsidian API tutorial 2026")
```

## Integração com Obsidian

### Salvar Pesquisas
```bash
# Criar nota de pesquisa
cat > ~/ObsidianGranMestre/referencias/pesquisa-$(date +%Y-%m-%d).md << EOF
# Pesquisa — $(date +%Y-%m-%d)

## Query
(Tópico pesquisado)

## Resultados
- (Resultado 1 — Fonte: ...)
- (Resultado 2 — Fonte: ...)

## Fontes
- (URL 1)
- (URL 2)

## Aplicação
(Como aplicar à task atual)

## Tags
#pesquisa #referencia #$(date +%Y-%m-%d)
EOF
```

### Atualizar Referências
```bash
# Adicionar à referência existente
cat >> ~/ObsidianGranMestre/referencias/vega20-hardware.md << EOF

## Pesquisa — $(date +%Y-%m-%d)
- (Nova informação — Fonte: ...)
EOF
```

## Regras de Pesquisa

### Regra 1: Pesquisar Antes de Implementar
> **ANTES de implementar qualquer solução, pesquisar melhores práticas.**
> Isso evita erros conhecidos e usa soluções testadas.

### Regra 2: Documentar Fontes
> **TODA informação da internet deve ter fonte documentada.**
> Isso permite verificação e atualização futura.

### Regra 3: Validar com Múltiplas Fontes
> **INFORMAÇÕES críticas devem ser validadas com 2+ fontes.**
> Isso reduz risco de informações erradas.

### Regra 4: Atualizar Memória
> **DESCOBERTAS relevantes devem ser salvas no Obsidian.**
> Isso mantém o conhecimento atualizado.

### Regra 5: Citar Sempre
> **SEMPRE citar fontes ao usar informação da internet.**
> Isso dá crédito e permite verificação.

## Ferramentas por Cenário

### Documentação Oficial
- `context7` — APIs e bibliotecas
- `webfetch` — Documentação específica

### Melhores Práticas
- `websearch` — Artigos e tutoriais
- `agent-reach` — Fóruns e comunidades

### Código de Exemplo
- `librarian` — Repositórios remotos
- `grep_app_searchGitHub` — Código em produção

### Validação
- `webfetch` — Fontes oficiais
- `websearch` — Múltiplas perspectivas

## Conclusão

O acesso à internet é um **reforço cognitivo essencial** para o Gran-Mestre em modos COMPLEX e FEATURE. Ao usar todas as ferramentas disponíveis (`websearch`, `webfetch`, `context7`, `librarian`, `agent-reach`), o Gran-Mestre pode:

1. **Pesquisar** documentação atualizada
2. **Validar** decisões com fontes externas
3. **Aprender** com exemplos reais
4. **Atualizar** a memória persistente
5. **Documentar** todas as fontes

**Usar a internet como reforço cognitivo é essencial para o Gran-Mestre funcionar como um sistema de conhecimento completo.**
