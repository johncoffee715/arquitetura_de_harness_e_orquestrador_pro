#!/usr/bin/env python3
# alucination_probe.py — identifica o limiar de degradação/alucinação por janela de contexto
# Protocolo: needle-in-haystack progressivo (R28: veredito binário com evidência)
# Alvos: 100K · 131K · 146K · 160K · 180K · 200K tokens
# Métricas: recall por profundidade (5/25/50/75/95%) + detector de invenção
import json
import random
import re
import sys
import time
import urllib.request

BASE = "http://127.0.0.1:8083"
TARGETS = [int(t) for t in __import__("os").environ.get("PROBE_TARGETS", "100000,128000,146000,160000").split(",")]
DEPTHS = [float(d) for d in __import__("os").environ.get("PROBE_DEPTHS", "0.05,0.25,0.50,0.75,0.95").split(",")]
GHOST_KEY = "NEEDLE-FANTASMA"
OUT_JSONL = "/mnt/dados/Assistente Pessoal/opencode/state/watcher/probe-results.jsonl"

TOPICS = [
    "compiladores e otimização de loops intermediários",
    "protocolos de transporte com retransmissão seletiva",
    "sistemas de arquivos copy-on-write e snapshots",
    "algoritmos de consenso em redes assíncronas",
    "quantização de pesos em inferência local",
    "gerenciadores de janelas e composição gráfica",
    "indexação invertida em motores de busca",
    "virtualização assistida por hardware",
    "compressão dicionário-based em tempo real",
    "agendamento de processos em tempo compartilhado",
]

rng = random.Random(424242)


def post(path, payload, timeout=4500):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def count_tokens(text):
    return len(post("/tokenize", {"content": text})["tokens"])


def make_paragraph(i):
    t = TOPICS[i % len(TOPICS)]
    filler = " ".join(rng.choice(TOPICS) for _ in range(6))
    return (
        f"Parágrafo {i:06d}: a discussão sobre {t} exige considerar {filler}. "
        f"A implementação correta depende de tradeoffs entre latência, memória e "
        f"throughput, validados por crivo empírico antes da adoção em produção."
    )


def make_needles():
    needles = []
    for d in DEPTHS:
        key = f"NEEDLE-{int(d*100):03d}"
        val = (f"{rng.randrange(10, 99)}{chr(65 + rng.randrange(26))}-"
               f"{rng.randrange(100, 999)}-{chr(65 + rng.randrange(26))}{chr(65 + rng.randrange(26))}")
        needles.append((key, val))
    return needles


def build_doc(target_tokens):
    """Documento com ~target_tokens tokens; needles inseridos nas profundidades."""
    # razão chars/token medida numa amostra real (evita overshoot)
    sample = make_paragraph(0)
    ratio = len(sample) / count_tokens(sample)
    need_chars = int(target_tokens * ratio * 0.98)
    paras = []
    total = 0
    i = 0
    while total < need_chars:
        p = make_paragraph(i)
        paras.append(p)
        total += len(p) + 2
        i += 1
    body = "\n\n".join(paras)

    needles = make_needles()
    header = "DOCUMENTO DE AUDITORIA TÉCNICA — LEIA ATENTAMENTE.\n\n"
    doc_parts = body.split("\n\n")
    total_chars = sum(len(p) + 2 for p in doc_parts)
    cum = 0
    boundaries = []
    for p in doc_parts:
        cum += len(p) + 2
        boundaries.append(cum)
    insertions = {}
    for i, (key, val) in enumerate(needles):
        target_char = int(total_chars * DEPTHS[i])
        line_no = min(range(len(boundaries)), key=lambda k: abs(boundaries[k] - target_char))
        insertions[line_no] = f"\nREGISTRO-AUDITORIA {key}: {val}.\n"
    out = [header]
    for idx, p in enumerate(doc_parts):
        out.append(p)
        if idx in insertions:
            out.append(insertions[idx])
    text = "".join(out)
    return text, needles


def trim_to_target(text, target_tokens):
    """Corta o final para ficar ≤ alvo (preserva needles, que estão no corpo)."""
    n = count_tokens(text)
    if n <= target_tokens:
        return text, n
    cut = text[: int(len(text) * target_tokens / n)]
    for _ in range(6):
        n = count_tokens(cut)
        if n <= target_tokens:
            break
        cut = cut[: int(len(cut) * target_tokens / n)]
    last_nl = cut.rfind("\n")
    return cut[:last_nl], count_tokens(cut[:last_nl])


