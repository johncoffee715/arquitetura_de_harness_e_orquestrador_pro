# Conceito de Recorrência de Memória (Memory Recall)

Esta feature é responsável por recuperar e injetar contexto de longo prazo do vault Obsidian,
baseado no conteúdo armazenado em arquivos Markdown/JSON na pasta vault (`/mnt/dados/Assistente Pessoal/cerebro`).

Personas:
- MemoryRecallSkill: o agente/skill que realiza a operação de busca e enriquecimento do contexto.
- Orchestrator: o orquestrador que solicita a habilidade ao subagente.
- User: o participante que interage com a funcionalidade.

Escopo de atuação:
- Arquivos: *.md, *.json, *.yaml, *.txt dentro da pasta vault principal.
- Limites: limite de tamanho máximo 10 KB por fragmento; evitar recuperação de arquivos grandes (>50 MB).
- Limites de contexto: máximo 200 tokens por retorno; se exceder, dividir em múltiplos fragments com checkpoints.

Fluxo de operação:
1. Receber instrução de busca (ex.: "releia o último bloco de texto relevante" ou "extrair o resumo das notas sobre tema X").
2. Buscar no vault usando tags, metadata ou texto correspondente (usar pattern de busca estruturada).
3. Validar e enriquecer o conteúdo com contexto atual (data, contexto de usuário, histórico de interação).
4. Limpar/condensar o fragmento para que o tamanho total de contexto no prompt seja ≤ 200 tokens.
5. Enviar o resultado embutido como contexto explícito no prompt do subagente (formato JSON estruturado).
6. Se o fragmento exceder limites, dividir em múltiplos fragmentos com checkpoints e processar sequencialmente.
7. Se nenhum conteúdo relevante for encontrado, registrar o resultado como "nenhum contexto recuperado".

Limites operacionais:
- Tempo de busca: ≤ 30 segundos.
- Processamento: usar parser legível; evitar formatação excessivamente complexa.
- Segurança: nunca exponha arquivos externos; apenas o conteúdo relevante com metadados de contexto.
- Conformidade: adicionar cabeçalho explicando a origem do conteúdo.

Limites de responsabilidade:
- Se a busca encontrar conteúdo que não seja seguro para exibir (secreta, sensível), reter apenas os metadados sem o conteúdo real.
- Se o conteúdo exceder o limite de tokens, dividir ou recomendar ao usuário para limpar/reduzir o vault.
- Se o usuário não autorizar a leitura de arquivos do vault, retornar mensagem de erro com instruções.

Critérios de sucesso:
- A operação retorna contexto de forma estruturada (JSON/XML).
- O número de tokens no contexto final ≤ 200.
- A instrução de busca é clara e específica.
- O resultado é rico o suficiente para continuar a conversa sem perder contexto.
- O processo é idempotente e seguro (não altera arquivos do vault).

Extensão do fluxo:
- Caso o usuário solicite uma revisão detalhada, o skill pode retornar um resumo estruturado com:
  - Contexto breve (≤ 150 tokens)
  - Principais pontos relevantes (tags, metadados, timestamps)
  - Sugestão de continuação (ex.: "O próximo passo é explorar X, pois Y é relevante para Z")
- Caso o conteúdo exceder 200 tokens, o skill deve gerar múltiplos fragmentos com checkpoints:
  - Fragmento 1: primeiros 150 tokens com contexto inicial
  - Fragmento 2: próximos 50 tokens com contexto contínuo
  - Fragmento 3: restante com contexto de continuação
- Caso nenhum conteúdo relevante seja encontrado, o skill retorne:
  - contexto_result: {"status": "no_context_found", "message": "Nenhum conteúdo relevante foi encontrado no vault."}
  - contexto estruturado com erro_info para o usuário entender o que aconteceu.

Validação de segurança:
- O skill nunca exibe conteúdo sensível (senhas, chaves, dados pessoais).
- O skill apenas processa metadados e não exibe o conteúdo completo se ele contiver informações sensíveis.
- O skill verifica o limite de tokens antes de retornar; se exceder, o skill divide automaticamente ou recomenda o usuário limpar o vault.

Validação de conformidade:
- O skill usa schema.gbnf para validar o formato do contexto estruturado.
- O gabarito.json define o allow/deny para tipos de conteúdo seguros.
- O mecanica.py valida a estrutura e segurança da operação.