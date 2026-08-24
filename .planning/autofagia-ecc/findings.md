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

### Checkpoint 20:52:44

### Checkpoint 20:52:47

### Checkpoint 20:53:16

### Checkpoint 20:53:17


### Checkpoint 20:53:19
### Checkpoint 20:53:19

### Checkpoint 05:59:20

### Checkpoint 06:57:36

### Checkpoint 06:57:36

### Checkpoint 06:58:20

### Checkpoint 07:27:31

### Checkpoint 18:13:10

### Checkpoint 19:45:58

### Checkpoint 20:51:25

### Checkpoint 22:17:16

### Checkpoint 22:18:17

### Checkpoint 22:53:06

### Checkpoint 23:08:51

### Checkpoint 23:10:59

### Checkpoint 23:11:24

### Checkpoint 23:16:00

### Checkpoint 23:32:06

### Checkpoint 23:47:39

### Checkpoint 00:13:04

### Checkpoint 00:13:23

### Checkpoint 00:17:19

### Checkpoint 00:21:44

### Checkpoint 00:26:22

### Checkpoint 00:26:46

### Checkpoint 00:27:07

### Checkpoint 00:27:16

### Checkpoint 00:27:26

### Checkpoint 00:28:17

### Checkpoint 00:30:58

### Checkpoint 00:36:13

### Checkpoint 00:40:59

### Checkpoint 00:41:11

### Checkpoint 00:43:20

### Checkpoint 00:51:28

### Checkpoint 01:10:36

### Checkpoint 01:26:10

### Checkpoint 01:26:30

### Checkpoint 01:36:01

### Checkpoint 01:37:07


### Checkpoint 01:41:49
### Checkpoint 01:41:49

### Checkpoint 01:59:56

### Checkpoint 02:37:32

### Checkpoint 02:37:41

### Checkpoint 02:37:42

### Checkpoint 02:37:53


### Checkpoint 02:38:06
### Checkpoint 02:38:06

### Checkpoint 02:38:06


### Checkpoint 02:38:17
### Checkpoint 02:38:17


### Checkpoint 02:38:25
### Checkpoint 02:38:25

### Checkpoint 02:38:25

### Checkpoint 02:38:38

### Checkpoint 02:49:49

### Checkpoint 08:46:45

### Checkpoint 22:29:04

### Checkpoint 22:44:24

### Checkpoint 22:45:18

### Checkpoint 22:50:13

### Checkpoint 22:50:15

### Checkpoint 22:50:16

### Checkpoint 22:50:25

### Checkpoint 22:50:28

### Checkpoint 22:53:30

### Checkpoint 23:18:51

### Checkpoint 23:18:55

### Checkpoint 23:19:05

### Checkpoint 23:19:10

### Checkpoint 23:19:10

### Checkpoint 23:20:16

### Checkpoint 23:21:57

### Checkpoint 23:35:11

### Checkpoint 00:51:27

### Checkpoint 00:52:12

### Checkpoint 01:52:15

### Checkpoint 01:52:15

### Checkpoint 01:52:32

### Checkpoint 01:52:35

### Checkpoint 01:52:35

### Checkpoint 01:52:35

### Checkpoint 02:00:56

### Checkpoint 02:00:58

### Checkpoint 02:00:59

### Checkpoint 02:01:01

### Checkpoint 02:01:01

### Checkpoint 02:04:26

### Checkpoint 02:04:26

### Checkpoint 02:04:32

### Checkpoint 02:04:38

### Checkpoint 02:04:38

### Checkpoint 02:06:48

### Checkpoint 02:06:49

### Checkpoint 02:06:59

### Checkpoint 02:07:06

### Checkpoint 02:07:44

### Checkpoint 02:15:00

### Checkpoint 02:16:27

### Checkpoint 02:16:28

### Checkpoint 02:16:32

### Checkpoint 02:17:13

### Checkpoint 02:17:48

### Checkpoint 02:18:53

### Checkpoint 02:18:56

### Checkpoint 02:21:15

### Checkpoint 02:22:05

### Checkpoint 02:27:25

### Checkpoint 02:28:19

### Checkpoint 02:28:36

### Checkpoint 02:31:21

### Checkpoint 02:48:21

