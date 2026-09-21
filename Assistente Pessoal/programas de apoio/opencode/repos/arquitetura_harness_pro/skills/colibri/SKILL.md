---
name: colibri
description: "Motor de inferência MoE puro C, zero deps: roda modelos frontier 744B-2.8T em hardware consumer tratando VRAM/RAM/storage como hierarquia única (multitiering). (absorvido de JustVugg/colibri)"
---
# Colibrì

Helenizado de [`JustVugg/colibri`](https://github.com/JustVugg/colibri) (v1.4.0).

## Propósito
**Tiny engine, immense model.** Motor de inferência puro C, zero dependências, que roda MoE frontier — GLM-5.2 (744B), Inkling (975B), Kimi K3 (2.8T), DeepSeek V4 Flash (284B), OLMoE (7B) — em hardware consumer/heterogêneo tratando **storage, RAM e VRAM como uma única hierarquia de inferência** (AI memory multitiering): experts são transmitidos do disco (streamed from disk).

## Padrões absorvidos (núcleo canônico do repo)
- **Multitiering de memória**: VRAM/RAM/storage como hierarquia única; expert residency por tier (dashboard mostra "full expert residency on 6× RTX 5090, disk 0"); 1 arquivo C por família de modelo.
- **Consumo e residência**: `resident 9.9 GB` mesmo para 744B (int4, streaming CPU); ready em 32s — MoE grande cabe no hardware modesto pela hierarquia.
- **Garantia de semântica, sem SLA de velocidade**: a política default **nunca muda silenciosamente precisão do modelo nem semântica do router**; memória rápida insuficiente reduz velocidade, não redefine o modelo. Experiments só entram com medição e2e reproduzível.
- **Front ends unificados**: `coli chat` / `coli serve` / `coli web` para todas as famílias — mesma UX, engine trocável.
- **Brain/dashboard observável** (19.456 experts como "cortex vivo"): cor = tier de storage, brilho = routing heat, experts usados no turno piscam — observabilidade de roteamento em tempo real.
- **Zero deps**: C puro, Makefile + flake.nix (Nix); reproduzível e portável.

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade de inferência de modelo grande (>100B) em hardware limitado (MI50 16GB): MoE streamed é o caminho, não modelos densos.
2. Carregar skill (`skill(name="colibri")`).
3. Aplicar a mentalidade de hierarquia única: cache em VRAM 1º, RAM 2º, storage 3º; medir residência por tier; nunca sacrificar semântica por velocidade.
4. Observar routing heat (dashboard) antes de otimizar expert placement.

## Fonte
https://github.com/JustVugg/colibri