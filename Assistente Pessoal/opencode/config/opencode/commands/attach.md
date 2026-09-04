---
description: "Anexar mídia ao contexto: imagem/vídeo/áudio por caminho (drag-and-drop no gerenciador de arquivos cola o caminho). Extrai metadata, frames e transcrição. Uso: /attach <caminho1> [caminho2 ...] [--frames N]"
---

Anexos de mídia processados pelo motor `attach_media` (schema: scripts/attach_media.schema.json).
Saída estruturada abaixo — use-a para integrar o anexo ao contexto (não invente descrição de
conteúdo; se o status for `partial`, declare a limitação com honestidade).

!`python3 /mnt/dados/Assistente Pessoal/opencode/config/opencode/scripts/attach_media.py $ARGUMENTS`

**Como usar a saída** (regras do orquestrador):
1. `status: ok` — incorpore o resumo/transcrição ao raciocínio e cite os caminhos dos frames.
2. `status: partial` — use apenas metadata + caminhos; informe ao usuário o que falta
   (ex.: ASR offline → instalar whisper; visão descontinuada 2026-08-28 — reativar só com modelo canonizado via ATTACH_VISION_MODEL).
3. `status: error` — repasse o erro exato; não prossiga sem o anexo se a task depende dele.
4. Vídeo: frames estão em /tmp/opencode/attach-frames/<nome>/ — referencie, não copie (R28 evidência).
5. Itens abaixo atendem a task. Não anexei nada que não foi solicitado.
