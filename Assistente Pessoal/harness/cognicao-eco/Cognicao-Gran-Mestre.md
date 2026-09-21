# Cognição Gran-Mestre

## Conceito
Cognição é a capacidade do cérebro de adquirir, processar, armazenar e usar informações.

## Componentes Cognitivos

### Atenção
Focar em estímulos importantes e ignorar o que atrapalha.
- **Implementação**: Verificar memória persistente PRIMEIRO antes de qualquer task

### Percepção
Dar sentido ao que vemos, ouvimos e sentimos pelo corpo.
- **Implementação**: Analisar contexto da sessão atual + histórico

### Memória
Guardar e lembrar de fatos, dados e experiências.
- **Implementação**: Obsidian como memória persistente global

### Linguagem
Compreender e usar palavras para nos comunicar.
- **Implementação**: Documentação estruturada em Markdown

### Raciocínio
Pensar, criar soluções e tomar decisões.
- **Implementação**: Pipeline Gran-Mestre (Prometheus → Héstia → Atlas)

## Para que serve

### Aprender
Transformar o que acontece ao redor em novos saberes.
- Cada sessão gera aprendizados documentados

### Agir
Decidir o que fazer diante de um problema do dia a dia.
- Delegação inteligente para agentes especializados

### Conviver
Entender o mundo e conversar com as pessoas.
- Comunicação clara em pt-BR

## Arquitetura Cognitiva

```
┌─────────────────────────────────────────────────────────┐
│                    GRAN-MESTRE                          │
│                    (Cérebro)                            │
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
│                    └───────────┘                        │
└─────────────────────────────────────────────────────────┘
```

## Obsidian como Cérebro

### Estrutura do Vault
```
ObsidianGranMestre/
├── sessions/          # Sessões salvas
├── memoria/           # Memória persistente
├── referencias/       # Referências técnicas
├── historico/         # Histórico de decisões
├── analise/           # Análises de dados
└── cognicao/          # Documentação cognitiva
```

### Fluxo Cognitivo
1. **Atenção**: Verificar Obsidian PRIMEIRO
2. **Percepção**: Analisar contexto atual + histórico
3. **Memória**: Salvar aprendizados no Obsidian
4. **Linguagem**: Documentar em Markdown estruturado
5. **Raciocínio**: Usar pipeline Gran-Mestre

## Regra Fundamental

> **ANTES de qualquer task, verificar a memória persistente no Obsidian.**
> Isso evita alucinações e perda de contexto.

## Implementação

### Para o Gran-Mestre
1. Ler `sessions/` para histórico
2. Verificar `memoria/` para decisões anteriores
3. Consultar `referencias/` para documentação
4. Atualizar `historico/` após decisões
5. Salvar `analise/` para dados processados

### Para o Usuário
1. Acessar vault em `~/ObsidianGranMestre/`
2. Navegar por pastas temáticas
3. Usar busca do Obsidian para encontrar informações
4. Adicionar notas manualmente se necessário
