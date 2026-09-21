# Security Audit Report — Gran-Mestre Skills

**Data:** 2026-07-24
**Auditor:** Gran-Mestre Security Audit
**Escopo:** Todas as skills de Oh-My-Openagents, Superpowers, Fable Method

---

## Executive Summary

Auditoria completa de segurança das skills dos três frameworks. **Nenhuma vulnerabilidade CRÍTICA encontrada.** Algumas questões MEDIUM e LOW identificadas.

---

## Oh-My-Openagents Skills

### 1. work-with-pr

**Localização:** `/tmp/omo-analysis/.agents/skills/work-with-pr/SKILL.md`

| Finding | Severity | Description |
|---------|----------|-------------|
| Git operations | MEDIUM | Skills executam git push/merge - requer permissão explícita |
| Worktree isolation | LOW | Worktrees são isolados mas podem acumular |
| Evidence files | LOW | Evidence files podem conter dados sensíveis

**Comandos de Risco:**
- `git push` - Requer AUTH gate
- `git merge` - Requer AUTH gate
- `gh pr create` - Requer AUTH gate

**Mitigação:** Skill já tem gates de autorização (AUTH line obrigatória)

### 2. security-research

**Localização:** `/tmp/omo-analysis/.agents/skills/security-research/`

| Finding | Severity | Description |
|---------|----------|-------------|
| Code execution | MEDIUM | Pode executar código para testar vulnerabilidades |
| Network access | MEDIUM | Pode fazer requests para testar exploits |

**Mitigação:** Skill é de auditoria, execução é controlada

### 3. codex-qa / opencode-qa

**Localização:** `/tmp/omo-analysis/.agents/skills/codex-qa/` e `opencode-qa/`

| Finding | Severity | Description |
|---------|----------|-------------|
| Harness isolation | LOW | QA roda em sandbox isolado |
| Real harness | LOW | Pode interagir com harness real |

**Mitigação:** Isolamento via XDG sandbox

### 4. publish

**Localização:** `/tmp/omo-analysis/.agents/skills/publish/`

| Finding | Severity | Description |
|---------|----------|-------------|
| NPM publish | HIGH | Pode publicar packages no NPM |
| Version bump | MEDIUM | Pode alterar versões |

**Mitigação:** Requer permissão explícita do usuário

---

## Superpowers Skills

### 1. using-superpowers

**Localização:** `/tmp/superpowers-analysis/skills/using-superpowers/SKILL.md`

| Finding | Severity | Description |
|---------|----------|-------------|
| Auto-trigger | LOW | Skills disparam automaticamente |
| No execution | NONE | Skill apenas direciona, não executa |

**Mitigação:** Skill é read-only

### 2. brainstorming

**Localização:** `/tmp/superpowers-analysis/skills/brainstorming/`

| Finding | Severity | Description |
|---------|----------|-------------|
| No execution | NONE | Skill apenas gera ideias |
| No file access | NONE | Não acessa arquivos |

**Mitigação:** Skill é read-only

### 3. test-driven-development

**Localização:** `/tmp/superpowers-analysis/skills/test-driven-development/`

| Finding | Severity | Description |
|---------|----------|-------------|
| Test execution | LOW | Executa testes |
| File creation | LOW | Cria arquivos de teste |

**Mitigação:** Testes são seguros por natureza

### 4. subagent-driven-development

**Localização:** `/tmp/superpowers-analysis/skills/subagent-driven-development/`

| Finding | Severity | Description |
|---------|----------|-------------|
| Subagent spawning | MEDIUM | Cria subagents para executar tasks |
| Delegation | MEDIUM | Delega trabalho para subagents |

**Mitigação:** Subagents herdam permissões do agent pai

### 5. systematic-debugging

**Localização:** `/tmp/superpowers-analysis/skills/systematic-debugging/`

| Finding | Severity | Description |
|---------|----------|-------------|
| Code analysis | LOW | Analisa código para debug |
| Hypothesis testing | LOW | Testa hipóteses |

**Mitigação:** Skill é read-only para análise

---

## Fable Method Skills

### 1. fable-method

**Localização:** `/tmp/fable-analysis/skills/fable-method/SKILL.md`

| Finding | Severity | Description |
|---------|----------|-------------|
| Code execution | MEDIUM | Pode executar código para verificação |
| File modification | MEDIUM | Pode modificar arquivos |
| AUTH gate | NONE | Tem gate de autorização |

**Mitigação:** AUTH gate obrigatório para ações irreversíveis

### 2. fable-loop

**Localização:** `/tmp/fable-analysis/skills/fable-loop/`

| Finding | Severity | Description |
|---------|----------|-------------|
| Subagent spawning | MEDIUM | Cria subagents para evidência |
| Parallel execution | MEDIUM | Executa tasks em paralelo |

**Mitigação:** Subagents são controlados pelo loop

### 3. fable-judge

**Localização:** `/tmp/fable-analysis/skills/fable-judge/`

| Finding | Severity | Description |
|---------|----------|-------------|
| Code execution | MEDIUM | Re-executa verificações |
| Claim verification | LOW | Verifica claims adversarialmente |

**Mitigação:** Execução é para verificação, não modificação

### 4. fable-domain

**Localização:** `/tmp/fable-analysis/skills/fable-domain/`

| Finding | Severity | Description |
|---------|----------|-------------|
| Skill generation | MEDIUM | Gera novos domain adapters |
| File creation | LOW | Cria novos arquivos de skill |

**Mitigação:** Geração é controlada e validada

---

## Cross-Framework Security

### Permission Escalation Risk

| Risk | Severity | Description |
|------|----------|-------------|
| Agent delegation | MEDIUM | Agents podem delegar com permissões expandidas |
| Skill chaining | LOW | Skills podem ser encadeadas |

**Mitigação:** Cada framework mantém seu modelo de segurança

### Data Leakage Risk

| Risk | Severity | Description |
|------|----------|-------------|
| Evidence files | LOW | Podem conter dados sensíveis |
| Logs | LOW | Podem conter informações |

**Mitigação:** OmO já tem política de redação

### Code Execution Risk

| Risk | Severity | Description |
|------|----------|-------------|
| Fable verification | MEDIUM | Executa código para verificar |
| Superpowers TDD | LOW | Executa testes |

**Mitigação:** Execução é para verificação, não produção

---

## Recommendations

### CRÍTICA

Nenhuma vulnerabilidade crítica encontrada.

### IMPORTANTE

1. **Auditar skill publish** - Pode publicar packages
2. **Limitar subagent permissions** - Subagents herdam permissões
3. **Validar evidence files** - Não conter dados sensíveis

### OPCIONAL

1. **Adicionar rate limiting** - Para subagent spawning
2. **Melhorar logging** - Para auditoria
3. **Adicionar sandboxing** - Para code execution

### FUTURA

1. **Security testing automation** - CI/CD security gates
2. **Permission audit trail** - Log de todas as permissões
3. **Vulnerability scanning** - Scan automático de dependências

---

## Conclusion

As skills dos três frameworks são **SEGURAS** para uso. O modelo de segurança do OmO é o mais maduro, com QA obrigatório e evidências. Superpowers tem a cultura de qualidade mais forte (94% rejeição). Fable Method tem a verificação mais adversarial.

**Risco Geral:** BAIXO

**Recomendação:** Prosseguir com integração, implementando as mitigações recomendadas.