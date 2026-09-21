---
name: skill-guidelines
description: Diretrizes canônicas de escrita de skills do harness — padrão quarteto R85, frontmatter mínimo, regra de ignição R91 (quarteto completo ou não ignita) e roteamento R75 (categoria > nome).
version: 1.0.0
tags: [skills, quarteto, R85, R91, R75, guidelines, harness]
---

# SKILL_GUIDELINES — Padrão de Escrita de Skills

> Doc curta e canônica. Skill nova que não cumpre isto NÃO ignita (R91).

## 1. Regra de ignição (R91)

**Skill nova = quarteto completo ou não ignita.** Sem as 4 peças da seção 2, a skill não
entra no catálogo, não recebe roteamento e não é carregada pelo harness. Não existe
"SKILL.md avulso" em produção.

## 2. O Quarteto R85 (4 peças obrigatórias)

| Peça | Papel | Conteúdo mínimo |
|---|---|---|
| `SKILL.md` | Instruções + frontmatter | `name`, `description` (obrigatórios); `version`, `tags` (recomendados) |
| `gabarito.json` | Contrato allow/deny | `feature`, `version`, `descricao`, blocos `allow`/`deny` (tools, paths, apis, formats, sampling) |
| `mecanica.py` | Validação de saída | pydantic `BaseModel` do output estrito (R77 tríplice + R81 constrained decoding) |
| `schema.gbnf` | Gramática byte-exato | regra `root` que força JSON estrito; LLM travado não alucina campo |

Exemplo dourado: `skills/bibliotecario/` (quarteto completo + tooling/).
Referência de bateria: `skills/crivo-padrao/` (usa `schema-probe.gbnf`).

## 3. Frontmatter mínimo (SKILL.md)

```yaml
---
name: nome-da-skill          # kebab-case, único no catálogo
description: Uma frase densa — o que faz, qual regra rege, quando usar.
version: 1.0.0               # semver
tags: [categoria, R-refs]     # categoria primeiro (R75)
---
```

- `description` é o gatilho de roteamento: mencione verbos de uso ("use ao...", "gatilhos:...").
- Sem `name`/`description` a skill é invisível ao catálogo.

## 4. Categoria > nome (R75)

O roteamento do harness é por **categoria** (crivo, ingestão, refutação, forja, memória,
segurança...), não por nome de batismo. Registre a categoria no `tags[0]` e no texto.
Nome bonito não substitui categoria correta: `categoria > nome`.

## 5. Checklist de merge (gate R28)

1. [ ] Quarteto completo (4 peças) no diretório da skill
2. [ ] Frontmatter com `name` + `description` (+ version/tags)
3. [ ] `gabarito.json` com allow/deny explícitos (paths restritos, sampling definido)
4. [ ] `mecanica.py` importa e valida (pydantic) sem erro
5. [ ] `schema.gbnf` parseia e casa com o modelo pydantic
6. [ ] Categoria declarada (R75) e regra de origem citada (ex.: helenizada de X, R84)

Falhou qualquer item → skill fica em `fitragem/` até canonizar (guardrail-llm-fitragem).

## 6. Proibições

- Não duplicar skill existente (catálogo primeiro, R8 — construa só o GAP).
- Não editar à mão espelhos gerados (ex.: alvos do `sync-llm-stack.py`).
- Não publicar skill sem `deny` de segredos (`**/.env`, `**/*.key`, `**/*.pem`).
