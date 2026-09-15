---
name: buzz
description: Offline audio transcription pattern — Whisper backends (CUDA/MPS/Vulkan), diarization, punctuation, SRT/VTT export, watch-folder + CLI (patterns only).
category: skill
model: local-forge/proposer
---

# buzz

Pipeline de transcrição offline: áudio → separação → backend Whisper → diarização →
pontuação → SRT/VTT/TXT, com watch-folder, CLI e plugins. Helenizado de
`chidiwilliams/buzz` (origem: https://github.com/chidiwilliams/buzz).

## Quando usar

- Transcrever/traduzir áudio/vídeo/YouTube sem upload (privacidade local)
- Legendas com speakers (diarização) e pontuação
- Automação via pasta observada ou CLI

## Como usar

1. **Backend**: escolher por hardware (CUDA / Apple Silicon / Vulkan-whisper.cpp / HF)
2. **Pipeline**: separação → whisper → diarização → pontuação → export (TXT/SRT/VTT)
3. **Live**: mic em tempo real; **Batch**: watch-folder p/ arquivos novos
4. **Plugins**: resumo IA, resize de transcript

## Princípio

Offline-first: modelo local, nada sai da máquina; backend pelo hardware, não pelo hype.
