---
numero: SPEC-AUTOPOIESE-v1
tema: Especificação da camada autopoiética do orquestrador (self-learning · self-scaffolding · self-healing)
categoria: spec
setor: gran-mestre
escopo: harness-portatil
vigencia: 2026-08-25
fontes: prompt_camada_autopoietica_orquestrador.md (canônico) · arch system.md · spec arch.md · auditoria real 2026-08-25
tags: [spec, autopoiese, self-learning, self-scaffolding, self-healing, audit]
---

# SPEC — Camada Autopoiética do Orquestrador v1

> Gerada seguindo `prompt_camada_autopoietica_orquestrador.md` (Blocos 3/11/12).
> Toda afirmação rotulada: **[VERIFICADO]** (visto/testado nesta sessão) · **[PROPOSTA]**
> (decisão de design) · **[PREMISSA]** (lacuna sinalizada) · **[ESPECULATIVO]** (futuro).
> Cada item classificado: 🔴 CRÍTICA · 🟡 IMPORTANTE · 🟢 OPCIONAL · ⏳ FUTURA.

---

## 1. Sumário executivo

O ecossistema OpenCode portátil (`/mnt/dados/Assistente Pessoal/opencode/`) já opera um
grafo físico de 8 slots alinhado às fases F0-F6 **[VERIFICADO]**. A camada autopoiética
NÃO exige reescrita: exige **fechar 6 loops** que hoje estão abertos entre componentes
que já existem. Esta spec define cada loop, seu gatilho, seu artefato e seu gate.
Princípio: **estender, nunca substituir** (Bloco 11 Fase 4 do prompt canônico).

```
hoje:  [vault]──ingestão manual──┐   [watcher R48]──relatório──(sem consumidor)
       [decision-log ARQUIVADO]  │   [circuit-breaker ARQUIVADO]
       [registry ARQUIVADO]      └──[trajectória tracer NOVO ✓]
alvo:  todos os loops fechados com gate humano nos pontos críticos (G1-G4)
```

---

## 2. Auditoria do estado atual — Fase 0 [VERIFICADO]

| Componente | Estado | Evidência |
|---|---|---|
| Árvore portátil opencode (XDG custom) | ✅ ativa | wrapper `bin/opencode` calcula ROOT dinâmico |
| Stack física 7 LLM + Needle2 L0 | ✅ 8/8 saudáveis | start-stack.sh health 7/7 + :8097 smoke |
| Mapeamento slots↔fases F0-F6 | ✅ | RS7 AGENTS.md + ctx-cost.py |
| Vault Obsidian | ✅ | `cerebro com IA/{wiki,aprendizados,decisoes,diario,sessions}` |
| Watcher R48 (delegações→relatório diário) | 🟡 script corrigido, agendar boot | `scripts/watchers/watch_subagents.sh` |
| Config-watcher anti-spam | ✅ | dedupe por hash validado |
| Trajectory tracer | ✅ plugin ativo | `config/opencode/plugin/tracer.js` → state/watcher/trajectory.jsonl |
| Probe de limiar cognitivo | ✅ em curso | alucination_probe.py (100K ÍNTEGRO) |
| **Registry central** | ❌ arquivado | `repos/arquitetura_harness_pro` (122KB, pré-portátil) |
| **Decision-log** | ❌ arquivado | sem gravação ativa |
| **Circuit breaker** | ❌ arquivado | `repos/.../safety/circuit_breaker.py` referência |
| **Watchdog decode (R63)** | ❌ órfãos eliminados hoje | wd.sh era inode-morto |
| **memory-recall skill** | ❌ arquivada | trigger "memória:" inoperante |
| Sandbox de execução | 🟡 criado hoje, sem integração | scripts/sandbox-exec.sh |

---

## 3. Engenharia reversa do existente

Fluxo real hoje: usuário → Gran-Mestre (opencode TUI) → delegação via task tool →
subagentes (nuvem/openrouter ou locais via providers) → tools nativas → tracer registra
execução → sessões persistem em data/opencode.db. O vault é alimentado MANUALMENTE pelo
agente quando lembrado. Não há leitura automática do vault no boot de tarefa, nem
promoção de lição→regra com auditoria, nem recuperação estruturada de memória.

## 4. Análise de gaps (o que impede as 3 capacidades)

### GAP-SL1 🔴 Self-Learning sem loop fechado
Relatório diário R48 nasce mas ninguém consome; lições vão pro vault mas nunca viram
regra auditada; decision-log morto = sem dado para aprender roteamento.

### GAP-SS1 🔴 Self-Scaffolding sem registro vivo
Não há catálogo consultável nem template canônico de módulo; criar skill nova hoje =
copiar arquivo solto, sem versionamento/proveniência/sandbox obrigatório.

### GAP-SH1 🔴 Self-Healing sem watchdog
Queda silenciosa de slot/watcher não dispara nada (evidência: watchers-zumbi de ontem;
llama-servers morreram hoje sem alarme até checagem manual).

### GAP-SH2 🟡 Sem post-mortem estruturado
Falhas viram aprendizado só quando o operador lembra de escrever.

### GAP-COMUM 🟡 Contexto orçamentário sem enforcement
RS7 definiu custos mas nenhum gate impede `-c` ad hoc futuro.

## 5. Predição de riscos (sem esta camada)

1. Recorrência dos zumbis: qualquer migração futura recria órfãos invisíveis → falha em cascata silenciosa
2. Degradação cognitiva do orquestrador: sem evacuação no limiar medido (146K Q4), janelas grandes mascaram perda
3. Proliferação de skills duplicadas a cada autofagia (já ocorrido: 214+ padrões, proveniência parcial)
4. Decisões de roteamento sem histórico → repetição de erros de seleção modelo/fase

