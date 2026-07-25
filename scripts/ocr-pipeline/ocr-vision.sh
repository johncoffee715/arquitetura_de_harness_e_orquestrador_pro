#!/bin/bash
# OCR Vision para OpenCode — "Olhos" do Agente
# Uso: ocr-vision.sh <comando> [argumentos]
#
# Comandos:
#   scan [pasta]    - Escaneia e extrai texto de todos os arquivos
#   file <arquivo>  - Extrai texto de um arquivo específico
#   search <texto>  - Busca no índice de extrações
#   stats           - Mostra estatísticas
#   rebuild         - Reconstrói índice completo

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/ocr_extract.py"
VAULT="/mnt/dados/cerebro com IA"
EXTRACTS="$VAULT/textos, pdf e esquemas/.ocr-extracts"
INDEX="$EXTRACTS/ocr-index.json"

export TESSDATA_PREFIX="$HOME/.local/share"

case "${1:-scan}" in
    scan)
        echo "🔍 Escaneando vault OCR..."
        python3 "$PYTHON_SCRIPT" --rebuild
        ;;
    file)
        if [ -z "$2" ]; then
            echo "Uso: ocr-vision.sh file <caminho_do_arquivo>"
            exit 1
        fi
        python3 "$PYTHON_SCRIPT" --file "$2"
        ;;
    search|find|q)
        if [ -z "$2" ]; then
            echo "Uso: ocr-vision.sh search <texto>"
            exit 1
        fi
        python3 "$PYTHON_SCRIPT" --query "$2"
        ;;
    stats)
        python3 "$PYTHON_SCRIPT" --stats
        ;;
    rebuild)
        python3 "$PYTHON_SCRIPT" --rebuild
        ;;
    text)
        # Retorna texto extraído de um arquivo específico
        if [ -z "$2" ]; then
            echo "Uso: ocr-vision.sh text <arquivo.extracted.txt>"
            exit 1
        fi
        EXTRACT_FILE="$EXTRACTS/$2.extracted.txt"
        if [ -f "$EXTRACT_FILE" ]; then
            cat "$EXTRACT_FILE"
        else
            echo "Extração não encontrada para: $2"
            echo "Execute: ocr-vision.sh file <arquivo_original>"
        fi
        ;;
    index)
        # Mostra resumo do índice
        if [ -f "$INDEX" ]; then
            python3 -c "
import json
with open('$INDEX') as f:
    idx = json.load(f)
print(f'📊 Índice OCR — {idx[\"stats\"][\"total_files\"]} arquivos')
print(f'   Extraídos: {idx[\"stats\"][\"extracted\"]}')
print(f'   Falharam: {idx[\"stats\"][\"failed\"]}')
print()
for path, data in sorted(idx['files'].items()):
    if data.get('has_text'):
        print(f'  ✅ {path} ({data[\"text_length\"]} chars)')
    else:
        print(f'  ⬜ {path} (sem texto)')
"
        else
            echo "Índice não existe. Execute: ocr-vision.sh rebuild"
        fi
        ;;
    *)
        echo "🔍 OCR Vision para OpenCode"
        echo ""
        echo "Comandos:"
        echo "  scan [pasta]    - Escaneia e extrai texto de todos os arquivos"
        echo "  file <arquivo>  - Extrai texto de um arquivo específico"
        echo "  search <texto>  - Busca no índice de extrações"
        echo "  text <arquivo>  - Retorna texto extraído"
        echo "  stats           - Mostra estatísticas"
        echo "  index           - Lista arquivos indexados"
        echo "  rebuild         - Reconstrói índice completo"
        ;;
esac
