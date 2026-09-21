#!/mnt/dados/opencode/harness/needle-env/bin/python
"""F4 Dispatcher L0 v4 (helenizado): leitura · busca · escrita · listagem via Needle 2.
Catálogo dinâmico ≤5 via vector_cache_surrogate (SQLite/cosseno) · escalão por confidence."""
import json, sys, re, math
import needle

DB = "/mnt/dados/opencode/harness/context_memory.db"
INDEX = "/mnt/dados/opencode/harness/needle_tool_index.bin"
FATOS = ("date: 2026-08-24\nlocale: pt-BR\ndevice: x99-harness-mi50\n"
         "network: local-only\nassistant: needle-dispatch L0")

@needle.tool
def run_shell(command: str):
    "Executa comando shell no host e retorna stdout."
    import subprocess
    r = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
    return {"stdout": r.stdout[:2000], "stderr": r.stderr[:500], "code": r.returncode}

@needle.tool
def read_file(path: str):
    "Lê arquivo texto do host (até 4000 chars)."
    try:
        return {"content": open(path, encoding="utf-8", errors="replace").read()[:4000]}
    except Exception as e:
        return {"error": str(e)}

@needle.tool
def write_file(path: str, content: str):
    "Escreve conteúdo em arquivo no host."
    open(path, "w", encoding="utf-8").write(content)
    return {"written": len(content), "path": path}

@needle.tool
def list_dir(path: str = "."):
    "Lista diretório com tamanhos em bytes."
    import os
    return {f: os.path.getsize(os.path.join(path, f)) for f in os.listdir(path)[:50]}

@needle.tool
def search_files(dir_path: str, name_pattern: str):
    "Busca arquivos por padrão de nome (glob) num diretório, retorna caminhos."
    import glob as g, os
    hits = g.glob(os.path.join(dir_path, name_pattern))[:40]
    return {"hits": sorted(hits)[:40], "total": len(hits)}

@needle.tool
def grep_content(file_path: str, termo: str):
    "Busca um termo dentro de um arquivo texto, retorna linhas com número de linha."
    try:
        linhas = [f"{i+1}: {l.rstrip()[:200]}" for i, l in enumerate(open(file_path, encoding='utf-8', errors='replace')) if termo.lower() in l.lower()]
        return {"matches": linhas[:30], "total": len(linhas)}
    except Exception as e:
        return {"error": str(e)}

IMPLEMENTADOS = {t.__name__: t for t in [run_shell, read_file, write_file, list_dir,
                                          search_files, grep_content]}

def recuperar_top5(query):
    import sqlite3
    tok = lambda s: set(re.findall(r"[a-z0-9_]{2,}", s.lower()))
    qt = tok(query); out = []
    con = sqlite3.connect(DB)
    for nome, intent, tags, fase, ej in con.execute(
            "SELECT name,intent,tags,fase,embedding_json FROM vector_cache_surrogate"):
        et = set(json.loads(ej)); inter = qt & et
        cos = len(inter)/math.sqrt(len(qt)*len(et)) if qt and et else 0
        out.append((cos, nome))
    out.sort(reverse=True)
    return [(n, IMPLEMENTADOS.get(n)) for _, n in out[:5]]

if __name__ == "__main__":
    tarefa = sys.stdin.read().strip()
    if not tarefa:
        print(json.dumps({"escalate": True, "motivo": "entrada vazia"})); sys.exit(1)
    top5 = recuperar_top5(tarefa)
    usaveis = [(n, f) for n, f in top5 if f]
    if not usaveis:
        print(json.dumps({"escalate": True, "motivo": "nenhum dos top-5 implementado",
                          "top5": [n for _, n in top5]})); sys.exit(1)
    agente = needle.Needle(tools=[f for _, f in usaveis], system=FATOS,
                           tool_index_path="/mnt/dados/opencode/harness/needle_tool_index.bin")
    try:
        resp = agente.run(tarefa)
        res = resp.get("results")
        if not res:
            print(json.dumps({"escalate": True,
                              "motivo": "confiança baixa/off-topic — rotear ao Orquestrador",
                              "catalogo_ativo": [n for n, _ in usaveis]})); sys.exit(1)
        print(json.dumps({"results": res, "catalogo_ativo": [n for n, _ in usaveis],
                          "response": str(resp.get("response", ""))[:600]}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"escalate": True, "motivo": str(e)[:120]})); sys.exit(1)
