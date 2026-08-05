# 🚀 Gran-Mestre Hybrid Harness

> **Sistema de orquestração híbrido de IA** — local (Radeon Pro VII / Vulkan) + cloud.

## 📦 O que este repositório faz

- Orquestra LLMs locais em GPU via `llama.cpp` + Vulkan.
- Mantém pipelines de Discovery → Contract → Plan → Execution → Review → Delivery.
- Suporta múltiplos backends/modelos GGUF com configuração unificada.
- Registro de sessão, auditoria, métricas e memória persistente em Obsidian.

## 🏗️ Estrutura principal

```
/mnt/dados/
├── harness/                    # Config e núcleo do pipeline
│   ├── harness-config.json     # Contratos, perfis de modelo, thresholds
│   ├── README.md               # Guia local do harness
│   ├── CONTEXT.md              # Estado da sessão atual
│   ├── core/                   # Entrypoints e lógica principal
│   ├── safety/                 # Checkpoints e rollback
│   ├── observability/          # Métricas/tracing
│   └── ...
├── llama.cpp-master/           # Fonte/build do llama.cpp com Vulkan
├── cerebro com IA/             # Obsidian vault (memória/cognição)
├── opencode/                   # Runtime do OpenCode
└── README.md                   # Este arquivo
```

## ⚙️ Requisitos

- GPU: Radeon Pro VII (driver Vulkan / RADV carregado).
- SO: CachyOS/Arch-like (ex.: gcc, clang, cmake, make, git, python3).
- Dependências Vulkan já presentes no build do llama.cpp (glslc, glslangValidator, libvulkan).

> Importante: llama.cpp no repositório é usado estritamente como dependência de inferência local; este README não cobre contribuições upstream do llama.cpp (siga o llama.cpp-master/CONTRIBUTING.md se for alterar o código do motor).

## 🧠 Como o “modo MIX + Dev Loop” funciona aqui

- **Trivial/SIMPLES** → N1 ReAct (correções pontuais, ajustes).
- **MÉDIO** → N2 Mini Loop (refator controlada, validações curtas).
- **COMPLEXO/CRÍTICO** → N3 Human Loop (revisão humana obrigatória).

## 🗺️ Mapa do fluxo principal

1. Discovery
2. Contract
3. Plan
4. Execution
5. Macro Review
6. Delivery

Cada fase pode usar hooks/tools/MCPs/LSPs/subagents/skills específicos conforme risco e complexidade.

## 🔌 Como plugar um novo modelo (passo-a-passo)

1. Coloque o arquivo GGUF em `/mnt/dados/Assistente Pessoal/modelos LLM/` (ou outro diretório de modelos do harness).

2. Registre em `harness/harness-config.json` dentro de `models`:
   - defina `name`, `quantization`, `vram_gb`, `location` e, se local, `local_model_path`.

3. Mapeie gate/fase em `pipeline.phases` e ajuste:
   - `model`, `filters`, `gate`, `dev_loop`, `safety_checkpoint`.

4. Reexecute o pipeline:
   - Discovery → validação de contexto
   - Plan → atualiza checkpoints
   - Execution → inicia serviços/modelos

5. Valide GPU:
   - confira em `CONTEXT.md` se `vram_gb` + alocação bate na VRAM disponível.

## 🚨 Fallback seguro se a inferência cair em CPU/híbrido

Forçar Vulkan ativo só resolve parte do problema se o próprio ponto de entrada cair num binário/serviço que não usa o backend Vulkan. Quando ocorrer CPU alta + GPU idle:

1. Pare qualquer `llama-server`/serviço legado rodando.
2. Garanta que o processo que serve/executa o modelo é o `llama-server` (ou CLI atual) construído com `GGML_VULKAN=ON`.
3. Inicie explicitamente com backend Vulkan (ex.: `llama-server --backend vulkan ...`).
4. Confira `CONTEXT.md`/logs do harness: se VRAM não subir, o modelo não está sendo despachado para a GPU.

## 📝 Convenções do repositório

- Commits pequenos e atômicos.
- Nenhuma operação destrutiva sem antes confirmar/descrever.
- Registros de sessão em `cerebro com IA/` e status em `harness/CONTEXT.md`.
- Para auditoria: use as diretrizes deste `README` como base.
