---
title: "Modelos LLM locais otimizados para 16GB VRAM"
source: "https://claude.ai/chat/44ea9b29-f02e-434c-8585-2af8ce75f61b"
author:
published:
created: 2026-07-21
description: "Claude conversation with 5 messages"
tags:
  - "clippings"
---
**Claude**

Rapidamente sobre as fontes: LM Arena e Copilot Arena são dominados por modelos frontier (Claude, Gemini, GPT) e não têm leaderboard granular pra modelos pequenos self-hosted — pra 16GB, a evidência mais confiável continua sendo SWE-bench + testes reais de agente (tipo o benchmark do OpenCode que te mostrei) + relatos do r/LocalLLaMA. Sendo honesto sobre isso em vez de forçar uma citação de Arena que não existe pra esse recorte.

**Novos candidatos (além de tudo já citado):**

- **Apriel-1.5/1.6-15B-Thinker** (ServiceNow, ~10GB) — pequeno mas eficiente, LiveCodeBench 0.728, MMLU-Pro 77%, multimodal (lê screenshots), ótimo custo-benefício de VRAM
- **Seed-OSS-36B-Instruct** (ByteDance, Q3\_K\_M ~15-17GB) — denso, "thinking budget" ajustável (controla quanto raciocina), contexto 512K, forte em agentes — aperta mas cabe
- **Qwen2.5-Coder-14B** (~9GB Q4) — coder mais antigo mas ainda referência, deixa bastante sobra de VRAM pra contexto longo
- **DeepSeek-Coder-V2-Lite-16B (MoE)** — ativa poucos parâmetros por token, boa opção pra Mi50 (bandwidth-friendly)

---

**Mapeamento dos 43 agents em 4 categorias:**

**1\. Orquestração/Planejamento/Verificação** → `Qwen3.5 27B IQ3_XXS (Unsloth)` (19 agents)  
`superpowers` (orquestrador), `gsd-planner`, `gsd-eval-planner`, `gsd-framework-selector`, `gsd-roadmapper`, `superpowers-plan-writer` (+alt1/alt2), `superpowers-spec-writer`, `gsd-assumptions-analyzer`, `gsd-verifier`, `gsd-plan-checker`, `gsd-eval-auditor`, `gsd-integration-checker`, `gsd-nyquist-auditor`, `gsd-security-auditor`, `gsd-ui-auditor`, `gsd-ui-checker`, `gsd-doc-verifier`

**2\. Execução/Código pesado** → `Qwen3.6-27B` ou `Qwen3-Coder-Next` (8 agents)  
`gsd-executor`, `gsd-code-fixer`, `gsd-code-reviewer`, `gsd-debugger`, `gsd-debug-session-manager`, `reverser`, `superpowers-implementer`, `superpowers-code-reviewer`

**3\. Pesquisa/Síntese/Documentação** → `Gemma 4 26B-A4B (MoE)` (11 agents)  
`gsd-advisor-researcher`, `gsd-ai-researcher`, `gsd-domain-researcher`, `gsd-phase-researcher`, `gsd-project-researcher`, `gsd-research-synthesizer`, `gsd-doc-synthesizer`, `gsd-doc-writer`, `gsd-codebase-mapper`, `gsd-pattern-mapper`, `gsd-ui-researcher`

**4\. Leve/Rápido** → `Qwen2.5-Coder-14B` ou `Apriel-1.6-15B` (5 agents)  
`gsd-doc-classifier`, `gsd-intel-updater`, `gsd-mempalace-curator`, `gsd-user-profiler`, `memory-keeper`

Quer que eu monte o arquivo de config (`opencode.json` ou provider mapping no OmniRoute) já com essa distribuição pronta pra colar?

---

**You**

Uso obsidian, como isso pode me ajudar no meu workflow, e gostaria de saber também sobre Fine tuning de LLM local se seria viável

---

**Claude**

### Obsidian no seu workflow GSD

Faz muito sentido, principalmente porque seu sistema já tem os agents `gsd-mempalace-capture` / `gsd-mempalace-recall` e o plugin `graphify.js` — ambos praticamente pedem por um vault:

