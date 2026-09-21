# Mecânica de Recorrência de Memória

Esta mecânica define o fluxo de operação para a feature memory-recall skill:

1. Receber o prompt de busca (ex.: "releia o último bloco de texto relevante sobre tema X" ou "extrair o resumo das notas sobre tema Y").

2. Buscar o conteúdo relevante do vault Obsidian:
   - Usar pattern de busca estruturada (tags, metadata, texto correspondente) para encontrar o fragmento mais relevante.
   - Limitar a busca a arquivos que contenham os tags ou metadados especificados.
   - Se múltiplos resultados forem encontrados, priorizar o mais recente.

3. Validar o resultado:
   - Verificar que o conteúdo possui no máximo 200 tokens.
   - Se exceder, dividir em múltiplos fragmentos com checkpoints.
   - Se nenhum conteúdo relevante for encontrado, registrar o resultado como "nenhum contexto recuperado".

4. Enriquecer o contexto:
   - Adicionar cabeçalho explicando a origem do conteúdo (ex.: "Contexto recuperado do vault Obsidian em [data] por memória-recall skill").
   - Limpar metadados complexos, mantendo apenas a estrutura relevante para o contexto.
   - Condensar o conteúdo para o número máximo de tokens permitidos (200).

5. Enviar o resultado embutido como contexto estruturado (JSON/XML) para o subagente.

6. Se o fragmento for legível e dentro do limite de tokens, retornar o resultado estruturado.

7. Caso a busca não encontre conteúdo relevante, retornar um resumo breve ou indicar que nenhum contexto foi encontrado.

8. Garantir que o processo seja idempotente e seguro:
   - Nunca exponha arquivos completos que excedam o limite de tokens.
   - Se o conteúdo exceder o limite, divida em múltiplos fragmentos com checkpoints.
   - Se o conteúdo contiver dados sensíveis, reter apenas metadados sem o conteúdo real.

Código de erro:
- -1: tempo de busca excedido (>30 segundos)
- -2: conteúdo não encontrado
- -3: limite de tokens excedido
- -4: dados sensíveis detectados
- -5: erro de integração com vault
