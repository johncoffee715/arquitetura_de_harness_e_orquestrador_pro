# SPEC-002: Harness Híbrido de IA para Hard Coding — Arquitetura Local/Nuvem

**Documento:** SPEC-002-HARNESS-HIBRIDO  
**Versão:** 1.0.0  
**Status:** Draft Técnico  
**Data:** 2026-08-07  
**Categoria:** Engenharia de Sistemas / Infraestrutura de IA  
**Escopo:** Arquitetura híbrida (local + nuvem) para orquestração de modelos de linguagem em pipelines de desenvolvimento de software  
**Público-alvo:** Engenheiros de Sistemas, MLOps, Tech Leads, Arquitetos de Hardware  

---

## 1. Sumário Executivo

Esta especificação define a arquitetura de um **Harness Híbrido de IA** que gerencia modelos locais (on-premise) e modelos em nuvem (MoE) para hard coding automatizado. O sistema é modular, event-driven e idempotente, composto por um **Meta-Orquestrador (Gran-Mestre)** que coordena subagentes especializados através de 6 fases de pipeline, com persistência temporal via Obsidian e validação contratual em múltiplos gates.

---

## 2. Glossário

| Termo | Definição |
|-------|-----------|
| **Harness** | Sistema de integração que conecta modelos de IA locais e em nuvem em um pipeline de execução unificado. |
| **Gran-Mestre** | Meta-orquestrador local (Ornith-1.0 9B) que atua como ponto de entrada único e roteador de tarefas. |
| **Subagente** | Instância especializada de modelo local invocada pelo Gran-Mestre para executar tarefas específicas. |
| **Skill** | Capacidade injetável (plugin) que estende a funcionalidade de um subagente. |
| **Hook** | Ponto de interceptação no ciclo de vida do pipeline para auditoria ou transformação de dados. |
| **Gate** | Ponto de validação obrigatória que bloqueia a progressão do pipeline até que critérios sejam atendidos. |
| **Contrato de Conclusão** | Manifesto rígido de validação de estado que um subagente deve assinar antes de entregar tarefa. |
| **Self-Scaffolding** | Capacidade do modelo de gerar sua própria estrutura de validação e testes. |
| **Hot-swap** | Troca dinâmica e assíncrona de modelos no backend sem interrupção do pipeline. |
| **MoE** | Mixture of Experts — modelo em nuvem acionado sob demanda para auditorias críticas. |

---

## 3. Hardware Base — Parâmetros de Infraestrutura

| ID | Componente | Especificação | Parâmetro de Desempenho | Restrição Crítica |
|----|------------|---------------|------------------------|-------------------|
| `HW-01` | CPU | Intel Xeon E5-2699 v3 | 18 cores / 36 threads @ 2.3GHz | Nunca offloadar camadas para CPU (`n_gpu_layers = total`) |
| `HW-02` | Placa-mãe | Jingsha X99-D8 (X99/C612) | 8x DDR4 slots, PCIe 3.0 x16 | Barramento pode gargalar se houver vazamento de VRAM |
| `HW-03` | RAM | 32 GB DDR4 2400 MHz | Dual-channel | Mínimo para state server e cache de sistema |
| `HW-04` | GPU | AMD MI50 16 GB HBM2 (spoofed as Pro VII) | 1024 GB/s bandwidth | VRAM total: 16 GB — orquestrador nunca deve estourar |
| `HW-05` | Storage — Slave A.I. | SSD 128 GB SATA3 | Leitura: ~500 MB/s | Dedicado ao harness; idempotente por design |

---

## 4. Catálogo de Modelos Locais — Parâmetros de Deploy

### 4.1. Modelo Principal — Gran-Mestre

