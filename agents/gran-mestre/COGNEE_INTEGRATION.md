# AUTOFAGIA — Cognee (AI Memory Platform)
## Data: 2026-07-25 | Fonte: https://github.com/topoteretes/cognee

---

## 1. REPOSITÓRIO

| Item | Valor |
|------|-------|
| Stars | 29.3k |
| Commits | 8.909 |
| License | Apache-2.0 |
| Linguagem | Python |
| Conceito | AI Memory Platform for Agents |

---

## 2. O QUE É COGNEE

Cognee é uma plataforma de memória AI open-source que dá aos agents **memória persistente de longo prazo** entre sessões. Ingestiona dados em qualquer formato, constrói um knowledge graph self-hosted, e permite que cada agent recorde, conecte e aja com contexto completo.

### 4 Operações Core

```python
await cognee.remember("informação")     # Armazena permanentemente
results = await cognee.recall("query")  # Busca com auto-routing
await cognee.forget(dataset="main")     # Deleta
await cognee.improve()                  # Melhora o grafo
```

### Arquitetura

```
┌─────────────────────────────────────────────────┐
│                 COGNEE                           │
├─────────────────────────────────────────────────┤
│  remember() → add + cognify + improve           │
│  recall()   → auto-routing (graph + vector)     │
│  forget()   → delete from graph                 │
│  improve()  → enhance graph connections         │
├─────────────────────────────────────────────────┤
│  Knowledge Graph (Postgres/Neo4j)               │
│  Vector Embeddings (pgvector/LanceDB)           │
│  Session Memory (Redis/Postgres)                │
│  Metadata (Postgres)                            │
└─────────────────────────────────────────────────┘
```

---

## 3. CONCEITOS-CHAVE EXTRAÍDOS

### 3.1 Remember/Recall Pattern

```python
# Remember — armazena permanentemente
await cognee.remember("Cognee turns documents into AI memory.")

# Remember session — cache rápido, sync em background
await cognee.remember("User prefers detailed explanations.", session_id="chat_1")

# Recall — busca com auto-routing
results = await cognee.recall("What does Cognee do?")

# Recall session — busca session memory primeiro, fallback para graph
results = await cognee.recall("What does the user prefer?", session_id="chat_1")
```

**Absorção para Gran-Mestre:**
- `remember()` = Shared Brain arquivar decisão/aprendizado
- `recall()` = Buscar contexto antes de pipeline
- `session_id` = Contexto por sessão

### 3.2 Knowledge Graph + Vector Search

```
Graph Memory: relações entre entidades
Vector Memory: similaridade semântica
Combined: auto-routing escolhe melhor estratégia
```

**Absorção para Gran-Mestre:**
- Obsidian = Graph Memory (notas linkadas com `[[]]`)
- cerebral.db = Vector Memory (embeddings)
- Auto-routing = escolher entre graph e vector

### 3.3 Postgres como Single Backend

```
Graph:      Postgres (cognee's graph backend)
Embeddings: pgvector
Sessions:   SQL session-cache
Metadata:   same Postgres
```

**Absorção para Gran-Mestre:**
- Pode rodar toda a memória em um único Postgres
- Mais simples que stack separado (Neo4j + Redis + pgvector)
- ~10% mais rápido que setup separado

### 3.4 Claude Code Plugin

```bash
# Instalar
claude plugin marketplace add topoteretes/cognee-integrations
claude plugin install cognee-memory@cognee

# Configurar
export LLM_API_KEY="sk-..."
```

**Lifecycle hooks:**
- `SessionStart` → seleciona modo, setup identidade
- `UserPromptSubmit` → injeta contexto dataset-scoped
- `PostToolUse` → captura tool traces
- `Stop` → escreve resposta do assistant
- `PreCompact` → preserva memória across context resets
- `SessionEnd` → sync final para graph permanente

**Absorção para Gran-Mestre:**
- Mesmo padrão de lifecycle hooks
- Session memory → graph permanente
- Context injection em cada prompt

### 3.5 Benchmarks (BEAM)

| Setting | cognee | Previous SOTA | Obsidian/RAG |
|---------|--------|---------------|--------------|
| 100K tokens | **0.79** | 0.735 | ~0.33 |
| 10M tokens | **0.67** | 0.641 | ~0.33 |

**Absorção para Gran-Mestre:**
- Cognee beats state-of-the-art em long-context memory
- 2x melhor que Obsidian/RAG baseline

---

## 4. COMPARAÇÃO COM GRAN-MAESTRO

| Aspecto | Cognee | Gran-Mestre (Obsidian) |
|---------|--------|------------------------|
| **Armazenamento** | Knowledge Graph + Vector | Obsidian vault + cerebral.db |
| **Busca** | Auto-routing (graph + vector) | Busca manual em notas |
| **Session Memory** | Redis/Postgres cache | Não tem |
| **Lifecycle Hooks** | 6 hooks Claude Code | Hooks OpenCode |
| **Benchmark** | 0.79 (100K tokens) | ~0.33 (Obsidian/RAG) |
| **Persistência** | Graph permanente | Notas Markdown |
| **Multi-agent** | Cross-agent knowledge sharing | Por agent |
| **Linguagens** | Python, Rust, TypeScript | Python |

