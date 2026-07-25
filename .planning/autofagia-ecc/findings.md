# Findings & Decisions — Autofagia do ECC (affaan-m/ECC)

## Requirements
- Aplicar autofagia ao repositório ECC (230K ⭐)
- Identificar gaps na arquitetura de hooks, agents e skills
- Propor melhorias baseadas em Gran-Mestre + planning-with-files + Claude-Mem
- Criar scripts de integração cross-harness

## Research Findings

### O que é ECC?
ECC (Everything Claude Code) é um **sistema de otimização de performance para harnesses de agentes AI**. Vencedor de hackathon da Anthropic, com 10+ meses de desenvolvimento intensivo.

**Estatísticas:**
- ⭐ 230.000+ estrelas no GitHub
- 🧠 67 agentes especializados (planner, code-reviewer, tdd-guide, architect, etc.)
- 📋 261+ skills workflows
- 🔌 30+ lifecycle hooks
- 🌐 Suporte a 8+ harnesses (Claude Code, Codex, Cursor, OpenCode, Gemini, Zed, Copilot, OpenClaw)
- 📦 297 releases em 10 meses
- 👥 110 contribuidores

### Arquitetura ECC
```
ECC/
├── .claude-plugin/       # Plugin e marketplace manifests
├── agents/               # 67 subagentes especializados
├── skills/               # 261+ workflows (primary surface)
├── commands/             # Slash commands (/tdd, /plan, /e2e, etc.)
├── hooks/                # Lifecycle hooks (30+)
│   ├── hooks.json        # Config principal
│   ├── memory-persistence/  # Hooks de sessão
│   ├── strategic-compact/   # Sugestões de compactação
│   └── README.md         # Documentação
├── rules/                # Regras universais + linguagem-específicas
│   ├── common/           # Princípios universais (sempre instalar)
│   ├── typescript/       # TypeScript/JavaScript
│   ├── python/           # Python
│   ├── golang/           # Go
│   └── ...               # 10+ linguagens
├── scripts/              # Utilitários Node.js
├── tests/                # Suite de testes
├── contexts/             # Injeção de contexto dinâmico
├── mcp-configs/          # Configurações MCP
└── ecc_dashboard.py      # Dashboard Tkinter
```

### Inovações do ECC vs Gran-Mestre

#### 1. Continuous Learning v2 (ECC-only)
ECC tem um sistema de aprendizado contínuo baseado em **instintos**:
- Observa ferramentas usadas (PreToolUse + PostToolUse)
- Extrai padrões com thresholds de confiança
- Cria instintos (regras automáticas) com metadados de confiança
- Promove instintos para skills quando maduros

**Comparação:** Gran-Mestre não tem equivalente. Claude-Mem é memória, não aprendizado.

#### 2. Cross-Harness Architecture (ECC-only)
ECC é projetado para funcionar em **múltiplos harnesses** com adaptadores:
- Claude Code (plugin nativo)
- Codex (plugin metadata + AGENTS.md)
- Cursor (regras adaptadas)
- OpenCode (plugin/event system adapter)
- Gemini (superfície de compatibilidade)

**Comparação:** Gran-Mestre é específico OpenCode. ECC é multi-harness.

#### 3. Hook Runtime Controls (ECC-only)
ECC permite controle de hooks via **variáveis de ambiente**:
- `ECC_HOOK_PROFILE` — minimal/standard/strict
- `ECC_DISABLED_HOOKS` — desabilitar hooks específicos
- `ECC_GATEGUARD` — gate de segurança
- `ECC_SESSION_START_MAX_CHARS` — limite de contexto

**Comparação:** Gran-Mestre tem gates fixos, não configuráveis por env vars.

#### 4. Async Hooks (ECC-only)
ECC suporta hooks **assíncronos** que não bloqueiam a execução:
```json
{
  "type": "command",
  "command": "node slow-hook.js",
  "async": true,
  "timeout": 30
}
```

**Comparação:** Gran-Mestre não tem hooks assíncronos.

#### 5. Strategic Compaction (ECC-only)
ECC tem sugestões de compactação estratégica para reduzir tokens:
- Análise de observações acumuladas
- Sugestões de resumo
- Preparação para nova sessão

