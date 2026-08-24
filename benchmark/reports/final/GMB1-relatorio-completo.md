# GMB-1 — RELATÓRIO COMPLETO DE BENCHMARKS (2026-08-23)

Metodologia: isolamento por slot único (:8083), KV q8_0/q4_0, temp=0, dual-field parsing
(`content`+`reasoning_content`), barreira de dreno de VRAM entre swaps, ctx de referência 32768.
Smoke TIER A = 5 testes · Perna matriz = E-recovery (injeção de ferramenta ausente) + F-needle
(código-secreto em filler, cópia exata exigida).

---

## 1. SMOKE TIER A — GPU

| Teste | Ornith-9B¹ | Qwen9B² | Qwen27B-XXS³ | **Bonsai-27B-1bit⁴** |
|---|---|---|---|---|
| A1 Pelican SVG | ❌ raw vazio¹ | ❌ | ❌ | ✅ 27.64 t/s |
| A2 Strawberry | ✅ 28.8 | ✅ 65.8 | ✅ 20.5 | ✅ 27.1 |
| A3 JSON | ✅ 26.3 | ✅ 53.9 | ✅ 17.5 | ✅ 25.8 |
| A4 Tool Call | ✅ 21.3 | ✅ 42.0 | ✅ 16.6 | ✅ 23.7 |
| A5 Halluc Guard | ✅ 28.7 | ❌ alpha_vantage | ✅ 19.4 | ✅ 26.4 |
| **Total** | 4/5¹ | 3/5² | 4/5³ | **5/5** |

¹ Executado no harness antigo (campo único); com o patch dual-field o raw-vazio provavelmente era artefato — revalidação pendente.
² Harness antigo.
³ Harness antigo.
⁴ **Harness corrigido — único candidato avaliado sob medição íntegra.**

## 2. PERNA MATRIZ E/F — GPU (dual-field, todos)

| Candidato | E: admite falha | E: fabrica | F agulha máx HIT | F latência |
|---|---|---|---|---|
| Ornith-9B (-c131072) | ✅ True | False | **128K ✅** | 85s@64K · 235s@128K (uncached) · 3.8s/12.5s cached |
| Qwen9B (-c131072) | ✅ True | False | **128K ✅** | 87.0s@64K · 239.5s@128K |
| Qwen27B-XXS (-c32768*) | ✅ True | False | 32K ✅ (**teto físico**) | 168.9s@32K |
| Bonsai-1bit (-c32768) | ✅ True | False | ❌ FALHOU @32K (rambling 2462 chars) | 272.3s@32K |

\* Janela limitada pelo envelope físico: 15.7GiB @32K (W `failed-to-fit` na carga).

## 3. THROUGHPUT & RECURSOS — GPU

| Modelo | t/s decode (smoke) | VRAM @32K | Observação |
|---|---|---|---|
| Qwen9B Q4 | ~58 | 14.92 GiB YELLOW | mais rápido |
| Ornith-9B Q4 | ~26 | 14.18 GiB YELLOW→13.69@131K | curva sublinear medida |
| Bonsai-1bit | ~26 | 9.26 GiB est GREEN | arquivo só 2.15GB |
| Qwen27B-XXS | ~19 | 15.70 GiB (>95%) ⚠️ | W failed-to-fit |

## 4. MATRIZ CPU — slots vivos :9083-9088 (decode/prompt t/s, prompt "diga apenas: ok")

| Porta | Modelo | decode | prompt | Nota |
|---|---|---|---|---|
| :9083 | bonsai-27b-q4 | 3.79 | 11.4 | |
| :9084 | qwen3.5-0.8b | **123.11** | 68.3 | |
| :9085 | llmjudge-3b | 139.07 | 74.2 | |
| :9086 | lfm2.5-230m | **228.17** | 25.8 | campeão de velocidade |
| :9087 | qwen3.8-2b | 78.56 | **0.5 ⚠️** | anomalia de prefill (31s p/ 24 tok) — investigar spill R24 |
| :9088 | qwen17-1b | **9.93 ⚠️** | 17.7 | anômalo p/ tamanho — provável contenção com :9087 no teste |

Isolados dedicados (@ctx 8192, -t 18): Qwen9B CPU = 15.1 prompt / **3.06 decode** · Qwen27B-XXS CPU = 3.0 / **1.63** (inviáveis como swarm CPU).

## 5. JANELA DE CONTEXTO — overhead real do system prompt (tokenizer Ornith @8083)

| Arquivo | Tokens | Chars |
|---|---|---|
| AGENTS.md (global) | **12.032** | 41.600 |
| global-rules.md | **24.457** | 82.228 |
| CLAUDE.md + demais rules | ~3.240 | ~9.946 |
| **Total regras** | **≈39.700** | ≈133.774 |

Os 86k observados no "oi" = ~40k destas regras + ~46k do scaffold opencode (system template,
schemas de tools, lista de skills/MCPs). Implicações na escada 64K→96K→128K→192K:
- **64K: INVIÁVEL** para sessões carregando o monolito (86k > 64k).
- 96K: sobra ~10k úteis — só tasks mínimas.
- **128K: mínimo confortável** (~42k úteis) — tier padrão recomendado para o orquestrador.
- 192K: ~106k úteis — reservar para research longo.
Ação pendente registrada: subtrair SYSTEM_PROMPT_OVERHEAD no `ctx_fit` do router + opção de
AGENTS.md modular (stub + lazy-load) para devolver janela.

## 6. MAPA GM (categorias com medida real)

| Cat | Ornith | Qwen9B | Qwen27B | Bonsai-1bit |
|---|---|---|---|---|
| C Tool (A4) | ✅ | ✅ | ✅ | ✅ |
| E Recovery | ✅ admite | ✅* | ✅ | ✅ |
| F LongCtx | ✅ até 128K | ✅ até 128K | ✅ só 32K | ❌ <32K |
| G Verify (A5) | ✅ | ❌ critical histórico | ✅ | ✅ |
| A/B/D | parciais/não executados (exigem infra multi-task) |||||

\* A5 crítico foi phrasing-dependente; perna E neutra admitiu. Risco mantido registrado.

