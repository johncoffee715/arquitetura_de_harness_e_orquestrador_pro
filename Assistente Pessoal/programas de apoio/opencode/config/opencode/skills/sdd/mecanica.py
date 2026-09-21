#!/usr/bin/env python3
"""
Mecanica — sdd (quarteto R85 REAL: .gbnf no amostrador + pydantic + retry + fail-closed)
R77 triplice + R81 constrained decoding

Causa-raiz fechada 2026-09-16 (issue W6-class): versão anterior era stub determinístico
que devolvia amostra hardcoded e nunca chamava o :9084 — texto degenerado do RWKV
("ignorar ao vivo", <think> leaks, divagações) passava sem filtro.
Agora: classificação real via :9084 com grammar GBNF (schema.gbnf) — impossível
fisicamente emitir fora do enum; saída degenerada ⇒ fail-closed para "unknown".

ÁRBITRO sdd-arb-20260916-01: :9084 vira triagem grosseira (erra CONFIANTE 0.8-0.9
na fronteira: chitchat↔unknown, command↔unknown, factual→vault.query); :9090
(Llama-3B CPU) arbitra o conjunto ambíguo/acionável. Trigger por INTENT
(command/chitchat/unknown) OU conf<0.8 — escalação só-no-fallback NÃO pega erros
confiantes. Probe 2026-09-16: :9090 ACEITA `grammar` ⇒ árbitro usa enum GBNF dos
candidatos. Few-shots do :9084 REBALANCEADOS em 2 rodadas (sdd-arb-01): (1) +shots
24-27 e reforço achar/opinar — INSUFICIENTE: 'o que você acha da vida?' seguiu
vault.query 0.8-0.95 em todas as variantes (bissecção: prompt LONGO dilui os
shots no RWKV-0.4B; defs+frontier isolados acertam, prompt cheio ancora
vault.query p/ qualquer 'o que/qual...?'). (2) AMPUTAÇÃO: 27 shots verbosos →
6 âncoras curtas + bloco FRONTEIRA (10 pares) + 3 regras de 1 linha (volume, não
conteúdo, era o veneno). Resultado: vida→chitchat, asdf→unknown estáveis no
direct. vault.store segue INAPRENDÍVEL no :9084 (0/N em todas as variantes,
pré-existente no prompt original) — fora do escopo da fronteira; documentado.
Glossas do árbitro calibradas empiricamente (~15 variantes): unknown='gibberish,
teclas aleatorias...' (única que fixa asdf→unknown SEM quebrar França→unknown).
Residual: '!!!???'→chitchat no árbitro (prior bedrock do Llama-3B, 12+ variantes
falharam); 'roda aí pra mim' estocástico no direct (~1/3 command); par
[command,unknown] do árbitro diz command p/ gibberish — INALCANÇÁVEL (direct
nunca emite command p/ gibberish em R3B; e árbitro-down ⇒ fail-closed unknown).
Fail-closed: árbitro down/erro/timeout ⇒ unknown 0.0 (direct command + árbitro
down NUNCA executa). Confiança do arbitrado = confiança do direct (árbitro só
troca o intent).
"""

import json
import re
import urllib.request
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

