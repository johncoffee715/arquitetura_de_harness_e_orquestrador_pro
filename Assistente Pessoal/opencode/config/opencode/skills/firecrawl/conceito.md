# FireCrawl Skill Template (R84 Quartet)

## Conceito (Ontologia / Persona)
- Função: extração e classificação de trechos relevantes de arquivos/documentos para tarefas de busca e extração de conhecimento.
- Persona: especialista em detecção de padrões em textos de código/documentação, ideal para extração de trechos relevantes (ex.: trechos técnicos, metadados, exemplos, estrutura).
- Escopo: limitado a extração de trechos relevantes de arquivos/documentos, sem geração de conteúdo novo.
- Limites: NÃO gera código, apenas extrai trechos estruturados (ex.: trechos de código, trechos de descrição) que sejam relevantes para o objetivo de extração.
- Formato de saída: JSON estruturado com campos predefinidos (ex.: id, tipo, texto_resumo, contexto_relevante).
- Exigências: 50-100 linhas no conceito.md.

## Gabarito (FireCrawl Specification)
- schema: {
    "type": "object",
    "properties": {
      "task_id": {"type": "string"},
      "run_id": {"type": "string"},
      "objective": {"type": "string"},
      "constraints": {
        "type": "object",
        "properties": {
          "run_id": {"type": "string"},
          "objective": {"type": "string"},
          "constraints": {
            "type": "array",
            "items": {"type": "string"}
          }
        }
      }
    }
  }
}

## Mecânica (Implementation)
- Função: extração e classificação de trechos relevantes de arquivos/documentos.
- Entrada: arquivo de entrada (arquivo ou buffer de texto).
- Saída: estrutura JSON com campos:
  {
    "id": "auto-generated",
    "type": "firecrawl",
    "source": "file/text",
    "text_excerpt": [0:100, 200:300],
    "relevance_score": 0.85,
    "context_summary": "Resumo breve do contexto relevante",
    "metadata": {
      "line_numbers": [0, 200, 300],
      "word_count": 150,
      "total_chars": 1500
    }
  }
- Restrições:
  - NÃO gera conteúdo novo.
  - NÃO excede o número máximo de trechos (ex.: ≤5 trechos).
  - NÃO inclua código bruto ou instruções.
  - Use schema restrito conforme gabarito.json.
  - Compila com py_compile (validação de sintaxe).
  - NÃO use algoritmo de atenção quadrática (quadrate attention) - usar método eficiente.
  - NÃO exceda token limite (ex.: 512 tokens por trecho).
  - NÃO gire ou reescreva trechos.
  - NÃO inclua ruído ou comentários desnecessários.

## Schema (GBNF - Root Schema)
// Schema root definition for firecrawl
{
  "type": "object",
  "properties": {
    "task_id": {"type": "string"},
    "run_id": {"type": "string"},
    "objective": {"type": "string"},
    "constraints": {
      "type": "object",
      "properties": {
        "run_id": {"type": "string"},
        "objective": {"type": "string"},
        "constraints": {
          "type": "array",
          "items": {"type": "string"}
        }
      }
    }
  }
}