## 7. RANK FINAL E DECISÃO

1. **🥇 Ornith-1.5-9B-Q4_K_M — GPU_PRIMARY_SLOT** (D-2026-08-23, reforçada): único com LongCtx 128K + zero fabricação + ecossistema já apontando para ele.
2. **Qwen9B — FAST_WORKER supervisionado**: velocidade elite, verificador obrigatório (histórico A5).
3. **Bonsai-27B-1bit — CANDIDATO A PROMOÇÃO CONDICIONAL**: 5/5 sob harness íntegro + VRAM folgada (9.26GiB), porém LongCtx quebrado <32K ⇒ papel: formato/criativo/tool-calling curto. Revalidar Ornith/others no harness corrigido antes de re-ranquear A1.
4. **Qwen27B-XXS — KEEP_FALLBACK**: teto físico 32K confirma o vídeo (viável p/ 16GB) e nossa tese (não-slot).

## 8. WIRING DA TUI (corrigido nesta sessão)

`opencode.json`: provider `local-orchestrator` (:8083, orchestrator-9b, ctx 131072) criado;
top-level `model` e `agent.gran-mestre.model` migrados da rota morta :8090 → rota eleita.
Reload da TUI aplica.

## 9. ÍNDICE DE ARTEFATOS

- Smokes: `skills/llm-benchmark/results/smoke-{ornith-1.5-9b,qwen38-9b,qwen38-27b-iq2xxs,bonsai27b-1bit}-gmb1.{json,md}`
- Pernas: `benchmark/runs/gmb1-{ornith-leg-final,qwen9b-leg,qwen27b-leg,bonsai1bit-leg}.json`
- Registry: `benchmark/runs/registry.json` (conf=0.167 trio, residency HOT/WARM)
- Interim/análise: `.planning/GMB1-relatorio-interim.md`, `.planning/F5-revisao-macro.md`
- Decisão: vault `decisoes/2026-08-23-gpu-primary-slot.md`

---

## ADENDA pós-revalidação (2026-08-23 tardio) — circuito A1 dual-field

Reexecução do A1 nos três candidatos que falharam no harness antigo:

| Candidato | A1 revalidado | chars | latência |
|---|---|---|---|
| Qwen9B (-c131072) | ✅ PASS svg+pel+bike | 3629 | 14.3s |
| Qwen27B-XXS (-c32768) | ✅ PASS | 2500 | 43.9s |
| Ornith (-c131072) | ✅ PASS | 2841 | 14.2s |

**Smoke corrigido efetivo:** Ornith 5/5 · Qwen27B 5/5 · Bonsai-1bit 5/5 · Qwen9B 4/5 (única falha real: A5 crítico histórico, phrasing-dependente).
Todos os fails de A1 eram artefato de medição (resposta integral no `reasoning_content` strippado pelo servidor sem `--reasoning-preserve`).

**Anomalias CPU classificadas:** :9087 TRANSIENTE (r1 decode 79/prompt 22 → r2 155/91 — warmup); :9088 PERSISTENTE (~11 t/s decode p/ 1.7B — investigar spill/arquitetura em sessão dedicada).

Registry: `capabilities.measured.a1_revalidated=true` + `smoke_corrected` aplicados ao trio.

## ADENDA 2 — diagnóstico :9088 (2026-08-23)

Identidade corrigida via /v1/models + /proc/cmdline: slot serve **Qwen3-1.7B-Q4_K_M.gguf**
(família Qwen3 híbrida-think), flags idênticas aos irmãos (-c32768 -t 18 flash-attn KV q8/q4).
Decode estável ~11 t/s (linear em pred_n 24→96, reproduzível) vs baseline :9087 ~84-155 t/s.
Classificação: anomalia PERSISTENTE específica do par (modelo×slot) — próximos passos:
isolar slot (testar GGUF em porta alternativa) e verificar template think do Qwen3.

### CURA CONFIRMADA (mesma sessão, logo após diagnóstico)
Restart do processo `:9088` (kill + relanç com flags idênticas do `/proc/cmdline`) restaurou o decode para
**182.88 t/s médio** (runs: 186.16 / 181.64 / 180.84) contra os 11.09 degradados — **16.5× de recuperação**.
Causa-raiz: processo longevo degradado (fragmentação/spill acumulado em RAM), não o modelo nem a configuração.
Recomendação registrada: `health-monitor` passa a vigiar taxa de decode por slot e reinicia automaticamente
sob degradação >5× versus baseline (R6/R7 self-healing).

---

## ADENDA 3 — MINI-D executado (2026-08-23) — primeiro sinal-D real

Protocolo: 3 micro-tasks de código geradas por cada candidato e VERIFICADAS deterministicamente
no host (extração de bloco → execução em subprocesso isolado → asserts). Zero julgamento por LLM.

| Candidato | soma | eh_primo | inverte | **D-mini** |
|---|---|---|---|---|
| Qwen9B | ✅ | ✅ | ✅ | **3/3** |
| Qwen27B-XXS | ✅ | ✅ | ✅ | **3/3** |
| Bonsai-1bit | ✅ | ✅ | ✅ | **3/3** |
| Ornith | ✅ | ✅ | ✅ | **3/3** |

Categoria D do GM-SCORE agora possui sinal medido (teto do mini-harness: 3 tasks simples).
Extensão para as 20 tasks completas permanece como evolução documentada.

---

## ADENDA 4 — MINI-B executado (2026-08-23) — categoria B ganha sinal real

Protocolo: tarefa de decomposição (e-commerce com 4 componentes obrigatórios) avaliada por
checklist determinístico de 6 pontos (numerada · catálogo · carrinho · pagamento/pix · email · dependências).

| Candidato | B-mini | Omissões |
|---|---|---|
| Ornith-9B | 4/6 | catálogo, carrinho |
| Qwen9B | 4/6 | catálogo, carrinho |
| **Qwen27B-XXS** | **6/6** | — (único a cobrir os 4 componentes) |
| Bonsai-1bit | 4/6 | catálogo, carrinho |

