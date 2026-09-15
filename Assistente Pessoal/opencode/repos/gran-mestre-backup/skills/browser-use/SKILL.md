---
name: browser-use
description: "Automação de navegador via AI Agent — absorvido criticamente de browser-use/browser-use (106k★ MIT). Integra Playwright MCP + Gran-Mestre para tarefas web complexas: formulários, scraping, QA, extração."
user-invocable: true
allowed-tools: "Read Write Edit Bash Task"
metadata:
  version: "1.0.0"
  origin: "https://github.com/browser-use/browser-use (MIT)"
  absorbed_at: "2026-07-22"
  antropofagia: "Devorada arquitetura Agent+Controller+Tools+MCP+CLI. Adaptada para ecossistema OpenCode com Gran-Mestre routing."
---

# 🦎 browser-use — Skill de Automação Web para OpenCode

## Origem (Antropofagia Tecnológica)

Esta skill é o resultado da **antropofagia tecnológica** do repositório
[`browser-use/browser-use`](https://github.com/browser-use/browser-use) (106k★, MIT):

| Componente Original | O que absorvemos | Como adaptamos |
|--------------------|-----------------|----------------|
| `Agent()` class | Padrão agente autônomo | Hook OpenCode + task subagent |
| `Controller` + `Tools` | Sistema de custom tools | Integração Playwright MCP |
| DOM History | Histórico de navegação | Logging estruturado |
| MCP module | Server MCP | Bridge para MCP Playwright |
| CLI tool | Comando `/browser` | Slash command OpenCode |
| AGENTS.md | Padrões de integração | Este SKILL.md |

> "Não copiamos. Devoramos, digerimos e transformamos em algo nosso."

## O Que Esta Skill Faz

Permite que o OpenCode **controle um navegador** via AI Agent:
- 📝 **Preencher formulários** — login, cadastro, job applications
- 📊 **Extrair dados** — scraping estruturado para CSV/JSON
- 🧪 **QA Automation** — testar sites, reportar bugs
- 🔍 **Pesquisar** — navegar, coletar informações
- 🤖 **Automação** — qualquer tarefa web repetitiva

## Arquitetura (Antropofágica)

```
browser-use skill (OpenCode)
│
├── SKILL.md              ← Este arquivo (diretrizes + playbook)
├── hooks/
│   └── agent.ts          ← Hook que wrappa agente browser-use
├── templates/
│   └── tasks.md          ← Templates de tarefas comuns
│
└── Integra com:
    ├── MCP Playwright    ← Controle real do navegador
    ├── Gran-Mestre       ← Routing de complexidade
    └── agent-reach       ← Coleta de dados social
```

## Pré-requisitos

```bash
# 1. Playwright MCP (já configurado no seu ecossistema)
# ~/.opencode/mcp-configs/mcp-servers.json já contém:
# "playwright": { "command": "npx", "args": ["-y", "@playwright/mcp"] }

# 2. Verificar instalação Playwright
npx playwright install chromium

# 3. Node.js (já disponível no ambiente)
node --version  # >= 18
```

## Comandos

| Comando | Descrição |
|---------|-----------|
| `/browser <tarefa>` | Executa tarefa no navegador |
| `/browser --record` | Grava sessão para replay |
| `/browser --screenshot` | Tira screenshot da página atual |
| `/browser --extract "seletor"` | Extrai dados estruturados |

Uso:
```
/browser Faça login no Gmail e verifique emails não lidos
/browser --extract ".product-card" Extraia nome, preço e avaliação de cada produto
/browser --screenshot Capture a página inicial
```

## Playbook de Automação

### 1. Formulários

```
1. Navegar para URL
2. Identificar campos (seletor CSS / aria-label / placeholder)
3. Preencher campo por campo
4. Clicar submit
5. Aguardar resposta
6. Verificar resultado
```

### 2. Extração de Dados

```
1. Navegar para página
2. Aguardar carregamento completo
3. Extrair elementos com seletor
4. Estruturar em JSON/CSV
5. Salvar em arquivo
```

### 3. QA Automation

```
1. Navegar para URL alvo
2. Executar fluxo de teste (click → preencher → submit)
3. Capturar screenshot em cada passo
4. Verificar elementos esperados
5. Reportar falhas encontradas
```

## Integração com Gran-Mestre

O Gran-Mestre roteia tarefas de browser para esta skill:

| Complexidade | Tarefa | Ação |
|-------------|--------|------|
| TRIVIAL | "Abrir google.com" | Execução direta |
| SIMPLE | "Pesquisar X no YouTube" | Hook agent.ts |
| MEDIUM | "Extrair dados de 5 páginas" | task subagent |
| COMPLEX | "QA automation completa" | Pipeline Gran-Mestre |

## Segurança

- ⚠️ **Nunca armazenar senhas/credenciais** — usar variáveis de ambiente
- ⚠️ **Nunca executar em produção não autorizada**
- ⚠️ **Sempre verificar URLs antes de navegar**
- ✅ Playwright roda em sandbox isolado
- ✅ Screenshots salvos localmente em `/tmp/browser-use/`

## Exemplos Práticos

### Exemplo 1: Scraping de dados
```
/browse --extract "table tr" Extraia o nome de cada repositório
da página https://github.com/trending e salve em trending.json
```

### Exemplo 2: QA de site local
```
/browser Navegue para http://localhost:3000, clique em "Cadastrar",
preencha o formulário com dados fictícios, submeta e verifique
se a mensagem de sucesso aparece. Reporte qualquer erro.
```

## Origem e Licença

- Repositório original: [browser-use/browser-use](https://github.com/browser-use/browser-use) (MIT)
- Skill derivada sob MIT, com modificações para ecossistema OpenCode
- A antropofagia segue o princípio: absorver o melhor, descartar redundância, criar identidade própria
