#!/usr/bin/env python3
"""
NEEDLE PYTEST FILTER — Filtro cirúrgico de logs pytest para o Needle 2.

O Needle 2 tem janela rígida de 256 tokens (sliding window) — logs brutos
estouram a memória ativa. Este filtro extrai APENAS os 3 componentes vitais:
📍 Localização (arquivo:linha) · 🛑 Assinatura da exceção · ⚖️ Delta (expected vs actual)

Baseado no documento "Needle 2 ai.md" (tranqueiras) — âncoras textuais do pytest:
- '>' (maior que) → linha exata do código que falhou
- 'E' (maiúsculo) → mensagem da exceção
- 'arquivo.py:linha: TipoDaExcecao' → localização
- '_____' → delimitador de escopo

Origin: helenizado: Needle 2 ai.md (2026-08-31)
"""

import argparse
import json
import re
import sys

# Âncoras textuais do pytest
RE_LOCATION = re.compile(r"([\w./\\-]+\.py):(\d+):\s*(\w+(?:Error|Exception|Failure)?)")
RE_EXCEPTION = re.compile(r"^E\s+(.+)$", re.MULTILINE)
RE_CODE_LINE = re.compile(r"^>\s+(.+)$", re.MULTILINE)
RE_DELTA = re.compile(r"(assert|expected|actual|!=|==)", re.IGNORECASE)


def filtrar_pytest(log: str, max_chars: int = 1500) -> dict:
    """Extrai Localização/Assinatura/Delta de um log pytest (densidade pura)."""
    linhas = log.splitlines()

    # 📍 Localização: arquivo.py:linha: Tipo
    locs = []
    for m in RE_LOCATION.finditer(log):
        locs.append({"arquivo": m.group(1), "linha": m.group(2), "tipo": m.group(3)})

    # 🛑 Assinatura: linhas 'E   ...' (mensagem da exceção)
    assinaturas = [m.group(1).strip() for m in RE_EXCEPTION.finditer(log)][:3]

    # ⚖️ Delta: linhas '>   ...' (código que falhou) + contexto assert
    codigo = [m.group(1).strip() for m in RE_CODE_LINE.finditer(log)][:3]
    deltas = [c for c in codigo if RE_DELTA.search(c)][:2]

    # Fallback: se não achou âncoras, pega as linhas com 'assert'/'Error'
    if not deltas:
        deltas = [l.strip()[:200] for l in linhas if "assert" in l.lower()][:2]
    if not assinaturas:
        assinaturas = [l.strip()[:200] for l in linhas if "Error" in l or "Exception" in l][:2]

    resultado = {
        "localizacoes": locs[:3],
        "assinaturas": assinaturas,
        "deltas": deltas,
        "total_linhas_originais": len(linhas),
    }
    # Estimar tokens (janela 256 do Needle — densidade pura)
    payload = json.dumps(resultado, ensure_ascii=False)
    resultado["tokens_estimados"] = max(1, len(payload) // 4)
    resultado["cabe_janela_256"] = resultado["tokens_estimados"] <= 256
    return resultado


def main():
    parser = argparse.ArgumentParser(description="Filtro cirúrgico pytest para Needle 2")
    parser.add_argument("file", nargs="?", help="arquivo de log (default: stdin)")
    parser.add_argument("--json", action="store_true", help="saída JSON")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
            log = f.read()
    else:
        log = sys.stdin.read()

    resultado = filtrar_pytest(log)
    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    else:
        print(f"📍 Localizações: {resultado['localizacoes']}")
        print(f"🛑 Assinaturas: {resultado['assinaturas']}")
        print(f"⚖️ Deltas: {resultado['deltas']}")
        print(f"Tokens estimados: {resultado['tokens_estimados']} "
              f"({'CABE na janela 256' if resultado['cabe_janela_256'] else 'EXCEDE 256'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())