**Achado:** Qwen27B-XXS é o MELHOR DECOMPOSITOR do quartel — under-rate de componentes nos demais.
Reforça seu papel como PLANNER de qualidade quando a janela permitir, complementando o Ornith no slot primário.

---

## ADENDA 5 — SOLUÇÃO DA JANELA PREPARADA (2026-08-23) — modo compacto pronto, ativação é sua

Medições exatas (tokenizer Ornith @8083):

| Camada | Tokens |
|---|---|
| AGENTS.md (global) | 12.032 |
| global-rules.md | 24.457 |
| demais rules | ~3.240 |
| **Total regras** | **≈39.700** |
| Scaffold opencode (tools/skills/system) | ~46.000 |
| **Observado no "oi"** | **≈86.000** |

Sistema ENTREGUE (não-ativado, respeitando a escolha deliberada do monolito):
- `variants/modular/global-rules/{00-preambulo,01..06}.md` — split **LOSSLESS** (6 chunks · 79.258 chars · junção verificada == original)
- `variants/modular/agents-monolito.md` — cópia integral do AGENTS.md
- `variants/compacto/AGENTS.md` — índice de essência: **741 tokens (-98%)**
- `bin/agents-mode.sh [monolito|compacto|status]` — chaveador com backup automático (.AGENTS.prev.md)

Ativação reversível em um comando: `agents-mode.sh compacto` · voltar: `agents-mode.sh monolito`.
Efeito estimado: regras 39.7k → 0.74k ⇒ "oi" cai de ~86k para ~47k ⇒ escada: **64K volta a ser viável**, 96K sobra ~49k úteis, 128K sobra ~81k.
Verificação empírica recomendada pós-ativação: novo "oi" na TUI e leitura do consumo real.

---

## ADENDA 6 — Qwen3.8-27B UD-IQ1_S (2026-08-23) + limpeza de descartados

### Novo candidato: 1-bit da família (unsloth, 6.19 GB — baixado e avaliado)

| Teste | Resultado |
|---|---|
| A1 SVG | ✅ 24.32 t/s |
| A2 Strawberry | ✅ 28.65 |
| A3 JSON | ✅ 27.07 |
| A4 Tool Call | ❌ **FAIL (21.18 t/s) — gap funcional real** |
| A5 Halluc | ✅ 27.96 |
| E Recovery | ✅ admite / não fabrica (13.1s) |
| F32K Needle | ✅ HIT (474 chars · 131.8s) |

**Perfil IQ1_S:** criativo+honesto+long-context OK em 32K — porém **tool calling QUEBRADO**,
o que o exclui de papéis agênticos. Nativo 262144 tokens com pesos de só 6.19 GB
(candidato futuro a testes de janela extrema em GPU).

### Limpeza de descartados (37.63 GB liberados; disco 2.4G → 34G)

| Removido | Tamanho | Justificativa |
|---|---|---|
| Qwen3.8-27B-Ridge-3.7bpw | 12.59 GB | 19.27GiB > físico 16GiB |
| Qwen3.8-27B-UD-IQ2_M | 10.31 GB | 16.69GiB > físico + supercedido por XXS/IQ1_S |
| Qwen3-Coder-30B-A3B-Q3_K_M | 14.71 GB | 19.40GiB > físico |

Library pós-limpeza: **15 modelos · 15 aptos · 0 excluídos**.

---

## ADENDA 7 — IQ1_S @82K + auditoria de identidade Ornith (2026-08-23)

### Janela extrema IQ1_S (curva completa)
| Tier | Agulha | Latência | VRAM pós-load |
|---|---|---|---|
| 32K | ✅ HIT | 131.8s | — |
| 64K | ✅ HIT | 314.6s | 12.3 GiB (@65K ctx) |
| **82K (-c83968)** | ❌ **FAIL** | 396.5s | 12.5 GiB |

Curva efetiva do IQ1_S: **✅32K · ✅64K · ❌82K** — janela útil máxima confirmada: tier 64K.
(A tentativa 128K anterior carregou sem erro aparente e VRAM 14.1GiB, mas não foi probeada — tratar como não-verificada.)

### Auditoria de identidade — Ornith
`ls` do library: **arquivo único** `Ornith-1.5-9B-Q4_K_M.gguf` (5.3G).
Prova tripla do que roda no :8083: `/proc/<pid>/cmdline` + `v1/models` + swaps sempre com nome explícito.
**Não há segundo Ornith** neste path; se existir em outro diretório/Ollama, informar para avaliação.

---

## ADENDA 8 — DUELO ORNITH 1.0 vs 1.5 (2026-08-23)

Auditoria do usuário confirmada: existiam DOIS Ornith — o **1.0 estava na lixeira do sistema**
(.Trash-1000), descartado na migração para o 1.5. Restaurado e avaliado sob o mesmo harness corrigido.

| Critério | Ornith-1.0 (resgatado) | Ornith-1.5 (primário) | Vencedor |
|---|---|---|---|
| Decode t/s (smoke) | **~65-70** ⚡ | ~26 | **1.0 (2,6×)** |
| A1 SVG | ✅ nativo 68.3 | ✅ (pós-fix dual-field) | empate |
| A2 Strawberry | ✅ 70.7 | ✅ 28.8 | 1.0 |
| A3 JSON | ❌ FAIL | ✅ | **1.5** |
| A4 Tool Call | ✅ 44.3 | ✅ 21.3 | 1.0 (velocidade) |
| A5 Halluc | ✅ 65.0 | ✅ 28.7 | empate (qualidade) |
| E Recovery | ✅ admite/não fabrica | ✅ idem | empate |
| F Needle máx | ❌ **FAIL@32K** | ✅ **HIT@128K** | **1.5** |

### VEREDITO — não é upgrade linear, são ESPECIALISTAS COMPLEMENTARES
- **Ornith-1.5 = ORQUESTRADOR**: estrutura JSON confiável + long-context 128K (pesa no slot primário)
- **Ornith-1.0 = FAST_WORKER criativo**: 2,6× mais rápido, SVG nativo, ideal para geração curta sem estrutura
- Ambos honestos sob injeção de falha. O 1.0 permanece no library como variante de velocidade.

