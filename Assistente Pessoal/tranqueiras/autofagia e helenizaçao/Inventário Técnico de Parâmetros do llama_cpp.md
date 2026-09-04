# Inventário Técnico de Parâmetros: llama.cpp
> **Status:** Referência de Engenharia para Integração de Features  
> **Escopo:** Mapeamento de Flags (`llama-cli` / `llama-server`) para otimização de infraestrutura, hardware e comportamento de inferência.

---

## 1. Gerenciamento de Modelos e Ciclo de Vida
Flags responsáveis pelo provisionamento, carregamento e alocação inicial dos pesos no ecossistema.

| Flag | Parâmetro Longo | Tipo de Dado | Descrição Funcional | Impacto no Ecossistema |
| :--- | :--- | :--- | :--- | :--- |
| `-m` | `--model` | `string` | Caminho local para o arquivo `.gguf`. | Ponto de entrada obrigatório para inicialização de instâncias locais. |
| `-hf` | `--hf-repo` | `string` | Identificador do repositório Hugging Face (`usuario/repo-GGUF`). | Automatiza o pipeline de deployment baixando modelos dinamicamente. |
| `-mu` | `--model-url` | `string` | URL direta para download do modelo. | Permite provisionamento via CDNs ou storages privados (S3/Azure). |
| `-lzm` | `--lazy-mode` | `boolean` | Ativa o carregamento tardio de tensores na memória. | Reduz o tempo de boot (*Cold Start*) em microserviços e funções serverless. |

---

## 2. Dimensionamento de Contexto e Pipeline de Entrada (Batching)
Configurações que ditam os limites de memória e a arquitetura de processamento de tokens.

| Flag | Parâmetro Longo | Tipo de Dado | Descrição Funcional | Impacto no Ecossistema |
| :--- | :--- | :--- | :--- | :--- |
| `-c` | `--ctx-size` | `integer` | Tamanho total da janela de contexto (Padrão: `0` = nativo do modelo). | Controla o consumo base de memória e o limite de retenção de histórico. |
| `-n` | `--n-predict` | `integer` | Quantidade máxima de tokens a gerar na resposta (`-1` = infinito). | Evita loops infinitos e gerencia o custo computacional por requisição. |
| `-b` | `--batch-size` | `integer` | Tamanho do lote lógico para processamento do prompt (Padrão: `2048`). | Impacta a velocidade de ingestão inicial (*Time to First Token* - TTFT). |
| `-ub` | `--ubatch-size` | `integer` | Tamanho físico do micro-lote de processamento (Padrão: `512`). | Otimiza o pipeline de execução evitando picos de alocação de memória temporária. |
| `---` | `--keep` | `integer` | Número de tokens do prompt original a reter em caso de estouro. | Mantém o contexto de instruções do sistema (*System Prompts*) em chats longos. |

---

## 3. Alocação de Recursos Computacionais (CPU)
Parâmetros de baixo nível para otimização do agendamento de processos e paralelismo em CPU.

| Flag | Parâmetro Longo | Tipo de Dado | Descrição Funcional | Impacto no Ecossistema |
| :--- | :--- | :--- | :--- | :--- |
| `-t` | `--threads` | `integer` | Número de threads lógicas para a etapa de geração de texto. | Deve ser alinhado com os núcleos físicos da CPU para evitar degradação por overhead. |
| `-tb` | `--threads-batch`| `integer` | Número de threads para processamento inicial do prompt. | Acelera a fase de processamento paralelo em lote do input inicial. |
| `-C` | `--cpu-mask` | `hex` | Máscara de afinidade de CPU em formato hexadecimal. | Isola processos do modelo em núcleos dedicados, evitando concorrência com o SO. |
| `---` | `--prio` | `integer` | Nível de prioridade do processo no SO (`-1` a `3`). | Garante SLA de tempo de resposta priorizando a inferência sobre outras tarefas. |

---

## 4. Aceleração de Hardware e Alocação de VRAM (GPU)
Configurações críticas para arquiteturas híbridas e escalabilidade de hardware focado em alta performance.

