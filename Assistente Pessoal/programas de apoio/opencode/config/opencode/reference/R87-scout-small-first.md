> [ARQUIVO FRI extraido de AGENTS.md em 2026-09-10 — regra R87 integral aqui. AGENTS.md carrega apenas o stub de 3 linhas.]

# ═══ REGRA GLOBAL R87 — SCOUT COMUNITÁRIO + DOUTRINA SMALL-FIRST ("FAZER + POR -") — promulgado 2026-09-05 ═══

**Regra**: o orquestrador PODE e DEVE averiguar e estudar LLMs **oficiais e não-oficiais da
comunidade** (HuggingFace, GGUFs comunitários — unsloth, bartowski, quants independentes, MoEs
modificadas, destilações) para **composição e upgrade contínuo da stack local**, otimizando
sempre o saldo de hardware — com viés estrutural por **LLMs pequenos, de sub-0,1M em diante
(estado da arte em LLMs pequenos)**. Gênio faz + por -: enxame proporcional de especialistas
pequenos derruba o que generalista gordo não derruba (FILOSOFIA DE ENXAME).

<Vetor de seleção (tudo medido, nada nominal — R84/R45)>
- Todo candidato (oficial OU comunitário) é ranqueado por: **ctx honesto** (nativo; YaRN =
  risco declarado) · **custo de pesos** (GB em disco/VRAM) · **kB/1k** (KV por mil tokens —
  a métrica que decide se o ctx cabe) · **t/s CPU e GPU** (timings do servidor, single e multi).
- Não-oficial NÃO é desqualificação: entra em `fitragem/` (quarentena) e só sai de lá por
  crivo R83 + auditoria R84 + veredito do Conselho R75 — o mesmo portão dos oficiais.
- Benchmark externo de modelo comunitário (likes/downloads/posts/vídeos — R80) é APOIO;
  empírico local prevalece (R45). Divergência >20% = investigação, não canonização.

<Demandas de ctx por agente (o ctx escolhe o modelo, nunca o contrário)>
| Agente | Demanda ctx | Por quê | Ocupante/exemplo |
|---|---|---|---|
| ingestor | ≥1M | logs massivos sem perda, O(1) | RWKV7-0.4B (1048576) |
| orquestrador | 262144 | síntese macro + histórico A2A | Qwen3.6-35B |
| proposer | 131072+ | contrato/plano inteiro na janela | Llama-1B (131072) |
| executor | 132K+ ideal | código + diff + testes sem truncar | coder-3B (32768 ⚠️ abaixo do ideal — suplente mapeado) |
| reflexo | 128000 | loops R42 c/ GBNF | LFM-1.2B |
| juiz | 8192 | veredito curto e categórico | VAGO (só :8083 dispensa) |
| micro | 4096 | classificação/extração pontual | SmolLM2-360M |

<Escada small-first (preencher de baixo para cima)>
- **sub-0,1M**: micro-classificadores, regex-GBNF, FSM determinística — antes de gastar 1 token de LLM, pergunta se regra resolve.
- **0,1–0,5B**: SmolLM2-360M, RWKV7-0.4B — filtro talâmico, ingestão, micro-tarefas (o grueso do volume).
- **0,5–4B**: 0.8B, 1B–3B, Gemma/Phi/coder — papéis com vocação (proposer, refuter, relay).
- **7B–14B**: síntese e crítica pesada (futuro; hoje o :8083 acumula).
- **30B+**: orquestração/suprema corte (um só — recurso único R2).
- Só escala de tier quando o crivo PROVA que o tier atual não passa no disjuntor do nó (R84) — nunca por "modelo maior parece melhor".

<Exemplar canônico — RWKV7-0.4B (imbatível no custo-benefício)>
- 0,91GB · ctx 1M · kB/1k ~0 (state fixo, não escala) · 86,8 t/s GPU / 14–20 CPU.
- Há modelos melhores que ele em cada requisito isolado (t/s, raciocínio, janela) — e nenhum
  melhor nele em **tudo ao mesmo tempo por 0,9GB**. É a prova viva do +por-: peneira grossa
  insubstituível até prova em contrário (R78).

<Estratégia de substituição por alavancagem CPU/GPU (intermediários e primário)>
- **Intermediários primeiro**: 0,5–4B cabem inteiros na VRAM — proposer/refuter/relay migram
  CPU→GPU quando o disjuntor de t/s do nó exigir (F4 ≥100, R65) E a guarda pós-mudança ficar
  ≥1GB. Caminho inverso (GPU→CPU) quando a VRAM apertar, por prioridade: orquestrador >
  ingestor > resto. Pequeno no CPU continua rápido (0.8B: 27,7; Smol: 48,4) — downgrade
  de device raramente mata o papel.
- **Primário (35B)**: sempre híbrido com curva ngl×t/s medida + batch junto (protocolo 05/09:
  pontos 20→40; ótimo = joelho antes da guarda <1GB — canônico: ngl36). Full-GPU só se
  couber com ctx operacional + casa mínima; CPU puro só se a GPU evaporar.
- **Rito de troca**: manifesto + `--apply` + restart só do slot + smoke + memorial (R27/R84).
  NUNCA dois moves simultâneos (isola a causa se degradar).
- **Reserva fria**: destronado vai para `fitragem/` até o sucessor estabilizar — lixeira só
  após veredito de descontinuidade (canônico 05/09: Phi).

<Otimização estrita via quarteto (prefill · decode · batch · KV · quant)>
- **.md** — declara por papel a métrica-rainha (decode p/ executor interativo; prefill p/
  orquestrador de janela longa; latência p/ micro) + sampling oficial R61.
- **.json** — firewall declara as flags ótimas do slot (batch/ubatch, KV, quant, ngl, FA):
  todas crivadas, nenhuma default silencioso (R66/R76).
- **.py** — harness de sweep: mede prefill+decode+VRAM por config, compara, canoniza o
  vencedor, grava memorial. Ordem: batch+ngl (estrutura) → KV/quant (precisão, ΔPPL) →
  FA/MTP (motor). Lei do colapso: batch maior degrada em bandwidth-bound (R76, 05/09: b8192).
- **.gbnf** — economia de decode (output contido no schema = menos tokens; max_tokens do
  schema = trava física) + economia de prefill (`cache_prompt` em prefixo repetido).

<Afinidade de threads — CPU pinning (parametrizar, nunca impor)>
- Afinidade vive no manifesto (`fisica_inferencia.threads/pin`); default = scheduler do SO (R72).
- Pin (`taskset`/`numactl`/cpuset) SOMENTE quando crivo provar contenção (decode cai sob
  carga paralela e recupera com isolamento).
- Neste hardware (Xeon 18C/36T single-socket, sem NUMA inter-socket): pinning isola vizinhos
  ruidosos, não cria banda nova — ganho esperado pequeno; medir antes (R62).
- Pin diz ONDE, nunca QUANTOS a menos: `-t` fixo arbitrário continua proibido (R72).

<Enforcement>
- Scout contínuo (R80 multi-idioma, todas as línguas, MoEs comunitárias com evidência) →
  quarentena `fitragem/` → R79/R83 → auditoria R84 → sync R27 → memorial.
- Métricas de todo candidato (kB/1k, t/s CPU/GPU, ctx honesto) entram na tabela de saldo;
  descoberta fresca sincroniza nos 5 pontos (R78-sync). Sem linha na tabela = sem existência operacional.

---

