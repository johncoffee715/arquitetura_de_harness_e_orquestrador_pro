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
from pathlib import Path

# Tríade fixa (R75 — bindings por categoria, slots reais)
# Escalação: Judge-3B (rápido 152 t/s) — 35B é EXCLUSIVO de orquestração (R46:
# dois 35B em RAM = ~40GB + contenção DDR; nunca usar 35B para outras funções)
# Reflexo (LFM-1.2B) e Ingestor (RWKV7) são papéis opcionais de apoio (R42)
TRIADE = {
    "propositor": {"port": 9088, "model": "qwen3.8-4b-distill", "temp": 0.6, "max_tokens": 1024},
    "refutador": {"port": 9090, "model": "ternary-bonsai-8b", "temp": 0.8, "max_tokens": 512},
    "refutador_agil": {"port": 9092, "model": "gemma-2-2b-it", "temp": 0.8, "max_tokens": 512},
    "arbitro": {"port": 9085, "model": "llmjudge-qwen2.5-3b", "temp": 0.15, "max_tokens": 256},
    "escalacao": {"port": 9085, "model": "llmjudge-qwen2.5-3b", "temp": 0.15, "max_tokens": 512},
    "reflexo": {"port": 9086, "model": "lfm2.5-1.2b-thinking-tomoe", "temp": 0.8, "max_tokens": 256},
    "ingestor": {"port": 9084, "model": "rwkv7-g1d-0.4b-instruct", "temp": 0.1, "max_tokens": 256},
}

MAX_ROUNDS = 12         # alta velocidade GPU (R42) — teto de segurança; critério real é progresso
CONVERGENCIA = 75.0     # R34 recalibrado homeopático: média > 75 encerra (era 95 — inflado)
IMPRESSAO = 70.0        # R40 recalibrado: nota ≥ 70 + elogios (era 90 — inflado)
PROGRESSO_MIN = 5.0     # subida homeopática mínima por rodada (nota baixa gradativa)

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
    "Compare as duas opções apresentadas (OPÇÃO 1 e OPÇÃO 2) e decida qual é mais "
    "correta, considerando falhas lógicas, desvios de contrato e gargalos. "
    "Seja CRÍTICO: não aprove por padrão — examine se a opção tem falhas reais. "
    "Responda APENAS com: winner_model_1 (se a OPÇÃO 1 vence) ou winner_model_2 "
    "(se a OPÇÃO 2 vence). Nada mais."
)
ESCALACAO_SYS = (
    "Você é a Suprema Corte (Árbitro Final). O debate entre Propositor e Refutador "
    "não convergiu. Analise o histórico compilado e emita a DECISÃO FINAL: "
    "escolha entre a proposta (winner_model_a) ou a refutação (winner_model_b), "
    "com justificativa curta. Responda APENAS com winner_model_a ou winner_model_b "
    "seguido de 1-2 frases de justificativa."
)


