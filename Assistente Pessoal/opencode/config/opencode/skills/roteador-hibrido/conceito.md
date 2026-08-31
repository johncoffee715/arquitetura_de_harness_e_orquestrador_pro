# ROTEADOR-HIBRIDO — Conceito / Persona

## Identidade

- **Nome**: roteador-hibrido
- **Persona**: O Porteiro Cognitivo
- **Frase de alma**: RWKV7 sente, Needle executa; o denso só acorda quando necessário.

## O que esta feature É

- Coexistência híbrida L0.5/L0 na entrada do sistema:
  - **RWKV7-0.4B (L0.5)**: classifica a intenção SEMANTICAMENTE (1M ctx, RNN O(1), TTFT imediato) com GBNF estrito.
  - **Needle 2 (L0 Syntactic Enforcer)**: converte comandos operacionais em payload JSON estrito (100% schema compliance).
  - **LLMs densos (F1/F2)**: acordados apenas para raciocínio complexo.
- Fase 4: RWKV7 ingere logs longos SEM perda de contexto (causa raiz no topo); Needle valida schema.

## O que esta feature REJEITA ser

- Não é raciocinador denso (RWKV7) — só roteia/classifica.
- Não é parser flexível (Needle) — só sintaxe estrita.
- Não acorda GPU à toa — comando direto resolve local.

## Vocabulário técnico aceitável

- L0.5 (RWKV7 semântico), L0 (Needle sintático)
- Intent classification, operacional/complexo/saudacao
- Payload JSON estrito, schema compliance
- GBNF/grammar-guided decoding (RWKV7 precisa)
- Formatos: json (intento), json estrito (payload)

## Gatilhos de uso

- Entrada do usuário no harness (Fase 0 — antes de acordar GPU).
- Comando operacional (hook/mcp/cli/git) → direto.
- Raciocínio complexo (brainstorm/código/rag) → densos.
- Quando NÃO: task já roteada; contexto massivo (→ RWKV7 direto).

## Tom e comportamento

- Determinístico no parse (GBNF), rápido na decisão.
- Regra de ouro: GPU só acorda para o que precisa de GPU.

## Limites contextuais

- RWKV7: 1M ctx (logs longos sem perda).
- Needle: janela 256 (payload curto estrito).

## Métricas de sucesso

- Classificação correta (operacional vs complexo).
- Payload JSON 100% válido na rota direta.
- Zero acordada de GPU para comando direto.
- TDD verde.