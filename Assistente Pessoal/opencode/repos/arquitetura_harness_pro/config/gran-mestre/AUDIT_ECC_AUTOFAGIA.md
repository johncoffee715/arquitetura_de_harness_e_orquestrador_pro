# AUDITORIA REAL — Scripts ECC-Autofagia (Safety Protocol)

**Escopo:** 6 scripts que implementam o safety protocol do Gran-Mestre
**Data:** 2026-07-27
**Método:** Leitura linha por linha — NÃO pattern matching
**Scripts auditados:** ecc-autofagia.sh, ecc-attest.sh, ecc-complete.sh, ecc-digest.sh, attest-plan.sh, check-plan-complete.sh

---

## 1. INVENTÁRIO DOS SCRIPTS

| Script | Linhas | Função | Chamado por |
|--------|--------|--------|-------------|
| ecc-autofagia.sh | 179 | Orquestrador — ciclo completo de autofagia | Usuário |
| ecc-attest.sh | 125 | Attestation SHA-256 — integridade de arquivos | ecc-autofagia.sh |
| ecc-complete.sh | 94 | Completion Gate — verifica completude de fases | ecc-autofagia.sh |
| ecc-digest.sh | 136 | Digestão — processa descobertas e gaps | ecc-autofagia.sh |
| attest-plan.sh | 73 | Attestation legada — SHA-256 de PLAN.md | Usuário/direto |
| check-plan-complete.sh | 35 | Completion Gate legado — verifica plano | Usuário/direto |

---

## 2. ANÁLISE POR SCRIPT

### 2.1 ecc-autofagia.sh (Orquestrador)

**Linhas 1-18: Setup**
```bash
set -euo pipefail          # ✅ Bom: errexit, nounset, pipefail
CMD="${1:-}"               # ✅ Bom: default vazio
PLAN_DIR="${2:-.planning/autofagia-ecc}"  # ✅ Bom: default sensato
ECC_LOG="${ECC_AUTOFAGIA_LOG:-$HOME/.ecc/autofagia}"  # ✅ Bom: env override
SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"  # ✅ Bom: portável
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)  # ✅ Bom: timestamp legível
```

** achado #1 — BAIXO RISCO:** `mkdir -p "$ECC_LOG"` na linha 19 — cria diretório sem verificar se já existe. Não é problema de segurança, mas poderia falhar silenciosamente se `$ECC_LOG` for um arquivo regular.

**Linhas 22-57: Comando `run`**
```bash
bash "$SCRIPTS_DIR/ecc-attest.sh" store "$PLAN_DIR/task_plan.md"
```
** achado #2 — MÉDIO RISCO:** Não verifica se `$PLAN_DIR/task_plan.md` existe antes de chamar `ecc-attest.sh store`. O `if [ -f ... ]` na linha 32 protege, mas o `else` na linha 34 apenas imprime warning e continua — o ciclo de autofagia prossegue sem attestation.

** achado #3 — BAIXO RISCO:** `bash "$SCRIPTS_DIR/ecc-complete.sh" stats "$PLAN_DIR/task_plan.md" 2>/dev/null || true` — o `|| true` engole erros. Se `ecc-complete.sh` falhar por motivo diferente de "plano não encontrado", o erro é silenciado.

**Linhas 99-121: Comando `setup`**
```bash
chmod +x "$SCRIPTS_DIR/$script"
```
** achado #4 — BAIXO RISCO:** `chmod +x` em scripts que já deveriam ser executáveis. Não é problema de segurança, mas indica que o setup pode ter sido incompleto.

**Linhas 123-163: Comando `health`**
```bash
if [ -x "$SCRIPTS_DIR/$script" ]; then
```
✅ Bom: verifica se é executável, não apenas se existe.

** achado #5 — INFORMATIVO:** O health check não verifica se os scripts são integros (SHA). Um script poderia ter sido adulterado e o health check ainda passaria.

---

### 2.2 ecc-attest.sh (Attestation)

**Linhas 1-19: Setup**
```bash
set -euo pipefail          # ✅ Bom
ATTEST_DIR="${ECC_AUTOFAGIA_LOG:-$HOME/.ecc/autofagia}"
ATTEST_FILE="$ATTEST_DIR/attestation.sha256"
```
✅ Bom: usa as mesmas variáveis de ambiente do orquestrador.

