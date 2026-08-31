# Decisão: Gran-Mestre v9 + R80-R83 + slot :9088 granite (2026-08-31)

## Contexto
- Subagente hefesto (:9088 qwen3.8-4b) ALUCINAVA sucesso sem escrita (3 rodadas) + lixo de retorno.
- Correção estrutural (anti-lixo gate) + substituição de LLM (diretriz usuário: comunidade/MoE).

## Decisões
1. **Slot :9088 → granite-4.2-3b-Q4_K_M** (Apache-2.0, BFCL 52.41, ctx 131072, decode ~104 t/s) — substituição 1:1 por categoria (R75), sync R27 5/5. MoE comunitários (qwen3.5-moe-4.7B-d4B) ficam em fitragem.
2. **R80-R83 promulgadas** (AGENTS.md): pesquisa multi-idioma obrigatória; constrained decoding universal; estrangulamento tríplice; crivo sistêmico de tudo.
3. **Doutrina v9.0.0**: núcleo v8.4 + R57-R79 + otimizações do fonte original + anti-lixo gate obrigatório.
4. **Hefesto v2**: dispatcher reconstruído + contrato retorno anti-lixo + temperature 0.8.
5. **Commit**: b8405e481.

## Evidência
- Testes: doctrine 8/8 · antilixo 9/9 · bridge R81 15/15.
- Crivo: granite PASSOU_CATEGORICO; ternary NAO (fence = GBNF necessário).
- FORJA byte-level: granite gerou JSON conforme com GBNF (chaves corretas).
