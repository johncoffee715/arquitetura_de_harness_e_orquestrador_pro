#!/usr/bin/env python3
"""Refutação do duelo pelo Conselho local (R40/R75): todos os LLMs aptos julgam.
Entrada: /tmp/opencode/duelo-gmb-lite.jsonl (task, slot, prompt, content).
Alvo: SÓ tarefas disputadas (placar GM 0.5 ou divergência entre contestants).
Jurados serving: 9090 (principal), 9092, 9088, 9086 (reflexo rápido).
Prompt tiny (modelos pequenos!): NOTA 0/0.5/1 + 1 defeito concreto.
Saída: /tmp/opencode/refuta-conselho.jsonl + .done. Sem julgamento próprio:
GM valida (R43) e decide depois. Modo autonomo ON.
Forja: Gran-Mestre 2026-09-07.
"""
import json
import re
import subprocess
import sys

DUEL = "/tmp/opencode/duelo-gmb-lite.jsonl"
OUT = "/tmp/opencode/refuta-conselho.jsonl"
DONE = "/tmp/opencode/refuta-conselho.done"
JUDGES = [9090, 9092, 9088, 9086]

JUDGE_TPL = ("Nota 0, 0.5 ou 1 para a RESPOSTA dada a PERGUNTA, mais 1 defeito "
             "concreto em poucas palavras. Formato exato: NOTA: <n> DEFEITO: <texto>. "
             "PERGUNTA: {q} RESPOSTA: {a}")


def ask(port, prompt, n=60):
    body = {"prompt": prompt[:1500], "n_predict": n, "temperature": 0.0}
    try:
        r = subprocess.run(
            ["curl", "-s", "-m", "150", "-X", "POST",
             f"http://127.0.0.1:{port}/completion",
             "-H", "Content-Type: application/json",
             "-d", json.dumps(body)],
            capture_output=True, text=True, timeout=170)
        return json.loads(r.stdout).get("content", "")
    except Exception as e:  # noqa: BLE001
        return f"[ERRO-JUIZ {e}]"


def parse_verdict(text):
    m = re.search(r"NOTA:\s*(0(?:\.5)?|1(?:\.0)?)", text)
    d = re.search(r"DEFEITO:\s*(.+)", text, re.S)
    nota = float(m.group(1)) if m else -1.0
    return nota, (d.group(1).strip()[:160] if d else "")


def main():
    dispute_file = sys.argv[1] if len(sys.argv) > 1 else None
    rows = [json.loads(l) for l in open(DUEL) if l.strip()]
    by_task = {}
    for r in rows:
        by_task.setdefault(r["task"], []).append(r)
    # Sem lista externa: disputa = tasks onde algum conteúdo difere muito
    # (heurística simples: ambas as respostas existem; o GM filtra depois).
    # Com lista: só essas tasks.
    wanted = set(json.load(open(dispute_file))) if dispute_file else set(by_task)
    out = open(OUT, "w")
    for tid in sorted(wanted & set(by_task)):
        for ans in by_task[tid]:
            q = ans.get("prompt", "")[:400]
            a = (ans.get("content", "") or "")[:800]
            for j in JUDGES:
                txt = ask(j, JUDGE_TPL.format(q=q, a=a))
                nota, defeito = parse_verdict(txt)
                out.write(json.dumps({
                    "task": tid, "contestant": ans.get("slot"),
                    "judge": j, "nota": nota, "defeito": defeito,
                    "raw": txt[:200]}, ensure_ascii=False) + "\n")
                out.flush()
    out.close()
    open(DONE, "w").write("DONE")


if __name__ == "__main__":
    main()