**Comparação:** Claude-Mem faz compactação semântica, ECC faz estratégica.

### Inovações do Gran-Mestre não presentes no ECC

| Inovação Gran-Mestre | Descrição | Gap no ECC | Prioridade | Status |
|---|---|---|---|---|
| **Attestation (SHA-256)** | Verificação de integridade de planos | 🔴 Não existe | Alta | ✅ CORRIGIDO |
| **Completion Gate** | Verifica se plano está completo | 🟡 Parcial (ECC_GATEGUARD) | Alta | ✅ CORRIGIDO |
| **2-Action Rule** | Salvar findings a cada 2 ações | 🔴 Não existe | Média | ✅ CORRIGIDO |
| **3-Strike Protocol** | 3 tentativas antes de escalar | 🟡 Parcial (retry embutido) | Média | ✅ CORRIGIDO |
| **SKILL.md padrão** | Metadados YAML + regras | 🟡 Migração em andamento | Média | ✅ CORRIGIDO |
| **Safety SHA rollback** | SHA antes de executar | 🔴 Não existe | Alta | ✅ CORRIGIDO |
| **Cerebral Memory** | Shared Brain pós-pipeline | 🟡 Parcial (continuous learning) | Média | 🟡 Pendente |

### Inovações do planning-with-files não presentes no ECC

| Inovação PWF | Descrição | Gap no ECC |
|---|---|---|
| **planning-with-files** | Arquivos de plano persistentes | 🟡 Skills já fazem isso parcialmente |
| **Ledger JSONL** | Rastreamento append-only | 🔴 Não existe |
| **Session Recovery** | Recuperação de sessão via timestamps | 🟡 Parcial (memory-persistence) |
| **UserPromptSubmit Hook** | Injeção de plano a cada prompt | 🟡 Não explicita |

### Inovações do Claude-Mem não presentes no ECC

| Inovação Claude-Mem | Descrição | Gap no ECC |
|---|---|---|
| **Memória persistente vetorial** | Chroma + SQLite FTS5 | 🟡 Usa JSONL + instintos |
| **MCP Search Tools** | search/timeline/get_observations | 🔴 Não existe |
| **Web Viewer UI** | Dashboard em tempo real | 🟡 Tem dashboard Tkinter |
| **Cloud Sync** | Backup para cmem.ai | 🔴 Não existe |
| **Compressão semântica AI** | Resumo automático de sessões | 🟡 Strategic compaction é manual |

### Análise de Integração

```
                    ┌─────────────────┐
                    │   Gran-Mestre   │
                    │  (Orquestrador) │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
     ┌──────────────┐ ┌──────────┐ ┌──────────────┐
     │     ECC      │ │Claude-Mem│ │ Planning-w-F  │
     │ (Performance)│ │ (Memory) │ │  (Filesystem) │
     └──────────────┘ └──────────┘ └──────────────┘
```

**Os quatro sistemas são complementares:**
1. **Gran-Mestre** — Orquestrador de alto nível, plano-delegação-revisão
2. **ECC** — Otimização de harness, agents, skills, hooks, regras
3. **Claude-Mem** — Memória persistente vetorial cross-sessão
4. **Planning-with-Files** — Planejamento baseado em arquivos (SHA, gates)

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| Criar scripts de autofagia ECC localmente | Não é possível fazer PR no repo remoto, mas scripts de análise são úteis |
| Foco em Attestation + Completion Gate | São os gaps mais críticos e já implementamos no Gran-Mestre |
| Integração cross-harness via adapter pattern | ECC já tem adapters; autofagia deve seguir mesma arquitetura |
| Documentar protocolos separadamente | ECC tem documentação própria robusta; protocolos devem complementar |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| ECC tem 30+ hooks que podem conflitar | Usar hooks específicos de autofagia com prefixo `ecc-autofagia-` |
| Continuous learning v2 pode competir com autofagia | Autofagia opera em nível meta (analisar o sistema), não no mesmo nível |
| Cross-harness testing complexo | Focar em Claude Code + OpenCode como harnesses primários |

## Resources
- ECC Repo: https://github.com/affaan-m/ECC
- ECC Docs: https://github.com/affaan-m/ECC/tree/main/docs
- Gran-Mestre: ~/.opencode/agent/gran-mestre.md
- Claude-Mem: https://github.com/thedotmack/claude-mem
- Planning-with-Files: https://github.com/OthmanAdi/planning-with-files