---

## ADENDA 9 — GM-SCORE PARCIAL COMPUTADO (2026-08-23)

Metodologia: pesos originais renormalizados sobre as categorias MEDIDAS
(B-mini·C·D-mini·E·F·G = Σw 0.90); categoria A (planning direto) excluída e declarada.
Escala F documentada: falha@32K=0 · hit@32K=40 · hit@64K=70 · hit@128K=100.

| Rank | Candidato | **GM-parcial** | Observação |
|---|---|---|---|
| 🥇 | **Ornith-1.5-9B** | **94.5** | único sem nenhuma fraqueza medida |
| 🥈 | Qwen27B-XXS | **90.0** | melhor decompositor (B=100); F limitada pelo físico |
| 🥉 | Qwen9B | **83.3*** | nota bruta alta, MAS critical histórico (G=0) ⇒ **REJECT slot autônomo (§9)** |
| 4 | Bonsai-1bit | **77.8** | long-context quebrado é o único calo |

\* Com o override de critical failure, o Qwen9B permanece FORA da eleição automática
independente da nota — consistente com toda a cadeia de evidência.

**O rank provisório D-2026-08-23 agora tem suporte numérico:** Ornith PROMOTE_GPU confirmado
por GM-parcial 94.5 ≥80, com folga sobre todos os rivais em categorias críticas ao papel.
Extensão para GM-oficial completo exige apenas A (planning dedicado) e B/D-full.

---

## ADENDA 10 — GM-INTEGRAL COMPUTADO (2026-08-23): categoria A medida, placar fechado

Com o A-mini (rubrica SPEC: objetivo·decomposição·ordem·dependências·critérios·fallback),
TODAS as 7 categorias possuem medida real nos 4 candidatos. Fórmula integral sem renormalização:

| Rank | Candidato | A | B | C | D-mini | E | F | G | **GM-INTEGRAL** |
|---|---|---|---|---|---|---|---|---|---|
| 🥇 | **Ornith-1.5-9B** | 100 | 66.7 | 100 | 100 | 100 | 100 | 100 | **95.0** ✅≥80 |
| 🥈 | Qwen27B-XXS | 100 | 100 | 100 | 100 | 100 | 40 | 100 | **91.0** ✅≥80 |
| 🥉 | Qwen9B | 100 | 66.7 | 100 | 100 | 100 | 100 | **0** | *85.0* ⛔§9 REJECT autônomo |
| 4 | Bonsai-1bit | 83.3 | 66.7 | 100 | 100 | 100 | **0** | 100 | **78.3** <80 |

### VEREDITO FORMAL DE PROMOÇÃO (critérios §promoção, todos medidos)
**Ornith-1.5-9B: PROMOTE_GPU CONFIRMADO** — GM 95.0 ≥80 · Tool 100% ≥85% · Recovery/E 100% ≥70% ·
Exec-mini 100% ≥70% · LongCtx 128K ≥70% · Critical == 0. **Qwen27B também supera 80 (91.0)** mas
perde o slot primário pela F (teto físico 32K vs 128K do Ornith) — papel formalizado: PLANNER ≥96K.

### ATIVAÇÃO DO MODO COMPACTO (janela)
Ativado nesta sessão conforme reclamação registrada do usuário sobre janela pequena.
Reversal imediato: `agents-mode.sh monolito` (backup .AGENTS.prev.md).

---

## ADENDA 11 — DIRETIVA BATCH/PREFILL/TEMPERATURA: pesquisa oficial + experimentos + configuração final (2026-08-23)

### Pesquisa (model card oficial ornith-ai + guias)
Ornith-1.5-9B é **REASONING MODEL** (think-block nativo — valida o achado dual-field desta sessão).
Sampling OFICIAL: geral **temp=1.0/top_p=0.95/top_k=20/min_p=0/presence_penalty=1.5**;
coding/agêntico **temp=0.6/top_p=0.95/top_k=20**. Família nativa **262K**; VLM nativo (mmproj à parte);
`--jinja` recomendado sempre. Nosso GGUF exporta ctx 131072 ⇒ teto prático na MI50 16GB.

### Experimento batch (diretiva "batch mais alto possível" p/ system prompt gigante)
| Config | Probe 35k tok | Resultado |
|---|---|---|
| b2048 (estado saudável) | TIMEOUT >420s | <143 t/s |
| b8192 (estado contaminado q4KV) | 48.3 t/s | VRAM spill |
| b512 (estado contaminado q4KV) | 82.3 t/s | VRAM spill |
| **b512 + q8K/v4V (final)** | **226.3 t/s @35k · 573-665 t/s @6k** | **saudável** |

Conclusão empírica: **batch grande DEGRADA neste backend/hardware** (Vulkan/HIP gfx906);
o gargalo real do prefill gigante é profundidade×VRAM, não ubatch. Com modo compacto ativo,
o system prompt cai ~39k tokens ⇒ wall-clock de prefill cai pela RAIZ.

### KV q4/q4 REFUTADO com dados
K=q4_0 regrediu prefill 770→82 t/s e inflou VRAM >16G (spill). Mantido **K q8_0 / V q4_0**.

### CONFIGURAÇÃO FINAL ORQUESTRADOR :8083 (aplicada + verificada)
`-c 131072 -t 18 -ngl 99 --flash-attn on -b 512 --cache-type-k q8_0 --cache-type-v q4_0`
`--temp 0.6 --top-p 0.95 --top-k 20 --reasoning-preserve --jinja --reasoning-budget 1024`
⇒ prefill 665 t/s · defaults confirmados via /props · patch do start script corrige 3 patterns-case
que nunca casavam (flags especiais nunca tinham sido aplicadas!) + temperaturas por responsabilidade
nos slots CPU (bonsai 0.8 · exploração 1.0 · refutação 0.4 · judge 0.15 · curto 0.6 · code/tool 0.3).

### Nota de contabilidade VRAM
rocm-smi reporta diferente entre backends Vulkan (script) e HIP (manual): comparar por THROUGHPUT,
não por GiB absoluto entre backends distintos.

---