def chamar_slot(papel: str, messages: list, grammar: str | None = None) -> dict:
    """Chama um slot llama.cpp via API OpenAI-compatible."""
    cfg = TRIADE[papel]
    payload = {
        "messages": messages,
        "temperature": cfg["temp"],
        "max_tokens": cfg["max_tokens"],
    }
    if grammar:
        payload["grammar"] = grammar  # GBNF — restrição na camada de amostragem (frente 1)
    req = urllib.request.Request(
        f"http://127.0.0.1:{cfg['port']}/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    # Escalação (35B CPU) é lenta — timeout generoso; tríade GPU 180s
    timeout = 600 if papel == "escalacao" else 300
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
        return {"ok": True, "content": data["choices"][0]["message"]["content"]}
    except (urllib.error.URLError, KeyError, json.JSONDecodeError) as e:
        return {"ok": False, "error": str(e)}


# GBNF — gramática estrita para o Árbitro (frente 1: restrição na amostragem)
ARBITRO_GRAMMAR = 'root ::= "winner_model_1" | "winner_model_2"'


def parse_arbitro(raw: str, rodada: int = 1) -> dict:
    """Converte a escolha emparelhada do Judge (winner_model_1/2) em veredito R34.

    Com GBNF (ARBITRO_GRAMMAR), o output é ESTRITO — sem ruído, parse determinístico.
    Alternância de ordem (rodada ímpar: 1=proposta, 2=refutação; par: invertido)
    elimina viés de posição.
    Mapeamento recalibrado homeopático (R34 — notas baixas gradativas, piso real):
    proposta vence → nota 70 (avança se elogios); refutação procede → nota 45.
    """
    raw_l = raw.strip().lower()
    proposta_venceu = None
    if "winner_model_1" in raw_l:
        proposta_venceu = (rodada % 2 == 1)  # ímpar: opção 1 = proposta
    elif "winner_model_2" in raw_l:
        proposta_venceu = (rodada % 2 == 0)  # par: opção 2 = proposta
    elif "winner_model_a" in raw_l:
        proposta_venceu = True  # compat legado
    elif "winner_model_b" in raw_l:
        proposta_venceu = False  # compat legado

    if proposta_venceu is True:
        return {"nota": 70.0, "bugs": [], "elogios": ["proposta venceu o embate"],
                "procede_refutacao": False, "veredito": "PASSOU_CATEGORICO"}
    if proposta_venceu is False:
        return {"nota": 45.0, "bugs": ["refutação procede — proposta precisa reescrever"],
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

        # Refutador Ágil (Gemma-2-2B) — 2ª voz crítica (lógica/matemática, diversidade Google)
        r_agil = chamar_slot("refutador_agil", [
            {"role": "system", "content": "Você é o Refutador Ágil no loop A2A. Analise a proposta com lógica rigorosa: aponte falhas matemáticas, lógicas e de consistência. Seja conciso e específico. 2-3 pontos."},
            {"role": "user", "content": f"PROPOSTA:\n{proposta[:2000]}\n\nCONTRATO: {contrato or '(livre)'}"},
        ])
        refutacao_agil = r_agil["content"] if r_agil["ok"] else ""
        if refutacao_agil:
            historico.append({"round": rodada, "papel": "refutador_agil", "content": refutacao_agil[:600]})

        # Reflexo (LFM-1.2B) — segunda opinião rápida (R42, fail-open)
        r_reflexo = chamar_slot("reflexo", [
            {"role": "system", "content": "Você é o Reflexo no loop A2A. Dê um palpite rápido e verbal sobre o embate: a proposta é sólida ou a refutação procede? 1-2 frases."},
            {"role": "user", "content": f"PROPOSTA:\n{proposta[:1500]}\n\nREFUTAÇÃO:\n{refutacao[:1500]}"},
        ])
        opiniao_reflexo = r_reflexo["content"] if r_reflexo["ok"] else ""
        if opiniao_reflexo:
            historico.append({"round": rodada, "papel": "reflexo", "content": opiniao_reflexo[:500]})

        # Árbitro decide — alterna ordem (elimina viés de posição: 1ª opção tende a vencer)
        if rodada % 2 == 1:
            op1, op2 = f"PROPOSTA:\n{proposta}", f"REFUTAÇÃO:\n{refutacao}"
        else:
            op1, op2 = f"REFUTAÇÃO:\n{refutacao}", f"PROPOSTA:\n{proposta}"
        r = chamar_slot("arbitro", [
            {"role": "system", "content": ARBITRO_SYS},
            {"role": "user", "content": f"OPÇÃO 1:\n{op1}\n\nOPÇÃO 2:\n{op2}"
             + (f"\n\nREFUTAÇÃO ÁGIL (Gemma): {refutacao_agil[:500]}" if refutacao_agil else "")
             + (f"\n\nOPINIÃO DO REFLEXO: {opiniao_reflexo[:500]}" if opiniao_reflexo else "")},
        ], grammar=ARBITRO_GRAMMAR)
        if not r["ok"]:
            return {"status": "ERRO", "error": f"árbitro offline: {r['error']}"}
        veredito = parse_arbitro(r["content"], rodada)
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
        if nota >= IMPRESSAO and veredito.get("elogios"):
            converged = True
            nota_final = nota
            break

        # Progresso gradativo (homeopatia R34): nota deve SUBIR ≥ PROGRESSO_MIN
        # por rodada. Se estagnar/regredir → para e escala (não força loop).
        if len(rodadas) >= 2:
            nota_anterior = rodadas[-2]["nota"]
            if nota <= nota_anterior + PROGRESSO_MIN * 0.5:
                break  # sem progresso homeopático → impasse real

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

    # Escalação: Judge-3B (Suprema Corte local, rápida) + fila assíncrona p/ 35B (frente 3)
    if not converged:
        escalado = True
        r = chamar_slot("escalacao", [
            {"role": "system", "content": ESCALACAO_SYS},
            {"role": "user", "content": (
                f"TÓPICO: {topic}\n\nHISTÓRICO COMPILADO:\n"
                + json.dumps(historico[-4:], ensure_ascii=False, indent=1)[:3000]
            )},
        ])
        decisao = r["content"] if r["ok"] else f"[escalação offline: {r.get('error')}]"
        # Enfileira para o 35B processar em background (não-bloqueante)
        try:
            escalar_35b_assincrono(topic, contrato, historico)
        except Exception:
            pass  # fila é best-effort
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


def escalar_35b_assincrono(topic: str, contrato: str, historico: list) -> str:
    """Frente 3 — escalação assíncrona para o 35B (fila não-bloqueante).

    O 35B é exclusivo de orquestração (R46) — a escalação padrão é o Judge-3B.
    Esta função ENFILEIRA o histórico para o 35B processar em background
    (quando o orquestrador estiver ocioso), sem bloquear o loop A2A.
    """
    fila = Path("/tmp/opencode/a2a-escalacao-35b")
    fila.mkdir(parents=True, exist_ok=True)
    arquivo = fila / f"{abs(hash(topic)) % 100000}.json"
    hist_curto = []
    for h in historico[-4:]:
        c = h["content"]
        hist_curto.append({"round": h["round"], "papel": h["papel"],
                           "content": c[:400] + ("…" if len(c) > 400 else "")})
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump({"topic": topic, "contrato": contrato, "historico": hist_curto},
                  f, ensure_ascii=False, indent=2)
    return (f"ESCALADO — histórico enfileirado para o 35B (assíncrono): {arquivo}. "
            "Decisão padrão já emitida pelo Judge-3B (Suprema Corte local).")


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