#!/bin/bash
#===============================================================================
# OPENCODE PORTABLE BOOTSTRAP
# Torna o OpenCode independente do disco do sistema (/dev/sda2).
# Resiste a formatação do disco mestre — toda a configuração e estado
# vivem em /mnt/dados (disco separado /dev/sdb).
#
# Uso:
#   ./PORTABLE_BOOTSTRAP.sh              # Modo normal (após format)
#   ./PORTABLE_BOOTSTRAP.sh --save       # Salvar estado atual (antes do format)
#   ./PORTABLE_BOOTSTRAP.sh --check      # Verificar integridade atual
#   ./PORTABLE_BOOTSTRAP.sh --fix        # Reparar symlinks quebrados
#===============================================================================
set -euo pipefail

# ─── Configurações ────────────────────────────────────────────────────────────
DATA_MOUNT="/mnt/dados"
DATA_DIR="${DATA_MOUNT}/opencode"
BINARY_URL="https://github.com/opencode-ai/opencode/releases/latest/download/opencode-linux-x86_64"
BINARY_PATH="/usr/bin/opencode"
BINARY_BACKUP="${DATA_DIR}/bin/opencode.bin"
BACKUP_REPO_URL="https://github.com/johncoffee715/gran-mestre-backup.git"
BACKUP_DIR="${HOME}/gran-mestre-backup"

USER_NAME="johncoffee"
USER_ID=1000

