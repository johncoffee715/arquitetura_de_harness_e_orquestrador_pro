#!/usr/bin/env python3
"""
OCR Pipeline para OpenCode — "Olhos" do Agente
Extrai texto de PDFs, imagens e documentos via Tesseract OCR + pdftotext.
Gera índice JSON pesquisável e atualiza notas .md com conteúdo extraído.

Uso:
    python3 ocr_extract.py                    # Processa todo o vault
    python3 ocr_extract.py --file <arquivo>   # Processa um arquivo específico
    python3 ocr_extract.py --query <texto>    # Busca no índice de extrações
    python3 ocr_extract.py --rebuild           # Reconstrói o índice completo
"""

import os
import sys
import json
import hashlib
import subprocess
import argparse
import re
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

# Configurações
VAULT_PATH = Path("/mnt/dados/cerebro com IA")
SOURCE_PATH = Path("/mnt/win2/textos, pdf e esquemas")
EXTRACTS_DIR = VAULT_PATH / "textos, pdf e esquemas" / ".ocr-extracts"
INDEX_FILE = EXTRACTS_DIR / "ocr-index.json"
LOG_FILE = EXTRACTS_DIR / "ocr-log.txt"

# Tipos suportados
PDF_EXTS = {'.pdf'}
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp'}
TEXT_EXTS = {'.txt', '.md', '.csv'}
ALL_EXTS = PDF_EXTS | IMAGE_EXTS | TEXT_EXTS

# Configuração Tesseract
TESSDATA = os.path.expanduser("~/.local/share/tessdata")
os.environ["TESSDATA_PREFIX"] = os.path.expanduser("~/.local/share")


def log(msg, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def file_hash(filepath):
    """Gera hash MD5 do arquivo para detectar mudanças."""
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_text_pdftotext(pdf_path):
    """Extrai texto de PDF usando pdftotext (poppler)."""
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", str(pdf_path), "-"],
            capture_output=True, text=True, timeout=120,
            env={**os.environ, "TESSDATA_PREFIX": TESSDATA}
        )
        text = result.stdout.strip()
        if text and len(text) > 10:
            return text
    except (subprocess.TimeoutExpired, Exception) as e:
        log(f"pdftotext falhou para {pdf_path}: {e}", "WARN")
    return None


def extract_text_tesseract(image_path):
    """Extrai texto de imagem usando Tesseract OCR."""
    try:
        result = subprocess.run(
            ["tesseract", str(image_path), "stdout", "-l", "por+eng", "--psm", "3"],
            capture_output=True, text=True, timeout=120,
            env={**os.environ, "TESSDATA_PREFIX": TESSDATA}
        )
        text = result.stdout.strip()
        if text and len(text) > 5:
            return text
    except (subprocess.TimeoutExpired, Exception) as e:
        log(f"Tesseract falhou para {image_path}: {e}", "WARN")
    return None


def extract_text_from_pdf_with_ocr(pdf_path):
    """Extrai texto de PDF: tenta pdftotext primeiro, depois OCR página por página."""
    # Tentar pdftotext primeiro
    text = extract_text_pdftotext(pdf_path)
    if text and len(text) > 50:
        return text, "pdftotext"

    # Fallback: converter PDF para imagens e usar OCR
    try:
        tmp_dir = Path("/tmp/ocr_tmp")
        tmp_dir.mkdir(exist_ok=True)

        prefix = tmp_dir / f"page_{hashlib.md5(str(pdf_path).encode()).hexdigest()[:8]}"

        subprocess.run(
            ["pdftoppm", "-r", "300", "-png", str(pdf_path), str(prefix)],
            capture_output=True, timeout=300,
            env={**os.environ, "TESSDATA_PREFIX": TESSDATA}
        )

        pages = sorted(tmp_dir.glob(f"{prefix.name}-*.png"))
        if not pages:
            # Tentar sem hífen
            pages = sorted(tmp_dir.glob(f"{prefix.name}*.png"))

        ocr_texts = []
        for page_img in pages:
            page_text = extract_text_tesseract(page_img)
            if page_text:
                ocr_texts.append(page_text)
            page_img.unlink(missing_ok=True)

        if ocr_texts:
            return "\n\n".join(ocr_texts), "ocr-pdf"

    except Exception as e:
        log(f"OCR PDF falhou para {pdf_path}: {e}", "WARN")

    return None, None