| ID | Parâmetro | Valor | Descrição |
|----|-----------|-------|-----------|
| `MOD-GM-01` | **Nome** | Ornith-1.0 9B | Modelo treinado com Self-Scaffolding |
| `MOD-GM-02` | **Quantização** | Q4_K_M | Preserva lógica de controle; baixo consumo de VRAM |
| `MOD-GM-03` | **VRAM Estática** | ~5.5 GB | Alocação fixa na HBM2 |
| `MOD-GM-04` | **Contexto Recomendado** | 4k–8k tokens | Texto estruturado de controle (JSON/Markdown) |
| `MOD-GM-05` | **Temperatura (Fase 1)** | 0.7 | Discovery / Brainstorming |
| `MOD-GM-06` | **Temperatura (Roteamento)** | 0.0 | Classificação rígida de rotas |
| `MOD-GM-07` | **Modo de Operação** | Agentic com Tool Calling ativo | Bash, Python, file system access |
| `MOD-GM-08` | **Papel** | Espinha dorsal de controle; gerencia árvore de execução (State Machine) |
| `MOD-GM-09` | **Regra de Ferro #1** | Nunca escreve código bruto; apenas lê resumos consolidados de alteração |
| `MOD-GM-10` | **Regra de Ferro #2** | Roteamento por complexidade obrigatório via ContextAnalyzer |
| `MOD-GM-11` | **Engine Recomendado** | llama.cpp com SGLang/vLLM | `--tool-call-parser qwen3_xml`, `--reasoning-parser` |
| `MOD-GM-12` | **Slots Paralelos** | 1 (estático) | Orquestrador único; não paralelizável |

### 4.2. Modelo de Raciocínio Profundo

| ID | Parâmetro | Valor | Descrição |
|----|-----------|-------|-----------|
| `MOD-RP-01` | **Nome** | Bonsai 27B | Modelo de raciocínio arquitetural e execução pesada |
| `MOD-RP-02` | **Quantização** | 1-bit | Economia extrema de VRAM; múltiplos slots paralelos |
| `MOD-RP-03` | **VRAM Estática** | ~3.9 GB | Alocação fixa na HBM2 |
| `MOD-RP-04` | **Contexto Recomendado** | 16k+ tokens | Leitura de códigos inteiros e documentos de arquitetura |
| `MOD-RP-05` | **Slots Paralelos** | 4–5 | Calculado a partir da folga de VRAM gerada pela escolha 1-bit |
| `MOD-RP-06` | **GBNF** | Gramática estrita obrigatória | Força JSONs e códigos válidos; anula desvios de sintaxe |
| `MOD-RP-07` | **Thinking Regulation** | Limitado | Tokens de pensamento regulados em contextos paralelos longos |
| `MOD-RP-08` | **Papel** | Geração de Design Doc (F2), Plano TDD (F3), Loop de Execução TDD (F4) |
| `MOD-RP-09` | **Modo Standby** | Estratégico | Invocado apenas em: (a) Fase 0 — arquitetura monolítica complexa; (b) Fase de Erro — 2 falhas seguidas de validação |
| `MOD-RP-10` | **Auto-Correção** | Loop Fase 5 | Gera em um slot; valida em outro slot paralelo com prompt: "Revise o documento acima em busca de contradições lógicas. Responda apenas [VÁLIDO] ou os erros encontrados." |

### 4.3. Modelo de Auditoria Intermediária

| ID | Parâmetro | Valor | Descrição |
|----|-----------|-------|-----------|
| `MOD-AI-01` | **Nome** | Nanbeige 4.2 3B | Supervisor textual de qualidade |
| `MOD-AI-02` | **Quantização** | 4-bit (GGUF/EXL2) | Balanceamento entre compreensão e velocidade |
| `MOD-AI-03` | **VRAM Estática** | ~2.5 GB (compartilhado com LFM) | Alocação dinâmica rápida |
| `MOD-AI-04` | **Papel** | Analista de qualidade regulatório |
| `MOD-AI-05` | **Fase 3 (Gating)** | Varre arquivo modificado + teste; garante contratos de tipo e asserções |
| `MOD-AI-06` | **Fase 4 (Micro-Review)** | Garante semântica e legibilidade conforme guia de estilo |
| `MOD-AI-07` | **Fase 5** | Valida cobertura de testes e contratos de verificabilidade antes do Gate 3 |

### 4.4. Modelo de Checagem Binária