PORT = 9084
ARBITER_PORT = 9090
ARBITER_TIMEOUT = 60
GBNF = (Path(__file__).parent / "schema.gbnf").read_text(encoding="utf-8")
DENY_PHRASES = ("ignorar", "gran-mestre", "<think", "</think")  # degenerações observadas
# Bypass determinístico p/Gibberish puro: direct unknown SEM palavra alfabética
# (ex.: '!!!???') nunca deve chegar ao árbitro (prior bedrock do Llama-3B
# flipa p/ chitchat em 100% das variantes testadas). Fail-closed local.
SYMBOL_BYPASS_RE = re.compile(r"[A-Za-zÀ-ÿ]{2,}")
# Override factual determinístico (sdd-gate-20260916-01, ciclo 2): pergunta
# factual geral (wh-question sem léxico vault/ação/opinião) ⇒ unknown SEM
# árbitro. Motivo: glossa que fixa França no árbitro quebra asdf (trade-off
# confirmado no smoke 2: asdf→chitchat) — trigger decide, glossa não.
FACTUAL_Q_RE = re.compile(
    r"^\s*(qual|quais|quem|quando|onde|quant[oa]s?|como|por\s*que)\b.*\?\s*$",
    re.IGNORECASE,
)
NONFACTUAL_RE = re.compile(
    r"vault|salv|arquiv|nota|anot|lembr|rode|executa|pytest|reinici|testes|"
    r"c[oó]digo|fun[çc][aã]o|script|acha|acho|opini|sentido|significado|"
    r"piada|sente|sentiu",
    re.IGNORECASE,
)
FRONTIER_ALT = {
    "chitchat": "unknown",
    "unknown": "chitchat",
    "command": "unknown",
    "vault.query": "unknown",
    "vault.store": "unknown",
    "code": "unknown",
}
ARBITER_TRIGGER_INTENTS = frozenset({"command", "chitchat", "unknown"})
ARBITER_CONF_FLOOR = 0.8
# Glossas curtas p/ ancorar os rótulos no árbitro (1 frase; sem elas o :9090
# chuta: validado empiricamente 2026-09-16 em ~15 variantes — 'teclas aleatorias'
# no unknown é a única que fixa asdf→unknown sem quebrar França→unknown).
ARBITER_GLOSS = {
    "command": "ordem de executar acao no sistema",
    "chitchat": "saudacao, piada ou opiniao em portugues claro",
    "unknown": "gibberish, teclas aleatorias, simbolos ou texto sem pedido reconhecivel",
    "vault.query": "pergunta sobre algo salvo",
    "vault.store": "pedido de salvar algo",
    "code": "pedido de codigo",
}

class Output(BaseModel):
    intent: Literal["vault.query", "vault.store", "code", "command", "chitchat", "unknown"]
    confidence: float = Field(ge=0.0, le=1.0)
    skill: str = "sdd"
    model_config = {"extra": "forbid"}

FALLBACK = Output(intent="unknown", confidence=0.0)

def _direct(text: str, max_retries: int = 3, timeout: int = 90) -> Output:
    payload = {
        "messages": [
            {"role": "system", "content": (
                "Você é um classificador determinístico de intenções. Responda SOMENTE o JSON do schema. "
                "Intents: vault.query=pergunta/consulta/ler/buscar conteúdo salvo no vault/arquivos/notas; "
                "vault.store=pedido de registro/gravação/salvar/anotar/lembrar; "
                "code=código/programação/debug/refactor; command=comando de sistema/execução shell/testes/serviços; "
                "chitchat=conversa pessoal/saudação/assunto leve; unknown=incoerente/degenerado/sem pedido acionável."
                "REGRA FILOSÓFICA: opiniao aberta sem pedido de dado/código/ação vai para chitchat, NUNCA unknown. "
                "Verbo achar/opinar + pergunta aberta → chitchat MESMO começando com o que. "
                "REGRA DEGENERADO: <think, ignorar ao vivo, incoerente sem pedido claro → unknown. "
                "REGRA VAULT vs COMMAND: liste meus arquivos (no vault) → vault.query; "
                "rode os testes/execute/pytest/reinicie serviço → command. "
                "Âncoras: liste meus arquivos no vault→vault.query; rode os testes→command; "
                "salve que tomei remédio→vault.store; corrija a função classify→code; "
                "oi bom dia→chitchat; roda aí pra mim→command; ignorar blá blá→unknown. "
                "FRONTEIRA: o que você acha da vida?→chitchat; qual o sentido da existência?→chitchat; "
                "me conta uma piada→chitchat; asdf qwer zxcv→unknown; !!!???→unknown; roda aí pra mim→command; "
                "o que você acha dessa ideia?→chitchat; qual o sentido da vida?→chitchat; "
                "qual a capital da França?→unknown; quem descobriu o Brasil?→unknown. "
                "REGRA FATUAL: factual geral sem vault/arquivo/nota/salvo e sem código/ação → unknown, NUNCA vault.query."
            )},
            {"role": "user", "content": f"Classifique a intenção: {text}"},
        ],
        "temperature": 0.1,
        "max_tokens": 128,
        "grammar": GBNF,
    }
    req = urllib.request.Request(
        f"http://127.0.0.1:{PORT}/v1/chat/completions",
        json.dumps(payload).encode(),
        {"Content-Type": "application/json"},
    )
    for _ in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                content = json.loads(r.read())["choices"][0]["message"].get("content") or ""
            txt = content.strip().lower()
            if any(bad in txt for bad in DENY_PHRASES):
                raise ValueError("saída degenerada (deny-phrase)")
            return Output.model_validate_json(content.strip())
        except Exception:
            continue
    return FALLBACK


