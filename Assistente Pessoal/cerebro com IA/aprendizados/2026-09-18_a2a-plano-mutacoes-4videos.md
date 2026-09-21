---
tipo: plano-mutacoes-a2a
status: parcialmente-aplicado-2026-09-18 (bypass cirúrgico autorizado; A2A/executor pendentes p/ runtime 429)
data: 2026-09-18
aplicado:
  - gran-mestre 9.2.1 (doutrina batedor + cautela NeoHorse)
  - gari 1.0.3 (gate evidência pérolas)
  - cientista 1.0.1 (2 estudos candidatos registrados)
  - jev-eval (seção Serviço Batedor — contrato; impl. PENDENTE runtime)
  - bibliotecario 2.1.0 (proposal-queue HITL — convenção; tooling PENDENTE runtime)
  - spec aprendiz: ideias/2026-09-18-aprendiz-ciclo-aprendizado-ingesta.md (proposta; forja PENDENTE)
pendente_runtime: [forja aprendiz (A2A), impl. batedor jev-eval, tooling proposal-queue]
origem: artefato intermediário gerado pelo GM (fallback de 429 nos roles) — NÃO é a2a completo
fontes:
  - HahjBkz-0eY (Nichonauta, ES) — NeoHorse-1-4B fine-tune
  - LqpRNhAP09U (RepoChad, EN) — Bonsai 27B 1.7bit
  - _bieksxg6oY (Wanderloots, EN) — Agentic Librarian HITL
  - ae92ibehs4Q (Hora de Codar, PT) — Jev decisões tipadas
diretriz_usuario: "LLM não gera txt, não gera codigo, não explica — só devolve decisões tipadas; pode usar LLM barato p/ essa feature"
---

# Plano de mutações — apoio cognitivo 4 vídeos → 6 features

## Sumário executivo

1. **Jev virou tese validada**: LLM-batedor que emite SÓ decisões tipadas (setor ∈ enum, frustração ∈ 1-3, urgência ∈ bool) com **gate de confiança 0.6** — abaixo vira fila de revisão. Nosso `jev-eval` já absorveu o padrão; a otimização é instanciar um batedor com **LLM BARATO** (diretriz do usuário).
2. **Agentic Librarian entrega o gap real do nosso vault**: "o maior perigo da memória de agente não é esquecer — é lembrar algo que nunca foi verdade; uma nota ruim contamina o vault em cadeia". Solução deles: **authority boundary + review proposal** (skill propõe diff, humano aprova, nada escreve direto).
3. **NeoHorse é evidência NEGATIVA útil**: fine-tune de small model com respostas curtas sem CoT NÃO venceu o base no teste agêntico — reforça R103/R104 (crivo antes de canonizar) e cautela no R12 (fine-tuning).
4. **Bonsai 27B** (1.7bit ternário + Hadamard): 98.2% retenção vs IQ2XXS 75.2 — dados para o crivo de quantização; e a lição "quanto menor o peso, mais o gargalo migra p/ KV/atenção" (R62).
5. Padrão transversal: **decisão tipada barata na frente, execução cara atrás** — é a consolidação do córtex talâmico (R71) com schema GBNF fechado (R81/R82).

---

## 1. jev-eval → feature "batedor" (decisões tipadas com LLM barato) [ALTA]

**Evidência** (ae92ibehs4Q): Jev faz "uma única chamada em três perguntas" — setor ∈ {financeiro, técnico, comercial}, frustração ∈ {1,2,3}, urgência ∈ {sim,não}; regra de corte: confiança < 0.6 → linha amarela "revisar manualmente". Nunca gera texto.

**Mutação proposta**:
- Instanciar o roteador jev-eval como **serviço permanente de batedor**: um LLM barato dedicado (candidatos: LFM-1.2B :9086 local 317 t/s — já existe; ou omniroute free-tier R23 como HA) que recebe cada mensagem do usuário e devolve SÓ um objeto GBNF-estrito: `{rota, topicos:[..3], urgente:bool, confianca:float, needs_dense:bool}`.
- `needs_dense=false` → resolve na camada barata/needle; `true` → acorda LLMs densos (F1/F2). Gate 0.6: abaixo disso, marca turno p/ revisão (log + flag), nunca silencia.
- Nenhuma saída de prosa do batedor chega ao usuário — decidido por schema, não por prompt (R81/R82 constrained decoding obrigatório).
- Métricas já existem na skill (completion, efficiency, distractorCalls) — plugar o batedor como arm do eval.

**Esforço**: 1-2 sessões (schema.gbnf já existe na skill; falta o serviço + fio no córtex). 
**Risco de não fazer**: seguimos acordando LLM denso para intenção trivial — desperdício de VRAM/janela (R21, R70) e latência desnecessária.

