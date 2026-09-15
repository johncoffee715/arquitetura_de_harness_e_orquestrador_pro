# YouTube Sync

Pipeline de sincronização de canais YouTube: download → transcrição (Whisper) → indexação vetorial (Qdrant).

## Script

`/mnt/dados/Assistente Pessoal/scripts/youtube/youtube_sync.sh`

## Requisitos

- `yt-dlp` instalado
- OpenAI Whisper (`openai-whisper`)
- Qdrant rodando em `localhost:6333`
- Ollama rodando em `localhost:11434` com modelo `nomic-embed-text`

## Uso

```
./scripts/youtube/youtube_sync.sh
```

Lê canais de `configs/youtube_channels.txt` (formato: `url|tags|max_videos`).

## Pipeline

1. Busca vídeos novos via yt-dlp (flat playlist)
2. Verifica índice JSON para evitar re-indexação
3. Transcreve áudio com Whisper (modelo: base)
4. Gera embeddings com nomic-embed-text (Ollama)
5. Indexa no Qdrant (collection: youtube_library)

## Módulo de Integração

`/mnt/dados/Assistente Pessoal/core/modules/youtube.sh` — funções:
- `youtube_search(query, limit)` — busca semântica nos vídeos indexados
- `youtube_ask(query, model)` — pergunta RAG com contexto dos vídeos
- `youtube_stats()` — estatísticas da biblioteca
