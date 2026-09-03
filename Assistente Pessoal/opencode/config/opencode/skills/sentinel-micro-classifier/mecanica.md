# Mecânica do Classificador Micro


**Agente**: ClassificadorMicro (Wave1-micro 0.1B)

**Mecânica de Ignição**:
1. Receber o texto de entrada (max 256 tokens).
2. Executar o modelo SmolLM2-360M :9093 via curl POST :9093/complete com GBNF para gerar a classificação de sentimento.
3. Validar a saída JSON contra o schema definido no gabarito.json.
4. Se a saída for válida, retornar o JSON estruturado conforme o conceito.md.
5. Se a saída for inválida ou exceder limites, gerar erro de validação e registrar no log.

**Contraints**:
- Token limit: 256 tokens.
- Saída deve ser JSON puro (sem texto extra).
- Schema válido conforme gabarito.json.
- Tempo de resposta ≤ 5 segundos.

**Validação**:
- Usar Pydantic para validar o JSON antes de encaminhar para o cliente.
- Garantir que o modelo use GBNF para restringir saída a schema estrita.
- Nenhum loop de repetição ou alucinação.