| ID | Parâmetro | Valor | Descrição |
|----|-----------|-------|-----------|
| `MOD-CB-01` | **Nome** | LFM 2.5-1.6B | Guardião do portão — avaliador booleano |
| `MOD-CB-02` | **Quantização** | FP8 | Respostas em milissegundos |
| `MOD-CB-03` | **VRAM Estática** | ~2.5 GB (compartilhado com Nanbeige) | Alocação dinâmica rápida |
| `MOD-CB-04` | **Papel** | Avaliador booleano (Sim/Não) |
| `MOD-CB-05` | **Fase 1–2** | Input original pedia X? Código gerado contém X? |
| `MOD-CB-06` | **Fase 4 (CI/CD)** | Commit cumpre regex Conventional Commits? Evidência possui string PASS? |
| `MOD-CB-07` | **Rejeição** | Instantânea | Se Não → rejeita sem inflar contexto do Ornith |

### 4.5. Modelo de Nuvem — Consultor de Elite

| ID | Parâmetro | Valor | Descrição |
|----|-----------|-------|-----------|
| `MOD-CL-01` | **Tipo** | MoE (Mixture of Experts) | Variações maiores (Ornith / Outros) |
| `MOD-CL-02` | **Acionamento** | Sob demanda apenas | Nunca como Gran-Mestre (latência/custo proibitivos) |
| `MOD-CL-03` | **Fase 5 — Revisão Macro** | Auditoria holística do diff total contra arquitetura do contrato | Janela de contexto massiva |
| `MOD-CL-04` | **Fase 6 — Entrega** | Veredito final de conformidade regulatória / segurança antes do Gate 4 | Selo de qualidade jurídica |
| `MOD-CL-05` | **Fallback de Erro** | Se Bonsai 1-bit falhar 3x seguidas no loop TDD da Fase 4 | Desvio automático para nuvem |
| `MOD-CL-06` | **Latência Aceitável** | > 5s | Tolerável apenas em fases finais de auditoria |

---

## 5. Alocação de VRAM — Matriz de Recursos

| Modelo | VRAM Estática | Contexto | Slots | Uso |
|--------|--------------|----------|-------|-----|
| Ornith-1.0 9B (Q4) | ~5.5 GB | 4k–8k | 1 | Gran-Mestre / Controle |
| Bonsai 27B (1-bit) | ~3.9 GB | 16k+ | 4–5 | Raciocínio / Execução |
| Nanbeige 4.2 3B (Q4) | ~2.5 GB* | 8k | 1 | Auditoria Intermediária |
| LFM 2.5-1.6B (FP8) | ~2.5 GB* | 4k | 1 | Checagem Binária |
| **TOTAL ESTÁTICO** | **~11.9 GB** | — | — | — |
| **FOLGA VRAM** | **~4.1 GB** | — | — | KV Cache dinâmico + slots paralelos do Bonsai |

> *Nanbeige e LFM compartilham alocação dinâmica devido à natureza rápida e linear das suas inferências.

### 5.1. Regras de Alocação

| ID | Regra | Parâmetro |
|----|-------|-----------|
| `VRAM-01` | `n_gpu_layers` deve ser **total** para a GPU | `offload_cpu: false` |
| `VRAM-02` | Nunca permitir vazamento para RAM do sistema | `max_system_ram_usage: 0%` |
| `VRAM-03` | KV Cache dinâmico alocado na folga de 4.1 GB | `kv_cache_max: 4.1GB` |
| `VRAM-04` | Hot-swap assíncrono entre modelos por rota | `swap_strategy: async`, `swap_timeout: 500ms` |

---

## 6. Pipeline Gran-Mestre — 6 Fases

### 6.1. Diagrama de Fluxo (Texto Estruturado)

```
[Usuário]
    │
    ▼
[Gran-Mestre] ──► Ornith-1.0 9B (Local)
    │
    ├─────────────────────────────┬─────────────────────────────┐
    ▼                             ▼                             ▼
[Estado/Filtro]           [Geração de Raciocínio]      [Falha de Validação?]
    │                             │                             │
    ▼                             ▼                             ▼
[LFM 2.5 /              [Bonsai 27B 1-bit (Local)]    [Nuvem: MoE]
 Nanbeige 3B]                     │                    (Auditoria pós-falha crítica)
                                  │                             │
                                  ▼                             ▼
                         [WORKFLOW COMPLETO]
                                  │
                                  ▼
                    [FASES 1–6 — Loop Externo]
```

