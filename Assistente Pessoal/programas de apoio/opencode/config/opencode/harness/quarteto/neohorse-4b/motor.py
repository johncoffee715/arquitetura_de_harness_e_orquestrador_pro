"""NeoHorse-4B — motor determinístico (R85 .py): validação + anti-lixo."""
import json, re

T6_RX = re.compile(r'^\s*\{\s*"status"\s*:\s*"ok"\s*,\s*"nota"\s*:\s*9\.5\s*\}\s*$', re.S)
T11_RX = re.compile(r'^\s*\{\s*"tool"\s*:\s*"read_file"\s*,\s*"args"\s*:\s*\{\s*"path"\s*:\s*"/tmp/opencode/probe\.txt"\s*\}\s*\}\s*$', re.S)

def extrair_json(c):
    c = re.sub(r'```(?:json)?\s*|\s*```', '', c).strip()
    i = c.find('{')
    if i < 0: return None
    depth = 0; instr = False; esc = False
    for j in range(i, len(c)):
        ch = c[j]
        if instr:
            if esc: esc = False
            elif ch == '\\': esc = True
            elif ch == '"': instr = False
        else:
            if ch == '"': instr = True
            elif ch == '{': depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0: return c[i:j+1]
    return None

def validar_t6(c): return bool(T6_RX.match(c.strip()))
def validar_t11(c): return bool(T11_RX.match(c.strip()))
def validar_extraido(c, rx): return bool(rx.match((extrair_json(c) or '').strip()))
