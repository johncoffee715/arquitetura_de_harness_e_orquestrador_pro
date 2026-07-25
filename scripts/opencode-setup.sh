#!/bin/bash
# ============================================================
# opencode-setup.sh
# Gerencia os symlinks do OpenCode para /mnt/dados/opencode/
# ============================================================
# Uso:
#   ./opencode-setup.sh          → Verifica e repara symlinks
#   ./opencode-setup.sh vacuum   → + Compacta o banco SQLite
#   ./opencode-setup.sh clean    → + Remove backups (.bak)
#   ./opencode-setup.sh status   → Só mostra o estado atual
# ============================================================

set -euo pipefail

OPENCODE_HOME="/mnt/dados/opencode"
DRY_RUN=false

# Cores
VERDE='\033[0;32m'
VERMELHO='\033[0;31m'
AMARELO='\033[1;33m'
AZUL='\033[0;34m'
NC='\033[0m' # No Color

# Mapa: "caminho_original" -> "caminho_no_opencode"
declare -A SYMLINKS=(
    ["$HOME/.opencode"]="$OPENCODE_HOME"
    ["$HOME/.omo"]="$OPENCODE_HOME/omo"
    ["$HOME/.local/share/opencode"]="$OPENCODE_HOME/share-data"
    ["$HOME/.local/share/opencode.old"]="$OPENCODE_HOME/share-data.old"
    ["$HOME/.config/opencode"]="$OPENCODE_HOME/config"
    ["$HOME/.claude"]="$OPENCODE_HOME/claude"
)

# Backups que podem ser removidos
BACKUP_DIRS=(
    "$HOME/.opencode.bak"
    "$HOME/.omo.bak"
    "$HOME/.local/share/opencode.bak"
    "$HOME/.local/share/opencode.old.bak"
    "$HOME/.config/opencode.bak"
    "$HOME/.claude.bak"
)

check_mount() {
    if ! mountpoint -q /mnt/dados 2>/dev/null; then
        echo -e "${VERMELHO}[ERRO]${NC} /mnt/dados NÃO está montado!"
        echo "  Monte com: sudo mount /dev/sdb /mnt/dados  (ou o dispositivo correto)"
        return 1
    fi
    if [ ! -d "$OPENCODE_HOME" ]; then
        echo -e "${VERMELHO}[ERRO]${NC} $OPENCODE_HOME não existe!"
        return 1
    fi
    return 0
}

check_symlinks() {
    local all_ok=true
    echo -e "${AZUL}=== Verificando symlinks ===${NC}"
    for origem in "${!SYMLINKS[@]}"; do
        local destino="${SYMLINKS[$origem]}"
        if [ -L "$origem" ]; then
            local atual
            atual=$(readlink -f "$origem" 2>/dev/null || readlink "$origem" 2>/dev/null)
            local esperado
            esperado=$(readlink -f "$destino" 2>/dev/null || echo "$destino")
            if [ "$atual" = "$esperado" ]; then
                echo -e "  ${VERDE}[OK]${NC} $origem → $destino"
            else
                echo -e "  ${AMARELO}[MISMATCH]${NC} $origem → $atual (esperado: $destino)"
                all_ok=false
            fi
        elif [ -d "$origem" ]; then
            echo -e "  ${AMARELO}[DIR]${NC} $origem é um diretório real (devia ser symlink)"
            all_ok=false
        else
            echo -e "  ${VERMELHO}[FALTA]${NC} $origem não existe"
            all_ok=false
        fi
    done
    $all_ok && echo -e "${VERDE}Todos os symlinks OK${NC}"
    $all_ok && return 0 || return 1
}

repair_symlinks() {
    echo -e "${AZUL}=== Reparando symlinks ===${NC}"
    for origem in "${!SYMLINKS[@]}"; do
        local destino="${SYMLINKS[$origem]}"
        if [ ! -d "$destino" ]; then
            echo -e "  ${VERMELHO}[ERRO]${NC} Destino não existe: $destino"
            echo "  Crie com: mkdir -p $destino"
            continue
        fi
        # Remove se for diretório real ou symlink errado
        if [ -d "$origem" ] && [ ! -L "$origem" ]; then
            echo -e "  ${AMARELO}[BACKUP]${NC} Movendo $origem → ${origem}.bak.auto"
            mv "$origem" "${origem}.bak.auto"
        elif [ -L "$origem" ]; then
            rm "$origem"
        fi
        ln -sf "$destino" "$origem"
        echo -e "  ${VERDE}[OK]${NC} $origem → $destino"
    done
}

