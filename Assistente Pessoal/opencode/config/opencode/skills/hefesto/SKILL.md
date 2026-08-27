---
name: hefesto
description: "Doutrina unificada de absorção tecnológica: DECOMPILAÇÃO (desconstrução com evidência) → AUTOFAGIA (digestão da essência) → HELENIZAÇÃO (normatização OpenCode) → FORJA (síntese final). Use ao absorver qualquer framework/agente/skill/plugin externo (zip, repo, binário, doc), ao criar hooks/plugins/skills/subagents/MCPs/LSPs/features a partir de fontes externas, ou quando 'autofagia', 'helenização', 'decompilação' ou 'antropofagia' forem mencionados. Substitui professional-decompilation e os fragmentos esparsos de autofagia/helenização."
mode: skill
origin: hefesto-creationist-v6-helenizado
metadata:
  category: methodology
  version: 1.0.0
  date: 2026-08-26
  author: Gran-Mestre
  source_sha256: 0057067d732eb4c1704fb3160a809d50375dfab8d84af4d50470e626c85ae793
  replaces: [professional-decompilation, .planning/autofagia]
---

# HEFESTO — Decompile. Digerir. Helenize. Forge.

Pipeline único e obrigatório para transformar artefatos externos (código, binário, zip, framework, agente, doc) em recursos nativos globais do harness (R2). Quatro estágios sequenciais, cada um com gate categórico (R28).

```text
[ARTEFATO EXTERNO] → 1.DECOMPILAÇÃO → 2.AUTOFAGIA → 3.HELENIZAÇÃO → 4.FORJA → [RECURSO GLOBAL]
                          gate G-D         gate G-A        gate G-H        gate G-F
```

Pré-requisitos herdados do criacionismo: **Self-Learning** (minerar conhecimento tácito durante o processo), **Self-Scaffold** (gerar parsers/ganchos/estruturas como subproduto), **Self-Healing** (detectar incoerência entre input e realidade estrutural → refutar input inválido, nunca aceitar acriticamente).

---

## Estágio 1 — DECOMPILAÇÃO (matéria-prima)

Desconstruir o artefato ao nível factual. Vale para binário (RE clássico) OU fonte/doc/zip (análise estrutural).

**Princípio central:** nunca transformar hipótese em fato sem evidência.

1. **INTAKE**: hash sha256, path, tamanho, método de aquisição. NUNCA modificar o original — cópia de trabalho.
2. **IDENTIFICATION**: formato, arquitetura, toolchain, dependências, entry points, packing.
3. **TRIAGE**: prioridade = Impact × Evidence Density × Centrality × Unknownness.
4. **ANÁLISE**: fluxo de controle/dados, componentes, interfaces, contratos. Cada descoberta = evidência ID `E-001...` com tipo, observação, reprodutibilidade.
5. **CORRELATION**: conclusão ganha confiança quando múltiplas fontes independentes convergem.

Classificação obrigatória por conclusão: `CONFIRMED | HIGH_CONFIDENCE | PROBABLE | POSSIBLE | UNKNOWN | CONTRADICTED`.
Rastreio: `CONCLUSÃO → EVIDÊNCIA → MÉTODO → VALIDAÇÃO`. Nunca escrever fato onde há apenas evidência.
Nunca preencher lacuna inventando comportamento — marcar `PARTIALLY UNDERSTOOD`.

**Gate G-D:** mapa estrutural completo com ≥1 evidência rastreável por afirmação central. Falhou → não avança.

## Estágio 2 — AUTOFAGIA (digestão)

Extrair a ESSENCIA, nunca a implementação literal. Digestão quantitativa E qualitativa (R38).

| Extrair (proteína) | Descartar (ruído) |
|---|---|
| Conceitos, invariantes, protocolos | Nomes de marca, cosmética |
| Métricas, gates, critérios de qualidade | Hardcodes de ambiente alheio (portas, paths inexistentes) |
| Padrões arquiteturais replicáveis | Código morto, duplicação |
| Falhas e vulnerabilidades DO ORIGINAL | Configuração acoplada ao ecossistema de origem |

**Auditoria adversarial obrigatória:** caçar bugs/fraudes no artefato original (ex.: no Hefesto v6, `_evaluate_pillar` retornava score default 96.5 sem evidência — auto-aprovação; corrigido aqui: validador sem evidência → `UNKNOWN`, score piso). Toda falha encontrada vira lição registrada no output.

**Catálogo primeiro (R8):** antes de decidir construir, varrer registry/skills/agents/hooks/MCPs/LSPs existentes. Só o GAP vira trabalho de forja; o resto é mapeamento.

**Gate G-A:** essência destilada (tabela proteína×ruído preenchida) + auditoria de falhas + GAP confirmado contra catálogo.

## Estágio 3 — HELENIZAÇÃO (normatização)

Converter a essência ao padrão estrito OpenCode/harness. Nunca copiar cegamente — SEMPRE adaptar.

### Alvo por tipo de recurso (aplicação global criteriosa)

