#!/usr/bin/env python3
"""Needle2 client do secretario — acelerador de acoes estruturais (:9099).

acelerar(pedido) pergunta ao Needle qual function call o pedido sugere.
O Needle NUNCA executa: quem executa e o python deterministico (mecanica.py),
que valida os argumentos contra paths reais antes de obedecer.
Qualquer falha/timeout -> {"usado": False} silencioso (fallback deterministico).
Zero deps externas (urllib stdlib).
"""

import json
import urllib.request

NEEDLE_URL = "http://127.0.0.1:9099/complete"


def acelerar(pedido, timeout=0.8, url=NEEDLE_URL):
    try:
        body = json.dumps({"input": f"Instrucao: {pedido}"}).encode()
        req = urllib.request.Request(url, data=body, method="POST",
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return {"usado": False}
            out = json.loads(resp.read())
        if out.get("type") != "call":
            return {"usado": False}
        calls = out.get("function_calls") or []
        if not calls:
            return {"usado": False}
        first = calls[0]
        name = first.get("name") or first.get("function") or ""
        args = first.get("arguments", {})
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except Exception:
                return {"usado": False}
        if not name or not isinstance(args, dict):
            return {"usado": False}
        return {"usado": True, "call": {"name": name, "arguments": args}}
    except Exception:
        return {"usado": False}