### Checkpoint 11:18:15

### Checkpoint 12:00:14

### Checkpoint 12:05:06

### Checkpoint 12:08:44

### Checkpoint 12:09:27

### Checkpoint 12:09:29

### Checkpoint 12:55:20

### Checkpoint 13:13:33

### Checkpoint 13:13:40

### Checkpoint 13:13:42

### Checkpoint 13:13:42

### Checkpoint 13:13:43

### Checkpoint 13:13:45

### Checkpoint 13:13:46

### Checkpoint 13:13:47

### Checkpoint 13:13:48

### Checkpoint 13:13:49

### Checkpoint 13:13:50

### Checkpoint 13:13:52

### Checkpoint 13:13:53

### Checkpoint 13:13:55

### Checkpoint 13:13:56

### Checkpoint 13:13:57

### Checkpoint 13:13:59

### Checkpoint 13:14:00

### Checkpoint 13:16:21




### Checkpoint 15:04:45
### Checkpoint 15:04:45
### Checkpoint 15:04:45
### Checkpoint 15:04:45

### Checkpoint 15:27:15

### Checkpoint 18:37:46

### Checkpoint 19:19:41

### Checkpoint 19:19:45

### Checkpoint 19:20:43

### Checkpoint 19:20:48

### Checkpoint 20:10:33

### Checkpoint 20:18:27

### Checkpoint 20:20:10


### Checkpoint 20:23:58
### Checkpoint 20:23:58

### Checkpoint 20:26:07

### Checkpoint 20:35:06

### Checkpoint 20:35:06

### Checkpoint 21:43:08

### Checkpoint 23:08:15

### Checkpoint 00:03:50

### Checkpoint 00:36:19

### Checkpoint 21:35:30

### Checkpoint 22:43:44

### Checkpoint 23:04:27

### Checkpoint 00:28:43

### Checkpoint 00:29:14

### Checkpoint 00:29:22

### Checkpoint 00:30:31

### Checkpoint 00:50:54

### Checkpoint 00:54:29

### Checkpoint 00:55:14

### Checkpoint 00:55:33

### Checkpoint 00:57:43

### Checkpoint 00:58:37

### Checkpoint 00:59:01

### Checkpoint 01:37:20

### Checkpoint 01:37:22

### Checkpoint 01:37:23

### Checkpoint 01:37:23

### Checkpoint 01:37:27

### Checkpoint 01:38:23

### Checkpoint 01:38:34

### Checkpoint 01:38:34

### Checkpoint 01:38:34

### Checkpoint 01:38:35



### Checkpoint 01:38:43
### Checkpoint 01:38:43
### Checkpoint 01:38:43

### Checkpoint 01:38:53

### Checkpoint 01:39:04

### Checkpoint 01:39:13

### Checkpoint 01:39:23

### Checkpoint 01:53:31

### Checkpoint 01:53:31

### Checkpoint 01:53:33

### Checkpoint 01:53:34


### Checkpoint 01:53:41
### Checkpoint 01:53:41

### Checkpoint 01:53:43



### Checkpoint 01:56:25
### Checkpoint 01:56:25
### Checkpoint 01:56:25

### Checkpoint 01:56:25

### Checkpoint 01:56:27


### Checkpoint 01:56:41
### Checkpoint 01:56:41

### Checkpoint 01:57:55

### Checkpoint 01:57:56

### Checkpoint 01:58:02

### Checkpoint 01:58:02

### Checkpoint 01:58:10

### Checkpoint 02:08:04

### Checkpoint 02:08:05

### Checkpoint 02:08:14

### Checkpoint 02:08:26

### Checkpoint 02:08:27

### Checkpoint 02:08:37

### Checkpoint 02:09:07

### Checkpoint 02:09:07

### Checkpoint 02:09:24

### Checkpoint 02:09:35

### Checkpoint 02:09:35

### Checkpoint 02:09:44

### Checkpoint 02:09:54

### Checkpoint 02:09:55


### Checkpoint 02:10:13
### Checkpoint 02:10:13

### Checkpoint 02:10:22