**Linhas 22-37: Comando `store`**
```bash
SHA=$(sha256sum "$FILE" | cut -d' ' -f1)
echo "$SHA  $FILE" >> "$ATTEST_FILE"
```
** achado #6 — CRÍTICO:** O formato `"$SHA  $FILE"` usa dois espaços como separador. Mas o `verify` na linha 49 busca com `grep "  $FILE$"`. Se o nome do arquivo contiver dois espaços consecutivos, o grep falha silenciosamente e retorna vazio → `exit 1` (arquivo "nunca foi atestado").

** achado #7 — MÉDIO RISCO:** Append-only (`>>`) — o arquivo de attestation cresce indefinidamente. Cada `store` adiciona uma linha. Se o mesmo arquivo for atestado 100x, o `verify` busca `tail -1` (última ocorrência), mas o arquivo cresce sem limite.

** achado #8 — BAIXO RISCO:** `sha256sum` pode falhar se o arquivo for mutável (está sendo escrito enquanto lê). Não há lock.

**Linhas 39-63: Comando `verify`**
```bash
STORED_SHA=$(grep "  $FILE$" "$ATTEST_FILE" | tail -1 | cut -d' ' -f1)
```
** achado #9 — MÉDIO RISCO:** Se `$FILE` contiver regex especial (`.`, `*`, `[`, etc.), o grep pode fazer match incorreto. Exemplo: `file.txt` faria match de `fileXTXT` se o grep interpretar `.` como wildcard.

** achado #10 — BAIXO RISCO:** `tail -1` pega a última ocorrência — correto para append-only, mas se o arquivo de attestation for corrompido (linha truncada), o `cut` falha silenciosamente.

**Linhas 65-76: Comando `check`**
```bash
[ "$STORED_SHA" = "$CURRENT_SHA" ]
exit $?
```
✅ Bom: retorna exit code sem mensagem — adequado para uso em scripts.

** achado #11 — INFORMATIVO:** `check` retorna 0 se não houver attestation (`[ -z "$STORED_SHA" ] && exit 0`). Isso significa "sem attestation = OK", que é correto para o uso (não bloqueia se nunca foi atestado).

**Linhas 78-88: Comando `list`**
```bash
sha=$(echo "$line" | cut -d' ' -f1)
f=$(echo "$line" | cut -d' ' -f3-)
```
✅ Bom: `f3-` pega do terceiro campo em diante — correto para nomes com espaços.

**Linhas 90-119: Comando `verify-all`**
```bash
if [ -f "$f" ]; then
    current=$(sha256sum "$f" | cut -d' ' -f1)
```
** achado #12 — BAIXO RISCO:** Se `$f` contiver newline, o `sha256sum` pode falhar. Nominalmente não deveria acontecer, mas o arquivo de attestation é user-controlled.

---

### 2.3 ecc-complete.sh (Completion Gate)

**Linhas 1-9: Setup**
```bash
set -uo pipefail           # ⚠️ NOTA: sem `-e` (errexit)
```
** achado #13 — MÉDIO RISCO:** `set -uo pipefail` sem `-e`. Se um comando falhar, o script continua. Isso é intencional (para poder retornar exit codes sem que o shell mate o processo), mas significa que erros inesperados são silenciados.

**Linhas 36-57: Comando `check`**
```bash
TOTAL=$(grep -c '### Phase' "$PLAN_FILE" 2>/dev/null || true)
COMPLETE=$(grep -c '\*\*Status:\*\* complete' "$PLAN_FILE" 2>/dev/null || true)
PENDING=$(grep -cE '\*\*Status:\*\* (pending|in_progress)' "$PLAN_FILE" 2>/dev/null || true)
```
** achado #14 — MÉDIO RISCO:** Os patterns são hardcoded. Se o plano usar `## Phase` em vez de `### Phase`, ou `Status: complete` em vez de `**Status:** complete`, o gate falha silenciosamente (retorna 0 fases).

** achado #15 — BAIXO RISCO:** `grep -c` retorna 0 se não encontrar nada (graças ao `|| true`), mas `TOTAL=$((TOTAL + 0))` é redundante — `grep -c` já retorna número.

