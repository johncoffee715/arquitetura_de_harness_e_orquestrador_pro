# Auditoria Técnica — Workflow Gran-Mestre × CrossOver (OmO / Superpowers / Fable Method)

**Escopo:** auditoria de arquitetura do workflow de 6 fases + auditoria de segurança das Skills dos três frameworks-fonte.
**Fontes primárias consultadas diretamente (não por memória):** repositórios `code-yeongyu/oh-my-openagent`, `obra/superpowers`, `Sahir619/fable-method` (READMEs), `fable-method/install.sh`, `fable-method/skills/fable-method/SKILL.md`.
**Limitação declarada:** não consegui acessar `hooks/`/`scripts/` do Superpowers nem `postinstall.mjs` do OmO nesta sessão (bloqueio de acesso automatizado). Isso é sinalizado onde relevante — nenhuma afirmação de segurança é feita sobre arquivos que não abri de fato.

---

## 1. Visão Geral da Arquitetura

**Estado atual.** O Gran-Mestre comanda dois pipelines (Padrão e Cascata) sobre um harness "zíper" que intercala nomes próprios (Prometheus, Spec Writer, Plan Writer, Atlas, Implementer, Code Reviewer, Héstia, Atena, Verification) com três frameworks externos. Apenas o Pipeline Cascata está de fato descrito (6 fases, 4 gates); o Pipeline Padrão é citado mas nunca especificado.

**Funcionamento.** Cada fase empilha 1-3 "filtros" (lentes de validação sequenciais) antes do gate humano seguinte. Fases 1-3 não tocam código produtivo (SHA salvo ao final da Fase 3); Fases 4-6 tocam.

**Dependências reais (verificadas na fonte, não por inferência):**

| Framework | O que realmente é | Componentes confirmados |
|---|---|---|
| **OmO** (oh-my-openagent) | Harness de agentes reais com modelos dedicados | Sisyphus (orquestrador), Prometheus + Metis (planejador modo-entrevista + consultor), Oracle (arquitetura/debug), Librarian (docs/busca), Explore (grep rápido), Hephaestus (executor autônomo). Categorias de delegação: `visual-engineering`, `deep`, `quick`, `ultrabrain`. Team Mode opcional (off por padrão): líder + até 8 membros paralelos, skills `hyperplan` (5 críticos hostis pré-execução) e `security-research` (3 hunters + 2 PoC engineers) |
| **Superpowers** | Biblioteca de **13 skills** que disparam automaticamente — não são "agentes" | brainstorming, using-git-worktrees, writing-plans, subagent-driven-development/executing-plans, test-driven-development, requesting-code-review, receiving-code-review, finishing-a-development-branch, dispatching-parallel-agents, systematic-debugging, verification-before-completion, writing-skills, using-superpowers |
| **Fable Method** | **3 skills apenas**: pensar/agir/provar | `fable-method` (classificar → definir pronto → evidência → decidir → agir → verificar → reportar, com portão de trivialidade e adapters de domínio) · `fable-loop` (orquestração completa: subagentes de evidência paralelos → plano único aprovado → execução cirúrgica → verificadores adversariais → relatório auditado) · `fable-judge` (veredito adversarial VERIFIED/CAVEATS/REFUTED, com trap suite própria) |

Confirmação direta do seu próprio apontamento: **Atena e Héstia não existem em nenhum dos três repositórios** — nem como agente OmO, nem como skill Superpowers, nem como skill Fable Method.

---

## 2. Auditoria Técnica

**Pontos fortes**
- Gates posicionados nos pontos certos de não-retorno (direção → spec → plano → entrega).
- Separação Fases 1-3 (sem código) vs 4-6 (com código), com SHA salvo exatamente na fronteira — boa prática de segurança operacional.
- A metáfora de "filtros em zíper" é defesa em profundidade genuína quando os filtros são independentes.

**Pontos fracos / inconsistências (evidenciados, não especulados)**

