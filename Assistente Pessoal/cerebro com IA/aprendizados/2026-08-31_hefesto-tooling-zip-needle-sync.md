# 2026-08-31 — Hefesto Ferramental Tríplice + Exportação ZIP + Needle 2 Sync

## O que foi feito
1. **Ferramental da Tríplice (.md/.py/.json/.gbnf)** helenizado no Hefesto (`skills/hefesto/tooling/`):
   - `llama_cpp_config.json` — contrato de dados (schema) Single Source of Truth
   - `hefesto_llama_bridge.py` — unificado: compile flags + autodescoberta + webhook
   - `hefesto_feature.gbnf` + `hefesto_deep_spec.gbnf` — gramáticas GBNF para JSON estrito
   - Fluxo: webhook → discover → PENDING_GBNF_VAL → GBNF enriquecimento → consolidação

2. **Exportação ZIP** (um por feature) em `/mnt/dados/Assistente Pessoal/projetos/features feitas/`:
   - `a2a-brainstorm.zip` (15KB) — loop A2A tríade VRAM
   - `hefesto.zip` (41KB) — dispatcher + 4 skills + tooling tríplice
   - `bibliotecario.zip` (15KB) — RAG híbrido Obsidian×Qdrant×RWKV7
   - Cada um com README.md completo (capacidades, competências, aplicabilidades, como usar, como incluir em harness)

3. **Needle 2 sincronizado com todos os LLMs compatíveis**:
   - `unified-tools.json` (6 ferramentas: validate_schema, triage_route, write_artifact, upsert_vault, emit_manifest, run_shell)
   - Registrado como compatível com todas as categorias (contrato-plano, refutacao, judge, reflexo, talamus-cortex, orquestrador)
   - Testado: validação 149 t/s + triagem 189 t/s, ~30MB RAM

## Evidência
- Bridge: `--compile` OK, `--discover` OK (detectou --ctx-size, --model, --new-hyper-parameter)
- Needle unified: validate_schema + triage_route funcionando
- Testes: 59/59 verdes
- Commits: 7bf5f4bab (tooling + needle sync)

## Lições
1. **Tríplice .md/.py/.json/.gbnf** é o padrão de construção de features do Hefesto — o .md é Single Source of Truth, o .py executa, o .json valida schema, o .gbnf garante saída estruturada.
2. **Needle 2** é compatível com toda a stack (validação/estruturação/triagem) — tool-set unificado cobre todos os casos.
3. **ZIP por feature** com README completo permite exportação/teste em outro harness.

## Estado
- Commits: 7bf5f4bab (último)
- ZIPs: 3 pacotes exportáveis
- Pendência: teste ngram do 35B (resultado não consolidado — draft-simple degradou 2.24→1.34 t/s; ngram-simple a testar com quoting correto)