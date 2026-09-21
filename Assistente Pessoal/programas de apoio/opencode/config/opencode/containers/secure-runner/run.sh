#!/usr/bin/env bash
# secure-runner.sh v1 (opencode-dev first-class, 2026-08-25)
# Autofagia de secure_runner.sh v3 (R71, gran-mestre-backup @7de10798d38b)
# helenizada p/ o monorepo: paths por env, sem hardcodes, contrato
# Permission.ask documentado no README.md do diretório.
#
# Whitelist estrita (PoLP): sistema RO + workspace RW + vault INVISÍVEL.
# Rede OFF por padrão. Uso:
#   SECURE_WORKSPACE=/tmp/wt ./run.sh [--net] -- comando [args...]
set -euo pipefail

WORKSPACE="${SECURE_WORKSPACE:-/tmp/opencode_tasks/$(date +%s)-$$}"
READONLY_BINDS="${SECURE_RO_BINDS:-/usr:/usr /bin:/bin /lib:/lib /etc:/etc}"
mkdir -p "$WORKSPACE"

NET_FLAG="--unshare-net"
while [ $# -gt 0 ]; do
  case "$1" in
    --net) NET_FLAG="--share-net"; shift ;;
    --) shift; break ;;
    *) break ;;
  esac
done

BWRAP_ARGS=()
for bind in $READONLY_BINDS; do BWRAP_ARGS+=(--ro-bind "${bind%%:*}" "${bind##*:}"); done

exec bwrap \
    --dev /dev --proc /proc \
    --tmpfs /tmp --tmpfs /home --tmpfs /var \
    "${BWRAP_ARGS[@]}" \
    --bind "$WORKSPACE" /tmp/workspace \
    "$NET_FLAG" \
    --unshare-all \
    --die-with-parent \
    --new-session \
    --chdir /tmp/workspace \
    -- "$@"
