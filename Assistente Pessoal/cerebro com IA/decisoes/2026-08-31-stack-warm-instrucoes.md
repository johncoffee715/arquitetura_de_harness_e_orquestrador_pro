# Instruções — Correção da lentidão do Orquestrador 35B (modo WARM + ctx)

Data: 2026-08-31 · Origem: diagnóstico Gran-Mestre (sessão 2026-08-31)

## Diagnóstico (causa raiz)
- Ornith-1.5-35B @ ctx 262144 exige ~26GB RAM (18GB pesos IQ4_XS + ~8.6GB KV q4/q4).
- RAM total: 31GB. Com 8 slots LLM up → 21GB em swap (zram) → thrash → tudo lento
  (incluindo subagentes, cujos backends Qwen-4B :9088 e Ternary :9090 estavam com
  5.7GB e 3.9GB em swap — por isso retornos alucinados/corrompidos).
- WARM sob demanda sozinho NÃO resolve: mesmo só GM+córtex ≈ 32GB > 31GB.
- Correção completa = ctx 32768 (libera ~7.5GB) + WARM sob demanda.

## Passo 1 — Editar `/mnt/dados/Assistente Pessoal/opencode/scripts/start-stack.sh`

### 1a. Reduzir ctx do GM (seção gerada, bloco launch 8083)
Trocar `-c 262144` por `-c 32768`:
```bash
launch 8083 "Ornith-1.5-35B-A3B-IQ4_XS.gguf" \
  -c 32768 -np 1 -b 2048 -ub 512 -ngl 0 \
  --cache-type-k q4_0 --cache-type-v q4_0 \
  --jinja --temp 0.6 --top-p 0.95 --top-k 20 \
  --chat-template-kwargs '{"enable_thinking": false}'
```
⚠️ Se `sync-llm-stack.py --apply` rodar depois, o ctx volta ao valor do
`manifesto_llm.json` — editar também lá (slot orquestrador) para persistir.

### 1b. Modo WARM (substituir bloco "MODELO WARM" + "PORTAS CANÔNICAS", linhas ~13-21)
```bash
# ── MODELO WARM (R21/R58): sobe SÓ sob demanda ──
# Uso: start-stack.sh            → só ESSENTIAL (8083 9084) + needles
#      start-stack.sh all        → todos os slots
#      start-stack.sh <porta|nome> ... → só os pedidos (ex.: 9088, proposer)
ESSENTIAL_PORTS=(8083 9084)
WARM_PORTS=(9086 9088 9090 9093 9095)
NEEDLE_PORTS=(8097 9091)
ALL_PORTS=(8083 9084 9086 9088 9090 9093 9095 8097 9091)
declare -A PORT_NAME=([gm]=8083 [cortex]=9084 [reflexo]=9086 [proposer]=9088 [refuter]=9090 [judge]=9092 [smol]=9093 [vlm]=9095)
TARGETS=()
MODE_WARM=1
for arg in "$@"; do
  case "$arg" in
    all) MODE_WARM=0 ;;
    *)
      if [[ "$arg" =~ ^[0-9]+$ ]]; then TARGETS+=("$arg")
      elif [ -n "${PORT_NAME[$arg]:-}" ]; then TARGETS+=("${PORT_NAME[$arg]}")
      else echo "[start-stack] alvo desconhecido: $arg (use porta ou nome)"; fi
      ;;
  esac
done
in_targets() { local p="$1" t; for t in "${TARGETS[@]:-}"; do [ "$t" = "$p" ] && return 0; done; return 1; }
```

### 1c. No launch() (linhas ~31-35), substituir o filtro WARM por:
```bash
  # R58: WARM slots só sobem sob demanda (arg explícito ou `all`)
  if [ "$MODE_WARM" -eq 1 ] && [[ " ${WARM_PORTS[*]} " =~ " $port " ]] && ! in_targets "$port"; then
    echo "[$port] WARM — skip (use: start-stack.sh $port)"
    return 0
  fi
```

### 1d. Health check final (linha ~110)
Trocar `for p in 8083 9084 9086 9088 9090; do` por `for p in "${ESSENTIAL_PORTS[@]}"; do`.

## Passo 2 — Editar `/mnt/dados/Assistente Pessoal/opencode/scripts/stop-all-models.sh`
- Trocar `PORTS=(8083 9084 9086 9088 9090)` por ALL_PORTS + TARGETS + parse de args
  (porta ou nome; sem args = todos), mesmo padrão do 1b.
- Loop usa `"${TARGETS[@]}"`.
- **REMOVER** a linha `pkill -f "llama-server" 2>/dev/null || true` (R19 — mata tudo).

## Passo 3 — Editar `/mnt/dados/Assistente Pessoal/opencode/scripts/stack-toggle.sh`
- Em `is_stack_up()`: `local ports=(8083 9084)` (essenciais apenas).

## Passo 4 — Aplicar (restart do GM)
```bash
# Backup primeiro
mkdir -p /tmp/opencode/stack-warm-backup-$(date +%s)
cp -p "/mnt/dados/Assistente Pessoal/opencode/scripts/"*.sh /tmp/opencode/stack-warm-backup-$(date +%s)/

# Derrubar (só depois de corrigir o stop-all-models.sh — o atual derruba 8083 também)
bash "/mnt/dados/Assistente Pessoal/opencode/scripts/stop-all-models.sh"

# Subir essenciais + WARM sob demanda
bash "/mnt/dados/Assistente Pessoal/opencode/scripts/start-stack.sh"        # 8083 + 9084 + needles
bash "/mnt/dados/Assistente Pessoal/opencode/scripts/start-stack.sh" 9088   # proposer sob demanda
```

## Passo 5 — Verificação
```bash
curl -s http://127.0.0.1:8083/props | grep -o '"n_ctx":[0-9]*'   # esperado: 32768
curl -s http://127.0.0.1:8083/health                            # ok
free -g                                                          # swap usada deve cair para <5GB
```

## Avisos
1. NÃO rodar `stop-all-models.sh` antes de corrigi-lo (versão atual derruba o GM 8083).
2. `sync-llm-stack.py --apply` regera a seção launch — ctx volta ao manifesto; WARM
   sobrevive (filtro está na função launch(), que o sync não reescreve).
3. Se preferir não reduzir ctx: alternativa é RAM 64GB (Pacote B) — única forma de
   manter 262K sem thrash.