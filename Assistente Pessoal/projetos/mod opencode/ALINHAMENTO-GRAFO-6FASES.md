# MANIFESTO DE ALINHAMENTO — Inventário LLM × Grafo de 6 Fases
> Harness Híbrido · 2026-08-26 · hardware: Xeon E5-2699v3 · X99-D8 · 32GB DDR4-2400 · MI50 16GB (spoof Pro VII) · SSD 128GB slave
> Path canônico: `/mnt/dados/Assistente Pessoal/modelos LLM/` (13 GGUFs) + Ollama (:11434)
> Nuvem = reforço para hard-coding sob demanda (R10/R20); local é a base.

## Mapeamento por fase (modelo primário → refutador → nuvem se necessário)

| Fase | Papel | Local (primário) | Refutador (loop A2A) | Escala p/ nuvem quando |
|---|---|---|---|---|
| **F0 USUÁRIO** | prompt/contexto/harness | — (humano) | — | — |
| **F1 DESCOBERTA** G1 | brainstorm/escopo/desambiguação | **Qwen3.8-27B-IQ1_S** (maior janela criativa) | Bonsai-8B (ternary rápido) | contexto > janela local |
| **F2 CONTRATO** G2 | design doc + spec.md + auditoria | **Ornith-1.5-9B** (orquestrador modular) | LLMJudge-Qwen2.5-3B (julgamento estrito) | spec jurídico-crítico |
| **F3 PLANO** G3 💾SHA | TDD plan + tasks bite-sized + decomposição registro | **Ornith-1.5-9B** | Qwen3.8-9B | plano >50 tasks |
| **F4 EXECUÇÃO** ⚡sem gates | implementação + commits atômicos | **Qwen3.8-9B** (executor F4) ↔ **qwen2.5-coder:7b** (Ollama, código puro) | par por task: gerador=Bonsai-4B / refutador=Qwen3.8-4B | hard-coding complexo (algoritmos difíceis, concorrência, perf) |
| **F5 REVISÃO MACRO** | diff holístico + acoplamento + arquitetura | **Ornith-1.5-9B** (visão de conjunto) | Qwen3.8-27B-IQ1_S (contra-peso pesado) | diff >2k linhas |
| **F6 ENTREGA** G4 | evidência de ferro + veredito final | **LLMJudge-Qwen2.5-3B** (juiz dedicado, temp baixa) | Ornith-1.5-9B | compliance externo |

## Papéis transversais (todas as fases)

| Papel | Modelo | Justificativa |
|---|---|---|
| **Visão/multimodal** | Qwen3.5-0.8B (Ollama, mmproj gerenciado) | R31/R35 — screenshots, UI, diagramas |
| **Refutação alta-velocidade (R42)** | LFM2.5-230M → Bonsai-1.7B → Qwen3-1.7B (escalada) | loops acerto-e-erro em segundos |
| **Tool calling nível 1.5** | Qwen3.8-2B | MCP/tool calls estritos baratos |
| **Embeddings/recall** | nomic-embed-text (Ollama) | memória semântica do vault |
| **Self-improvement** | todo o grafo alimenta `decision-log` + `dev-loop-metrics.jsonl` | R44/R48/R49 |

## Regras de operação híbrida

1. **Local-first**: nuvem só entra quando (a) tarefa excede capacidade do executor da fase, ou (b) janela estourar (R20). Registrar redflag.
2. **Slots CPU** (RS7, KB/tok medido): 9084 qwen0.8B · 9086 lfm230M 🏆 · 9088 qwen3.8-4B · 9089 qwen3.8-2B · 9085 judge3B · 9090 ternary8B · 9083 qwen3.5-4B-iq2 · 9087 qwen3.8-9B — MI50 reserva ornith.
3. **Re-align automático**: qualquer GGUF adicionado/removido do path → re-rodar este mapeamento (R47). Ferramenta: varredura `ls -lhS` + Ollama list + atualização deste arquivo + commit.
4. **Modularidade total**: nenhum modelo é dono de fase — o orquestrador (ornith hoje) reatribui papéis conforme inventário e métricas (`record_decision`).

## Pendências conhecidas (herdadas da auditoria)

- App migration (manifesto de 51 mapas pronto) · temas fonte-única (decisão drift) · i18n unificação · aposentadoria V1 — ver RELATORIO-FINAL §6+§MIX
