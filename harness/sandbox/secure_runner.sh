#!/bin/bash
# secure_runner.sh v3 — WHITELIST ESTRITA (PoLP, R71)
# Skills/subagentes não-confiáveis: veem SÓ o harness (RO) + workspace (RW).
# Vault cognitivo INVISÍVEL (escrita só via memory_keeper.sh, fora da jaula).
# Uso: secure_runner.sh [--net] -- comando [args...]
BASE=/mnt/dados/harness/sandbox
HARNESS_RO=/mnt/dados/opencode/harness
TASK_ID="${TASK_ID:-$(date +%s)-$$}"
WORKSPACE="/tmp/opencode_tasks/${TASK_ID}"
DONE_DIR="/tmp/opencode_tasks/_done"
mkdir -p "$WORKSPACE"

NET_FLAG="--unshare-net"
while [ $# -gt 0 ]; do
  case "$1" in
    --net) NET_FLAG="--share-net"; shift ;;
    --) shift; break ;;
    *) break ;;
  esac
done

bwrap \
    --ro-bind /usr /usr \
    --ro-bind /bin /bin \
    --ro-bind /lib /lib \
    --ro-bind /lib64 /lib64 2>/dev/null \
    --ro-bind /etc /etc \
    --dev /dev \
    --proc /proc \
    --tmpfs /tmp \
    --tmpfs /home \
    --tmpfs /mnt \
    --tmpfs /var \
    --ro-bind "$HARNESS_RO" "$HARNESS_RO" \
    --bind "$WORKSPACE" /tmp/workspace \
    $NET_FLAG \
    --unshare-all \
    --die-with-parent \
    --new-session \
    --chdir /tmp/workspace \
    --setenv PATH "/usr/bin:/bin" \
    --setenv TASK_ID "$TASK_ID" \
    --setenv HOME /tmp/workspace \
    -- "$@"

EXIT_CODE=$?
mkdir -p "$DONE_DIR"
mv "$WORKSPACE" "${DONE_DIR}/${TASK_ID}-exit${EXIT_CODE}" 2>/dev/null || rm -rf "$WORKSPACE"
ls -1t "$DONE_DIR" 2>/dev/null | tail -n +51 | while read -r old; do rm -rf "${DONE_DIR:?}/${old}"; done
exit $EXIT_CODE