# ─── Cores ────────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; NC='\033[0m'
info() { echo -e "${CYAN}[INFO]${NC} $1"; }
ok()   { echo -e "${GREEN}[OK]${NC}   $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
err()  { echo -e "${RED}[ERR]${NC}  $1"; }

# ─── Funções ──────────────────────────────────────────────────────────────────

check_root() {
  if [[ $EUID -ne 0 ]]; then
    err "Este script precisa ser executado como ROOT (sudo) para criar symlinks e instalar binários."
    exit 1
  fi
}

check_data_disk() {
  if ! mountpoint -q "$DATA_MOUNT"; then
    warn "$DATA_MOUNT não está montado. Tentando montar..."
    mount "$DATA_MOUNT" 2>/dev/null || {
      err "Não foi possível montar $DATA_MOUNT. Verifique /etc/fstab."
      err "UUID=f42ca24a-a9fb-4911-9aff-d56f9068ef47  $DATA_MOUNT  btrfs  rw,noatime,compress=zstd:3,nofail  0  0"
      exit 1
    }
  fi
  ok "$DATA_MOUNT montado"
}

create_symlinks() {
  info "Criando symlinks para $DATA_DIR..."

  SYMLINKS=(
    "$HOME/.opencode:$DATA_DIR"
    "$HOME/.config/opencode:$DATA_DIR/config"
    "$HOME/.claude:$DATA_DIR/claude"
    "$HOME/.omo:$DATA_DIR/omo"
    "$HOME/.bun:$DATA_DIR/bun"
    "$HOME/.opencode-mem:$DATA_DIR/mem"
    "$HOME/.local/share/opencode:$DATA_DIR/share-data"
    "$HOME/.local/state/opencode:$DATA_DIR/state"
    "$HOME/.npm:$DATA_DIR/npm"
    "$HOME/.cache/opencode:$DATA_DIR/cache"
  )

  for entry in "${SYMLINKS[@]}"; do
    target="${entry%%:*}"
    source="${entry##*:}"

    # Remove target existente se for um diretório real (não symlink)
    if [[ -e "$target" && ! -L "$target" ]]; then
      warn "$target é diretório real, movendo para backup..."
      mv "$target" "${target}.bak.$(date +%s)"
    fi

    # Remove symlink quebrado
    if [[ -L "$target" && ! -e "$target" ]]; then
      rm -f "$target"
    fi

    # Cria diretório source se não existir
    mkdir -p "$source"

    # Cria symlink
    if [[ ! -L "$target" ]]; then
      ln -sf "$source" "$target"
      ok "Symlink: $target → $source"
    else
      ok "Symlink já existe: $target → $(readlink "$target")"
    fi
  done
}

install_opencode_binary() {
  local binary_source=""

  # 1. Tenta copiar do backup
  if [[ -f "$BINARY_BACKUP" ]]; then
    binary_source="$BINARY_BACKUP"
    info "Usando binário do backup: $BINARY_BACKUP"
  fi

  # 2. Tenta baixar
  if [[ -z "$binary_source" ]]; then
    info "Baixando OpenCode do GitHub..."
    mkdir -p "$(dirname "$BINARY_BACKUP")"
    curl -L -o "$BINARY_BACKUP" "$BINARY_URL"
    chmod +x "$BINARY_BACKUP"
    binary_source="$BINARY_BACKUP"
  fi

  # Instalar
  cp "$binary_source" "$BINARY_PATH"
  chmod +x "$BINARY_PATH"
  ok "OpenCode instalado: $BINARY_PATH"
  info "Versão: $($BINARY_PATH --version 2>/dev/null || echo 'desconhecida')"
}

install_gh_cli() {
  if command -v gh &>/dev/null; then
    ok "GitHub CLI já instalado"
    return
  fi
  info "Instalando GitHub CLI..."
  if command -v apt &>/dev/null; then
    apt update && apt install -y gh
  elif command -v pacman &>/dev/null; then
    pacman -S --noconfirm github-cli
  fi
  ok "GitHub CLI instalado"
}

clone_backup_repo() {
  if [[ -d "$BACKUP_DIR/.git" ]]; then
    ok "Backup repo já clonado em $BACKUP_DIR"
    return
  fi
  info "Clonando repositório de backup..."
  if command -v gh &>/dev/null && gh auth status &>/dev/null; then
    gh repo clone johncoffee715/gran-mestre-backup "$BACKUP_DIR"
    ok "Repositório clonado"
  else
    git clone "$BACKUP_REPO_URL" "$BACKUP_DIR"
    ok "Repositório clonado"
  fi
}

save_binary_backup() {
  if [[ -f "$BINARY_PATH" ]]; then
    mkdir -p "$(dirname "$BINARY_BACKUP")"
    cp "$BINARY_PATH" "$BINARY_BACKUP"
    ok "Binário copiado para $BINARY_BACKUP"
  else
    warn "Binário não encontrado em $BINARY_PATH"
  fi
}

save_fstab_entry() {
  local fstab_entry="UUID=f42ca24a-a9fb-4911-9aff-d56f9068ef47  $DATA_MOUNT  btrfs  rw,noatime,compress=zstd:3,nofail  0  0"
  if grep -q "$DATA_MOUNT" /etc/fstab; then
    ok "Entrada fstab para $DATA_MOUNT já existe"
  else
    warn "Adicione ao /etc/fstab:"
    echo "$fstab_entry"
    echo "$fstab_entry" >> /etc/fstab
    ok "Entrada fstab adicionada"
  fi
}

save_user_configs() {
  local user_config_dir="${DATA_DIR}/user-configs"
  mkdir -p "$user_config_dir"

  local configs=(
    "$HOME/.bashrc"
    "$HOME/.bash_profile"
    "$HOME/.gitconfig"
    "$HOME/.gitignore"
    "$HOME/.zshrc"
    "$HOME/CLAUDE.md"
  )

  for cfg in "${configs[@]}"; do
    if [[ -f "$cfg" ]]; then
      cp "$cfg" "$user_config_dir/"
      ok "Config salvo: $cfg"
    fi
  done
}

restore_user_configs() {
  local user_config_dir="${DATA_DIR}/user-configs"
  if [[ ! -d "$user_config_dir" ]]; then
    warn "Nenhum backup de configs de usuário encontrado"
    return
  fi

  for cfg in "$user_config_dir"/*; do
    local filename
    filename=$(basename "$cfg")
    local target="$HOME/$filename"
    if [[ ! -f "$target" ]]; then
      cp "$cfg" "$target"
      ok "Config restaurado: $target"
    fi
  done
}

save_critical_system_files() {
  local sys_backup="${DATA_DIR}/system-backup"
  mkdir -p "$sys_backup"

  # fstab
  cp /etc/fstab "$sys_backup/fstab"
  ok "fstab salvo"

  # Pacotes instalados
  if command -v apt &>/dev/null; then
    dpkg --get-selections > "$sys_backup/packages-dpkg.list"
    ok "Lista de pacotes dpkg salva"
  elif command -v pacman &>/dev/null; then
    pacman -Q > "$sys_backup/packages-pacman.list"
    ok "Lista de pacotes pacman salva"
  fi

  # Symlinks do sistema
  ls -la /usr/bin/opencode 2>/dev/null > "$sys_backup/opencode-binary-info.txt"
}

check_integrity() {
  info "Verificando integridade da instalação portável..."
  local all_ok=true

  # Verificar disco de dados
  if ! mountpoint -q "$DATA_MOUNT"; then
    err "$DATA_MOUNT não está montado"
    all_ok=false
  fi

  # Verificar diretórios
  for dir in "$DATA_DIR" "${DATA_DIR}/config" "${DATA_DIR}/skills"; do
    if [[ ! -d "$dir" ]]; then
      err "Diretório ausente: $dir"
      all_ok=false
    fi
  done

  # Verificar symlinks
  for link in "$HOME/.opencode" "$HOME/.config/opencode" "$HOME/.claude"; do
    if [[ ! -L "$link" ]]; then
      err "Symlink ausente: $link"
      all_ok=false
    elif [[ ! -e "$link" ]]; then
      err "Symlink quebrado: $link → $(readlink "$link")"
      all_ok=false
    fi
  done

  # Verificar binário
  if [[ ! -f "$BINARY_PATH" ]] && [[ ! -f "$BINARY_BACKUP" ]]; then
    err "Binário do OpenCode não encontrado"
    all_ok=false
  fi

  if $all_ok; then
    ok "✅ TODAS AS VERIFICAÇÕES PASSARAM"
    echo ""
    echo "  Sistema OpenCode: 🟢 PORTÁVEL"
    echo "  Disco de dados:   🟢 $(df -h $DATA_MOUNT | tail -1 | awk '{print $4}') livre"
    echo "  Config:           🟢 $(du -sh $DATA_DIR/config 2>/dev/null | cut -f1)"
    echo "  Skills:           🟢 $(ls $DATA_DIR/skills 2>/dev/null | wc -l) skills"
    echo "  Backup:           🟢 $([[ -f $BINARY_BACKUP ]] && echo 'binário salvo' || echo 'ausente')"
  else
    err "❌ INTEGRIDADE COMPROMETIDA — execute com --fix"
  fi
}

fix_broken_symlinks() {
  info "Reparando symlinks quebrados..."
  check_data_disk
  create_symlinks
  ok "Reparação concluída"
}

save_all() {
  info "Salvando tudo para o disco de dados..."
  check_data_disk

  save_binary_backup
  save_user_configs
  save_critical_system_files
  save_fstab_entry

  ok "✅ Backup completo salvo em $DATA_DIR"
  echo ""
  echo "  Binário:    ${DATA_DIR}/bin/opencode.bin"
  echo "  Configs:    ${DATA_DIR}/user-configs/"
  echo "  Sistema:    ${DATA_DIR}/system-backup/"
  echo ""
  echo "Para restaurar após format:"
  echo "  sudo mount /mnt/dados"
  echo "  sudo ./PORTABLE_BOOTSTRAP.sh --restore"
}

restore_all() {
  info "Restaurando tudo do disco de dados..."
  check_data_disk

  # Verificar se o diretório de dados existe
  if [[ ! -d "$DATA_DIR" ]]; then
    err "Diretório $DATA_DIR não encontrado!"
    err "Execute --save ANTES de formatar o disco."
    exit 1
  fi

  create_symlinks

  # Restaurar binário
  if [[ -f "$BINARY_BACKUP" ]]; then
    install_opencode_binary
  else
    install_opencode_binary  # Vai baixar
  fi

  # Restaurar configs de usuário
  restore_user_configs

  # Instalar gh
  install_gh_cli

  # Clonar backup
  clone_backup_repo

  ok "✅ RESTAURAÇÃO COMPLETA"
  echo ""
  echo "Recomendado:"
  echo "  1. Verificar gh auth:     gh auth status"
  echo "  2. Verificar OpenCode:    opencode --version"
  echo "  3. Verificar symlinks:    ls -la ~/.opencode"
}

# ─── Main ────────────────────────────────────────────────────────────────────

case "${1:-}" in
  --save)
    save_all
    ;;
  --check)
    check_integrity
    ;;
  --fix)
    fix_broken_symlinks
    check_integrity
    ;;
  --restore)
    restore_all
    ;;
  "")
    # Modo normal: verificar e restaurar o que precisar
    if [[ ! -L "$HOME/.opencode" ]]; then
      restore_all
    else
      check_integrity
    fi
    ;;
  *)
    echo "Uso: $0 [--save|--check|--fix|--restore]"
    echo ""
    echo "  --save      Salvar estado atual para o disco de dados"
    echo "  --check     Verificar integridade da instalação portável"
    echo "  --fix       Reparar symlinks quebrados"
    echo "  --restore   Restaurar tudo do disco de dados (após format)"
    echo "  (sem args)  Auto-detecção e restauração"
    exit 1
    ;;
esac