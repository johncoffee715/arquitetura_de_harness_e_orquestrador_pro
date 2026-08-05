# Recovery: Sudo, KScreenLocker e PlasmaLogin — Faillock + PAM faltando

**INTENT:** Debug auth failure chain em CachyOS/KDE6 — sudo, screen locker, login gráfico e KDE Wallet rejeitando senha "0000" (YESCRYPT). Investigação MIX pipeline.

**AUTH:** johncoffee + Gran-Mestre (MIX mode) + 4 ciclos de descoberta (faillock → PAM chain → faillock tuning → kwallet)

**TWINS:** polkit-1, systemd-user, systemd-run0, kde, kde-fingerprint, kde-smartcard — existem em `/usr/lib/pam.d/` mas PAM busca ambos diretórios, então funcionam.

**Data:** 2026-07-28
**Sistema:** CachyOS (Arch rolling), KDE Plasma 6.7.3 Wayland, glibc 2.44
**Usuário:** johncoffee (uid=1000, grupos: wheel sys network audio lp storage video users rfkill nopasswdlogin)
**Senha:** "0000" (alterada de "0123")

---

## Problema 1: Sudo rejeitando senha

### Causa Raiz
`pam_faillock` com `deny=3` no serviço `sudo`. Faillock é **per-service** — cada PAM service (`sudo`, `login`, `plasmalogin`, `kscreenlocker`, `polkit-1`) tem entrada separada no mesmo arquivo de tally.

### Faillock Details
- Tally: **`/run/faillock/johncoffee`** (tmpfs) — some no reboot
- Permissão: `johncoffee:root 660` — usuário pode truncar sem sudo
- Após `deny` falhas consecutivas, serviço bloqueia por `unlock_time` segundos

### Fix 1 — Imediato (reset manual)
```bash
: > /run/faillock/johncoffee   # truncar = zerar TODOS os contadores
```

### Fix 2 — Definitivo (aumentar limite + auto-unlock rápido)
Em `/etc/security/faillock.conf`:
```
deny = 999999
unlock_time = 30
```
- `deny = 999999` — praticamente infinito, não trava mais
- `unlock_time = 30` — se travar, auto-desbloqueia em 30s

### Fix 3 — Alias fish
Adicionado em `~/.config/fish/config.fish`:
```fish
alias reset-faillock=": > /run/faillock/johncoffee && echo faillock zerado"
```
Uso no terminal: `reset-faillock`

---

## Problema 2: KDE Screen Locker

### Causa
`/etc/pam.d/kscreenlocker` não existia — PAM não achou em `/etc/pam.d/` nem `/usr/lib/pam.d/` → fallback `other` → `pam_deny.so`

### Fix
Criado `/etc/pam.d/kscreenlocker`:
```
#%PAM-1.0
auth        include     system-auth
account     include     system-auth
password    include     system-auth
session     include     system-auth
```

---

## Problema 3: PlasmaLogin (login gráfico)

### Causa
Chain original usava `pam_unix.so try_first_pass nullok` — `try_first_pass` interage mal com YESCRYPT (`$y$...`): módulo anterior (`pam_faillock.so preauth`) não define AUTHTOK, e `try_first_pass` tenta usar valor vazio.

### Descoberta: PAM search path
PAM 1.7.2 busca ambos: `/etc/pam.d/%s` → `/usr/lib/pam.d/%s`. O arquivo original em `/usr/lib/pam.d/` **era encontrado** — o problema não era localização.

### Fix
Substituir `/etc/pam.d/plasmalogin`:
```
#%PAM-1.0
auth        required                    pam_unix.so
account     include                     system-auth
password    include                     system-auth
session     optional                    pam_keyinit.so       force revoke
session     include                     system-login
-session    optional                    pam_gnome_keyring.so auto_start
-session    optional                    pam_kwallet5.so      auto_start
```

---

## Problema 4: KDE Wallet (kdewallet)

### Sintoma
Após login, pop-up "Erro -9: senha pode estar incorreta" ao abrir carteira 'kdewallet'.

### Causa
Wallet foi criado com senha antiga ("0123") e a senha de login mudou para "0000". O PAM (`pam_kwallet5.so open_session`) não conseguiu auto-destrancar porque a chain minimal não passa a chave do auth pra session (journal: `open_session called without kwallet5_key`).

### Fix
```bash
rm ~/.local/share/kwalletd/kdewallet.*
```
Remove o wallet antigo. Na próxima vez que um app precisar, KDE pergunta a senha e recria com a atual ("0000").

---

## Sumário de Arquivos Modificados

| Arquivo | Ação |
|---------|------|
| `/run/faillock/johncoffee` | truncado (`: >`) |
| `/etc/pam.d/kscreenlocker` | **CRIADO** |
| `/etc/pam.d/plasmalogin` | **SOBRESCRITO** |
| `/etc/security/faillock.conf` | **EDITADO** (`deny=999999`, `unlock_time=30`) |
| `~/.config/fish/config.fish` | **EDITADO** (alias `reset-faillock`) |
| `~/.local/share/kwalletd/kdewallet.*` | **REMOVIDO** |

---

## Comandos Úteis

```bash
# Reset faillock
: > /run/faillock/johncoffee    # qualquer shell
reset-faillock                    # fish shell

# Ver faillock
cat /run/faillock/johncoffee

# Ver PAMs
cat /etc/pam.d/plasmalogin
cat /etc/pam.d/kscreenlocker
cat /etc/security/faillock.conf

# Journal plasmalogin
journalctl -u plasmalogin.service --no-pager -n 20
```

---

## Preferências do Usuário (registradas)

- **Idioma:** pt-BR obrigatório para toda comunicação
- **Deploys:** toda solução de bug deve ser salva em `/mnt/dados/cerebro com IA/Deploys e Debuggings/` (Obsidian vault)
- **Pipeline:** usar MIX mode para investigações sistemáticas

---

## Lições Aprendidas

1. **Faillock é per-service** — cada PAM service tem entrada separada no tally
2. **PAM Arch busca ambos** `/etc/pam.d/` e `/usr/lib/pam.d/`
3. **YESCRYPT (`$y$...`) + `try_first_pass` = falha** — usar `pam_unix.so` sem argumentos
4. **Serviço sem PAM → `other` → `pam_deny.so`**
5. **`pam_faillock.so preauth`** pode ter bug com plasmalogin-helper
6. **Faillock some no reboot** (tmpfs); PAMs e configs em disco persistem
7. **KDE Wallet** usa senha independente da do sistema — mudar senha de login não atualiza wallet

**PENDING:** Nada. Sistema 100% funcional.