## 6. Prevenção — guardrails propostos

| Guardrail | Mecanismo | Prioridade |
|---|---|---|
| G-AUD1 Todo módulo entra por gate | checklist frontmatter (papel·origem·não-faz·validação·versão) antes de registrar | 🔴 |
| G-AUD2 Custo declarado por slot | ctx-cost.py --all no obsidian-sync full diário | 🟡 |
| G-AUD3 Limiar cognitivo vigente | campo `limite_cognitivo_ctx` no manifesto lido pelo orquestrador no boot | 🔴 |
| G-AUD4 Post-mortem obrigatório pós-falha ≥2 tentativas | template fixo → aprendizados/ | 🟡 |

## 7. Correção — mecanismos self-healing concretos

### SH-M1 stack-guard.sh 🔴 [PROPOSTA]
Loop 60s idempotente: health 7+1 slots; slot DOWN → restart cirúrgico (mesmas flags do
start-stack) máx 2×; persistindo → notify dedupe + linha em `decisoes/`.
Estende config-watcher existente (mesmo padrão dedupe). **Nunca reinicia :8083 durante
probe** (lock file state/watcher/.probe-lock).

### SH-M2 circuit-breaker mínimo 🟡 [PROPOSTA]
Porta do arquivo arquivado → `scripts/circuit-breaker.sh <recurso>`: contador JSONL
(falhas consecutivas); 3 falhas → recurso marcado OPEN por cooldown 10min; HALF_OPEN
testa 1 requisição. Sem dependências externas.

### SH-M3 post-mortem automático 🟡
Trazer do legado: toda correção após 2ª tentativa gera nota em `aprendizados/`
com campos: sintoma · causa-raiz · correção · guardrail derivado.

## 8. Refatoração — self-scaffolding concreto

### SS-M1 template-canônico.md 🔴 [PROPOSTA]
`templates/modulo-canonical.md`: papel · origem/proveniência · modelo+fallback ·
o que NÃO faz · ciclo de validação · modo autônomo vs supervisionado · versão.
Todo skill/subagent/hook novo NASCE deste template — sem exceção.

### SS-M2 registry.json vivo 🟡 [PROPOSTA]
Reativar registro em `state/registry.json` (leve): índice {id, tipo, versão, origem,
tags, path} gerado por varredura das árvores config/ + skills/. Comando `registry-rebuild`.

### SS-M3 dedupe obrigatório 🟡
Antes de criar módulo: busca no registry por tags; colisão ≥70% de descrição →
extender o existente (R8 codificado).

## 9. Integração (registro único)

Schema mínimo por entrada do registry (Bloco 10 do canônico):
`{id, tipo∈{plugin,mcp,lsp,hook,skill,subagent,script}, ver, origem, tags[], path,
nao_faz[], validacao, autonomia∈{auto,supervisionado}}`
Descoberta dinâmica: o orquestrador consulta registry-rebuild output; HUD resume ≤200 tokens.

## 10. Comparação atual × proposta

| Aspecto | Hoje | Proposta |
|---|---|---|
| Falha de slot | silenciosa | SH-M1 detecta+reinicia+registra |
| Skill nova | arquivo solto | SS-M1 template+gate G-AUD1 |
| Lição | nota avulsa | SL-M1 pipeline fechado c/ promoção auditada |
| -c de slot | RS7 documentação | G-AUD2 enforcement diário |
| Memória | escrita manual | SL-M0 ingestão no fim de todo pipeline |

## 11. Melhorias técnicas

- **Imediatas**: SH-M1 · SS-M1 · SL-M0 · G-AUD3
- **Médio prazo**: SH-M2 · SS-M2/SS-M3 · SL-M1 · G-AUD2/G-AUD4
- **Longo prazo** ⏳: fine-tuning do orquestrador com decision-log consolidado; A2A entre instâncias; engram retrieval sobre o vault

## 12. Roadmap faseado

**Piloto (esta semana)**: SH-M1 · SS-M1 · SL-M0 · G-AUD3 — fecha os loops críticos sem novo código além de shell/python stdlib
**Construção**: SH-M2/SS-M2/SL-M1/G-AUD2/G-AUD4 — registry vivo + breaker + promoção de lições
**Escala ⏳**: fine-tuning · A2A · métricas MELT consolidadas

## 13. Checklist de validação final

- [x] Fase 0 executada e documentada com evidência
- [x] 3 capacidades com mecanismo concreto (SH-M*, SS-M*, SL-M*)
- [x] 5 camadas mapeadas (Prompt=AGENTS.md · Contexto=ctx-cost/R60-v3 · Harness=start-stack/tracer · Loop=probe/gates · Grafo=mapeamento slots)
- [x] Sem menção órfã (todos os componentes citados existem ou têm path definido)
- [x] Prioridades classificadas
- [x] Auto-auditoria: contradições removidas; afirmações rotuladas; números só de fonte desta sessão

## 14. Entrega plug-and-play

Arquivos a criar (todos sob árvore portátil):
1. `scripts/stack-guard.sh` ← SH-M1 (🔴 piloto)
2. `templates/modulo-canonical.md` ← SS-M1 (🔴 piloto)
3. Hook fim-de-pipeline SL-M0: instrução em AGENTS.md §"APRENDIZADO CONTÍNUO" +obsidian-sync session
4. `state/registry.json` + `scripts/registry-rebuild.sh` (🟡 construção)

---
*Spec v1 — 2026-08-25 · gerada pelo próprio sistema como primeiro artefato autopoiético.*
