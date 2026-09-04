---
title: "Proporção ideal de overclock Vega20"
source: "https://www.kimi.com/chat/19f8ccb2-7fa2-825c-8000-0947d497de21?chat_enter_method=history"
author:
published:
created: 2026-07-24
description: "Experimente o Kimi K3 para criar jogos multiplayer e 3D jogáveis, gerar slides com qualidade de consultoria e executar tarefas em paralelo com Swarm e Goal para trabalhar com mais eficiência."
tags:
  - "clippings"
---
para um overclock saudavel qual e a proporçao ideal Vega 20 (MI50) Clock Domains: 1. SCLK (Graphics/Shader Clock) - GPU core 2. FCLK (Infinity Fabric Clock) - interconnect between GPU core and memory controller 3. MCLK (Memory Clock) - HBM2 memory 4. SOCCLK (SoC Clock) - memory controller and SoC components

Editar

Copiar

Compartilhar

Finding Ideal Clock Domain Ratios for Vega 20 Overclocking

Raciocínio concluído

Desculpe, o Kimi está um pouco ocupado. Tente novamente mais tarde.

conclua

Editar

Copiar

Compartilhar

## Overclock Saudável na Vega 20 (MI50) — Proporções Ideais dos Domínios de Clock

A Vega 20 (MI50) possui quatro domínios de clock interdependentes. Para um overclock **estável e saudável**, a chave está em manter **relações harmônicas** entre eles, não apenas empurrar cada um ao máximo isoladamente.

---

## 1\. SCLK (Graphics/Shader Clock) — GPU Core

| Parâmetro | Stock | Overclock Saudável | Máximo Seguro |
| --- | --- | --- | --- |
| **Frequência** | ~1500 MHz | **1600–1700 MHz** | ~1800 MHz |
| **Voltagem** | ~1000 mV | **980–1050 mV** | ~1100 mV |

- O SCLK é o clock mais crítico para performance em compute e gráficos.
- Na MI50, o limite térmico e de voltagem é mais restritivo que na MI60 (que tem TDP maior).
- **Dica**: comece com +50 MHz incrementais e teste estabilidade. A Vega 20 tende a ter "wall" de voltagem acima de 1700 MHz.

---

## 2\. MCLK (Memory Clock) — HBM2

| Parâmetro | Stock | Overclock Saudável | Máximo Seguro |
| --- | --- | --- | --- |
| **Frequência** | 1000 MHz | **1050–1100 MHz** | ~1200 MHz |
| **Largura de banda** | ~1 TB/s | ~1,05–1,1 TB/s | ~1,2 TB/s |

- A HBM2 da MI50 é de alta qualidade (ECC habilitado por padrão).
- Overclock de memória traz ganhos significativos em workloads de compute (mineração, ML, render).
- **Atenção**: o MCLK está diretamente ligado ao FCLK — eles devem caminhar juntos.

---

## 3\. FCLK (Infinity Fabric Clock) — Interconexão

| Parâmetro | Stock | Overclock Saudável | Máximo Seguro |
| --- | --- | --- | --- |
| **Frequência** | ~1000 MHz | **1050–1100 MHz** | ~1200 MHz |

- O FCLK conecta o GPU core ao controlador de memória (HBM2).
- **Regra de ouro**: `FCLK ≈ MCLK` (ou muito próximo).
- Se o FCLK ficar muito abaixo do MCLK, cria-se um gargalo entre o core e a memória.
- Se o FCLK ficar muito acima do MCLK, desperdiça-se potência sem ganho real.

---

## 4\. SOCCLK (SoC Clock) — Controlador de Memória e SoC

| Parâmetro | Stock | Overclock Saudável | Máximo Seguro |
| --- | --- | --- | --- |
| **Frequência** | ~1100 MHz | **1100–1200 MHz** | ~1267 MHz |

- O SOCCLK alimenta o controlador de memória e componentes do SoC.
- Na Vega 20, o SOCCLK tem **relação fixa ou semi-fixa** com o MCLK/FCLK.
- Em alguns casos, o SOCCLK é automaticamente ajustado pelo driver/VBIOS quando você altera o MCLK.
- **Não force o SOCCLK muito acima do MCLK** — isso pode causar instabilidade no controlador de memória.

---

## 📐 Proporções Ideais para Overclock Saudável

Aqui está a receita prática:

```markdown
┌─────────────────────────────────────────────────────────────┐
│  SCLK : MCLK : FCLK : SOCCLK                                │
│                                                             │
│  1600–1700 : 1050–1100 : 1050–1100 : 1100–1200  (MHz)      │
│                                                             │
│  Ou, em termos de proporção simplificada:                   │
│                                                             │
│  SCLK ≈ 1,5× a 1,6× o MCLK                                  │
│  FCLK ≈ 1,0× o MCLK (sempre igual ou muito próximo)        │
│  SOCCLK ≈ 1,0× a 1,1× o MCLK                               │
└─────────────────────────────────────────────────────────────┘
```

### Exemplo prático de configuração estável:

| Domínio | Frequência |
| --- | --- |
| SCLK | **1650 MHz** @ 1000 mV |
| MCLK | **1050 MHz** |
| FCLK | **1050 MHz** |
| SOCCLK | **1100 MHz** |

---

## ⚠️ Regras de Ouro

1. **FCLK = MCLK** (ou no máximo 50 MHz de diferença) — qualquer desbalanceamento aqui causa instabilidade.
2. **Nunca deixe SOCCLK < MCLK** — o controlador de memória precisa de clock suficiente para atender a HBM2.
3. **SCLK é independente**, mas respeite os limites térmicos (target < 85°C hotspot).
4. **Voltagem é o inimigo da longevidade** — prefira under-volt + overclock moderado a voltagem alta.
5. **Teste com workloads reais** — benchmarks sintéticos podem parecer estáveis enquanto aplicações reais crasham.

---

## 🛠️ Ferramentas de Overclock na MI50

Como a MI50 não tem suporte oficial a overclock via AMD Software (Adrenalin), você precisa de:

- **AMDVBFlash** — para modificar o VBIOS (avançado, risco de brick).
- **Radeon Profile / CoreCtrl** — para ajustes via driver no Linux.
- **OverdriveNTool** — para Windows (funcionalidade limitada em GPUs profissionais).
- **Modificação do Power Play Table (PPT)** — método mais comum para MI50/MI60.

---

## Resumo Visual

```markdown
SCLK (Core)
       ↑
┌──────┴──────┐
│   GPU Core  │  ← 1600–1700 MHz
└──────┬──────┘
       │
  FCLK (Fabric)  ← 1050–1100 MHz  ════
       │                          ║
┌──────┴──────┐                   ║
│  Mem Ctrl   │  ← SOCCLK        ║
│  (SoC)      │  1100–1200 MHz   ║
└──────┬──────┘                   ║
       │                          ║
  MCLK (HBM2)  ← 1050–1100 MHz  ════
```

**A HBM2 e o Infinity Fabric devem dançar no mesmo ritmo.** O core pode correr mais rápido, mas se a memória e a interconexão não acompanharem, você terá gargalos ou instabilidade.

A demanda está alta. Mudamos para o K2.6 Instantâneo para responder mais rápido. Faça upgrade para usar o K2.6 Pensando.

Pergunte qualquer coisa. As imagens também funcionam.

Instantâneo Alto