### Checkpoint 02:49:27

### Checkpoint 02:50:15

### Checkpoint 02:50:23

### Checkpoint 02:50:28

### Checkpoint 02:50:28

### Checkpoint 02:50:32

### Checkpoint 02:50:36

### Checkpoint 02:50:37

### Checkpoint 02:50:37

### Checkpoint 02:50:39

### Checkpoint 02:50:43

### Checkpoint 02:50:47

### Checkpoint 02:50:50

### Checkpoint 02:50:53

### Checkpoint 02:50:56

### Checkpoint 02:50:57

### Checkpoint 02:56:59

### Checkpoint 02:57:36

### Checkpoint 02:57:44

### Checkpoint 02:57:44

### Checkpoint 02:57:48

### Checkpoint 02:57:54

### Checkpoint 02:57:57

### Checkpoint 02:58:02

### Checkpoint 02:58:18

### Checkpoint 02:58:24

### Checkpoint 03:02:41

### Checkpoint 03:03:00

### Checkpoint 03:03:33

### Checkpoint 03:06:27

### Checkpoint 03:07:00

### Checkpoint 03:09:59

### Checkpoint 03:10:28

### Checkpoint 03:11:18

### Checkpoint 03:11:22

### Checkpoint 03:11:24

### Checkpoint 03:11:28

### Checkpoint 03:11:30

### Checkpoint 03:11:31

### Checkpoint 03:11:33

### Checkpoint 03:11:38

### Checkpoint 03:11:47

### Checkpoint 03:11:51

### Checkpoint 03:11:55

### Checkpoint 03:11:56

### Checkpoint 03:12:01

### Checkpoint 03:12:09

### Checkpoint 03:12:48

### Checkpoint 03:14:27

### Checkpoint 03:17:49

### Checkpoint 03:21:31

### Checkpoint 03:23:24

### Checkpoint 03:23:28

### Checkpoint 03:24:03

### Checkpoint 03:32:51

### Checkpoint 03:32:52

### Checkpoint 03:42:06

### Checkpoint 04:17:55

### Checkpoint 04:19:59

### Checkpoint 04:26:56

### Checkpoint 04:39:20

### Checkpoint 04:41:20

### Checkpoint 04:48:06

### Checkpoint 04:50:43

### Checkpoint 04:52:57

### Checkpoint 04:54:55

### Checkpoint 04:56:57

### Checkpoint 05:05:34

### Checkpoint 05:06:14

### Checkpoint 05:07:13

### Checkpoint 05:11:07

### Checkpoint 05:13:50

### Checkpoint 05:15:10

### Checkpoint 05:19:40

### Checkpoint 05:22:56

### Checkpoint 05:23:51

### Checkpoint 05:29:23

### Checkpoint 05:31:32

### Checkpoint 05:32:40

### Checkpoint 05:34:38

### Checkpoint 05:37:43

### Checkpoint 05:38:35

### Checkpoint 05:40:49

### Checkpoint 05:42:40

### Checkpoint 05:44:53

### Checkpoint 05:51:42

### Checkpoint 06:02:47

### Checkpoint 06:05:50

### Checkpoint 06:07:41

### Checkpoint 06:08:40

### Checkpoint 06:09:16

### Checkpoint 06:12:07

### Checkpoint 06:14:12

### Checkpoint 06:20:14

### Checkpoint 06:24:12

### Checkpoint 06:26:16

### Checkpoint 06:33:21

### Checkpoint 06:33:22

### Checkpoint 06:35:56

### Checkpoint 06:38:23

### Checkpoint 06:52:21

### Checkpoint 06:55:07

### Checkpoint 06:56:57

### Checkpoint 06:57:29

### Checkpoint 06:59:15

### Checkpoint 07:01:16

### Checkpoint 07:02:17

### Checkpoint 07:06:10

### Checkpoint 07:09:45

### Checkpoint 07:14:21

### Checkpoint 07:18:36

### Checkpoint 07:21:09

### Checkpoint 07:22:51

### Checkpoint 07:26:59

### Checkpoint 07:29:50

### Checkpoint 07:29:56

### Checkpoint 07:30:04

### Checkpoint 07:30:11

### Checkpoint 07:30:20

### Checkpoint 07:40:14

