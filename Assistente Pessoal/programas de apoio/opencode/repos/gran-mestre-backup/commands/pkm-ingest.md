# PKM Ingest

Ingestão de documentos no Qdrant como vetores para RAG.

## Script

`/mnt/dados/Assistente Pessoal/scripts/ingest/pkm_ingest.py`

## Requisitos

- Qdrant em `localhost:6333`
- Ollama em `localhost:11434` com `nomic-embed-text`
- `pip install qdrant-client httpx tqdm`

## Uso

```bash
# Ingerir conversas do Claude
python3 pkm_ingest.py --source conversas --file ~/exports/claude.json

# Ingerir transcrições do YouTube
python3 pkm_ingest.py --source youtube --dir ~/transcricoes/

# Ingerir datasheets de hardware
python3 pkm_ingest.py --source hardware --dir ~/docs/datasheets/

# Ingerir histórico do Open-WebUI
python3 pkm_ingest.py --source webui --file ~/.config/open-webui/chats.json
```

## Coleções Qdrant

| Collection | Fonte |
|------------|-------|
| `conversas` | Conversas do Claude |
| `youtube` | Transcrições de vídeo |
| `hardware` | Datasheets e docs de PCB |
| `webui` | Histórico do Open-WebUI |

## Parâmetros de Chunking

- Tamanho do chunk: 400 palavras
- Sobreposição: 60 palavras
- Modelo de embedding: nomic-embed-text (768 dim)
