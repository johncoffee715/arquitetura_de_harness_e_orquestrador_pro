---
setor: pipeline
tipo: plano
data: 2026-09-13
run_id: 78b214b9-5725-4266-bb0f-043ddf624f24
dono: planejador-f23 (Hemisfério Esquerdo)
status: G3 — aguardando aprovação humana
deriva_de: 2026-09-13-snn-conectoma-SPEC.md
---

# PLANO TDD — Protótipo SNN-Conectoma + RAG Obsidian

> Waves bite-sized (R45: ≤3 arquivos/task). Cada task carrega envelope:
> `objective | tools_allowlist | acceptance | output_artifact`.
> Métricas SOLO com critério categórico (R28): `PASSOU_CATEGORICO` / `NAO_PASSOU`.

## Ordem de execução (dependências)

```
Wave 1 (fundação) → Wave 2 (parser) → Wave 3 (event-loop) → Wave 4 (ponte) → Wave 5 (HMI) → Wave 6 (pin)
```

- Wave 1 é pré-requisito de todas (fixture + tipos).
- Wave 2 depende de Wave 1 (fixture CSR).
- Wave 3 depende de Wave 1 (tipos) e Wave 2 (dados parseados).
- Wave 4 depende de Wave 1 (tipos de evento).
- Wave 5 depende de Wave 2 (dados agregados) e Wave 3 (estado de ativação).
- Wave 6 depende de Wave 3 (event-loop) e Wave 4 (ponte) — pin só com runtime validado.

---

## Wave 1 — Fundação: fixture + tipos de domínio

**Task 1.1 — Fixture CSR sintética + tipos de domínio**
- objective: criar fixture CSR pequena (não 125M) + dataclasses de domínio (Sinapse, Regiao, Evento).
- tools_allowlist: [write]
- acceptance: `PASSOU_CATEGORICO` se fixture carrega e tipos instanciam sem erro (import limpo).
- output_artifact: `snn/fixture.py`, `snn/types.py`

**Task 1.2 — Teste de contrato da fixture**
- objective: teste RED que valida shape/estrutura da fixture (n_sinapses, índices CSR válidos).
- tools_allowlist: [write]
- acceptance: `PASSOU_CATEGORICO` se teste falha antes da fixture existir (RED) e passa após (GREEN).
- output_artifact: `snn/test_fixture.py`

---

## Wave 2 — Parser CSR streaming

**Task 2.1 — Parser CSR chunked**
- objective: ler CSR 125M sinapses em chunks, sem materializar matriz densa (R1).
- tools_allowlist: [write]
- acceptance: `PASSOU_CATEGORICO` se parse da fixture retorna contagem correta com pico de RAM < 1GB.
- output_artifact: `snn/parser.py`

**Task 2.2 — Teste do parser (RED→GREEN)**
- objective: teste que valida contagem + streaming + tolerância a formato (R5).
- tools_allowlist: [write]
- acceptance: `PASSOU_CATEGORICO` se teste RED antes do parser e GREEN após, com fixture real.
- output_artifact: `snn/test_parser.py`

---

## Wave 3 — Event-loop LIF assíncrono

**Task 3.1 — Núcleo LIF (neurônio)**
- objective: implementar neurônio LIF (membrana, leak, threshold, reset) puro, sem I/O.
- tools_allowlist: [write]
- acceptance: `PASSOU_CATEGORICO` se neurônio dispara acima do threshold e reseta abaixo (teste unitário).
- output_artifact: `snn/lif.py`

**Task 3.2 — Event-loop assíncrono (asyncio)**
- objective: event-loop que avança passos de simulação de forma assíncrona, sem bloquear.
- tools_allowlist: [write]
- acceptance: `PASSOU_CATEGORICO` se loop processa N passos sem deadlock e com ordem determinística.
- output_artifact: `snn/event_loop.py`

**Task 3.3 — Teste do event-loop**
- objective: teste de integração LIF + event-loop (disparo propagado entre neurônios).
- tools_allowlist: [write]
- acceptance: `PASSOU_CATEGORICO` se spike propaga de A→B com latência esperada.
- output_artifact: `snn/test_event_loop.py`

---

## Wave 4 — Ponte inotify→LLM

**Task 4.1 — Watcher inotify com debounce + backpressure**
- objective: watch do vault Obsidian com debounce e fila limitada (R3).
- tools_allowlist: [write]
- acceptance: `PASSOU_CATEGORICO` se rajada de eventos colapsa em 1 evento pós-debounce e fila não estoura.
- output_artifact: `snn/watcher.py`

