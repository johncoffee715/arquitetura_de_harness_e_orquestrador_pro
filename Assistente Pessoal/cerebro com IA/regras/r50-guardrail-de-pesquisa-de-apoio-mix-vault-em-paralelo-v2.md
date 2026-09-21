---
regra: R50
titulo: "Guardrail de Pesquisa de Apoio (MIX + Vault em Paralelo)"
fonte: AGENTS.md (linha 748)
data: 2026-09-11
---

## R50 — Guardrail de Pesquisa de Apoio (MIX + Vault em Paralelo)
Sempre que a task gerar dúvidas no escopo do orquestrador (ambiguidade de rota, referência
desconhecida, incerteza de abordagem, boas práticas não dominadas), ANTES de decidir:
(1) vasculhar a internet para apoio via MIX (≥2 rodadas de buscas web paralelas multi-idioma —
inglês, russo, chinês, japonês, alemão, português etc.) + Dev Loop, extraindo referência CONCISA
(síntese tabelada; nunca cópia literal) para destrinchar a task com o máximo de eficiência
possível; (2) EM PARALELO, verificar no vault Obsidian (/mnt/dados/Assistente Pessoal/cerebro com IA/) similaridades
(aprendizados/, decisoes/, wiki/, evidências) para aproveitar conhecimento já digerido do harness
e evitar re-trabalho; (3) cruzar as duas fontes (externa + vault) com dissecação técnica (R46)
e benchmarks externos (R45) antes de definir rota; (4) após concluir a task, helenizar o
aprendizado no vault (R14/R26: aprendizados/ + log.md) e, se aplicável, gerar scaffolding (R44).
Fonte externa é APOIO de decisão, nunca verdade absoluta — evidência empírica local (R45) e
veredito do pipeline (R28) prevalecem. Regra em vigor desde 2026-08-18 (pedido do usuário).
- GUARDRAIL GLOBAL: pesquisa web paralela obrigatória para toda task (diretiva usuário 2026-08-23)
- GUARDRAIL GLOBAL REFUTAÇÃO UNIVERSAL APEX: orquestrador refuta o usuário e conduz loop de refutação entre LLMs baseado em fatos/dados/argumentos irrefutáveis — meta: ápice em todas as métricas cabíveis (diretiva usuário 2026-08-23)
- FILOSOFIA DE ENXAME (doutrina central): 1 abelha não derruba elefante; ENXAME PROPORCIONAL derruba — pequenos especialistas coordenados > generalistas gordos (validado GM-oficial 12/12)
- FÓRMULA DO ENXAME EFICAZ: LLMs pequenos·especialistas·precisos·rápidos = swarm eficaz (destilação final, validada por 12/12 tarefas × 4 candidatos + todas as pernas E/F/A/B/G)
- GUARDRAIL PERFIS DE SERVING (R66): KV·temp·MTP·think·quant-KV(K e V separada)·batch/ubatch·ctx SEMPRE parametrizados por crivo empírico (sweep prefill/decode/VRAM-pico vs teto 15.85GB) por função no grafo — FIXOS, sem defaults silenciosos. Exemplo canônico validado 24/08: Ornith-1.5-9B {ctx 262144 nativo · K=q5_0 · V=q4_0 · b2048/ub1024 · t0.6} = prefill 491 · decode 67.8 · pico 10.11GB. Alteração sem novo crivo = proibida (R62). Detalhe por slot: manifesto_llm.json

---

# ═══ REGRAS DA SESSÃO 2026-08-23/24 (sync compacto ATIVO ⇄ monolito · RS1-RS6) ═══
Fontes: Adendas 7-21 · validação GM-oficial 12/12 tarefas ×4 candidatos · rank invariado mini↔full

