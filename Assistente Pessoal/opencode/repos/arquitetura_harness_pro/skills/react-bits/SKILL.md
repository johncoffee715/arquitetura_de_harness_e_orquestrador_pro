---
name: react-bits
description: >-
  Catálogo de componentes UI React reutilizáveis (helenizado de
  serif-ai/react-bits, 90+ componentes, 4 variantes por componente, MIT):
  animações, backgrounds, componentes, textos, agrupados por categoria. Use ao
  construir interfaces React, precisar de componente de animação/background/
  texto pronto, ou para padronizar UI sem reescrever do zero. Consulte
  https://reactbits.dev para preview interativo.
---
# React Bits (helenizada)

## Origem (antropofagia)
- **serif-ai/react-bits** (MIT) — 90+ componentes React standalone com 4
  variantes de tema cada (padrão de qualidade: um componente, quatro
  estilos). Essência: catálogo componentizado, zero dependência de framework
  de UI, props minimalistas para customização.

## Categorias (index)

| Categoria | O que contém | Uso típico |
|-----------|--------------|------------|
| **Animações** | `AnimatedContent`, `BlobCursor`, `Magnet`, `SpotlightCard`, `TiltedCard`, `SplittingText` | Micro-interações, hover, entrada de elementos |
| **Backgrounds** | `Aurora`, `GridDistortion`, `ParticleField`, `Ripple`, `Squares`, `Threads`, `Waves` | Hero sections, fundos dinâmicos |
| **Componentes** | `Stack`, `Carousel`, `TiltedCard`, `Masonry`, `Timeline`, `Menu` | Layouts estruturados |
| **Textos** | `AnimatedText`, `CountUp`, `DecryptedText`, `FallingText`, `SplitText`, `TrueFocus`, `TypingEffect` | Tipografia animada, contadores, efeitos de texto |

## Padrão de uso (doutrina)
1. **4 variantes por componente** — o componente vem com 4 estilos (dark/light,
   minimal/rich, etc.). Sempre examinar as variantes antes de customizar.
2. **Props mínimas** — customização via props (`className`, `animationDelay`,
   `intensity`, etc.), não via fork do código.
3. **Standalone** — cada componente é um arquivo autocontido; copiar o arquivo
   do componente (não o repositório inteiro).
4. **Sem dependência externa de UI** — apenas React + CSS/JS; compatível com
   Tailwind ou CSS puro.

## Fluxo de integração
1. Identificar a categoria no index acima.
2. Consultar `https://reactbits.dev` para o preview do componente desejado.
3. Copiar o arquivo do componente + ajustar props (4 variantes disponíveis).
4. Verificar com `/shared/visual-qa` (skill global) após montar a UI.

## Anti-padrões
- NUNCA reescrever um componente que já existe no catálogo (regra R8: catálogo
  primeiro, constrói só o GAP).
- NUNCA importar o repositório inteiro — copiar só o componente necessário.
- NUNCA customizar o CSS interno do componente sem antes tentar via props.
