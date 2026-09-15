#!/usr/bin/env bash
# ============================================================
# opencode-maintain.sh
# Mantém os symlinks do OpenCode em /mnt/dados/opencode/
# Uso: opencode-maintain [status|fix|vacuum|clean|all]
# ============================================================
set -euo pipefail

DADOS="/mnt/dados/opencode"
HOME_DIR="/home/johncoffee"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

check_symlinks() {
    echo "┌─────────────────────────────────────────────┐"
    echo "│ Verificando symlinks do OpenCode...         │"
    echo "└─────────────────────────────────────────────┘"
    local all_ok=true

    for entry in \
        "$DADOS:$HOME_DIR/.opencode:.opencode → $DADOS" \
        "$DADOS/omo:$HOME_DIR/.omo:.omo → $DADOS/omo" \
        "$DADOS/config:$HOME_DIR/.config/opencode:.config/opencode → $DADOS/config" \
        "$DADOS/claude:$HOME_DIR/.claude:.claude → $DADOS/claude" \
        "$DADOS/share-data:$HOME_DIR/.local/share/opencode:.local/share/opencode → $DADOS/share-data" \
        "$DADOS/share-data.old:$HOME_DIR/.local/share/opencode.old:.local/share/opencode.old → $DADOS/share-data.old"
    do
        IFS=':' read -r target link name <<< "$entry"
        if [ -L "$link" ] && [ "$(readlink "$link")" = "$target" ]; then
            echo -e "  ${GREEN}✅${NC} $name"
        else
            echo -e "  ${RED}❌${NC} $name"
            all_ok=false
        fi
    done

    echo ""
    if $all_ok; then
        echo -e "  ${GREEN}✓ Todos os symlinks estão ok${NC}"
    else
        echo -e "  ${RED}✗ Alguns symlinks precisam ser reparados${NC}"
    fi
    echo ""
    $all_ok
}

fix_symlinks() {
    echo "┌─────────────────────────────────────────────┐"
    echo "│ Reparando symlinks do OpenCode...           │"
    echo "└─────────────────────────────────────────────┘"

    for entry in \
        "$DADOS:$HOME_DIR/.opencode:.opencode" \
        "$DADOS/omo:$HOME_DIR/.omo:.omo" \
        "$DADOS/config:$HOME_DIR/.config/opencode:.config/opencode" \
        "$DADOS/claude:$HOME_DIR/.claude:.claude" \
        "$DADOS/share-data:$HOME_DIR/.local/share/opencode:.local/share/opencode" \
        "$DADOS/share-data.old:$HOME_DIR/.local/share/opencode.old:.local/share/opencode.old"
    do
        IFS=':' read -r target link name <<< "$entry"

        # Remove se existir como diretório real (não symlink)
        if [ -d "$link" ] && [ ! -L "$link" ]; then
            echo -e "  ${YELLOW}⚠  $name é diretório real — movendo para backup...${NC}"
            mv "$link" "${link}.bak.$(date +%s)"
        fi

        # Remove symlink quebrado
        if [ -L "$link" ] && [ ! -e "$link" ]; then
            echo -e "  ${YELLOW}⚠  Symlink quebrado: $name${NC}"
            rm "$link"
        fi

        # Garante que o diretório pai existe
        parent_dir=$(dirname "$link")
        mkdir -p "$parent_dir"

        # Cria o symlink se não existir
        if [ ! -e "$link" ]; then
            ln -s "$target" "$link"
            echo -e "  ${GREEN}✅ Criado: $name → $target${NC}"
        fi
    done
    echo ""
}

vacuum_db() {
    local DB="$DADOS/share-data/opencode.db"
    if [ ! -f "$DB" ]; then
        echo -e "${YELLOW}Banco não encontrado em $DB${NC}"
        return 1
    fi

    if pgrep -x "opencode" > /dev/null 2>&1; then
        echo -e "${RED}OpenCode está rodando. Feche antes de compactar.${NC}"
        return 1
    fi

    echo "┌─────────────────────────────────────────────┐"
    echo "│ Compactando opencode.db...                  │"
    echo "└─────────────────────────────────────────────┘"
    local before=$(du -h "$DB" | cut -f1)
    echo -e "  Antes: ${YELLOW}$before${NC}"

    echo "  Verificando integridade..."
    sqlite3 "$DB" "PRAGMA integrity_check;"
    echo "  Compactando (VACUUM)..."
    sqlite3 "$DB" "VACUUM;"
    echo "  Checkpoint WAL..."
    sqlite3 "$DB" "PRAGMA wal_checkpoint(TRUNCATE);"

    local after=$(du -h "$DB" | cut -f1)
    echo -e "  Depois: ${GREEN}$after${NC}"
    echo ""
}

clean_sessions() {
    echo "┌─────────────────────────────────────────────┐"
    echo "│ Limpando continuations antigas...           │"
    echo "└─────────────────────────────────────────────┘"
    local count=0
    if [ -d "$DADOS/omo/run-continuation" ]; then
        count=$(find "$DADOS/omo/run-continuation" -name "*.json" -mtime +30 | wc -l)
        find "$DADOS/omo/run-continuation" -name "*.json" -mtime +30 -delete 2>/dev/null
        echo -e "  ${GREEN}🗑  $count continuations antigas (+30d) removidas${NC}"
    fi
    echo ""
}

show_usage() {
    echo "Uso: $0 [comando]"
    echo "  status     - Verifica symlinks"
    echo "  fix        - Repara symlinks quebrados"
    echo "  vacuum     - Compacta opencode.db (fechar opencode antes)"
    echo "  clean      - Remove continuations antigas (+30d)"
    echo "  all        - Executa tudo (fix + vacuum + clean)"
    echo ""
    echo "Sem argumento: executa status"
}

case "${1:-status}" in
    status)
        check_symlinks
        ;;
    fix)
        fix_symlinks
        check_symlinks
        ;;
    vacuum)
        vacuum_db
        ;;
    clean)
        clean_sessions
        ;;
    all)
        echo "═══ opencode-maintain: execução completa ═══"
        echo ""
        fix_symlinks
        clean_sessions
        vacuum_db
        echo "═══════════════════════════════════════════════"
        ;;
    *)
        show_usage
        exit 1
        ;;
esac