1. **Prometheus mal posicionado.** No OmO real, Prometheus é o planejador em **modo entrevista** que constrói plano detalhado — isso é trabalho de Fase 3 (Plano), não de Fase 1 (decomposição leve). Você está chamando o agente mais caro do harness para o trabalho mais barato.
2. **`fable-method` subutilizado.** O Step 0 do skill (classificar: trivial? pergunta? tarefa? plano-primeiro?) e o portão de trivialidade são desenhados para rodar **antes de qualquer pipeline ser escolhido** — inclusive decidindo se vale abrir uma fase sequer. No seu workflow ele é só "filtro 1" dentro de uma Fase 1 de um pipeline já selecionado.
3. **`fable-judge` fora de escopo na Fase 2.** O mecanismo real do fable-judge é reexecutar verificações reivindicadas e diffar o que realmente mudou. Na Fase 2 (Contrato) só existe um documento de spec — não há diff nem verificação de código para auditar. Aplicar fable-judge aqui, sem o domain adapter de documentos, é usar a ferramenta fora do tipo de evidência que ela precisa.
4. **Héstia redundante com fable-judge.** Nas Fases 2, 3 e 6, ambos fazem "validação contra o pedido original / conformidade" — sem escopo diferenciado, é o mesmo trabalho em dobro.
5. **Atlas e Atena sem lastro.** Suas funções já existem no CrossOver sob outros nomes (seção 3) — inventá-los do zero contraria a própria filosofia de antropofagia tecnológica que rege o projeto.

**Redundâncias confirmadas:** Héstia × Fable Judge (Fases 2, 3, 6); Atlas × Sisyphus+git-master+Fable Loop (Fase 4 — você mesmo já identificou isso no documento original).

---

## 3. Engenharia Reversa

**Camada de despacho oculta, que deveria vir antes da Fase 1:**

```
pedido do usuário
   │
   ▼
fable-method Step 0 — classificar
   ├─ trivial (1 arquivo, <10 linhas, sem busca)?  → micro-loop: fazer, checar, relatar (sem fases)
   ├─ pergunta/avaliação?                          → responder, mudar nada
   ├─ requisitos claros (task)?                    → PIPELINE PADRÃO → entra direto na Fase 3
   └─ escopo aberto / plano-primeiro?               → PIPELINE CASCATA → Fase 1 completa
```

**Fluxo operacional remapeado para os agentes/skills reais** (o que cada nome do seu diagrama *deveria* invocar de fato):

| Fase | Nome no seu doc | Motor real recomendado |
|---|---|---|
| 1 — Descoberta | Prometheus | Explore/Librarian (OmO) para levantamento leve; **brainstorming** (Superpowers) já é literalmente "explora alternativas, dialoga, salva documento de design" |
| 2 — Contrato | Spec Writer / Héstia / fable judge | Saída do brainstorming vira o rascunho; Héstia audita rastreabilidade requisito↔spec; `fable-method` com domain adapter de design/documentos audita coerência (não fable-judge puro) |
| 3 — Plano | Plan Writer / Fable Loop / Héstia | **Prometheus + Metis** (OmO, agora no lugar certo) ou **writing-plans** (Superpowers); fable-loop decompõe em subtarefas |
| 4 — Execução | Atlas / Fable Loop / Implementer / Code Reviewer | **Sisyphus + skill git-master** (OmO) = "Atlas"; **Hephaestus** ou **subagent-driven-development** (Superpowers) = "Implementer"; **requesting-code-review/receiving-code-review** (Superpowers) já É revisão em dois estágios (conformidade → qualidade) = "Code Reviewer" |
| 5 — Revisão Macro | Atena / Fable Judge | **Oracle** (OmO) em modo pós-hoc = base de "Atena"; fable-judge audita contra o contrato |
| 6 — Entrega | Verification / Héstia / Fable Judge | Uso **canônico** de fable-judge (finalmente há diff e evidência para auditar) |