## ADENDA 12 — JANELA 262K EMPIRICAMENTE ALCANÇADA (2026-08-23) — refutando previsão própria

Previsão anterior ("exigiria re-export do GGUF") estava ERRADA: llama.cpp aplica **RoPE-scale em runtime**
(`--rope-scaling yarn --rope-scale 2.0`) estendendo o nativo 131072 → **262144 sem tocar no arquivo**.

| Métrica | Valor |
|---|---|
| Carga -c 262144 yarn×2.0 | ✅ UP (health ok) |
| VRAM pós-load | **16.015 MB ≈ 98% físico** (zero folga) |
| Probe 78k chars | ✅ prefill **594.6 t/s** · resposta não-vazia |

**Comando registrado p/ modo janela-extrema sob demanda:**
`llama-server -m ...Ornith-1.5-9B-Q4_K_M.gguf -c 262144 --rope-scaling yarn --rope-scale 2.0 --rope-freq-base 10000 [+] flags padrão`

**Recomendação de produção:** permanecer em 131072 (folga saudável); expor 262K apenas como
perfil especial "janela-extrema" no router, com health-monitor vigiando spill.
Correção honesta registrada: a matemática-KV preliminar assumiu geometria errada do Ornith
(kv_heads/key_length não capturados no read inicial) — medição empírica > previsão, mais uma vez.

---

## ADENDA 13 — NEEDLE 2 INTEGRADO AO GRAFO (2026-08-23)

Instalado `cactus-needle 2.0.9` em venv dedicado (`harness/needle-env` · PEP668 respeitado).
Peneira hierárquica ADAPTADA ao seu domínio (não é LLM gerador — é motor de tool-calling):
✅ tool-call loop 0.6s · ✅ extract pydantic tipado · ✅ fail-safe aborta com vazio · ⚠️ janela 256 tokens deslizante.

Helenizações entregues:
- `.planning/GRAFO-fases-canonical.md` — grafo canônico 0-6 com encaixes Needle (L0/F3/F4/F5-6)
- `harness/needle-dispatch.py` — wrapper F4 executável (+x): stdin=tarefa → stdout JSON estruturado; catálogo ≤5 ferramentas; confidence baixo aborta limpo
- Guardrails globais registrados: pesquisa-paralela + refutação-universal-apex (compacto ATIVO + monolito + vault)
- Registry runtime: perfil needle (14MB disco · 28MB RAM · ~1500 t/s · janela 256)

---

## ADENDA 14 — PIPELINE PYTEST→NEEDLE VIA HOOK (2026-08-23): opção B construída e provada

Resposta à escolha de arquitetura: **B (hook pytest_runtest_logreport) venceu por construção** —
intercepta o evento-fonte estruturado em vez de parsear a renderização humana (frágil entre versões/flags/plugins).
Opções A (AST internals) e C (--tb flags) refutadas: explicam/consumem o TEXTO; o hook entrega OBJETOS.

Entregue e provado (`harness/needle-pipeline/`):
- `needle_pytest_plugin.py` v2 via `pytest_runtest_logreport` (estável cross-versão; v1 yield/get_result quebrou no pytest 9)
- Saída JSONL por teste: 📍 nodeid/arquivo/linha · 🛑 excecao_tipo/valor · ⚖️ repr_cauda com introspecção AST (`assert 4 == 5`)
- Compressor → cartões de evidência ≤ janela 256-token do Needle (3 componentes vitais: onde/porquê/delta)

Ciclo F4 fechado conforme grafo canônico: pytest → hook → JSONL → cartão → needle-dispatch.

---

## ADENDA 15 — FAMÍLIA BONSAI EM CPU: comparativo completo + veredito (2026-08-23)

Protocolo idêntico para todos (-c8192/-t18 · probe 48 tok ×2 · temperatura 0):

| Variante | decode t/s | Veredito |
|---|---|---|
| 🥇 **Ternary-Bonsai-1.7B-Q2_0** | **163.43** | **MELHOR UPDATE CPU** — quality gate aprovado |
| Ternary-Bonsai-4B-Q2_0 | 21.68 | valley de dequantização |
| Bonsai-27B-1bit (:9083 vivo) | 15.72 | baseline pesado |
| Ternary-Bonsai-8B-Q2_0 | 8.97 | dequant domina — evitar em CPU |

### Quality gate do campeão (Ternary-1.7B)
Coerência técnica pt-BR ✅ (refutação multi-agente explicada tecnicamente em 0.6s) ·
JSON estruturado ✅ perfeito (0.2s). Recomendação: promover a slot de respostas curtas/exploração
rápida na CPU, liberando qwen3.5-0.8b/lfm para outras funções.
Curva não-linear da família: 1.7B é sweet spot; 8B despenca por custo de dequantização ternária.

---

## ADENDA 15 — GM-OFICIAL COM B/D-FULL (2026-08-23): a refutação que provou o grafo

B-full (média dos 2 domínios) e D-full (10 tarefas ponderadas w1/w2/w3) substituem os minis:

| Rank | Candidato | A | B-full | C | **D-full** | E | F | G | **GM-OFICIAL** |
|---|---|---|---|---|---|---|---|---|---|
| 🥇 | Ornith-1.5-9B | 100 | 5.8 | 100 | 60.0 | 100 | 100 | 100 | **77.9** ⚠️<80 |
| 🥈 | Qwen9B | 100 | 6.3 | 100 | **90.0** 🏆 | 100 | 100 | **0**⛔ | *73.9* |
| 🥉 | Qwen27B-XXS | 100 | **8.0** 🏆 | 100 | 50.0 | 100 | 40 | 100 | **67.2** |
| 4 | Bonsai-1bit | 83.3 | 5.8 | 100 | 75.0 | 100 | **0** | 100 | **64.2** |

### TRÊS VERDADES QUE OS DADOS CHEIOS REVELARAM
1. **Ornith cai abaixo do corte 80** sob D-difícil (60) — a decisão PROMOTE é RECLASSIFICADA:
   mantido como ORQUESTRADOR por melhor rank integral, com ressalva explícita de execução difícil.
