---
title: "Template de registry para agents e ferramentas"
source: "https://claude.ai/chat/8dff7b46-edc2-4fed-9ede-da135a92e8cd"
author:
published:
created: 2026-07-25
description: "Claude conversation with 6 messages"
tags:
  - "clippings"
---
**You**

criar template de registry para registro de agents, subagents, tools, mcp, skills

---

**Claude**

Fiz três arquivos:

- **agent-registry.schema.json** — o schema em si: define os campos obrigatórios pra qualquer `entry` (id, tipo, status, origem, proposito, modelo+fallback, regras.nao\_faz, validacao.gates, autonomia), com os `enum` já batendo com seu vocabulário (TRIVIAL→CRITICAL/FEATURE, safety-sha/attestation-gate/2-action-rule/3-strike-protocol/completion-gate, ativo/legado pra separar build-ECC de GSD).
- **agent-registry.example.json** — um entry preenchido de cada tipo (agent = gran-mestre, subagent = reviewer-rust, mcp = shared-brain/Obsidian, skill = archify, tool = safety-sha), pra você copiar o padrão em vez de começar do zero.
- **README-registry.md** — como validar com `ajv-cli`, o mapeamento direto pros seus hooks/gates existentes, e a diferença entre isso e o template de construção que você já tinha pedido antes (aquele descreve como construir uma entidade; este é o índice que o Gran-Mestre consulta em runtime pra saber o que existe).

A diferença mais importante pra não confundir os dois templates: este registry **referencia** a definição de cada entidade, não a substitui.

---

**You**

❯ opencode --port 59213 Configuration is invalid at /home/johncoffee/.config/opencode/agents/gran-mestre/templates/TEMPLATE-subagent.md ↳ Expected string | undefined, got {"primary":"\<modelo-principal-do-harness>","fallback\_chain":\["\<modelo-alternativo-1>","cloud:<provider/modelo>"\]} model

---

**Claude**

O erro é claro: o opencode está escaneando `~/.config/opencode/agents/` recursivamente e tentando validar **todo** `.md` ali dentro — inclusive o seu `TEMPLATE-subagent.md` dentro de `templates/` — como se fosse a definição real de um agent. E no schema nativo do opencode, `model` tem que ser **string** (`"provider/model-id"`), não um objeto com `primary` / `fallback_chain`.

Duas coisas erradas ao mesmo tempo:

**1\. Localização do template**  
O opencode não tem noção de "isso é só um template". Qualquer `.md` com frontmatter dentro da árvore de agents é tratado como agent real. Precisa tirar o template desse caminho:

```bash
mv ~/.config/opencode/agents/gran-mestre/templates \
   ~/.config/opencode/gran-mestre-templates
# ou, se quiser manter perto, prefixe com _ ou . — a maioria dos scanners ignora:
mv templates/TEMPLATE-subagent.md templates/.TEMPLATE-subagent.md.example
```

O mais seguro é mover pra fora da árvore `agents/` de vez — guardar em `docs/`, no vault do Obsidian, ou num repo separado. Templates não deveriam nunca estar num diretório que o harness varre como config ativa.

**2\. O campo `model` no template está no formato errado pro schema nativo**

O opencode espera:

```yaml
model: anthropic/claude-sonnet-4-5#high
```

não:

```yaml
model:
  primary: "<modelo-principal-do-harness>"
  fallback_chain: ["<modelo-alternativo-1>", "cloud:<provider/modelo>"]
```

Isso porque `fallback_chain` **não existe** no schema de agent do opencode core — isso é conceito do seu registry (ou do oh-my-opencode, que resolve fallback em `oh-my-opencode.json` separadamente, via sistema de categorias). Se você quer manter o conceito de fallback documentado no template, ele não pode ir no campo `model:` do frontmatter — vai como comentário/nota no corpo do markdown, ou você resolve o fallback de fato em `oh-my-opencode.json` /no seu registry, e o frontmatter do agent real só recebe o modelo primário já resolvido como string.

Template corrigido, versão mínima que passa validação:

```yaml
---
description: <descrição curta e específica>
mode: subagent
model: <provider>/<modelo-principal>
temperature: 0.3
---

<!-- fallback chain (resolvido pelo registry/oh-my-opencode, não pelo opencode core):
     1. <modelo-alternativo-1>
     2. cloud:<provider/modelo>
-->

<corpo do prompt do subagent>
```

Quer que eu gere o `TEMPLATE-subagent.md` completo já corrigido nesse formato, coerente com o registry que te passei antes?

---

**You**

❯ mv ~/.config/opencode/agents/gran-mestre/templates \\ ~/.config/opencode/gran-mestre-templates # ou, se quiser manter perto, prefixe com \_ ou. — a maioria dos scanners ignora: mv templates/TEMPLATE-subagent.md templates/.TEMPLATE-subagent.md.example mv: não foi possível obter estado de '/home/johncoffee/.config/opencode/agents/gran-mestre/templates': Arquivo ou diretório inexistente mv: não foi possível obter estado de 'templates/TEMPLATE-subagent.md': Arquivo ou diretório inexistente

---

**Claude**

Faz sentido checar o caminho real antes — o opencode pode estar resolvendo um `XDG_CONFIG_HOME` diferente, ou a pasta pode ter outro nome (`agent` no singular, por exemplo). Roda isso pra achar o arquivo de verdade:

```bash
find / -iname "TEMPLATE-subagent.md" 2>/dev/null
```

e também confere se `~/.config/opencode` aponta pra onde você acha que aponta:

```bash
echo $XDG_CONFIG_HOME
ls -la ~/.config/opencode
```

Também vale conferir se `agents` não é na verdade um symlink quebrado ou se o nome real da pasta é `agent` (singular) — o opencode v2 usa `agent/` no singular em alguns lugares e `agents/` em outros dependendo da versão/plugin (oh-my-opencode usa convenções próprias por cima do opencode core). Roda:

```bash
find ~/.config/opencode -maxdepth 3 -type d
```

Manda o resultado que eu ajusto o `mv` pro caminho certo.