### Checkpoint 07:43:22

### Checkpoint 14:51:42

### Checkpoint 14:56:32

### Checkpoint 15:27:51

### Checkpoint 16:34:52

### Checkpoint 16:35:53

### Checkpoint 16:36:22

### Checkpoint 16:36:39

### Checkpoint 16:42:17

### Checkpoint 16:42:44

### Checkpoint 19:55:35

### Checkpoint 20:27:29

### Checkpoint 20:44:58

### Checkpoint 20:49:13

### Checkpoint 20:52:41

### Checkpoint 22:54:27

### Checkpoint 22:57:57

### Checkpoint 23:03:17

### Checkpoint 00:34:05

### Checkpoint 01:26:10

### Checkpoint 01:33:41

### Checkpoint 01:33:41

### Checkpoint 01:36:17

### Checkpoint 01:37:00

### Checkpoint 05:39:21

### Checkpoint 06:30:53

### Checkpoint 06:33:44

### Checkpoint 06:34:18

### Checkpoint 06:34:32

### Checkpoint 06:44:00

### Checkpoint 06:44:48

### Checkpoint 07:13:44

### Checkpoint 07:13:44

### Checkpoint 11:59:44

### Checkpoint 12:07:42

### Checkpoint 12:08:12

### Checkpoint 12:14:38

### Checkpoint 12:14:50

### Checkpoint 12:17:30

### Checkpoint 12:20:31

### Checkpoint 12:22:56

### Checkpoint 12:23:49

### Checkpoint 12:24:26

### Checkpoint 11:33:44

### Checkpoint 11:41:45

### Checkpoint 11:42:11

### Checkpoint 11:42:38

### Checkpoint 11:42:38

### Checkpoint 11:42:46


### Checkpoint 11:43:17
### Checkpoint 11:43:17

### Checkpoint 11:43:58

### Checkpoint 11:48:28

### Checkpoint 11:50:56

### Checkpoint 11:51:19

### Checkpoint 11:51:54

### Checkpoint 11:55:50

### Checkpoint 11:56:22

### Checkpoint 11:56:41

### Checkpoint 11:57:13

### Checkpoint 11:58:27

### Checkpoint 12:05:54

### Checkpoint 12:11:27

### Checkpoint 12:13:46

### Checkpoint 12:14:05

### Checkpoint 12:18:34

### Checkpoint 12:24:05

### Checkpoint 12:25:28

### Checkpoint 12:29:32

### Checkpoint 12:32:26



### Checkpoint 12:32:35
### Checkpoint 12:32:35
### Checkpoint 12:32:35

### Checkpoint 12:35:24

### Checkpoint 12:35:45

### Checkpoint 12:35:48

### Checkpoint 12:38:59

### Checkpoint 12:40:55

### Checkpoint 12:42:12

### Checkpoint 12:45:48

### Checkpoint 12:45:53

### Checkpoint 12:46:20

### Checkpoint 12:47:20

### Checkpoint 12:48:41

### Checkpoint 12:48:55

### Checkpoint 12:49:14

### Checkpoint 12:52:02

### Checkpoint 12:52:54

### Checkpoint 12:54:02

### Checkpoint 12:54:47

### Checkpoint 12:54:47

### Checkpoint 12:54:55

### Checkpoint 12:56:48



### Checkpoint 12:57:00
### Checkpoint 12:57:00
### Checkpoint 12:57:00

### Checkpoint 13:04:32

### Checkpoint 13:04:32

### Checkpoint 13:05:04

### Checkpoint 13:05:23

### Checkpoint 13:06:54

### Checkpoint 13:07:12

### Checkpoint 13:07:53

### Checkpoint 13:09:05

### Checkpoint 13:09:18

### Checkpoint 13:10:00

### Checkpoint 13:13:14

### Checkpoint 13:20:00

### Checkpoint 13:27:20

### Checkpoint 13:28:44

### Checkpoint 13:28:59


### Checkpoint 13:36:23
### Checkpoint 13:36:23

### Checkpoint 13:36:56

### Checkpoint 13:40:56

### Checkpoint 13:41:05

### Checkpoint 13:41:21

### Checkpoint 13:59:19

### Checkpoint 13:59:26

### Checkpoint 14:01:59