### Checkpoint 02:10:33

### Checkpoint 03:11:04


### Checkpoint 03:11:04
### Checkpoint 03:11:04

### Checkpoint 03:14:27

### Checkpoint 03:14:28

### Checkpoint 03:16:16


### Checkpoint 03:16:32
### Checkpoint 03:16:32

### Checkpoint 03:17:01

### Checkpoint 03:17:20

### Checkpoint 03:51:14

### Checkpoint 03:51:14

### Checkpoint 03:51:21

### Checkpoint 03:51:21

### Checkpoint 03:51:22

### Checkpoint 03:51:39

### Checkpoint 03:51:40

### Checkpoint 03:51:40

### Checkpoint 03:51:43

### Checkpoint 03:51:44

### Checkpoint 03:51:48

### Checkpoint 03:51:48

### Checkpoint 03:51:53

### Checkpoint 03:51:53

### Checkpoint 03:51:58

### Checkpoint 03:52:01


### Checkpoint 03:52:02
### Checkpoint 03:52:02

### Checkpoint 03:52:05

### Checkpoint 03:52:05

### Checkpoint 03:52:06

### Checkpoint 03:52:11

### Checkpoint 03:52:13

### Checkpoint 03:52:23


### Checkpoint 03:52:23
### Checkpoint 03:52:23

### Checkpoint 03:52:27

### Checkpoint 03:52:27

### Checkpoint 03:53:28

### Checkpoint 03:53:31

### Checkpoint 03:53:32

### Checkpoint 03:53:34

### Checkpoint 03:53:34

### Checkpoint 03:53:34

### Checkpoint 03:53:37

### Checkpoint 03:53:41

### Checkpoint 03:53:41

### Checkpoint 03:53:42

### Checkpoint 03:53:42

### Checkpoint 03:53:43

### Checkpoint 03:53:53

### Checkpoint 03:53:56

### Checkpoint 03:53:57

### Checkpoint 03:53:57

### Checkpoint 03:53:58

### Checkpoint 03:54:21

### Checkpoint 03:54:21

### Checkpoint 03:54:21


### Checkpoint 03:54:33
### Checkpoint 03:54:33

### Checkpoint 03:54:35

### Checkpoint 03:54:55

### Checkpoint 03:54:56


### Checkpoint 03:55:02
### Checkpoint 03:55:02

### Checkpoint 03:55:18

### Checkpoint 03:55:21

### Checkpoint 03:55:23

### Checkpoint 03:57:32

### Checkpoint 03:57:33

### Checkpoint 03:57:35

### Checkpoint 03:57:44

### Checkpoint 03:57:55

### Checkpoint 03:58:32

### Checkpoint 03:59:32

### Checkpoint 03:59:32

### Checkpoint 03:59:49

### Checkpoint 04:00:07

### Checkpoint 04:00:32

### Checkpoint 04:00:32

### Checkpoint 04:00:35

### Checkpoint 04:00:35

### Checkpoint 04:00:36

### Checkpoint 04:00:36

### Checkpoint 04:00:37


### Checkpoint 04:00:37
### Checkpoint 04:00:37


### Checkpoint 04:00:38
### Checkpoint 04:00:38

### Checkpoint 04:00:38

### Checkpoint 04:00:39


### Checkpoint 04:00:39
### Checkpoint 04:00:39

### Checkpoint 04:00:40

### Checkpoint 04:00:41

### Checkpoint 04:00:42

### Checkpoint 04:00:43


### Checkpoint 04:00:43
### Checkpoint 04:00:43

### Checkpoint 04:00:44

### Checkpoint 04:00:44

### Checkpoint 04:00:45

### Checkpoint 04:00:46

### Checkpoint 04:00:46

### Checkpoint 04:00:46

### Checkpoint 04:00:48

### Checkpoint 04:00:48

### Checkpoint 04:00:49

### Checkpoint 04:00:49

### Checkpoint 04:00:49


### Checkpoint 04:00:50
### Checkpoint 04:00:50

### Checkpoint 04:00:51

### Checkpoint 04:00:55


### Checkpoint 04:00:56
### Checkpoint 04:00:56

### Checkpoint 04:00:56

### Checkpoint 04:00:56

### Checkpoint 04:00:56

