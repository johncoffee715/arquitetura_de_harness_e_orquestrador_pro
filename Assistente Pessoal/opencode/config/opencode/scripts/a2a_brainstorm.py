#!/usr/bin/env python3
"""
A2A BRAINSTORM — Loop de refutação incansável com nota retroativa (R40/R34).

REDESIGN 2026-08-31 (diretriz usuário):
- SEM árbitro externo no loop (Judge-3B era caro p/ escolha binária).
- Os próprios LLMs se refutam incansavelmente (R40).
- A nota inicial alimenta retroativamente cada rodada (alimento de aprendizado).
- Notas recalibradas HOMEOPÁTICAS: piso real 0.0000001, delta +1..+3 por melhoria
  real (nunca salto grande). Convergência em limiar BAIXO (30.0) + impressão real.
- Judge-3B (escalacao) só em IMPASSE final (Suprema Corte opcional — coexistência justificada).

Papéis: Propositor (Qwen-4B) · Refutador (Ternary-8B) · Refutador Ágil (Gemma-2-2B) ·
Reflexo (LFM-1.2B, opinião verbal) · Ingestor (ingestor, contexto) · Escalação (Judge-3B, raro).
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

# Papéis (R75 — bindings por categoria)
TRIADE = {
    "propositor": {"port": 9088, "model": "proposer-distill", "temp": 0.6, "max_tokens": 1024},
    "refutador": {"port": 9090, "model": "refuter", "temp": 0.8, "max_tokens": 512},
    "refutador_agil": {"port": 9092, "model": "gemma-2-2b-it", "temp": 0.8, "max_tokens": 512},
    "reflexo": {"port": 9086, "model": "reflexo", "temp": 0.8, "max_tokens": 256},
    "ingestor": {"port": 9084, "model": "ingestor-instruct", "temp": 0.1, "max_tokens": 256},
    "escalacao": {"port": 9092, "model": "gemma-2-2b-it", "temp": 0.8, "max_tokens": 512},
}

# Constantes recalibradas — homeopatia real (R34, piso 0.0000001)
NOTA_INICIAL = 0.0000001     # piso real — nada é perfeito
LIMIAR_CONVERGENCIA = 30.0   # recalibrado (era 70 — inflado); convergência BAIXA + impressão
MAX_ROUNDS = 10              # teto de segurança (refutação incansável com trava anti-loop)
DELTA_ACEITO = 1.0           # subida homeopática mínima por rodada (melhoria real)

PROPOSITOR_SYS = (
    "Você é o Propositor (Criador) no loop A2A. Gere/reescreva a proposta com base nas "
    "refutações recebidas. Responda apenas com a proposta (plano, código ou extração)."
)
REFUTADOR_SYS = (
    "Você é o Refutador (Crítico) no loop A2A. Inspecione a proposta buscando falhas lógicas, "
    "desvios de contrato e gargalos. Seja implacável: tente QUEBRAR a ideia. "
)
REFUTADOR_AGIL_SYS = (
    "Você é o Refutador Ágil no loop A2A. Analise a proposta com lógica rigorosa: aponte "
    "falhas matemáticas, lógicas e de consistência. Seja conciso. 2-3 pontos."
)
REFLEXO_SYS = (
    "Você é o Reflexo no loop A2A. Dê um palpite rápido e verbal: a proposta é sólida ou a "
    "refutação procede? 1-2 frases."
)
ESCALACAO_SYS = (
    "Você é a Suprema Corte (Árbitro Final). O debate não convergiu após refutação "
    "incansável. Analise o histórico e emita a DECISÃO FINAL: a proposta é aceitável "
    "(PASSOU) ou é rejeitada (REJEITADA)? Responda apenas: PASSOU ou REJEITADA."
)

# GBNF — refutador avalia com delta homeopático + impressão (JSON estrito)
REFUTADOR_GRAMMAR = (
    'root ::= "{" "\\"delta\\":" " " int " " " "," " " "\\"impresso\\":" " " bool " " " "}"\n'
    'int ::= "-"? [0-3]\n'
    'bool ::= "true" | "false"'
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
        payload["grammar"] = grammar
    req = urllib.request.Request(
        f"http://127.0.0.1:{cfg['port']}/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    timeout = 600 if papel == "escalacao" else 300
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
        return {"ok": True, "content": data["choices"][0]["message"]["content"]}
    except (urllib.error.URLError, KeyError, json.JSONDecodeError) as e:
        return {"ok": False, "error": str(e)}


def parse_avaliacao(raw: str) -> dict:
    """Parse do JSON estrito (GBNF) do Refutador: delta homeopático + impresso."""
    try:
        d = json.loads(raw)
        return {"delta": int(d.get("delta", 0)), "impresso": bool(d.get("impresso", False))}
    except (json.JSONDecodeError, ValueError, TypeError):
        # Fallback tolerante
        if "impresso" in raw and "true" in raw:
            return {"delta": 1, "impresso": True}
        return {"delta": 0, "impresso": False}


def escalar_35b_assincrono(topic: str, contrato: str, historico: list) -> str:
    """Enfileira histórico para o 35B (fila não-bloqueante — best-effort)."""
    try:
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
        return f"ESCALADO — enfileirado para 35B (assíncrono): {arquivo}"
    except Exception as e:
        return f"ESCALADO — fila 35B falhou (best-effort): {e}"


def brainstorm(topic: str, contrato: str = "") -> dict:
    """Loop de refutação incansável com nota retroativa (alimento de aprendizado)."""
    historico = []
    rodadas = []
    nota = NOTA_INICIAL
    proposta = ""
    converged = False
    escalado = False
    decisao = ""
    motivo_parada = ""

    # Rodada 0: Propositor gera proposta v1 (nota inicial como alimento)
    ctx = f"TÓPICO: {topic}\nCONTRATO: {contrato or '(sem contrato — escopo livre)'}\nNOTA ATUAL: {nota} (piso — precisa subir com qualidade)"
    r = chamar_slot("propositor", [
        {"role": "system", "content": PROPOSITOR_SYS},
        {"role": "user", "content": ctx},
    ])
    if not r["ok"]:
        return {"status": "ERRO", "error": f"propositor offline: {r['error']}"}
    proposta = r["content"]
    historico.append({"round": 0, "papel": "propositor", "content": proposta})

    for rodada in range(1, MAX_ROUNDS + 1):
        # 1. Refutador (Ternary) ataca — nota atual alimenta o prompt (retroativo)
        r = chamar_slot("refutador", [
            {"role": "system", "content": REFUTADOR_SYS},
            {"role": "user", "content": (
                f"PROPOSTA:\n{proposta[:2000]}\n\nCONTRATO: {contrato or '(livre)'}\n"
                f"NOTA ATUAL: {nota:.4f} — se a proposta tem falhas, a nota NÃO deve subir."
            )},
        ])
        refutacao = r["content"] if r["ok"] else f"[refutador offline: {r.get('error')}]"
        historico.append({"round": rodada, "papel": "refutador", "content": refutacao})

        # 2. Refutador Ágil (Gemma) — 2ª voz crítica
        r_agil = chamar_slot("refutador_agil", [
            {"role": "system", "content": REFUTADOR_AGIL_SYS},
            {"role": "user", "content": f"PROPOSTA:\n{proposta[:2000]}\n\nCONTRATO: {contrato or '(livre)'}"},
        ])
        refutacao_agil = r_agil["content"] if r_agil["ok"] else ""
        if refutacao_agil:
            historico.append({"round": rodada, "papel": "refutador_agil", "content": refutacao_agil[:600]})

        # 3. Propositor corrige (responde às refutações — nota como alimento)
        r = chamar_slot("propositor", [
            {"role": "system", "content": PROPOSITOR_SYS},
            {"role": "user", "content": (
                f"Reescreva a proposta corrigindo TODOS os pontos.\n"
                f"PROPOSTA ANTERIOR:\n{proposta[:1500]}\n\n"
                f"REFUTAÇÃO (Ternary):\n{refutacao[:1500]}\n\n"
                f"REFUTAÇÃO ÁGIL (Gemma):\n{refutacao_agil[:1000]}\n\n"
                f"NOTA ATUAL: {nota:.4f} — sua correção deve JUSTIFICAR subir a nota."
            )},
        ])
        if r["ok"]:
            proposta = r["content"]
            historico.append({"round": rodada, "papel": "propositor", "content": proposta})

        # 4. Refutador avalia a correção (GBNF: delta homeopático + impressão)
        r = chamar_slot("refutador", [
            {"role": "system", "content": (
                "Você é o avaliador do loop A2A. Compare a proposta CORRIGIDA com as "
                "refutações anteriores. Atribua um DELTA homeopático: +1 a +3 se as "
                "refutações foram endereçadas (subida lenta), 0 se estagnou, negativo se "
                "regrediu. 'impresso': true APENAS se ficou genuinamente impressionado."
            )},
            {"role": "user", "content": f"PROPOSTA CORRIGIDA:\n{proposta[:2000]}\n\nREFUTAÇÕES:\n{refutacao[:1000]}\n{refutacao_agil[:600]}"},
        ], grammar=REFUTADOR_GRAMMAR)
        if not r["ok"]:
            return {"status": "ERRO", "error": f"refutador avaliação offline: {r['error']}"}
        avaliacao = parse_avaliacao(r["content"])
        delta = avaliacao["delta"]
        impresso = avaliacao["impresso"]

        # 5. Nota evolui homeopaticamente (retroativo — alimento da próxima rodada)
        nota_anterior = nota
        nota = max(0.0000001, nota + delta)  # piso real, nunca negativo
        rodadas.append({
            "round": rodada, "nota": nota, "delta": delta,
            "impresso": impresso, "nota_anterior": nota_anterior,
        })

        # Convergência: nota ≥ limiar BAIXO + impressão real (R40)
        if nota >= LIMIAR_CONVERGENCIA and impresso:
            converged = True
            motivo_parada = f"convergência: nota {nota:.2f} ≥ {LIMIAR_CONVERGENCIA} + impressão real"
            break

        # Estagnação (delta < mínimo aceito) → impasse real
        if delta < DELTA_ACEITO and len(rodadas) >= 2:
            motivo_parada = f"estagnação: delta {delta} < {DELTA_ACEITO} na rodada {rodada}"
            break

    # Escalação (apenas em impasse — Judge-3B Suprema Corte, coexistência justificada)
    if not converged:
        escalado = True
        r = chamar_slot("escalacao", [
            {"role": "system", "content": ESCALACAO_SYS},
            {"role": "user", "content": (
                f"TÓPICO: {topic}\n\nHISTÓRICO COMPILADO:\n"
                + json.dumps(historico[-4:], ensure_ascii=False, indent=1)[:2500]
            )},
        ], grammar='root ::= "PASSOU" | "REJEITADA"')
        decisao = r["content"] if r["ok"] else f"[escalação offline: {r.get('error')}]"
        escalar_35b_assincrono(topic, contrato, historico)  # best-effort

    media = sum(rd["nota"] for rd in rodadas) / len(rodadas) if rodadas else NOTA_INICIAL

    return {
        "status": "SUCCESS",
        "topic": topic,
        "rounds": len(rodadas),
        "converged": converged,
        "escalated_to_35b": escalado,
        "nota_final": round(nota, 5),
        "nota_media": round(media, 5),
        "motivo_parada": motivo_parada,
        "verdict": "PASSOU_CATEGORICO" if converged else "ESCALADO",
        "proposal_final": proposta[:2000],
        "rounds_detail": rodadas,
        "escalation_decision": decisao if escalado else None,
    }


def main():
    parser = argparse.ArgumentParser(description="A2A Brainstorm — refutação incansável com nota retroativa")
    parser.add_argument("topic", nargs="?", help="tópico do brainstorm")
    parser.add_argument("--contrato", default="", help="contrato/spec.md (opcional)")
    parser.add_argument("--json", action="store_true", help="saída JSON pura")
    args = parser.parse_args()

    if not args.topic:
        parser.print_help()
        return 1

    result = brainstorm(args.topic, args.contrato)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"TÓPICO: {result.get('topic')}")
        print(f"RODADAS: {result.get('rounds')} | CONVERGIU: {result.get('converged')} | ESCALADO: {result.get('escalated_to_35b')}")
        print(f"NOTA FINAL: {result.get('nota_final')} | MÉDIA: {result.get('nota_media')} | VEREDITO: {result.get('verdict')}")
        print(f"PARADA: {result.get('motivo_parada')}")
        for rd in result.get("rounds_detail", []):
            print(f"  R{rd['round']}: delta={rd['delta']} nota={rd['nota']:.4f} impresso={rd['impresso']}")
    return 0 if result.get("status") == "SUCCESS" else 1


if __name__ == "__main__":
    sys.exit(main())