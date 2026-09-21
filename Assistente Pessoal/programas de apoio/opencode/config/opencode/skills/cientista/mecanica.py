#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mecanica.py — motor DETERMINISTICO (zero-LLM) da skill `cientista` (L2, spec
2026-09-17-feature-cientista-spec.md §4/§6/§8/§9; quarteto R85 com gabarito.json/schema.gbnf).

(a) agrega sinais de 7 dias: linhas/dia do decision-log.jsonl (parse tolerante — linhas
    ruins contadas, nunca fatais), arquivos novos/modificados (mtime) em decisoes/ e
    aprendizados/, eventos com campo severidade; leitura SOB allowlist_leitura.
(b) dedupe anti-eco: fingerprint sha1(nome-normalizado + primeiros 80 chars); recorrencia
    entre semanas sobe severidade info->atencao->acao — item unico evolui, nunca duplica.
(c) autorreferencia `origem: cientista` => classe "auto", contada a parte, NUNCA vira
    experimento (max_recursao); mecanica nao agenda nada (guard 2, spec §6).
(d) classifica cada achado em exatamente 1 self (S-ca/H-e/L-e/A-m) por keywords
    (defaults embutidos; gabarito.json pode sobrescrever; fail-closed se invalido).
(e) emite relatorio-esqueleto JSON — cada achado valida contra schema.gbnf (parser
    equivalente embutido: 8 campos exatos, enums exatos, strings nao-vazias).
(f) idempotencia ISO-week: runs_locks/<YYYY-Www>.done — semana completa + lock => no-op
    exit 0; --dry-run nunca escreve lock nem state.
(g) exit_status explicito; erros com path real; NUNCA silencioso.

