---
title: "Meu setup atual"
source: "https://chatgpt.com/c/6a063a4e-ea74-83e9-880a-4f79d1d9072c"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 2 messages"
tags:
  - "clippings"
---
**Você disse**

meu setup

---

Vou consolidar o que já aparece no histórico: hardware, sistema, GPU/driver, armazenamento e ecossistema AI-LAB. Onde eu não tiver certeza, vou marcar como “provável”.

Pelo teu histórico, **teu setup atual** está assim:

## Setup principal

| Área | Configuração |
| --- | --- |
| **CPU** | Intel Xeon E5-2699 v3 — 18c/36t, base 2.30 GHz, turbo até ~3.6 GHz |
| **Placa-mãe** | X99-D8 / plataforma X99-C612 provável |
| **RAM** | 32 GB DDR4 |
| **GPU** | AMD Radeon Instinct MI50 / Vega 20 / gfx906 — 16 GB HBM2 |
| **GPU mod** | MI50 com spoof/perfil próximo de Radeon Pro VII |
| **Resfriamento GPU** | Waterblock, sem fan ativo na GPU |
| **Sistema** | CachyOS Linux / Arch-based |
| **Kernel visto** | Linux 7.0.3-1-cachyos |
| **Shell** | Fish |
| **Interface** | KDE Plasma / Wayland |
| **Editor** | Kate |
| **Driver gráfico** | `amdgpu` + Mesa |
| **Stack compute alvo** | ROCm/HIP com `HSA_OVERRIDE_GFX_VERSION=9.0.6` |
| **Armazenamento** | SSD 128 GB + HDDs/partições de 1 TB, incluindo `/mnt/win1` e `/mnt/win2` |
| **Pasta crítica** | `/mnt/win2/Assistente Pessoal/` |
| **Projeto principal** | AI-LAB local, slave-first |

## AI-LAB / IA local

Teu ecossistema está desenhado para rodar assim:

```
/mnt/win2/Assistente Pessoal/
├── core/
├── scripts/
├── config/
├── logs/
├── data/
│   ├── models/
│   └── ollama_models/
├── open-webui/
├── vector-db/
├── rocm-cache/
├── venv-ingest/
└── re-workspace/
```

Serviços previstos/atuais:

| Serviço | Função |
| --- | --- |
| **Ollama** | Runner local de modelos |
| **llama.cpp ROCm** | Inferência primária via GPU, quando funcionando |
| **Open-WebUI** | Interface web |
| **Qdrant** | Banco vetorial/RAG |
| **OpenClaude** | Orquestração/agent |
| **AI-LAB CLI** | Controle plug n play via `ai-lab` |

Modelos citados no teu ambiente:

```
qwen2.5-coder:14b
mistral-nemo
mistral-small:22b
deepseek-coder-v2:lite
deepseek variants
phi3:medium
llama3.1:8b
```

## Situação técnica real

Na lata:

1. **Teu hardware é forte para laboratório local**, principalmente por causa da MI50 16 GB HBM2.
2. **O gargalo não é exatamente força bruta**, é compatibilidade ROCm + gfx906 + CachyOS rolling.
3. **32 GB RAM dá**, mas para RAG pesado, Open-WebUI, Qdrant, Ollama e modelo grande juntos, começa a ficar apertado.
4. **A MI50 é excelente para inferência**, mas exige stack bem travada. ROCm quebrado, `rocm-smi` ausente ou PATH errado derruba tudo para CPU.
5. **Qdrant não deve morar em NTFS**. O projeto pode ficar no slave, mas runtime sensível, banco vetorial, WAL e locks ficam melhor em ext4/btrfs.
6. **Teu padrão ideal é híbrido**:  
	`/mnt/win2/Assistente Pessoal/` como fonte de verdade, e runtime seguro em `~/.local/share/ai-lab`.

## Resumo visionário

Teu setup ideal deve ser tratado como uma **workstation soberana de engenharia reversa + IA local**, não como PC gamer comum.

Arquitetura correta:

```
CachyOS master = sistema descartável
/mnt/win2/Assistente Pessoal = cérebro persistente
MI50 = acelerador bruto
Ollama/llama.cpp = motor de inferência
Qdrant = memória vetorial
Open-WebUI/OpenClaude = interface/orquestração
ai-lab = painel de comando
```

## Ponto crítico atual

Antes de evoluir qualquer coisa, o próximo check deveria ser:

```bash
rocminfo
/opt/rocm/bin/rocm-smi
ollama ps
systemctl status ollama --no-pager
ls -lah "/mnt/win2/Assistente Pessoal/"
```

Se `rocminfo` e `rocm-smi` falharem, tua inferência **vai cair em CPU**, mesmo com a MI50 instalada.