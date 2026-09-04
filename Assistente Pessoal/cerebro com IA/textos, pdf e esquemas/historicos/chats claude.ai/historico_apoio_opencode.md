# Histórico de Apoio — Contexto Técnico para OpenCode

> Documento consolidado a partir do histórico de projetos registrado, para uso como contexto de apoio (referência) ao trabalhar com o OpenCode. Cobre arquitetura, decisões já tomadas, bugs conhecidos e estado atual de cada frente. Atualize este arquivo conforme os projetos evoluem.

---

## 1. Perfil técnico do usuário

- Técnico eletrônico e engenheiro de hardware, 10+ anos de experiência.
- Especialidades: reparo em bancada/campo, rework SMD/PTH, microssoldagem, automação industrial, sistemas embarcados.
- Cursando Engenharia Mecatrônica. Certificação NR10 SEP.
- Foco técnico atual: stack de IA local soberana e offline-first, hoje centrada no **OpenCode**.

---

## 2. Migração de stack: AI-Lab2 → OpenCode

- A stack antiga **AI-Lab2** (CachyOS Linux) foi **totalmente deletada** — hoje o fluxo de trabalho usa **apenas o OpenCode**.
- Filosofia mantida: *"o modelo muda, o conhecimento persiste"* — infraestrutura modular, sem vendor lock-in.
- Legado técnico da AI-Lab2 (para referência, caso algo seja reaproveitado):
  - Modelos ativos por papel: `qwen2.5-coder:14b` (CODER), `gemma4:e4b` (REASONER), `qwen3:14b` (GENERAL), `deepseek-r1:14b` (HEAVY, sem tool-calling), `mistral-nemo:latest` (FAST), `nomic-embed-text` (EMBED).
  - Arquitetura de estado/eventos/quotas: `state_authority.py`, `event_bus.py`, `quotas.py`, `state.sh`.
  - Scripts de deploy: `update_lab.sh`, `update_geral.sh`, `bootstrap.sh`.
  - Bug conhecido (histórico): inconsistência de paths `ailab` vs `ailab2` em scripts de produção.
  - Fix de GPU resolvido: pacote ROCm do Ollama no CachyOS não trazia o binário `llama-server`; solução foi usar binário Vulkan-backend do llama.cpp pré-existente (`~/.local/share/ailab2/bin/llamacpp/`) — GPU confirmada em uso (VRAM 1.75GB idle → 9.34GB carregado, 100% GPU).
  - Paths: NTFS slave `/mnt/win2/Assistente Pessoal2/`; runtime ext4 `~/.local/share/ailab2/`.
  - Origem (v1): sync de inteligência do YouTube, pipeline RAG com Qdrant, transcrição Whisper, integração Open-WebUI.

---

## 3. Upgrade de infraestrutura em SSD — "Jarvis" / AI-Lab v12

- Codinome **Jarvis**, alvo `/srv/ai-lab`.
- Documentos de planejamento já analisados; problemas identificados: inconsistências de path, versões concorrentes de `SYSTEM_PROMPT`, subcomandos de CLI faltando.

---

## 4. Pipeline book-to-skill

- Pipeline `ai-lab book` está operacional.
- Já processou um lote de 170+ skills a partir de datasheets de hardware e livros de eletrônica.
- Problema de qualidade recorrente: LLMs locais alucinam valores numéricos de hardware.
- Direção de correção validada: extração verbatim, sem passar tabelas numéricas pelo LLM.

---

## 5. Pipeline de engenharia reversa via OpenCode + Ghidra

- Usa OpenCode com os modelos "opencode zen" e "go" (free) para raciocínio pesado.
- **Camada 1 — Infraestrutura**: Java JDK 21, Ghidra (última versão), plugin GhidraMCP, MCP remoto em `mcp-configs/mcp-servers.json`.
- **Camada 2 — Agente especializado**: agente `reverser` definido em `opencode.json` → agent, integrado ao GhidraMCP.
- **Camada 3 — Skill de pipeline RE**: skill `ghidra-re-pipeline` orquestrando: abrir binário no Ghidra → decompilar função alvo → enviar pseudocódigo ao LLM → aplicar renomeação sugerida → documentar análise → gerar relatório para validação manual/assistida.
- Prioridade atual: fluxo de trabalho e automação (scripts, agentes).

---

## 6. Engenharia reversa da GPU MI50 16GB