## 2. bibliotecario → proposal-queue HITL (anti nota-podre) [ALTA]

**Evidência** (_bieksxg6oY): "The biggest danger of giving AI memory is not that it forgets something. It's that it remembers something that was never true... one bad note can cause a chain reaction that taints your vault." Skill deles cria *review proposal* (conteúdo proposto + diff), humano aprova, só então escreve. Raw é preservado intocado.

**Mutação proposta**:
- Novo estado de escrita no bibliotecário: `pending_review/`. Toda ingestão/síntese nova NÃO entra direto no vault — vira arquivo-proposta com frontmatter `{proposta_de: <origem>, diffs, evidencias}`.
- Gate humano (ou GM em modo autônomo com R34 nota ≥ limiar) promove proposal → nota canônica. Raw/original sempre preservado (já alinha com nosso `raw/`).
- Revisitar R94: bibliotecário vira *gerente com fronteira de autoridade* — escreve índice/log livremente, mas conteúdo factual novo passa por proposta.

**Esforço**: 1 sessão (estrutura de dirs + convenção de frontmatter + adaptar tooling/consultar).
**Risco de não fazer**: contaminação silenciosa do vault (hallucinated facts viram "memória" e alimentam decisões futuras — piora com escala).

## 3. gari → sanity-check de pérolas pré-arquivo [MÉDIA]

**Evidência** (_bieksxg6oY, mesma tese): pérolas salvas no fechamento de sessão são exatamente onde entra "memória que nunca foi verdade".

**Mutação proposta**: no fluxo do gari, antes de salvar pérolas empíricas, adicionar gate determinístico: toda afirmação quantitativa/carregável precisa de anexo de evidência (path de arquivo, saída de comando, teste) ou ser marcada `claim_sem_evidencia: true` (visível no relatório). Sem evidência e sem flag → não salva.
**Esforço**: meia sessão. **Risco**: falsos aprendizados consolidados (R34 vira decoração).

## 4. cientista → dois estudos prontos [MÉDIA]

**Evidência**: (a) _bieksxg6oY → estudo observacional: taxa de "nota podre" no vault (amostra de notas antigas × verificação de fato). (b) LqpRNhAP09U → benchmark: Bonsai-style 1.7bit (ternário+Hadamard, 98.2% retenção, 90.9 t/s na 4090) contra nosso crivo A/B R103 — testa a hipótese R104 de piso de quantização com técnica nova; e a tese deles "pesos encolhem → gargalo migra p/ KV/atenção" alinha R62 (geometria ≠ custo) com nossa métrica t/s-por-KV-GB (R59).

**Mutação**: registrar os dois estudos como candidatos na próxima rodada semanal R106 (gate dom 20h). **Esforço**: só registro de hipóteses. **Risco de não fazer**: cientista sem pauta fresca vira ritual vazio.

## 5. gran-mestre → doutrina "batedor barato" + lição NeoHorse [MÉDIA]

**Evidência**: (a) ae92ibehs4Q — separação decisão/execução com modelo dedicado; (b) HahjBkz-0eY — veredito negativo: NeoHorse (FT de respostas curtas sem CoT) "em nenhum ponto foi melhor que o original" no uso agêntico, e sem MTP a GPU esquenta mais (custo oculto de não ter MTP — reforça nossa skill llama-mtp).

**Mutação**:
- Adicionar à doutrina (gran-mestre/SKILL.md seção de roteamento) o princípio: *toda decisão de roteamento/triagem é emitida por LLM barato em schema tipado; LLMs densos só recebem trabalho já triado* — formaliza o que R71 sugere.
- Adicionar cautela explícita: fine-tune/fork de modelo NÃO é promovido por promessa — só após crivo A/B (R103) com evidência fresca (R29). NeoHorse é o contra-exemplo canônico a citar.

**Esforço**: edição cirúrgica de SKILL.md (≤20 linhas). **Risco**: drift ideológico — FTs anunciados como melhoria entram sem prova.

## 6. roteador-hibrido → coerência com o batedor [BAIXA-MÉDIA]

**Evidência**: convergência ótima — RWKV7 L0.5 classifica intenção hoje; o batedor jev-pattern tipifica. **Mutação**: o batedor (decisões tipadas) vira a camada ANTES do roteador-hibrido para entradas de usuário; roteador-hibrido continua para parsing de logs longos (1M). Definir fronteira: texto-usuário → batedor; payload-estrutural → needle; fluxo-longo → RWKV7.
**Esforço**: documento de fronteira (1 diagrama). **Risco**: sobreposição de papéis → decisões duplas contraditórias.

---

## Próximo passo

Quando os roles saírem do 429: executar A2A real (proposer × refuter × juiz) sobre ESTE plano, virar mutações aprovadas em commits. Este arquivo é o insumo.