### Checkpoint 14:15:13

### Checkpoint 14:16:11

### Checkpoint 14:39:38

### Checkpoint 21:51:27

### Checkpoint 22:02:27

### Checkpoint 22:05:44

### Checkpoint 22:07:32

### Checkpoint 22:14:32

### Checkpoint 22:14:50

### Checkpoint 22:16:57

### Checkpoint 22:18:15

### Checkpoint 22:22:35

### Checkpoint 22:29:06

### Checkpoint 22:33:38

### Checkpoint 22:34:25

### Checkpoint 22:39:23

### Checkpoint 22:45:01

### Checkpoint 22:47:57

### Checkpoint 22:59:54

### Checkpoint 23:02:25

### Checkpoint 23:04:31

### Checkpoint 23:07:19

### Checkpoint 23:10:05

### Checkpoint 23:16:46

### Checkpoint 23:23:25


### Checkpoint 23:31:25
### Checkpoint 23:31:25

### Checkpoint 23:33:36

### Checkpoint 23:42:50

### Checkpoint 23:59:09

### Checkpoint 00:00:56

### Checkpoint 00:06:31


### Checkpoint 00:13:13
### Checkpoint 00:13:13

### Checkpoint 00:19:26

### Checkpoint 00:38:55

### Checkpoint 00:38:57

### Checkpoint 00:51:38

### Checkpoint 01:24:48

### Checkpoint 01:28:39

### Checkpoint 01:29:20

### Checkpoint 01:31:04

### Checkpoint 01:48:22

### Checkpoint 02:13:00

### Checkpoint 02:14:22

### Checkpoint 03:41:49

### Checkpoint 05:20:33

### Checkpoint 05:50:56

### Checkpoint 06:46:58

### Checkpoint 06:49:24

### Checkpoint 06:49:27

### Checkpoint 06:49:31

### Checkpoint 06:49:36

### Checkpoint 06:49:40

### Checkpoint 06:49:44

### Checkpoint 06:49:48

### Checkpoint 06:49:52

### Checkpoint 06:50:51

### Checkpoint 06:51:06

### Checkpoint 06:52:00

### Checkpoint 07:00:27

### Checkpoint 07:08:18

### Checkpoint 07:08:41

### Checkpoint 07:09:02

### Checkpoint 07:09:13

### Checkpoint 07:09:53

### Checkpoint 07:13:38

### Checkpoint 07:14:18

### Checkpoint 07:16:21

### Checkpoint 07:16:36

### Checkpoint 07:18:09

### Checkpoint 07:19:32

### Checkpoint 07:19:41

### Checkpoint 07:23:43

### Checkpoint 07:25:54

### Checkpoint 07:26:13

### Checkpoint 07:29:14

### Checkpoint 07:29:22

### Checkpoint 07:32:18

### Checkpoint 07:32:27

### Checkpoint 22:02:53

### Checkpoint 22:04:40

### Checkpoint 22:06:27

### Checkpoint 22:06:29

### Checkpoint 22:06:35

### Checkpoint 22:08:06

### Checkpoint 22:09:42

### Checkpoint 09:27:12

### Checkpoint 09:40:09

### Checkpoint 09:40:10

### Checkpoint 09:40:22

### Checkpoint 09:40:23

### Checkpoint 09:40:33

### Checkpoint 09:40:33

### Checkpoint 09:44:19

### Checkpoint 09:49:45

### Checkpoint 09:58:00

### Checkpoint 09:58:39

### Checkpoint 09:59:46

### Checkpoint 10:05:15

### Checkpoint 10:13:12

### Checkpoint 10:18:00

### Checkpoint 10:20:47

### Checkpoint 10:20:59

### Checkpoint 10:21:14

### Checkpoint 10:23:42

### Checkpoint 10:54:20

### Checkpoint 11:06:16

### Checkpoint 11:07:44

### Checkpoint 11:19:21

### Checkpoint 11:52:42

### Checkpoint 11:53:00

### Checkpoint 11:53:38

### Checkpoint 15:16:14

### Checkpoint 16:03:25

### Checkpoint 16:03:43

### Checkpoint 16:31:30

### Checkpoint 17:38:37

### Checkpoint 17:38:47