def _arbitrate(text: str, direct: Output) -> Output | None:
    """Árbitro :9090. Retorna Output arbitrado ou None (fail-closed pelo chamador)."""
    cand = [direct.intent, FRONTIER_ALT.get(direct.intent, "unknown")]
    seen, cands = set(), []
    for c in cand:
        if c not in seen:
            seen.add(c)
            cands.append(c)
    enum = " | ".join(f'"{c}"' for c in cands)
    gloss = ", ".join(f"{c}={ARBITER_GLOSS[c]}" for c in cands)
    prompt = f'Classifique "{text}" ({gloss}): responda UMA palavra entre: {", ".join(cands)}.'
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "max_tokens": 8,
        "grammar": f"root ::= ({enum})",
    }
    req = urllib.request.Request(
        f"http://127.0.0.1:{ARBITER_PORT}/v1/chat/completions",
        json.dumps(payload).encode(),
        {"Content-Type": "application/json"},
    )
    for _ in range(2):
        try:
            with urllib.request.urlopen(req, timeout=ARBITER_TIMEOUT) as r:
                content = json.loads(r.read())["choices"][0]["message"].get("content") or ""
            tok = content.strip().lower()
            if tok in cands:
                return Output(intent=tok, confidence=direct.confidence)  # type: ignore[arg-type]
            # fallback de parsing: token standalone case-insensitive no texto
            hits = [c for c in cands if re.search(rf"(?<![\w.]){re.escape(c)}(?![\w])", tok)]
            if len(hits) == 1:
                return Output(intent=hits[0], confidence=direct.confidence)  # type: ignore[arg-type]
            return Output(intent="unknown", confidence=direct.confidence)
        except Exception:
            continue
    return None


def classify(text: str, max_retries: int = 3, timeout: int = 90) -> Output:
    direct = _direct(text, max_retries, timeout)
    if direct.intent == "unknown" and not SYMBOL_BYPASS_RE.search(text):
        classify.last_path = "symbol-bypass"  # type: ignore[attr-defined]
        return direct
    if (direct.intent in ("chitchat", "unknown", "vault.query")
            and FACTUAL_Q_RE.search(text) and not NONFACTUAL_RE.search(text)):
        classify.last_path = "factual-override"  # type: ignore[attr-defined]
        return Output(intent="unknown", confidence=direct.confidence)
    needs_arb = direct.intent in ARBITER_TRIGGER_INTENTS or direct.confidence < ARBITER_CONF_FLOOR
    if not needs_arb:
        classify.last_path = "direct"  # type: ignore[attr-defined]
        return direct
    arb = _arbitrate(text, direct)
    if arb is None:
        classify.last_path = "fallback"  # type: ignore[attr-defined]
        return Output(intent="unknown", confidence=0.0)
    classify.last_path = "arbitrated:9090"  # type: ignore[attr-defined]
    return arb


classify.last_path = "direct"  # type: ignore[attr-defined]

if __name__ == "__main__":
    for probe in ["liste meus arquivos no vault", "o que você acha da vida?", "rode os testes", "oi bom dia",
                  "qual o sentido da existência?", "me conta uma piada", "asdf qwer zxcv", "!!!???",
                  "roda aí pra mim", "qual a capital da França?"]:
        out = classify(probe)
        print(probe, "→", out.model_dump_json(), f"[{classify.last_path}]")