### 6.2. Tabela de Fases — Parâmetros Completos

| Fase | Nome | Task | Escolha de Subagentes/Skills | Modelo Local | Modelo Nuvem | Gate | Contrato de Conclusão |
|------|------|------|------------------------------|--------------|--------------|------|----------------------|
| **F1** | **Descoberta** | Ideias, definição de escopo, remoção de ambiguidade, decomposição leve, brainstorm de agents | Filtros via registro global de plugins, subagentes, hooks, skills, MCPs, LSPs | Ornith-1.0 9B | — | **GATE 1:** Usuário aprova direção | Escopo atual conflita com código de ontem? |
| **F2** | **Contrato** | Transforma direção em design doc; cria `spec.md`; valida spec contra pedido original; brainstorm de agents | Filtros via registro global | Ornith-1.0 9B / Bonsai 27B (arquitetura complexa) | — | **GATE 2:** Usuário aprova spec | Código gerado quebrou sintaxe básica? |
| **F3** | **Plano** | TDD, tasks bite-sized, código completo; decomposição em tasks; planejamento/orquestração via registro global; brainstorm de agents valida cobertura | Filtros via registro global | Bonsai 27B 1-bit (slots paralelos) | — | **GATE 3:** Usuário aprova plano | Novos tipos quebram contratos antigos? |
| **F4** | **Execução** | Supervisiona e sequencia tasks; gerencia git (commits atômicos); orquestra subagentes frescos por task; loop TDD por task; evidência de verificação; revisão micro | Subagentes frescos por task, plugins, hooks, skills, MCPs, tool callings, LSPs | Bonsai 27B 1-bit (slots paralelos) + LFM (validação) + Nanbeige (micro-revisão) | — | Sem gates — commits atômicos, progresso visível | Evidência de teste gerada e salva no SQLite? |
| **F5** | **Revisão Macro** | Revisão holística do diff total; coerência cross-task; acoplamento; auditoria contra critérios de qualidade; brainstorm de agents arquitetura | Filtros macro via registro global | Ornith-1.0 9B | **MoE Nuvem** (obrigatório) | — | — |
| **F6** | **Entrega** | Verification: evidência fresca; validação final contra pedido original; audita evidência; veredito final; brainstorm de agents conformidade | Filtros via registro global | Ornith-1.0 9B | **MoE Nuvem** (obrigatório) | **GATE 4:** Relatório → memória cerebral Obsidian | — |

### 6.3. Safety Protocol — Fases 1–3

| ID | Regra | Parâmetro |
|----|-------|-----------|
| `SAF-01` | Fases 1–3 **não tocam código produtivo** | `touch_prod_code: false` |
| `SAF-02` | SHA de segurança salvo antes do Gate 3 | `safety_sha: git rev-parse HEAD` |
| `SAF-03` | Rollback automático em falha | `rollback_trigger: test_fail OR lint_fail` |

---

## 7. Roteamento por Complexidade

| Rota | Pipeline | Agentes | Modelo Principal | Modelo Secundário |
|------|----------|---------|------------------|-------------------|
| `TRIVIAL` | Execução direta | 1 | Ornith-1.0 9B | — |
| `SIMPLE` | Mini-plano | 1–2 | Ornith-1.0 9B | LFM 2.5 |
| `MEDIUM` | Plano estruturado | 3 | Ornith-1.0 9B | Nanbeige 3B |
| `COMPLEX` / `CRITICAL` | Cascata 6 fases | 5 | Ornith-1.0 9B + Bonsai 27B | Nanbeige + LFM |
| `FEATURE` | Cascata 6 fases completa | 6+ | Arsenal completo do registro global | Todos os modelos locais + MoE nuvem |
| `MIX` | Cascata 6 fases | Arsenal no registro global | Ornith-1.0 9B + Bonsai 27B | Todos + MoE nuvem |

