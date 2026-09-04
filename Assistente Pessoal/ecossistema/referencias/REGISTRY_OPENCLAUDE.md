# REGISTRY — OpenClaude Components
## Data: 2026-07-27 | Autofagia de Gitlawb/openclaude v0.26.0

---

## Agents/Subagents

### oc-fork-worker
```json
{
  "id": "oc-fork-worker",
  "tipo": "subagent",
  "nome": "Fork Worker (OpenClaude)",
  "versao": "1.0.0",
  "status": "ativo",
  "origem": {
    "tipo_origem": "framework-externo",
    "framework": "openclaude",
    "repo_url": "https://github.com/Gitlawb/openclaude",
    "adaptacoes": [
      "Fork implícito: omitir subagent_type ativa herança de contexto",
      "Prompt cache sharing com prefixes byte-idênticos",
      "Rules do fork child: NÃO spawnar sub-agents, executar diretamente"
    ]
  },
  "proposito": "Worker forked que herda contexto completo do pai. Executa task diretamente e reporta structured facts.",
  "categoria_roteamento": "COMPLEX",
  "modelo": {
    "primario": "inherit",
    "fallback": ["auto/coding", "auto/reasoning"],
    "provider": "omniroute"
  },
  "capacidades": [
    "Herda contexto completo do agente pai",
    "Executa tools diretamente (Bash, Read, Write, Edit)",
    "Reporta: Scope/Result/Key files/Files changed/Issues",
    "Commita mudanças antes de reportar"
  ],
  "regras": {
    "nao_faz": [
      "NÃO spawn sub-agents (já É um fork)",
      "NÃO conversa ou faz perguntas",
      "NÃO adiciona meta-comentário",
      "NÃO emite texto entre tool calls"
    ],
    "escopo_maximo": "Declarado pelo directive do pai"
  },
  "validacao": {
    "gates": ["safety-sha", "completion-gate"],
    "tdd_obrigatorio": false,
    "fase_pipeline": "Fase 4 (Execução)"
  },
  "autonomia": {
    "modo_autonomo": true,
    "condicoes": ["directive válido do pai"]
  },
  "dependencias": {
    "subagents": [],
    "mcps": [],
    "skills": [],
    "hooks": []
  },
  "registrado_em": "2026-07-27",
  "atualizado_em": "2026-07-27",
  "notas": "Fork herda prompt cache do pai para maximizar cache hits. Guard contra fork recursivo via detecção de fork boilerplate tag."
}
```

### oc-coordinator
```json
{
  "id": "oc-coordinator",
  "tipo": "agent",
  "nome": "Coordinator Mode (OpenClaude)",
  "versao": "1.0.0",
  "status": "ativo",
  "origem": {
    "tipo_origem": "framework-externo",
    "framework": "openclaude",
    "repo_url": "https://github.com/Gitlawb/openclaude",
    "adaptacoes": [
      "Gran-Mestre já usa este padrão — refinamento com workers autônomos",
      "Coordinator não executa código — apenas orquestra"
    ]
  },
  "proposito": "Modo especial onde o agente principal vira coordinator e spawna workers autônomos para execução paralela.",
  "categoria_roteamento": "CRITICAL",
  "modelo": {
    "primario": "auto/coding",
    "fallback": ["auto/reasoning", "auto/coding:reliable"],
    "provider": "omniroute"
  },
  "capacidades": [
    "Orquestra workers autônomos",
    "Não executa código diretamente",
    "Workers têm tools próprias",
    "Explore/Plan são read-only workers"
  ],
  "regras": {
    "nao_faz": [
      "NÃO executa código de produção",
      "NÃO interfere nos workers durante execução"
    ],
    "requer_aprovacao_humana_para": ["mudanças em config core"]
  },
  "validacao": {
    "gates": ["safety-sha", "attestation-gate"],
    "tdd_obrigatorio": false
  },
  "autonomia": {
    "modo_autonomo": true,
    "condicoes": ["rota >= COMPLEX"]
  },
  "dependencias": {
    "subagents": ["oc-fork-worker"],
    "mcps": [],
    "skills": [],
    "hooks": []
  },
  "registrado_em": "2026-07-27",
  "atualizado_em": "2026-07-27"
}
```

---

## Tools

### oc-repo-map
```json
{
  "id": "oc-repo-map",
  "tipo": "tool",
  "nome": "Repo Map (OpenClaude)",
  "versao": "1.0.0",
  "status": "ativo",
  "origem": {
    "tipo_origem": "framework-externo",
    "framework": "openclaude",
    "repo_url": "https://github.com/Gitlawb/openclaude",
    "adaptacoes": [
      "Tree-sitter parsing → symbol extraction → PageRank ranking",
      "Cache em disco para re-consultas instantâneas",
      "Suporta TypeScript, JavaScript, Python"
    ]
  },
  "proposito": "Mapa estrutural do repositório ranqueado por importância (PageRank). Extrai funções, classes, tipos e interfaces.",
  "modelo": { "primario": "n/a" },
  "capacidades": [
    "Parsing com tree-sitter",
    "Extração de símbolos (funções, classes, tipos)",
    "Grafo de referências cross-file",
    "Ranking por PageRank (importância estrutural)",
    "Output token-budgeted",
    "Focus files/symbols para boost"
  ],
  "regras": {
    "nao_faz": ["não modifica código", "não mostra bodies — só signatures"]
  },
  "validacao": { "gates": ["nenhum"] },
  "autonomia": { "modo_autonomo": true, "condicoes": [] },
  "dependencias": {},
  "registrado_em": "2026-07-27",
  "atualizado_em": "2026-07-27",
  "notas": "Complementar ao graphify. Usar no início de sessões em repos desconhecidos."
}
```

