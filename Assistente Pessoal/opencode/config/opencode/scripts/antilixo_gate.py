"""antilixo_gate.py — Detector determinístico anti-lixo / anti-alucinação de entrega.

Roda no GATE DE ENTREGA do orquestrador (R28/R53/R70), antes de aceitar o retorno de um
subagente. Zero LLM, custo ~0, fail-closed (nunca deixa passar suspeito).

Detecta (padrões observados 2026-08-31 no retorno do subagente hefesto :9088):
  1. LIXO DE FORMATAÇÃO: linhas gigantes de um único caractere separador (─ ═ = - * ~),
     repetição extrema, texto com <5% de conteúdo útil, conteúdo mínimo sem evidência.
  2. ALUCINAÇÃO DE ENTREGA: o retorno afirma sucesso ("8/8 PASS", "concluído", "OK") mas
     NENHUM arquivo-alvo mudou vs baseline de SHA (o subagente "reporta" sem ter escrito).
  3. INCOMPLETO: afirma sucesso sem `exit_status` explícito (contrato de retorno MIX r6).

Uso (gate do orquestrador):
    from antilixo_gate import classificar
    ver = classificar(retorno_bruto, arquivos_alvo, baseline_shas)
    if ver["status"] != "ok":  # NAO_PASSOU_CATEGORICO com motivos
        ...

Escopo: governança de orquestração — criação por execução supervisionada direta
(R6/R11: o executor designado era o próprio fonte da alucinação; lição no decision-log).
"""
import hashlib
import re
from pathlib import Path
from typing import Dict, List

SEP_CHARS = set("─═☰-=*_#~·")

# Sinais de sucesso/realização que disparam verificação de evidência de escrita
PADRAO_SUCESSO = re.compile(
    r"(8/8\s*PASS|PASSOU|tudo\s*ok|conclu[íi]do\s*com\s*sucesso|✅|done|success|entrega\s*ok)",
    re.IGNORECASE,
)

MIN_LINHA_SUSPEITA = 120       # linha longa demais para ser conteúdo sadio de retorno
MIN_RETORNO_MINIMO = 30        # chars totais abaixo disso = retorno quase vazio
MIN_CONTEUDO_AFIRMACAO = 50    # chars úteis mínimos para sustentar afirmação de sucesso
RATIO_SEP_SUSPEITO = 0.9       # fração de chars separadores em uma linha para marcar lixo
RATIO_LIXO_GLOBAL = 0.5        # fração global de chars-separador sobre o total


def sinais_lixo(texto: str) -> Dict:
    """Detecta lixo de FORMATAÇÃO/repetição no retorno bruto (não julga conteúdo)."""
    if not texto:
        return {"lixo": True, "motivos": ["retorno_vazio"]}

    motivos: List[str] = []
    linhas = texto.splitlines()

    # 1. Linhas gigantes de separadores
    for i, linha in enumerate(linhas[:200]):
        if len(linha) < MIN_LINHA_SUSPEITA:
            continue
        unicos = set(linha.strip())
        if len(unicos) <= 4 and unicos.issubset(SEP_CHARS | {" "}):
            motivos.append(f"linha_separador_gigante_L{i + 1}")
            break

    # 2. Retorno quase vazio (sem afirmação nenhuma de entrega)
    if len(texto) < MIN_RETORNO_MINIMO:
        motivos.append("retorno_minimo")

    # 3. Densidade extrema só para textos grandes (evita falso-positivo em retorno curto)
    if len(texto) > 1000:
        conteudo = "".join(ch for ch in texto if ch.isalnum() or ch.isspace())
        if len(conteudo) / len(texto) < (1 - RATIO_LIXO_GLOBAL):
            motivos.append("densidade_conteudo_baixa")

    return {"lixo": bool(motivos), "motivos": motivos}


def afirmar_sucesso(texto: str) -> bool:
    return bool(PADRAO_SUCESSO.search(texto))


def tem_exit_status(texto: str) -> bool:
    return "exit_status" in texto


def verificar_entrega(
    retorno: str,
    arquivos_alvo: List[Path],
    baseline_shas: Dict[str, str],
    exigir_exit_status: bool = True,
) -> Dict:
    """Verifica evidência de escrita real + contrato de retorno. Retorna dict com status."""
    motivos: List[str] = []
    lixo = sinais_lixo(retorno)
    if lixo["lixo"]:
        motivos.extend(lixo["motivos"])

    # Evidência de escrita: algum arquivo-alvo com sha diferente do baseline?
    escrita = False
    for p in arquivos_alvo:
        if not p.exists():
            motivos.append(f"arquivo_alvo_ausente:{p.name}")
            continue
        atual = hashlib.sha256(p.read_bytes()).hexdigest()
        if baseline_shas.get(str(p)) != atual:
            escrita = True

    alucinacao = afirmar_sucesso(retorno) and bool(arquivos_alvo) and not escrita
    if alucinacao:
        motivos.append("alucinacao_entrega:afirma_sucesso_sem_escrita")

    # Afirmação de sucesso com conteúdo útil insuficiente (retorno curto "tudo ok")
    util = len("".join(ch for ch in retorno if ch.isalnum() or ch.isspace()))
    if afirmar_sucesso(retorno) and util < MIN_CONTEUDO_AFIRMACAO:
        motivos.append(f"conteudo_insuficiente_para_afirmacao_{util}")

    incompleto = exigir_exit_status and afirmar_sucesso(retorno) and not tem_exit_status(retorno)
    if incompleto:
        motivos.append("incompleto:afirma_sucesso_sem_exit_status")

    status = "ok" if not motivos else "NAO_PASSOU_CATEGORICO"
    return {
        "status": status,
        "motivos": motivos,
        "lixo": lixo["lixo"],
        "alucinacao_entrega": alucinacao,
        "incompleto": incompleto,
        "escrita_detectada": escrita,
    }


def classificar(retorno: str, arquivos_alvo: List[Path], baseline_shas: Dict[str, str], exigir_exit_status: bool = True) -> Dict:
    """API de gate: classifica o retorno bruto de um subagente."""
    ver = verificar_entrega(retorno, arquivos_alvo, baseline_shas, exigir_exit_status)
    if ver["status"] == "ok":
        return {"status": "ok", "motivos": [], "evidencia": {"escrita_detectada": True}}
    return ver


if __name__ == "__main__":
    # smoke manual
    import sys
    demo = "Tudo pronto! 8/8 PASS ✅"
    print(classificar(demo, [], {}))