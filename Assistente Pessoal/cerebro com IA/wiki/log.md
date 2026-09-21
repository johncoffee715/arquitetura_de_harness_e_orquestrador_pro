# Log do Cérebro

Histórico cronológico de operações no wiki — ativações neurais.

## 2026-07-29 (Segunda Sessão) — Otimização Neural 13 Métodos

### Neurônios Criados
- `wiki/concepts/ppr-cascade.md` — Recuperação neural 5 estágios sem embeddings
- `decisoes/2026-07-29-otimizacao-neural-obsidian.md` — Decisão dos 13 métodos
- `hot.md` — Contexto quente da rede neural (~500 palavras)
- `.manifest.json` — SHA-256 delta tracking (14 neurônios)

### Neurônios Atualizados
- `OBSIDIAN_COGNITIVE_BRAIN.md` → v2.1.0 (13 métodos de otimização)
- `REGISTRY_SUBAGENTS.md` → v2.1.0 (tags granulares)
- `index.md` — 6 entidades, 4 conceitos, 3 decisões
- `pipeline/contexto-atual.md` — sinapses ativas adicionadas
- `entities/gran-mestre.md` — v7 com delegação dinâmica

### Métricas da Sessão
- Coesão neural: 0.58 (excelente ✅)
- God nodes: gran-mestre (10 links), delegacao-dinamica (8), antropofagia (7), dev-loop (6)
- Manifest: 14 neurônios rastreados
- Dashboard: METRICS_DASHBOARD.py pronto

### Aprendizados
- hot.md elimina scan frio do vault inteiro
- SHA-256 > timestamp para detectar drift real
- PPR cascade > embeddings para recall semântico em grafos de [[links]]
- Cohesion scoring revela saúde da rede em um número

---

## 2026-07-29 (Primeira Sessão) — Delegação Dinâmica + Dev Loop + Autofagia 35 Fontes

### Neurônios Criados
- `wiki/entities/gran-mestre.md` — atualizado para v7 (delegação dinâmica)
- `wiki/concepts/delegacao-dinamica.md` — pipeline líquido
- `wiki/concepts/dev-loop.md` — 3 níveis de iteração
- `decisoes/2026-07-29-gran-mestre-v7-mix-dev-loop.md` — decisão arquivada
- `aprendizados/2026-07-29_autofagia-35-fontes.md` — aprendizado arquivado
- `pipeline/contexto-atual.md` — working memory atualizada

### Sinapses Criadas
- delegação-dinamica ⟷ antropofagia-tecnologica
- delegação-dinamica ⟷ gran-mestre
- dev-loop ⟷ gran-mestre
- dev-loop ⟷ delegação-dinamica
- 2026-07-29-decisao ⟷ 2026-07-25-decisao

### Arquivos Modificados (fora do vault)
- SKILL.md, REGISTRY_SUBAGENTS.md, PIPELINE_MODES.md, INVENTORY.md,
  MIX_MODE.md, GLOBAL_POLICY.md, INVENTORY_AUDIT.md, dev-loop/SKILL.md

### Padrões Helenizados
- 86 padrões de 35+ fontes em 10 áreas
- Registry: 61 subagents com tags
- Modelo único: omniroute/auto/best-free

---

## 2026-07-16

### 11:00 — Ingestão inicial
- Vídeo: Rafael Quintanilha — "Transformei meu Obsidian em um cérebro para meus agentes de IA"
- Vídeo 2: https://www.youtube.com/watch?v=PqJJTmqukAo (pendente)
- Pattern: LLM Wiki de Andrej Karpathy

### 11:10 — Estrutura criada
- AGENTS.md schema escrito
- Diretórios wiki/ criados
- Skill cerebral-wikia criada

## [2026-08-25] decisão | reinstalação-harness-limpo
- Harness OpenCode reinstalado do zero em `/mnt/dados/Assistente Pessoal/opencode/` — wrapper autônomo (XDG próprio), binário v1.18.23 com SHA verificado, AGENTS.md R1–R50 restaurado dos repos
- Autofagia de 12 vestígios da instalação antiga; causa-raiz documentada (10 symlinks `$HOME → /mnt/dados/opencode` + fantasma `/usr/local/bin`)
- ⚠️ auth.json exposto em repo público → rotacionar chaves
- [[decisoes/2026-08-25-reinstalacao-harness-limpo]] · relatório: `Assistente Pessoal/projeto opencode/harness/AUDITORIA-MIGRACAO-2026-08-25.md`

## 2026-08-26 — Absorção sentinel-guard (hefesto G-D→G-A→G-H→G-F)
- Artefato externo = POISON confirmado: SQLi como caminho feliz (F-001), key `sk-live-*` hardcoded, validate_token fraudulento (score 96.5 sem verificar) — 10 falhas catalogadas com evidência
- Forjado global: `sentinel_guard.py` (63 linhas exec., cobertura 100%, 24 testes) + subagent `sentinel-guard.md` + scaffold `mini_coverage.py`
- Gate segurança existente: PASSOU_CATEGORICO · Panteão 96.75 (>95 convergiu)
- ⚠️ Key do original em /tmp plaintext → rotacionar
- [[aprendizados/2026-08-26_absorcao-sentinel-guard-hefesto]]

