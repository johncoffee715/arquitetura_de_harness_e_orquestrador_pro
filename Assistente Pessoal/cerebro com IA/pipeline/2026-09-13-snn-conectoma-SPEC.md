---
setor: pipeline
tipo: spec
data: 2026-09-13
run_id: 78b214b9-5725-4266-bb0f-043ddf624f24
dono: planejador-f23 (Hemisfério Esquerdo)
status: G2/G3 — aguardando aprovação humana
deriva_de: 2026-09-13-snn-conectoma-CONTEXT.md
---

# SPEC — Protótipo SNN-Conectoma + RAG Obsidian

## 1. Objetivo (uma frase)

Protótipo **user-space** que (a) renderiza uma HMI de macro-regiões do conectoma, (b) faz parse do CSR de 125M sinapses, (c) roda um event-loop LIF assíncrono, e (d) conecta o vault Obsidian via ponte inotify→LLMs — **sem tocar kernel, sem 166k notas, sem alterar gran-mestre/manifesto**.

## 2. Escopo (IN)

| # | Componente | Descrição | Categoria (R75) |
|---|---|---|---|
| E1 | HMI macro-regiões | Visualização agregada (não 166k neurônios individuais) das regiões do conectoma | `hmi` |
| E2 | Parser CSR | Leitor do formato CSR (Compressed Sparse Row) para 125M sinapses, streaming, sem carregar tudo em RAM | `parser` |
| E3 | Event-loop LIF | Simulação assíncrona Leaky Integrate-and-Fire em user-space (threads, não kernel) | `simulacao` |
| E4 | Ponte inotify→LLM | Watch do vault Obsidian → roteia mudanças para Qwen/Needle/RWKV7 | `ponte` |
| E5 | Thread-pinning | Pin de threads **pós-validação** de devices (não antes — divergência flagada no CONTEXT) | `infra` |

## 3. Fora de escopo (OUT)

- ❌ Implementar código (esta task é só contrato/spec/plano).
- ❌ Alterar kernel CachyOS (user-space only, restrição dura).
- ❌ 166k notas individuais no Obsidian (R22/perf — usar macro-regiões).
- ❌ Tocar `gran-mestre/` ou `manifesto_llm.json`.
- ❌ Inventar benchmarks ou paths (só usar evidência real).
- ❌ Absorver material externo (Alura/Cell MaleCNS/Janelia/Neuroglancer) — isso é do Hefesto (run paralelo `snn-hefesto-absorb`).

## 4. Restrições duras (herdadas do CONTEXT)

1. **User-space only** — zero alteração de kernel.
2. **R39 preservado** — gran-mestre fora do cloud.
3. **Hardware**: 32GB DDR4, MI50 16GB VRAM, sem kernel panic.
4. **MIX**: síntese/planejamento cloud (`opencode/muse-spark-1.3-contributor-free`), execução pesada local.
5. **R22**: sem fragmentação de 166k notas — agregar em macro-regiões.
6. **Divergência thread-pinning** (CONTEXT linha 22): manifesto aloca 9086/9090/9092 no CPU, mas `stack_atual.gpu` lista em VRAM. **Desempate = `start-stack.sh` + health check, ANTES de pinar** (task do Hefesto, não desta).

## 5. Riscos mapeados

| Risco | Prob | Impacto | Mitigação |
|---|---|---|---|
| R1: CSR 125M sinapses estoura 32GB se carregado inteiro | Alta | Alto | Parser streaming (chunked), nunca materializar matriz densa |
| R2: Event-loop LIF assíncrono satura CPU e compete com LLMs locais | Média | Médio | Thread-pinning pós-validação + budget de CPU por wave |
| R3: Ponte inotify dispara rajada de eventos em sync do Obsidian | Alta | Médio | Debounce + fila limitada (backpressure) |
| R4: Divergência device (CPU vs VRAM) não resolvida antes do pin | Média | Alto | Gate explícito: pin só após health check (E5) |
| R5: 125M sinapses = dado externo não verificado (MaleCNS parcial) | Média | Médio | Parser tolerante a formato; fallback a fixture sintética pequena |
| R6: HMI macro-regiões vira 166k nós por acidente | Baixa | Alto | Agregação forçada por região (R22) |

## 6. Matriz de validação vs pedido original

| Pedido original | Coberto por | Status |
|---|---|---|
| HMI macro-regiões | E1 | ✅ |
| Parser CSR 125M sinapses | E2 | ✅ |
| Event-loop LIF assíncrono user-space | E3 | ✅ |
| Ponte inotify→Qwen/Needle/RWKV7 | E4 | ✅ |
| Thread-pinning pós-validação de devices | E5 | ✅ |
| Mix local+cloud | §4.4 | ✅ |
| 32GB DDR4 / MI50 16GB / sem kernel panic | §4.3 | ✅ |
| Sem 166k notas | §3 + §4.5 | ✅ |
| Não tocar gran-mestre/manifesto | §3 | ✅ |
| Não inventar benchmarks/paths | §3 | ✅ |
| Self-scaffolding [S-ca] (gerar/refinar artefato funcional) | §8 | ✅ |
| Self-healing [H-e] (debounce+backpressure+fallback fixture) | §9 | ✅ |
| Self-learning [L-e] (ponte vault→LLMs só user-space) | §10 | ✅ |
| Self-ameliorative [A-m] (pin pós-health + gate R34) | §11 | ✅ |
| Imitação FUNCIONAL MaleCNS (não réplica biológica) + Aprovar spec 7-10 | §§8-12 | ✅ |

## 8. [S-ca] self-scaffolding

Definição operacional: bootstrap do grafo dirigido químico + LIF + macro-regiões MB/CX/PPL101 sem 166k notas, imitação FUNCIONAL do MaleCNS v1.0.
[Gate] self-scaffolding → PASSOU_CATEGORICO se HMI+CSR streaming ativos | NAO_PASSOU caso contrário — evidência: health-check log.
Riscos: CSR parcial, agregação errada.

## 9. [H-e] self-healing

Debounce inotify + fila backpressure + fallback fixture sintética.
[Gate] self-healing → PASSOU_CATEGORICO se rajada absorvida sem crash | NAO_PASSOU caso contrário — evidência: contador fila.
Riscos: OOM, starvation LLM.

## 10. [L-e] self-learning

Ponte vault→Qwen/Needle/RWKV7 atualiza só pesos/config user-space, sem kernel.
[Gate] self-learning → PASSOU_CATEGORICO se evento vault roteado | NAO_PASSOU caso contrário — evidência: trace ponte.
Riscos: loop inotify, drift.

## 11. [A-m] self-ameliorative

Thread-pinning só pós start-stack.sh + health + gate métrica R34, sem tocar kernel/manifesto/gran-mestre.
[Gate] self-ameliorative → PASSOU_CATEGORICO se pin pós-health | NAO_PASSOU caso contrário — evidência: exit health.
Riscos: divergência CPU/VRAM, contenção.

## 12. Exit status

- `exit_status: 0` — spec + plano escritos, zero código implementado, G2/G3 prontos para aprovação humana.
- `exit_status: 1` — se qualquer path de escrita falhar (propagar erro bruto, sem mascarar) — valores: exit_status: ok|failed|blocked.