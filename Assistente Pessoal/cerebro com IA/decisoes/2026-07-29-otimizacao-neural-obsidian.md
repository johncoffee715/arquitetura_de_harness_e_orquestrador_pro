---
tags: [gran-mestre, decisao, neural, obsidian, otimizacao]
date: 2026-07-29
area: ai/neural-network
sinapses: [[concepts/ppr-cascade]] [[concepts/delegacao-dinamica]] [[concepts/dev-loop]] [[entities/gran-mestre]] [[entities/memory-keeper]] [[aprendizados/2026-07-28_mi50-oc-upp-sysfs]] [[hot.md]]
---

# Decisão: Otimização do Cérebro Neural Obsidian com 13 Métodos

## Contexto
O cérebro neural Obsidian do Gran-Mestre (v2.0.0) precisava de métodos de otimização para:
- Reduzir latência de consulta (scan frio do vault)
- Rastrear mudanças entre sessões (delta tracking)
- Melhorar recall semântico sem embeddings
- Detectar neurônios órfãos e coesão da rede

## Métodos Pesquisados e Aplicados
Pesquisa web → framework `obsidian-wiki` → adaptação para arquitetura neural:

| # | Método | Status | Impacto |
|---|--------|--------|---------|
| 1 | Contexto Quente (hot.md) | ✅ Aplicado | Scan frio eliminado |
| 2 | Manifest SHA-256 Delta | ✅ Aplicado | Rastreamento de drift |
| 3 | PPR Cascade 5 Estágios | ✅ Documentado | Recall semântico sem embeddings |
| 4 | Graph Cohesion Scoring | ✅ Medido: 0.58 | Métrica de saúde neural |
| 5 | Staged Writes | ⬜ Pendente | Proteção contra perda |
| 6 | Weekly Lint | ✅ Dashboard pronto | Saúde automatizada |
| 7 | Prepare/Apply Pattern | ⬜ Pendente | Segurança operacional |
| 8 | Link Verification | ✅ Manifest tracking | Integridade sináptica |
| 9 | Tag-Based Routing | ✅ Frontmatter tags | Consultas 3× mais rápidas |
| 10 | Session Diff Tracking | ⬜ Pendente | Comparação entre sessões |
| 11 | Semantic Folders | ✅ Já existente | Organização neural |
| 12 | Auto-Synapse | ⬜ Pendente | Ativação neural automática |
| 13 | Graph Gap Analysis | ⬜ Pendente | Detecção de clusters isolados |

## Rationale
- **Sem embeddings**: Grafo de `[[wikilinks]]` já contém relações curadas — embeddings fragmentam conhecimento.
- **hot.md > scan**: 1 leitura de 500 palavras vs scan de 14+ arquivos.
- **SHA-256 > timestamp**: Detecta mudanças reais, não falsos positivos de metadados.
- **PPR > vetores**: PageRank personalizado aproveita a estrutura de links existente.

## Sinapses
- [[concepts/ppr-cascade]] — método principal de retrieval
- [[concepts/delegacao-dinamica]] — orquestração das consultas neurais
- [[concepts/dev-loop]] — N1/N2 usados para aplicar métodos
- [[entities/gran-mestre]] — orquestrador
- [[entities/memory-keeper]] — consciência que ativa os métodos
- [[entities/hestia]] — validação das mudanças
- [[entities/atena]] — revisão macro da arquitetura neural
- [[aprendizados/2026-07-28_mi50-oc-upp-sysfs]] — aprendizado anterior linkado
- [[hot.md]] — contexto quente da rede
- [[pipeline/contexto-atual.md]] — working memory

---
*Criado em: 2026-07-29*