| Flag | Parâmetro Longo | Tipo de Dado | Descrição Funcional | Impacto no Ecossistema |
| :--- | :--- | :--- | :--- | :--- |
| `-ngl`| `--n-gpu-layers` | `integer` | Número de camadas do modelo enviadas para a GPU (Offloading). | Permite a execução fragmentada (CPU+GPU) ou aceleração total em VRAM. |
| `-fa` | `--flash-attn` | `boolean` | Habilita/desabilita algoritmos de Flash Attention. | Reduz drasticamente a pegada de memória do KV cache e acelera o processamento. |
| `---` | `--fit` | `boolean` | Avalia e aloca automaticamente a carga máxima na VRAM livre. | Automatiza o balanceamento em ambientes com GPUs dinâmicas/compartilhadas. |
| `---` | `--fit-margin` | `integer` | Margem de segurança de VRAM em MiB (Padrão: `1024`). | Previne falhas catastróficas de Out Of Memory (OOM) causadas por flutuações do SO. |
| `---` | `--cache-type-k` | `string` | Define a quantização do cache de chaves (Key) (Ex: `q8_0`, `f16`). | Reduz a memória necessária para manter o contexto em atendimentos simultâneos. |
| `---` | `--cache-type-v` | `string` | Define a quantização do cache de valores (Value) (Ex: `q4_0`, `f16`). | Economiza VRAM em contextos extensos sacrificando o mínimo de precisão. |
| `---` | `--mlock` | `boolean` | Trava o modelo na RAM/VRAM física do host. | Impede o uso de swap em disco, mantendo a latência estável e previsível. |
| `-sm` | `--split-mode` | `string` | Estratégia de divisão multi-GPU (`none`, `layer`, `row`). | Escala a inferência horizontalmente em máquinas com múltiplas placas de vídeo. |

---

## 5. Escalonamento e Extensão de Contexto (RoPE / YaRN)
Ajustes matemáticos para leitura de sequências longas sem necessidade de retreinar o modelo.

| Flag | Parâmetro Longo | Tipo de Dado | Descrição Funcional | Impacto no Ecossistema |
| :--- | :--- | :--- | :--- | :--- |
| `---` | `--rope-scaling` | `string` | Método de expansão de contexto (`none`, `linear`, `yarn`). | Permite habilitar o processamento de documentos gigantescos sob demanda. |
| `---` | `--rope-scale` | `float` | Fator multiplicador de escala aplicado ao contexto. | Modifica a capacidade de interpretação de janelas estendidas (Ex: `2.0` dobra o contexto). |
| `---` | `--rope-freq-base` | `float` | Altera a frequência base do RoPE. | Sintoniza a estabilidade matemática do modelo para manipulação de textos longos. |

---

## 6. Amostragem e Controle de Variabilidade (Sampling)
Parâmetros que regulam o comportamento estocástico do modelo para adequação de personas e precisão lógica.

| Flag | Parâmetro Longo | Tipo de Dado | Descrição Funcional | Impacto no Ecossistema |
| :--- | :--- | :--- | :--- | :--- |
| `---` | `--temp` | `float` | Controla o nível de aleatoriedade/criatividade da saída. | Valores baixos (~`0.1`) focam em respostas exatas (RAG/JSON); altos (~`0.8`) em textos fluidos. |
| `---` | `--top-k` | `integer` | Limita a seleção aos K tokens mais prováveis. | Filtra caudas longas de tokens irrelevantes nas fases iniciais de escolha. |
| `---` | `--top-p` | `float` | Seleção baseada em probabilidade acumulada (Nucleus). | Mantém o dinamismo do texto limitando o vocabulário a termos plausíveis. |
| `---` | `--min-p` | `float` | Filtro dinâmico escalado com base no token principal. | Técnica moderna e robusta para eliminar alucinações sem cortar respostas criativas. |
| `---` | `--repeat-penalty`| `float` | Penaliza tokens que já apareceram recentemente na saída. | Reduz problemas de loop de repetição e redundâncias em respostas prolixas. |
| `---` | `--mirostat` | `integer` | Ativa controle ativo de entropia (`0`=off, `1`, `2`=Mirostat 2.0). | Mantém a qualidade gramatical e de surpresa textual estável ao longo de gerações longas. |

---

## 7. Interfaces de Operação e Sintaxe Estrita
Modos de execução e ferramentas de engenharia de prompt controlada.

| Flag | Parâmetro Longo | Tipo de Dado | Descrição Funcional | Impacto no Ecossistema |
| :--- | :--- | :--- | :--- | :--- |
| `-i` | `--interactive` | `boolean` | Modo chat interativo contínuo via terminal. | Ideal para loops de teste rápido de prompts em ambiente de desenvolvimento local. |
| `-ins`| `--instruct` | `boolean` | Ativa modo de escuta para estruturas de instrução (Alpaca/ChatML).| Garante aderência estrita a blocos de comando em modelos ajustados para tarefas. |
| `-mli`| `--multiline-input`| `boolean` | Permite quebras de linha (`\n`) na entrada do terminal. | Facilita a passagem de códigos e blocos estruturados em fases de depuração manual. |
| `---` | `--grammar` | `string` | Aplica um arquivo de regras sintáticas GBNF. | **Garante 100% de conformidade com schemas estruturados** (Ex: saídas estritamente em JSON). |
