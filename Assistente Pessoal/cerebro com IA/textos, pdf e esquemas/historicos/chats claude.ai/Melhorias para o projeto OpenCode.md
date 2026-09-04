---
title: "Melhorias para o projeto OpenCode"
source: "https://claude.ai/chat/21d2c8e5-5c90-40aa-baa4-11dcfc550b8f"
author:
published:
created: 2026-07-17
description: "Claude is Anthropic's AI, built for problem solvers. Tackle complex challenges, analyze data, write code, and think through your hardest work."
tags:
  - "clippings"
---
**Claude**

Antes de mais nada: os teus documentos antigos descrevem o Hermes como basicamente "controle remoto via Telegram" usando a API grátis da NVIDIA. Isso está desatualizado — o projeto cresceu bastante desde então, e isso muda a arquitetura que você desenhou (pra melhor, na maior parte). Vale eu te passar o estado atual antes de você ir mexer nos documentos antigos, porque parte do que tava planejado como gambiarra futura já vem pronto.

### O que mudou no Hermes

Hoje o Hermes já não é um wrapper fino em cima de um provider — ele tem tarefas agendadas via cron, delegação de sub-agentes com contexto isolado e toolsets restritos, execução de código via ferramenta própria, hooks de eventos e processamento em lote. Especificamente pro teu desenho:

- **"Cabeça" (Hermes) despachando sub-agentes locais**: já existe nativamente. A ferramenta `delegate_task` spawna instâncias filhas de agente com contexto isolado, toolset restrito e sessão de terminal própria, rodando até 3 sub-agentes concorrentes por padrão. E o roteamento de provider é por chamada — dá pra apontar um sub-agente específico pro teu Ollama local sem tocar no resto da config.
- **"Braços e pernas" (OpenCode)**: aqui tem uma sobreposição que você precisa decidir conscientemente. O Hermes já vem com execução de terminal, edição de arquivo e diagnósticos de código próprios — ele não *precisa* do OpenCode pra editar código. A razão legítima pra manter o OpenCode como camada separada é que ele já está configurado com o teu roteamento de modelo específico pro Ollama (o `opencode.json` que montamos nesta conversa) e tem o split plan/build que o Hermes não replica. Dá pra chamar de duas formas: Hermes rodando `opencode` como comando de terminal (mais simples, menos observável) ou via MCP, conectando a qualquer servidor externo sem precisar escrever ferramenta nativa — já que o OpenCode também roda como servidor web, essa ponte é direta. Eu recomendaria decidir isso antes de construir: se o Hermes mantém suas próprias ferramentas de terminal/arquivo *ligadas* enquanto delega pro OpenCode, você vai ter dois caminhos possíveis pra mexer no mesmo arquivo, o que quebra a rastreabilidade que teu SAFETY.md já persegue. Mais limpo: desligar terminal/file tools do Hermes especificamente pra esse projeto, forçando toda edição de código a passar pelo OpenCode.
- **"LLM paga pro vcoding" separada da LLM que a cabeça usa pra pensar**: isso é uma decisão de orçamento que vale documentar cedo. São dois gastos distintos — o Hermes pensando (pode ser um provider mais barato ou até via assinatura, ele funciona com qualquer provedor compatível com OpenAI, trocando modelo e provider no meio do fluxo sem mudar mais nada) e o OpenCode codando (aqui sim vale banda larga de contexto e qualidade). Não junta os dois numa métrica só, ou você não vai saber onde o custo tá vindo. [GitHub](https://github.com/mudrii/hermes-agent-docs)
- **"Artérias e vísceras" (VS Code)**: essa parte ficou mais literal do que você talvez esperasse — o Hermes tem integração nativa via ACP com VS Code, Zed e JetBrains, renderizando chat, diffs de arquivo e comandos de terminal dentro do próprio editor. Então o VS Code não é só onde a extensão do OpenCode mora — o Hermes também pode aparecer ali. Faz sentido com a tua metáfora: é o vaso que carrega os dois. [Nousresearch](https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server)

### Dois riscos reais que valem atenção antes de ligar tudo

**Custo composto na delegação**: a profundidade de delegação é limitada a 1-3 níveis, mas o custo escala multiplicativamente — no nível máximo com 3 filhos concorrentes por nível, a árvore pode chegar a 27 sub-agentes rodando ao mesmo tempo. Se a cabeça decidir autonomamente disparar sub-tarefas (o teu próprio exemplo do "corrija erros de tipagem toda sexta-feira" via cron), isso pode sair caro rápido se a profundidade não estiver travada em 1.

**Aprovação de escrita vem desligada por padrão**: tanto a aprovação de escrita de skills quanto o scanner de padrões perigosos em skills novas vêm desativados por padrão — decisão dos mantenedores porque fluxos legítimos que tocam ~/.ssh/ ou mencionam variáveis de API estavam disparando falso positivo demais. Dado que teu SAFETY.md já assume postura restritiva por padrão, isso é uma linha de config que você vai querer inverter manualmente, não assumir que já vem seguro. [GitHub](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/configuration.md)

### O que do AI-Lab antigo entra direto, sem reescrever

- **`permissions.yaml` / `SAFETY.md`** → vira a allowlist do que o Hermes pode acionar no `ai-lab` CLI e no OpenCode. A estrutura allow/ask/deny que você já tem é exatamente o padrão que o Hermes espera pra gate de comando perigoso.
- **`fit_rules.yaml`** → continua decidindo qual modelo Ollama vai pra qual sub-agente quando o Hermes despachar `delegate_task`.
- **`state_authority.py` / `event_bus.py` / `quotas.py`** (já prontos, testados nesta sessão) → seguem sendo a única verdade compartilhada entre Hermes, OpenCode e qualquer sub-agente — nenhuma das duas ferramentas tem isso nativamente entre si.
- **`adapters/opencode/config.json`** → é literalmente o `opencode.json` que já geramos, só falta decidir se o Hermes chama via MCP ou via terminal.

Quer que eu já desenhe a config do Hermes com os sub-agentes mapeados pros teus modelos Ollama (CODER/REASONER/FAST/HEAVY), ou prefere fechar a revisão dos documentos antigos primeiro e voltar com o que sobrou?

---

**You**

glm5.2 via opencode no dia a dia sub-agents de llm local para tarefas cada tarefa com a respectiva llm pra sua o hermes eu vou estudar um pouco mais

---

**Claude**

A resposta do Claude foi interrompida.

Tentar novamente

---

**You**

atualmente estou rodando isso apos formataçao

---

**Claude**

---

**You**

conclua

---

**Claude**

Bug confirmado empiricamente: com zero argumentos, as três flags continuam `false` — o caso "tudo" documentado no cabeçalho do script não existe na prática. Vou testar a correção antes de aplicar.