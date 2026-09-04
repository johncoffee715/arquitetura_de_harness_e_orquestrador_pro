#!/bin/bash
# Gran-Mestre Internet Cognitive Reinforcement
# Sistema de pesquisa na internet como reforço cognitivo

VAULT="/home/johncoffee/ObsidianGranMestre"
TODAY=$(date '+%Y-%m-%d')
NOW=$(date '+%H:%M:%S')

echo "=== Gran-Mestre Internet Cognitive Reinforcement ==="
echo "Data: $TODAY | Hora: $NOW"

# Criar estrutura de pesquisas
mkdir -p "$VAULT/pesquisas/$TODAY"
mkdir -p "$VAULT/referencias/internet"
mkdir -p "$VAULT/fontes"

# 1. Criar log de pesquisas do dia
cat > "$VAULT/pesquisas/$TODAY/log-pesquisas.md" << EOF
# Log de Pesquisas — $TODAY

## Status
- **Data**: $TODAY
- **Hora**: $NOW
- **Gran-Mestre**: Ativo
- **Internet**: Habilitada

## Pesquisas Realizadas
### Manhã
- (Pesquisa 1 — Query: ..., Ferramenta: ..., Resultado: ...)
- (Pesquisa 2 — Query: ..., Ferramenta: ..., Resultado: ...)

### Tarde
- (Pesquisa 3 — Query: ..., Ferramenta: ..., Resultado: ...)
- (Pesquisa 4 — Query: ..., Ferramenta: ..., Resultado: ...)

### Noite
- (Pesquisa 5 — Query: ..., Ferramenta: ..., Resultado: ...)
- (Pesquisa 6 — Query: ..., Ferramenta: ..., Resultado: ...)

## Fontes Consultadas
- (Fonte 1 — URL: ..., Confiança: ...)
- (Fonte 2 — URL: ..., Confiança: ...)

## Descobertas
- (Descoberta 1 — Impacto: ..., Aplicação: ...)
- (Descoberta 2 — Impacto: ..., Aplicação: ...)

## Tags
#pesquisa #internet #gran-mestre #$TODAY
EOF

echo "✅ Log de pesquisas criado"

# 2. Criar referências de internet
cat > "$VAULT/referencias/internet/fontes-confiaveis.md" << EOF
# Fontes Confiáveis — Internet

## Documentação Oficial
- **AMD**: https://www.amd.com/en/support
- **Linux Kernel**: https://www.kernel.org/doc/
- **Arch Wiki**: https://wiki.archlinux.org/

## Fóruns e Comunidades
- **Reddit**: https://www.reddit.com/r/linux/
- **Stack Overflow**: https://stackoverflow.com/
- **GitHub Discussions**: https://github.com/

## Tutoriais e Artigos
- **Medium**: https://medium.com/
- **Dev.to**: https://dev.to/
- **Hashnode**: https://hashnode.com/

## Repositórios de Código
- **GitHub**: https://github.com/
- **GitLab**: https://gitlab.com/
- **Bitbucket**: https://bitbucket.org/

## Confiança por Fonte
- **Oficial**: Alta (documentação do fabricante)
- **Comunidade**: Média (fóruns e discussões)
- **Pessoal**: Baixa (blogs individuais)

## Tags
#fontes #internet #confianca #referencia
EOF

echo "✅ Fontes confiáveis criadas"

# 3. Criar protocolo de pesquisa
cat > "$VAULT/cognicao/Protocolo-Pesquisa-Internet.md" << EOF
# Protocolo de Pesquisa na Internet

## Conceito
A internet é uma fonte externa de conhecimento que complementa a memória persistente.

## Ferramentas Disponíveis

### Web Search
\`\`\`bash
websearch(query="sua busca aqui")
\`\`\`

### Web Fetch
\`\`\`bash
webfetch(url="https://exemplo.com", format="markdown")
\`\`\`

### Context7
\`\`\`bash
context7_resolve-library-id(libraryName="biblioteca", query="documentação")
context7_query-docs(libraryId="/org/biblioteca", query="tópico")
\`\`\`

### Agent Reach
\`\`\`bash
skill(name="agent-reach", user_message="research tópico Reddit")
\`\`\`

### Librarian
\`\`\`bash
task(subagent_type="librarian", prompt="Find código em repositório")
\`\`\`

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
EOF

echo "✅ Protocolo de pesquisa criado"

# 4. Atualizar mapa cognitivo
cat >> "$VAULT/MAPA-COGNITIVO.md" << EOF

## Internet como Reforço Cognitivo — $TODAY
- Protocolo de pesquisa criado
- Fontes confiáveis documentadas
- Ferramentas disponíveis mapeadas
- Regras de pesquisa definidas
EOF

echo "✅ Mapa cognitivo atualizado"

echo ""
echo "=== Internet Cognitive Reinforcement Concluído ==="
echo ""
echo "Arquivos criados:"
echo "  - $VAULT/pesquisas/$TODAY/log-pesquisas.md"
echo "  - $VAULT/referencias/internet/fontes-confiaveis.md"
echo "  - $VAULT/cognicao/Protocolo-Pesquisa-Internet.md"
echo ""
echo "Ferramentas disponíveis:"
echo "  - websearch: Busca geral na web"
echo "  - webfetch: Buscar conteúdo de URLs"
echo "  - context7: Documentação de bibliotecas"
echo "  - agent-reach: Buscar em plataformas específicas"
echo "  - librarian: Buscar em repositórios remotos"
echo ""
echo "Para usar:"
echo "  1. Definir query de pesquisa"
echo "  2. Escolher ferramenta apropriada"
echo "  3. Executar pesquisa"
echo "  4. Documentar descobertas no Obsidian"
echo "  5. Aplicar conhecimento à task"
