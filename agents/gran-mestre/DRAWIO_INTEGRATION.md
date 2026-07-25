# Draw.io (Diagrams.net) — Autofagia + Helenização
## Integração com Gran-Mestre Pipeline

**Data:** 2026-07-25
**Fonte:** https://github.com/jgraph/drawio (Apache 2.0)
**Status:** Autofagia completa

---

## 1. O QUE É DRAW.IO

**Draw.io (diagrams.net)** é uma ferramenta de diagramação de código aberto da JGraph. Usa XML como formato nativo (.drawio) e suporta exportação para PNG, SVG, PDF, HTML. Integra-se com editors via plugins e CLI.

```
┌──────────────────────────────────────────────────────────────┐
│                    DRAW.IO / DIAGRAMS.NET                      │
├──────────────────────────────────────────────────────────────┤
│  Formatos:      .drawio (XML) | .png (embutido) | .svg       │
│  Editores:      VS Code plugin | draw.io desktop | Web       │
│  Exportação:    PNG | SVG | PDF | HTML | URL                 │
│  Features:      Camadas | Temas | Shapes custom | Math       │
│  Integração:    Git (diff XML) | Mermaid import | CLI        │
└──────────────────────────────────────────────────────────────┘
```

## 2. CONCEITOS-CHAVE EXTRAÍDOS

### 2.1 XML-Based Diagram Format (Formato XML)
- **Conceito:** Diagramas são armazenados como XML comprimido (ou plano)
- **Benefício:** Versionável em git, diff comparável, editável por script
- **Formato:** `<mxfile><diagram>...</diagram></mxfile>` com `<mxCell>` para nós

### 2.2 Embedded PNG (PNG Embutido)
- **Conceito:** XML pode ser embutido dentro de um PNG (metadados)
- **Benefício:** Arquivo único que é imagem E fonte editável
- **Formato:** PNG padrão + metadados XML no chunk de metadados

### 2.3 Shape Library (Biblioteca de Shapes)
- **Conceito:** Shapes customizáveis como XML (stencils)
- **Benefício:** Reutilização de componentes de diagrama
- **Formato:** Arquivo .xml com definições de stencil

### 2.4 Mermaid Import
- **Conceito:** Importa diagramas Mermaid para edição visual
- **Benefício:** Bridge entre texto e visual
- **Limitação:** Perde alguns detalhes na conversão

---

## 3. COMPARAÇÃO COM GRAN-MESTRE

| Aspecto | Draw.io | Gran-Mestre |
|---------|---------|-------------|
| **Formato** | XML (.drawio) | Markdown (.md) |
| **Versionamento** | Diff XML em git | Diff markdown em git |
| **Diagramas** | Editor visual | ASCII art / Mermaid |
| **Automação** | CLI drawio | Geração de mermaid em scripts |
| **Integração** | VS Code, Web, Desktop | OpenCode CLI |
| **Exportação** | PNG, SVG, PDF | Markdown + renderização |

## 4. O QUE ABSORVER DO DRAW.IO

### 4.1 Padrão XML de Diagrama ✅ ABSORVIDO
```xml
<!-- Draw.io pattern: diagrama como XML -->
<mxfile>
  <diagram id="arch-001" name="Architecture">
    <mxGraphModel>
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="2" value="Component A" style="rounded=1;" parent="1" vertex="1">
          <mxGeometry x="40" y="40" width="120" height="60" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>

# Gran-Mestre adaptation
# Diagramas são documentados como ASCII art em Markdown
# Draw.io pode ser usado como ferramenta de edição visual
# Os .drawio são versionados em git junto com docs
```

### 4.2 Padrão de Arquitetura como Código ✅ ABSORVIDO
```yaml
# Draw.io: diagramas versionados em XML
# Gran-Mestre: arquitetura documentada em Markdown + ASCII
# 
# Draw.io pode ser usado para diagramas complexos:
# - Pipeline do Gran-Mestre (.drawio)
# - Arquitetura de agentes (.drawio)
# - Fluxo de dados (.drawio)
# 
# Script de geração automatizada via CLI:
# drawio --export --format svg --output diagram.svg input.drawio
```

### 4.3 Padrão de Shape Library 🟡 PARCIAL
```
# Draw.io: shapes reutilizáveis em XML
# Gran-Mestre: templates de componente reutilizáveis

# Templates de componente Gran-Mestre como shapes draw.io:
# - Agent shape (Héstia, Atena, Prometheus, Atlas)
# - Gate shape (Gate 1-4)
# - Pipeline shape (standard, cascata)
# - Integração shape (CrossOver)
```

### 4.4 Embedded Format (Auto-Contido) ✅ ABSORVIDO
```markdown
# Draw.io: PNG com XML embutido = auto-contido
# Gran-Mestre: .md com YAML frontmatter = auto-contido
# 
# Mesmo princípio: um arquivo contém:
# 1. Metadados (YAML / XML)
# 2. Conteúdo (markdown / diagrama)
# 3. Versionável (git diff)
```

