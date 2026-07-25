#!/bin/bash
# ============================================================
# AUTO-SYNC: Observa /mnt/win2/textos, pdf e esquemas/
# e sincroniza novos arquivos para o Obsidian automaticamente
# ============================================================

ORIGEM="/mnt/win2/textos, pdf e esquemas"
DESTINO="/mnt/dados/cerebro com IA/textos, pdf e esquemas"
LOG="/home/johncoffee/.opencode/scripts/ocr-pipeline/sync.log"
STATE="/home/johncoffee/.opencode/scripts/ocr-pipeline/.sync-state"
OCR_SCRIPT="/home/johncoffee/.opencode/scripts/ocr-pipeline/ocr_extract.py"

export TESSDATA_PREFIX="$HOME/.local/share"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG"
}

# Coletar assinatura atual da árvore (arquivo → timestamp)
scan_tree() {
    find "$ORIGEM" -type f \( \
        -iname "*.pdf" -o -iname "*.PDF" -o \
        -iname "*.txt" -o -iname "*.md" -o \
        -iname "*.doc" -o -iname "*.docx" -o \
        -iname "*.jpg" -o -iname "*.jpeg" -o \
        -iname "*.png" -o -iname "*.gif" -o \
        -iname "*.bmp" -o -iname "*.tiff" -o \
        -iname "*.mp4" -o -iname "*.mkv" -o -iname "*.avi" -o \
        -iname "*.xlsx" -o -iname "*.xls" -o \
        -iname "*.rar" -o -iname "*.zip" \
    \) -printf "%T@ %p\n" 2>/dev/null | sort -n
}

process_new_file() {
    local filepath="$1"
    local basename_full=$(basename "$filepath")
    local ext="${basename_full##*.}"
    local ext_lower=$(echo "$ext" | tr '[:upper:]' '[:lower:]')

    # Criar subpasta destino mantendo estrutura
    local rel_path="${filepath#$ORIGEM/}"
    local dir_destino="$DESTINO/$(dirname "$rel_path")"
    mkdir -p "$dir_destino"

    # Copiar arquivo
    cp "$filepath" "$dir_destino/$basename_full" 2>/dev/null
    log "📎 Copiado: $rel_path"

    # Processar conforme tipo
    case "$ext_lower" in
        pdf)
            # Criar nota .md com embed
            local md_name="${basename_full%.*}.md"
            local title=$(echo "${basename_full%.*}" | sed 's/_/ /g; s/-/ /g; s/  */ /g')

            if [ ! -f "$dir_destino/$md_name" ]; then
                cat > "$dir_destino/$md_name" << NOTEEOF
---
aliases:
  - "${basename_full%.*}"
tags:
  - datasheet
  - esquematico
  - referencia
  - auto-sync
source: "auto-sync"
file: "${basename_full}"
---

# ${title}

![[${basename_full}]]

## Informações

- **Arquivo:** \`${basename_full}\`
- **Tipo:** PDF/Datasheet
- **Sincronizado:** $(date '+%Y-%m-%d %H:%M')
NOTEEOF
                log "📝 Nota criada: $md_name"

                # OCR automático
                python3 "$OCR_SCRIPT" --file "$dir_destino/$basename_full" 2>/dev/null
            fi
            ;;
        jpg|jpeg|png|gif|bmp|tiff)
            local md_name="${basename_full%.*}.md"
            local title=$(echo "${basename_full%.*}" | sed 's/_/ /g; s/-/ /g; s/  */ /g')

            if [ ! -f "$dir_destino/$md_name" ]; then
                cat > "$dir_destino/$md_name" << IMGEOF
---
aliases:
  - "${basename_full%.*}"
tags:
  - imagem
  - referencia
  - auto-sync
source: "auto-sync"
file: "${basename_full}"
---

# ${title}

![[${basename_full}]]

## Informações

- **Arquivo:** \`${basename_full}\`
- **Tipo:** Imagem
- **Sincronizado:** $(date '+%Y-%m-%d %H:%M')
IMGEOF
                log "📝 Nota imagem criada: $md_name"

                # OCR na imagem
                python3 "$OCR_SCRIPT" --file "$dir_destino/$basename_full" 2>/dev/null
            fi
            ;;
        txt|md)
            # Converter .txt para .md se necessário
            if [ "$ext_lower" = "txt" ]; then
                local md_name="${basename_full%.*}.md"
                if [ ! -f "$dir_destino/$md_name" ]; then
                    echo "---\ntags:\n  - texto\n  - auto-sync\n---\n" > "$dir_destino/$md_name"
                    echo "# ${basename_full%.*}" >> "$dir_destino/$md_name"
                    echo "" >> "$dir_destino/$md_name"
                    cat "$filepath" >> "$dir_destino/$md_name"
                    log "📝 TXT→MD: $md_name"
                fi
            fi
            ;;
        doc|docx)
            local md_name="${basename_full%.*}.md"
            if [ ! -f "$dir_destino/$md_name" ]; then
                cat > "$dir_destino/$md_name" << DOCEOF
---
tags:
  - documento
  - word
  - auto-sync
---

# ${basename_full%.*}

> [!info] Arquivo Word
> \`${basename_full}\` na mesma pasta.
DOCEOF
                log "📝 Nota Word: $md_name"
            fi
            ;;
        mp4|mkv|avi)
            local md_name="${basename_full%.*}.md"
            if [ ! -f "$dir_destino/$md_name" ]; then
                cat > "$dir_destino/$md_name" << VIDEOEOF
---
tags:
  - video
  - referencia
  - auto-sync
---

# ${basename_full%.*}

> [!info] Vídeo
> Arquivo \`${basename_full}\` sincronizado automaticamente.
VIDEOEOF
                log "📝 Nota vídeo: $md_name"
            fi
            ;;
    esac
}

# ============================================================
# MAIN
# ============================================================

log "=== Auto-Sync iniciado ==="
log "Origem: $ORIGEM"
log "Destino: $DESTINO"

# Scan inicial
scan_tree > "$STATE.new" 2>/dev/null
cp "$STATE.new" "$STATE" 2>/dev/null
log "State inicial: $(wc -l < "$STATE") arquivos"

while true; do
    # Scan atual
    scan_tree > "$STATE.new" 2>/dev/null

    # Comparar: encontrar arquivos novos (não estão no state anterior)
    while IFS=' ' read -r timestamp filepath; do
        if ! grep -qF "$filepath" "$STATE" 2>/dev/null; then
            log "🆕 Novo arquivo detectado: $(basename "$filepath")"
            process_new_file "$filepath"
        fi
    done < "$STATE.new"

    # Atualizar state
    mv "$STATE.new" "$STATE" 2>/dev/null

    # Esperar 30 segundos antes do próximo check
    sleep 30
done