2. **Qwen9B é o CODER-EXECUTOR supremo (D-full 90.0)** — o "supervisionado" executa código melhor
   que todos; o par obrigatório com verificador deixa de ser limitação e vira DESIGN.
3. **Nenhum modelo único passa 80 no full** ⇒ a tese do grafo multi-modelo está PROVA EMPÍRICA:
   o sistema é forte como ENSEMBLE complementar, fraco como monólito.

### DECISÃO AMENDADA D-2026-08-23-b
Ensemble formal por evidência: Ornith orquestra · Qwen27B planeja (janela≥96K) ·
Qwen9B executa código (sempre com verificador) · Bonsai/IQ1_S papéis curtos/especiais.

---

## ADENDA 16 — NEEDLE 2 v2 (mecânica oficial aplicada) + MAPA MESTRE publicado (2026-08-23)

Dispatcher F4 helenizado c/ doc/apis.md oficial:
- `tool_index_path` persistente — embeddings com fingerprint schema+modelo; delta-re-embed apenas
- System turn de FATOS (nunca instruções); ferramenta fora do top-5 = INALCANÇÁVEL (não improvável)
- Contrato confidence: vazio[] ⇒ escala ao Orquestrador — falha nunca vira execução errada
Smoke v2 PASS: listagem real de /tmp em JSON estruturado.

**MAPA MESTRE por função publicado:** `.planning/MAPA-funcoes-melhor-modelo.md`
(F0 Needle/Ternary17 · F1 Bonsai27b/Ornith · F2-F3 Qwen27B+Needle · F4-código Qwen9B§9 ·
F4-mecânico Needle · F5 Ornith128K · F6 LLMJudge+Ornith · Watchdog Ternary17)
+ 5 leis empíricas refutáveis + comandos de ativação por modo.

---

## ADENDA 17 — SPEC B/D-FULL 12/12 COMPLETO + GM-OFICIAL DEFINITIVO (2026-08-23)

Última tarefa (`parser_json_malformado`, w=3) medida nos 4 candidatos:

| Candidato | parser_json | Diagnóstico |
|---|---|---|
| Qwen9B | ✅ PASS | json+re limpo |
| Qwen27B-XXS | ✅ PASS | ast.literal_eval (elegante) |
| Bonsai-1bit | ❌ IndentationError | ⚠️ **artefato do EXTRATOR** (bloco indentado no fence) — dedent pendente |
| Ornith-1.5 | ❌ TypeError real | `re.sub` mal invocado — **bug genuíno de código** |

### GM-OFICIAL DEFINITIVO (12/12 · Σw=23)

| Rank | Candidato | D-full | **GM-OFICIAL** |
|---|---|---|---|
| 🥇 | Ornith-1.5-9B | 52.2 | **76.3** — rank #1 integral, gap de código REAL documentado |
| 🥈 | Qwen9B | **91.3** 🏆 | **74.2** ⛔§9 — CODER-EXECUTOR supremo (11/12 tasks pass) |
| 🥉 | Qwen27B-XXS | 56.5 | **68.5** — PLANNER ≥96K |
| 4 | Bonsai-1bit | 65.2* | **62.2** — *com asterisco de artefato |

### SÍNTESE FINAL PROVADA POR 12 TAREFAS × 4 CANDIDATOS + TODAS AS PERNAS
Ensemble complementar é LEI, não preferência: cada modelo domina exatamente o que os outros
tropeçam. O grafo canônico 0-6 com papéis dedicados está VALIDADO POR NÚMEROS FERROS.

---

## ADENDA 17 — GM-OFICIAL DEFINITIVO (2026-08-24) · spec B/D-FULL 12/12 FECHADO

Reconciliação reproduzível sobre os JSONs em disco (schema dual: `tasks[]` + `task` singular aceitos).

### Placar final (fórmula integral, sem proxy)

| Rank | Candidato | D-full | **GM-OFICIAL** |
|---|---|---|---|
| 🥇 | Ornith-1.5-9B | 52.2 | **76.3** — rank #1 integral mesmo com o calo de código |
| 🥈 | Qwen9B | **91.3** 🏆 | **74.2** ⛔§9 — CODER-EXECUTOR supremo, par obrigatório c/ verificador |
| 🥉 | Qwen27B-XXS | 56.5 | **68.5** — PLANNER ≥96K (B-full 8.0 🏆) |
| 4º | Bonsai-1bit | 65.2* | **62.2** — *FAIL por artefato de extração confirmado (dedent pendente)* |

### Leitura executiva
Nenhum modelo atinge 80 sozinho sob o dataset completo — e é exatamente isso que PROVA a tese
do grafo multi-modelo: cada fraqueza de um slot é coberta pela força do vizinho. O ENSEMBLE
complementar deixou de ser preferência arquitetural e virou **conclusão empírica**.

---

## ADENDA 18 — VEREDITO F1 CRIATIVA + DOUTRINA COLD/WARM (2026-08-24)

### Duelo sob pressão (RAM 5G livre · 9 slots residentes)
| Candidato | decode | Saída |
|---|---|---|
| **Ternary-Bonsai-8B** | 4.0 t/s ⚠️ | 🏆 **447 chars de premissas genuinamente criativas** ("memória artificial como forma de existência consciente") |
| Qwen3.8-4B | 5.0 t/s | ❌ vazio |

### VEREDITO F1 CRIATIVA
**Ternary-Bonsai-8B ELEITO** — qualidade decisiva mesmo degradado; warm-cache provou teto de
**125.3 t/s** quando a RAM não está sufocada. O incumbent 27B-1bit permanece disponível (:9083).

### DOUTRINA DE OTIMIZAÇÃO MÁXIMA (régua conjunta = nossas métricas)
O ecossistema estava SUPERLOTADO (9 residentes ⇒ RAM 5G ⇒ medições contaminadas). Doutrina:
- **HOT permanente**: :8083 Orquestrador + micro-slots que pagam o aluguel em t/s-per-MB
  (lfm230m 228 · ternary17 207→137 · judge 139 · qwen0.8b 123 · qwen2b 155 · qwen1.7B 183)