Usage: python3 mecanica.py --semana atual|YYYY-Www [--dry-run] [--out PATH]
"""
import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
VAULT = Path("/mnt/dados/Assistente Pessoal/cerebro com IA")
SELF_IDS = ["S-ca", "H-e", "L-e", "A-m"]  # guard 4: exatamente 1 self por achado
SEVERIDADES = ["info", "atencao", "acao"]  # escada anti-eco (spec §6.3), ordem crescente
CAMPOS = ["fenomeno_observado", "hipotese_refutacao_vies", "variavel_e_controle",
          "protocolo_teste", "confianca", "risco", "self", "origem"]
ENUMS = {"confianca": ["alta", "media", "baixa"],
         "risco": ["nenhum", "baixo", "medio", "alto"], "self": SELF_IDS}
DESTRUTIVO = ("rm -rf", "delete", "apagar", "force-push", "drop table", "reset --hard")

DEFAULT_GABARITO = {
    "paths": {"vault": str(VAULT), "experimentos": str(VAULT / "experimentos"),
              "runs_locks": str(VAULT / "experimentos" / ".runs"),
              "decision_log": str(VAULT / "harness" / "decision-log.jsonl"),
              "decisoes": str(VAULT / "decisoes"), "aprendizados": str(VAULT / "aprendizados")},
    "allowlist_leitura": [str(VAULT / "decisoes") + "/**", str(VAULT / "aprendizados") + "/**",
                          str(VAULT / "harness" / "decision-log.jsonl")],
    "exclusion_list": ["**/quarentena/**", "**/archive/**", "**/ImagensFundo/**",
                       "**/*.gguf", "**/*.bin", "**/*.safetensors", "**/*.onnx"],
    "selfs": {"S-ca": ["skill", "harness", "forja", "hefesto", "instala", "config",
                       "plugin", "hook", "spec", "quarteto", "gbnf", "schema", "scaffold"],
              "H-e": ["erro", "falha", "falhou", "fix", "corrige", "correcao", "bug",
                      "crash", "trava", "travou", "down", "fallback", "pendencia", "retry"],
              "L-e": ["aprendizado", "licao", "benchmark", "crivo", "evidencia", "memoria",
                      "wiki", "perola", "insight", "decisao", "registro"],
              "A-m": ["otimiza", "melhora", "refactor", "performance", "velocidade",
                      "custo", "token", "upgrade", "migra", "reduz", "economia", "vram"]},
    "self_default": "S-ca", "max_recursao": 1, "max_experimentos": 3,
    "thresholds": {"confianca_alta_min": 5, "confianca_media_min": 2}}

_ACCENT = str.maketrans("áàâãéêíóôõúüçÁÀÂÃÉÊÍÓÔÕÚÜÇ", "aaaaeeiooouucAAAAEEIOOOUUC")


def sem_acento(s):
    return (s or "").translate(_ACCENT)


def die(codigo, msg):
    """(g) NUNCA silencioso: exit_status failed no stderr + codigo de saida."""
    print(json.dumps({"exit_status": "failed", "erro": msg}, ensure_ascii=False), file=sys.stderr)
    sys.exit(codigo)


def glob_regex(pat):
    """Glob do gabarito (**/x/**, **/*.ext) -> regex deterministica (fullmatch)."""
    r = re.escape(pat).replace(r"\*\*/", "(?:.*/)?").replace(r"/\*\*", "(?:/.*)?")
    return re.compile("^" + r.replace(r"\*", "[^/]*") + "$", re.IGNORECASE)


def load_gabarito():
    """gabarito.json e a FONTE UNICA: ausente => defaults; presente e invalido => exit 2."""
    g = json.loads(json.dumps(DEFAULT_GABARITO))
    p = SKILL_DIR / "gabarito.json"
    if not p.exists():
        print(f"[aviso] gabarito.json ausente ({p}) — defaults embutidos", file=sys.stderr)
        data = {}
    else:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            die(2, f"gabarito invalido (parse JSON): {p} :: {e}")
        if not isinstance(data, dict):
            die(2, f"gabarito invalido (raiz nao-e-objeto): {p}")
        for chave in ("selfs_validos", "severidades", "exclusion_list", "paths"):
            if chave not in data:
                die(2, f"gabarito invalido (chave obrigatoria ausente '{chave}'): {p}")
        if set(data["selfs_validos"]) != set(SELF_IDS):
            die(2, f"gabarito invalido (selfs_validos != {SELF_IDS}): {p}")
        if set(data["severidades"]) != set(SEVERIDADES):
            die(2, f"gabarito invalido (severidades != {SEVERIDADES}): {p}")
        if not (isinstance(data["exclusion_list"], list) and data["exclusion_list"]):
            die(2, f"gabarito invalido (exclusion_list vazia): {p}")
        if not isinstance(data["paths"], dict):
            die(2, f"gabarito invalido (paths nao-e-objeto): {p}")
        if "iso_week_runid" in data and not data["iso_week_runid"]:
            die(2, f"gabarito invalido (iso_week_runid=false; motor exige run-id ISO): {p}")
    g.update({k: v for k, v in data.items()
              if k in ("paths", "exclusion_list", "allowlist_leitura", "selfs",
                        "thresholds", "self_default", "max_recursao",
                        "max_experimentos", "porta_teste")})
    g["paths"] = {**DEFAULT_GABARITO["paths"], **data.get("paths", {})}
    if "runs_locks" not in g["paths"]:
        g["paths"]["runs_locks"] = str(Path(g["paths"]["experimentos"]) / ".runs")
    for e in data.get("allowlist_leitura", DEFAULT_GABARITO["allowlist_leitura"]):
        b = re.sub(r"/\*\*$", "", e)  # deriva fontes concretas do allowlist
        if b.endswith("decision-log.jsonl"):
            g["paths"]["decision_log"] = b
        elif b.endswith("/decisoes"):
            g["paths"]["decisoes"] = b
        elif b.endswith("/aprendizados"):
            g["paths"]["aprendizados"] = b
    allow = [glob_regex(e) for e in g["allowlist_leitura"]]
    for k in ("decision_log", "decisoes", "aprendizados"):  # leitura SOB allowlist
        if not any(rx.fullmatch(g["paths"][k]) or rx.fullmatch(g["paths"][k] + "/x")
                   for rx in allow):
            die(2, f"fonte '{k}' fora do allowlist_leitura: {g['paths'][k]}")
    g["_excl"] = [glob_regex(e) for e in g["exclusion_list"]]
    g["_gabarito_path"] = str(p) if p.exists() else "defaults-embutidos"
    return g


def parse_semana(arg):
    """Retorna (week_id, segunda, domingo, completa). Fail-closed em formato invalido."""
    hoje = date.today()
    if arg == "atual":
        iso = hoje.isocalendar()
        segunda = date.fromisocalendar(iso[0], iso[1], 1)
        return f"{iso[0]}-W{iso[1]:02d}", segunda, segunda + timedelta(days=6), False
    m = re.fullmatch(r"(\d{4})-W(\d{2})", arg or "")
    if not m:
        die(2, f"--semana invalida: '{arg}' (use 'atual' ou YYYY-Www, ex. 2026-W38)")
    try:
        segunda = date.fromisocalendar(int(m.group(1)), int(m.group(2)), 1)
    except (ValueError, TypeError) as e:
        die(2, f"--semana invalida: '{arg}' :: {e}")
    if segunda > hoje:
        die(2, f"--semana futura nao executavel: '{arg}' (hoje={hoje.isoformat()})")
    domingo = segunda + timedelta(days=6)
    return f"{int(m.group(1))}-W{int(m.group(2)):02d}", segunda, domingo, domingo < hoje


def fingerprint(nome, amostra):
    """(b) sha1(nome-normalizado + primeiros 80 chars) — formula fixa (spec §6.3)."""
    n = re.sub(r"\s+", " ", sem_acento(nome).lower()).strip()
    return hashlib.sha1((n + "|" + (amostra or "")[:80]).encode("utf-8", "replace")).hexdigest()


def agrega(g, ini, fim):
    """(a) sinais da janela de 7 dias. Parse tolerante: linhas ruins contadas."""
    sinais, resumo = [], Counter()
    dl = Path(g["paths"]["decision_log"])
    if dl.exists():
        with dl.open(encoding="utf-8", errors="replace") as fh:
            for linha in fh:
                linha = linha.strip()
                try:
                    ev = json.loads(linha)
                    ts = str(ev["ts"])[:10] if isinstance(ev, dict) and "ts" in ev else ""
                    d = date.fromisoformat(ts) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", ts) else None
                except Exception:
                    d = None
                if d is None:
                    if linha:
                        resumo["linhas_ruins"] += 1
                    continue
                if not ini <= d <= fim:
                    continue
                resumo[f"decisionlog_linhas_{ts}"] += 1
                resumo["decisionlog_linhas_janela"] += 1
                sev = sem_acento(str(ev.get("severidade", ""))).lower()
                if sev in SEVERIDADES:
                    resumo["eventos_com_severidade"] += 1
                else:
                    sev = "info"
                sinais.append({"nome": str(ev.get("event") or "evento_sem_nome"),
                               "amostra": linha, "severidade": sev,
                               "origem": f"decision-log:{ts}",
                               "auto": sem_acento(str(ev.get("origem", ""))).lower() == "cientista",
                               "ocorrencias": 1})
    else:
        print(f"[aviso] decision-log ausente: {dl}", file=sys.stderr)
    for chave in ("decisoes", "aprendizados"):
        base = Path(g["paths"][chave])
        if not base.exists():
            print(f"[aviso] diretorio ausente: {base}", file=sys.stderr)
            continue
        for f in sorted(base.rglob("*")):
            if not f.is_file() or any(rx.fullmatch(str(f)) for rx in g["_excl"]):
                continue
            try:
                if not ini <= date.fromtimestamp(f.stat().st_mtime) <= fim:
                    continue
                head = f.read_text(encoding="utf-8", errors="replace")[:400]
            except OSError as e:
                print(f"[aviso] leitura falhou: {f} :: {e}", file=sys.stderr)
                continue
            resumo["arquivos_na_janela"] += 1
            auto = bool(re.search(r"origem:\s*cientista", head, re.IGNORECASE))
            resumo["auto_referencia"] += 1 if auto else 0
            sinais.append({"nome": f.name, "amostra": head, "severidade": "info",
                           "origem": str(f), "auto": auto, "ocorrencias": 1})
    return sinais, resumo


def dedupe(sinais, state, week):
    """(b) anti-eco: fp repetido entre semanas sobe severidade; na semana agrega."""
    fps, unicos = state.get("fingerprints", {}), {}
    for s in sinais:
        s["fp"] = fingerprint(s["nome"], s["amostra"])
        if s["fp"] in unicos:
            unicos[s["fp"]]["ocorrencias"] += 1  # item unico evolui, nunca duplica
            continue
        anteriores = [w for w in fps.get(s["fp"], {}).get("semanas", []) if w != week]
        if anteriores:
            s["severidade"] = max(s["severidade"],
                                  "atencao" if len(anteriores) == 1 else "acao",
                                  key=SEVERIDADES.index)
            s["recorrencia_semanas"] = sorted(anteriores)
        unicos[s["fp"]] = s
    return list(unicos.values())


def classifica(s, g):
    """(d) exatamente 1 self por achado; keywords; empate => ordem SELF_IDS."""
    texto = sem_acento(f"{s['nome']} {s['amostra']}").lower()
    melhor, pontos = g.get("self_default", "S-ca"), 0
    for sid in SELF_IDS:
        pts = sum(1 for kw in g["selfs"].get(sid, []) if sem_acento(kw).lower() in texto)
        if pts > pontos:
            melhor, pontos = sid, pts
    return melhor


def esqueleto(s, g, week):
    """(e) 1 achado conforme schema.gbnf (root do schema = 1 achado)."""
    thr = g.get("thresholds", {})
    occ = s["ocorrencias"] + len(s.get("recorrencia_semanas", []))
    conf = ("alta" if occ >= thr.get("confianca_alta_min", 5) else
            "media" if occ >= thr.get("confianca_media_min", 2) else "baixa")
    texto = sem_acento(f"{s['nome']} {s['amostra']}").lower()
    rec = f" Recorre nas semanas {s['recorrencia_semanas']}." if s.get("recorrencia_semanas") else ""
    return {"fenomeno_observado": f"[{s['severidade']}] {s['nome']} — {s['ocorrencias']} "
            f"ocorrencia(s) na janela, origem {s['origem']}.{rec}",
            "hipotese_refutacao_vies": "Vies conhecido: o vault observa o reflexo do que o "
            "usuario registrou (spec §11.4); correlacao nao-e causalidade. Hipotese nula: "
            "o padrao e ruido de cadencia semanal.",
            "variavel_e_controle": f"Variavel: frequencia de '{s['nome']}'. Controle: "
            "baseline das semanas anteriores em experimentos/.runs/state.json.",
            "protocolo_teste": f"Observar 2 semanas ISO; comparar contagens de {week} vs "
            "baseline; criterio de refutacao: variacao dentro do ruido => descartar.",
            "confianca": conf,
            "risco": "medio" if any(k in texto for k in DESTRUTIVO) else "nenhum",
            "self": classifica(s, g),
            "origem": s["origem"]}


def valida_achado(a):
    """Parser equivalente ao schema.gbnf: 8 campos exatos, enums exatos, strings min 1."""
    erros = []
    if set(a) != set(CAMPOS):
        erros.append(f"campos: esperados {sorted(CAMPOS)}, obtidos {sorted(a)}")
    for c in CAMPOS:
        v = a.get(c)
        if not isinstance(v, str) or len(v) < 1:
            erros.append(f"{c}: string nao-vazia obrigatoria (min 1 char)")
        elif c in ENUMS and v not in ENUMS[c]:
            erros.append(f"{c}: '{v}' fora do enum {ENUMS[c]}")
    return erros


def main():
    ap = argparse.ArgumentParser(
        description="cientista.mecanica — motor deterministico zero-LLM (spec 2026-09-17)")
    ap.add_argument("--semana", default="atual", help="'atual' ou YYYY-Www (ex. 2026-W38)")
    ap.add_argument("--dry-run", action="store_true", help="nunca escreve lock nem state")
    ap.add_argument("--out", default=None, help="escreve o relatorio JSON em PATH")
    args = ap.parse_args()

    g = load_gabarito()
    week, segunda, domingo, completa = parse_semana(args.semana)
    runs = Path(g["paths"]["runs_locks"])
    lock, state_path = runs / f"{week}.done", runs / "state.json"
    try:
        runs.mkdir(parents=True, exist_ok=True)  # infraestrutura (smoke exige)
    except OSError as e:
        die(2, f"impossivel criar {runs} :: {e}")

    if lock.exists():  # (f) idempotencia ISO-week: lock => reexecucao e' no-op exit 0
        print(json.dumps({"exit_status": "ok", "no-op": f"semana {week} ja executada",
                          "lock": str(lock)}, ensure_ascii=False))
        return 0

    ini = date.today() - timedelta(days=6) if args.semana == "atual" else segunda
    fim = date.today() if args.semana == "atual" else domingo

    state = {}
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except Exception as e:
            die(2, f"state.json invalido: {state_path} :: {e}")
        if not isinstance(state, dict):
            die(2, f"state.json invalido (raiz nao-e-objeto): {state_path}")

    sinais, resumo = agrega(g, ini, fim)
    unicos = dedupe(sinais, state, week)
    auto = [s for s in unicos if s["auto"]]
    candidatos = [s for s in unicos if not s["auto"]]  # (c) nunca experimento sobre si
    candidatos.sort(key=lambda s: (-SEVERIDADES.index(s["severidade"]),
                                   -s["ocorrencias"], s["nome"]))
    achados = [esqueleto(s, g, week) for s in candidatos[:int(g["max_experimentos"])]]
    erros = [err for a in achados for err in valida_achado(a)]
    if erros:
        die(2, "achado(s) fora do schema.gbnf: " + "; ".join(erros))

    relatorio = {"exit_status": "ok", "semana": week, "run_id": f"cientista-{week}",
                 "janela": [ini.isoformat(), fim.isoformat()],
                 "semana_completa": completa,
                 "modo": "dry-run" if args.dry_run else "execucao",
                 "gabarito": g["_gabarito_path"], "porta_teste": g.get("porta_teste"),
                 "resumo": {**{k: resumo[k] for k in sorted(resumo)},
                            "sinais_unicos": len(unicos), "auto_referencia": len(auto),
                            "recursao_capada": len(auto) > int(g["max_recursao"]) - 1},
                 "origem_stack": ["harness/decision-log.jsonl", "decisoes/", "aprendizados/"],
                 "achados": achados,
                 "schema": "schema.gbnf (root=achado; cada item validado pelo parser equivalente)"}
    out = json.dumps(relatorio, ensure_ascii=False, indent=2)
    print(out)

    if args.out:
        try:
            Path(args.out).write_text(out + "\n", encoding="utf-8")
        except OSError as e:
            die(2, f"impossivel escrever --out {args.out} :: {e}")

    if not args.dry_run:
        fps = state.setdefault("fingerprints", {})
        for s in unicos:
            e = fps.setdefault(s["fp"], {"semanas": [], "ocorrencias": 0, "severidade": "info"})
            if week not in e["semanas"]:
                e["semanas"].append(week)
            e["ocorrencias"] += s["ocorrencias"]
            if SEVERIDADES.index(s["severidade"]) > SEVERIDADES.index(e["severidade"]):
                e["severidade"] = s["severidade"]
        try:
            state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2),
                                  encoding="utf-8")
            lock.write_text(f"run_id=cientista-{week}\njanela={ini.isoformat()}..{fim.isoformat()}"
                            f"\ngerado_em={datetime.now().isoformat(timespec='seconds')}\n",
                            encoding="utf-8")
        except OSError as e:
            die(2, f"impossivel escrever estado/lock em {runs} :: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
