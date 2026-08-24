# 📚 Biblioteca de Regras — `/mnt/dados/opencode/config/rules/`

> Estrutura otimizada (2026-08-18 · atualizada 2026-08-24): **bootstrapper conciso carregado globalmente + biblioteca canônica detalhada com lazy-load + doutrinas de sessão sincronizadas (RS1-RS6 / R57-R63)**.
> Pesquisa MIX (docs OpenCode, Anthropic, 60k+ repos): AGENTS.md ideal ≤150-200 linhas; detalhes em biblioteca referenciada — nunca duplicada.

## Decisão arquitetural (arquivo único vs biblioteca)

| Opção | Prós | Contras | Veredito |
|---|---|---|---|
| Arquivo único grande | Simples, tudo em contexto | >200 linhas degrada adesão, custa tokens em TODA sessão, conflitos ao editar | ❌ (era o estado anterior: 41 KB) |
| Biblioteca pura (sem bootstrapper) | Modular, auditável | Agente pode não ler → regras esquecidas | ❌ isolada |
| **Híbrido: bootstrapper conciso + biblioteca** | Essência sempre em contexto (R1-R63); detalhes sob demanda; symlinks preservam compatibilidade | Requer disciplina de referência | ✅ **ESCOLHIDO** |

## Modos de constituição (2026-08-24)

| Modo | Conteúdo | Uso |
|---|---|---|
| **Monolito integral** | AGENTS.md (42k) + global-rules.md (85k, R1-R63 + RS/R57-63) | Auditoria, referência histórica, agentes que exigem texto integral |
| **Compacto** (ATIVO via symlink `~/.config/opencode/AGENTS.md`) | Índice-essência 741 tokens + doutrinas da sessão + guardrails | Sessões TUI — devolve ~39k tokens de janela |
Alternância: `~/.config/opencode/bin/agents-mode.sh [monolito|compacto|status]` (backup automático).

## Índice

| Arquivo | Papel | Carregado automaticamente? |
|---|---|---|
| `AGENTS.md` | **Bootstrapper global** — Constituição R1-R51 essência + R57-R63 da sessão | Sim (via symlink) |
| `global-rules.md` | Texto canônico integral + §REGRAS DA SESSÃO (RS1-RS6/R57-R63) | 🔗 Lazy-load |
| `modules/01-constituicao-nucleo.md` | R1-R14 | 🔗 |
| `modules/02-orquestracao-workflow.md` | R16-R20 | 🔗 |
| `modules/03-rota-janela-vram.md` | R21-R23 | 🔗 |
| `modules/04-workflow-6-fases.md` | R25-R28 | 🔗 |
| `modules/05-metricas-validacao.md` | R34-R42 | 🔗 |
| `modules/06-governanca-scaffolding.md` | R43-R51 | 🔗 |
| `variants/modular/global-rules/*.md` | Split lossless do global-rules (6 chunks) | 🔗 |
| `variants/compacto/AGENTS.md` | **Índice-essência 741 tokens + guardrails da sessão** | ✅ ATIVO |
| `CLAUDE.md` | Preferências globais do usuário | Sim (fallback `~/CLAUDE.md`) |
| `vault-AGENTS.md` | Regras do vault Obsidian | 🔗 |
| `antropofagia-global.md` | Regra de autofagia (R14) | 🔗 |
| `backup-2026-08-18/` | Backup pré-migração | — |

## ⚠️ Armadilha conhecida (documentar, não remover)
`"/mnt/dados/cerebro com IA/AGENTS.md" → rules/vault-AGENTS.md` — desvia agentes que resolvem caminhos relativos a partir do vault (incidente 2026-08-24, Apêndice C do relatório GMB-1).

## Stack de inferência (9 slots + L0 — medidos 2026-08-23/24)

```
GPU :8083 🥇 Ornith-1.5-9B ... ORQUESTRADOR (GM 76.3 rank#1 · nativo 262144 · no-think lei#7)
CPU HOT ...................... :9086 lfm230m 228 · :9089 ternary17 207 · :9088 qwen1.7B 183 ·
                               :9087 qwen2b 155 t0.3 · :9085 judge 139 t0.15 · :9084 qwen0.8b 123
CPU WARM sob demanda ......... :9083 bonsai27B F1-prosa densa 15.72 · ternary8b A2A 44.5-125
L0 Needle 2 .................. dispatcher F4 ~1500 t/s · vector_cache_surrogate semântico
```
Métrica de seleção operacional: **t/s-per-KV-GB** (campeão ternary17 544.8 · orquestrador compra janela 5.8 por design). Doutrina cold/warm: especialistas pesados NÃO pagam aluguel permanente.

## KRON-SUBSTITUIÇÕES (ciclo 15 dias · timer systemd-user + gate hook)

Scout multilíngue (pt/en/es/zh/ja/de/ru · fóruns · YouTube) caçando substituições quantitativas/qualitativas → conflito contra baselines locais → veredito pela filosofia de enxame. Script: `harness/kron-substituicoes.sh` · intel: `cerebro/aprendizados/kron-scouts/`.

## GM-OFICIAL (12/12 tarefas × 4 candidatos · dataset completo)

ornith 76.3 🥇ORQUESTRADOR · qwen9b 74.2⛔§9 CODER c/ verificador · qwen27b 68.5 PLANNER≥96K · bonsai 62.2 curtos. Detalhes: `benchmark/reports/final/GMB1-relatorio-completo.md` (19 adendas + apêndices A-C).

## Regra de catalogação (R51) — procedimento obrigatório

Toda regra nova DEVE entrar AQUI (nunca em arquivo avulso). Template:

```yaml
---
numero: R##
tema: <domínio>
categoria: <harness|config|seguranca|qualidade|processo>
setor: <orquestrador|subagentes|hooks|skills|stack>
escopo: <global|sessao|modulo>
vigencia: YYYY-MM-DD
---
```

1. Adicionar essência em `AGENTS.md` (seção 14, ≤200 linhas total — quebrar em módulo se exceder)
2. Adicionar texto canônico detalhado em `global-rules.md`
3. Atualizar rodapé de histórico do `AGENTS.md` (data + regra)
4. Registrar decisão em `/mnt/dados/cerebro com IA/decisoes/`
5. **Nova (2026-08-24)**: registrar ferramenta associada no `vector_cache_surrogate` (context_memory.db) com convenção canônica — name tipado (`mcp_|hook_|skill_|tool_`) · intent de alta densidade · tags técnicas + fase do grafo
6. **Nova (2026-08-24)**: avaliar candidato pelo t/s-per-KV-GB antes de promover a slot
7. Atualizar este README se a estrutura mudar
