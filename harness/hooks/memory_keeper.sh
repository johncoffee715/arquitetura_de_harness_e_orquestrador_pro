#!/bin/bash
# memory_keeper.sh — Gatekeeper de Cognição (R71): ÚNICO caminho de escrita no Vault
# Correções vs proposta original:
#   1. contenção REAL de path (realpath dentro do vault), não substring ".."
#   2. extensão .md obrigatória (vault é markdown)
#   3. NUL + caracteres de controle + tamanho máximo
#   4. escrita atômica no MESMO filesystem (temp no destino, não em /tmp)
#   5. log de auditoria de toda escrita
# Uso: memory_keeper.sh <caminho-relativo-no-vault> <arquivo-conteudo>
VAULT="/mnt/dados/cerebro com IA"
LOG=/mnt/dados/harness/logs/memory-keeper.log
MAX_BYTES=2097152  # 2MB por nota
TARGET_PATH="${1:-}"
CONTENT_FILE="${2:-}"
log() { echo "[$(date '+%F %T')] $*" >> "$LOG"; }

[ -n "$TARGET_PATH" ] && [ -n "$CONTENT_FILE" ] && [ -f "$CONTENT_FILE" ] || { echo "[Gate] uso: memory_keeper.sh <rel-vault-path> <content-file>" >&2; exit 2; }

# 1. extensão .md
case "$TARGET_PATH" in
  *.md) ;;
  *) echo "[Gate] NAO_PASSOU — só .md no vault: $TARGET_PATH" >&2; exit 1 ;;
esac

# 2. sem traversal (substring rápido + contenção real via realpath depois)
case "$TARGET_PATH" in
  *..*|/*|*~*) echo "[Gate] NAO_PASSOU — path suspeito: $TARGET_PATH" >&2; exit 1 ;;
esac

FULL_PATH="${VAULT}/${TARGET_PATH}"
PARENT=$(dirname "$FULL_PATH")
mkdir -p "$PARENT" || { echo "[Gate] NAO_PASSOU — mkdir falhou" >&2; exit 1; }

# 3. contenção REAL: resolved path deve estar dentro do vault resolvido
RP=$(realpath -m "$FULL_PATH")
RV=$(realpath -m "$VAULT")
case "$RP" in
  "$RV"/*) ;;
  *) echo "[Gate] NAO_PASSOU — escape de vault: $RP" >&2; log "BLOCK escape: $TARGET_PATH"; exit 1 ;;
esac

# 4. sanitização: NUL, controles C0/C1 (mantém \n \t), teto de tamanho
tr -d '\000' < "$CONTENT_FILE" | LC_ALL=C sed 's/[\x01-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]//g' > "$PARENT/.mk-tmp.$$"
SIZE=$(wc -c < "$PARENT/.mk-tmp.$$")
if [ "$SIZE" -gt "$MAX_BYTES" ]; then
  rm -f "$PARENT/.mk-tmp.$$"
  echo "[Gate] NAO_PASSOU — nota ${SIZE}B > ${MAX_BYTES}B" >&2
  log "BLOCK oversize: $TARGET_PATH ($SIZE B)"; exit 1
fi

# 5. escrita atômica no MESMO filesystem
mv "$PARENT/.mk-tmp.$$" "$FULL_PATH" && \
  { log "OK: $TARGET_PATH ($SIZE B)"; echo "[Gate] PASSOU_CATEGORICO — memória consolidada: $TARGET_PATH"; exit 0; } || \
  { rm -f "$PARENT/.mk-tmp.$$"; log "FALHA mv: $TARGET_PATH"; echo "[Gate] falha na escrita" >&2; exit 1; }