### Checkpoint 04:00:57

### Checkpoint 04:00:57

### Checkpoint 04:00:58

### Checkpoint 04:00:58

### Checkpoint 04:00:58


### Checkpoint 04:00:59
### Checkpoint 04:00:59

### Checkpoint 04:01:00

### Checkpoint 04:01:15

### Checkpoint 04:01:42

### Checkpoint 04:01:42

### Checkpoint 04:01:42

### Checkpoint 04:01:45

### Checkpoint 04:01:53

### Checkpoint 04:02:07

### Checkpoint 04:02:07

### Checkpoint 04:02:22

### Checkpoint 04:02:23

### Checkpoint 04:02:30

### Checkpoint 04:02:37

### Checkpoint 04:02:38

### Checkpoint 04:02:42

### Checkpoint 04:02:52

### Checkpoint 04:02:52

### Checkpoint 04:02:53

### Checkpoint 04:02:53

### Checkpoint 04:02:53




### Checkpoint 04:02:54
### Checkpoint 04:02:54
### Checkpoint 04:02:54
### Checkpoint 04:02:54

### Checkpoint 04:02:54

### Checkpoint 04:02:55

### Checkpoint 04:02:56

### Checkpoint 04:02:58

### Checkpoint 04:03:03

### Checkpoint 04:03:04

### Checkpoint 04:03:04

### Checkpoint 04:03:43

### Checkpoint 04:03:43

### Checkpoint 04:03:43

### Checkpoint 04:03:46

### Checkpoint 04:03:46

### Checkpoint 04:03:46


### Checkpoint 04:03:46
### Checkpoint 04:03:46

### Checkpoint 04:03:47

### Checkpoint 04:03:47


### Checkpoint 04:03:48
### Checkpoint 04:03:48

### Checkpoint 04:03:48

### Checkpoint 04:03:50

### Checkpoint 04:03:54

### Checkpoint 04:03:54

### Checkpoint 04:03:54

### Checkpoint 04:03:55


### Checkpoint 04:03:55
### Checkpoint 04:03:55

### Checkpoint 04:03:56

### Checkpoint 04:04:00

### Checkpoint 04:04:00

### Checkpoint 04:04:00


### Checkpoint 04:04:01
### Checkpoint 04:04:01

### Checkpoint 04:04:02

### Checkpoint 04:04:40

### Checkpoint 04:04:43

### Checkpoint 04:04:44

### Checkpoint 04:04:50

### Checkpoint 04:04:51

### Checkpoint 04:05:00

### Checkpoint 04:05:00

### Checkpoint 04:05:43

### Checkpoint 04:05:51

### Checkpoint 04:05:51

### Checkpoint 04:05:52

### Checkpoint 04:05:52

### Checkpoint 04:05:52

### Checkpoint 04:05:59

### Checkpoint 04:06:00

### Checkpoint 04:06:01


### Checkpoint 04:06:01
### Checkpoint 04:06:01

### Checkpoint 04:06:01

### Checkpoint 04:06:01

### Checkpoint 04:06:03

### Checkpoint 04:06:04

### Checkpoint 04:06:04

### Checkpoint 04:06:04

### Checkpoint 04:06:04

### Checkpoint 04:06:06

### Checkpoint 04:06:08

### Checkpoint 04:06:08

### Checkpoint 04:06:09

### Checkpoint 04:06:10

### Checkpoint 04:06:11


### Checkpoint 04:06:12
### Checkpoint 04:06:12

### Checkpoint 04:06:12

### Checkpoint 04:06:13

### Checkpoint 04:06:15

### Checkpoint 04:06:15

### Checkpoint 04:06:15



### Checkpoint 04:06:16
### Checkpoint 04:06:16
### Checkpoint 04:06:16


### Checkpoint 04:06:17
### Checkpoint 04:06:17


### Checkpoint 04:06:18
### Checkpoint 04:06:18

### Checkpoint 04:06:19

### Checkpoint 04:06:21

### Checkpoint 04:06:22

### Checkpoint 04:06:23

### Checkpoint 04:06:23

### Checkpoint 04:06:24

### Checkpoint 04:06:26

### Checkpoint 04:06:31

### Checkpoint 04:06:31

### Checkpoint 04:06:36

