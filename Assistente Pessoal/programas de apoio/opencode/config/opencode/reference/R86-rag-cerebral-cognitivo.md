> [ARQUIVO FRI extraido de AGENTS.md em 2026-09-10 — regra R86 integral aqui. AGENTS.md carrega apenas o stub de 3 linhas.]

# ═══ REGRA GLOBAL R86 — RAG CEREBRAL COGNITIVO (OBSIDIAN COMO MEMÓRIA DE LONGO PRAZO + 4 PROPRIEDADES) — promulgado 2026-09-05 ═══

**Regra**: o vault Obsidian é o **RAG cerebral cognitivo** do ecossistema — memória de longo prazo
com 4 propriedades ativas (self-scaffolding · self-healing · self-learning · self-ameliorative),
aplicadas ao llama.cpp e ao opencode, sempre no quarteto R85 (.md .json .py .gbnf). Fonte
helenizada: `tranquileiras/autofagia e helenização/rag_cerebral_cognitivo_regra_universal.md`
(v2.0, arquitetura-validada — arquivo do usuário, referência viva, nunca movido).

<As 4 propriedades (com amarração de slot e cadência)>
- **Self-scaffolding** — nota nova cria o próprio andaime (tags+links no frontmatter, validados
  contra taxonomia e índice; nunca link para nota inexistente). Motor: slot rápido
  (:9093 Smol / :9086-CPU) + GBNF por tarefa + debounce 10s em fila SQLite. GBNF garante
  sintaxe; validação pós-inferência garante semântica (R85: trilho ≠ juízo).
- **Self-healing** — varredura semanal (systemd timer + cgroups: CPUQuota 30%, MemoryMax 2G):
  órfãos, tags obsoletas, notas desconectadas. Correção SUGERIDA, nunca aplicada
  (`status: revisar_healing`) — decisão final humana (R18/G4). NUNCA fundir notas
  automaticamente (contextos distintos colidem).
- **Self-learning** — lacunas (`#pesquisar`, `status: incompleto`, `???`) viram expansão em
  nota-filha/bloco colapsível com metadado de origem; NUNCA sobrescreve nota humana.
  Busca local primeiro (vault/FAISS), remota só se habilitada. Motor: :8083 (síntese).
- **Self-ameliorative** — revisita notas antigas (>6 meses, ≤5/dia): `valido|obsoleto|
  sugestao_taxonomia|confianca` via GBNF; obsoleto preserva insight original como contexto
  histórico; crítica = perguntas orientadoras, NUNCA reescrita (o modelo não viveu teu
  aprendizado posterior).

<Adaptações helenizadas (onde o doc-fonte divergia do harness — R8/R43)>
- **Qdrant MANTIDO** (:6333, skill bibliotecario): o doc rejeita Qdrant por peso, mas ele JÁ
  existe e funciona — catálogo-primeiro proíbe reconstruir (R8). FAISS/SQLite = fallback
  para coleções novas, não substituição.
- **Slots por tarefa** (doc §3.3 confirmada pelo nosso crivo): scaffolding→rápidos (:9093,
  :9086-CPU); síntese/crítica→:8083. Juízo final sempre humano/G4 — GBNF prende sintaxe,
  nunca confere sabedoria (canônico 05/09: Gemma 4/4 conforme + vereditos errados).
- **Grammar por requisição**, nunca `--grammar-file` global no slot (nossos slots servem
  múltiplas tasks; R85).
- **Anti-patterns do doc viram lei**: sem fusão/exclusão/sobrescrita automática (R18);
  sem JSON no corpo do .md (frontmatter); sem inferência sem debounce/fila (DDoS próprio);
  sem escrita sem Git antes de lote; sem confiança cega na semântica (schemas controlados).
- **Métricas §8 do doc como gates R28** do RAG: scaffolding <3s/nota · links quebrados <1% ·
  tags inválidas 0% · healer <30% CPU e <2GB · aprovação humana >80%.

<Enforcement>
- Features RAG nascem no quarteto R85 ou não ignitam; cada propriedade passa por auditoria
  R83 antes de operar no vault real; memorial no `llm-crivo-memorial.jsonl`.
- Trilho (GBNF) é condição necessária, nunca suficiente — veredito humano fecha o loop.

---