### oc-team-create
```json
{
  "id": "oc-team-create",
  "tipo": "tool",
  "nome": "Team Create (OpenClaude)",
  "versao": "1.0.0",
  "status": "ativo",
  "origem": {
    "tipo_origem": "framework-externo",
    "framework": "openclaude",
    "repo_url": "https://github.com/Gitlawb/openclaude",
    "adaptacoes": [
      "Team = TaskList (1:1 correspondence)",
      "Persistência em ~/.openclaude/teams/ e ~/.openclaude/tasks/"
    ]
  },
  "proposito": "Cria equipes de agents com task lists persistentes para projetos complexos.",
  "modelo": { "primario": "n/a" },
  "capacidades": [
    "Criar equipe com nome e descrição",
    "Criar task list associada",
    "Persistir config em disco"
  ],
  "regras": {
    "nao_faz": ["não destrói teams existentes sem confirmação"]
  },
  "validacao": { "gates": ["nenhum"] },
  "autonomia": { "modo_autonomo": true, "condicoes": [] },
  "dependencias": {},
  "registrado_em": "2026-07-27",
  "atualizado_em": "2026-07-27"
}
```

### oc-websearch-multi
```json
{
  "id": "oc-websearch-multi",
  "tipo": "tool",
  "nome": "WebSearch Multi-Provider (OpenClaude)",
  "versao": "1.0.0",
  "status": "ativo",
  "origem": {
    "tipo_origem": "framework-externo",
    "framework": "openclaude",
    "repo_url": "https://github.com/Gitlawb/openclaude",
    "adaptacoes": [
      "9 backends: DuckDuckGo, Firecrawl, Exa, Brave, Bing, Jina, Mojeek, Tavily, You.com",
      "DuckDuckGo como fallback gratuito",
      "Firecrawl para páginas JS-rendered"
    ]
  },
  "proposito": "Busca web multi-provider com fallback chain para máxima cobertura.",
  "modelo": { "primario": "n/a" },
  "capacidades": [
    "DuckDuckGo (free, default)",
    "Firecrawl (JS-rendered pages)",
    "Exa (semantic search)",
    "Brave Search",
    "Bing",
    "Jina",
    "Mojeek",
    "Tavily",
    "You.com",
    "Custom (user-defined)"
  ],
  "regras": {
    "nao_faz": ["não envia dados sensíveis para providers externos"]
  },
  "validacao": { "gates": ["nenhum"] },
  "autonomia": { "modo_autonomo": true, "condicoes": [] },
  "dependencias": {},
  "registrado_em": "2026-07-27",
  "atualizado_em": "2026-07-27",
  "notas": "Integrar com agent-reach. Fallback chain: Exa → Brave → DuckDuckGo."
}
```

### oc-cron-scheduler
```json
{
  "id": "oc-cron-scheduler",
  "tipo": "tool",
  "nome": "Cron Scheduler (OpenClaude)",
  "versao": "1.0.0",
  "status": "experimental",
  "origem": {
    "tipo_origem": "framework-externo",
    "framework": "openclaude",
    "repo_url": "https://github.com/Gitlawb/openclaude",
    "adaptacoes": [
      "CronCreate, CronDelete, CronList tools",
      "Jitter config para evitar thundering herd"
    ]
  },
  "proposito": "Agendamento de tasks recorrentes via cron.",
  "modelo": { "primario": "n/a" },
  "capacidades": [
    "Criar agendamentos cron",
    "Listar agendamentos ativos",
    "Deletar agendamentos",
    "Jitter para evitar sobrecarga"
  ],
  "regras": {
    "nao_faz": ["não agenda tasks destrutivas sem aprovação"]
  },
  "validacao": { "gates": ["nenhum"] },
  "autonomia": { "modo_autonomo": false, "condicoes": ["requer aprovação humana"] },
  "dependencias": {},
  "registrado_em": "2026-07-27",
  "atualizado_em": "2026-07-27",
  "notas": "Usar para: audits periódicos, syncs de memória, backups."
}
```

---

## Skills