---

## 4. Análise de Problemas

**Causa raiz.** O CrossOver foi montado por analogia de *papel* ("isso parece um juiz", "isso parece um supervisor") em vez de por mapeamento de *mecanismo* (o que a ferramenta realmente observa e produz como evidência). Daí nascem os dois tipos de erro das seções 2-3: fase errada (Prometheus) e ferramenta fora do domínio de evidência (fable-judge na Fase 2).

**Impacto.** Nas Fases 2 e 6, Héstia + Fable Judge fazem trabalho sobreposto → custo de tokens/tempo sem ganho de cobertura. Na Fase 1, um Prometheus mal-configurado ou frustra a expectativa de leveza (se ele insistir no modo entrevista completo) ou subutiliza o agente mais capaz do harness na fase mais barata.

**Risco.** Enquanto Héstia e Atena não forem formalizadas com arquivo próprio, elas são "personas" invocadas ad-hoc dentro do prompt do Gran-Mestre: funcionam, mas não são testáveis isoladamente, não aparecem em nenhum registry, e não podem trocar de modelo (ex.: rodar Héstia no seu 27B local) sem reescrever o prompt inteiro.

**Efeito cascata.** Como o SHA só é salvo ao final da Fase 3 ("fases 1-3 não tocam código produtivo"), um Prometheus fazendo planejamento pesado cedo demais — antes do Gate 1 aprovar a direção — pode gerar retrabalho de plano inteiro se a direção for rejeitada. É desperdício computacional que se propaga fase a fase.

---

## 5. Predição

- **Gargalo futuro (IMPORTANTE):** sem arquivo versionado para Héstia/Atena, cada sessão nova reinterpreta o que elas fazem — deriva de prompt. Compare com fable-method/fable-judge, que têm SKILL.md fixo.
- **Limitação (IMPORTANTE):** os três frameworks evoluem rápido e de forma independente — OmO está em *Multi-Harness Agent OS Refactor* ativo agora, e um zíper hardcoded em nomes de agentes atuais (Sisyphus, Prometheus, Hephaestus) quebra silenciosamente se o upstream renomear ou reestruturar.
- **Escalabilidade (CRÍTICA para seu hardware):** seu setup local de 16GB VRAM é teto real para quantos agentes "pesados" (Prometheus modo-entrevista, Hephaestus autônomo) rodam em paralelo. O Team Mode do OmO permite até 8 membros simultâneos — isso provavelmente excede sua VRAM se cada membro precisar de contexto de 27B carregado, e isso não está refletido em nenhum lugar do workflow atual.
- **Ponto de falha (IMPORTANTE):** os MCPs injetados em runtime pelo OmO (Exa, Context7, Grep.app) **não aparecem em `opencode mcp list`** — isso é admitido pela própria documentação do projeto, não é suposição minha. Se observabilidade é um dos seus 12 pilares, esse é um ponto cego já documentado que seu workflow ainda não monitora.

---

## 6. Prevenção

- Formalizar Héstia e Atena com arquivo próprio (Anexo A) antes da próxima sessão de produção — evita deriva de prompt. **CRÍTICA**
- Fixar (pin) commit/tag das três dependências externas — os três têm alta velocidade de release (OmO: 222 releases; Superpowers: v6.1.1 há poucas semanas). **IMPORTANTE**
- Checagem de orçamento de VRAM antes de habilitar Team Mode com múltiplos membros paralelos. **IMPORTANTE**
- Rodar `fable-method` Step 0 antes da escolha de pipeline, não dentro da Fase 1. **CRÍTICA**

---

## 7. Correção

