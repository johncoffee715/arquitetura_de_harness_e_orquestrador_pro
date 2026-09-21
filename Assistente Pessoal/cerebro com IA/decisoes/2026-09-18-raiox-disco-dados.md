---
tipo: decisao
data: 2026-09-18
status: pendente-humano
tags: [disco, housekeeping, llm-filtragem, R99]
---

# 2026-09-18 — Raio-X /mnt/dados (9,2G livres — DECISÃO DE DELEÇÃO PENDENTE)

## Estado (evidência da sessão R99)

| Métrica | Valor |
|---|---|
| Partição | /dev/sdb 120G (NTFS) |
| Usado | 108G (**93%**) |
| Livre | **9,2G** |

## Vilões (123G de 136G em 3 pontos)

| Peso | Caminho | Detalhe |
|---|---|---|
| 67G | `modelos LLM/` | 33G raiz + **33G `filtragem/`** (nada canonizado usa filtragem) |
| 38G | `programas de apoio/fotografo/` | inclui 11G GGUF visão em `fitragem/` |
| 17G | `programas de apoio/ConfyUI/` | |

## Top arquivos (GGUF)

| Tamanho | Arquivo |
|---|---|
| 13G | filtragem/Qwen3.5-35B-A3B-APEX-Mini.gguf |
| 13G | Qwen3.5-35B-A3B-UD-IQ3_XXS.gguf (raiz) |
| 10G | filtragem/Qwen3.5-35B-A3B-UD-IQ2_XXS.gguf |
| 9,6G | Ornith-1.5-35B-A3B-IQ2_XXS.gguf |
| 9,3G | filtragem/gemma-4-26B-A4B-it-UD-IQ2_XXS.gguf |

## Redundância-chave

Três GGUF da família Qwen3.5-35B-A3B (~36G somados): APEX-Mini 13G (filtragem) + IQ3_XXS 13G (raiz) + IQ2_XXS 10G (filtragem). R104 (piso de quantização) tende a reprovar os ultra-baixos — candidatos primários a deleção.

## Opções apresentadas ao usuário (escolha abortada — ficou PENDENTE)

1. **(~23G)** Apagar os 2 Qwen-35B redundantes de `filtragem/` (IQ2_XXS + IQ3_XXS), manter APEX-Mini.
2. **(~33G)** Limpar `modelos LLM/filtragem/` inteira.
3. **(~11G)** Apagar `fotografo/fitragem/` (qwen2vl-7b 4,4G + minicpmv26 4,4G + gemma3-4b 2,4G).

Descartados: lixeiras vazias, /var/log ~50M, caches vivem no `/` (178G livres).

## Próximo passo

Usuário escolhe os alvos → executor apaga (irreversível = gate humano obrigatório). Modelos são re-baixáveis da HuggingFace.
