regra global guardrail kronjob a cada atualizaçao nos llms da stack local descreva quais sao os llms de alta precisao que devem ter sua janela de cxt economizada nesta stack local Para otimizar o desempenho e reduzir a latência em uma stack local, os Grandes Modelos de Linguagem (LLMs) de alta precisão que mais exigem economia e gerenciamento rigoroso da janela de contexto, A economia de contexto nesses modelos é crítica porque o consumo de memória RAM/VRAM cresce linearmente (ou quadraticamente, dependendo da atenção) com o tamanho do contexto, degradando rapidamente a velocidade de geração (t/s) em hardware local, Analisando estritamente os dados e as métricas da stack local, os modelos de alta precisão que devem ter sua janela de contexto economizada são aqueles que apresentam alto índice de acerto em benchmarks complexos ja citados online e nos nossos benchmarks empiricos internos, e em seguida usar a llm local mais veloz da arquitetura(t/s) e com ctx enorme na economia da janela de cxt dos llm de alta precisao para atuar como o Córtex Sensorial Primário (Filtro Talâmico de Larga Escala). Ele ingere o texto massivo, processa tarefas mecânicas (ler, limpar, estruturar) e entrega apenas o "suco condensado" (fatos puros), interceptando as requisições pesadas e realizar tasks simples de pré-processamento antes que o texto chegue aos modelos de alta precisão e cuspir  IDs, JSONs ou texto limpo:

1. Reranking de Contexto em RAG (Busca de Documentos)
Como economiza: Em vez de enviar 150k tokens de documentos brutos para o orquestrador,
você joga tudo no llm local mais veloz da arquitetura.
Task simples: Peça para ele apenas listar os IDs dos 3 parágrafos mais relevantes,
descarta o resto e envia apenas o essencial para o modelo de alta precisão.
Ingestão bruta de 150k tokens do banco documental.
O córtex cospe estritamente os IDs dos 3 parágrafos úteis,
O LLM alvo recebe apenas o enxuto, zerando o risco de OOM.

2. Sumarização de Histórico de Conversa (Trimming)
Task simples: Use o llm local mais veloz da arquitetura para
ler as últimas 20 interações do usuário e
gerar um resumo executivo de 1 parágrafo no prompt do LLM alvo.
Substitua o histórico longo por esse resumo no prompt do orquestrador.

3. Extração e Deduplicação de Logs brutos
Como economiza: Analisar logs diretamente consome milhares de tokens
de contexto à toa.
Task simples: Passe os logs extensos pelo llm local mais veloz da arquitetura
com o prompt: Ingestão de dumps pesados. Aplica regras rígidas,
filtra o lixo cronológico e preserva apenas linhas com "ERROR" ou "CRITICAL".
Blinda o throughput do LLM alvo
"Remova linhas duplicadas, timestamps repetidos".

4. Filtragem de Ruído de Web Scraping / Markdown
Como economiza: Páginas web raspadas vêm cheias de scripts,
tags HTML ou menus de navegação inúteis que incham o contexto.
Task simples: O llm local mais veloz da arquitetura lê a página inteira
e extrai apenas o texto corrido do artigo,
limpando o lixo estrutural antes do modelo de plano processar.

5. Pré-classificação e Roteamento de Intenção
Como economiza: Evita acionar o "raciocínio profundo" do orquestrador para comandos bobos.
Task simples: Avaliar se a pergunta do usuário exige ferramentas complexas.
Se o usuário disser apenas "olá" ou "obrigado", o próprio llm local mais veloz da arquitetura
responde imediatamente, poupando 100% do contexto e da VRAM dos modelos maiores.
Early-exit para phatics ("olá", "ok"). Responde a nível sensorial,
sem jamais despertar a GPU ou alocar memória nos modelos de plano.

6. Sincronia com o needle 2 AI:
O modelo veloz de CPU faz a triagem.
Se ele encontrar um padrão que exija busca exata,
o Harness dispara o POST /complete para a
porta do needle 2 de forma cirúrgica,
em vez de inundar a lib C com ruído de texto.
Em tempo de voo, o córtex varre a intenção.
Se o pattern exigir extração algorítmica ou hash exact match,
ele desvia a requisição: o Harness faz o
POST /complete cirúrgico na porta do needle 2,
devolvendo a resposta da lib C sem poluir a attention dos LLMs de alta densidade
