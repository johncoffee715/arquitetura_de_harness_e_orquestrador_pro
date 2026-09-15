#!/usr/bin/env python3
"""
Agenda do secretário — compromissos determinísticos em tooling/data/agenda.json.

Uso:
    agenda.py add "descrição" --em "em 2 dias" | "toda SEG" | "2026-09-20" | "hoje" | "amanhã"
    agenda.py list [--todas]
    agenda.py due
    agenda.py done <id>

`due` = itens com data <= hoje e não concluídos. Saída sempre JSON, exit 0.
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data", "agenda.json")

SEMANA = {"dom": 6, "seg": 0, "ter": 1, "qua": 2, "qui": 3, "sex": 4, "sab": 5}


def _hoje():
    return datetime.date.today()


def parse_quando(expr, ref=None):
    """Parser determinístico de datas pt-BR. Retorna date ou levanta ValueError."""
    ref = ref or _hoje()
    e = expr.strip().lower()
    if e in ("hoje",):
        return ref
    if e in ("amanha", "amanhã"):
        return ref + datetime.timedelta(days=1)
    m = re.fullmatch(r"em\s+(\d+)\s+dias?", e)
    if m:
        return ref + datetime.timedelta(days=int(m.group(1)))
    m = re.fullmatch(r"(?:toda|todo)\s+([a-zç]{3,})", e)
    if m:
        alvo = SEMANA.get(m.group(1)[:3])
        if alvo is None:
            raise ValueError(f"dia da semana desconhecido: {expr}")
        delta = (alvo - ref.weekday()) % 7 or 7
        return ref + datetime.timedelta(days=delta)
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.datetime.strptime(expr.strip(), fmt).date()
        except ValueError:
            continue
    raise ValueError(f"expressão de data não suportada: {expr!r} "
                     "(use: hoje | amanhã | em N dias | toda SEG | YYYY-MM-DD)")


def _carregar():
    if not os.path.exists(DATA):
        return []
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def _salvar(itens):
    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(itens, f, ensure_ascii=False, indent=2)


def cmd_add(descricao, em):
    quando = parse_quando(em)
    agora = datetime.datetime.now(datetime.timezone.utc).isoformat()
    item = {
        "id": hashlib.md5((agora + descricao).encode()).hexdigest()[:8],
        "descricao": descricao, "quando": quando.isoformat(),
        "criada_em": agora, "feita": False,
    }
    itens = _carregar()
    itens.append(item)
    _salvar(itens)
    return {"acao": "agenda_add", "item": item, "exit_status": "ok"}, 0


def cmd_list(todas=False):
    itens = _carregar()
    if not todas:
        itens = [i for i in itens if not i.get("feita")]
    itens = sorted(itens, key=lambda i: i["quando"])
    return {"acao": "agenda_list", "total": len(itens), "itens": itens,
            "exit_status": "ok"}, 0


def cmd_due():
    hoje = _hoje().isoformat()
    itens = [i for i in _carregar()
             if not i.get("feita") and i["quando"] <= hoje]
    itens = sorted(itens, key=lambda i: i["quando"])
    return {"acao": "agenda_due", "hoje": hoje, "total": len(itens),
            "itens": itens, "exit_status": "ok"}, 0


def cmd_done(item_id):
    itens = _carregar()
    for i in itens:
        if i["id"] == item_id or i["id"].startswith(item_id):
            i["feita"] = True
            _salvar(itens)
            return {"acao": "agenda_done", "item": i, "exit_status": "ok"}, 0
    return {"acao": "agenda_done", "erro": f"id não encontrado: {item_id}",
            "exit_status": "failed"}, 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="Agenda do secretário")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_add = sub.add_parser("add")
    p_add.add_argument("descricao")
    p_add.add_argument("--em", required=True)
    p_list = sub.add_parser("list")
    p_list.add_argument("--todas", action="store_true")
    sub.add_parser("due")
    p_done = sub.add_parser("done")
    p_done.add_argument("id")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "add":
            out, code = cmd_add(args.descricao, args.em)
        elif args.cmd == "list":
            out, code = cmd_list(todas=args.todas)
        elif args.cmd == "due":
            out, code = cmd_due()
        else:
            out, code = cmd_done(args.id)
    except ValueError as e:
        print(json.dumps({"acao": f"agenda_{args.cmd}", "erro": str(e),
                          "exit_status": "failed"}, ensure_ascii=False))
        return 1
    except Exception as e:
        print(json.dumps({"acao": "agenda", "erro": str(e),
                          "exit_status": "failed"}, ensure_ascii=False))
        return 1
    print(json.dumps(out, ensure_ascii=False), flush=True)
    return code


if __name__ == "__main__":
    sys.exit(main())