- **Memória persistente como vault** — em vez (ou além) de um banco interno, os agents de mempalace podem escrever/ler markdown direto num vault Obsidian via plugin **Local REST API** (expõe um endpoint HTTP local que seus hooks já chamariam como qualquer outra ferramenta). Isso transforma a "memória" do GSD em notas navegáveis com backlinks, em vez de uma caixa-preta.
- **`graphify.js` → Obsidian Canvas** — se esse plugin já gera algum grafo de dependências/decisões, vale exportar direto pro formato `.canvas` do Obsidian em vez de um formato próprio — você ganha visualização e edição manual de graça.
- **Documentação dos agents** (`gsd-doc-writer`, `gsd-doc-synthesizer`, `gsd-roadmapper`) — apontar a saída deles direto pra pastas do vault, com frontmatter YAML padronizado (fase, status, agent que gerou). Com o plugin **Dataview** você consulta isso depois tipo SQL ("todas as specs pendentes da fase X").
- **Relatórios de auditoria** (como esse que você colou) — dá pra ter um hook `Stop` / `SessionEnd` jogando isso direto numa nota diária ou numa pasta `/audits/`, criando histórico buscável ao longo do tempo em vez de log perdido.
- **RAG leve pro agent de categoria "leve/rápido"** — antes de responder, ele consulta o vault (grep/embeddings simples) em vez de alucinar — reduz exatamente o problema que vimos no teste real (Qwen 3 14B inventando URLs de documentação).

### Fine-tuning local na Mi50 — viável, com ressalvas

**Full fine-tuning: não.** Precisa de ~4x o tamanho do modelo em VRAM (pesos + gradientes + estados do otimizador) — mesmo um 7B já estouraria os 16GB.

**LoRA (fp16, sem quantização do modelo base): sim, funciona.** Há relato direto de comunidade rodando LoRA em fp16 numa Mi50 (gfx906) "sem configuração adicional". Na prática isso te dá margem confortável até modelos na faixa de **7-8B** (ex: Qwen3 8B) — o modelo congelado em fp16 já consome boa parte dos 16GB, sobrando espaço justo pra ativações/gradientes do adapter.

**QLoRA (4-bit via bitsandbytes): possível, mas manual.** O bitsandbytes oficial em ROCm tem como alvo arquiteturas mais novas (gfx90a/gfx942 — MI200/MI300), não gfx906. Pra Mi50 é preciso compilar um fork ROCm específico na mão, e relatos de comunidade (fev/2025) descrevem "sucesso parcial" — funciona, mas espere debugar. Se conseguir fazer funcionar, QLoRA abriria margem pra treinar modelos maiores (13-14B) nos mesmos 16GB.

**Recomendação prática:** comece com LoRA fp16 num modelo pequeno (Qwen3 8B ou Qwen2.5-Coder-14B com quantização leve) pra especializar, por exemplo, o agent "leve/rápido" (classificação de docs, perfil de usuário) — é o cenário de menor risco e maior ROI. QLoRA em modelo maior fica como fase 2, depois de validar que o build do bitsandbytes-ROCm está estável na sua gfx906 — há também o risco documentado de segfaults em rocBLAS/rocSPARSE especificamente em Mi50 com ECC desabilitado, vale checar isso antes de investir tempo em QLoRA.

Quer que eu monte um passo a passo de setup do LoRA fp16 (docker ROCm + PEFT + dataset a partir dos seus logs de agent), ou prefere focar primeiro na integração com o Obsidian?

---

**You**

(Qwen3 8B ou Qwen2.5-Coder-14B com quantização leve) pra especializar, por exemplo, o agent "leve/rápido" pra refinanciamento especializada em codificação e viável? Minha ideia é pegar um modelo pequeno que já e bom em codificação e melhora-lo ao máximo com Fine tunning

---

**Claude**

Viável, mas eu ajustaria o ponto de partida. Vamos ao porquê:

**A conta de VRAM não fecha pro Qwen2.5-Coder-14B em LoRA fp16:**

