---
name: roteador-hibrido
description: "Roteador Híbrido L0/L0.5 — coexistência RWKV7-0.4B (L0.5 Córtex Cognitivo: classificação semântica com GBNF, ingestão de logs longos 1M sem perda) + Needle 2 (L0 Syntactic Enforcer: payload JSON estrito 100% schema). Entrada do usuário → RWKV7 classifica intenção → comando operacional vai direto ao Needle (zero GPU) ou raciocínio complexo acorda LLMs densos (F1/F2). Use como camada de entrada do harness (Fase 0) e para parsing TDD de logs longos (Fase 4)."
mode: skill
tags: "roteador, hibrido, l0, l0.5, rwkv7, needle, intent, classificacao, semantico, sintatico, coexistencia"
origin: helenizado: doc RWKV7 L0.5 + Needle L0 (2026-08-31)
metadata:
  category: methodology
  version: 1.0.0
  date: 2026-08-31
  author: Gran-Mestre
  motor: RWKV7 :9084 (L0.5) + Needle :9091 (L0)
---

# ROTEADOR-HIBRIDO — O Porteiro Cognitivo

Coexistência **L0.5 (RWKV7 semântico) + L0 (Needle sintático)** — o fluxo do documento:
entrada → RWKV7 classifica intenção → operacional vai ao Needle (payload estrito) ou complexo acorda LLMs densos.

## Fluxo

```text
[ENTRADA USUÁRIO]
      │
      ▼
[FASE 0: RWKV7-0.4B (L0.5) — classificação semântica com GBNF]
      │
      ├── saudacao ────────────────► resposta local (zero GPU)
      ├── operacional (mcp/hook/cli/git) ──► [L0: Needle 2 — payload JSON estrito]
      └── complexo (brainstorm/codigo/rag) ──► [F1/F2: LLMs densos]

[FASE 4: RWKV7 ingere logs longos SEM perda (RNN O(1)) — causa raiz no topo]
         Needle 2 valida schema (100% compliance)
```

## Por que a coexistência

| | RWKV7-0.4B (L0.5) | Needle 2 (L0) |
|---|---|---|
| Memória | janela RECORRENTE O(1) — logs longos sem descarte | janela 256 fixa — descarta início |
| Cognição | 400M — small-step reasoning, classificação multi-rótulo | 45M — sintaxe pura |
| JSON | precisa de GBNF (grammar-guided) | força por construção (byte-level) |
| Papel | semântico (intent, logs) | sintático (payload estrito) |

## Como usar

```bash
# Roteamento da entrada (Fase 0)
python3 scripts/roteador_hibrido.py "Execute o hook stack-health-check" --json
# → rota direto → needle (payload JSON estrito)

python3 scripts/roteador_hibrido.py "Preciso brainstorm do RAG" --json
# → rota complexo → llm-densos

# Fase 4: log longo → RWKV7 extrai causa raiz (sem filtro agressivo)
# (RWKV7 1M ctx lê o traceback completo sem perder o topo)
```

## Output contract

```yaml
roteador_hibrido:
  rota: direto | complexo
  destino: needle-{tipo} | llm-densos | resposta-local
  intento: {intent, tipo, confianca, resumo}
  payload: {...}
```

## Anti-padrões

- Acordar GPU para comando direto (RWKV7+Needle resolvem).
- RWKV7 sem GBNF para JSON (divaga — documentado).
- Inventar intento/payload.
- Tratar Needle como raciocinador (45M — sintaxe só).