### Checkpoint 04:06:36


### Checkpoint 04:06:47
### Checkpoint 04:06:47

### Checkpoint 04:06:53

### Checkpoint 04:07:00

### Checkpoint 04:07:00


### Checkpoint 04:07:01
### Checkpoint 04:07:01


### Checkpoint 04:07:02
### Checkpoint 04:07:02


### Checkpoint 04:07:03
### Checkpoint 04:07:03

### Checkpoint 04:07:05

### Checkpoint 04:07:06

### Checkpoint 04:07:06

### Checkpoint 04:07:07

### Checkpoint 04:07:07

### Checkpoint 04:07:08

### Checkpoint 04:07:08

### Checkpoint 04:07:09


### Checkpoint 04:07:11
### Checkpoint 04:07:11

### Checkpoint 04:07:13

### Checkpoint 04:07:13

### Checkpoint 04:07:13

### Checkpoint 04:07:14


### Checkpoint 04:07:15
### Checkpoint 04:07:15

### Checkpoint 04:07:16

### Checkpoint 04:07:16

### Checkpoint 04:07:22

### Checkpoint 04:07:22


### Checkpoint 04:07:23
### Checkpoint 04:07:23

### Checkpoint 04:07:23

### Checkpoint 04:07:24

### Checkpoint 04:07:24

### Checkpoint 04:07:24

### Checkpoint 04:07:25

### Checkpoint 04:07:25

### Checkpoint 04:07:26

### Checkpoint 04:07:26

### Checkpoint 04:07:31

### Checkpoint 04:07:32

### Checkpoint 04:07:35

### Checkpoint 04:07:35

### Checkpoint 04:07:36

### Checkpoint 04:07:36


### Checkpoint 04:07:37
### Checkpoint 04:07:37


### Checkpoint 04:07:38

### Checkpoint 04:07:38
### Checkpoint 04:07:38


### Checkpoint 04:07:38
### Checkpoint 04:07:38

### Checkpoint 04:07:39

### Checkpoint 04:07:39

### Checkpoint 04:07:40

### Checkpoint 04:07:40

### Checkpoint 04:07:40


### Checkpoint 04:07:42
### Checkpoint 04:07:42

### Checkpoint 04:07:42

### Checkpoint 04:07:42

### Checkpoint 04:07:43

### Checkpoint 04:07:43

### Checkpoint 04:07:54



### Checkpoint 04:07:55
### Checkpoint 04:07:55
### Checkpoint 04:07:55

### Checkpoint 04:07:56

### Checkpoint 04:07:56

### Checkpoint 04:07:56


### Checkpoint 04:07:57
### Checkpoint 04:07:57

### Checkpoint 04:07:57

### Checkpoint 04:07:58

### Checkpoint 04:07:58

### Checkpoint 04:07:58

### Checkpoint 04:07:59


### Checkpoint 04:07:59
### Checkpoint 04:07:59


### Checkpoint 04:08:00
### Checkpoint 04:08:00

### Checkpoint 04:08:00

### Checkpoint 04:08:00

### Checkpoint 04:08:12

### Checkpoint 04:08:13

### Checkpoint 04:08:24

### Checkpoint 04:08:24

### Checkpoint 04:08:25

### Checkpoint 04:08:25

### Checkpoint 04:08:42

### Checkpoint 04:08:48

### Checkpoint 04:08:49

### Checkpoint 04:08:56


### Checkpoint 04:08:57
### Checkpoint 04:08:57

### Checkpoint 04:08:58

### Checkpoint 04:08:58

### Checkpoint 04:09:06

### Checkpoint 04:09:11

### Checkpoint 04:09:12

### Checkpoint 04:09:12

### Checkpoint 04:09:13

### Checkpoint 04:09:24

### Checkpoint 04:09:25

### Checkpoint 04:09:26

### Checkpoint 04:09:26


### Checkpoint 04:09:27
### Checkpoint 04:09:27

### Checkpoint 04:09:47

### Checkpoint 04:09:57

### Checkpoint 04:09:59

### Checkpoint 04:09:59

### Checkpoint 04:10:00

### Checkpoint 04:10:07

### Checkpoint 04:10:08

### Checkpoint 04:10:09

### Checkpoint 04:10:10