**RS1 — LEI #7 ENDLESS-THINK ⇒ NO-THINK**: LLM que falha generativo por think infinito ⇒ relançar com `--chat-template-kwargs '{"enable_thinking": false}'`. Curou Qwen38-4B (0c→481c @21 t/s) e o loop de fabricação do próprio Orchestrator no TUI (symlink-fantasma ×90).
**RS2 — DOUTRINA COLD/WARM**: GPU = 1 LLM (Ornith). CPU HOT = micro-slots rentáveis. WARM sob demanda = especialistas pesados (Bonsai-27B F1-prosa · Ternary-8B A2A · IQ1_S reserva-BD). Mecanismos: start script idempotente + watchdog-decode >5× ⇒ restart cirúrgico do slot.
**RS3 — MÉTRICA t/s-PER-KV-GB**: KV@ctx = camadas × kv_dim × ctx × ~1.61B ÷ 2³⁰. Seleção operacional = máxima densidade. Campeões: ternary17 544.8 · qwen1.7B 151.1 · judge 114.9. Orquestrador compra janela (5.8) POR DESIGN.
**RS4 — ORNITH NATIVO 262144**: declarado no próprio GGUF (qwen35.context_length). Produção @262K via yarn×2.0 (76% VRAM idle-fill validado). Rodar 131072 causava loop compactação/perda em reasoning-model.
**RS5 — SAMPLING OFICIAL POR RESPONSABILIDADE**: agentic/coding t0.6 tk20 tp0.95 · criativo t0.8-1.0 pp1.5 · judge ≤0.15 · code/tool ≤0.3 · exploração ≥1.0. Defaults no start script por slot.
**RS6 — GEOMETRIA DECLARADA ≠ CUSTO REAL**: kv_heads/key_length variam por export; fórmula cega produziu lixo (1648 GiB @16K). Medir smaps_rollup-anon/VRAM por bancada antes de teorizar.

---

# ═══ REGRAS DA SESSÃO 2026-08-23/24 — FORMALIZADAS 2026-08-24 (ex-RS1-RS6) ═══