- Primeira documentação pública dessa família de BIOS.
- BIOS de fábrica (D1631400-X11) subclockeia HBM2 para 600MHz (vs 1000MHz nas variantes Pro VII).
- BIOS instalada: Lenovo OEM Pro VII 113-D1640700-100 ver .064.015933, 512KB, UEFI, FP64 ativo, ReBAR 16GB, PCIe Gen3 max, cap de 350W.
- Famílias de BIOS documentadas: D1631400 (MI50 16GB stock), D1640600 (Pro VII AMD WS), D1640700 (Pro VII Lenovo), D3600200 (MOONSHOT consumer).
- VRM: IR35217 8+0/6+2 fases; Vcore idle 0.743V, carga 1.118–1.162V; escala SVID 0.25mV/unidade confirmada.
- OC unlock: `ppfeaturemask=0xfff7ffff` no GRUB (`linux-cachyos.conf`); pp_table patchada via Python.
- Patch MOONSHOT D3600200-106: patch de 3 bytes no DeviceID (offsets 0x000AE/0x002C6/0x0E622, AF→A1) + checksums; MD5 `f690c8aedc64c7f0c2d152ff4cac5301`; flash pendente.
- `amdvbflash` 4.104e instalado via AUR em `/usr/bin/amdvbflash`; flash pendente ativação de SSH e backup.
- Problema térmico: junction 100–102°C a 181–292W, edge 62–68°C, delta 32–37°C, Rθ 0,13–0,69°C/W — correção de TIM pendente no bloco Bykski A-MI50-X.
- Loop d'água: radiador 1200mm, duas bombas em série (800+900 L/h), reservatório 350ml — capacidade do loop está OK, o problema é contato do TIM.
- Segunda MI50 16GB disponível para reparo — diagnóstico ainda não iniciado.
- Documentação da comunidade gerada: `MI50_16GB_VBIOS.md` (252 linhas); relatório de sessão `relatorio_sessao_MI50_RE.txt` (520 linhas).

---

## 7. BIOS modding — Jingsha X99-D8

- Placa: Jingsha X99-D8 (Intel C612, Xeon E5-2699v3).
- 19+ versões de ROM analisadas entre famílias X99 chinesas.
- Regras de compatibilidade confirmadas: `FD[0x17]=0x02` obrigatório; módulos TPM PEI causam travamento em POST 0x79.
- Throttle de clock por microcode diagnosticado (bit LOCK do MSR 0x610 durante PEI); fix correto é invalidar o microcode + writes de MSR em nível de SO.
- **CX99DE30** é a melhor ROM base para a D8 (padronizada, melhores temps/estabilidade).
- Abordagem final adotada: BIOS faz só o mínimo seguro (invalidação de microcode); o fix real de clock all-core 3.6GHz (MSR 0x610 PkgPowerLimit + MSR 0x1AD/1AE/1AF TurboRatio=36) é aplicado via serviço systemd no CachyOS (`xeon-clock-unlock.sh`), não via driver DXE na BIOS.
- Histórico de tentativas de driver DXE (v15–v19), todas superadas pela abordagem OS-level:
  - v15–v16: hook em bootblock + driver DXE para MSR 0x610 → travamento em POST 0x79 e FF; subsystem PE32+ errado e sem DEPEX.
  - v17: injeção de NvmExpressDxe sem DEPEX → SSD/UEFI não reconhecido + freeze.
  - v18: microcode invalidado por corrupção de CPUID (0x306F2→0xFFFFFFFF) → boota mas sem NVMe.
  - v19 (mais recente): CX99DE30 + microcode invalidado (método v18) + NvmExpressDxe injetado COM DEPEX no offset correto — resultado do teste do usuário ainda pendente.
- Entregáveis: `CX99DE30_v19_NVMe_DEPEX.bin`, `xeon-clock-unlock.sh` + `.service` para o fix de clock no CachyOS.

---

## Notas de uso deste documento

- Este arquivo é gerado a partir do que ficou registrado como contexto de projeto — não é uma cópia literal de conversas.
- Sugestão: manter este arquivo dentro do repositório/projeto ativo do OpenCode (ex: como `CONTEXT.md` ou referenciado no `AGENTS.md`/`opencode.json`) para que o agente tenha acesso a esse histórico como contexto de apoio.
- Recomendo atualizar as seções conforme cada frente evolui (principalmente MI50, X99-D8 e o pipeline RE, que estão com testes/flashes pendentes).