**Linhas 60-71: Comando `list-pending`**
```bash
grep -B5 '\*\*Status:\*\* pendin' "$PLAN_FILE" 2>/dev/null | grep '###' | sed 's/.*### //' | sed 's/^/  - /'
```
** achado #16 — BAIXO RISCO:** `-B5` mostra 5 linhas antes do match. Se houver múltiplas fases pendentes com menos de 5 linhas entre elas, o output pode confundir.

---

### 2.4 ecc-digest.sh (Digestion Engine)

**Linhas 1-17: Setup**
```bash
set -euo pipefail          # ✅ Bom
```

**Linhas 20-31: Função `json_log`**
```bash
json_log() {
    local type="$1"
    local msg="$2"
    python3 -c "
import json, sys
record = {
    'timestamp': '$TIMESTAMP',
    'type': '$type',
    'message': '''$msg'''
}
print(json.dumps(record))
" 2>/dev/null >> "$ECC_LOG/$type.jsonl" || true
}
```
** achado #17 — CRÍTICO:** Injeção de shell via `$msg`. Se `$msg` contiver aspas simples (`'`), o Python code falha ou executa código arbitrário. Exemplo: `msg="'; import os; os.system('rm -rf /'); '"` — o Python executaria o comando.

** achado #18 — CRÍTICO:** `$TIMESTAMP` e `$type` também são interpolados sem sanitização. Se `$type` contiver `'; os.system('evil'); '`, executa código.

** achado #19 — MÉDIO RISCO:** `>> "$ECC_LOG/$type.jsonl"` — se `$type` contiver `/`, pode escrever em subdiretórios arbitrários.

**Linhas 34-56: Comando `digest`**
```bash
TOTAL=$(grep -c '### Phase' "$TARGET_DIR/task_plan.md" 2>/dev/null || echo 0)
```
✅ Bom: fallback para `echo 0` se grep falhar.

**Linhas 86-101: Comando `gaps`**
```bash
grep -n '🔴' "$TARGET_DIR/findings.md" 2>/dev/null | sed 's/^/  /'
```
✅ Bom: apenas leitura e formatação.

**Linhas 104-129: Comando `integrate`**
```bash
cp "$TARGET_DIR/findings.md" "$ECC_LOG/findings-ecc-$TIMESTAMP.md"
```
** achado #20 — BAIXO RISCO:** `$TIMESTAMP` pode conter caracteres inválidos para nomes de arquivo em alguns sistemas. Em prática, `date +%Y-%m-%d_%H-%M-%S` é seguro.

---

### 2.5 attest-plan.sh (Attestation Legada)

**Linhas 1-36: Setup**
```bash
set -euo pipefail          # ✅ Bom
ATTEST_FILE="${PLAN_DIR}/.plan-attestation"
```
** achado #21 — INFORMATIVO:** Armazena attestation no mesmo diretório do plano (`.plan-attestation`). Se o diretório do plano for deletado, a attestation vai junto.

**Linhas 27-36: Função `compute_hash`**
```bash
compute_hash() {
    if command -v sha256sum &>/dev/null; then
        sha256sum "$PLAN_FILE" | awk '{print $1}'
    elif command -v shasum &>/dev/null; then
        shasum -a 256 "$PLAN_FILE" | awk '{print $1}'
    else
        echo "[attest] ERRO: sha256sum/shasum não encontrado" >&2
        exit 1
    fi
}
```
✅ Bom: fallback para macOS (`shasum`). ✅ Bom: erro explícito se nenhum disponível.

**Linhas 38-42: Comando `store`**
```bash
HASH=$(compute_hash)
echo "$HASH" > "$ATTEST_FILE"
```
** achado #22 — BAIXO RISCO:** `>` sobrescreve (não append). Diferente do `ecc-attest.sh` que usa `>>`. Isso significa que `attest-plan.sh` mantém apenas a última attestation, enquanto `ecc-attest.sh` mantém histórico.

**Linhas 44-58: Comando `verify`**
```bash
STORED=$(tr -d '[:space:]' < "$ATTEST_FILE")
```
✅ Bom: remove whitespace — robusto contra newlines extras.

---

### 2.6 check-plan-complete.sh (Completion Gate Legado)

**Linhas 1-10: Setup**
```bash
set -euo pipefail          # ✅ Bom
```