- **R57 — LEI #7 ENDLESS-THINK ⇒ NO-THINK**: LLM que falha em tarefa generativa por think infinito (content=0 com reasoning explosivo) ⇒ relançar com `--chat-template-kwargs '{"enable_thinking": false}'`. Curou Qwen38-4B (0c→481c @21 t/s) e o loop de fabricação do Orchestrator no TUI (symlink-fantasma ×90). ON permanece disponível por requisição (`chat_template_kwargs`) para raciocínio complexo de saída curta.
- **R58 — DOUTRINA COLD/WARM**: GPU = 1 LLM (Ornith rank#1). CPU HOT = micro-slots rentáveis em t/s-per-anon-MB. WARM sob demanda = especialistas pesados (Bonsai-27B F1-prosa · Ternary-8B Refutação-A2A · IQ1_S reserva-BD-migração). Mecanismos: start script idempotente + watchdog-decode R63.
- **R59 — MÉTRICA t/s-PER-KV-GB**: KV@ctx = camadas × kv_dim × ctx × ~1.61B ÷ 2³⁰ (K q8_0≈1.06B/el + V q4_0≈0.55B/el). Seleção operacional = máxima densidade. Campeões medidos: ternary17 **544.8** 🏆 · qwen1.7B 151.1 · judge 114.9. Orquestrador compra janela (5.8) POR DESIGN — janela é o produto dele.
- **R60 — DESCONTINUADA (2026-09-18, ordem do usuário; auditoria Hefesto)**: o fixo 131072 (2026-08-24) ficou obsoleto após o crivo atual do harness/ecossistema. Estado vigente: ctx EFETIVO do Ornith = **262144 nativo** (declarado no próprio GGUF, qwen35.context_length), produzido via yarn×2.0 e validado no crivo R66/R50 ({ctx 262144 · K q4_0 · V q4_0 · ΔPPL +0.0006 ≈ 13% do custo FP16}) — launcher vivo: `restart-stack.sh -c 262144 $KV` + `stack-final-flags.json` (8083: ctx 262144, cache q4_0/q4_0). Rodar `-c` abaixo de 262144 causava loop de compactação/perda em reasoning-model (RS4) e desperdiça a janela nativa comprada por design (R59). Fonte: auditoria GGUF header + restart-stack.sh + stack-final-flags.json.
- **R61 — SAMPLING OFICIAL POR RESPONSABILIDADE**: agentic/coding t0.6 tk20 tp0.95 · criativo t0.8-1.0 pp1.5 · judge ≤0.15 · code/tool ≤0.3 · exploração ≥1.0. Defaults no start script por slot.
- **R62 — GEOMETRIA DECLARADA ≠ CUSTO REAL**: kv_heads/key_length variam por export; fórmula cega produziu lixo (1648 GiB @16K). Medir smaps_rollup-anon/VRAM por bancada antes de teorizar.
- **R63 — WATCHDOG-DECODE**: queda >5× vs baseline do slot ⇒ processo degradado ⇒ restart cirúrgico (kill+relanç flags idênticas). Baselines: ornith 26 · bonsai27b-cpu 15.72 · lfm230m 228 · ternary17 207 · ternary8b 44.5 · qwen2b 155 · judge 139 · qwen0.8b 123 · qwen1.7B 182.88.
- **R64 — ESCADA DE CONTEXTO ESTÁTICA POR VOCAÇÃO (corrigida 2026-09-18, auditoria Hefesto)**: a escada de janelas (16K→32K→131K→262K) é TOPOLOGIA congelada por papel do slot, não scheduler dinâmico: llama.cpp fixa KV no boot; múltiplas instâncias do mesmo modelo estouram a MI50 (pesos ×N). Escada dinâmica intra-modelo = PROIBIDA por medida (RS4/R66: **262144 é o teto nativo EFETIVO do Ornith** — topo da escada, não degrau removível). Ganho de TTFT mora na camada CONTEXTO (filtrar pré-prefill via `needle`/`context-selector` — wrapper global R67), nunca em manobra de serving.
- **R65 — ROTEAMENTO HÍBRIDO EM CAMADAS (amplia R28 p/ produção; disjuntor + score)**: alocação fase↔modelo usa DUAS camadas em ordem estrita: (1) DISJUNTORES determinísticos por limiar medido — F4 exige tps_decode ≥100 (loop TDD multiplica latência; violação = thread starvation do loop externo); F1/F2/F5 exigem GM-oficial ≥60; refutação exige tps ≥180. Limiar violado = BLOQUEIO absoluto, incompensável. (2) SCORE elástico `w_logic*GM + w_speed*norm(tps)` SOMENTE dentro do conjunto elegível (pesos por fase no manifesto_llm.json). Fonte de verdade: `/mnt/dados/Assistente Pessoal/modelos LLM/manifesto_llm.json` — preenchido por auditoria local (GGUF header + R63 + GMB); nulls restantes = alvo de busca web paralelizada (HF/papers/fóruns).
- **R67 — UNIDADE DO ORQUESTRADOR (sem rótulos)**: não existem marcas (superpowers, OMO, TDD, MoE, needle...) — toda capacidade absorvida por autofagia/helenização PERTENCE ao Orquestrador. Todo o arsenal do registro (agent-registry v2.2, 344+ entries) está a serviço do LLM primário GM: skills/MCPs/LSP via sessão · needle-L0 via wrapper global `needle` · métricas via watchdog (orchestrator-metrics.jsonl, diff de contadores do server — independente de plugins) · estado via harness_state.json. HUD/métricas do GM leem do ESTADO DO GM, nunca de plugins de terceiros (que mudam de versão e perdem features).
- **R68 — WATCHERS INICIAM COM O ORQUESTRADOR**: o launcher dos modelos garante os vigias de pé ao subir o primário (gran-mestre-wd · config-watcher · llm-usage@porta) — watchdog nunca fica para trás nem troca o modelo do launcher (respawn usa o MESMO launcher). Sem watcher órfão, sem primário sem vigilância.
- **R69 — CONFIG MODULAR DO ORQUESTRADOR (ID neutro, zero acoplamento)**: a config do OpenCode NUNCA aponta nome de modelo — o provider usa ID neutro `orchestrator` (:8083 serve o que o launcher carregar). Troca de modelo = editar APENAS o launcher; o capture (R68) sincroniza limit.context automaticamente via /props. Proibido keys de provider com nome de GGUF/versão (quebra sintaxe a cada troca — ocorrido 24/08).
- **R70 — PRESERVAÇÃO DA JANELA DO ORQUESTRADOR (guardrail imprescindível)**: o primário NÃO lê, NÃO escreve, NÃO corrige, NÃO faz trabalho pesado — cada token bruto na janela é janela perdida (evidência 24/08: estouro 146K). O primário: **delega, ignita, julga, gerencia, supervisiona, mentora, faz self-improvement, self-learning, self-scaffolding**. EXCEÇÃO ÚNICA de leitura: diff CURTO quando necessário para julgar, refutar, delegar, ignitar, gerenciar, supervisionar ou mentorar. Trabalho bruto (leitura extensa, escrita, correção iterativa, pesquisa longa) vai SEMPRE para subagentes frescos, que devolvem ao GM apenas evidências e resumos destilados. O GM consome estado compacto (harness_state, orchestrator-metrics, resumos) — nunca a matéria-prima.

---