---

## 8. Fluxo de Interceptação e Orquestração

### 8.1. Camadas Técnicas do Harness

| ID | Camada | Função | Acoplamento | Tecnologia | Parâmetro |
|----|--------|--------|-------------|------------|-----------|
| `LAY-01` | **Hook de Ciclo de Vida** | Intercepta o exato momento em que a nuvem termina de gerar o token; repassa payload brutamente para o Ornith | Síncrono | Custom hook | `trigger: token_end`, `target: ornith_input` |
| `LAY-02` | **LSP (Language Server Protocol)** | Valida se classes e arquivos mencionados pela nuvem existem no projeto atual | Síncrono | Pyright / rust-analyzer / tsserver | `validation_mode: strict`, `project_root: ./` |
| `LAY-03` | **MCP (Model Context Protocol)** | Canais seguros para subagentes consultarem Obsidian, ferramentas locais do SO ou internet | Assíncrono | MCP Server local | `channels: [obsidian, os_tools, web]`, `auth: local_token` |
| `LAY-04` | **Plugins** | Injetam capacidades específicas (cobertura de testes, formatadores) nos subagentes operários | Dinâmico | Registry global | `load_strategy: lazy`, `isolation: container` |
| `LAY-05` | **Skills** | Capacidades declarativas injetáveis por task | Dinâmico | Registry global | `injection_point: pre_task`, `scope: per_agent` |

### 8.2. Fluxo Nuvem → Harness Local

```
[Modelo de Nuvem (Claude/GPT)]
            │
            ▼ (emite task macro)
    [Hook lê buffer]
            │
            ▼
    [Ornith-1.0 consome escopo]
            │
            ▼
    [Monta grafo de dependências]
            │
            ▼
    [Spawna subagentes operários]
            │
            ├──────► [LFM 2.5] ──► Gate 1/2 (validação binária)
            │
            ├──────► [Nanbeige 3B] ──► Gate 3 (auditoria textual)
            │
            ├──────► [Bonsai 27B] ──► F2/F3/F4 (raciocínio + execução)
            │
            └──────► [LSP/MCP/Plugins] ──► Validação + Persistência
```

---

## 9. Persistência Temporal — Memória Cerebral

### 9.1. Arquitetura do Obsidian Integrado

| ID | Componente | Função | Schema | Parâmetro |
|----|------------|--------|--------|-----------|
| `MEM-01` | **interactions_history** | Registra ID da task, prompt da nuvem, plano do Ornith, hash do commit | `task_id: UUID`, `cloud_prompt: TEXT`, `plan: JSON`, `commit_hash: CHAR(40)` | `retention: 90d`, `encryption: AES-256` |
| `MEM-02` | **vector_cache_surrogate** | Indexa palavras-chave de arquitetura, decisões de gates, assinaturas de métodos modificados | `keyword: TEXT`, `embedding: VECTOR(768)`, `source_file: PATH` | `index_type: hnsw`, `top_k: 10` |
| `MEM-03` | **gate_telemetry** | Registra pass/fail de subagentes por Gate; pontuação de confiabilidade local do projeto | `agent_id: TEXT`, `gate: ENUM`, `result: PASS|FAIL`, `confidence_score: FLOAT` | `aggregation: daily`, `alert_threshold: <0.7` |

### 9.2. Integração como MCP Server

| ID | Requisito | Implementação | Parâmetro |
|----|-----------|---------------|-----------|
| `MEM-04` | Memória como tool/MCP, não recurso nativo do modelo | `search_vault(query)`, `append_note(content, tags)` | `context_injection: false` |
| `MEM-05` | Persistência cross-day sem estourar janela de contexto | LangGraph Checkpointer + PostgreSQL | `checkpoint_saver: postgres`, `state_ttl: 30d` |
| `MEM-06` | Memória episódica e semântica de longo prazo | Obsidian vault + pgvector | `sync_interval: 60s`, `vector_dim: 768` |

---

## 10. Governança e Segurança do Harness

### 10.1. Regras de Ferro do Gran-Mestre

