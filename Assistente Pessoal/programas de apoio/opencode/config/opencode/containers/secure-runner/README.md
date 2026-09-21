# Secure Runner (Perspectiva C)

Isolamento OS-level para execução não-confiável (skills/subagentes), absorvido do
`secure_runner.sh` R71 do harness e helenizado como pacote first-class.

## Garantias (PoLP)

| Superfície | Política |
|---|---|
| Sistema (`/usr`, `/bin`, `/lib`, `/etc`) | **read-only** |
| Workspace | RW **apenas** em `$SECURE_WORKSPACE` (montado em `/tmp/workspace`) |
| Vault cognitivo / home | **invisíveis** (tmpfs vazio) |
| Rede | **off** por padrão (`--net` opt-in explícito) |
| Processo | `--unshare-all --die-with-parent --new-session` |

## Uso

```bash
SECURE_WORKSPACE=/tmp/minha-task ./run.sh -- bash script.sh
SECURE_WORKSPACE=/tmp/t ./run.sh --net -- curl https://exemplo.com
```

Requer `bubblewrap` (bwrap) instalado.

## Contrato de integração com Permission.ask

A ativação no runtime segue a mesma filosofia do gate `command_shell`
(FIX S1): execução roteada pelo runner quando policy exigir, com o comando
final visível ao usuário antes da aprovação:

```
permission.ask({ permission: "secure_exec", patterns: [cmd],
                 metadata: { sandbox: "bwrap", workspace }, always: [cmd] })
→ aprovado → spawn via run.sh
→ negado  → DeniedError (default-safe)
```

Configuração futura: `"permission": { "secure_exec": "ask" | "allow" }`.

## Validação adversarial pendente (roadmap)

Antes de ativar por padrão: auditoria de escape (Frente F style) sobre
mounts, env vars herdadas e signals — ver AUDITORIA-opencode-dev §7-C.