| Tipo | Quando forjar | Forma helenizada |
|---|---|---|
| **skill** | metodologia/procedimento reutilizável | `<global>/skills/<nome>/SKILL.md` + frontmatter YAML |
| **subagent** | execução isolada descartável (contexto fresco) | agent `.md` com frontmatter (`mode: subagent`) |
| **hook** | reação automática a evento (session.start, before/after tool) | script idempotente registrado em hooks/ |
| **plugin** | comportamento transversal programático | plugin OpenCode nativo (não wrapper de outro harness) |
| **MCP** | integração com serviço/ferramenta externa | MCP server com traversal-safe + fail-fast |
| **LSP** | linguagem com análise estática valiosa | config LSP global |
| **feature** | capacidade nova fim-a-fim | scaffolding resolutivo global (R44) — nunca ficar em /tmp |

### Campos obrigatórios (todo recurso helenizado)

`name` (lowercase-hífens) · `description` (1-2 linhas precisas) · `mode` · `origin` (prefixo `absorvido:`/`crossover:`/`helenizado:`) · `metadata` (category, version, date, source hash).

### Registro global (R2/R44)

Instalar em `/mnt/dados/Assistente Pessoal/opencode/config/opencode/` — invocável de QUALQUER instância. Proibido deixar em sessão isolada, /tmp ou projeto local.

**Gate G-H:** recurso parseável + funcional + instalado no path global + campos obrigatórios completos + provenance documentada.

## Estágio 4 — FORJA (síntese e validação)

Síntese determinística com precisão cirúrgica (temperature 0.0 para código). TDD obrigatório: RED→GREEN→REFACTOR. Cobertura ≥80%.

### Panteão — validação categórica (R28/R34/R37/R40)

- 4 validadores independentes (um por pilar: decomposição, digestão, normatização, síntese).
- Escala **0.0000001–100** (R34); nota SEMPRE acompanhada de bugs concretos apontados.
- Convergência: **média > 95.0 encerra o dev loop** (excelência absoluta).
- Abaixo de 95 → refutação incansável (R40): loop A2A sem limite entre executor e refutador até impressão real (≥90 + elogios concretos + bugs corrigidos).
- Validador sem evidência → `UNKNOWN` + nota piso (NUNCA default alto — antifraude herdada da auditoria ao original).
- 3 rodadas sem convergência → escalar camada superior (R18).

**Gate G-F (saída):** evidência fresca de execução real (R29) + veredito de impressão + memória cerebral alimentada (R26: aprendizados/ + log.md) + lição arquivada.

---

## Modo MIX + Dev Loop (apoio, R50)

Sempre que houver dúvida de rota/conceito durante qualquer estágio:
1. ≥2 rodadas de buscas web paralelas multi-idioma (pt/en/zh/ru/de/ja...) — síntese tabelada, nunca cópia.
2. EM PARALELO: consultar vault Obsidian (`memória: <tema>` — R26) por conhecimento já digerido.
3. Cruzar externa + vault + dissecação técnica (R46) antes de decidir.
4. Ao concluir: helenizar o aprendizado de volta ao vault (R14) + scaffolding se aplicável (R44).

## Motor full modular (helenizado — IMPLEMENTADO 2026-08-27)

Resolução de motor NUNCA é hardcoded (antipadrão do original v6.0: portas/scan dirs fictícios, auto-aprovação 96.5). O motor helenizado está em `scripts/hefesto_motor.py` (R2/R44):

```bash
# Listar slots CPU vivos (inventário real via llm-inventory.json)
python3 scripts/hefesto_motor.py --list-cpu

# Resolver slot para um papel (R47)
python3 scripts/hefesto_motor.py --resolve forja
python3 scripts/hefesto_motor.py --resolve judge
python3 scripts/hefesto_motor.py --resolve refutador

# Executar workflow com Panteão de validadores
python3 scripts/hefesto_motor.py --execute '{"autophagy_score":96.0,"decompilation_score":97.0,"helenization_score":95.5,"forging_score":98.0}'
```

**Correções aplicadas ao original v6.0:**
- ✅ Paths hardcoded substituídos por `llm-inventory.json` (R35/R47)
- ✅ `_evaluate_pillar` sem evidência → `UNKNOWN` + piso R34 (0.0000001), nunca default 96.5
- ✅ `scoring_range` corrigido para 0.0000001–100 (R34)
- ✅ Logger em `/tmp/opencode/hefesto.log` (seguro, não `/var/log/`)
- ✅ Resolução dinâmica de slots via inventário real (não porta fixa 9090)

**Testes TDD:** `tests/test_hefesto_motor.py` — 21/21 passando (cobertura ≥80%).

## Anti-padrões (proibidos)

- Copiar implementação literal ou criar dependência do agente/framework original.
- Declarar fato sem evidência (estágio 1) ou validar sem evidência (estágio 4).
- Score default alto, aprovação burocrática ("ok", "passou"), impressão simulada.
- Recurso novo quando equivalente já existe no catálogo (R8).
- Scaffolding local/temporário — tudo global (R2/R44).

## Output contract (obrigatório ao fim)

```yaml
artifact: {name, sha256, origin}
decompilation: {structure_map, evidence_total, confirmed: n, unknown: n}
autophagy: {essence: [...], discarded_noise: [...], flaws_found_in_original: [...], gap_confirmed: bool}
helenization: {targets: [{type, path}], registry_updated: bool}
forging: {validators_scores: {D: x, A: x, H: x, F: x}, average: x.x, converged: bool}
memory: {vault_entries: [...], lessons: [...]}
```