| ID | Regra | Descrição | Parâmetro de Enforcement |
|----|-------|-----------|--------------------------|
| `RF-01` | **Nunca executa trabalho bruto** | Classifica e delega; nunca escreve código, nunca edita arquivo de implementação | `write_permission: false`, `edit_permission: false` |
| `RF-02` | **Roteamento por complexidade obrigatório** | Toda requisição passa pelo ContextAnalyzer antes de delegação | `skip_analyzer: false`, `penalty: abort` |
| `RF-03` | **Safety Protocol** | Gatilho do SHA antes da Fase 4; rollback em falha | `pre_exec_check: git_status_clean`, `rollback_on_fail: true` |
| `RF-04` | **Observabilidade completa** | Métricas nativas em cada fase; registro em `harness_state.json` | `melt_enabled: true`, `trace_genai: true` |

### 10.2. Mecanismo de Rollback Híbrido

| ID | Gatilho | Ação | Parâmetro |
|----|---------|------|-----------|
| `RB-01` | Arquivos modificados não salvos antes da Fase 4 | Pipeline recusa execução | `precondition: git diff --quiet` |
| `RB-02` | Falha na Fase 5 ou testes da Fase 6 | Aborta conexões de nuvem pendentes; roda `git reset --hard` | `auto_reset: true`, `timeout: 5s` |
| `RB-03` | API de nuvem cai ou sofre injeção de prompt | Validador local intercepta; barra código malicioso antes do arquivo do usuário | `injection_scan: enabled`, `fallback: local_only` |

---

## 11. Core Loop Event-Driven (Idempotência)

| ID | Evento | Publicador | Assinante | Ação | Parâmetro |
|----|--------|------------|-----------|------|-----------|
| `EVT-01` | `phase.completed` | Nó do grafo LangGraph | State Server | Grava estado em `harness_state.json` | `persist: true`, `idempotency_key: uuid` |
| `EVT-02` | `gate.blocked` | Gate Validator | Gran-Mestre | Emite `interrupt_before`; aguarda aprovação | `interrupt_timeout: 24h` |
| `EVT-03` | `agent.failed` | Subagente | Bonsai 27B (fallback) | Reescrita da lógica pesada | `max_retries: 2`, `escalation: cloud_moe` |
| `EVT-04` | `metrics.collected` | Observability Hook | Dashboard | Registra MELT data | `flush_interval: 30s` |
| `EVT-05` | `cloud.fallback` | Gran-Mestre | MoE Nuvem | Auditoria crítica sob demanda | `cost_budget: $5/task`, `latency_max: 30s` |

---

## 12. Checklist de Deploy do Harness

```
[ ] HW-01: n_gpu_layers = total (sem offload para CPU)
[ ] HW-02: SSD Slave A.I. dedicado e idempotente
[ ] MOD-GM-01: Ornith-1.0 9B Q4_K_M carregado com tool calling ativo
[ ] MOD-RP-01: Bonsai 27B 1-bit com GBNF estrita e slots paralelos configurados
[ ] MOD-AI-01: Nanbeige 4.2 3B Q4 pronto para auditoria
[ ] MOD-CB-01: LFM 2.5-1.6B FP8 pronto para validação binária
[ ] MEM-04: MCP Server do Obsidian operacional (search_vault/append_note)
[ ] MEM-05: LangGraph Checkpointer PostgreSQL configurado
[ ] LAY-02: LSP local integrado (Python/TypeScript/Rust)
[ ] LAY-03: MCP Servers catalogados e autenticados
[ ] GOV-01: Policy-as-code na camada de orquestração
[ ] GOV-03: RBAC/ABAC configurado para isolamento de agentes
[ ] SAF-01: Fases 1–3 isoladas de código produtivo
[ ] SAF-02: Gatilho do SHA implementado antes da Fase 4
[ ] RB-01: Mecanismo de rollback híbrido testado
[ ] OBS-01: OpenTelemetry com convenções semânticas GenAI
[ ] EVT-01: Core loop event-driven com idempotência validada
```

---

## 13. Apêndice A: Comandos de Inicialização Recomendados