| # | Mudança | Classificação | Prós | Contras | Risco | Impacto técnico |
|---|---|---|---|---|---|---|
| 1 | Mover Prometheus da Fase 1 → Fase 3 | **CRÍTICA** | Usa o agente no papel para o qual foi desenhado; libera Fase 1 para exploração barata | Exige reescrever a chamada na Fase 1 | Baixo — muda *quando*, não *como* | Nenhuma mudança de infraestrutura, só de sequência |
| 2 | Diferenciar escopo Héstia (requisito↔spec) vs Fable Judge (evidência↔alegação) | **CRÍTICA** | Elimina trabalho duplicado nas Fases 2/3/6 | Exige documentar o contrato de cada uma (Anexo A) | Baixo | Reduz custo de tokens por fase |
| 3 | Trocar "fable judge" solto na Fase 2 por `fable-method` + domain adapter de documentos | **IMPORTANTE** | Usa a ferramenta certa para o tipo de artefato (spec, não diff) | Precisa validar se seu domain adapter cobre "spec de arquitetura" | Baixo-médio | Fable-judge só entra a partir da Fase 5, com evidência real |
| 4 | Promover `fable-method` Step 0 para despachante pré-Fase-1 | **IMPORTANTE** | Decide Padrão/Cascata/execução-direta sem gastar uma fase inteira nisso | Exige definir explicitamente o Pipeline Padrão (hoje inexistente) | Baixo | Ver Anexo C |
| 5 | Registrar Atlas como alias de Sisyphus+git-master (não agente novo) | **OPCIONAL** | Herda updates do upstream automaticamente | Perde o "nome próprio" no diagrama | Nenhum | Só documentação, zero código |
| 6 | Registrar Atena como composição sobre Oracle (não invenção do zero) | **OPCIONAL** | Aproveita o que já existe (antropofagia tecnológica) | Precisa de prompt adicional de "coerência cross-task" sobre Oracle | Baixo | Um SKILL.md a mais (Anexo A) |
| 7 | Acompanhar o Multi-Harness Refactor do OmO | **FUTURA** | Pode simplificar o zíper quando a separação de camadas estabilizar | Nenhum agora | N/A | Reavaliar quando o ROADMAP fechar |

---

## 8. Refatoração

- **Simplificação:** em cada fase, apenas uma camada deve responder por "conformidade contra o pedido original" — não duas. Exceção real: Fase 6, onde Héstia (requisito) e Fable Judge (evidência) têm papéis genuinamente distintos e ambos se justificam.
- **Modularização:** dar a Héstia e Atena o mesmo padrão de arquivo que os três frameworks-fonte já usam — frontmatter (`name`/`description`/`trigger`) + corpo em Markdown, exatamente como o `fable-method/SKILL.md` que você está usando como referência (Anexo A já segue esse padrão).
- **Redução de complexidade:** a numeração ad-hoc dos filtros ("filtro 1", "filtro 1.5", "filtro 2 macro", "filtro 3 — o último") não escala. Nomear por função (`spec-conformance`, `evidence-audit`, `code-quality`) facilita tanto o registry quanto a leitura por qualquer subagente novo.
- **Melhoria arquitetural:** o Pipeline Padrão nunca foi de fato especificado — hoje todo pedido, mesmo com requisito claro, paga o custo das 6 fases do Cascata. Corrigir isso é estrutural, não cosmético (ver Anexo C).

---

## 9. Integração

**Compatibilidade com seu projeto:** nenhuma correção proposta troca OmO, Superpowers ou Fable Method — são apenas correções de *mapeamento* (qual agente/skill real cobre qual papel) e de *formalização* (dar arquivo a Héstia/Atena). Zero reescrita de infraestrutura.

**Impacto nos módulos existentes:** a única mudança de comportamento observável é o reposicionamento do Prometheus — muda *quando* ele é chamado, não como ele funciona internamente.

**Plano de migração (Ctrl+A / Ctrl+C / Ctrl+V / Ctrl+S):**
1. Copiar os blocos YAML do **Anexo A** para o seu arquivo de registry de agents (ajuste as chaves ao schema exato do seu registry — não tenho visibilidade do arquivo real).
2. Substituir o diagrama de fases atual pelo do **Anexo C**.
3. Salvar. Nenhuma outra mudança de código é necessária nesta rodada.