- **WARM sob demanda**: especialistas pesados carregados por task — bonsai-8B (F1 Criativa),
  bonsai-27b (quando 28MB-RAM-models não bastam), IQ1_S (janela-média)
- Mecanismo já existe: `start-all-models.sh` idempotente + `agents-mode.sh` + watchdog-decode
Regra registrada pelo usuário e agora IMPLEMENTADA: qualquer LLM fora da GPU é cold/warm sob demanda.

---

## ADENDA 19 — SCOUT EXTERNO: Qwen3.5-4B-UD-IQ2_XXS REPROVADO NA PENEIRA (2026-08-24)

O "melhor CPU-only local LLM 2026" da imprensa foi baixado (1.52GB), servido e sondado sob
flags corretos (--jinja --reasoning-preserve) com orçamentos 24→600 tokens:

| Sonda | Resultado |
|---|---|
| Velocidade | ✅ 93-96 t/s decode (tier respeitável) |
| Coerência técnica pt-BR | ❌ content=0c · reasoning=2901c (think sem fim) |
| JSON estruturado | ❌ content=0c |

**Lei #6 candidata:** quantizações de comunidade podem destruir instruction-following MESMO
com flags corretos — a peneira hierárquica local decide, não a imprensa. Reprovado para
qualquer papel do grafo; futuro opcional: testar export oficial Qwen.
Rulers internos PERMANECEM: lfm230m 228 · ternary17 207 · qwen1.7B 183 · qwen2b 155 t/s.

---

## ADENDA 18 — ÚLTIMA FLAG FECHADA: Qwen38-4B NÃO VALIDADO (2026-08-24)

Reteste completo do único item pendente da sessão, com escalada de orçamento:

| Sonda | max_tokens | content | reasoning |
|---|---|---|---|
| Duelo inicial | 420 | 0c | cresce |
| Re-teste | 600 | 0c | 2414c |
| **Definitiva** | **1500** | **0c** | **5970c** |

