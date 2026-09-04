---
name: sdd
description: Speculative Data Distillation — Córtex Sensorial Primário (Filtro Talâmico) operando >100 t/s em CPU com contexto massivo, especulando e condensando fluxos do usuário, nuvem e A2A em tempo real, sofrendo mutações autônomas via SubAgente Hefesto.
mode: skill
origin: absorvido:sdd-speculative-data-distillation
metadata:
  category: sensorial-filter
  version: "1.0"
  date: 2026-08-28
  source_hash: sha256:placeholder
  tags: sdd, thalamus, speculative, distillation, cortex, sensorial, filter, real-time, a2a
---

# SDD — Speculative Data Distillation (Destilação de Dados Especulativa)

## Visão Geral

A SDD é o **Córtex Sensorial Primário (Filtro Talâmico)** da arquitetura híbrida de produção. Operando no modelo local ultraveloz na CPU (>100 t/s) com contexto massivo, ela especula e condensa fluxos em tempo real:

- **Input do Usuário** → especulação probabilística → destilação
- **Input da Nuvem** → especulação probabilística → destilação  
- **Tráfego A2A / Agent Input** → especulação probabilística → destilação

A SDD **NÃO usa parsers técnicos rígidos** (Tec DD). Ela usa a capacidade probabilística do filtro para especular e condensar, sofrendo mutações autônomas através do **SubAgente Hefesto**.

## Arquitetura

```
[FLUXO BRUTO] → [FILTRO TALÂMICO SDD] → [DESTILAÇÃO] → [OUTPUT CONDENSADO]
                     ↑                              ↓
              [SubAgente Hefesto] ←──────── [MUTAÇÃO AUTÔNOMA]
```

### Componentes

1. **Filtro Talâmico (SDD Core)**: Modelo local ultraveloz CPU (>100 t/s, contexto massivo)
   - Especulação probabilística
   - Condensação de fluxos
   - Sem parsers técnicos rígidos

2. **SubAgente Hefesto**: Mutação autônoma
   - Recebe output condensado
   - Aplica decomposição/autofagia/helenização
   - Gera melhorias iterativas

3. **Canais de Input**:
   - Usuário (interface direta)
   - Nuvem (APIs, serviços externos)
   - A2A / Agent Input (comunicação entre agentes)

## Fluxo de Trabalho

### 1. Ingestão
- Recebe fluxo bruto de qualquer canal
- Identifica tipo e densidade de informação
- Prioriza por relevância

### 2. Especulação Probabilística
- Usa modelo local para prever intenções e padrões
- Gera múltiplas hipóteses de interpretação
- Avalia confiança de cada hipótese

### 3. Destilação
- Condensa múltiplas hipóteses em output único
- Remove redundâncias
- Mantém apenas o essencial

### 4. Mutação Autônoma (via Hefesto)
- SubAgente Hefesto recebe output destilado
- Decomõe, digere, heleniza
- Gera versões mutadas e melhoradas

### 5. Feedback Loop
- Output mutado alimenta novo ciclo
- Aprendizado contínuo
- Adaptação ao padrão de uso

## Configuração de Modelo

### Slot Recomendado
- **role:ingestor** (porta 9084, 180 t/s, 18 threads)
  - Arquitetura: RWKV v7 DeltaNet + attention hybrid
  - Contexto: 8192 nativo
  - Peso: 0.91 GB FP16
  - Ideal para: especulação rápida, prompt caching

### Parâmetros de Inferência
- **Temperatura**: 0.7-0.9 (especulação criativa)
- **Top-p**: 0.9
- **Max tokens**: 512-1024 (output condensado)
- **Context window**: 8192 (uso eficiente)

## Integração com o Ecossistema

### Gates de Roteamento
- F1 Descoberta → SDD para pré-filtragem
- F2 Contrato → SDD para condensação de especificação
- F4 Execução → SDD para compressão de contexto
- A2A → SDD para comunicação entre agentes

### Catálogo de Recursos
- **SubAgente Hefesto**: mutação autônoma
- **Skill memory-recall**: recuperação de contexto
- **Hook sdd-talamus-filter**: pré-filtragem Tálamos
- **Plugin guard-gap-p5**: segurança de output

## Anti-padrões (Proibidos)

- Usar parsers técnicos rígidos (Tec DD) — SDD é probabilística
- Especular sem feedback loop — always mutate via Hefesto
- Output bruto sem destilação — sempre condensar
- Hardcoding de modelo — usar inventário real (R35/R47)

## Output Contract

```yaml
sdd:
  input:
    source: user|cloud|a2a
    raw_size_tokens: N
    channel_metadata: {...}
  speculation:
    hypotheses: [H1, H2, ...]
    confidence_scores: [0.95, 0.87, ...]
    top_hypothesis: H_best
  distillation:
    output_tokens: M
    compression_ratio: N/M
    distilled_content: "..."
  mutation:
    hefesto_subagent: invoked
    mutations_applied: [M1, M2, ...]
    final_output: "..."
  metrics:
    tps_decode: 180
    latency_ms: N
    confidence: 0.95
```

## Modo MIX + Dev Loop

Sempre que houver dúvida sobre:
- Qual canal de input processar
- Que nível de especulação aplicar
- Como configurar parâmetros de destilação

1. Consultar vault Obsidian (`memória: sdd`)
2. Buscar web paralela multi-idioma
3. Dissecação técnica (R46)
4. Decidir com evidência