---

## 10. Comparação

| Aspecto | Original | Corrigido | Benefício obtido |
|---|---|---|---|
| Fase 1 | Prometheus (papel "leve" que não é o real) | Explore/Librarian + brainstorming | Agente certo na fase certa |
| Fase 2 | Héstia + Fable Judge (mesma função) | Héstia (requisito↔spec) + fable-method/adapter (coerência do doc) | Elimina duplicidade de auditoria |
| Despacho de pipeline | Implícito, dentro da Fase 1 | `fable-method` Step 0, explícito, antes de qualquer fase | Padrão/Cascata/execução-direta decidido sem custo de fase |
| Atlas / Atena | Agentes "do zero", sem arquivo | Aliases/composições registradas sobre Sisyphus e Oracle | Herdam updates do upstream; aparecem no registry |
| Pipeline Padrão | Citado, nunca definido | Definido explicitamente (Anexo C) | Requisitos claros não pagam custo de 6 fases |

---

## 11. Melhorias Técnicas

- **Imediatas:** registrar Héstia/Atena (Anexo A); mover Prometheus; inserir o despacho `fable-method` Step 0 antes da Fase 1.
- **Médio prazo:** pin de versão das três dependências externas + monitoramento de changelog; checagem de orçamento de VRAM antes do Team Mode.
- **Longo prazo:** acompanhar o *Multi-Harness Agent OS Refactor* do OmO e reavaliar o zíper quando a separação de camadas (core/MCP/skills/adapters) estabilizar — parte do seu CrossOver pode se tornar nativa.

---

## 12. Roadmap

Próxima evolução recomendada: instrumentar observabilidade sobre os MCPs que o OmO injeta em runtime (Exa/Context7/Grep.app) e que hoje não aparecem em `opencode mcp list` — essa lacuna já é admitida pela documentação upstream, e resolvê-la é o próximo passo natural depois de estabilizar este zíper corrigido, já que observabilidade é um dos seus 12 princípios declarados.

---

## 13. Checklist

- ✔ **Implementado:** nada ainda — esta é a primeira formalização do zíper.
- ✔ **Corrigido nesta auditoria:** mapeamento de fase do Prometheus; escopo diferenciado Héstia vs Fable Judge; posição do despacho `fable-method` Step 0.
- ✔ **Pendente (seu lado):** colar o Anexo A no registry real; substituir o diagrama de fases pelo Anexo C.
- ✔ **Futuro:** checagem de orçamento de VRAM para Team Mode; pin de versões; observabilidade dos MCPs runtime do OmO.

---

## 14. Entrega

Os anexos abaixo são o artefato Plug-and-Play: Ctrl+A, Ctrl+C, Ctrl+V no seu registry/config, Ctrl+S.

---

### Anexo A — Registro de Agents (adaptar chaves ao schema real do seu registry)

```yaml
# Héstia — CRIAR (necessidade real confirmada: escopo distinto de fable-judge)
name: hestia
description: >
  Valida rastreabilidade requisito -> especificação (não evidência de execução,
  isso é papel do fable-judge). Confere se o spec/plano ainda corresponde ao
  pedido original do usuário e se cobertura/contratos/verificabilidade estão
  completos antes de cada gate.
trigger: interno (chamado pelo Gran-Mestre ao final das Fases 2, 3 e 6)
escopo: requisito <-> spec (rastreabilidade)
não_faz: reexecutar verificações, diffar código, caçar fraude de conclusão (isso é fable-judge)
modelo_sugerido: pode rodar em modelo local menor (ex.: 27B) — tarefa é comparação
  textual estruturada, não geração criativa nem raciocínio profundo de código

---

# Atena — CRIAR COMO COMPOSIÇÃO sobre Oracle (não invenção do zero)
name: atena
description: >
  Oracle (OmO) em modo pós-hoc, com prompt adicional focado em coerência
  cross-task e acoplamento do diff total — não substitui Oracle, adiciona
  a lente de "revisão holística de todas as tasks juntas" que o Oracle
  genérico não cobre sozinho.
base: oracle (oh-my-openagent)
trigger: interno (chamado pelo Gran-Mestre ao final da Fase 5)
escopo: coerência arquitetural cross-task, acoplamento
não_faz: validar conformidade contra o pedido original (isso é Héstia/fable-judge)

---

# Atlas — NÃO CRIAR como agente novo; registrar como alias operacional
name: atlas
alias_de: sisyphus + skill:git-master (oh-my-openagent)
motivo: função já coberta 1:1 pelo orquestrador principal do OmO combinado
  com a skill de commits atômicos; você mesmo identificou essa redundância
  no documento original ("Atlas já é, na prática, um Fable Loop manual")
```