def extract_text_plain(txt_path):
    """Lê arquivo de texto plano."""
    try:
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        for enc in encodings:
            try:
                with open(txt_path, 'r', encoding=enc) as f:
                    return f.read(), "plain-text"
            except UnicodeDecodeError:
                continue
    except Exception as e:
        log(f"Leitura falhou para {txt_path}: {e}", "WARN")
    return None, None


def process_file(filepath):
    """Processa um arquivo individual e retorna dados de extração."""
    filepath = Path(filepath)
    ext = filepath.suffix.lower()

    # Caminho relativo ao vault
    try:
        rel_path = filepath.relative_to(VAULT_PATH)
    except ValueError:
        rel_path = filepath.relative_to(SOURCE_PATH)

    # Hash do arquivo
    fhash = file_hash(filepath)

    # Extrair texto conforme tipo
    text = None
    method = None

    if ext in PDF_EXTS:
        text, method = extract_text_from_pdf_with_ocr(filepath)
    elif ext in IMAGE_EXTS:
        text, method = extract_text_tesseract(filepath), "ocr-image"
    elif ext in TEXT_EXTS:
        text, method = extract_text_plain(filepath)

    if text and len(text) > 5:
        # Criar diretório de extrações
        extract_dir = EXTRACTS_DIR / rel_path.parent
        extract_dir.mkdir(parents=True, exist_ok=True)

        # Salvar texto extraído
        extract_file = extract_dir / f"{filepath.stem}.extracted.txt"
        with open(extract_file, "w", encoding="utf-8") as f:
            f.write(text)

        # Atualizar nota .md correspondente se existir
        md_file = filepath.parent / f"{filepath.stem}.md"
        if md_file.exists() and ext in PDF_EXTS | IMAGE_EXTS:
            update_md_with_extract(md_file, text, method)

        return {
            "path": str(rel_path),
            "hash": fhash,
            "method": method,
            "text_length": len(text),
            "preview": text[:500],
            "extracted_at": datetime.now().isoformat(),
            "has_text": True
        }

    return {
        "path": str(rel_path),
        "hash": fhash,
        "method": method,
        "text_length": 0,
        "preview": "",
        "extracted_at": datetime.now().isoformat(),
        "has_text": False
    }


def update_md_with_extract(md_file, text, method):
    """Atualiza nota .md com o texto extraído."""
    try:
        content = md_file.read_text(encoding="utf-8")

        # Se já tem seção de extração, substituir
        marker_start = "<!-- OCR_EXTRACT_START -->"
        marker_end = "<!-- OCR_EXTRACT_END -->"

        extract_section = f"""
{marker_start}
## 📝 Texto Extraído (OCR)

> [!info] Método: {method}
> Extraído automaticamente pelo OpenCode OCR Pipeline

{text[:5000]}{"..." if len(text) > 5000 else ""}

{marker_end}"""

        if marker_start in content:
            # Substituir seção existente
            start_idx = content.index(marker_start)
            end_idx = content.index(marker_end) + len(marker_end)
            content = content[:start_idx] + extract_section + content[end_idx:]
        else:
            # Adicionar ao final
            content += extract_section

        md_file.write_text(content, encoding="utf-8")
    except Exception as e:
        log(f"Erro ao atualizar {md_file}: {e}", "WARN")