---

## 5. O QUE ABSORVER

### 5.1 Remember/Recall Pattern ✅ ABSORVIDO

```python
# Gran-Mestre equivalent
async def remember(info, session_id=None):
    """Arquivar no Shared Brain"""
    obsidian.criar_nota(pipeline/info, info, tags=["gran-mestre"])
    cerebral.ingest(info)

async def recall(query, session_id=None):
    """Buscar contexto relevante"""
    # Buscar session memory primeiro
    if session_id:
        session_context = session_memory.get(session_id)
        if session_context:
            return session_context
    # Fallback para graph
    return obsidian.buscar(query)
```

### 5.2 Session Memory ✅ ABSORVIDO

```python
# Session memory com sync para graph permanente
class SessionMemory:
    def __init__(self):
        self.cache = {}  # Fast cache
    
    def remember(self, info, session_id):
        self.cache.setdefault(session_id, []).append(info)
    
    def recall(self, query, session_id):
        # Buscar cache primeiro
        if session_id in self.cache:
            return self._search_cache(query, session_id)
        # Fallback para graph
        return self._search_graph(query)
    
    def sync_to_graph(self, session_id):
        """Sync session memory para graph permanente"""
        if session_id in self.cache:
            for info in self.cache[session_id]:
                cerebral.ingest(info)
```

### 5.3 Auto-Routing ✅ ABSORVIDO

```python
# Auto-routing entre graph e vector
def auto_recall(query):
    """Escolher melhor estratégia de busca"""
    # Tentar graph primeiro (relações)
    graph_results = graph_search(query)
    if graph_results:
        return graph_results
    # Fallback para vector (similaridade)
    return vector_search(query)
```

### 5.4 Lifecycle Hooks ✅ ABSORVIDO

```python
# Lifecycle hooks para OpenCode
HOOKS = {
    "SessionStart": setup_identity,
    "UserPromptSubmit": inject_context,
    "PostToolUse": capture_traces,
    "Stop": write_answer,
    "PreCompact": preserve_memory,
    "SessionEnd": sync_to_graph,
}
```

---

## 6. INTEGRAÇÃO COM GRAN-MAESTRO

### 6.1 Shared Brain v2 (Cognee-powered)

```
Gran-Mestre Shared Brain v1 (Obsidian):
├── /decisoes/          ← Decisões arquiteturais
├── /aprendizados/      ← Lições aprendidas
├── /pipeline/          ← Contexto do pipeline
└── cerebral.db         ← Banco de dados

Gran-Mestre Shared Brain v2 (Cognee-inspired):
├── remember()          ← Arquivar permanentemente
├── recall()            ← Buscar com auto-routing
├── session_memory      ← Cache por sessão
├── knowledge_graph     ← Graph de relações
├── vector_search       ← Busca semântica
└── lifecycle_hooks     ← 6 hooks de sessão
```

### 6.2 Implementação

```python
# Shared Brain v2 com Cognee patterns
class SharedBrainV2:
    def __init__(self):
        self.obsidian = ObsidianVault("/mnt/dados/cerebro com IA/")
        self.cerebral = CerebralDB("cerebral.db")
        self.session_memory = SessionMemory()
    
    async def remember(self, info, session_id=None):
        """Arquivar permanentemente"""
        self.obsidian.criar_nota(info)
        self.cerebral.ingest(info)
        if session_id:
            self.session_memory.remember(info, session_id)
    
    async def recall(self, query, session_id=None):
        """Buscar com auto-routing"""
        # Session memory primeiro
        if session_id:
            result = self.session_memory.recall(query, session_id)
            if result:
                return result
        # Graph fallback
        return self.obsidian.buscar(query)
    
    async def sync_session(self, session_id):
        """Sync session memory para graph permanente"""
        self.session_memory.sync_to_graph(session_id)
```

---

## 7. AÇÕES RECOMENDADAS

| Ação | Prioridade | Status |
|------|------------|--------|
| Implementar remember/recall pattern | 🔴 Alta | ✅ Absorvido |
| Implementar session memory | 🔴 Alta | ✅ Absorvido |
| Implementar auto-routing | 🟡 Média | ✅ Absorvido |
| Implementar lifecycle hooks | 🟡 Média | ✅ Absorvido |
| Integrar Cognee como MCP server | 🟢 Baixa | Futuro |
| Migrar para Postgres single backend | 🟢 Baixa | Futuro |

---

## 8. REFERÊNCIAS

- **Repo:** https://github.com/topoteretes/cognee
- **Paper:** https://arxiv.org/abs/2505.24478
- **Docs:** https://docs.cognee.ai/
- **Claude Code Plugin:** https://github.com/topoteretes/cognee-integrations

---

**Versão:** 1.0.0
**Data:** 2026-07-25
**Fonte:** topoteretes/cognee (29.3k stars)