def ask(question, doc_text, max_tokens=64):
    payload = {
        "messages": [
            {"role": "system", "content": "Você responde de forma literal e curta, apenas com base no documento."},
            {"role": "user", "content": doc_text + "\n\nPERGUNTA: " + question},
        ],
        "max_tokens": max_tokens,
        "temperature": 0,
        "cache_prompt": True,
    }
    r = post("/v1/chat/completions", payload)
    return r["choices"][0]["message"]["content"].strip()


def main():
    results = open(OUT_JSONL, "a", encoding="utf-8")
    verdict = {}
    done_sizes = set()
    try:
        for line in open(OUT_JSONL.replace(".jsonl", ".jsonl"), encoding="utf-8"):
            r = json.loads(line)
            if "size" in r:
                done_sizes.add(round(r["size"], -3))
    except FileNotFoundError:
        pass
    import os as _os
    if _os.environ.get("PROBE_TARGETS"):
        pending = list(TARGETS)   # override explícito = intenção de re-teste
    else:
        pending = [t for t in TARGETS if not any(abs(t - ds) < 12000 for ds in done_sizes)]
    for target in pending:
        print(f"[probe] construindo doc ~{target} tokens...", flush=True)
        t0 = time.time()
        raw, needles = build_doc(target)
        doc, actual = trim_to_target(raw, target)
        print(f"[probe] doc pronto: {actual} tokens ({time.time()-t0:.0f}s) — prefill na 1ª pergunta", flush=True)

        size_res = {"target": target, "actual_tokens": actual, "needles": []}
        first = True
        invented = False
        misses = 0
        for key, val in needles:
            q = (f"Qual é exatamente o valor do REGISTRO-AUDITORIA com chave {key}? "
                 f"Responda APENAS o valor.")
            ans = ask(q, doc)
            ok = val.upper() in ans.upper()
            if not ok:
                misses += 1
            size_res["needles"].append({"key": key, "expected": val, "answer": ans, "recall_ok": ok})
            results.write(json.dumps({"ts": time.strftime("%FT%T"), **size_res["needles"][-1], "size": actual}) + "\n")
            results.flush()
            if first:
                print(f"[probe] prefill concluído; recall {key}: {'OK' if ok else 'MISS'}", flush=True)
                first = False
            else:
                print(f"[probe] recall {key}: {'OK' if ok else 'MISS'}", flush=True)

        qg = (f"Qual é o valor do REGISTRO-AUDITORIA com chave {GHOST_KEY}? "
              f"Se essa chave NÃO existir no documento, responda exatamente: AUSENTE")
        gans = ask(qg, doc)
        ghost_ok = "AUSENTE" in gans.upper() and len(gans) < 40
        if not ghost_ok:
            invented = True
        size_res["ghost_answer"] = gans
        size_res["ghost_ok"] = ghost_ok
        results.write(json.dumps({"ts": time.strftime("%FT%T"), "size": actual, "ghost_key": GHOST_KEY, "answer": gans, "ghost_ok": ghost_ok}) + "\n")
        results.flush()

        degraded = misses > 0 or invented
        verdict[target] = {"misses": misses, "invented": invented, "degraded": degraded}
        print(f"[probe] === {actual} tok → misses={misses}/5 invented={invented} ⇒ {'DEGRADADO' if degraded else 'ÍNTEGRO'}", flush=True)

    limiar = next((t for t in TARGETS if verdict[t]["degraded"]), None)
    summary = {
        "veredito": f"LIMIAR_EM_{limiar}" if limiar else "INTEGRO_ATE_200K",
        "limiar_alucinacao_ctx": limiar,
        "por_tamanho": verdict,
        "modelo": "Ornith-1.5-9B-Q5_K_M @163840 K=q5_0 V=q5_0 sem context-shift sem fa",
    }
    with open("/mnt/dados/Assistente Pessoal/opencode/state/watcher/probe-verdict.json", "w") as f:
        json.dump(summary, f, indent=1, ensure_ascii=False)
    print("[probe] VEREDITO:", json.dumps(summary, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
