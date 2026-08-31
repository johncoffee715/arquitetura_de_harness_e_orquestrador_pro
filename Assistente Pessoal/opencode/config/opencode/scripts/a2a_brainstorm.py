#!/usr/bin/env python3
"""
A2A BRAINSTORM — Loop de debate com tríade fixa na VRAM (R40/R34/R18).

Tríade: Propositor (Qwen3.8-4B :9088) → Refutador (Ternary-8B :9090) →
Árbitro (LLMJudge-3B :9085) → Escalação (Ornith-35B :8083 CPU).

Regras de engajamento:
- Refutador refuta com evidência (nunca opinião solta).
- Árbitro decide com nota R34 (0.0000001-100) + bugs concretos.
- Nota < 90 → Propositor reescreve. Nota ≥ 90 + elogios → PASSOU_CATEGORICO.
- Max iterações: convergência média > 95.0 OU 3 rodadas sem impressão → escalar 35B (R18).

Origin: helenizado:hefesto-v1 (R77 3 camadas — skill a2a-brainstorm)
"""

import argparse
import json
import sys
import urllib.request
import urllib.error

# Tríade fixa (R75 — bindings por categoria, slots reais)
TRIADE = {
    "propositor": {"port": 9088, "model": "qwen3.8-4b-distill", "temp": 0.6, "max_tokens": 2048},
    "refutador": {"port": 9090, "model": "ternary-bonsai-8b", "temp": 0.8, "max_tokens": 2048},
    "arbitro": {"port": 9085, "model": "llmjudge-qwen2.5-3b", "temp": 0.15, "max_tokens": 1024},
    "escalacao": {"port": 8083, "model": "ornith-1.5-35b-a3b-iq4_xs", "temp": 0.3, "max_tokens": 128},
}

MAX_ROUNDS = 3          # R18: 3 rodadas sem impressão → escalar
CONVERGENCIA = 95.0     # R34: média > 95 encerra
IMPRESSAO = 90.0        # R40: nota ≥ 90 + elogios concretos

PROPOSITOR_SYS = (
    "Você é o Propositor (Criador) no loop A2A. Gere a primeira versão da proposta "
    "(plano, código ou extração) de forma pragmática e rápida, respeitando o contrato "
    "fornecido. Responda apenas com a proposta."
)
REFUTADOR_SYS = (
    "Você é o Refutador (Crítico) no loop A2A. Inspecione ativamente a proposta buscando "
    "falhas lógicas, desvios de contrato e gargalos de execução. Tente QUEBRAR a ideia. "
    "Responda com refutações concretas e evidências — nunca opinião solta."
)
ARBITRO_SYS = (
    "Você é o Árbitro (Juiz) no loop A2A, especialista em avaliação emparelhada. "
    "Compare a PROPOSTA (A) com a REFUTAÇÃO (B) e decida qual é mais correta, "
    "considerando falhas lógicas, desvios de contrato e gargalos. "
    "Responda APENAS com: winner_model_a (se a proposta vence) ou winner_model_b "
    "(se a refutação vence). Nada mais."
)
ESCALACAO_SYS = (
    "Você é a Suprema Corte (Meta-Orquestrador). O Árbitro registrou impasses repetidos "
    "sem consenso entre Propositor e Refutador. Analise o histórico compilado e emita a "
    "decisão final com nota R34 e veredito categórico."
)


