#!/usr/bin/env python3
"""
Mecânica — secretário (CLI orquestrador).

Uso:
    mecanica.py "<pedido>" [--hitl] [--alvo PATH] [--motivo TXT]
    mecanica.py --registrar "texto" [--tipo decisao|nota|lembrete] [--tags a,b]
    mecanica.py --agenda <add|list|due|done> [...]
    mecanica.py --corresponder --template X --dados '{...}' [--print]

Saída: sempre JSON no stdout. Exit 0 ok / 1 failed / 2 blocked (HITL/governança).
Ação crítica (organizar_mover) sem --hitl = exit 2. Com --hitl + --alvo, move o
alvo para quarentena com backup prévio e log no diário.
"""

import argparse
import json
import os
import sys

from pydantic import BaseModel, ConfigDict, Field, ValidationError

TOOLING = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tooling")
sys.path.insert(0, TOOLING)
from triagem import triar  # noqa: E402
from diario import logar, mover_para_quarentena  # noqa: E402
try:
    from needle_client import acelerar  # noqa: E402
except Exception:  # needle offline -> fallback deterministico silencioso
    def acelerar(pedido, timeout=0.8, url=None):
        return {"usado": False}

SAUDACAO_TEMPLATE = (
    "Olá! Sou o secretário do bibliotecário. "
    "Posso organizar, agendar, registrar, redigir ou pesquisar no vault. "
    "Como posso ajudar?"
)


class Output(BaseModel):
    model_config = ConfigDict(extra="forbid")
    acao: str = Field(pattern=r"^[a-z_]+$")
    destino: str = Field(pattern=r"^[a-z_]+$")
    confidence: float = Field(ge=0.0, le=1.0)
    payload: dict = Field(default_factory=dict)
    vetor_placebo: bool = False
    exit_status: str = Field(pattern=r"^(ok|failed|blocked)$")


def _emit(acao, destino, confidence, payload, vetor_placebo=False,
          exit_status="ok"):
    try:
        out = Output(acao=acao, destino=destino, confidence=confidence,
                     payload=payload, vetor_placebo=vetor_placebo,
                     exit_status=exit_status)
    except ValidationError as e:
        print(json.dumps({"acao": "erro_schema", "erro": str(e),
                          "exit_status": "failed"}, ensure_ascii=False))
        return 1
    print(out.model_dump_json(), flush=True)
    return {"ok": 0, "failed": 1, "blocked": 2}[exit_status]