run_vacuum() {
    local db_path="$OPENCODE_HOME/share-data/opencode.db"
    if [ ! -f "$db_path" ]; then
        echo -e "${AMARELO}[AVISO]${NC} Banco não encontrado: $db_path"
        return
    fi
    
    local antes depois
    antes=$(stat -c%s "$db_path" 2>/dev/null || echo 0)
    echo -e "${AZUL}=== VACUUM no banco SQLite ===${NC}"
    echo "  Tamanho atual: $(numfmt --to=iec $antes)"
    
    # Verificar se o opencode está rodando (se sim, não consegue lock exclusivo)
    if pgrep -x "opencode" >/dev/null 2>&1; then
        echo -e "  ${AMARELO}[AVISO]${NC} OpenCode está rodando. VACUUM precisa de lock exclusivo."
        echo "  Feche o OpenCode e rode: sqlite3 \"$db_path\" \"VACUUM;\""
        return
    fi
    
    sqlite3 "$db_path" "PRAGMA integrity_check;" 2>/dev/null | head -1
    sqlite3 "$db_path" "VACUUM;" 2>/dev/null && {
        depois=$(stat -c%s "$db_path" 2>/dev/null || echo 0)
        echo -e "  ${VERDE}[OK]${NC} VACUUM concluído: $(numfmt --to=iec $antes) → $(numfmt --to=iec $depois)"
    } || {
        echo -e "  ${VERMELHO}[ERRO]${NC} VACUUM falhou (banco pode estar em uso)"
    }
}

clean_backups() {
    echo -e "${AZUL}=== Limpando backups (.bak) ===${NC}"
    for dir in "${BACKUP_DIRS[@]}"; do
        # Também procura .bak.auto (criados pelo repair)
        for pattern in "${dir}" "${dir%.bak}.bak.auto"; do
            if [ -d "$pattern" ]; then
                echo -e "  ${AMARELO}[DEL]${NC} Removendo $pattern ($(du -sh "$pattern" 2>/dev/null | cut -f1))"
                rm -rf "$pattern"
            fi
        done
    done
    echo -e "${VERDE}Backups removidos${NC}"
}

status_report() {
    echo -e "${AZUL}========================================${NC}"
    echo -e "${AZUL}  OpenCode Setup - Relatório de Status${NC}"
    echo -e "${AZUL}========================================${NC}"
    echo ""
    echo "Data: $(date)"
    echo ""
    
    # Montagem
    if mountpoint -q /mnt/dados 2>/dev/null; then
        echo -e "  ${VERDE}[OK]${NC} /mnt/dados montado"
        df -h /mnt/dados | tail -1 | awk '{print "  Espaço: " $3 " usado / " $4 " disponível"}'
    else
        echo -e "  ${VERMELHO}[ERRO]${NC} /mnt/dados NÃO montado"
    fi
    
    echo ""
    if [ -d "$OPENCODE_HOME" ]; then
        echo -e "  ${VERDE}[OK]${NC} $OPENCODE_HOME existe"
        du -sh "$OPENCODE_HOME" 2>/dev/null | awk '{print "  Tamanho total: " $1}'
    else
        echo -e "  ${VERMELHO}[ERRO]${NC} $OPENCODE_HOME não existe"
    fi
    
    echo ""
    check_symlinks
    
    echo ""
    # Tamanho do banco
    local db="$OPENCODE_HOME/share-data/opencode.db"
    if [ -f "$db" ]; then
        echo -e "  Banco SQLite: $(numfmt --to=iec $(stat -c%s "$db" 2>/dev/null || echo 0))"
    fi
    
    # OpenCode rodando?
    local oc_pid
    oc_pid=$(pgrep -x "opencode" 2>/dev/null || echo "")
    if [ -n "$oc_pid" ]; then
        echo -e "  OpenCode rodando: PID $oc_pid ($(ps -p "$oc_pid" -o %cpu,%mem,etime --no-headers 2>/dev/null))"
    else
        echo -e "  OpenCode: parado"
    fi
}

# ============================================================
# MAIN
# ============================================================

case "${1:-check}" in
    status)
        check_mount 2>/dev/null || true
        status_report
        ;;
    vacuum)
        check_mount || exit 1
        check_symlinks || repair_symlinks
        run_vacuum
        ;;
    clean)
        check_mount || exit 1
        clean_backups
        ;;
    repair|fix)
        check_mount || exit 1
        repair_symlinks
        ;;
    check|"" )
        check_mount 2>/dev/null || true
        check_symlinks || {
            echo ""
            echo -e "${AMARELO}Execute './opencode-setup.sh repair' para corrigir${NC}"
        }
        ;;
    *)
        echo "Uso: $0 {check|repair|vacuum|clean|status}"
        echo ""
        echo "  check   → Verifica symlinks (padrão)"
        echo "  repair  → Recria symlinks quebrados"
        echo "  vacuum  → + Compacta banco SQLite"
        echo "  clean   → Remove backups (.bak)"
        echo "  status  → Relatório completo"
        exit 1
        ;;
esac
