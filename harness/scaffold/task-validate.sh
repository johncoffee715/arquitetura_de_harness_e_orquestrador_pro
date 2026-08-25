#!/bin/bash
# task-validate.sh — scaffold de validação de task (F4 · R70 self-scaffolding)
# O GM cria o teste; ESTE scaffold executa, captura evidência e reporta PASS/FAIL.
# Uso: task-validate.sh <task_id> <project_path> <test_command...>
set -u
TASK_ID="${1:?task_id obrigatório}"
PROJECT="${2:?project_path obrigatório}"
shift 2
TEST_CMD=("$@")
[ ${#TEST_CMD[@]} -eq 0 ] && { echo "[scaffold] test_command obrigatório" >&2; exit 2; }

EV=/mnt/dados/harness/evidence/${TASK_ID}
mkdir -p "$EV"
TS=$(date -Iseconds)

cd "$PROJECT" || { echo "[scaffold] projeto inacessível: $PROJECT" >&2; exit 2; }

echo "[scaffold ${TASK_ID}] executando: $*" | tee "$EV/command.txt"
START=$(date +%s.%N)
"${TEST_CMD[@]}" > "$EV/output.log" 2>&1
EXIT=$?
END=$(date +%s.%N)
DUR=$(python3 -c "print(f'{float('$END')-float('$START'):.1f}')")

cat > "$EV/result.json" <<JSON
{
  "task_id": "$TASK_ID",
  "project": "$PROJECT",
  "command": "$(printf '%q ' "${TEST_CMD[@]}")",
  "exit_code": $EXIT,
  "duration_s": $DUR,
  "ts": "$TS",
  "verdict": "$([ $EXIT -eq 0 ] && echo PASS || echo FAIL)"
}
JSON

if [ $EXIT -eq 0 ]; then
  echo "[scaffold ${TASK_ID}] PASS em ${DUR}s — evidência: $EV"
  exit 0
fi
echo "[scaffold ${TASK_ID}] FAIL (exit $EXIT) em ${DUR}s — evidência: $EV/output.log"
tail -20 "$EV/output.log"
exit 1
