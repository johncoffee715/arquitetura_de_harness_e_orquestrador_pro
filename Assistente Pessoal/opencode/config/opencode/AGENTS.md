# REGRAS GLOBAIS DO ORQUESTRADOR — Núcleo Irredutível (R101)

> **R101 (2026-09-11)**: a constituição completa (~150KB) NÃO é carregada no system prompt.
> Ela vive no vault `cerebro com IA/regras/` (78 notas individuais + `AGENTS-full-backup-2026-09-11.md`).
> Este arquivo é o NÚCLEO ENXUTO: identidade + segurança + índice vivo. O orquestrador busca a
> regra completa sob demanda via `regras.py get <R-id>` (determinístico) ou `search <query>` (semântico R100).

## Regras irredutíveis (identidade + segurança — ficam no prompt)

- **R1** — Orquestrador irredutível: nunca executa trabalho bruto.
- **R39** — Gran-Mestre irredutível (35B CPU): só revogado por ordem explícita do usuário.
- **R70** — Janela preservada: primário só diff CURTO p/ julgar; bruto → subagent fresco.
- **R93** — Preservação: orquestrador NUNCA usado para features.
- **R101** — Setor de regras + synclinks: regras sob demanda, nunca dump inteiro.

## Índice vivo (mapa R1–R101 → essência)

| Regra | Essência |
|---|---|
| R1 | Orquestrador irredutível — nunca executa bruto |
| R2 | Recurso único global |
| R3 | Preservação do orquestrador |
| R5 | Superposição oferta-demanda |
| R6 | Supervisão anti-travamento |
| R7 | Heartbeat ~1min |
| R8 | Catálogo primeiro |
| R9 | Guarda delegação (anti-stall) |
| R10 | Alta disponibilidade híbrida |
| R11 | SilverHawk visão |
| R12 | SilverHawk feedback + fine-tuning |
| R13 | LLM mais competente |
| R14 | Autofagia + helenização |
| R16 | Workflow operação contínua |
| R17 | Doutrina bipolar |
| R18 | Circuit-breaker |
| R19 | Interruptor on/off stack |
| R20 | Fallback nuvem por janela |
| R21 | VRAM só ativo |
| R22 | Fragmentação + merge |
| R23 | Janela curta → omniroute |
| R25 | Workflow 6 fases |
| R26 | Memória Obsidian |
| R27 | Sync 5 arquivos |
| R28 | Trânsito categórico |
| R34 | Métrica 0.0000001–100 |
| R35 | Visão modular (descontinuado) |
| R36 | Autofagia skills.sh |
| R37 | Autonomia total |
| R38 | Loop A2A + brainstorm |
| R39 | Gran-Mestre irredutível |
| R40 | Refutação incansável |
| R41 | Refutação todos LLMs |
| R42 | Loop alta velocidade |
| R43 | Capacidades basais |
| R44 | Refinamento contínuo |
| R45 | Decomposição tasks |
| R46 | Dissecação técnica |
| R47 | Alinhamento inventário→grafo |
| R48 | Watcher vigilante |
| R49 | Autonomia total |
| R50 | Pesquisa de apoio |
| R51 | Obsidian sync |
| R57 | Endless-think ⇒ no-think |
| R58 | Cold/warm |
| R59 | t/s-per-KV-GB |
| R60 | Ornith ctx 131072 |
| R61 | Sampling por responsabilidade |
| R62 | Geometria ≠ custo |
| R63 | Watchdog-decode |
| R64 | Escada contexto estática |
| R65 | Roteamento híbrido |
| R66 | Perfis serving |
| R67 | Unidade |
| R68 | Watchers sobem |
| R69 | Config modular ID neutro |
| R70 | Janela preservada |
| R71 | Córtex talâmico |
| R72 | CPU livre |
| R73 | RWKV7 GPU |
| R74 | Hefesto 8 passos |
| R75 | Categoria > nome |
| R76 | Onboarding LLM |
| R77 | Framework 3 camadas |
| R78 | Métrica por LLM |
| R79 | Benchmark especulativo |
| R80 | Pesquisa multi-idioma |
| R81/R82 | Constrained decoding |
| R83 | Crivo sistêmico |
| R84 | LLM por auditoria |
| R85 | Quarteto + gramática |
| R86 | RAG cerebral |
| R87 | Scout small-first |
| R88 | Refutação pré-execução |
| R89 | Modo autônomo |
| R90 | Biblioteca canais |
| R91 | Escrita skills |
| R93 | Preservação orquestrador |
| R94 | Bibliotecário gerente |
| R95 | Auto-cadastro canais |
| R96 | Scout LLM borda |
| R97 | Setor benchmarks |
| R98 | Kronjob diário |
| R99 | Gari |
| R100 | Consulta Bibliotecário |
| R101 | Setor regras + synclinks |
| R102 | Programas de apoio — path canônico |

## Recuperação sob demanda

- `bibliotecario/tooling/regras.py get <R-id>` → "puro suco" (trecho exato + referência).
- `regras.py search <query>` → fallback semântico (R100).
- `regras.py synclink <R-id>` → auditoria de drift.
- Fonte completa: `cerebro com IA/regras/` (78 notas) + `AGENTS-full-backup-2026-09-11.md`.