### Checkpoint 04:10:11

### Checkpoint 04:10:12

### Checkpoint 04:10:51

### Checkpoint 04:10:53

### Checkpoint 04:11:08

### Checkpoint 04:11:09

### Checkpoint 04:11:40

### Checkpoint 04:57:50

### Checkpoint 05:06:48

### Checkpoint 06:22:33

### Checkpoint 06:25:00

### Checkpoint 17:38:08

### Checkpoint 17:38:09

### Checkpoint 17:38:21

### Checkpoint 17:40:18

### Checkpoint 17:41:17

### Checkpoint 17:57:45

### Checkpoint 17:57:50

### Checkpoint 17:57:51

### Checkpoint 17:57:57

### Checkpoint 17:58:02

### Checkpoint 17:59:45

### Checkpoint 18:07:52


### Checkpoint 18:22:22
### Checkpoint 18:22:22

### Checkpoint 18:22:25


### Checkpoint 18:22:26
### Checkpoint 18:22:26

### Checkpoint 18:22:26

### Checkpoint 18:22:33

### Checkpoint 18:22:33

### Checkpoint 18:22:34



### Checkpoint 18:22:35
### Checkpoint 18:22:35
### Checkpoint 18:22:35

### Checkpoint 18:22:35

### Checkpoint 18:22:35

### Checkpoint 18:22:36

### Checkpoint 18:22:40

### Checkpoint 18:22:40

### Checkpoint 18:22:46

### Checkpoint 18:22:47

### Checkpoint 18:22:57

### Checkpoint 18:22:58

### Checkpoint 18:26:14

### Checkpoint 18:26:15

### Checkpoint 18:26:15

### Checkpoint 18:27:20

### Checkpoint 18:27:21

### Checkpoint 18:27:35

### Checkpoint 18:27:36

### Checkpoint 19:03:44

### Checkpoint 19:04:30

### Checkpoint 19:48:59

### Checkpoint 19:48:59

### Checkpoint 19:50:03

### Checkpoint 19:50:04

### Checkpoint 19:50:08

### Checkpoint 19:50:09

### Checkpoint 19:50:10

### Checkpoint 19:50:16

### Checkpoint 19:50:17

### Checkpoint 19:50:18

### Checkpoint 19:50:18

### Checkpoint 19:50:23

### Checkpoint 19:50:24

### Checkpoint 19:50:24

### Checkpoint 19:50:25

### Checkpoint 19:50:29

### Checkpoint 19:50:30

### Checkpoint 19:50:30

### Checkpoint 19:50:31

### Checkpoint 19:50:35

### Checkpoint 19:50:35

### Checkpoint 19:50:36

### Checkpoint 19:50:40

### Checkpoint 19:50:41

### Checkpoint 19:50:41

### Checkpoint 19:50:42

### Checkpoint 19:50:48

### Checkpoint 19:51:51

### Checkpoint 19:51:51

### Checkpoint 19:51:52

### Checkpoint 19:51:52

### Checkpoint 19:51:56

### Checkpoint 19:52:01

### Checkpoint 20:20:41


### Checkpoint 20:21:56
### Checkpoint 20:21:56


### Checkpoint 20:22:08
### Checkpoint 20:22:08

### Checkpoint 20:29:33

### Checkpoint 20:53:47

### Checkpoint 20:55:20

### Checkpoint 21:05:32

### Checkpoint 21:15:34

### Checkpoint 19:17:43

### Checkpoint 19:17:49


### Checkpoint 19:20:38
### Checkpoint 19:20:38

### Checkpoint 19:20:39

### Checkpoint 19:20:45

### Checkpoint 19:20:46

### Checkpoint 19:20:49

### Checkpoint 19:20:49

### Checkpoint 19:20:52

### Checkpoint 19:20:52

### Checkpoint 19:20:53

### Checkpoint 19:20:53

### Checkpoint 19:20:54

### Checkpoint 19:20:56

### Checkpoint 19:21:00

### Checkpoint 19:21:00

### Checkpoint 19:21:00




### Checkpoint 19:21:00
### Checkpoint 19:21:00
### Checkpoint 19:21:00
### Checkpoint 19:21:00

### Checkpoint 19:21:00

### Checkpoint 19:21:00