- Modelo congelado em fp16 = ~28GB só de pesos → não cabe nos 16GB de jeito nenhum.
- Pra caber, você precisaria de QLoRA (4-bit) — que é justamente o caminho instável na Mi50 (bitsandbytes-ROCm mira gfx90a/gfx942, gfx906 é "sucesso parcial" via build manual).

**Qwen3 8B cabe fácil, mas não é especialista em código** — é um modelo generalista. Fine-tunar um generalista pra virar "bom em código" do zero é caro em dados e menos eficiente do que partir de um modelo que já foi pré-treinado pesado em código.

**A escolha que resolve os dois problemas: `Qwen2.5-Coder-7B-Instruct`.**

- Já é especialista em codificação (mesma família do 14B, treinado especificamente pra isso).
- Em fp16 são ~14GB de pesos — cabe nos 16GB com LoRA fp16 (o caminho que já confirmamos que funciona sem drama na Mi50), com uma margem apertada mas real pra ativações/gradientes do adapter (use `batch_size=1`, `gradient_checkpointing=True`, contexto curto nas primeiras rodadas).

Essa é a resposta direta pra "pegar um modelo pequeno que já é bom em codificação" — em vez de forçar o 14B por um caminho de treino instável.

**Sobre "melhorar ao máximo":** vale calibrar a expectativa. Um LoRA seu, com dataset pequeno (algumas centenas a poucos milhares de exemplos), não vai empurrar o SWE-bench geral do modelo pra cima de forma notável — quem tem orçamento pra isso são os labs, com milhões de exemplos e clusters inteiros. O ganho real e alcançável nesse formato é **especialização estreita**: o modelo aprende os padrões do seu stack, suas convenções de código, e principalmente a seguir o protocolo de tool-calling do GSD de forma mais consistente — que foi exatamente onde os modelos pequenos falharam nos testes reais (alucinar doc, se confundir com file ops). Isso é mais valioso pro seu caso de uso do que ganhar 2 pontos de SWE-bench genérico.

Aliás, você já tem a infraestrutura pra gerar esse dataset: os hooks `pre:observe:continuous-learning` e `post:observe:continuous-learning` do seu setup já capturam observações de uso de ferramentas — isso é praticamente o dataset de fine-tuning esperando pra ser exportado (pares prompt→tool-call corretos das suas próprias sessões GSD).

Quer que eu monte o pipeline: extrair dataset dos logs de continuous-learning → formatar pro SFTTrainer → LoRA fp16 no Qwen2.5-Coder-7B via ROCm?

**Claude**

Bom sinal — a auditoria já mostra minha correção do SWE-Bench aplicada, e o "46 vs 43" se resolve: 43 GSD + 3 skills + 5 builtins (Gran-Mestre/Prometheus/Héstia/Atlas/Atena) = 51. Consistente.

Agora, o pipeline do Gran-Mestre muda a jogada: em vez de mapear 4 categorias soltas pros 43 agents, o pipeline principal tem **5 papéis fixos chamados em sequência todo request** — isso simplifica bastante o roteamento.

### Mapeamento Gran-Mestre → LLM local

| Papel | Modelo (Q corrigido p/ 16GB) | Por quê |
| --- | --- | --- |
| **Gran-Mestre** (roteador, todo request) | Curto prazo: **Qwen3.5 27B IQ3\_XXS** — confiabilidade de protocolo importa mais que velocidade, já que erro de rota contamina todo o pipeline | Ver nota de fine-tune abaixo — candidato ideal |
| **Prometheus** (planejamento) | **Qwen3.5 27B IQ3\_XXS** | Mesma justificativa da categoria 1 já validada |
| **Héstia** (validação, chamada 2x) | **Qwen3.5 27B IQ3\_XXS** | Mesmo modelo do Prometheus — reaproveitado, sem swap |
| **Atlas** (execução) | **Qwen3-Coder-30B-A3B, Q3\_K\_M/IQ4\_XS (~15GB, quant corrigida)** ou Qwen3.6-27B | SWE-bench real ~50%, MoE eficiente na Mi50 — mas ainda não validado no seu teste de agente real; testar antes de confiar em CRITICAL |
| **Atena** (revisão de código) | Mesmo modelo do Atlas | Evita swap extra — revisão de código usa a mesma capacidade de leitura de código da execução |

