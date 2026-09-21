---
setor: regras
tipo: indice
fonte: AGENTS.md (constituicao canonica, hardlink 2 vias)
data: 2026-09-11
---

# Índice de Regras (R1–R101)

> Setor APENAS para regras (R101). Fonte única: AGENTS.md. O orquestrador NÃO carrega o dump
> inteiro — consulta o Bibliotecário (tool call ultra-fast) e recebe SÓ o "puro suco" da regra
> relevante. Synclink audita drift entre vault e AGENTS.md.

## Mapa vivo (regra → essência)

| Regra | Essência (1 linha) |
|---|---|
| R1 | Orquestrador irredutível — nunca executa trabalho bruto |
| R2 | Recurso único global |
| R3 | Preservação do orquestrador (anti-gargalo) |
| R5 | Superposição oferta-demanda via scaffold |
| R6 | Supervisão anti-travamento + self-healing |
| R7 | Heartbeat de supervisão ~1min |
| R8 | Catálogo primeiro (anti-reinvenção) |
| R9 | Guarda de delegação global (anti-stall) |
| R10 | Alta disponibilidade híbrida (redflag + recovery) |
| R11 | SilverHawk visão/imagem/vídeo |
| R12 | SilverHawk interpretação + feedback + fine-tuning |
| R13 | LLM mais competente por caso de uso |
| R14 | Autofagia + helenização global permanente |
| R16 | Workflow operação contínua |
| R17 | Doutrina bipolar (orquestrador ↔ executor) |
| R18 | Circuit-breaker global |
| R19 | Interruptor on/off stack local |
| R20 | Fallback nuvem por janela |
| R21 | VRAM só conteúdo ativo |
| R22 | Fragmentação de contexto + merge |
| R23 | Roteamento janela curta → omniroute |
| R25 | Workflow 6 fases via ArsenalScaffold |
| R26 | Memória Obsidian universal |
| R27 | Sync 5 arquivos ao agregar LLM |
| R28 | Critério de trânsito categórico |
| R34 | Métrica universal 0.0000001–100 |
| R35 | Fallback visão modular (descontinuado) |
| R36 | Autofagia + helenização skills.sh |
| R37 | Autonomia total do orquestrador |
| R38 | Loop A2A + brainstorming |
| R39 | Gran-Mestre irredutível (35B CPU) |
| R40 | Refutação incansável até impressão |
| R41 | Refutação a todos LLMs + scaffolding |
| R42 | Loop alta velocidade (acerto-erro) |
| R43 | Capacidades basais (raciocínio retido) |
| R44 | Refinamento contínuo harness + grafo |
| R45 | Decomposição tasks complexas |
| R46 | Dissecação técnica como filtro |
| R47 | Alinhamento inventário→grafo |
| R48 | Watcher vigilante loop diário |
| R49 | Doutrina autonomia total |
| R50 | Guardrail pesquisa de apoio |
| R51 | Obsidian sync bridge |
| R57 | Endless-think ⇒ no-think |
| R58 | Doutrina cold/warm |
| R59 | Métrica t/s-per-KV-GB |
| R60 | DESCONTINUADA 2026-09-18 — ctx efetivo Ornith = 262144 nativo (ver r50/RS4/R66) |
| R61 | Sampling por responsabilidade |
| R62 | Geometria ≠ custo real |
| R63 | Watchdog-decode |
| R64 | Escada contexto estática |
| R65 | Roteamento híbrido em camadas |
| R66 | Perfis serving fixos |
| R67 | Unidade do orquestrador |
| R68 | Watchers sobem com orquestrador |
| R69 | Config modular ID neutro |
| R70 | Preservação janela orquestrador |
| R71 | Kronjob tálamos (córtex sensorial) |
| R72 | CPU livre (36 threads) |
| R73 | RWKV7 GPU com ornith |
| R74 | Modelo implementação features (Hefesto) |
| R75 | Catalogação por categoria + conselho |
| R76 | Onboarding LLM (batch/KV/MTP) |
| R77 | Framework 3 camadas (ontologia/firewall/mecânica) |
| R78 | Métrica avaliativa por LLM |
| R79 | Benchmark especulativo |
| R80 | Pesquisa comunitária multi-idioma |
| R81/R82 | Constrained decoding + estrangulamento |
| R83 | Crivo sistêmico |
| R84 | Escolha LLM por auditoria |
| R85 | Quarteto + tool-call com gramática |
| R86 | RAG cerebral cognitivo |
| R87 | Scout small-first |
| R88 | Refutação pré-execução universal |
| R89 | Modo autônomo |
| R90 | Biblioteca de canais |
| R91 | Exceção escrita skills helenizadas |
| R93 | Preservação orquestrador (nunca features) |
| R94 | Bibliotecário gerente geral vault |
| R95 | Auto-cadastro canais vídeo |
| R96 | Scout LLM minimalista borda |
| R97 | Setor benchmarks (régua própria) |
| R98 | Kronjob diário (leite e mel) |
| R99 | Gari (faxineiro pós-veredito) |
| R100 | Consulta automática ao Bibliotecário |
| R101 | Setor regras + synclinks (prefill otimizado) |
| R107 | Transcrição automática de vídeo lido (guardrail universal) |

## Notas individuais (extração 2026-09-11)

- 78 notas `RXX-<slug>.md` extraídas do AGENTS.md via `bibliotecario/tooling/extract_regras.py`
  (determinístico, re-executável). Duplicatas (R35/R46-R50) com sufixo `-v2`.
- Cada nota: frontmatter (regra/titulo/fonte/linha) + texto integral da regra.

## Synclink

- Tool call: `bibliotecario/tooling/regras.py get <R-id>` → devolve o "puro suco" (trecho exato
  da regra no AGENTS.md + referência).
- Audit: `regras.py synclink <R-id>` → verifica drift (presente no AGENTS.md?).
- `regras.py index` → mapa vivo R-id → linha no AGENTS.md.
- Re-extração: `extract_regras.py` (após qualquer mudança no AGENTS.md).