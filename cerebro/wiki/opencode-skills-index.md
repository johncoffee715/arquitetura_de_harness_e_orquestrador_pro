# 🧩 Catálogo de Skills OpenCode

> Atualizado: 17 de Julho de 2026
> Total: **72 skills** catalogadas com MANIFEST.yaml

---

## 📊 Visão Geral

O diretório `opencode-skills/` contém todos os manifests das skills do sistema.
Cada skill tem um `MANIFEST.yaml` com metadados, triggers e requisitos.

---

## 🔍 Como Navegar

- Cada pasta é uma skill com seu `MANIFEST.yaml`
- Skills com prioridade `high` são as mais críticas
- Skills com `requires: [docker]` dependem de Docker rodando

---

## 📋 Skills por Prioridade

### 🔴 Alta (High)

```dataview
TABLE description, triggers, requires
FROM "opencode-skills"
WHERE priority = "high"
SORT file.name ASC
```

### 🟡 Média (Medium)

```dataview
TABLE description, triggers
FROM "opencode-skills"
WHERE priority = "medium"
SORT file.name ASC
```

### 🟢 Baixa (Low)

```dataview
TABLE description, triggers
FROM "opencode-skills"
WHERE priority = "low"
SORT file.name ASC
```

---

## 📂 Skills por Categoria

### GSD Core (52 skills)

```dataview
TABLE priority AS Prioridade
FROM "opencode-skills"
WHERE category = "gsd-core"
SORT priority DESC, file.name ASC
```

### Segurança

```dataview
TABLE priority AS Prioridade
FROM "opencode-skills"
WHERE category = "security"
SORT priority DESC
```

### Pesquisa Web

```dataview
TABLE priority AS Prioridade
FROM "opencode-skills"
WHERE category = "pesquisa-web"
SORT priority DESC
```

---

## ⚡ Skills Recentes

```dataview
TABLE description, priority AS Prioridade
FROM "opencode-skills"
SORT file.ctime DESC
LIMIT 10
```

---

## 📊 Estatísticas

- **Total de skills:** 72
- **High priority:** 14
- **Medium priority:** 46
- **Low priority:** 12
- **Dependências externas:** open-notebook (Docker)

---

## 🔗 Links Rápidos

- [Skills abertas](opencode-skills/)
- [Script de geração automática](/home/johncoffee/scripts/generate-all-manifests.py)
- [Relatório de auditoria](/home/johncoffee/AUDITORIA_2026-07-17.md)
