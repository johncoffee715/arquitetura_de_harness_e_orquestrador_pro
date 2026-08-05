---
title: "LLMs locais para coding com 16GB VRAM"
source: "https://claude.ai/chat/0506b381-4d13-453f-a5e3-ff02769367a9"
author:
published:
created: 2026-07-17
description: "Claude is Anthropic's AI, built for problem solvers. Tackle complex challenges, analyze data, write code, and think through your hardest work."
tags:
  - "clippings"
---
**You**

As Melhores LLMs para Coding no meu Hardware meu setup com 16 GB de VRAM (HBM2) e 32 GB de RAM, as melhores opções de LLM locais focadas em programação (coding)

---

**Claude**

Dado que teu MI50 tem 16GB HBM2 + 32GB RAM (bom para offload), o fator decisivo aqui não é só "qual modelo é melhor", mas qual **arquitetura** aproveita esse combo. Modelos MoE (Mixture-of-Experts) com poucos parâmetros ativos são a jogada certa: o arquivo todo fica maior que 16GB, mas só uma fração roda por token, e o `llama.cpp` tem uma flag específica (`--n-cpu-moe`) que joga os experts menos usados pra tua RAM enquanto mantém attention/experts "quentes" na GPU. Isso já foi testado e confirmado funcionando bem em **Vulkan/RADV** — inclusive em GPUs AMD mais antigas que a tua — o flag correto é manter -ngl 99 e usar --n-cpu-moe N para empurrar só os tensors de experts pra CPU, mantendo attention/shared weights na GPU. Um detalhe importante pro teu caso: o flag --override-tensor exps=CPU (comum em configs tunadas pra CUDA) na verdade piora performance no Vulkan, com quedas de 9% no Windows e 11% no Linux/RADV — então usa `--n-cpu-moe`, não `--override-tensor`. [GitHub](https://github.com/ggml-org/llama.cpp/discussions/20765) [GitHub](https://github.com/ggml-org/llama.cpp/discussions/20765)

### Comparativo pro teu tier (16GB VRAM)

| Modelo | Arquitetura | VRAM/Quant | Contexto | Tool-calling | Papel sugerido |
| --- | --- | --- | --- | --- | --- |
| **Qwen3-Coder-30B-A3B-Instruct** | MoE (30.5B/3.3B ativo) | ~18,6GB em Q4\_K\_M puro; roda confortável com `--n-cpu-moe` | Nativo 256K, até 1M via YaRN | Excelente (feito pra agentes) | Upgrade do teu CODER |
| **GLM-4.7-Flash** | MoE (30B/~3,6B ativo) | 24GB recomendado oficialmente, mesma lógica de offload se aplica | 200K | Forte | Alternativa a testar lado a lado |
| **Devstral Small 2 (24B)** | Denso | ~13-14GB em Q4 (sem espaço de sobra) | 256K | Muito forte, feito com All Hands/OpenHands | Só se quiser evitar offload |
| **Codestral 22B/25.12** | Denso | ~14GB | Menor, focado em FIM | Fraco pra agentes | Autocomplete no editor, não agente |
| **DeepSeek-R1-0528 (distill)** | Denso reasoning | Mesma classe do teu `deepseek-r1:14b` atual | 128K | Sim (correção do R1 original) | Substituto do teu HEAVY |

#### Por que Qwen3-Coder-30B-A3B é a escolha natural

É essencialmente o sucessor espiritual do teu `qwen2.5-coder:14b` atual — que hoje ocupa 9GB em Q4 com apenas 32K de contexto — só que agora MoE. Foi desenhado especificamente para coding agêntico, uso de browser e tarefas fundamentais de código, com suporte nativo a 256K tokens de contexto, extensível até 1M via Yarn, otimizado para entendimento em nível de repositório. O tool-calling teve bugs no início mas a Unsloth corrigiu o tool-calling do Qwen3-Coder, funcionando de forma transparente em llama.cpp, Ollama, LMStudio, Open WebUI e Jan — relevante porque é exatamente esse o gargalo que teu `deepseek-r1:14b` tem hoje (sem tool-calling, por isso "HEAVY" ficou de fora dos agentes). [Morph + 2](https://www.morphllm.com/best-ollama-models)

Sobre o encaixe em 16GB: em Q4\_K\_M o arquivo fica em torno de 18,6GB, e rodando puro em VRAM (30,5B parâmetros totais) exige cerca de 21,9GB em Q4\_K\_M — ou seja, **não cabe 100% na GPU sozinho**, é aí que entra o `--n-cpu-moe`. Existe até um relato de alguém rodando esse mesmo modelo em apenas 8GB de VRAM usando --cpu-moe (offload total dos experts pra CPU) com cache KV comprimido, atingindo contexto de 262K tokens — com teus 16GB + 32GB de RAM, tu tens bem mais folga que esse cenário limite. [Arsturn + 2](https://www.arsturn.com/blog/running-qwen3-coder-30b-at-full-context-memory-requirements-performance-tips)

**Comando de teste (llama.cpp raw, adaptado pro teu backend Vulkan):**

```bash
./llama-server \
  -hf unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M \
  --jinja -ngl 99 --n-cpu-moe 8 \
  --ctx-size 32768 --device Vulkan0 \
  --temp 0.7 --top-p 0.8 --top-k 20 --repeat-penalty 1.05
```

Ajusta o `8` em `--n-cpu-moe` pra cima/baixo conforme sobrar ou faltar VRAM — quanto menos camadas offloadadas, mais rápido.

#### GLM-4.7-Flash — vale testar em paralelo

Mesma classe (MoE ~3B ativo), mas pontua 59,2% no SWE-bench Verified, 91,6% no AIME 25 e 79,5% no τ²-Bench, e usa cerca de 3,6B parâmetros ativos, suporta 200K de contexto e roda em 24GB de RAM/VRAM/memória unificada oficialmente — mas como também é MoE, o mesmo truque de `--n-cpu-moe` deve funcionar bem no teu setup. Adiciona também **MLA** (multi-head latent attention), que reduz o custo do cache KV — bom pra ti justamente porque VRAM é teu recurso mais apertado. [Lambda](https://lambda.ai/inference-models/zai-org/glm-4.7-flash) [Unsloth AI](https://unsloth.ai/docs/models/glm-4.7-flash)

#### Se preferir evitar offload (denso, cabe 100% na GPU)

**Devstral Small 2 (24B)** é o mais forte em coding agêntico "puro" — leve o suficiente pra rodar numa única RTX 4090 ou Mac com 32GB de RAM — mas é denso, então não tem o benefício do offload seletivo: em Q4 ocupa a VRAM inteira sem sobra pra contexto grande. Funciona, mas é "osso" pro teu card — outras fontes o colocam exatamente na fronteira dos 16GB. **Codestral** é melhor só se tua prioridade for autocomplete rápido no editor (FIM), não agente completo. [Hugging Face](https://huggingface.co/unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF)

#### Corrigindo o gargalo do teu REASONER

Vale conferir se existe uma distill 14B baseada no **DeepSeek-R1-0528**: essa versão adicionou suporte a function calling que o R1 original não tinha, o que resolveria diretamente a limitação que você já documentou (`deepseek-r1:14b`, sem tool-calling). Mesmo tamanho, mesmo footprint de VRAM — só troca de checkpoint. [Fireworks AI](https://fireworks.ai/blog/deepseek-models)

### Observação sobre os benchmarks

Boa parte desses números (SWE-bench, Aider Polyglot) vem de model cards dos próprios laboratórios ou de leaderboards que ainda não fecharam avaliação independente pros lançamentos mais recentes — trata como direção, não verdade absoluta, e testa no teu próprio fluxo (`book-to-skill`, extração verbatim de specs) antes de trocar de vez o modelo padrão.

### Sugestão de próximo passo

Eu testaria primeiro o **Qwen3-Coder-30B-A3B** como upgrade do slot CODER, mantendo o `qwen2.5-coder:14b` como fallback leve (ele já cabe com folga e tem histórico comprovado no teu pipeline). Uma ressalva: como tua infra roda hoje via Ollama (systemd, `OLLAMA_VULKAN=1`), vale confirmar se a versão instalada expõe `--n-cpu-moe` no Modelfile ou se esse controle fino só está disponível chamando `llama-server` diretamente — dado que já compilaste o `llama.cpp` na mão antes, isso não deve ser problema, mas é o tipo de coisa que prefiro confirmar contigo antes de assumir.

Quer que eu monte um script de teste comparando os três (Qwen3-Coder-30B-A3B, GLM-4.7-Flash, teu Qwen2.5-Coder atual) rodando a mesma tarefa de extração de spec table, pra você comparar tokens/s e qualidade lado a lado?