def despachar(pedido, hitl=False, alvo=None, motivo="", destino=None):
    try:
        tri, _ = triar(pedido)
    except Exception as e:
        return _emit("triagem", "nenhuma", 0.0, {"erro": str(e)},
                     exit_status="failed")
    intent, conf = tri["intent"], float(tri.get("confidence", 0.0))
    rota, critica = tri["rota"], tri.get("acao_critica", False)
    placebo = tri.get("modo") == "lexical_placebo"

    if intent == "saudacao":
        return _emit("triagem", "nenhuma", conf,
                     {"resposta": SAUDACAO_TEMPLATE, "early_exit": True},
                     vetor_placebo=placebo)
    if intent in ("ambiguo", "fora_escopo"):
        return _emit("triagem", "escalar_orquestrador", conf,
                     {"intent": intent, "scores": tri.get("scores", {}),
                      "candidatos": tri.get("candidatos", [])},
                     vetor_placebo=placebo)
    if intent in ("catalogar", "pesquisar", "resumir"):
        return _emit("triagem", "bibliotecario_rwkv7", conf,
                     {"intent": intent,
                      "motivo": "leitura profunda/curadoria — escala ao bibliotecário (:9084)",
                      "scores": tri.get("scores", {})},
                     vetor_placebo=placebo)
    if intent == "organizar_mover":
        if not hitl:
            logar("hitl_bloqueio", pedido, "blocked: ação crítica sem hitl:true")
            return _emit("organizar_mover", "execucao_local", conf,
                         {"intent": intent,
                          "erro": "ação crítica exige --hitl (governança HITL); nada foi executado",
                          "scores": tri.get("scores", {})},
                         vetor_placebo=placebo, exit_status="blocked")
        if not alvo:
            return _emit("organizar_mover", "execucao_local", conf,
                         {"erro": "com --hitl, informe --alvo PATH e --motivo TXT",
                          "exit_status": "blocked"}, exit_status="blocked")
        # Acelerador Needle2 :9099: SUGERE a function call; quem executa e o
        # python deterministico abaixo. Sugestao valida = name==mover_nota e
        # basename(path_origem)==basename(alvo real); destino autoritativo e
        # --destino (ou quarentena quando ausente). Invalido -> deterministico.
        acelerador = "deterministico"
        try:
            sug = acelerar(pedido)
        except Exception:
            sug = {"usado": False}
        if (sug.get("usado") and (sug.get("call") or {}).get("name") == "mover_nota"):
            args = (sug["call"].get("arguments") or {})
            if os.path.basename(str(args.get("path_origem", ""))) == os.path.basename(alvo):
                acelerador = "needle"
        try:
            if destino:
                import shutil
                if not os.path.exists(alvo):
                    raise FileNotFoundError(f"alvo inexistente: {alvo}")
                os.makedirs(os.path.dirname(os.path.abspath(destino)), exist_ok=True)
                shutil.move(alvo, destino)
                entry = logar("organizar_mover", alvo,
                              f"ok (acelerador: {acelerador}; destino {destino}; {motivo or 'hitl aprovado via mecanica.py'})",
                              {"tipo": "mover_deterministico", "path_destino": destino})
            else:
                entry = mover_para_quarentena(alvo, motivo or "hitl aprovado via mecanica.py")
                entry = logar("organizar_mover", alvo,
                              f"ok (acelerador: {acelerador}; quarentena; {entry.get('resultado', '')})",
                              entry.get("reversao", {}))
        except Exception as e:
            return _emit("organizar_mover", "execucao_local", conf,
                         {"erro": str(e)}, exit_status="failed")
        return _emit("organizar_mover", "execucao_local", conf,
                     {"intent": intent, "diario": entry, "acelerador": acelerador})
    # agendar / registrar / corresponder -> despacho orientado (execução via subcomando)
    comando = {"agendar": "mecanica.py --agenda add|list|due",
               "registrar": "mecanica.py --registrar \"texto\"",
               "corresponder": "mecanica.py --corresponder --template X --dados '{...}'"}.get(intent, "")
    return _emit("triagem", rota, conf,
                 {"intent": intent, "comando": comando,
                  "scores": tri.get("scores", {})},
                 vetor_placebo=placebo)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Secretário — CLI orquestrador")
    ap.add_argument("pedido", nargs="?", default=None)
    ap.add_argument("--hitl", action="store_true")
    ap.add_argument("--alvo", default=None)
    ap.add_argument("--destino", default=None)
    ap.add_argument("--motivo", default="")
    ap.add_argument("--registrar", default=None)
    ap.add_argument("--tipo", default="nota")
    ap.add_argument("--tags", default="")
    ap.add_argument("--agenda", nargs=argparse.REMAINDER, default=None)
    ap.add_argument("--corresponder", action="store_true")
    ap.add_argument("--template", default=None)
    ap.add_argument("--dados", default=None)
    ap.add_argument("--print", dest="imprimir", action="store_true")
    args = ap.parse_args(argv)

    if args.registrar is not None:
        from registro import registrar
        try:
            out, _ = registrar(args.registrar, tipo=args.tipo,
                               tags=[t.strip() for t in args.tags.split(",") if t.strip()])
        except Exception as e:
            return _emit("registro", "registro_vetorial", 0.0, {"erro": str(e)},
                         vetor_placebo=True, exit_status="failed")
        code = {"ok": 0, "failed": 1, "blocked": 2}[out.get("exit_status", "failed")]
        print(json.dumps(out, ensure_ascii=False), flush=True)
        return code
    if args.agenda is not None:
        from agenda import main as agenda_main
        return agenda_main(args.agenda)
    if args.corresponder:
        from correspondencia import redigir
        if not args.template or not args.dados:
            print(json.dumps({"acao": "correspondencia",
                              "erro": "exija --template X --dados '{...}'",
                              "exit_status": "failed"}, ensure_ascii=False))
            return 1
        try:
            dados = json.loads(args.dados)
            out, code, doc = redigir(args.template, dados, gravar=not args.imprimir)
        except Exception as e:
            print(json.dumps({"acao": "correspondencia", "erro": str(e),
                              "exit_status": "failed"}, ensure_ascii=False))
            return 1
        if args.imprimir and code == 0:
            print(doc, flush=True)
            return 0
        print(json.dumps(out, ensure_ascii=False), flush=True)
        return code
    if not args.pedido:
        ap.print_help()
        return 1
    return despachar(args.pedido, hitl=args.hitl, alvo=args.alvo, motivo=args.motivo,
                       destino=args.destino)


if __name__ == "__main__":
    sys.exit(main())
