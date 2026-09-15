# Deploy Log — OpenCode

## [2026-07-30] Update OpenCode 1.18.8 → 1.18.9

### Bug
- OpenCode 1.18.9 foi baixado mas instalado em `/opencode` (raiz) em vez de `/usr/bin/opencode`
- O `cachy-update` (pacman) gerencia o pacote `opencode` em `/usr/bin/opencode`, versão 1.18.8-1.1
- `~/.opencode/bin/opencode` é um symlink para `/usr/bin/opencode`
- `~/.opencode` → `/mnt/dados/opencode` (diretório real)
- Binário antigo `opencode.bin` (1.18.7) ainda existia em `~/.opencode/bin/`

### Solução
1. Identificar todas as instalações do OpenCode:
   - `/usr/bin/opencode` — 1.18.8 (pacote pacman)
   - `/opencode` — 1.18.9 (download manual, solto)
   - `/mnt/usb/opencode/opencode` — 1.18.9 (cópia recovery)
   - `~/.opencode/bin/opencode.bin` — 1.18.7 (antigo)

2. Substituir binário ativo:
   ```bash
   sudo mv /usr/bin/opencode /usr/bin/opencode.old  # renomeia o em uso
   sudo cp /opencode /usr/bin/opencode               # copia 1.18.9
   ```

3. Limpeza:
   ```bash
   rm /mnt/dados/opencode/bin/opencode.bin           # remove 1.18.7
   sudo rm /usr/bin/opencode.old                     # remove backup
   sudo pacman -Qdtq                                  # verifica órfãos
   ```

### Aprendizado
- Ao atualizar binary em uso via pacman, usar `mv` + `cp` (não `cp` direto) para evitar "Text file busy"
- `cachy-update` usa `arch-update` que wrappa pacman — versões manuais fora do pacote podem ser sobrescritas
- `~/.opencode` é symlink para `/mnt/dados/opencode` — verificar antes de mexer
- Senha sudo: 0000

### Comandos Úteis
```bash
# Versão ativa
opencode --version

# Verificar pacote
pacman -Q opencode

# Pacotes órfãos
pacman -Qdtq

# Localização do binário
which opencode && readlink -f $(which opencode)
```