**Task 4.2 — Roteador para Qwen/Needle/RWKV7**
- objective: rotear evento de mudança para o endpoint correto (Needle :9091, RWKV7 :9084, Qwen :8083) por categoria.
- tools_allowlist: [write]
- acceptance: `PASSOU_CATEGORICO` se evento de nota roteia ao endpoint certo sem chamada real (mock).
- output_artifact: `snn/router.py`

**Task 4.3 — Teste da ponte**
- objective: teste integrado watcher→router com mock de endpoints.
- tools_allowlist: [write]
- acceptance: `PASSOU_CATEGORICO` se mudança de arquivo dispara roteamento correto.
- output_artifact: `snn/test_ponte.py`

---

## Wave 5 — HMI macro-regiões

**Task 5.1 — Agregação por região**
- objective: agregar sinapses/neurônios em macro-regiões (nunca 166k nós — R22).
- tools_allowlist: [write]
- acceptance: `PASSOU_CATEGORICO` se agregação produz ≤ N regiões (N configurável, default pequeno).
- output_artifact: `snn/aggregate.py`

**Task 5.2 — Render HMI (HTML/terminal)**
- objective: renderizar macro-regiões com estado de ativação do event-loop.
- tools_allowlist: [write]
- acceptance: `PASSOU_CATEGORICO` se HMI renderiza regiões + atividade sem travar.
- output_artifact: `snn/hmi.py`

**Task 5.3 — Teste da HMI**
- objective: teste que valida saída da HMI (estrutura, não pixel).
- tools_allowlist: [write]
- acceptance: `PASSOU_CATEGORICO` se saída contém regiões esperadas e contagem correta.
- output_artifact: `snn/test_hmi.py`

---

## Wave 6 — Thread-pinning pós-validação

**Task 6.1 — Health check de devices (gate)**
- objective: verificar `start-stack.sh` + health check para resolver divergência CPU/VRAM (R4) ANTES de pinar.
- tools_allowlist: [read, bash]
- acceptance: `PASSOU_CATEGORICO` se health check reporta device real de cada slot (9086/9090/9092) sem ambiguidade.
- output_artifact: `snn/health_check.py`

**Task 6.2 — Pin de threads condicional**
- objective: pinar threads do event-loop/ponte APENAS se health check passou (nunca antes).
- tools_allowlist: [write]
- acceptance: `PASSOU_CATEGORICO` se pin é no-op quando health check falha/ambíguo.
- output_artifact: `snn/pin.py`

**Task 6.3 — Teste do pin**
- objective: teste que valida gate (pin bloqueado sem health check válido).
- tools_allowlist: [write]
- acceptance: `PASSOU_CATEGORICO` se pin não executa com health check ausente/ambíguo.
- output_artifact: `snn/test_pin.py`

---

## Critérios de trânsito por métrica (R28)

| Métrica | Critério categórico |
|---|---|
| Contagem de sinapses (parser) | `PASSOU_CATEGORICO` se == valor da fixture |
| Pico de RAM (parser) | `PASSOU_CATEGORICO` se < 1GB |
| Disparo LIF | `PASSOU_CATEGORICO` se spike acima do threshold |
| Propagação de spike | `PASSOU_CATEGORICO` se A→B com latência esperada |
| Debounce (watcher) | `PASSOU_CATEGORICO` se rajada → 1 evento |
| Roteamento (router) | `PASSOU_CATEGORICO` se endpoint correto |
| Agregação (HMI) | `PASSOU_CATEGORICO` se ≤ N regiões |
| Pin gate | `PASSOU_CATEGORICO` se no-op sem health check |

## Budget por wave (tokens estimados)

| Wave | Tasks | Arquivos | Budget estimado |
|---|---|---|---|
| 1 | 2 | 3 | ~2k |
| 2 | 2 | 2 | ~2k |
| 3 | 3 | 3 | ~3k |
| 4 | 3 | 3 | ~3k |
| 5 | 3 | 3 | ~3k |
| 6 | 3 | 3 | ~3k |
| **Total** | **16** | **17** | **~16k** |

## Nota de handoff para F4 (executor)

- Cada task é RED→GREEN com evidência fresca (R29).
- Não implementar nada fora do envelope da task.
- Wave 6 exige health check real (bash) — não inventar device.
- Fixture sintética é o ground truth até o Hefesto absorver o dado real (MaleCNS).