### Anexo B — Auditoria de Segurança das Skills (o que foi verificado de fato, e o que não)

| Framework | Arquivos abertos diretamente nesta sessão | Veredito | Base do veredito |
|---|---|---|---|
| **Fable Method** | `install.sh` (16 linhas), `skills/fable-method/SKILL.md` (111 linhas) | **Seguro**, com verificação direta | `install.sh` só copia pastas para `~/.claude/skills` — sem `curl\|bash`, sem `eval`, sem chamada de rede, sem `sudo`. O SKILL.md é texto puro de instrução (prompt), sem código executável embutido |
| **Superpowers** (`superpowers-brainstorming/scripts/{start,stop}-server.sh`) | Verificado por auditoria local do usuário (shellcheck) + changelog/issues upstream cruzados por mim | **Seguro**, com ressalva de versão | `rm -rf "$SESSION_DIR"` e `kill -9 "$pid"` são o ciclo de vida documentado do servidor local do *visual companion* do brainstorming (serve HTML de mockups). O upstream confirma: `SESSION_DIR` é um subdiretório escopado em `/tmp/` (ou `.superpowers/brainstorm/<pid>-<ts>/` com `--project-dir`), e o `kill -9` é a escalada documentada de SIGTERM→SIGKILL após timeout de shutdown gracioso (changelog PR #723). shellcheck só achou SC2164/SC2034 — estilo, não segurança |
| **OmO** | Não consegui abrir `postinstall.mjs` nesta sessão (acesso automatizado bloqueado) | **Não verificado diretamente** — ressalva concreta já admitida pelo próprio projeto: MCPs injetados em runtime (Exa/Context7/Grep.app) não aparecem em `opencode mcp list`. Telemetria é documentada com granularidade (hash SHA256, sem hostname bruto, opt-out por env var) | Monorepo grande (11k+ commits, refactor ativo) — auditoria exaustiva de terceiros em uma sessão não é realista; recomendo não habilitar Team Mode/`security-research` de forma irrestrita e revisar `postinstall.mjs` localmente antes de rodar em produção |
| **browser-use** (`mcp_bridge.py`, terceiro não-CrossOver, achado no inventário local) | Verificado por bandit (auditoria local do usuário) | **Aceitável com 2 correções pendentes** | B108: `/tmp/browser-use/screenshots` é caminho fixo, não randomizado por sessão — trocar por `tempfile.mkdtemp()`. B603: `subprocess.run(cmd, shell=False)` é o padrão *seguro* (bandit só pede confirmação); risco real depende de como `cmd` é montado — preciso do arquivo completo para confirmar que argumentos não vêm de conteúdo de página não sanitizado |

**Resposta direta à pergunta "é seguro usar" (atualizada com dados reais do disco, 27/07/2026):** Fable Method — sim, verificado diretamente. Superpowers (os 2 scripts encontrados) — sim, os dois achados do `findings.tsv` têm explicação documentada no upstream, não são indício de comportamento oculto. browser-use/mcp_bridge.py — aceitável, com 2 ajustes de hardening pendentes (tabela acima). OmO — segue não verificado por mim; sinais públicos favoráveis, sem auditoria de código de fato. **Ponto em aberto de maior prioridade:** o próprio script do usuário aponta 4 scripts "de ecc-autofagia" (a própria implementação do safety protocol) como nunca cobertos por auditoria anterior — isso ainda não foi revisado linha a linha por mim; ver seção "Ação prioritária" na resposta.

**Divergência de inventário (89 vs. relatórios anteriores de 3/72/84):** o próprio script do usuário trata o scan de 27/07 como a contagem real em disco agora; eu não tenho visibilidade do que gerou os números anteriores, então não posso explicar a origem da divergência — apenas registrar que 89 SKILL.md / 4 scripts é o número a tratar como atual daqui em diante.

**Lacuna de cobertura de linguagem (achado meu, não do script do usuário):** shellcheck cobre `.sh` e bandit cobre `.py` — juntos isso só explica 3 dos 4 scripts do inventário (2 `.sh` do brainstorming + 1 `.py` do browser-use). A própria pasta `scripts/` do brainstorming no upstream também contém `server.cjs` e `helper.js` — se o 4º script contado for um desses (JavaScript), ele teve **zero cobertura de análise estática** nesta auditoria, já que nem shellcheck nem bandit tocam `.js`/`.cjs`. Vale confirmar a identidade do 4º arquivo e, se for JS, rodar `eslint` com plugin de segurança ou `semgrep --config=auto` (cobre bash/python/JS numa passada só). **IMPORTANTE.**

**Ação prioritária — os 4 scripts "de ecc-autofagia":** o aviso final do seu próprio script chama atenção para revisão manual dos scripts que implementam o safety protocol em si, nunca cobertos por auditoria externa. Isso é exatamente o ponto que shellcheck/bandit não conseguem resolver sozinhos (a ressalva "zero achados não significa seguro" no seu próprio output é literal: nenhum dos dois pega instrução manipulativa em texto nem exfiltração em duas etapas). Preciso do conteúdo completo desses arquivos — não apenas grep/linter — para fazer essa revisão de verdade. **CRÍTICA — próximo passo antes de qualquer outra ação neste ambiente.**

### Anexo C — Pipeline Padrão (definido explicitamente, ausente no documento original)

```
PIPELINE PADRÃO (requisitos claros — despachado pelo fable-method Step 0)

  entra direto na FASE 3 — PLANO
    Prometheus + Metis (OmO) ou writing-plans (Superpowers)
    >>> Fable Loop: decompõe em sub-tasks
    >>> Héstia: valida cobertura/contratos
  ⏸️ GATE 3 (único gate antes da execução — Fases 1-2 puladas por design,
     já que a direção e o contrato já eram claros no pedido original)
  💾 SHA salvo aqui

  FASE 4 — EXECUÇÃO  (idêntica ao Cascata)
  FASE 5 — REVISÃO MACRO  (idêntica ao Cascata)
  FASE 6 — ENTREGA  (idêntica ao Cascata)
```

---

### Anexo D — Auditoria dos scripts ECC-Autofagia (a partir de `AUDIT_ECC_AUTOFAGIA.md`, 27/07/2026)

**Ressalva de proveniência (importante):** o arquivo enviado é um **relatório sobre** os 6 scripts (`ecc-autofagia.sh`, `ecc-attest.sh`, `ecc-complete.sh`, `ecc-digest.sh`, `attest-plan.sh`, `check-plan-complete.sh`), não o código-fonte bruto deles. Eu não li o bash/python real — analisei os trechos e conclusões desse relatório. Isso significa: a análise abaixo é uma **auditoria da auditoria**, não uma verificação independente linha a linha. Para essa segunda camada, preciso do conteúdo bruto dos 6 arquivos.

**CRÍTICA — corrobora o achado principal, com correção da correção proposta.** A injeção em `json_log()` (`ecc-digest.sh`) é uma vulnerabilidade real e séria, pelo trecho mostrado: `$msg`/`$type` são interpolados dentro de uma string Python delimitada por `'''`, sem qualquer sanitização — uma aspa simples no valor quebra o literal e o texto seguinte vira código Python executado. Isso é injeção de código clássica (mesma família de SQL injection por concatenação), não uma questão de estilo.

- A correção com `printf '%s'` que o relatório propõe **remove a execução de código, mas não resolve tudo**: `printf` não faz JSON-escaping. Uma `$msg` contendo `"` gera JSON malformado; uma `$msg` como `x", "type":"malicious` produz JSON *sintaticamente válido* com uma chave `type` duplicada e sobrescrita — ou seja, ainda dá para injetar estrutura no log, só que sem execução de código.
- **Use a correção `jq --arg`** que o próprio relatório também sugere (a segunda opção) — essa sim escapa corretamente. Não adote a versão `printf` como fix final.
- `$TIMESTAMP` especificamente tem risco prático baixo mesmo sem fix — é gerado internamente por `date +%Y-%m-%d_%H-%M-%S`, formato fixo sem caracteres especiais. O relatório o inclui no mesmo achado que `$msg`/`$type`, mas o vetor de exploração real está nesses dois, não em `$TIMESTAMP`.

**IMPORTANTE — achado #19 (path via `$type`) ficou sem correção proposta.** O relatório identifica que `$type` entra direto em `"$ECC_LOG/$type.jsonl"` sem sanitização, mas a seção 4 (Correções Propostas) só cobre os achados #17/#18 e #6/#9 — não há um fix para #19. Recomendo validar `$type` contra um allowlist fixo (`^[a-zA-Z0-9_-]+$` ou uma lista literal de valores conhecidos) antes de usá-lo em qualquer caminho de arquivo.

**IMPORTANTE — inconsistências internas do próprio relatório de auditoria** (o tipo de coisa que o princípio "releia como revisor hostil" do fable-method existe para pegar):
- Achado #6 é rotulado **CRÍTICO** no corpo do texto (seção 2.2), mas reclassificado como **MÉDIO** na tabela-resumo — e não aparece na tabela de Críticos, que lista só #17/#18.
- Achado #5 (health check não verifica integridade SHA) é descrito na seção 2.1 mas **desaparece** das três tabelas-resumo — não está em Críticos, Médios nem Baixos.
- Os cabeçalhos "Médios (5)" e "Baixos (8)" não batem com as linhas reais dessas tabelas (6 e 13, respectivamente).
- O total final declarado ("2 críticos, 5 médios, 8 baixos" = 15) não reconcilia com os 22 achados numerados no corpo do documento nem com os 21 que de fato aparecem somando as três tabelas.
- Nenhum desses pontos invalida o achado crítico principal (a injeção é real pelo código mostrado), mas reforça por que uma auditoria de segundo grau não substitui ler o script bruto.

**CRÍTICA — a seção 5 do próprio relatório (verificação de integridade dos scripts) nunca foi executada.** Os 6 hashes SHA-256 estão como `[a ser calculado]` — literalmente um placeholder. Essa é a pergunta que mais importa aqui ("os scripts do safety protocol foram adulterados?") e continua sem resposta. Rodar isso é o próximo passo de maior prioridade, antes de tratar qualquer parte deste relatório como definitiva.

**Próximo passo recomendado, em ordem:**
1. Rodar `ecc-attest.sh store` (ou `sha256sum`) nos 6 scripts agora e guardar o hash — fecha a seção 5 do relatório recebido.
2. Colar aqui o conteúdo bruto de `ecc-digest.sh` (pelo menos a função `json_log` completa e todos os call sites que passam `$type`) para eu confirmar a correção e verificar se algum caller usa valor não-literal para `$type`.
3. Aplicar o fix `jq --arg` (não o `printf`) e o allowlist de `$type`.

---

*Fim do relatório.*
