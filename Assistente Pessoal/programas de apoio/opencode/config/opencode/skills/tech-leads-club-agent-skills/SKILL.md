---
name: tech-leads-club-agent-skills
description: Validated skill registry pattern — scan-before-publish, integrity via lockfiles, progressive-disclosure MCP catalog, audited installs.
category: skill
model: local-forge/proposer
---

# tech-leads-club-agent-skills

Registry discipline for agent skills: every skill scanned before publish, integrity
pinned by lockfile + content hash, catalog exposed via progressive disclosure
(search → read → fetch files), installs audited. Helenizado de
`tech-leads-club/agent-skills` (origem: https://github.com/tech-leads-club/agent-skills).

## Quando usar

- Antes de absorver skill de terceiros (13%+ dos marketplaces têm falhas críticas)
- Ao expor catálogo via MCP (list/search/read/fetch, nunca o catálogo inteiro)
- Ao instalar skills (copy vs symlink, global vs local, com audit trail)

## Como usar

1. **Validar**: 100% open source (sem binários) + análise estática no CI + scan (Snyk Agent Scan) antes de publicar
2. **Pinar integridade**: lockfile + hash de conteúdo; re-download só com `--force`
3. **Expor**: MCP `list_skills`/`search_skills`/`read_skill`/`fetch_skill_files` (só buscar o necessário)
4. **Instalar**: copy (recomendado) ou symlink; escopo global ou local; tudo no audit log

## Princípio

Attribution obrigatória ao Tech Leads Club ao usar o catálogo (CC-BY-4.0 nas skills, MIT no engine).
