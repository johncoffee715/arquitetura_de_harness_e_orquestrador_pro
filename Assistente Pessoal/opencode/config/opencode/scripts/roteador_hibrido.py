#!/usr/bin/env python3
"""
ROTEADOR HÍBRIDO L0/L0.5 — Coexistência RWKV7 (semântico) + Needle 2 (sintático).

Implementa o fluxo do documento "RWKV7-0.4B L0.5":
- FASE 0: RWKV7 :9084 classifica a intenção (semântico, 1M ctx, TTFT imediato).
  → comando operacional direto → Needle 2 (L0 sintático) executa payload JSON estrito.
  → raciocínio complexo → roteia para LLMs densos (F1/F2).
- FASE 4: RWKV7 ingere logs longos SEM perda (RNN O(1)) e extrai a causa raiz;
  Needle 2 valida o payload estruturado (schema 100%).

Origin: helenizado: doc RWKV7 L0.5 + Needle L0 (2026-08-31)
"""

import argparse
import json
import sys
import urllib.request
import urllib.error

RWKV_URL = "http://127.0.0.1:9084/v1/chat/completions"
NEEDLE_URL = "http://127.0.0.1:9091/complete"

RWKV_SYSTEM = (
    "Você é o Córtex Cognitivo L0.5 (RWKV7, janela 1M). Classifique a intenção do usuário. "
    "Responda APENAS com JSON: {\"intent\": \"operacional\" | \"complexo\" | \"saudacao\", "
    "\"tipo\": \"mcp\" | \"hook\" | \"cli\" | \"git\" | \"brainstorm\" | \"codigo\" | \"rag\" | \"outro\", "
    "\"confianca\": 0.0-1.0, \"resumo\": \"1 linha\"}"
)

NEEDLE_SYSTEM = (
    "Você é o Enforcer Sintático L0 (Needle 2). Converta a instrução em payload JSON estrito "
    "para acionamento direto de MCP/Hook — 100% schema compliance, zero alucinação de formato."
)

ROTAS_DIRETAS = {"mcp", "hook", "cli", "git"}
ROTAS_COMPLEXAS = {"brainstorm", "codigo", "rag"}


def chamar_rwkv(texto: str) -> dict:
    """RWKV7 :9084 — classificação semântica (Fase 0) com GBNF estrito.

    O RWKV7-0.4B NÃO segue JSON sem grammar (documento L0.5: 'necessita de
    prompting e/ou Grammar-Guided Decoding para 100% conformidade JSON').
    """
    grammar = (
        'root ::= "{" ws "\\"intent\\":" ws intent ws "," ws "\\"tipo\\":" ws tipo '
        'ws "," ws "\\"confianca\\":" ws num ws "," ws "\\"resumo\\":" ws string ws "}"\n'
        'ws ::= " "?\n'
        'intent ::= "\\"operacional\\"" | "\\"complexo\\"" | "\\"saudacao\\""\n'
        'tipo ::= "\\"mcp\\"" | "\\"hook\\"" | "\\"cli\\"" | "\\"git\\"" | "\\"brainstorm\\"" | "\\"codigo\\"" | "\\"rag\\"" | "\\"outro\\""\n'
        'num ::= [0-9] "." [0-9]+\n'
        'string ::= "\\"" [^\\"]* "\\""'
    )
    payload = {
        "messages": [
            {"role": "system", "content": RWKV_SYSTEM},
            {"role": "user", "content": texto[:8000]},
        ],
        "temperature": 0.1,
        "max_tokens": 128,
        "grammar": grammar,
    }
    req = urllib.request.Request(RWKV_URL, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())


def chamar_needle(instrucao: str) -> dict:
    """Needle 2 :9091 — execução sintática (payload JSON estrito)."""
    payload = {"input": f"{NEEDLE_SYSTEM}\nInstrução: {instrucao}"}
    req = urllib.request.Request(NEEDLE_URL, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def parse_intent(raw: str) -> dict:
    """Extrai o JSON da classificação do RWKV7 (tolerante a ruído)."""
    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end > start:
            return json.loads(raw[start:end])
    except json.JSONDecodeError:
        pass
    return {"intent": "complexo", "tipo": "outro", "confianca": 0.0, "resumo": "parse falhou"}


def rotear(texto: str) -> dict:
    """Roteia a entrada pelo fluxo híbrido L0.5 → L0."""
    # FASE 0: RWKV7 classifica
    try:
        r = chamar_rwkv(texto)
        raw = r["choices"][0]["message"]["content"]
        intento = parse_intent(raw)
    except Exception as e:
        intento = {"intent": "complexo", "tipo": "outro", "confianca": 0.0, "resumo": f"rwkv offline: {e}"}

    tipo = intento.get("tipo", "outro")
    intent = intento.get("intent", "complexo")

    # Roteamento
    if intent == "saudacao":
        return {"rota": "direto", "destino": "resposta-local", "intento": intento,
                "payload": {"resposta": "Olá! Como posso ajudar?"}}
    if intent == "operacional" and tipo in ROTAS_DIRETAS:
        # Needle 2 — enforcer sintático (payload JSON estrito)
        try:
            r = chamar_needle(texto)
            return {"rota": "direto", "destino": f"needle-{tipo}", "intento": intento,
                    "payload": r}
        except Exception as e:
            return {"rota": "direto", "destino": f"needle-{tipo} (offline)", "intento": intento,
                    "payload": {"erro": str(e)}}
    # Complexo → LLMs densos (F1/F2)
    return {"rota": "complexo", "destino": "llm-densos (F1/F2)", "intento": intento,
            "payload": {"motivo": "requer raciocínio denso — acionar Qwen/Ornith"}}


def main():
    parser = argparse.ArgumentParser(description="Roteador Híbrido L0/L0.5 (RWKV7 + Needle)")
    parser.add_argument("texto", help="entrada do usuário")
    parser.add_argument("--json", action="store_true", help="saída JSON")
    args = parser.parse_args()

    resultado = rotear(args.texto)
    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    else:
        print(f"ROTA: {resultado['rota']} → {resultado['destino']}")
        print(f"INTENTO: {resultado['intento']}")
        print(f"PAYLOAD: {json.dumps(resultado['payload'], ensure_ascii=False)[:300]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())