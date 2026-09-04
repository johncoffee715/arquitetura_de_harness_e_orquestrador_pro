---
tags:
  - system
  - ocr
  - opencode
---

# 🔍 OCR Vision — Olhos do OpenCode

Este diretório contém o sistema de extração de texto (OCR) que permite ao OpenCode examinar, analisar e pesquisar em PDFs, imagens e documentos.

## Como Usar

### Buscar texto nas extrações
```bash
python3 ~/.opencode/scripts/ocr-pipeline/ocr_extract.py --query "termo de busca"
```

### Extrair texto de um arquivo específico
```bash
python3 ~/.opencode/scripts/ocr-pipeline/ocr_extract.py --file "/caminho/para/arquivo.pdf"
```

### Ver estatísticas
```bash
python3 ~/.opencode/scripts/ocr-pipeline/ocr_extract.py --stats
```

### Rebuild completo
```bash
python3 ~/.opencode/scripts/ocr-pipeline/ocr_extract.py --rebuild
```

## Estrutura

```
.ocr-extracts/
├── OCR_CONTEXT.md          # Este arquivo
├── ocr-index.json          # Índice pesquisável de todas as extrações
├── ocr-log.txt             # Log de processamento
└── [mesma estrutura do vault]/
    └── *.extracted.txt     # Texto extraído de cada arquivo
```

## Integração com OpenCode

Para usar o OCR como contexto no OpenCode:
1. Use `--query` para buscar texto específico
2. Use `--file` para extrair texto de um documento
3. Os arquivos `.extracted.txt` contêm o texto puro para referência
4. O `ocr-index.json` permite buscas rápidas

## Motor OCR

- **PDFs:** pdftotext (poppler) → fallback para Tesseract OCR
- **Imagens:** Tesseract 5.5.2 com suporte PT+EN
- **Textos:** Leitura direta com detecção de encoding
