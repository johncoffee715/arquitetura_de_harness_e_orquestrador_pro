---
regra: R102
titulo: "GUARDRAIL UNIVERSAL — PATH CANÔNICO DE INSTALAÇÃO: programas de apoio/"
fonte: user session 2026-09-15
data: 2026-09-15
---

# ═══ REGRA GLOBAL R102 — PATH CANÔNICO: "programas de apoio/" — promulgado 2026-09-15 ═══

**Regra**: todo programa, binário, tarball ou dependência instalado/movido a pedido do usuário via session no opencode é canonizado em `/mnt/dados/Assistente Pessoal/programas de apoio/`. **Nunca** despejar na raiz `/`, `/usr` ou path solto fora dele.

<Workflow (fail-closed)>
1. Pedido de instalação sem destino explícito → default `programas de apoio/` (dono johncoffee; criar se ausente).
2. Artefato avulso achado fora (ex.: `/opencode`) → mover p/ cá via `pkexec` + `chown johncoffee:johncoffee`.
3. Path com espaços → **sempre** aspas duplas em scripts/comandos.

<Enforcement>
- "Acesso negado" ao colar em `/` NÃO é falha: Dolphin roda como johncoffee e `/` = root por design do Unix. Exceção consciente → barra do Dolphin: `admin:///` (polkit pede senha).
- Órfãos de uid inexistente (ex.: uid 1001) → tratar como lixo mal colocado, canonizar ou arquivar, nunca deixar na raiz.

<Exemplo canônico (2026-09-15)>
- User tentou colar em `/` → "Não é possível colar". Diagnóstico: permissão correta do Unix; solução: órfãos `/opencode` (179MB, uid 1001 inexistente) + `opencode-linux-x64.tar.gz` (59MB, root) movidos p/ `programas de apoio/` via pkexec, dono corrigido.

---