### Checkpoint 19:21:01
### Checkpoint 19:21:01

### Checkpoint 19:21:01

### Checkpoint 19:21:02

### Checkpoint 19:21:06


### Checkpoint 19:21:11
### Checkpoint 19:21:11

### Checkpoint 19:21:12

### Checkpoint 19:21:13

### Checkpoint 19:21:23

### Checkpoint 19:21:23

### Checkpoint 19:21:24

### Checkpoint 19:21:25

### Checkpoint 19:21:30

### Checkpoint 19:21:31

### Checkpoint 19:21:31

### Checkpoint 19:21:40

### Checkpoint 19:21:40

### Checkpoint 19:22:46

### Checkpoint 19:22:52

### Checkpoint 19:22:52

### Checkpoint 19:22:57

### Checkpoint 19:23:02

### Checkpoint 19:23:32

### Checkpoint 19:23:48

### Checkpoint 19:23:51

### Checkpoint 19:24:06

### Checkpoint 19:24:23

### Checkpoint 19:39:32

### Checkpoint 19:39:39

### Checkpoint 19:39:40

### Checkpoint 19:56:08

### Checkpoint 19:56:09

### Checkpoint 19:56:44

### Checkpoint 20:51:14

### Checkpoint 20:51:18

### Checkpoint 20:51:26

### Checkpoint 20:51:29

### Checkpoint 20:51:31

### Checkpoint 20:51:35


### Checkpoint 20:51:35

### Checkpoint 20:51:35
### Checkpoint 20:51:35



### Checkpoint 20:51:36
### Checkpoint 20:51:36
### Checkpoint 20:51:36

### Checkpoint 20:51:36


### Checkpoint 20:51:36
### Checkpoint 20:51:36

### Checkpoint 20:51:36


### Checkpoint 20:51:36
### Checkpoint 20:51:36

### Checkpoint 20:51:37


### Checkpoint 20:51:37
### Checkpoint 20:51:37

### Checkpoint 20:51:38


### Checkpoint 20:51:40
### Checkpoint 20:51:40


### Checkpoint 20:51:42
### Checkpoint 20:51:42

### Checkpoint 20:51:42

### Checkpoint 20:51:43




### Checkpoint 20:51:43
### Checkpoint 20:51:43
### Checkpoint 20:51:43
### Checkpoint 20:51:43

### Checkpoint 20:51:43

### Checkpoint 20:51:44

### Checkpoint 20:51:44

### Checkpoint 20:51:45

### Checkpoint 20:51:45

### Checkpoint 20:51:46

### Checkpoint 20:51:46

### Checkpoint 20:51:46


### Checkpoint 20:51:47
### Checkpoint 20:51:47

### Checkpoint 20:51:47

### Checkpoint 20:51:48


### Checkpoint 20:51:48
### Checkpoint 20:51:48

### Checkpoint 20:51:49


### Checkpoint 20:51:50
### Checkpoint 20:51:50



### Checkpoint 20:51:50
### Checkpoint 20:51:50
### Checkpoint 20:51:50

### Checkpoint 20:51:50




### Checkpoint 20:51:51
### Checkpoint 20:51:51
### Checkpoint 20:51:51
### Checkpoint 20:51:51

### Checkpoint 20:51:52


### Checkpoint 20:51:52
### Checkpoint 20:51:52



### Checkpoint 20:51:52
### Checkpoint 20:51:52
### Checkpoint 20:51:52

### Checkpoint 20:51:52


### Checkpoint 20:51:54

### Checkpoint 20:51:54
### Checkpoint 20:51:54

### Checkpoint 20:51:57

### Checkpoint 20:51:57

### Checkpoint 20:51:58

### Checkpoint 20:51:59

### Checkpoint 20:52:00

### Checkpoint 20:52:00

### Checkpoint 20:52:01

### Checkpoint 20:52:01

### Checkpoint 20:52:07

### Checkpoint 20:52:08

### Checkpoint 20:52:08

### Checkpoint 20:52:13

### Checkpoint 20:52:16

### Checkpoint 20:52:29


### Checkpoint 20:52:30
### Checkpoint 20:52:30


### Checkpoint 20:52:31
### Checkpoint 20:52:31

### Checkpoint 20:52:32