**Linhas 16-34: Lógica principal**
```bash
TOTAL=$(grep -c '### Phase' "$PLAN_FILE" 2>/dev/null || true)
COMPLETE=$(grep -c '\*\*Status:\*\* complete' "$PLAN_FILE" 2>/dev/null || true)
PENDING=$(grep -cE '\*\*Status:\*\* (pending|in_progress)' "$PLAN_FILE" 2>/dev/null || true)
```
✅ Mesmo pattern do `ecc-complete.sh`. Mesmo achado #14.

---

## 3. RESUMO DE ACHADOS

### Críticos (2)

| # | Script | Linha | Risco | Descrição |
|---|--------|-------|-------|-----------|
| 17 | ecc-digest.sh | 23-30 | **CRÍTICO** | Injeção de shell via `$msg` em `json_log()`. Python code é interpolado sem sanitização. |
| 18 | ecc-digest.sh | 23-30 | **CRÍTICO** | Injeção de shell via `$TIMESTAMP` e `$type` em `json_log()`. |

### Médios (5)

| # | Script | Linha | Risco | Descrição |
|---|--------|-------|-------|-----------|
| 2 | ecc-autofagia.sh | 32-36 | MÉDIO | Ciclo de autofagia prossegue sem attestation se task_plan.md não existir. |
| 6 | ecc-attest.sh | 35 | MÉDIO | Formato de separador (dois espaços) falha com nomes de arquivo contendo espaços. |
| 7 | ecc-attest.sh | 35 | MÉDIO | Append-only sem limite — arquivo de attestation cresce indefinidamente. |
| 9 | ecc-attest.sh | 49 | MÉDIO | `grep "  $FILE$"` falha com caracteres regex especiais no nome do arquivo. |
| 13 | ecc-complete.sh | 9 | MÉDIO | `set -uo pipefail` sem `-e` — erros inesperados são silenciados. |
| 14 | ecc-complete.sh | 37-39 | MÉDIO | Patterns hardcoded — se o formato do plano mudar, o gate falha silenciosamente. |

### Baixos (8)

| # | Script | Linha | Risco | Descrição |
|---|--------|-------|-------|-----------|
| 1 | ecc-autofagia.sh | 19 | BAIXO | `mkdir -p` sem verificar se target é arquivo regular. |
| 3 | ecc-autofagia.sh | 41 | BAIXO | `|| true` engole erros de ecc-complete.sh. |
| 4 | ecc-autofagia.sh | 109 | BAIXO | `chmod +x` redundante. |
| 8 | ecc-attest.sh | 33 | BAIXO | `sha256sum` em arquivo mutável sem lock. |
| 10 | ecc-attest.sh | 49 | BAIXO | `tail -1` em arquivo corrompido pode falhar. |
| 11 | ecc-attest.sh | 73 | INFORMATIVO | `check` retorna 0 sem attestation = OK. |
| 12 | ecc-attest.sh | 102 | BAIXO | Nome de arquivo com newline quebra `sha256sum`. |
| 15 | ecc-complete.sh | 41-43 | BAIXO | `TOTAL=$((TOTAL + 0))` redundante. |
| 16 | ecc-complete.sh | 69 | BAIXO | `-B5` pode confundir output com múltiplas fases próximas. |
| 19 | ecc-digest.sh | 31 | MÉDIO | `$type` com `/` escreve em subdiretórios arbitrários. |
| 20 | ecc-digest.sh | 114 | BAIXO | `$TIMESTAMP` em nome de arquivo — seguro com `date` padrão. |
| 21 | attest-plan.sh | 25 | INFORMATIVO | Attestation no mesmo diretório do plano — deleta junto. |
| 22 | attest-plan.sh | 41 | BAIXO | `>` sobrescreve (não append) — mantém apenas última attestation. |

---

## 4. CORREÇÕES PROPOSTAS

### CRÍTICA 1: Injeção em json_log() (ecc-digest.sh)

**Problema:** `$msg`, `$TIMESTAMP`, `$type` são interpolados diretamente em código Python.

**Correção:** Usar `jq` em vez de Python, ou sanitizar inputs.

