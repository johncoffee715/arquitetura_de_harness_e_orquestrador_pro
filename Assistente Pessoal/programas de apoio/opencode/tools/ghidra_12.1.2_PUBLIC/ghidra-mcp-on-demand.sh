#!/usr/bin/env bash
# ghidra-mcp-on-demand.sh — RECONSTRUÍDO 2026-09-16 (original perdido com /mnt/dados/opencode).
# Sobe o Ghidra 12.1.2 com a extensão GhidraMCP (TheMixedNuts 0.8.0, embedded MCP :8080).
# Uso: ghidra-mcp-on-demand.sh [IDLE_S=300]
# INFERIDO (verificar no uso): arg $1 = janela ociosa em segundos; aqui mantido como
# tempo máximo de vida do processo em foreground (systemd gerencia o ciclo real).
set -euo pipefail
IDLE_S="${1:-300}"
TOOLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export JAVA_HOME="${JAVA_HOME:-$TOOLS_DIR/jdk-21.0.12.1+1}"
export PATH="$JAVA_HOME/bin:$PATH"
GHIDRA_DIR="$TOOLS_DIR/ghidra_12.1.2_PUBLIC"
echo "ghidra-mcp-on-demand: JAVA_HOME=$JAVA_HOME idle=${IDLE_S}s" >&2
exec "$GHIDRA_DIR/ghidraRun"