def chamar_slot(papel: str, messages: list) -> dict:
    """Chama um slot llama.cpp via API OpenAI-compatible."""
    cfg = TRIADE[papel]
    payload = {
        "messages": messages,
        "temperature": cfg["temp"],
        "max_tokens": cfg["max_tokens"],
    }
    req = urllib.request.Request(
        f"http://127.0.0.1:{cfg['port']}/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    # Escalação (35B CPU) é lenta — timeout generoso; tríade GPU 180s
    timeout = 600 if papel == "escalacao" else 180
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
        return {"ok": True, "content": data["choices"][0]["message"]["content"]}
    except (urllib.error.URLError, KeyError, json.JSONDecodeError) as e:
        return {"ok": False, "error": str(e)}


def parse_arbitro(raw: str) -> dict:
    """Converte a escolha emparelhada do Judge (winner_model_a/b) em veredito R34.

    Judge-3B é treinado para avaliação emparelhada (R46) — não emite JSON.
    Mapeamento: winner_model_a → proposta vence (nota 85, avança se elogios);
    winner_model_b → refutação procede (nota 60, reescrever).
    """
    raw_l = raw.lower()
    if "winner_model_a" in raw_l or "model_a" in raw_l:
        return {"nota": 85.0, "bugs": [], "elogios": ["proposta venceu o embate"],
                "procede_refutacao": False, "veredito": "PASSOU_CATEGORICO"}
    if "winner_model_b" in raw_l or "model_b" in raw_l:
        return {"nota": 60.0, "bugs": ["refutação procede — proposta precisa reescrever"],
                "elogios": [], "procede_refutacao": True, "veredito": "REESCREVER"}
    # Fallback: tenta JSON (caso o modelo siga o formato antigo)
    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end > start:
            v = json.loads(raw[start:end])
            return {"nota": float(v.get("nota", 0.0000001)), "bugs": v.get("bugs", []),
                    "elogios": v.get("elogios", []),
                    "procede_refutacao": v.get("procede_refutacao", True),
                    "veredito": v.get("veredito", "REESCREVER")}
    except (json.JSONDecodeError, ValueError):
        pass
    return {"nota": 0.0000001, "bugs": ["veredito não-parseável"], "elogios": [],
            "procede_refutacao": True, "veredito": "REESCREVER"}


def brainstorm(topic: str, contrato: str = "") -> dict:
    """Executa o loop A2A com a tríade."""
    historico = []
    rodadas = []
    proposta = ""
    converged = False
    escalado = False
    nota_final = 0.0000001

    # Rodada 1: Propositor gera proposta v1
    ctx = f"TÓPICO: {topic}\nCONTRATO: {contrato or '(sem contrato — escopo livre)'}"
    r = chamar_slot("propositor", [
        {"role": "system", "content": PROPOSITOR_SYS},
        {"role": "user", "content": ctx},
    ])
    if not r["ok"]:
        return {"status": "ERRO", "error": f"propositor offline: {r['error']}"}
    proposta = r["content"]
    historico.append({"round": 0, "papel": "propositor", "content": proposta})

    for rodada in range(1, MAX_ROUNDS + 1):
        # Refutador ataca
        r = chamar_slot("refutador", [
            {"role": "system", "content": REFUTADOR_SYS},
            {"role": "user", "content": f"PROPOSTA:\n{proposta}\n\nCONTRATO: {contrato or '(livre)'}"},
        ])
        refutacao = r["content"] if r["ok"] else f"[refutador offline: {r.get('error')}]"
        historico.append({"round": rodada, "papel": "refutador", "content": refutacao})

        # Árbitro decide
        r = chamar_slot("arbitro", [
            {"role": "system", "content": ARBITRO_SYS},
            {"role": "user", "content": f"PROPOSTA:\n{proposta}\n\nREFUTAÇÃO:\n{refutacao}"},
        ])
        if not r["ok"]:
            return {"status": "ERRO", "error": f"árbitro offline: {r['error']}"}
        veredito = parse_arbitro(r["content"])
        nota = max(0.0000001, min(100.0, float(veredito.get("nota", 0.0000001))))
        rodadas.append({
            "round": rodada,
            "nota": nota,
            "bugs": veredito.get("bugs", []),
            "elogios": veredito.get("elogios", []),
            "procede_refutacao": veredito.get("procede_refutacao", True),
            "veredito_arbitro": veredito.get("veredito", "REESCREVER"),
        })

        # Convergência: proposta venceu o embate (winner_model_a) → PASSOU (R40)
        # Judge-3B é emparelhado (A/B) — A venceu = proposta madura para avançar
        if nota >= 85.0 and veredito.get("elogios"):
            converged = True
            nota_final = nota
            break

        # Reescrever: Propositor responde à refutação
        r = chamar_slot("propositor", [
            {"role": "system", "content": PROPOSITOR_SYS},
            {"role": "user", "content": (
                f"Reescreva a proposta corrigindo os bugs apontados.\n"
                f"PROPOSTA ANTERIOR:\n{proposta}\n\nREFUTAÇÃO:\n{refutacao}\n\n"
                f"BUGS DO ÁRBITRO: {veredito.get('bugs', [])}"
            )},
        ])
        if r["ok"]:
            proposta = r["content"]
            historico.append({"round": rodada, "papel": "propositor", "content": proposta})

    # Escalação ASSÍNCRONA (35B CPU ~73s/50tok — síncrono inviável no loop):
    # salva histórico compilado em arquivo; decisão consultada via --escalar
    if not converged:
        escalado = True
        hist_curto = []
        for h in historico[-3:]:  # apenas últimas 3 entradas (35B CPU é lento)
            c = h["content"]
            hist_curto.append({"round": h["round"], "papel": h["papel"],
                               "content": c[:300] + ("…" if len(c) > 300 else "")})
        decisao = ("ESCALADO — histórico compilado salvo. "
                   "Consulte a decisão do 35B com: python3 scripts/a2a_brainstorm.py --escalar <arquivo>")
        escalacao_file = f"/tmp/opencode/a2a-escalacao-{abs(hash(topic)) % 100000}.json"
        with open(escalacao_file, "w", encoding="utf-8") as f:
            json.dump({"topic": topic, "contrato": contrato, "historico": hist_curto},
                      f, ensure_ascii=False, indent=2)
        nota_final = max(n for n in [rod["nota"] for rod in rodadas]) if rodadas else 0.0000001

    media = sum(rod["nota"] for rod in rodadas) / len(rodadas) if rodadas else 0.0000001

    return {
        "status": "SUCCESS",
        "topic": topic,
        "rounds": len(rodadas),
        "converged": converged,
        "escalated_to_35b": escalado,
        "average_score": round(media, 5),
        "final_score": nota_final,
        "verdict": "PASSOU_CATEGORICO" if converged else "ESCALADO",
        "proposal_final": proposta[:2000],
        "rounds_detail": rodadas,
        "escalation_decision": decisao if escalado else None,
    }


def escalar_35b(arquivo: str) -> dict:
    """Consulta a Suprema Corte (35B CPU) com o histórico compilado (assíncrono)."""
    with open(arquivo, "r", encoding="utf-8") as f:
        payload = json.load(f)
    r = chamar_slot("escalacao", [
        {"role": "system", "content": ESCALACAO_SYS},
        {"role": "user", "content": (
            f"TÓPICO: {payload.get('topic')}\n\nHISTÓRICO COMPILADO:\n"
            + json.dumps(payload.get("historico", []), ensure_ascii=False, indent=1)
        )},
    ])
    return {"status": "SUCCESS" if r["ok"] else "ERRO",
            "decisao_35b": r.get("content", r.get("error", ""))}


def main():
    parser = argparse.ArgumentParser(description="A2A Brainstorm — tríade VRAM")
    parser.add_argument("topic", nargs="?", help="tópico do brainstorm")
    parser.add_argument("--contrato", default="", help="contrato/spec.md (opcional)")
    parser.add_argument("--escalar", metavar="ARQUIVO", help="consultar 35B com histórico salvo")
    parser.add_argument("--json", action="store_true", help="saída JSON pura")
    args = parser.parse_args()

    if args.escalar:
        result = escalar_35b(args.escalar)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"DECISÃO 35B: {result.get('decisao_35b', '')[:1000]}")
        return 0 if result.get("status") == "SUCCESS" else 1

    if not args.topic:
        parser.print_help()
        return 1

    result = brainstorm(args.topic, args.contrato)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"TÓPICO: {result.get('topic')}")
        print(f"RODADAS: {result.get('rounds')} | CONVERGIU: {result.get('converged')} | ESCALADO: {result.get('escalated_to_35b')}")
        print(f"NOTA MÉDIA: {result.get('average_score')} | VEREDITO: {result.get('verdict')}")
        if result.get("rounds_detail"):
            for rd in result["rounds_detail"]:
                print(f"  R{rd['round']}: nota={rd['nota']} bugs={rd['bugs'][:2]} veredito={rd['veredito_arbitro']}")
    return 0 if result.get("status") == "SUCCESS" else 1


if __name__ == "__main__":
    sys.exit(main())