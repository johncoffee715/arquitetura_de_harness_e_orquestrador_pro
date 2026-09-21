# UNLAZY - Mecanica de Ignicao (R77 camada 3)

## 1. Selecao de motor (catalogo R75 - sempre refutando)

- **Categoria alvo**: `metodologia` (skill de processo; motor = scripts Node zero-dep, NAO LLM).
- **Refutacao do catalogo**: unlazy nao consome inferencia para enforcement - o checker e deterministico. LLM entra so no julgamento de gates manuais e na autoria dos ledgers (contrato-plano :9088 ou orquestrador :8083).
- **Fallback**: sem Node 16+ a skill nao ignita (motor e Node); verificar `node --version` antes.

## 2. Parametros de ignicao (samplers & setup)

```json
{
  "temp": 0.2,
  "top_k": 20,
  "top_p": 0.95,
  "max_tokens": 4096
}
```

- **Ganchos de backend**: nenhum (zero-dependencia). Aprovacoes em `~/.unlazy/approved`; estado de pipeline em `.unlazy/<scope>/`.

## 3. Sequencia de ignicao

1. Validar gabarito (deny) - nenhuma acao antes.
2. `node --version` >= 16 (motor).
3. **Solo**: copiar `templates/gates-leaf.md` -> `GATES.md`; preencher placeholders; `gate-lint.mjs GATES.md` (esperar `LINT OK`).
4. **Orquestrado**: `templates/PLAN.md` -> `.unlazy/<scope>/PLAN.md`; um ledger por folha (`gates/leaf-*.md`) e ramo (`gates/node-*.md`).
5. `gate-check.mjs --status` em todo ledger herdado (parse sem executar; ler cada CHECK/EXPECT/CWD).
6. `--approve` so apos inspecao; executar; `--reverify` para verificacao de pai (NUNCA `--status`).
7. Dispatch paralelo: `--claim` -> wave (`dispatch-check open` -> `task` nativo por folha -> `start --handle <task_id>` -> `seal`) -> esperar -> `return` -> `--reverify` -> `--release`.
8. Gate categorico (R28): relatorio final so com contagens medidas met/unmet/abandoned + todo abandono surfaced.

## 4. Funcoes focadas (Python 30-60 linhas por bloco)

```python
def smoke_unlazy(skill_dir: str, workdir: str) -> dict:
    """Prova de fumaca: ledger minimo passa no checker helenizado."""
    import subprocess, pathlib
    gates = pathlib.Path(workdir, "GATES.md")
    if not gates.exists():
        return {"status": "SKIP", "motivo": "sem GATES.md"}
    r = subprocess.run(["node", f"{skill_dir}/scripts/gate-check.mjs", "--status", str(gates)],
                       capture_output=True, text=True, timeout=30)
    ok = "ALL MET" in r.stdout or "UNMET" in r.stdout
    return {"status": "SUCCESS" if ok else "FAIL", "evidencia": r.stdout.strip()[-200:]}
```

## 5. Enforcement

- Motor recusa ignicao se acao violar deny do gabarito (camada 2 e lei).
- `CHECK:` e codigo: aprovacao explicita vinculada; mudanca de qualquer entrada vinculada invalida a aprovacao.
- Alteracao de sampling sem novo crivo = proibida (R62/R66).
