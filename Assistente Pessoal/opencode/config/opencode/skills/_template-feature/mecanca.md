# Mecânica de Ignição (Execution & Validation)

## Função
O agente de memória-recall ignita o fluxo de trabalho ao:
1. Buscar e extrair contexto relevante da stack (health check)
2. Condensar o contexto usando o RWKV7 sensorial model
3. Validar que o contexto condensado é executável e não contém ruído
4. Retornar o resumo sintetizado no formato esperado

## Parâmetros de Entrada
- `context_id`: ID do contexto a ser resumido (ex.: observação, observação histórica)
- `stack_health`: Resultado do health check da stack (ex.: lista de métricas de saúde)
- `max_context_tokens`: Limite de contexto (ex.: 1048576 tokens)

## Fluxo de Execução
1. Executar o modelo RWKV7 (1M contexto) para condensar o contexto fornecido.
2. Validar o resultado usando Pydantic para garantir schema válido.
3. Se o resultado for válido, retornar o resumo sintetizado.
4. Se o resultado for inválido ou degradação acima de limiares, retornar erro com detalhes de diagnóstico.

## Parâmetros de Saída
- `summary`: Texto resumido do contexto (max 512 tokens)
- `context_id`: ID do contexto original
- `timestamp`: Timestamp da operação (UTC)
- `status`: "success" ou "failure"
- `validation_details`: Detalhes de validação (ex.: token count, schema check)

## Restrições de Segurança
- Nenhum token pode ser inventado além do contexto fornecido.
- O agente nunca deve gerar conteúdo não presente no contexto.
- Stop tokens garantem que o agente pare após a validação.
- Max tokens limita o tamanho da saída para eficiência.

## Stop Tokens
```
</|eot_id|>
```

## Stop Tokens (para execução do agente)
```
</|eot_id|>
</|eot_id|>
```

## Stop Tokens (para o modelo LLM)
```
</|eot_id|>
</|eot_id|>
```

## Stop Tokens (para o motor)
```
</|eot_id|>
```

## Stop Tokens (para a execução)
```
</|eot_id|>
```

## Stop Tokens (para a validação)
```
</|eot_id|>
```