---

## 5. INTEGRAÇÃO COM GRAN-MESTRE

### 5.1 Diagramas de Pipeline (Draw.io)
```xml
<!-- pipeline.drawio — Diagrama do pipeline Gran-Mestre -->
<mxfile>
  <diagram name="Pipeline Padrão">
    <!-- Fase 1: Descoberta -->
    <!-- Fase 2: Contrato -->
    <!-- Fase 3: Plano -->
    <!-- Fase 4: Execução -->
    <!-- Fase 5: Revisão -->
    <!-- Fase 6: Entrega -->
  </diagram>
  <diagram name="Pipeline Cascata">
    <!-- Fase 1-6 com intercalação Superpowers -->
  </diagram>
  <diagram name="Agentes">
    <!-- Héstia, Atena, Prometheus, Atlas -->
  </diagram>
</mxfile>
```

### 5.2 Geração Automática de Diagramas
```bash
# Comando para gerar diagrama do pipeline atual
drawio-pipeline --phase current --format svg --output docs/pipeline.svg

# Comando para exportar todos os diagramas
drawio-export --input diagrams/ --format png --output docs/diagrams/
```

### 5.3 Integração com Documentação
```markdown
# Em documentação markdown, referenciar diagramas draw.io:
![Pipeline Gran-Mestre](diagrams/pipeline.svg)

# Draw.io original (editável):
[Pipeline Gran-Mestre (editável)](diagrams/pipeline.drawio)
```

---

## 6. IMPLEMENTAÇÃO

### 6.1 Configuração Draw.io no Gran-Mestre

```json
{
  "gran-mestre": {
    "drawio": {
      "enabled": true,
      "diagrams_path": "docs/diagrams/",
      "export_format": "svg",
      "version_control": true,
      "auto_generate": {
        "pipeline": true,
        "architecture": true,
        "agent_flow": true
      },
      "templates": {
        "pipeline": "docs/templates/pipeline.drawio",
        "agent": "docs/templates/agent.drawio"
      }
    }
  }
}
```

### 6.2 Script de Geração de Diagrama

```bash
#!/bin/bash
# generate-pipeline-diagram.sh
# Gera diagrama do pipeline atual a partir do template

TEMPLATE="docs/templates/pipeline.drawio"
OUTPUT_DIR="docs/diagrams"
PHASE=${1:-current}

drawio --export \
  --format svg \
  --output "${OUTPUT_DIR}/pipeline-${PHASE}.svg" \
  "${TEMPLATE}"

echo "Diagram generated: ${OUTPUT_DIR}/pipeline-${PHASE}.svg"
```

### 6.3 Shapes Customizados para Gran-Mestre

```xml
<!-- gran-mestre-shapes.xml — Shapes customizados -->
<shapes>
  <!-- Agent shape -->
  <shape name="agent" h="60" w="120">
    <connections>
      <constraint x="0.5" y="0" perimeter="0" name="top"/>
      <constraint x="0.5" y="1" perimeter="0" name="bottom"/>
    </connections>
    <background>
      <rect x="0" y="0" w="120" h="60" 
            fillColor="#4A90D9" strokeColor="#2171C7" rounded="8"/>
    </background>
    <foreground>
      <text x="60" y="35" fontSize="14" 
            fontWeight="bold" align="center" fillColor="#FFFFFF"/>
    </foreground>
  </shape>
  
  <!-- Gate shape -->
  <shape name="gate" h="40" w="100">
    <background>
      <path>M 0 0 L 100 0 L 100 40 L 0 40 Z</path>
    </background>
  </shape>
</shapes>
```

---

## 7. BENEFÍCIOS DA INTEGRAÇÃO

| Benefício | Descrição |
|-----------|-----------|
| **Visualização** | Diagramas profissionais dos pipelines |
| **Versionamento** | XML diff em git (mudanças rastreáveis) |
| **Edição** | VS Code plugin para edição visual |
| **Automação** | CLI para geração e exportação |
| **Documentação** | Diagramas embutidos em docs markdown |
| **Colaboração** | Draw.io desktop para edição compartilhada |

## 8. PRÓXIMOS PASSOS

1. **Criar template draw.io** do pipeline Gran-Mestre
2. **Configurar shapes customizados** (agent, gate, pipeline)
3. **Automatizar exportação** em svg para documentação
4. **Integrar com geração de relatórios**

---

## 9. REFERÊNCIAS

- **Draw.io:** https://github.com/jgraph/drawio — Apache 2.0, diagramas em XML
- **VS Code Plugin:** drawio:drawio (extensão oficial)
- **Draw.io CLI:**
- **Formato .drawio:** Documentação do schema XML

---

**Versão:** 1.0.0
**Data:** 2026-07-25
**Autor:** Gran-Mestre (autofagia de Draw.io)
**Helenização:** XML diagram pattern convertido para documentação de pipeline
