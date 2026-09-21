# GRAFO CANÔNICO — LOOP EXTERNO 0→6 (especificação mestre do usuário, 2026-08-23)

Loop externo que orquestra **plugins · subagentes · hooks · skills · MCPs · tool callings · LSPs**
de forma autônoma, aprendendo sozinho conforme o orquestrador se aperfeiçoa
(self-improvement · auto-ameliorativo · scaffold · self-learning).

---

## [FASE 0 — USUARIO]
Prompt >>> Contexto >>> Harness >>> Loop >>> Grafo engineering
**Habitat do Needle 2 (L0 micro-router CPU):** intercepta entrada antes de acordar a GPU;
extrai metadados/classifica se exige subagentes pesados ou resolução local; confidence score
decide fallback.

## [FASE 1 — DESCOBERTA]  (filtros)
Ideias(filtro) → Definição de Escopo(filtro) → remover ambiguidade(filtro) → decomposição leve
(contexto, não camisa-de-força)(filtro) → loop de refutações no brainstorm de llms/subagents/
vice-subagent(filtro)
⏸️ **GATE 1**: usuário aprova a direção
❌ Needle 2 não entra aqui (zero capacidade cognitiva).

## [FASE 2 — CONTRATO]  (filtros)
Transforma direção aprovada em design doc(filtro) → cria spec.md(filtro) → valida spec contra o
pedido original(filtro) → audita resultado em brainstorm de agents(filtro) → preservar contexto
⏸️ **GATE 2**: usuário aprova o spec
❌ Needle 2 não entra.

## [FASE 3 — PLANO]  (filtros)
TDD, tasks bite-sized, código completo(filtro) → quebrar trabalho em tasks(filtro) → planejar,
orquestrar e implementar decomposição de acordo com o REGISTRO: plugins, subagentes, hooks,
skills, mcps, tool callings, lsps(filtro) → loop de refutações valida cobertura, contratos,
verificabilidade(filtro)
⏸️ **GATE 3**: usuário aprova o plano
💾 **Safety: SHA salvo AQUI** (fases 1-3 não tocam código produtivo)
✅ **Needle 2: mapeador de assinaturas de ferramentas** — valida que assinaturas batem com o
plano; extrai/valida declaração de parâmetros garantindo JSON schemas válidos nas bite-sized tasks.

## [FASE 4 — EXECUÇÃO]  ⚡ sem gates
Supervisiona e sequencia tasks, gerencia git(commits atômicos) → reporta ao Orquestrador →
orquestra subagentes frescos por task + registro completo(filtro operacional) → loop de
refutações TDD por task(filtro) → evidência de verificação por task(filtro) → revisão micro(filtro)
⚡ **HABITAT NATURAL DO NEEDLE 2 (~1500 t/s)**: roteador operacional — traduz intenção em
chamada exata de função/MCP/hook/LSP; parsing de logs e saídas de testes TDD brutos → JSON
estruturado SEM gastar VRAM.
⚠️ Pré-requisito: pré-filtragem cirúrgica dos logs ANTES do binário (janela deslizante 256 tokens):
extrair apenas 📍 Localização (arquivo:linha) · 🛑 Assinatura da exceção · ⚖️ Delta expected-vs-actual.
Máx 5 ferramentas no catálogo ativo por micro-passo.

## [FASE 5 — REVISÃO MACRO]
Revisão holística do diff total — coerência cross-task(filtro macro) → acoplamento → audita
contra critérios de qualidade → loop de refutações arquitetura+contrato(filtro macro)
🛡️ **Needle 2: guardrail de ESTRUTURA apenas** (conformidade de esquema byte-a-byte);
cognição macro fica nos modelos grandes.

## [FASE 6 — ENTREGA]
Verification: evidência fresca de ferro(filtro) → validação final contra pedido original(filtro) →
audita evidência(filtro) → loop de refutações conformidade+qualidade(filtro)
⏸️ **GATE 4**: relatório do orquestrador → **memória cerebral** (Obsidian)
🛡️ **Needle 2: filtro de validação de evidências** — confiança baixa aborta; output imperfeito
no nível de byte nega entrega da micro-task antes de poluir o Obsidian.

---

## MATRIZ DE AGREGAÇÕES NEEDLE 2
| Categoria | Agregação |
|---|---|
| 💾 VRAM | GPU 100% raciocínio; tool-calling/parsing na CPU (28MB RAM) |
| 🛡️ Imunidade A4/A5 | Extração por gramática no byte = 100% schema compliance |
| ⏱️ Latência | Milissegundos; não engasga o loop externo |
| 🛑 Circuit breaker nativo | Confidence baixo intercepta antes de execução errada |
| 📦 Footprint | 14MB disco · 28MB RAM · KV-sink fixo p/ schemas |

## LIMITES DECLARADOS
Zero cognição (F1/2) · janela 256 tokens deslizante · máx 5 ferramentas/catálogo ativo ·
recusa input ambíguo (retorna vazio = alerta limpo ao orquestrador).