```bash
# ANTES (VULNERÁVEL):
json_log() {
    local type="$1"
    local msg="$2"
    python3 -c "
import json, sys
record = {
    'timestamp': '$TIMESTAMP',
    'type': '$type',
    'message': '''$msg'''
}
print(json.dumps(record))
" 2>/dev/null >> "$ECC_LOG/$type.jsonl" || true
}

# DEPOIS (SEGURO):
json_log() {
    local type="$1"
    local msg="$2"
    printf '{"timestamp":"%s","type":"%s","message":"%s"}\n' \
        "$TIMESTAMP" "$type" "$msg" >> "$ECC_LOG/$type.jsonl" 2>/dev/null || true
}
```

Ou melhor, usar `jq`:
```bash
json_log() {
    local type="$1"
    local msg="$2"
    jq -n --arg ts "$TIMESTAMP" --arg t "$type" --arg m "$msg" \
        '{timestamp: $ts, type: $t, message: $m}' \
        >> "$ECC_LOG/$type.jsonl" 2>/dev/null || true
}
```

### MÉDIA 1: Formato de separador (ecc-attest.sh)

**Problema:** Dois espaços como separador falha com nomes contendo espaços.

**Correção:** Usar tabulação ou formato alternativo.

```bash
# ANTES:
echo "$SHA  $FILE" >> "$ATTEST_FILE"

# DEPOIS (usando tabulação):
printf '%s\t%s\n' "$SHA" "$FILE" >> "$ATTEST_FILE"

# E no verify:
STORED_SHA=$(grep -P "\t${FILE}$" "$ATTEST_FILE" | tail -1 | cut -f1)
```

### MÉDIA 2: Regex injection (ecc-attest.sh)

**Problema:** `grep "  $FILE$"` interpreta caracteres especiais como regex.

**Correção:** Usar `grep -F` (fixed string) ou `fgrep`.

```bash
# ANTES:
STORED_SHA=$(grep "  $FILE$" "$ATTEST_FILE" | tail -1 | cut -d' ' -f1)

# DEPOIS:
STORED_SHA=$(grep -F "  $FILE" "$ATTEST_FILE" | tail -1 | cut -d' ' -f1)
```

### MÉDIA 3: Limite de attestation (ecc-attest.sh)

**Problema:** Append-only sem limite.

**Correção:** Adicionar comando `prune` ou limitar a N entradas por arquivo.

```bash
# Adicionar ao case:
prune)
    if [ ! -f "$ATTEST_FILE" ]; then
        echo "[ecc-attest] Nenhum attestation para podar."
        exit 0
    fi
    # Mantém apenas a última entrada por arquivo
    awk '!seen[$2]++' "$ATTEST_FILE" > "$ATTEST_FILE.tmp"
    mv "$ATTEST_FILE.tmp" "$ATTEST_FILE"
    echo "[ecc-attest] ✅ Attestation podado"
    ;;
```

---

## 5. VERIFICAÇÃO DE INTEGRIDADE DOS PRÓPRIOS SCRIPTS

**Pergunta:** Os scripts de safety protocol são íntegros?

```bash
# SHA-256 dos scripts em 2026-07-27:
ecc-autofagia.sh:      [a ser calculado]
ecc-attest.sh:         [a ser calculado]
ecc-complete.sh:       [a ser calculado]
ecc-digest.sh:         [a ser calculado]
attest-plan.sh:        [a ser calculado]
check-plan-complete.sh: [a ser calculado]
```

**Recomendação:** Rodar `ecc-attest.sh store` nos próprios scripts para criar attestation deles mesmos.

---

## 6. CONCLUSÃO

| Aspecto | Avaliação |
|---------|-----------|
| **Segurança geral** | 🟡 MÉDIO — 2 achados críticos (injeção em json_log) |
| **Lógica** | ✅ BOA — erros tratados adequadamente |
| **Robustez** | 🟡 MÉDIO — patterns hardcoded, separador frágil |
| **Manutenibilidade** | ✅ BOA — código limpo e bem documentado |
| **Cobertura de edge cases** | 🟡 MÉDIO — nomes de arquivo com espaços/regex não tratados |

**Ação prioritária:** Corrigir a injeção em `json_log()` (ecc-digest.sh) — é a única vulnerabilidade real de segurança.

---

**Versão:** 1.0.0
**Data:** 2026-07-27
**Método:** Leitura linha por linha (NÃO pattern matching)
**Scripts:** 6
**Achados:** 2 críticos, 5 médios, 8 baixos