**Ganho prático:** isso reduz o caminho crítico a **2 modelos carregados** (não 5), já que Gran-Mestre+Prometheus+Héstia compartilham um, e Atlas+Atena compartilham outro. Resolve o problema de latência de troca que discutimos antes.

Os outros 46 agents (research/docs, leve/rápido) seguem o mapeamento de 4 categorias já fechado: Gemma 4 26B-A4B pra pesquisa/síntese, Qwen2.5-Coder-14B/Phi-4-14B pra leve.

**Sobre o Gran-Mestre em si — reaproveitando sua ideia de fine-tuning:** ele é chamado em *todo* request só pra classificar TRIVIAL→CRITICAL e escolher o agente — é uma tarefa estreita e repetitiva, exatamente o perfil ideal pra fine-tune dedicado (melhor ainda que o alvo de coding que definimos antes). Um Qwen3 8B fine-tunado só nessa decisão, usando os spans do OTel que você já vai ter rodando, seria mais rápido e provavelmente mais confiável que reusar o 27B genérico só pra rotear.

Vou aplicar isso como refatoração no manifesto:

---

**You**

e como o obsidian pode ajudar o gran-mestre, e outro detalhe que quando possivel irei usar o omnirouter e casos especificos como o kimi k3

---

**Claude**

### Obsidian + Gran-Mestre especificamente

O manifesto já tem 3 pontos que são vault esperando pra acontecer:

- **Shared Brain (Cerebral Memory)** — `ingest_source`, `create_summary`, `upsert_entity`, `upsert_concept` hoje são chamadas pra um sistema abstrato. Trocar isso por notas Obsidian com frontmatter (`tipo: entity|concept`, `pipeline_run`, `fase`) transforma essa memória de caixa-preta em algo que você navega e edita — e o grafo do Obsidian passa a *ser* literalmente o mapa de entidades/conceitos acumulados entre pipelines.
- **Relatório Final** — cada execução do pipeline já gera sumário executivo + arquivos modificados + testes + recomendações. Isso é a estrutura perfeita de uma nota datada, linkada ao projeto, com o Dataview te dando "todos os relatórios CRITICAL desta semana" de graça.
- **Safety Protocol / CONTEXT.md** — o SHA salvo antes de cada execução do Atlas e o log de rollback ganham histórico visual se você sincronizar o `CONTEXT.md` pro vault em vez de deixar como arquivo solto — dá pra ver ao longo do tempo quando/por que o Gran-Mestre precisou reverter.

Isso complementa (não substitui) o OTel/Jaeger: Jaeger é pra debugar performance e trace técnico; o vault é pra você e o próprio Gran-Mestre navegarem decisões e aprendizados de forma legível.

### OmniRoute + Kimi K3

Faz todo sentido, e o timing é bom pra citar: **Kimi K3 acabou de sair (16/jul/2026)** — modelo open-weight da Moonshot AI, mas com ~2,8 trilhões de parâmetros (MoE). Isso é **impossível de rodar local** mesmo com quant agressivo — é escala de datacenter, só via API. Então o uso correto dele no seu setup não é como substituto dos modelos da Mi50, é como **escalonamento do Gran-Mestre**: quando uma tarefa é classificada como CRITICAL e o Atlas local (Qwen3-Coder-30B) não dá conta ou o Héstia reprova a validação repetidamente, o Gran-Mestre escala pro OmniRoute → Kimi K3 (ou outro modelo grande do seu grupo `oc` / `tllm`) em vez de insistir no local.

Isso é exatamente o padrão TRIVIAL→CRITICAL que já está no manifesto — só falta formalizar que **CRITICAL pode sair do roteamento local e cair no OmniRoute**. Quer que eu adicione essa regra de escalonamento na seção que já criamos no `GRAN_MESTRE.md`?

---

**You**

sim

---

**Claude**

Adicionei a regra: só escala pra nuvem em CRITICAL, depois de 2 falhas locais seguidas, e sempre registrada no CONTEXT.md — pra Kimi K3 (ou qualquer outro modelo grande via OmniRoute) não virar custo/latência escondido em tarefas que o pipeline local já resolveria.