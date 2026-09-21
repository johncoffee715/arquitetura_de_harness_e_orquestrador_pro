# Protocolo de Pesquisa na Internet

## Conceito
A internet é uma fonte externa de conhecimento que complementa a memória persistente.

## Ferramentas Disponíveis

### Web Search
```bash
websearch(query="sua busca aqui")
```

### Web Fetch
```bash
webfetch(url="https://exemplo.com", format="markdown")
```

### Context7
```bash
context7_resolve-library-id(libraryName="biblioteca", query="documentação")
context7_query-docs(libraryId="/org/biblioteca", query="tópico")
```

### Agent Reach
```bash
skill(name="agent-reach", user_message="research tópico Reddit")
```

### Librarian
```bash
task(subagent_type="librarian", prompt="Find código em repositório")
```

## Protocolo de Pesquisa

### 1. Definir Query
- Identificar o que precisa ser pesquisado
- Formular query específica
- Escolher ferramenta apropriada

### 2. Executar Pesquisa
- Usar ferramenta adequada ao cenário
- Coletar múltiplos resultados
- Filtrar ruído

### 3. Validar Resultados
- Verificar fontes
- Cruzar informações
- Confirmar confiabilidade

### 4. Documentar Descobertas
- Salvar no Obsidian
- Citar fontes
- Atualizar referências

### 5. Aplicar Conhecimento
- Usar na task atual
- Atualizar memória
- Compartilhar insights

## Regras de Pesquisa

### Regra 1: Pesquisar Antes de Implementar
> ANTES de implementar qualquer solução, pesquisar melhores práticas.

### Regra 2: Documentar Fontes
> TODA informação da internet deve ter fonte documentada.

### Regra 3: Validar com Múltiplas Fontes
> INFORMAÇÕES críticas devem ser validadas com 2+ fontes.

### Regra 4: Atualizar Memória
> DESCOBERTAS relevantes devem ser salvas no Obsidian.

### Regra 5: Citar Sempre
> SEMPRE citar fontes ao usar informação da internet.

## Tags
#protocolo #pesquisa #internet #cognicao
