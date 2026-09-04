# Especificação Técnica de Parâmetros: llama.cpp

## [CATEGORY] model_lifecycle
> Gerenciamento e provisionamento de arquivos de pesos GGUF.

- **--model**
  - flag: `-m`
  - type: `string`
  - default: `null`
  - desc: Caminho absoluto para o arquivo de modelo local .gguf.

- **--hf-repo**
  - flag: `-hf`
  - type: `string`
  - default: `null`
  - desc: Repositório Hugging Face para download dinâmico (ex: user/model-gguf).

- **--lazy-mode**
  - flag: `-lzm`
  - type: `boolean`
  - default: `false`
  - desc: Ativa o carregamento tardio de tensores na memória RAM.

## [CATEGORY] hardware_allocation
> Parâmetros computacionais calculados dinamicamente com base no ambiente do host.

- **--threads**
  - flag: `-t`
  - type: `integer`
  - default: `auto`
  - desc: Número de threads de CPU alocadas para processamento de geração.

- **--n-gpu-layers**
  - flag: `-ngl`
  - type: `integer`
  - default: `0`
  - desc: Quantidade de camadas do modelo enviadas diretamente para a VRAM da GPU.

- **--flash-attn**
  - flag: `-fa`
  - type: `boolean`
  - default: `true`
  - desc: Habilita o Flash Attention para otimização extrema de memória de contexto.

## [CATEGORY] context_management
> Dimensionamento do buffer e comportamento de ingestão de tokens.

- **--ctx-size**
  - flag: `-c`
  - type: `integer`
  - default: `0`
  - desc: Tamanho da janela de contexto. O valor `0` força o uso do limite nativo do modelo.

- **--batch-size**
  - flag: `-b`
  - type: `integer`
  - default: `2048`
  - desc: Tamanho do lote lógico de tokens processados de uma única vez no prompt.

- **--n-predict**
  - flag: `-n`
  - type: `integer`
  - default: `-1`
  - desc: Limite de tokens a serem gerados. O valor `-1` significa geração contínua.

## [CATEGORY] sampling_profiles
> Ajustes estocásticos para controle de determinismo, criatividade e fidelidade estrutural.

- **--temp**
  - flag: `null`
  - type: `float`
  - default: `0.8`
  - desc: Temperatura de amostragem. `0.0` ativa o modo estritamente determinístico.

- **--min-p**
  - flag: `null`
  - type: `float`
  - default: `0.05`
  - desc: Filtro de probabilidade mínima truncada relativo ao token principal.

- **--grammar**
  - flag: `null`
  - type: `string`
  - default: `null`
  - desc: Regras GBNF inline ou caminho de arquivo para garantir formatação estrita.
