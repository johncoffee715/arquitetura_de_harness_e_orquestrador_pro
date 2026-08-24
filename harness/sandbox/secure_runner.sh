#!/bin/bash
# secure_runner.sh — Sandbox Zero-Trust (bwrap) p/ execução de skills/subagentes não-confiáveis
# R71 · correções vs proposta original:
#   1. /mnt/dados montado RO opcional (--harness-ro) — o ecossistema vive lá; sem a flag, invisível
#   2. workspace PRESERVADO em _done/ (auditoria pós-mortem) em vez de rm -rf
#   3. rede: NEGADA por default; --net habilita
#   4. GPU/VRAM não exposta (skills não tocam na MI50)
# Uso: secure_runner.sh [--net] [--harness-ro] -- comando [args...]

BASE=/mnt/dados/harness/sandbox
TASK_ID="${TASK_ID:-$(date +%s)-$$}"
WORKSPACE="/tmp/opencode_tasks/${TASK_ID}"
DONE_DIR="/tmp/opencode_tasks/_done"
mkdir -p "$WORKSPACE"

NET_FLAG="--unshare-net"
HARNESS_FLAG=""
while [ $# -gt 0 ]; do
  case "$1" in
    --net) NET_FLAG="--share-net"; shift ;;
    --harness-ro) HARNESS_FLAG="--ro-bind /mnt/dados /mnt/dados"; shift ;;
    --) shift; break ;;
    *) break ;;
  esac
done

bwrap \
    --ro-bind / / \
    --dev /dev \
    --proc /proc \
    --tmpfs /tmp \
    --tmpfs /home \
    --tmpfs /mnt \
    $HARNESS_FLAG \
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
# auditoria: mantém os últimos 50 workspaces
ls -1t "$DONE_DIR" 2>/dev/null | tail -n +51 | while read -r old; do rm -rf "${DONE_DIR:?}/${old}"; done
exit $EXIT_CODE