### 13.1. llama.cpp — Bonsai 27B 1-bit (Slots Paralelos)

```bash
# Calcular slots paralelos com base na folga de VRAM
calc_slots() {
    local vram_total=16384        # 16 GB em MB
    local vram_ornith=5500        # Ornith estático
    local vram_bonsai=3900        # Bonsai estático
    local vram_shared=2500        # Nanbeige/LFM compartilhado
    local vram_folga=$((vram_total - vram_ornith - vram_bonsai - vram_shared))
    local kv_cache_reserva=1000   # Reserva para KV Cache dinâmico
    local slot_size=400           # Estimativa por slot Bonsai
    local max_slots=$(( (vram_folga - kv_cache_reserva) / slot_size ))
    echo "Slots paralelos recomendados para Bonsai: $max_slots"
}

# Execução
./llama-server \
    -m bonsai-27b-1bit.gguf \
    -np 4 \
    -c 16384 \
    --host 127.0.0.1 \
    --port 8081 \
    -ngl 999 \
    --grammar-file strict_json.gbnf
```

### 13.2. vLLM / SGLang — Ornith-1.0 9B (Endpoint OpenAI-Compatible)

```bash
python -m vllm.entrypoints.openai.api_server \
    --model Ornith-1.0-9B-Q4_K_M.gguf \
    --tensor-parallel-size 1 \
    --max-model-len 8192 \
    --tool-call-parser qwen3_xml \
    --reasoning-parser deepseek_r1 \
    --port 8080
```

### 13.3. LangGraph — Configuração de StateGraph

```python
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import StateGraph, END

# Configuração do checkpointer
conn_string = "postgresql://user:pass@localhost:5432/harness_db"
checkpointer = PostgresSaver.from_conn_string(conn_string)

# StateGraph com interrupts para auditoria
builder = StateGraph(HarnessState)
builder.add_node("fase1_descoberta", fase1_node)
builder.add_node("fase2_contrato", fase2_node)
builder.add_node("fase3_plano", fase3_node)
builder.add_node("fase4_execucao", fase4_node)
builder.add_node("fase5_revisao", fase5_node)
builder.add_node("fase6_entrega", fase6_node)

# Interrupts para gates de aprovação humana
builder.add_edge("fase1_descoberta", "gate1_interrupt")
builder.add_edge("fase2_contrato", "gate2_interrupt")
builder.add_edge("fase3_plano", "gate3_interrupt")

# Compile com checkpointer
graph = builder.compile(checkpointer=checkpointer, interrupt_before=["gate1", "gate2", "gate3", "gate4"])
```

---

## 14. Apêndice B: Matriz de Decisão de Modelo por Fase

| Fase | Task Típica | Modelo Local | Modelo Nuvem | Justificativa |
|------|-------------|--------------|--------------|---------------|
| F1 | Brainstorm, definição de escopo | Ornith-1.0 9B | — | Baixa latência, controle de estado |
| F2 | Design doc, spec.md | Bonsai 27B (slots) | — | Raciocínio profundo, múltiplas cláusulas paralelas |
| F3 | Plano TDD, tasks bite-sized | Bonsai 27B (slots) | — | Geração de código completo com cobertura |
| F4 | Execução TDD, commits atômicos | Bonsai 27B + LFM + Nanbeige | — | Paralelismo máximo; validação binária rápida |
| F5 | Revisão macro do diff | Ornith-1.0 9B | **MoE** | Contexto massivo + abstração arquitetural |
| F6 | Veredito final, conformidade | Ornith-1.0 9B | **MoE** | Selo de qualidade jurídica/regulatória |

---

## 15. Apêndice C: Versionamento e Referências

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0.0 | 2026-08-07 | Engenharia de Harness | Especificação inicial consolidada do harness híbrido |

---

> **Nota Estratégica:** Esta arquitetura híbrida transforma o harness em uma **linha de montagem industrial**: o controle é leve e local, a força bruta de execução é barata/paralela (1-bit), e a inteligência extrema (MoE) só é paga e ativada quando o produto final precisa do **selo de qualidade jurídica e arquitetônica**.
