#!/usr/bin/env python3
"""
Correspondência do secretário — redige por templates, NUNCA inventa fatos.

Uso:
    correspondencia.py --template ata_decisao --dados '{"titulo": "...", ...}' [--print] [--slug X]

Todo placeholder {{campo}} do template DEVE existir em --dados; campo ausente =
exit 2 (blocked), nunca preenchimento criativo. Saída padrão: grava em
<cerebro>/harness/correspondencias/YYYY-MM-DD-<slug>.md e imprime recibo JSON.
Com --print: imprime o documento no stdout (sem gravar).
"""

import argparse
import datetime
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(BASE, "templates")
VAULT = "/mnt/dados/Assistente Pessoal/cerebro com IA"
DEST_DIR = os.path.join(VAULT, "harness", "correspondencias")

PH = re.compile(r"\{\{(\w+)\}\}")


def _slug(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9à-ú]+", "-", s).strip("-")
    return s[:60] or "sem-titulo"


def redigir(template, dados, slug=None, gravar=True, hoje=None):
    tpl_path = os.path.join(TEMPLATES, f"{template}.md")
    if not os.path.exists(tpl_path):
        disp = sorted(f[:-3] for f in os.listdir(TEMPLATES) if f.endswith(".md"))
        return {"acao": "correspondencia",
                "erro": f"template desconhecido: {template!r} (disponíveis: {disp})",
                "exit_status": "failed"}, 1, None
    with open(tpl_path, encoding="utf-8") as f:
        corpo = f.read()
    campos = sorted(set(PH.findall(corpo)))
    faltantes = [c for c in campos if c not in dados]
    if faltantes:
        return {"acao": "correspondencia", "template": template,
                "erro": f"campos ausentes em --dados (invenção proibida): {faltantes}",
                "exit_status": "blocked"}, 2, None
    doc = corpo
    for c in campos:
        doc = doc.replace("{{" + c + "}}", str(dados[c]))
    if not doc.startswith("---"):
        return {"acao": "correspondencia", "template": template,
                "erro": "template sem frontmatter YAML — corrompido",
                "exit_status": "failed"}, 1, None
    if gravar:
        dia = hoje or datetime.date.today().isoformat()
        nome = f"{dia}-{slug or _slug(str(dados.get('titulo', template)))}.md"
        os.makedirs(DEST_DIR, exist_ok=True)
        path = os.path.join(DEST_DIR, nome)
        with open(path, "w", encoding="utf-8") as f:
            f.write(doc)
        return {"acao": "correspondencia", "destino": "correspondencia",
                "template": template, "path": path,
                "exit_status": "ok"}, 0, None
    return None, 0, doc


def main(argv=None):
    ap = argparse.ArgumentParser(description="Correspondência do secretário")
    ap.add_argument("--template", required=True)
    ap.add_argument("--dados", required=True, help="JSON com TODOS os campos")
    ap.add_argument("--print", dest="imprimir", action="store_true")
    ap.add_argument("--slug", default=None)
    args = ap.parse_args(argv)
    try:
        dados = json.loads(args.dados)
    except json.JSONDecodeError as e:
        print(json.dumps({"acao": "correspondencia",
                          "erro": f"--dados não é JSON válido: {e}",
                          "exit_status": "failed"}, ensure_ascii=False))
        return 1
    try:
        out, code, doc = redigir(args.template, dados, slug=args.slug,
                                 gravar=not args.imprimir)
    except Exception as e:
        print(json.dumps({"acao": "correspondencia", "erro": str(e),
                          "exit_status": "failed"}, ensure_ascii=False))
        return 1
    if args.imprimir:
        if code != 0:
            print(json.dumps(out, ensure_ascii=False), flush=True)
            return code
        print(doc, flush=True)
        return 0
    print(json.dumps(out, ensure_ascii=False), flush=True)
    return code


if __name__ == "__main__":
    sys.exit(main())
