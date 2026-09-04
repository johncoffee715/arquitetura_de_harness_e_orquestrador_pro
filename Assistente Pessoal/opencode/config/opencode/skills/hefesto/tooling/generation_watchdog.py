#!/usr/bin/env python3
"""
Generation Watchdog — Camada 2.5 (R22/R18)

Detecta n-gram repetition, sequence repetition, semantic cycle, token stall,
timeout, max generation, entropy anomaly durante geração.
Ação: STOP / INVALIDATE / RETRY
"""
from __future__ import annotations
import time
import re
from collections import Counter
from typing import Dict, List

def detect_ngram_repetition(text: str, n: int = 4, threshold: int = 3) -> Dict:
    """Detecta repetição de n-grams (ex: 4-gram repetido 3x → loop)."""
    words = text.split()
    if len(words) < n * threshold:
        return {"repetition": False}
    ngrams = [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]
    counts = Counter(ngrams)
    most_common = counts.most_common(1)[0] if counts else ("", 0)
    repetition = most_common[1] >= threshold
    return {"repetition": repetition, "ngram": most_common[0], "count": most_common[1], "action": "STOP" if repetition else "continue"}

def detect_sequence_repetition(text: str, min_repeat: int = 3) -> Dict:
    """Detecta repetição de sequência (ex: 'abc abc abc')."""
    # Procurar padrões de 10+ chars repetidos
    for length in [20, 30, 50]:
        for i in range(len(text) - length * min_repeat):
            seq = text[i:i+length]
            if text.count(seq) >= min_repeat:
                return {"repetition": True, "sequence": seq[:30], "action": "INVALIDATE"}
    return {"repetition": False}

def detect_token_stall(last_token_time: float, timeout: float = 5.0) -> Dict:
    """Detecta token stall (sem token por > timeout)."""
    elapsed = time.time() - last_token_time
    stalled = elapsed > timeout
    return {"stalled": stalled, "elapsed": elapsed, "action": "RETRY" if stalled else "continue"}

def detect_entropy_anomaly(text: str, window: int = 100) -> Dict:
    """Detecta anomalia de entropia/diversidade (texto muito repetitivo ou muito aleatório)."""
    if len(text) < window:
        return {"anomaly": False}
    # Entropia simplificada: razão de caracteres únicos / total
    recent = text[-window:]
    unique_ratio = len(set(recent)) / len(recent) if recent else 0
    # Muito baixo (<0.2) = repetitivo, muito alto (>0.9) = aleatório (pode ser alucinação)
    anomaly = unique_ratio < 0.2 or unique_ratio > 0.95
    return {"anomaly": anomaly, "unique_ratio": unique_ratio, "action": "INVALIDATE" if anomaly else "continue"}

def check_max_generation(generated_tokens: int, max_tokens: int) -> Dict:
    """Verifica se atingiu max_tokens sem stop."""
    reached = generated_tokens >= max_tokens
    return {"reached": reached, "action": "STOP" if reached else "continue"}

def watchdog_check(text: str, generated_tokens: int, max_tokens: int, last_token_time: float) -> Dict:
    """Orquestra todos os checks da Camada 2.5. Retorna ação agregada."""
    checks = [
        detect_ngram_repetition(text),
        detect_sequence_repetition(text),
        detect_token_stall(last_token_time),
        detect_entropy_anomaly(text),
        check_max_generation(generated_tokens, max_tokens),
    ]
    # Se qualquer check pedir STOP/INVALIDATE/RETRY, propagar a mais severa
    actions = [c.get("action", "continue") for c in checks]
    if "STOP" in actions or "INVALIDATE" in actions:
        return {"action": "STOP", "reason": "watchdog triggered", "details": checks}
    if "RETRY" in actions:
        return {"action": "RETRY", "reason": "stall/timeout", "details": checks}
    return {"action": "continue", "details": checks}

if __name__ == "__main__":
    # Teste
    print(detect_ngram_repetition("hello world hello world hello world hello world"))
    print(detect_sequence_repetition("abc def abc def abc def"))
    print(watchdog_check("test " * 100, 100, 200, time.time()))
