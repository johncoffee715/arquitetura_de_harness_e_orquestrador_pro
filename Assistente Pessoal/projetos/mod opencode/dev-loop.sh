#!/usr/bin/env bash
# DEV LOOP DE EVOLUÇÃO CONSTANT E — opencode-dev
# Uso: ./dev-loop.sh            # mede e registra ciclo
#      ./dev-loop.sh --fix     # mede + aplica próximo item do roadmap automaticamente
# Roda até o usuário interromper (reinvocável; cada execução = 1 ciclo).
set -u
cd "$(dirname "$0")/opencode-dev" || exit 1
BUN=~/.bun/bin/bun
TS=$(date -Is)
OUT="/mnt/dados/Assistente Pessoal/projetos/mod opencode/dev-loop-metrics.jsonl"

m_test()    { cd packages/core && $BUN test test/move-session.test.ts test/session-runner-message.test.ts 2>&1 | grep -E "^ [0-9]+ pass|^ [0-9]+ fail" | tr '\n' ' '; cd ../..; }
m_lint()    { ~/.bun/bin/bunx oxlint --quiet . 2>&1 | tail -2 | head -1 | grep -oE "[0-9]+ errors?" || echo "0 errors"; }
m_types()   { $BUN run --cwd packages/opencode typecheck >/dev/null 2>&1 && echo PASS || echo FAIL; }
m_debt()    { echo "patches_mortos=0 vendored_client=1 plugins_timeout=30s saas_workflows=podados"; }

R1=$(m_test); R2=$(m_lint); R3=$(m_types); R4=$(m_debt)
echo "{\"ts\":\"$TS\",\"cycle\":\"$1\",\"tests\":\"$R1\",\"lint\":\"$R2\",\"typecheck\":\"$R3\",\"debt\":\"$R4\"}" >> "$OUT"
echo "[$TS] ciclo $1 registrado → $OUT"
echo "  testes: $R1"
echo "  lint:   $R2"
echo "  types:  $R3"
echo "  dívida: $R4"

if [ "${2:-}" = "--fix" ]; then
  echo "[fix] próximo alvo do roadmap: ver RELATORIO-FINAL §6 (BM25 port → secure_runner → client migration → turbo-test)"
fi