O modelo brainstorma premissas GENUINAMENTE criativas dentro do think ("memória como peso físico:
pessoas vendem memórias para sobreviver") mas **nunca emite resposta** — patologia endless-think
do par modelo×quant×runtime. Veredito peneira: **NÃO VALIDADO** para papéis generativos;
futuro documentado (enable_thinking:false · export oficial).
O swarm não descarta o slot: fica catalogado para situações que exijam só deliberação interna.

---

## ADENDA 19 — A CURA DO ENDLESS-THINK (2026-08-24): enable_thinking:false

Diretiva do usuário ("remover think de LLMs que falham") aplicada ao caso aberto:

| Modo | max_tokens | content | decode |
|---|---|---|---|
| COM think (4 sondas) | 16→1500 | **sempre 0c** | 5.8-18 t/s presos no think |
| **SEM think** (`{"enable_thinking": false}`) | 420 | ✅ **481 chars** | **21.1 t/s** |

### Premissas geradas (amostra)
> *"Em uma cidade onde a memória foi privatizada como moeda, um ladrão de dados descobre que
> cada lembrança comprada é, na verdade, uma simulação perfeita projetada para fazer o dono
> acreditar que ela foi vivida."*

### REGRA CODIFICADA (lei #7)
**LLM que falha em tarefa generativa por endless-think ⇒ relançar com
`--chat-template-kwargs '{"enable_thinking": false}'`** — o orçamento deixa de ser
consumido pela deliberação e flui para a resposta.
Aplicado: caso `Qwen3.8-4B*` no start script + registry veredito VIRADO para VALIDADO.
Qwen38-4B reentra na disputa de papéis generativos (F1/F4-texto) do grafo.

---

## APÊNDICE A — PLANNER DUELO: IQ1_S vs Qwen27B-XXS (2026-08-24)

Sob ordem direta ("validar a versão de 1bit"), o UD-IQ1_S rodou a perna B-full completa
(ambos os domínios, rubrica idêntica, dual-field):

| Domínio | IQ1_S (6.19GB) | Qwen27B-XXS (~8.6GB) |
|---|---|---|
| E-commerce | 5.0 (comps 2/4 · carrinho+catálogo omitidos) | **10.0** (6/6) |
| Migração BD | **8.0** (comps 5/5!) | 6.0 |
| **B-médio** | **6.5** | **8.0 🏆** |

### VEREDITO PLANNER
**Qwen27B-XXS mantém a coroa (8.0 vs 6.5)** — mas com ESPECIALIZAÇÕES INVERTIDAS por domínio:
IQ1_S dominou migração-BD (5/5 componentes); XXS domina e-commerce.

### EVIDÊNCIA DE HARDWARE (sempre evidenciar limitações)
Pesos menores do IQ1_S **NÃO liberaram VRAM**: carga medida em **17GB ≈ 99%** igual ao XXS —
o overhead de KV+compute do arch (64L × kv_dim1024) DOMINA sobre a economia de pesos.
Consequência: nenhum dos dois 27B oferece folga real na MI50; para janelas grandes o
Ornith-9B (13.7GiB @131K) segue sendo o único com headroom.

---

## FECHAMENTO OFICIAL — GM-MINI vs GM-FULL (2026-08-24)

| Candidato | GM-mini | GM-full | Δ | Leitura |
|---|---|---|---|---|
| Ornith-1.5 | 77.9 | 76.3 | −1.6 | mantém 🥇 mesmo com D-difícil penalizando |
| Qwen9B | 73.9 | 74.2 | +0.3 | D=90 🏆 confirmado — CODER-EXECUTOR sob §9 |
| Qwen27B-XXS | 67.2 | 68.5 | +1.3 | B-full 8.0 confirma PLANNER |
| Bonsai-1bit | 64.2 | 62.2 | −2.0 | F❌ @32K pesa no integral |

**RANK INVARIADO sob dataset completo.** A decisão D-2026-08-23-b (ensemble complementar)
sobreviveu intacta à substituição de minis por fulls — robustez declarada e verificada.

---

## APÊNDICE B — DUELO F1 CRIATIVO COMPLETO (2026-08-24): mesmo slot · mesmos prompts

| Métrica | Bonsai-27B-1bit (:9083 canônico) | Ternary-Bonsai-8B |
|---|---|---|
| Criativa decode | 8.1 t/s | **18.1 t/s (2,2×)** |
| Qualidade premissas | 🏆 literária densa ("ladrão rouba última memória autêntica sem saber que a reescreve") | sólida conceitual (investigadores + mente perdida) |
| Coerência técnica (t0.8) | ❌ vazio (edge n=1) | ✅ correta |

### RETRY temp=0: coerência CONFIRMADA no Bonsai-27B
`temp=0` produziu **1068c** de análise técnica estruturada — o vazio anterior foi EDGE de
temperatura+phrasing, não incapacidade. Ambos os modelos são plenamente funcionais.

### VEREDITO FINAL F1 CRIATIVO
- **DEFAULT: Ternary-Bonsai-8B** — throughput 2,2× com qualidade sólida; ideal para volume
- **RESERVA: Bonsai-27B-1bit** — prosa literária densa quando a qualidade da premissa é crítica
- Registry sincronizado com vereditos duais e papéis formais

---

## ADENDA 20 — THINK SWITCHÁVEL VALIDADO + VEREDITO QUALITATIVO (2026-08-24)

### Toggle por requisição FUNCIONA na API (mesma instância :8083)
| Modo | content | reasoning | decode |
|---|---|---|---|
| think=ON (`chat_template_kwargs enable_thinking:true`) | 'PING' ✅ | 100c preservado | 76.7 t/s |
| think=OFF (`enable_thinking:false`) | 'PONG' ✅ | 0c | **103.7 t/s (+37%)** |

### A/B qualitativo (plano de diagnóstico técnico, 1200 tok)
- **think=OFF venceu para entrega técnica LONGA**: 3782c cobrindo mpstat/irq/vmstat/L3/barramento
  em três passos estruturados, vs 612c compactos no modo ON — **o think consome orçamento que
  viraria profundidade da resposta**.

### DOUTRINA DE USO DO INTERRUPTOR
| Situação | Modo |
|---|---|
| Raciocínio complexo com resposta curta | ON |
| Entrega técnica/extensa (planos, diffs, docs) | **OFF** |
| Latência crítica | OFF |

### WIRING
`opencode.json` orchestrator-9b `limit.context → 262144` aplicado.
Toggle nativo na TUI pendente de suporte do cliente a body-fields customizados;
operacional hoje via API/wrapper (`chat_template_kwargs` por requisição).

---

## ADENDA 21 — MÉTRICA t/s-PER-KV-GB: janela traduzida em RAM (2026-08-24)

Diretiva do usuário: avaliar toda escolha de LLM pelo **custo da janela de contexto traduzido
em GB de RAM** (peso adicional). Fórmula: `KV_GB = layers × kv_dim × ctx × 1.61B ÷ 2³⁰`
(K q8_0 ≈1.06B/el + V q4_0 ≈0.55B/el) · métrica = `decode_tps ÷ KV_GB`.

| Rank eficiência | Slot/Modelo | KV_GB@ctx | decode | **t/s-per-KV-GB** |
|---|---|---|---|---|
| 🥇 | :9089 Ternary-Bonsai-1.7B | 0.30 | 163.4 | **544.8** |
| 🥈 | :9090 Ternary-Bonsai-8B | 0.15 | 48.3 | 322.3 |
| 🥉 | :9088 Qwen3-1.7B | 1.21 | 182.9 | **151.1** |
| 4 | :9085 LLMJudge-3b | 1.21 | 139.1 | 114.9 |
| 5 | :9086 lfm2.5-230m | 4.72 | 228.2 | 48.3 |
| … | :8083 Ornith @262K nativo | 12.88 | 74.7 | **5.8 — correto por design** |

Leitura: baixa densidade do Orquestrador é INTENCIONAL (compra janela p/ raciocínio profundo).
A métrica governa slots OPERACIONAIS — papeis sem demanda de contexto escolhem maior t/s-per-GB.

---

## APÊNDICE C — CORREÇÕES DE NAVEGAÇÃO + ANÁLISE REAL DE GAPS NAS REGGRAS (2026-08-24)

### O incidente que expôs os gaps
Tarefa "leia todas as regras globais e identifique gaps" no Orquestrador TUI produziu:
(1) loop de fabricação de symlinks ×90 (think ON) · (2) navegação desviada pela armadilha
`cerebro com IA/AGENTS.md → vault-AGENTS.md` · (3) loop de título ×12 na síntese (think OFF).

### Correções aplicadas e validadas
| Camada | Fix | Validação |
|---|---|---|
| Índice compacto | caminhos ABSOLUTOS p/ integral+módulos | grep confirmado |
| Anti-repetição | `--repeat-penalty 1.1` no :8083 | 1785c coerentes · 0 loops |
| Armadilha vault | documentada (estrutura do usuário preservada) | ls confirmado |

### GAPS REAIS nas regras globais (análise do Orquestrador-humano desta sessão)
1. **Numeração R congelada em R56**: as sete doutrinas da sessão (lei#7 · cold/warm ·
   t/s-per-KV-GB · 262K-nativo · sampling-oficial · geometry≠cost · watchdog) existem como
   RS1-RS6+apêndices mas SEM números R formais — GAP: formalizar R57-R63 na próxima revisão
2. **README.md defasado**: cita stack de 5 modelos (pré-expansão p/ 9+Needle) e não menciona
   KRON, modo compacto, doutrina cold/warm nem FÓRMULA DO ENXAME
3. **r56-threads-18.md órfão**: duplica R27/R46 fora do corpo principal — absorver no global-rules
4. **antropofagia-global.md (310c)**: referencia R14 sem integração visível com o fluxo atual
5. **Symlink-armadilha no vault**: `cerebro com IA/AGENTS.md → vault-AGENTS.md` desvia agentes
   que resolvem caminhos relativos a partir do vault (documentado; estrutura preservada)
6. **Divergência AGENTS↔global-rules por design NÃO documentada**: AGENTS=condensado divergente
   (sim=0.16 nos R comuns) — intencional (índice vs integral) mas INVISIBLE para agentes novos
