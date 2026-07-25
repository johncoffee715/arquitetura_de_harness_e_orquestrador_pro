# Protocolos do Gran-Mestre

Versão 6.1 — Atualizado com Autofagia (planning-with-files + AAS)

## 1. Roteamento por Complexidade

| Complexidade | Critério | Pipeline | Agentes |
|---|---|---|---|
| **TRIVIAL** | 1 passo, sem side effects | Execução direta | Sisyphus |
| **SIMPLE** | 2-3 passos, escopo fechado | Mini-plano → Atlas | Atlas |
| **MEDIUM** | 3-7 passos, múltiplos arquivos | Prometheus → Héstia → Atlas | 3 agentes |
| **COMPLEX** | 7+ passos, arquitetura envolvida | Prometheus → Héstia → Superpowers → Atlas → Atena | 5 agentes |
| **CRITICAL** | Produção, segurança, dados | Mesmo que COMPLEX + escalona se falhar 2x | 5 agentes |
| **FEATURE** | Design em aberto, requisito ambíguo | Pipeline em Cascata | 6+ agentes |

## 2. Safety Protocol

```
1. ANTES de executar: git rev-parse HEAD → salvar SHA em CONTEXT.md
2. Se falhar: git reset --hard {SHA}
3. Máximo 1 rollback por pipeline
4. Reportar ao usuário com 3 opções:
   - Tentar abordagem diferente
   - Revisar plano com Prometheus
   - Cancelar pipeline
5. Aguardar decisão do usuário — NUNCA continuar rollback automático
```

## 3. Attestation (SHA-256 do Plano)

O Gran-Mestre **atesta a integridade** dos seus planos via SHA-256:

```bash
# Store attestation
./scripts/attest-plan.sh store PLAN.md

# Verify attestation
./scripts/attest-plan.sh verify PLAN.md

# Check (return 0/1)
./scripts/attest-plan.sh check PLAN.md
```

**Hook PreToolUse:** Verifica attestation antes de delegar para Atlas.

## 4. Completion Gate

O Gran-Mestre implementa **completion gate** no Stop hook:

```bash
# Check if plan is complete
./scripts/check-plan-complete.sh PLAN.md
```

**Comportamento:**
- Se plano incompleto → notifica e sugere continuar
- Se plano completo → permite parada normal
- Em modo `--gated` → bloqueia até plano completo

## 5. 2-Action Rule

> "After every 2 view/browser/search operations, IMMEDIATELY save key findings to text files."

Isso evita que informação visual/multimodal seja perdida quando o contexto é resetado.

**Aplicado em:**
- `findings.md` — descobertas de pesquisa
- `progress.md` — log de sessão
- `task_plan.md` — progresso do plano

## 6. 3-Strike Error Protocol

```
ATTEMPT 1: Diagnosticar e corrigir
  → Ler erro com atenção
  → Identificar causa raiz
  → Aplicar correção direcionada

ATTEMPT 2: Abordagem alternativa
  → Mesmo erro? Método diferente
  → Ferramenta diferente? Biblioteca diferente?
  → NUNCA repetir exatamente a mesma ação

ATTEMPT 3: Repensar abordagem
  → Questionar premissas
  → Pesquisar soluções
  → Considerar atualizar o plano

APÓS 3 FALHAS: Escalar ao usuário
```

## 7. Observabilidade

Registrar após cada fase em CONTEXT.md:
```
[Metrics] Phase: {decompose|plan|validate|execute|review}
[Metrics] Route: {TRIVIAL|SIMPLE|MEDIUM|COMPLEX|CRITICAL|FEATURE}
[Metrics] Status: {success|escalated|failed}
```

## 8. Shared Brain (Cerebral Memory)

```
1. ingest_source() — contexto do pipeline
2. create_summary() — aprendizados
3. upsert_entity() — decisões chave
4. upsert_concept() — padrões descobertos
```

## 9. Pipeline em Cascata (FEATURE)

```
FASE 1 — Descoberta (27B): Prometheus → Brainstorming → GATE 1
FASE 2 — Contrato  (27B): Spec Writer → Héstia → GATE 2
FASE 3 — Plano     (27B): Plan Writer → Héstia → GATE 3 → 💾 SHA
FASE 4 — Execução  (30B): Atlas (supervisor) + Implementer (TDD) + Code Reviewer
FASE 5 — Revisão   (30B): Atena (diff total)
FASE 6 — Entrega   (27B): Verification → Héstia → GATE 4 → Memória
```

## 10. Integração com AAS (antigravity-awesome-skills)

**Conceitos transferíveis:**
- Agent-First Control Plane → MCP local para discovery de skills
- AAS Core Stack Validation → compose_stack do Gran-Mestre
- Specialized Plugins → bundles por domínio (Security, DevOps, QA)

**Recursos AAS:** 1,969+ skills catalog, 15.1.0