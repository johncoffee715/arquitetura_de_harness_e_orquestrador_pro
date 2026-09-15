---
tags: [aprendizado, hefesto, snn, conectoma, drosophila, csr, event-loop]
data: 2026-09-13
run_id: c9b7fddb-f10f-4e6d-b1ef-50cdf26b1446
---

# Absorção MaleCNS v1.0 → recurso SNN nativo (Hefesto)

## O que foi feito

Pipeline Hefesto completo (DECOMPILAÇÃO→AUTOFAGIA→HELENIZAÇÃO→FORJA) absorvendo o
conectoma *Drosophila* MaleCNS v1.0 (166K neurônios, 312M sinapses) em 3 recursos nativos:

1. **HMI Obsidian** — 4 notas macro-região em `wiki/concepts/snn/` (índice + MB + CX + PPL101).
2. **Spec parser CSR** — `opencode/config/opencode/skills/snn-conectoma/spec-parser-csr.md`.
3. **Esqueleto event-loop SNN** — `.../esqueleto/event_loop.rs` (Rust, Min-Heap + Timing Wheel).

## Proteína extraída (essência)

- Sinapse poliádica → multiedge `pre→post` com peso = contagem de sinapses.
- Conectoma = grafo dirigido; só sinapses químicas (gap junction/neuromodulação FORA).
- Valência (dopamina/octopamina) é canal modulador separado do sensorial (CS/US → plasticidade).
- MB = convergência densa KC→MBON (pooling esparso); CX = representação em anel (heading).

## Lição técnica (anti-alocação no hot path)

- `BinaryHeap` com `Ord` invertido = min-heap por tempo (sem crate externa).
- Borrow duplo (`neurons` vs `heap`) resolvido com spill buffer reutilizável + `mem::take`
  (zero alocação por spike). `.drain()` dentro de loop mantém borrow vivo → usar `mem::take`.
- CSR com `row_ptr` u64 (N×N não cabe em u32); `col_idx` ordenado p/ busca binária.

## Device-map resolvido (divergência do CONTEXT.md)

- 9086/9090/9092 são **CPU** (`-ngl 0`), confirmado via `/proc/<pid>/cmdline` + start-stack.sh.
- String `stack_atual.gpu` no manifesto_llm.json está **stale** (lista esses slots em VRAM).
- Pinagem SNN (taskset): usar 9086/9090/9092; NÃO 9088/9084/9093 (GPU ngl999).

## Limitações (adversarial)

- "PPL101" como ID de cluster: HIGH_CONFIDENCE (manifesto usuário), sem fonte primária aberta.
- DOOMFLY/Alex Wormuth: NÃO verificado (UNKNOWN).
- Sem gap junctions/neuromodulação no grafo → simulação comportamental completa fora do escopo.

## Evidência de execução

- `rustc --test event_loop.rs` → 3 testes verdes, 0 warnings (Rust 1.97.0).
- SHA256 dos 8 arquivos gerados registrados no relatório de retorno.