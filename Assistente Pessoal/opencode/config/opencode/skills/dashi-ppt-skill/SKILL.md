---
name: dashi-ppt-skill
description: Browser-editable presentations from visual themes — layout+copy HTML decks with per-page console, export HTML/PDF/PPTX.
category: skill
model: local-forge/proposer
---

# dashi-ppt-skill

Generate editable slide decks from docs: themed HTML pages (layout + copy fields),
each with an edit console (modules, palette, focus, animations), exportable to HTML/PDF/PPTX.
Helenizado de `chuspeeism/dashi-ppt-skill` (origem: https://github.com/chuspeeism/dashi-ppt-skill).

## Quando usar

- Relatórios, pitches, reviews, treinamento — deck estruturado, visual uniforme, editável
- Quando o pedido for "gera um PPT/deck/slides" a partir de um documento
- NÃO usar p/ pixel-perfect artesanal (fora do escopo do padrão)

## Como usar

1. **Brief**: tema, público, nº páginas, conclusões a destacar
2. **Tema**: escolher entre os temas instalados (mostrar previews)
3. **Montar**: páginas = (layout × campos de copy) + console por página
4. **Editar**: texto in-place, mídia por clique/arrasto, módulos via sliders
5. **Exportar**: HTML offline / PDF / PPTX (PPTX/PDF exigem Chrome local)

## Princípio

HTML primeiro (agent lê, edita, valida), export depois. Conteúdo zero-upload:
geração/edição/export tudo local. ~100k tokens por deck de 10 páginas — orçar antes.