def build_index():
    """Constrói índice JSON de todas as extrações."""
    index = {
        "version": "1.0",
        "last_updated": datetime.now().isoformat(),
        "vault_path": str(VAULT_PATH),
        "source_path": str(SOURCE_PATH),
        "files": {},
        "stats": {
            "total_files": 0,
            "extracted": 0,
            "failed": 0,
            "by_method": {}
        }
    }

    # Listar todos os arquivos processáveis
    source_dir = VAULT_PATH / "textos, pdf e esquemas"
    files_to_process = []

    for root, dirs, files in os.walk(source_dir):
        # Pular diretório de extrações
        if ".ocr-extracts" in root:
            continue
        for fname in files:
            fpath = Path(root) / fname
            if fpath.suffix.lower() in ALL_EXTS:
                files_to_process.append(fpath)

    log(f"Encontrados {len(files_to_process)} arquivos para indexar")

    # Processar arquivos
    for i, fpath in enumerate(files_to_process):
        rel = fpath.relative_to(source_dir)

        # Verificar se já foi processado (hash)
        extract_file = EXTRACTS_DIR / rel.with_suffix(".extracted.txt")
        if extract_file.exists():
            # Ler extração existente
            try:
                text = extract_file.read_text(encoding="utf-8")
                index["files"][str(rel)] = {
                    "path": str(rel),
                    "method": "cached",
                    "text_length": len(text),
                    "preview": text[:500],
                    "has_text": True
                }
                index["stats"]["extracted"] += 1
                method = "cached"
                index["stats"]["by_method"][method] = index["stats"]["by_method"].get(method, 0) + 1
            except Exception:
                pass
        else:
            # Processar novo arquivo
            result = process_file(fpath)
            index["files"][str(rel)] = result
            if result["has_text"]:
                index["stats"]["extracted"] += 1
                method = result["method"]
                index["stats"]["by_method"][method] = index["stats"]["by_method"].get(method, 0) + 1
            else:
                index["stats"]["failed"] += 1

        index["stats"]["total_files"] += 1

        if (i + 1) % 50 == 0:
            log(f"Progresso: {i + 1}/{len(files_to_process)}")

    # Salvar índice
    EXTRACTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    log(f"Índice salvo: {INDEX_FILE}")
    log(f"Total: {index['stats']['total_files']} arquivos, "
        f"{index['stats']['extracted']} extraídos, "
        f"{index['stats']['failed']} falharam")
    log(f"Métodos: {index['stats']['by_method']}")

    return index


def search_index(query, limit=20):
    """Busca texto no índice de extrações."""
    if not INDEX_FILE.exists():
        log("Índice não existe. Execute --rebuild primeiro.", "ERROR")
        return []

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        index = json.load(f)

    results = []
    query_lower = query.lower()

    for path, data in index.get("files", {}).items():
        preview = data.get("preview", "").lower()
        if query_lower in preview:
            results.append({
                "path": path,
                "preview": data["preview"][:300],
                "text_length": data.get("text_length", 0),
                "score": preview.count(query_lower)
            })

    # Ordenar por relevância
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]


def extract_single(filepath):
    """Extrai texto de um único arquivo e retorna resultado."""
    result = process_file(Path(filepath))
    if result["has_text"]:
        log(f"Extraído: {result['path']} ({result['text_length']} chars, método: {result['method']})")
        print(f"\n{'='*60}")
        print(f"ARQUIVO: {result['path']}")
        print(f"MÉTODO: {result['method']}")
        print(f"TAMANHO: {result['text_length']} caracteres")
        print(f"{'='*60}")
        print(result["preview"])
    else:
        log(f"Sem texto: {result['path']}", "WARN")
    return result


def main():
    parser = argparse.ArgumentParser(description="OCR Pipeline para OpenCode")
    parser.add_argument("--file", "-f", help="Processar arquivo específico")
    parser.add_argument("--query", "-q", help="Buscar no índice de extrações")
    parser.add_argument("--rebuild", "-r", action="store_true", help="Reconstruir índice completo")
    parser.add_argument("--limit", "-l", type=int, default=20, help="Limite de resultados na busca")
    parser.add_argument("--stats", "-s", action="store_true", help="Mostrar estatísticas do índice")

    args = parser.parse_args()

    if args.file:
        extract_single(args.file)
    elif args.query:
        results = search_index(args.query, args.limit)
        if results:
            print(f"\n🔍 {len(results)} resultados para '{args.query}':\n")
            for r in results:
                print(f"  📄 {r['path']} ({r['text_length']} chars, score: {r['score']})")
                print(f"     {r['preview'][:200]}...")
                print()
        else:
            print(f"Nenhum resultado para '{args.query}'")
    elif args.rebuild:
        log("=== Reconstruindo índice OCR ===")
        build_index()
    elif args.stats:
        if INDEX_FILE.exists():
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                index = json.load(f)
            stats = index.get("stats", {})
            print(f"\n📊 Estatísticas OCR:")
            print(f"   Total: {stats.get('total_files', 0)} arquivos")
            print(f"   Extraídos: {stats.get('extracted', 0)}")
            print(f"   Falharam: {stats.get('failed', 0)}")
            print(f"   Métodos: {json.dumps(stats.get('by_method', {}), indent=2)}")
        else:
            print("Índice não existe. Execute --rebuild primeiro.")
    else:
        # Modo padrão: extrair tudo
        log("=== Iniciando extração OCR completa ===")
        build_index()


if __name__ == "__main__":
    main()