### Checkpoint 21:02:48

### Checkpoint 06:22:35

### Checkpoint 06:34:15


### Checkpoint 06:37:06
### Checkpoint 06:37:06

### Checkpoint 06:38:00

### Checkpoint 06:39:37

### Checkpoint 06:40:12

### Checkpoint 06:44:50

### Checkpoint 06:45:24

### Checkpoint 06:47:42

### Checkpoint 06:49:35


### Checkpoint 06:50:45
### Checkpoint 06:50:45

### Checkpoint 06:51:45

### Checkpoint 07:00:24

### Checkpoint 07:00:45

### Checkpoint 07:01:21

### Checkpoint 07:06:38

### Checkpoint 07:06:50

### Checkpoint 07:08:46

### Checkpoint 07:15:49

### Checkpoint 07:21:16

### Checkpoint 07:23:24

### Checkpoint 07:23:56

### Checkpoint 07:35:49

### Checkpoint 07:37:46

### Checkpoint 07:49:08

### Checkpoint 07:49:44

### Checkpoint 07:54:21

### Checkpoint 07:55:32

### Checkpoint 07:57:00

### Checkpoint 07:57:56

### Checkpoint 07:58:12

### Checkpoint 08:54:22

### Checkpoint 08:54:41

### Checkpoint 08:55:23

### Checkpoint 08:57:13

### Checkpoint 08:58:08

### Checkpoint 13:05:13

### Checkpoint 13:11:16

### Checkpoint 19:34:28

### Checkpoint 07:37:50

### Checkpoint 07:52:44

### Checkpoint 07:56:02

### Checkpoint 08:09:43

### Checkpoint 08:12:23

### Checkpoint 08:32:06

### Checkpoint 08:34:37

### Checkpoint 08:59:01

### Checkpoint 09:07:46

### Checkpoint 06:47:56

### Checkpoint 08:58:42

### Checkpoint 10:15:26

### Checkpoint 10:56:43

### Checkpoint 11:05:48

### Checkpoint 12:20:56

### Checkpoint 15:34:17

### Checkpoint 15:42:28

### Checkpoint 15:45:08

### Checkpoint 15:48:54

### Checkpoint 05:57:01

### Checkpoint 06:56:28

### Checkpoint 08:26:51

### Checkpoint 08:42:18

### Checkpoint 09:45:10

### Checkpoint 11:30:29

### Checkpoint 11:38:31

### Checkpoint 12:19:10

### Checkpoint 12:23:13

### Checkpoint 12:36:36

### Checkpoint 12:44:29

### Checkpoint 12:44:30

### Checkpoint 13:08:20

### Checkpoint 13:10:31

### Checkpoint 13:11:54

### Checkpoint 13:35:59

### Checkpoint 13:41:32

### Checkpoint 13:41:49

### Checkpoint 13:44:31

### Checkpoint 13:46:55

### Checkpoint 14:49:03

### Checkpoint 16:01:02

### Checkpoint 17:04:23

### Checkpoint 17:29:44

### Checkpoint 17:32:06

### Checkpoint 17:33:17

### Checkpoint 17:33:27

### Checkpoint 17:33:29

### Checkpoint 17:33:31

### Checkpoint 17:33:33

### Checkpoint 17:36:33

### Checkpoint 17:36:35

### Checkpoint 17:36:37

### Checkpoint 17:36:58

### Checkpoint 17:37:00

### Checkpoint 17:39:00

### Checkpoint 17:39:02

### Checkpoint 17:39:05

### Checkpoint 17:39:07

### Checkpoint 18:22:55

### Checkpoint 18:25:51

### Checkpoint 18:26:01

### Checkpoint 18:26:02

### Checkpoint 18:26:20

### Checkpoint 18:26:22

### Checkpoint 18:26:34

### Checkpoint 18:26:37

### Checkpoint 18:44:28

### Checkpoint 18:44:29

### Checkpoint 18:44:31

### Checkpoint 19:02:20

### Checkpoint 20:09:28

### Checkpoint 20:09:29

### Checkpoint 20:09:30

### Checkpoint 20:13:37

### Checkpoint 20:13:38


### Checkpoint 20:17:17
### Checkpoint 20:17:17

### Checkpoint 20:32:25
