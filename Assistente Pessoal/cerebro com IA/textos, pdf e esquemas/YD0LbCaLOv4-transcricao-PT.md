---
video_id: YD0LbCaLOv4
titulo: "Adiós a la nube: Convierte imágenes en segundos con esta herramienta local"
url: https://www.youtube.com/watch?v=YD0LbCaLOv4
canal: Manuel Cabrera Caballero
publicado: 2026-09-08
duracao: 10:54
etiquetas_4selfs: [L-e, S-ca]
origem_legenda: auto-sub PT (yt-dlp 2026.08.19, traduzido do ES)
data_ingestao: 2026-09-17
cues: 231
ferramenta: NoCloud Bulk Image Converter (NoConvert) v3.0.5, Java, multiplataforma (Linux DEB/portátil, Windows, macOS Intel+ARM64)
nota_relevancia: BAIXA p/ P2 — conversor de formato em lote (PNG→JPG/TIF/BMP/GIF), não gera imagem nem vídeo. Utilidade residual: normalizar keyframes em lote.
---

# Transcrição PT limpa — YD0LbCaLOv4 (dedupe, sem timestamps)

Já utilizamos a nuvem há anos. Eles oferecem todo tipo de serviço lá, informações e muito mais, mas certamente já estamos cansados de tanta computação em nuvem, de computação em nuvem, seus custos e a falta de privacidade. Hoje trago para vocês um aplicativo para converter todas essas imagens que você tem isso disponível localmente e não quer. Faça o upload para a nuvem porque você não sabe se eles podem estar copiando, se conseguirem estar usando para outras coisas que eles não te contaram e também é de graça e você está pagando por isso. Vamos analisar um aplicativo. Ok, tudo certo. Isso e muito mais desta equipe que é Pop OS 2404. O aplicativo sobre o qual vamos falar chama-se No Convert ou pelo seu nome completo é o Nocloud Bulk Image Converter. Atualmente está na versão 305. Foi atualizado há 10 meses. Aqui no GitHub que eu já compartilhei com você. Na descrição deste vídeo, nós diz que é rápido, não usa a nuvem, e é um conversor em lote. Ou seja, podemos usar um grupo de imagens, não um por um com o tempo conhecido que podem ser transportados, convertem muitos imagens e fotos armazenadas localmente no modo bash. Se descermos teremos muitos mais características, explicação que é de alto desempenho, processamento em paralelo, etc., etc. Já eu já trouxe esse tipo de coisa para você antes. modelos, este tipo de aplicação ou soluções. Vou deixar outro vídeo onde há vários deles, mas este se chama o atenção principalmente por parte de desempenho. Vamos fazer um teste com mais pessoas também. de 100 arquivos de imagem para ver o quê leva muito tempo para esse tipo de processo. [Demonstração: 149 imagens PNG (~200MB) instaladas via DEB no Pop!_OS/Ubuntu; conversão em lote para JPG; processamento paralelo rápido; BUG observado: arquivos que já existiam em JPG foram duplicados em vez de convertidos (149→249 arquivos).] Isso é perfeito. Não, eles não os têm. O problema são as imagens. Em outras palavras, não vejo nenhum problema para eles. Mas existem vários duplicados e isso porque já eles existiam como arquivos JPG. Então, bem, JPEG, não é um JPG, como se poderia dizer, mas, enfim, é alguma coisa para ter em mente. Hum, provavelmente eu o consideraria um livro. Esperemos que sim. Eles vão corrigir isso em versões futuras. E certo, me diga, você já sabia disso? A ferramenta não converte? Você vai usar? Você vai dar uma chance? Ou o que você faz quando precisa converter um grande número de imagens de um formatá-lo para outro formato e você não quer carregá-lo para o nuvem? Estou te lendo.

## Extraído p/ P2 (útil residual)

- Formatos suportados: PNG→TIF/BMP/GIF/ICNS/JPG e outros; processamento paralelo; multiplataforma (Linux/Windows/macOS).
- Uso no pipeline P2: normalização em lote de keyframes SDXL (ex.: PNG→JPG) antes do img2vid; alternativa nativa: `mogrify`/ffmpeg (já instalado).
- Bug: não sobreskipa destino existente — duplica. Cuidado em lote.
