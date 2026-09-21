#!/usr/bin/env bash
# sandbox-exec.sh — executa comando em container descartável quando Docker está saudável;
# fallback transparente para execução local (nunca bloqueia o fluxo).
# Uso: sandbox-exec.sh <imagem> <comando...>
set -u
IMG="${1:-}"
shift || true
[ -z "$IMG" ] && { echo "uso: sandbox-exec.sh <imagem> <cmd...>" >&2; exit 2; }

if docker info >/dev/null 2>&1; then
  exec docker run --rm -i \
    -v "$PWD":"$PWD" -w "$PWD" \
    --network none \
    --memory 4g --cpus 4 \
    --security-opt no-new-privileges \
    "$IMG" "$@"
fi
# fallback: sem Docker, executa local (comportamento fail-open documentado)
exec "$@"
