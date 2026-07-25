# Protocolos — Autofagia Cross-Harness (ECC + Gran-Mestre)

## Arquitetura de Integração

```
Gran-Mestre (Orquestrador)
    │
    ├── ECC (Performance & Hooks)
    │   ├── 67 agents → delegar tarefas especializadas
    │   ├── 261 skills → workflows reutilizáveis
    │   ├── 30+ hooks → lifecycle automation
    │   └── rules/ → regras universais
    │
    ├── Claude-Mem (Memória Persistente)
    │   ├── SQLite + Chroma → armazenamento vetorial
    │   ├── MCP Search → busca semântica
    │   └── Compressão AI → resumo de sessões
    │
    └── Planning-with-Files (Planejamento)
        ├── Attestation → SHA-256
        ├── Completion Gate → verificação de fases
        └── Ledger → rastreamento JSONL
```

## Protocolo 1: Attestation Cross-Harness

```bash
# ECC Plugin Hook (PreToolUse)
# Verifica integridade do plano antes de executar
ECC_ATTEST_ENABLED=true  # default: false

# Attestation check
ecc-attest.sh verify .planning/task_plan.md
if [ $? -ne 0 ]; then
  echo "[ECC-Attest] ❌ Plano adulterado — execução bloqueada"
  exit 1
fi
```

**Configuração:**
- Adicionar ao `hooks.json` do ECC como PreToolUse hook
- Matcher: `tool == "Write" && file_path matches "\\.planning/"`
- Usar `ecc-attest.sh` para store/verify/check

## Protocolo 2: Completion Gate

```bash
# ECC Stop Hook
# Verifica se fase atual está completa
ECC_COMPLETION_GATE=true  # default: false

ecc-complete.sh check .planning/task_plan.md
if [ $? -ne 0 ]; then
  echo "[ECC-Gate] ⚠️  Fases pendentes detectadas"
  ecc-complete.sh list-pending .planning/task_plan.md
fi
```

**Configuração:**
- Adicionar ao `hooks.json` do ECC como Stop hook
- Usar env var `ECC_COMPLETION_GATE` para controle
- Modo gated: `ECC_COMPLETION_GATE=strict` bloqueia parada

## Protocolo 3: 2-Action Rule (ECC)

```
A cada 2 operações de leitura/pesquisa:
  1. Salvar descobertas em .planning/findings.md
  2. Atualizar .planning/progress.md
  3. Verificar se há gaps identificados
```

**Implementação no ECC:**
- Hook PostToolUse com contador
- Reseta a cada 2 matches de `tool == "Grep" || tool == "Read" || tool == "WebSearch"`
- Escreve em `.planning/autofagia-ecc/findings.md`

## Protocolo 4: 3-Strike Error Protocol (ECC)

```
ATTEMPT 1: Diagnosticar (hook PreToolUse registra tentativa)
ATTEMPT 2: Abordagem alternativa (hook PostToolUse registra resultado)
ATTEMPT 3: Repensar abordagem (hook Stop registra falha final)
ESCALAR: Notificar usuário + sugerir próximo passo
```

**Implementação no ECC:**
- Usar `ECC_ERROR_COUNTER` como env var
- Registrar em `~/.ecc/autofagia/error-log.jsonl`
- Escalar via comando `/escalate` ou notificação

## Protocolo 5: Safety SHA Rollback

```bash
# Antes de qualquer execução que modifique arquivos
SHA_BEFORE=$(git rev-parse HEAD)
echo "[ECC-Safety] SHA: $SHA_BEFORE" >> .planning/context.md

# Se falhar
git reset --hard $SHA_BEFORE
echo "[ECC-Safety] ✅ Rollback executado para $SHA_BEFORE"
```

## Protocolo 6: Continuous Learning Integration

```
ECC Continuous Learning v2
    │
    ├── Observa → registra em observations.jsonl
    ├── Analisa → thresholds de confiança
    ├── Instinto → regra automática com score
    └── Promove → skill quando score > 0.8
        │
        ▼
Gran-Mestre Autofagia
    │
    ├── Lê instintos do ECC
    ├── Correlaciona com gaps identificados
    ├── Propor melhorias no task_plan.md
    └── Fecha ciclo de autofagia
```

## Protocolo 7: Cross-Harness Adapter

```yaml
autofagia-adapter:
  claude-code:
    hooks: native plugin hooks
    skills: SKILL.md + commands/
    rules: rules/common/ + rules/typescript/
    
  opencode:
    hooks: plugin events (gran-mestre bridge)
    skills: skills/ + commands/
    rules: rules/common/ adaptadas
    
  codex:
    hooks: instruction-backed (no native hooks)
    skills: AGENTS.md + skills/
    rules: rules/common/ via instruction
    
  cursor:
    hooks: cursor-adapted hooks
    skills: cursor-adapted copies
    rules: cursor rules format
```

## Variáveis de Ambiente

```bash
# Controles ECC
ECC_HOOK_PROFILE=standard        # minimal | standard | strict
ECC_DISABLED_HOOKS=""             # hook IDs separados por vírgula
ECC_GATEGUARD=off                 # on | off
ECC_SESSION_START_MAX_CHARS=8000  # limite de contexto
ECC_SKIP_OBSERVE=0                # 0 | 1

# Controles Autofagia
ECC_AUTOFAGIA_ENABLED=true        # true | false
ECC_ATTEST_ENABLED=true           # true | false
ECC_COMPLETION_GATE=false         # true | false | strict
ECC_ERROR_COUNTER=0               # contador de erros
ECC_AUTOFAGIA_LOG=~/.ecc/autofagia/  # diretório de logs
```

## Integrantes do Sistema

| Componente | Função | Harness Primário | Status |
|---|---|---|---|
| Gran-Mestre | Orquestrador | OpenCode | ✅ Ativo |
| ECC | Performance + Hooks | Claude Code | 230K ⭐ |
| Claude-Mem | Memória Persistente | Claude Code | 87K ⭐ |
| Planning-with-Files | Planejamento | Multi-harness | 25.6K ⭐ |
| Autofagia Bridge | Integração cross-harness | OpenCode → ECC | 🚧 Em desenvolvimento |