### oc-background-sessions
```json
{
  "id": "oc-background-sessions",
  "tipo": "skill",
  "nome": "Background Sessions (OpenClaude)",
  "versao": "1.0.0",
  "status": "ativo",
  "origem": {
    "tipo_origem": "framework-externo",
    "framework": "openclaude",
    "repo_url": "https://github.com/Gitlawb/openclaude",
    "adaptacoes": [
      "--bg flag para sessões desacopladas",
      "ps/logs/kill para gerenciamento"
    ]
  },
  "proposito": "Rodar tasks em background desacopladas do terminal.",
  "modelo": { "primario": "n/a" },
  "capacidades": [
    "Executar task em background",
    "Listar sessões ativas",
    "Ver logs de sessão",
    "Terminar sessão"
  ],
  "regras": {
    "nao_faz": ["não destrói sessões sem confirmação"]
  },
  "validacao": { "gates": ["nenhum"] },
  "autonomia": { "modo_autonomo": true, "condicoes": [] },
  "dependencias": {},
  "registrado_em": "2026-07-27",
  "atualizado_em": "2026-07-27",
  "notas": "Equivalente a task(run_in_background=true) no Gran-Mestre."
}
```

### oc-provider-profiles
```json
{
  "id": "oc-provider-profiles",
  "tipo": "skill",
  "nome": "Provider Profiles (OpenClaude)",
  "versao": "1.0.0",
  "status": "ativo",
  "origem": {
    "tipo_origem": "framework-externo",
    "framework": "openclaude",
    "repo_url": "https://github.com/Gitlawb/openclaude",
    "adaptacoes": [
      "Profile system com guided setup via /provider",
      "200+ providers suportados"
    ]
  },
  "proposito": "Sistema de profiles para providers LLM com setup guiado.",
  "modelo": { "primario": "n/a" },
  "capacidades": [
    "Guided setup de providers",
    "Salvar profiles em ~/.openclaude-profile.json",
    "Auto-routing por modelo",
    "Fallback chain entre providers"
  ],
  "regras": {
    "nao_faz": ["não expõe credenciais em logs"]
  },
  "validacao": { "gates": ["safety-sha"] },
  "autonomia": { "modo_autonomo": true, "condicoes": [] },
  "dependencias": {},
  "registrado_em": "2026-07-27",
  "atualizado_em": "2026-07-27",
  "notas": "Expandir model_rotation existente para multi-provider."
}
```

### oc-doctor-runtime
```json
{
  "id": "oc-doctor-runtime",
  "tipo": "skill",
  "nome": "Doctor/Runtime (OpenClaude)",
  "versao": "1.0.0",
  "status": "ativo",
  "origem": {
    "tipo_origem": "framework-externo",
    "framework": "openclaude",
    "repo_url": "https://github.com/Gitlawb/openclaude",
    "adaptacoes": [
      "Health checks de providers e reachability",
      "Privacy verification (sem phone-home)",
      "PR intent scan"
    ]
  },
  "proposito": "Diagnósticos de saúde do harness e verificação de privacidade.",
  "modelo": { "primario": "n/a" },
  "capacidades": [
    "Verificar providers e reachability",
    "Verificar sem phone-home",
    "Scan de segurança em PRs",
    "Output JSON para automação"
  ],
  "regras": {
    "nao_faz": ["não envia dados para serviços externos"]
  },
  "validacao": { "gates": ["nenhum"] },
  "autonomia": { "modo_autonomo": true, "condicoes": [] },
  "dependencias": {},
  "registrado_em": "2026-07-27",
  "atualizado_em": "2026-07-27",
  "notas": "Complementa o gsd-health existente."
}
```

---

## MCPs

### oc-grpc-server
```json
{
  "id": "oc-grpc-server",
  "tipo": "mcp",
  "nome": "gRPC Server (OpenClaude)",
  "versao": "1.0.0",
  "status": "experimental",
  "origem": {
    "tipo_origem": "framework-externo",
    "framework": "openclaude",
    "repo_url": "https://github.com/Gitlawb/openclaude",
    "adaptacoes": [
      "Bidirectional streaming gRPC service",
      "Proto definition: src/proto/openclaude.proto"
    ]
  },
  "proposito": "Expor capacidades do agente como serviço gRPC headless para integração com CI/CD e UIs.",
  "modelo": { "primario": "n/a" },
  "capacidades": [
    "Bidirectional streaming",
    "Session management",
    "Query execution via gRPC",
    "Tool invocation via gRPC"
  ],
  "regras": {
    "nao_faz": ["não expõe sem autenticação"]
  },
  "validacao": { "gates": ["safety-sha"] },
  "autonomia": { "modo_autonomo": false, "condicoes": ["requer configuração explícita"] },
  "dependencias": {},
  "registrado_em": "2026-07-27",
  "atualizado_em": "2026-07-27",
  "notas": "Experimental — requer avaliação de segurança antes de uso em produção."
}
```

---

## Resumo do Registro

| Tipo | Quantidade | Status |
|------|-----------|--------|
| Agents/Subagents | 2 | ✅ Ativos |
| Tools | 4 | ✅ Ativos (1 experimental) |
| Skills | 3 | ✅ Ativos |
| MCPs | 1 | 🟡 Experimental |
| **Total** | **10** | **✅ Registrados** |

---

**Versão:** 1.0.0
**Data:** 2026-07-27
**Fonte:** Gitlawb/openclaude v0.26.0 (30.4k stars)