## 2026-08-26 — Swap LLM Stack CPU (R52 + R54)
- **9086 LFM1.2B Q4_K_M fica** (730MB, 3.8 KB/tok, 30.5 pico/10.3 carga, IFEval 88.42) — reflexo R42/GBNF
- **9087 Qwen3.8-9B (6.2GB UNKNOWN 0.4 t/s) → Granite 4.2-3B Q4_K_M** (2.24GB, 25.0 KB/tok, 3.25 t/s, RULER 67/55, BFCL 52.41, AIME 78.33, 12 línguas com PT)
- Candidatos rejeitados: G9v3-3B (en/zh UNKNOWN), Ling-3.0-tiny (7.9B/1.3B MoE real 4.82GB RAM bloqueante)
- R54 guardrail: Gran-Mestre preserva janela delegando, subagents devolvem só supra-sumo ≤25 linhas
- Health 9/9 ok (8083 Ornith 212992 q4_0), KV 11.99GB, inventário R52 sync
- [[summaries/2026-08-26-swap-llm-stack]] · [[decisoes/2026-08-26-swap-llm-stack]] · [[aprendizados/2026-08-26_swap-llm-stack]]

## 2026-09-13 — Absorção MaleCNS v1.0 → recurso SNN nativo (hefesto snn-hefesto-absorb)
- Artefato externo = conectoma Drosophila MaleCNS v1.0 (166K neurônios, 312M sinapses) → 3 recursos nativos
- HMI Obsidian: `wiki/concepts/snn/` 4 notas macro-região (índice + Corpos Cogumelo + Complexo Central + PPL101)
- Spec parser CSR + esqueleto event-loop SNN (Rust, Min-Heap/Timing Wheel): `opencode/config/opencode/skills/snn-conectoma/`
- Device-map validado: 9086/9090/9092 = CPU (-ngl 0); string `stack_atual.gpu` do manifesto = stale
- `rustc --test event_loop.rs` → 3 testes verdes, 0 warnings
- [[aprendizados/2026-09-13_snn-conectoma-hefesto-absorb]]

## 2026-09-14 — HMI SNN viva (motor índice + 4 regiões ligadas ao live_loop)
- Índice motor: `wiki/concepts/snn/snn-motor-indice.md` (mapa módulo→região → live_loop)
- 4 regiões com seção 'Estado vivo': índice/topologia + MB/KC + CX/navegação + PPL101/valência

## [2026-09-16] ingest | Memory Caching: RNNs with Growing Memory (arxiv-2602.24281)
- Paper Google Research real e verificado (Behrouz et al., fev/2026, ICML 2026): segmentos + checkpoints de hidden state + agregação, O(N·L)
- [[summaries/memory-caching-rnns-growing-memory]] + [[concepts/memory-caching-externo]] (mapa MC↔harness + ruptura honesta + esboço Experimento B)
- Correlação vault: padrão aplica como engenharia (notas atômicas/MOCs/RAG), não como arquitetura diferenciável

## [2026-09-16] ingest | Pérolas YT destiladas + mapa 4-selfs (fila biblioteca-canais)
- [[summaries/yt-GlRHi8SmmQ0-intro-prog-ia]] (Nichonauta, L-e/S-ca) — dual ferramentas×engenharia
- [[summaries/yt-DRcknO84EZk-qwen-claudecode-local]] (L-e/S-ca) — VLM llama.cpp + Claude Code; receita = a do nosso fotógrafo
- [[concepts/4-selfs-biblioteca-canais]] — agregador canônico dos 4 eixos × canais
- Guardrail novo: linter de vault (skills/bibliotecario/tooling/vault_lint.py) — ingestão só vale se script verde

## [2026-09-17] ingest | Spec vídeo P2 — transcrições + veredito honesto (fila biblioteca-canais)
- [[../textos, pdf e esquemas/0LtdXQ_deUA-transcricao-PT]] (Astra 6 = agente cloud, 218 cues) — IRRELEVANTE p/ diffusion local
- [[../textos, pdf e esquemas/YD0LbCaLOv4-transcricao-PT]] (NoConvert v3.0.5, 231 cues) — conversor de formato, não gerador
- YX90I23Ys1Y (Director Studio OSS): sem legendas (yt-dlp: "has no subtitles") — spec via descrição (MiniMax H3 cloud + Qwen3.8-27B diretor + ComfyUI API)
- [[../marca/spec-video-p2-2026-09-17]] — veredito: vault SEM rival ao LTX-2B; ranking + gaps (UltraSharp/COMFY-OFF/RIFE)
## [2026-09-20] ingest | hefesto-fastvideo (hao-ai-lab/FastVideo) -> skills video-local + porta-modelo + swap-guard
## [2026-09-20] ingest | hefesto-h3mix (doc gerador-prompts-H3 + Ilpwa9vqZ7s) -> skill prompt-h3 + runbook H3 no video-local
