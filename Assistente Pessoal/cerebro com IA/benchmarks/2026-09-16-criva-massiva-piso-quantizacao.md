---
data: 2026-09-16
hardware: MI50 16GB + Xeon E5-2699v3 (36 threads)
tipo: crivo A/B massivo (R103+R104) — fila de 6 candidatos
rubrica: v1.1
---

# 2026-09-16 — Criva massiva do piso (6 candidatos × A/B × CPU/GPU)

> Experimento R104 completo. Tese sob refutação: "acima de 4B, Q1 é o verdadeiro limite".
> **VEREDITO FINAL: REFUTADA DUAS VEZES** — nem 27B-IQ1_S (1.78bpw) nem 35B-IQ1_M (~1.9bpw)
> absorvem quartetos. E mais: nem sequer IQ2_S 2.17bpw aguenta. **O piso de absorção real
> desta arquitetura mora entre 2.17 e 2.31 bpw.** GSQ-IQ2_XS (2.31bpw) é o piso empírico confirmado.

## Tabela consolidada (placar /7, rubrica v1.1; dec/pre em t/s)

| Modelo | A-CPU | B-CPU | A-GPU | B-GPU | dec/pre CPU | dec/pre GPU | Veredito |
|---|---|---|---|---|---|---|---|
| Qwen3.8-27B-GSQ-IQ2_XS (2.31bpw) | 2.5 | **6.2** | 3.1 | 4.7* | 1.7/0.7 | 3.4/14.7* | piso confirmado — fica filtragem |
| Qwen3.8-27B-UD-IQ1_S (1.78bpw) | 3.4 | 4.5 | — | — | 1.7/0.55* | — | **piso FURADO: absorção colapsa (ΔB=+1.1 vs +3.7 do irmão)** |
| Qwen3.6-35B-UD-IQ1_M | 1.6* | 2.1* | — | — | 6.4/19.1 | — | refutado |
| Qwen3.6-35B-IQ2_S (2.17bpw) | 2.1* | 2.8* | — | — | 7.9/18.2 | — | refutado |
| Qwen3.6-35B-IQ1_M (qwen_) | 2.6* | 1.8* | — | — | 7.2/19.6 | — | refutado |
| Qwen3.5-35B-IQ2_S (2.17bpw) | 2.1* | 1.3* | — | — | 7.7/18.2 | — | refutado |
| Ornith-1.5-9B-AD (híbrido) | 2.1 | 1.8 | 1.4 | 2.6 | 4.9/9.8 | **68.6/88.4** ✔GPU | veloz mas fraco — segue fora |
| 8083 incumbent (IQ3_XXS ~2.9bpw) | 3.5 | **6.2** | — | — | 26.5 idle | — | intocado (R39) |

\* CPU fastio porque GPU híbrida não cabia (VRAM livre pós-pausa 9095 ≈ 5.2GB < necessário); *temp 0.6 = variância ±0.3 entre rodadas.

## Lições sistêmicas empíricas

1. **Dois pisos distintos existem**: piso-cru (modelo funciona) ≠ **piso-absorção** (modelo obedece quartetos). O que importa para o harness é o segundo.
2. **Piso-absorção medido: ~2.3bpw** (IQ2_XS passa; IQ2_S 2.17 / IQ1_M ~1.9 / IQ1_S 1.78 falham) para famílias Qwen3.x nesta bateria.
3. **ΔA→B é a métrica-chave do crivo**: candidato bom cru mas que NÃO responde aos trilhos é lixo para o harness (vivemos trilhados).
4. Peripécias de método (autópsia documentada): (a) facilitador — runner sem matar o port anterior mediu 5 modelos contra o MESMO servidor (descoberto pelo campo `model` nos ts-json); (b) kwargs JSON com quotes aninhadas quebrava o launch; (c) thinking-models esvaziam `content` (usar reasoning ou `enable_thinking:false`).
5. **Recomendação**: 27B-GSQ-IQ2_XS pode disputar slot futuro SE houver GPU dedicada (BGP 14.7 t/s prefill); sob CPU é peso-morto (1.7 t/s).

## Adendo 2 — 2026-09-16 ~15:30: os 2 Ornith-9B restantes + Ornith-35B na fronteira exacta

| Modelo | A-cpu | B-cpu | A-gpu | B-gpu | dec CPU | dec GPU | Veredito |
|---|---|---|---|---|---|---|---|
| Ornith-1.5-9B-IQ2_M | 1.9 | 3.4 | 1.9 | 3.1 | 4.3/10.5 | 70.5/94.8 | reprovado |
| Ornith-1.5-9B-Q4_K_M-layers0-16 | 0.9 | 0.9 | 0.9 | 0.9 | — | — | reprovado (truncado) |
| **Ornith-1.5-35B-A3B-IQ2_XXS** (bartowski, 2.33bpw) | **4.5** | **6.0** | n/a (VRAM) | n/a | ~3.4 | — | **PASSOU R104** (ΔB vs incumbent 6.2 = 0.2) |

**Refinamento R104**: piso de absorção ~2.3bpw sustenta-se (2.33 passa, 2.17 colapsa) — e o **quantizador conta** (bartowski/imatrix na fronteira > UD/custom). Ornith-35B-IQ2_XXS sobrevive em filtragem/ esperando slot GPU.

## Adendo 3 — 2026-09-16 ~16:50: limpeza externa + falso-negativo documentado

1. `Qwen3.5-35B-UD-IQ2_XXS`: o par A/B que registrei ANTES como 0.9/0.9 era **falso-negativo** — rodou contra servidor morto (`[ERRO]` transporte ×7, nenhuma resposta real). **Inválido, descartar; NÃO é reprovação do modelo.**
2. Em momento posterior, **`filtragem/` foi esvaziada integralmente** (decisão do user — incluindo Ornith-35B-IQ2_XXS que havia PASSADO R104). Veredito da fronteira continua valendo como conhecimento (B=6.0, Δ0.2 do incumbent).
3. Se o interesse voltar em Ornith-35B: redownload `bartowski/Ornith-1.5-35B-A3B-GGUF/resolve/main/Ornith-1.5-35B-A3B-IQ2_XXS.gguf` (10.255.140.512 bytes conferidos).
4. Regra de robustez aprendida: bateria SEM health-**com-identidade** do modelo antes de rodar NÃO entra na tabela (o runner v2 já faz isso com `/v1/models` grep).

## Estado físico pós-sessão

- Stack: 10 slots saudáveis (9088/9097 ficaram sob gestão da session paralela "refinando").
- Disco `/mnt/dados`: **98% → 62%** (42GB liberados em 2026-09-16 12:2x, ordem direta do user: apagados os 6 reprovados — IQ1_S-27B, 3×35B-IQ1_M/IQ2_S, Qwen_-3.6-IQ1_M, Ornith-AD; evidências preservadas em `/tmp/opencode/crivo2-*.jsonl`).
- `.part` de downloads (APEX-Mini 12.4G + IQ2_XXS 9.35G): mortos por ENOSPC às 06:00; agora há espaço para retomar.
- 8090 livre; GSQ permanece em filtragem/ (único reprovável que aguentou a régua).
