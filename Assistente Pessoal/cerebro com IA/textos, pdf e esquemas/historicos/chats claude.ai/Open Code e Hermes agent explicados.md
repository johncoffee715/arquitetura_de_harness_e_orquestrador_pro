---
title: "Open Code e Hermes agent explicados"
source: "https://claude.ai/chat/0fc9e550-74a2-49fb-8aec-f3cb29644793"
author:
published:
created: 2026-07-17
description: "Claude is Anthropic's AI, built for problem solvers. Tackle complex challenges, analyze data, write code, and think through your hardest work."
tags:
  - "clippings"
---
**You**

Me explique o que é o open Code, Hermes agent e como eles podem me ajudar conforme meu histórico.

---

**Claude**

Ótimas ferramentas para explorar, John. Deixa eu te explicar as duas e conectar com o teu setup.

---

### OpenCode

OpenCode é um agente de coding AI open-source para terminal, escrito em Go, criado pelo time da SST. Ele acumula mais de 95.000 estrelas no GitHub, é licença MIT (gratuito), e suporta mais de 75 providers de modelos. [OpenAIToolsHub](https://www.openaitoolshub.org/en/blog/opencode-review-terminal-ai-coding)

O diferencial central: suporta configuração "bring-your-own-provider" — você traz sua própria API key de qualquer provider, ou roda modelos locais via Ollama sem custo de API. Também suporta MCP (Model Context Protocol), LSP para entendimento inteligente do código, e comandos customizados definidos como arquivos Markdown. [OpenReplay](https://blog.openreplay.com/opencode-ai-coding-agent/)

**Como te ajuda:**  
Você já roda `qwen2.5-coder:14b`, `deepseek-coder-v2:16b` e outros modelos no teu Ollama local. O OpenCode se conecta diretamente ao Ollama e oferece uma TUI (Terminal User Interface) para interagir com esses modelos para tarefas de coding, debugging e mais — tudo sem sair do terminal, sem assinatura, e com os modelos que você já tem no AI-Lab2. Ideal para trabalhar no próprio `core/ai-lab.sh` e demais scripts da stack. [GitHub](https://github.com/opencode-ai/opencode)

---

### Hermes Agent

Hermes Agent foi lançado em 26 de fevereiro de 2026 pelo NousResearch (os mesmos do modelo Hermes). É Apache 2.0, com mais de 40 ferramentas built-in: gerenciamento de arquivos, navegação web, execução de código, terminal remoto e chamadas de API. [OpenAIToolsHub](https://www.openaitoolshub.org/en/blog/hermes-agent-ai-review)

O grande diferencial: é um agente autônomo open-source com memória persistente, mais de 70 skills built-in, automações agendadas, e integração com plataformas de mensagens como Telegram, Discord, Slack e WhatsApp. Qualquer serviço que implemente o endpoint `/v1/chat/completions` compatível com OpenAI funciona como backend. [Fastio](https://fast.io/resources/hermes-agent-ollama-local-llm/)

O mecanismo de auto-melhoria é o que o diferencia: ele aprende com falhas de tarefas passadas via memória episódica e ajusta a abordagem nas execuções seguintes. [OpenAIToolsHub](https://www.openaitoolshub.org/en/blog/hermes-agent-ai-review)

**Como te ajuda:**  
Os benefícios do inference local são custo zero de API, privacidade total (nenhum prompt sai da sua rede), e funcionamento offline ou em máquinas isoladas. Isso se encaixa perfeitamente no teu conceito de AI-Lab soberano. Você poderia apontar o Hermes Agent para o teu Ollama local (com `HSA_OVERRIDE_GFX_VERSION=9.0.6` no teu MI50) e ter um agente autônomo que executa tarefas complexas como o sync de vídeos do YouTube, análise de PCB, ou até automações de manutenção do próprio AI-Lab2. [Fastio](https://fast.io/resources/hermes-agent-ollama-local-llm/)

---

### Resumo prático para o teu caso

|  | OpenCode | Hermes Agent |
| --- | --- | --- |
| **Foco** | Coding assistido no terminal | Agente autônomo multi-tarefa |
| **Melhor uso** | Desenvolver/debugar scripts do AI-Lab2 | Automatizar tarefas, memória persistente |
| **Backend** | Ollama (já tens) | Ollama (já tens) |
| **ROCm/MI50** | Indiferente (usa Ollama como proxy) | Indiferente (usa Ollama como proxy) |
| **Integração** | MCP, LSP, comandos custom | MCP, Telegram, memória episódica |

Os dois rodam em cima do teu Ollama existente — zero custo adicional de infraestrutura.

---

**You**

Nesse caso e possível usá-los no openwebui, ou seguir em outro caminho de gui

---

**Claude**

Boa notícia: ambos integram com Open-WebUI, mas de formas bem diferentes. Deixa eu mapear o cenário completo pra ti.

---

### Hermes Agent + Open-WebUI ✅ Integração nativa

O Hermes Agent tem documentação oficial para Open-WebUI. A integração funciona server-to-server: o Open-WebUI se conecta ao servidor de API do Hermes exatamente como se fosse o OpenAI. O Hermes processa as requisições com todo o seu toolset — terminal, operações de arquivo, web search, memória, skills — e retorna a resposta final. [Nousresearch](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/open-webui)

O processo é simples:  
Basta rodar o script `setup_open_webui.sh` dentro do diretório do Hermes Agent. Ele configura automaticamente as variáveis de ambiente necessárias (`API_SERVER_ENABLED`, `API_SERVER_HOST`, `API_SERVER_KEY`, etc.), reinicia o gateway do Hermes, e em Linux com systemd instala um user service. [GitHub](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/open-webui.md)

Depois disso, o modelo `hermes-agent` aparece no dropdown de modelos do Open-WebUI. Ao selecionar e conversar, o agente tem acesso completo ao seu toolset — terminal, arquivos, web search, memória, skills — direto pela interface do Open-WebUI. Streaming está habilitado por padrão, com indicadores inline enquanto as ferramentas executam. [Open WebUI](https://docs.openwebui.com/getting-started/quick-start/connect-an-agent/hermes-agent/)

**Ponto crítico para o teu setup:** as tool calls rodam no host onde o servidor da API do Hermes está rodando — ou seja, no teu CachyOS. Se o Open-WebUI estiver em Docker (como no teu AI-Lab2), os comandos de terminal, arquivo e MCP executam na máquina local, não no container. [Nousresearch](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/open-webui)

---

### OpenCode + Open-WebUI ⚠️ Sem integração direta

O OpenCode tem uma WebUI embutida no próprio binário e um desktop app oficial, mas não foi projetado para ser servido como backend de outro frontend. Ele é TUI/desktop-first — não expõe uma API compatível com OpenAI que o Open-WebUI possa consumir. [GitHub](https://github.com/nesquena/hermes-webui/blob/master/HERMES.md)

---

### Mapa de caminhos de GUI

| Ferramenta | Open-WebUI | GUI própria | Terminal |
| --- | --- | --- | --- |
| **Hermes Agent** | ✅ Nativo (via API server) | ❌ | ✅ |
| **OpenCode** | ❌ | ✅ WebUI embutida + desktop app | ✅ TUI |

---

### Recomendação para o teu AI-Lab2

Dado que já tens o Open-WebUI rodando via Docker no teu setup, o caminho mais limpo seria:

**Hermes Agent via Open-WebUI** — Ele se encaixa na tua arquitetura já existente sem criar um novo ponto de acesso. Vira essencialmente um "super-modelo" no dropdown que executa ferramentas no teu host CachyOS, com o Ollama (MI50) servindo os pesos.

**OpenCode separado** — Melhor usado como ferramenta de coding no próprio terminal quando estiveres desenvolvendo scripts do AI-Lab2, não como substituto de GUI. A TUI embutida ou o desktop app cobrem esse caso de uso.

Quer que eu detalhe o processo de instalação e configuração do Hermes Agent para o teu ambiente específico (CachyOS, Docker, ROCm, Ollama)?