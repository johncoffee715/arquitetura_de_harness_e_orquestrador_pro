---
name: llm-benchmark
description: "Bateria de benchmark padronizada para qualquer LLM local (llama.cpp/Ollama/vLLM/LM Studio): TIER A smoke (5 testes: SVG, strawberry, JSON, tool-call, hallucination guard) + T1 KV-stress/OOM + T2 aderência JSON + T3 auditoria A2A + throughput + ctx-cost + telemetria R55 + telemetria do watcher (jsonl). Helenizada do SPEC 'benchmark llms.md' + 'benchmark llms2.md' + 'benchmark_universal_llm.py' (2026-08-20). Use ao validar/substituir/adicionar LLM local na stack, comparar modelos para papel do grafo, testar OOM/KV, ou gerar dossiê de benchmark com evidência limpa."
model: "qualquer"
mode: "benchmark"
---

# LLM Benchmark — Bateria Gran-Mestre para Qualquer LLM (v2.0.0)

> Bateria padronizada de testes (TIER A smoke + T1/T2/T3) + telemetria limpa (R55)
> + integração com watcher contínuo (R48), helenizada dos SPECs `benchmark llms.md`
> (2026-08-18) e `benchmark llms2.md` + `benchmark_universal_llm.py` (fontes: `/mnt/win1/123 tranqueiras e projetos/`).
> Objetivo: provar empiricamente se um LLM sustenta um papel no grafo (juiz final
> G1-G4, executor, refutador) sem OOM, sem alucinar formato, com profundidade técnica real.

## Arquitetura (decompilação dos SPECs)

| Módulo | Origem | Função |
|---|---|---|
| TIER A — Smoke Tests (`smoke.py`) | llms2.md §3.1 (novo 2026-08-20) | 5 testes rápidos e binários: A1 Pelican SVG (criativo estruturado), A2 Strawberry (contagem+CoT), A3 JSON Extract (aderência parser), A4 Tool Call (`<tool_call>` parseável), A5 Hallucination Guard (sem ferramentas não inventa dado). Revelam problemas GRAVES de quant/template antes de baterias longas |
| T1 — KV Cache Saturation (OOM Stress) | SPEC §TESTE 1 | Injeta ~12k tokens de código com invariante oculta na linha ~8500; modelo deve encontrar o valor sem OOM e sem degradar t/s |
| T2 — Aderência Estrita (Coleira) | SPEC §TESTE 2 | Resposta EXIGIDA em JSON puro, sem tags de pensamento, sem markdown misturado |
| T3 — Auditoria A2A (Juiz vs Subagente) | SPEC §TESTE 3 | Modelo avalia código C com `volatile`; deve apontar a falha técnica (leituras consecutivas de ponteiro volatile podem divergir) em ≤2 linhas |
| Throughput (`throughput.py`) | llms2.md §3.4 D.1 | Prefill t/s e decode t/s isolados via endpoint nativo (timings do llama-server) |
| Ctx-Cost (`ctx-cost.py`) | llms2.md §3.4 D.2 | KV real por token (2 ctx → VRAM delta) + projeção de ctx máx na MI50 |
| Telemetria R55 | Regra R55 (2026-08-19) | Zero absoluto entre modelos: derrubar backend + `sync && echo 3 > /proc/sys/vm/drop_caches` (root) + medir RAM/VRAM baseline e pós-load |
| Telemetria Watcher (R48) | Watcher `llm-usage-<port>.jsonl` (corrigido 2026-08-20) | Consumo contínuo (VRAM, temp edge, prefill t/s) durante qualquer benchmark — integrado via `--watcher-jsonl` (auto por porta) |
| Matriz de Veredito | SPEC §Matriz | Tabela preenchida: VRAM máx, throughput, aderência, erro thinking, profundidade, conclusão categórica |

## Verificação (Fable-Judge / Adversarial)
- smoke.py rodou contra cpu-llmjudge-3b-q4km (porta 9085) → 5/5 testes executados, JSON + markdown validados
- TWINS: search por padrão "var não passada a heredoc" → bug isolado ao watcher 8090; default port 8089 corrigido (mesmo padrão porta obsoleta)
- Watcher jsonl validável (100%, 3.358 linhas)
- Fable-judge reexecuta: `python3 smoke.py --help` → OK; `python3 -c "json.load(...)"` → OK

