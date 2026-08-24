---
aliases:
  - "arquitetura do meu lab"
tags:
  - datasheet
  - esquematico
  - referencia
source: "/mnt/win2/textos, pdf e esquemas"
file: "arquitetura do meu lab.pdf"
---

# arquitetura do meu lab

![[arquitetura do meu lab.pdf]]

## Informações

- **Arquivo original:** `arquitetura do meu lab.pdf`
- **Tipo:** PDF/Datasheet
- **Caminho:** `textos, pdf e esquemas/Textos/desenvolvimentos/arquitetura do meu lab.pdf`

<!-- OCR_EXTRACT_START -->
## 📝 Texto Extraído (OCR)

> [!info] Método: pdftotext
> Extraído automaticamente pelo OpenCode OCR Pipeline

/mnt/win2/Assistente Pessoal/            ← SLAVE NTFS (sobrevive a qualquer format)
│
├── core/                                ← CÉREBRO DO SISTEMA
│   ├── ai-lab.sh            v7.0        Orquestrador principal (CLI unificada)
│   ├── bootstrap.sh         v6.0        Setup soberano idempotente pós-format
│   ├── supervisor.sh        v2.0        Modo autônomo supervisionado
│   ├── super-run.fish       v2.0        Execução aprovada + auto-debug
│   ├── refactor_prompt.sh v2.0          Deploy do system prompt para modelos
│   ├── update_lab.sh        v4.0        Upgrade pipx + snapshot + rollback
│   ├── config.sh                        Modelos e parâmetros de controle
│   ├── router.sh                        Roteamento de modelo por intenção
│   ├── runner.sh                        Execução LLM com fallback
│   ├── feedback.sh                      Ingest RAG de aprendizado
│   ├── memory.sh                        Recuperação de contexto vetorial
│   ├── executor.sh                      Despachante de ações (safe_mode)
│   ├── bridge.sh                        Ponte para sistema legacy
│   ├── events.sh                        Log de eventos CSV atômico
│   └── scheduler.sh                     Fila de tarefas atômica
│
├── bin/                                 ← BINÁRIOS SOBERANOS (compilados, sem
pacman)
│   ├── qdrant               v1.9.2      Vector DB nativo (sem Docker)
│   └── rg                   v14.1.0     ripgrep (requerido pelo OpenClaude)
│
├── node/                                ← NODE.JS SOBERANO (sem pacman)
│   ├── bin/
│   │     ├── node           v22 LTS     Runtime JavaScript
│   │     ├── npm                        Gerenciador de pacotes
│   │     └── openclaude     v0.9.x      Coding agent → Ollama local
│   └── lib/node_modules/
│         └── @gitlawb/openclaude
│
├── config/                              ← CONFIGURAÇÕES SOBERANAS
│   ├── env_vars.sh                      Fonte única de variáveis (sourced por bash/
fish)
│   ├── qdrant_config.yaml               Config Qdrant (aponta para ext4 local)
│   └── system_prompt_v5.md              System prompt Engineering Mode v5 FINAL
│
├── state/                               ← ESTADO VERSIONADO
│   ├── state.json                       Versões e status dos serviços
│   └── *.pid                            PIDs dos processos ativos
│
├── scripts/                             ← PIPELINES E ADDONS LEGADOS
│   ├── ai-lab               (symlink)   → core/ai-lab.sh
│   ├── ai-lab-c2-addon.sh               Camada C2
│   ├── ai-lab-c3-addon.sh               Camada C3
│   ├── ai-lab-c4-addon.sh               Camada C4
│   ├── ai-lab-c5678-addon.sh            Camadas C5-C8
│   ├── pipeline.sh                       Pipeline principal
│   ├── youtube_sync.sh                   Sync YouTube → Whisper → RAG
│   ├── setup_youtube.sh                  Configuração pipeline YouTube
│   ├── pull-best-models.sh               Download modelos otimizados
│   └── [ingest/ pcb/ scope/ voice/]      Domínios de engenharia
│
├── pkg/                                  ← RECEITAS DE RECONSTRUÇÃO
│   ├── pacman_explicit.txt               Lista de pacotes do master
│   ├── pipx_list.txt                     Pacotes pipx (open-webui)
│   └── requirements_ingest.txt           Dependências Python do venv ingest
│
├── venvs/                                ← RECEITAS (venv real em ext4)
│   └── (requirements apenas)
│
├── data/
│   └── ollama_models/                    Pesos dos modelos LLM
│
├── logs/                                 ← LOGS DE SESSÃO
├── backups/                              ← SNAPSHOTS PRÉ-UPDATE
│   └── core/snapshots/
└── ai-lab/
    ├── prompts/
    │   └── master.prompt                 System prompt injetado em cada query
    └── qdrant/
        ├── ingest.py                     Ingestão RAG
        └── retrieve.py                  Recuperação vetorial


─────────────────────────────────────────────────────────────────
~/.local/share/ai-lab/                    ← MASTER ext4 (EFÊMERO — recriado)
├── qdrant/                               WAL + índices (flock requer ext4/btrfs)
└── venvs/ingest/                         Python .so extensions (NTFS não executa)


/usr/local/bin/ai-lab → slave/core/ai-lab.sh       ← Symlink recriado pelo bootstrap
/usr/local/bin/rg       → slave/bin/rg             ← Symlink recriado pelo bootstrap
/opt/rocm/              ← ROCm stack (master, pacman)
Iniciar stack completa com health checks    ai-lab start

Encerrar todos os serviços                  ai-lab stop

Restart com veriﬁcação                      ai-lab restart

Status visual (serviços + portas + GPU)     ai-lab status

Watch em tempo real (GPU + processos)       ai-lab monitor

Tail de logs por serviço                    ai-lab logs [qdrant|ollama|webui]

Setup soberano idempotente pós-format       ai-lab bootstrap

GPU performance mode MI50 (300W)            ai-lab gpu-tune




Snapshot preventivo (conﬁg + versão)                      ai-lab snapshot

Rollback para última...

<!-- OCR_EXTRACT_END -->