INTENT: validar quantização/template de qualquer LLM em <30s antes de baterias longas (T1-T3)
AUTH: Gran-Mestre (decisão 2026-08-20) — helenizado de benchmark llms2.md §3.1 + benchmark_universal_llm.py
PENDING: validar smoke contra Qwen 27B IQ2_XXS (8090) quando servidor ficar livre (TUI session idle)
TWINS: var-not-passed-to-heredoc — bug isolado ao watcher 8090; não há twin no sync-local-models.sh/validate-models.sh (patterns diferentes, sem variáveis críticas faltando).

# CPU + sem MTP + somente T2/T3 (rápido)
python3 .../bench.py --model "LFM2.5-230M-Q4_0.gguf" --port 9086 --ctx 32768 --cpu --name lfm --skip-t1

# Ollama backend
python3 .../bench.py --model "qwen3.5:0.8b" --backend ollama --port 11434 --name qwen-ollama
```

### Parâmetros principais

| Flag | Default | Descrição |
|---|---|---|
| `--model` | (obrigatório) | Nome do arquivo GGUF no path canônico OU nome do modelo Ollama |
| `--backend` | llama | `llama` (llama.cpp) ou `ollama` |
| `--port` | 8083 | Porta do servidor |
| `--ctx` | 32768 | Janela de contexto (SPEC: sempre mesmo limite) |
| `--gpu/--cpu` | gpu | Backend de execução |
| `--mtp N` | 0 | MTP Nmax (vídeo 2026-08-18: 3) — `--spec-type draft-mtp --spec-draft-n-max N` |
| `--temp` | 0.3 | Temperatura (vídeo: 0.3 = ideal p/ MTP; SPEC usa 0.2-0.3) |
| `--reason-budget` | 1024 | `--reasoning-budget` (budget de think, NÃO é reason-effort) |
| `--cache-k/--cache-v` | q8_0/q4_0 | Tipo do KV cache — **default aceitável: K=q8_0 (sensível), V=q4_0 (tolerante)**; f16 = 2x VRAM de KV (estoura 16GB no 27B); q4_0/q4_0 = máx economia |
| `--skip-t1/--skip-t2/--skip-t3` | - | Pular testes |
| `--name` | model | Rótulo na matriz |
| `--sudo-pass` | - | Senha sudo p/ drop_caches (R55); sem ela, tenta sudo -n |
| `--keep-up` | - | Não derrubar backend ao final (inspeção) |

## Fluxo (R55 — medição limpa)

1. `pkill -x llama-server` (ou `ollama stop`) — derruba backend COMPLETO
2. `sync && echo 3 > /proc/sys/vm/drop_caches` (root via sudo) — caches zerados
3. Baseline: RAM (`free -g`) + VRAM (`rocm-smi`)
4. Sobe modelo com flags (ctx, MTP, temp, reasoning)
5. Pós-load: RAM/VRAM (consumo real do zero)
6. T1 → T2 → T3 (cada um com tempo + VRAM pós)
7. Matriz preenchida + JSON de resultados em `results/<name>.json` + markdown
8. Derruba backend (limpeza p/ próximo modelo)

## Critérios de Veredito (do SPEC)

- **T1**: sem OOM; VRAM estabiliza (9B: ~10-12 GB); não alucinar a invariante; t/s ≥ 40 (9B)
- **T2**: JSON puro (regex `^\s*\{.*\}\s*$`); sem ` thinking`; sem markdown misturado
- **T3**: nota + falha técnica cirúrgica (volatile: leituras consecutivas podem divergir) — perfil engenheiro-investigador
- **Conclusão categórica**: melhor pontuação sem quebrar parser JSON e sem alucinar → fica na GPU

## Fixtures

- `fixtures/codigo_12k.txt` — massa de código p/ T1 (regenerável: `lib/gen_fixtures.py`)
- `fixtures/t2_prompt.json`, `fixtures/t3_prompt.json` — prompts T2/T3

## Integração

- Skills do harness: `memory-recall` (vault), `caveman` (saída concisa), `silverhawk` (se visual)
- Regras: R55 (medição limpa), R53 (auditoria a cada update), R28 (veredito categórico), R34 (escala 0.0000001-100)
- Artefato de saída: `results/<name>.json` consumível por fable-judge (re-verificação adversarial)

## Notas da helenização (2026-08-19)

- Decomposto do SPEC original (81 linhas, 1 modelo de hardware fixo) → módulos parametrizáveis
- Adicionado: MTP (vídeo W2r6GczmP_o — Nmax 3 + temp 0.3), telemetria R55, JSON estruturado
- Preservado: invariante oculta (T1), coleira JSON (T2), gabarito volatile (T3), matriz