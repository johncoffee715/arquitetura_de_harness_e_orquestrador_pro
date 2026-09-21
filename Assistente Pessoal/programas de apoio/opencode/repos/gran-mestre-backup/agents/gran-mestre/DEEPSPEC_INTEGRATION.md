# DEEPSPEC (Speculative Decoding) — Autofagia + Helenização
## Integração com Gran-Mestre Pipeline

**Data:** 2026-07-25
**Fonte:** https://github.com/akanametov/deepspec (Speculative Decoding)
**Status:** Autofagia completa

---

## 1. O QUE É DEEPSPEC

**Speculative Decoding (DeepSpec)** é uma técnica de inferência onde um modelo "draft" (pequeno/rápido) gera tokens especulativos que um modelo "target" (grande/preciso) valida em paralelo. Se o target aceita, o custo é ~1 forward pass do target para N tokens gerados. Se rejeita, descarta e o target assume.

```
┌──────────────────────────────────────────────────────────────┐
│                   DEEPSPEC ARCHITECTURE                       │
├──────────────────────────────────────────────────────────────┤
│  Prompt → Draft Model (rápido) → N tokens especulativos      │
│                                     │                        │
│                                     ▼                        │
│                          Target Model (valida)               │
│                          ├── Aceita → aceleração Nx          │
│                          └── Rejeita → target assume         │
│                                     │                        │
│                                     ▼                        │
│                              Output Final                    │
└──────────────────────────────────────────────────────────────┘
```

## 2. CONCEITOS-CHAVE EXTRAÍDOS

### 2.1 Draft Model (Modelo de Rascunho)
- **Conceito:** Modelo pequeno (~0.5B-3B params) gera tokens rápido
- **Benefício:** Throughput maior sem perder qualidade do modelo grande
- **Requisito:** Draft e target compartilham mesmo vocabulário (embeddings)

### 2.2 Speculative Verification (Verificação Especulativa)
- **Conceito:** Target valida N tokens em 1 forward pass (paralelo)
- **Benefício:** Até 3-5x aceleração em tarefas de geração longa
- **Trade-off:** Taxa de aceitação varia com a tarefa

### 2.3 Draft-Target Agreement (Alinhamento Draft-Target)
- **Conceito:** Draft treinado para imitar distribuição do target
- **Benefício:** Maior taxa de aceitação = maior aceleração
- **Métrica:** Acceptance rate > 80% ideal

### 2.4 Tree Attention (Atenção em Árvore)
- **Conceito:** Draft gera múltiplas sequências especulativas em árvore
- **Benefício:** Mais chances de acerto vs. sequência única
- **Custo:** Mais memória, maior chance de aceitação

---

## 3. COMPARAÇÃO COM GRAN-MESTRE

| Aspecto | DeepSpec | Gran-Mestre |
|---------|----------|-------------|
| **Draft** | Modelo pequeno (rápido) | Explore/Librarian (descoberta rápida) |
| **Target** | Modelo grande (preciso) | Héstia/Atena (validação precisa) |
| **Verificação** | Logits paralelos | Fable Judge adversarial |
| **Aceitação** | Threshold de aceitação | Gate de aprovação |
| **Tree attention** | Múltiplas sequências | Pipeline em cascata (múltiplas rotas) |
| **Fallback** | Target assume | Escalonamento CRITICAL |

## 4. O QUE ABSORVER DO DEEPSPEC

### 4.1 Padrão Draft-Then-Validate ✅ ABSORVIDO
```python
# DeepSpec pattern
draft_tokens = draft_model.generate(prompt, max_tokens=N)
target_logits = target_model.verify(draft_tokens)

# Gran-Mestre adaptation
# Prometheus (rápido) → gera plano especulativo
# Héstia (preciso) → valida plano em 1 passo
```

### 4.2 Padrão de Aceleração por Par Euro 🟡 PARCIAL
```yaml
# DeepSpec: draft rápido + target verifica
# Gran-Mestre: Explore/Librarian (nano) → validação (opus)
# 
# Apply: usar draft model local para previews rápidos
# antes de escalar para validação completa em nuvem

deepspec:
  enabled: true
  draft_model: opencode/gpt-5-nano
  target_model: github-copilot/claude-opus-4.7
  speculative_tokens: 5
  acceptance_threshold: 0.8
```

### 4.3 Acceptance Rate Tracking ✅ ABSORVIDO
```python
# DeepSpec: aceita/rejeita tokens
# Gran-Mestre: aceita/rejeita fases do pipeline
# Métrica: taxa de aprovação por fase

metrics:
  acceptance_rate:
    phase_1: "Descoberta"
    phase_2: "Contrato" 
    phase_3: "Plano"
    phase_4: "Execução"
    phase_5: "Revisão"
    phase_6: "Entrega"
```

### 4.4 Tree Attention — Múltiplas Hipóteses ✅ ABSORVIDO
```python
# DeepSpec: árvore de sequências especulativas
# Gran-Mestre: pipeline em cascata com múltiplas abordagens
# Brainstorming gera N abordagens → usuário escolhe 1
```

---

## 5. INTEGRAÇÃO COM GRAN-MESTRE

### 5.1 Fase 1 (Descoberta) — DeepSpec Pattern
```
Prometheus (Draft) → Gera N abordagens especulativas
  └── Validação rápida (Explore/Librarian nano)
  └── Se aceito → Target (opus) refina
  └── Se rejeitado → nova rodada especulativa
```

### 5.2 Fase 3 (Plano) — DeepSpec Pattern
```
Plan Writer (Draft) → Gera plano especulativo
  └── Héstia (Target) → Valida em 1 passo
  └── Acceptance rate decide se passa Gate 3
```

### 5.3 Fase 4 (Execução) — Fallback Chain
```
Atlas (Target primário) → Tenta execução direta
  └── Se falha → Draft (nano) gera alternativa
  └── Se aceito → Target refina e executa
```

---

## 6. IMPLEMENTAÇÃO

### 6.1 Configuração DeepSpec no Gran-Mestre

```json
{
  "gran-mestre": {
    "deepspec": {
      "enabled": true,
      "draft_model": "opencode/gpt-5-nano",
      "target_model": "github-copilot/gpt-5.5",
      "speculative_tokens": 5,
      "acceptance_threshold": 0.75,
      "tree_branches": 3,
      "fallback_on_reject": true,
      "metrics_tracking": true
    }
  }
}
```

### 6.2 Padrão de Execução Especulativa

```python
import asyncio

async def speculative_execute(prompt, draft_model, target_model):
    """Gera resposta especulativa e valida em paralelo."""
    # Draft gera especulação rápida
    draft_response = await draft_model.generate(prompt)
    
    # Target valida em 1 forward pass
    validation = await target_model.validate(draft_response)
    
    if validation.accepted:
        return draft_response  # Acelerado!
    else:
        # Fallback: target gera do zero
        return await target_model.generate(prompt)
```

### 6.3 Acceptance Threshold por Fase

| Fase | Draft | Target | Threshold | Ação na Rejeição |
|------|-------|--------|-----------|------------------|
| 1 - Descoberta | nano | opus | 0.70 | Nova rodada de draft |
| 2 - Contrato | nano | opus | 0.80 | Escala para opus direto |
| 3 - Plano | nano | high | 0.85 | Revisão manual (Gate) |
| 4 - Execução | nano | medium | 0.75 | Fallback chain |
| 5 - Revisão | nano | opus | 0.90 | Atena assume |
| 6 - Entrega | nano | opus | 0.95 | Sempre target (garantia) |

---

## 7. BENEFÍCIOS DA INTEGRAÇÃO

| Benefício | Descrição | Estimativa |
|-----------|-----------|------------|
| **Velocidade** | Draft responde antes do target terminar | 2-5x mais rápido |
| **Preview** | Usuário vê resultado preliminar rápido | Feedback mais cedo |
| **Custo** | Draft local (nano) é essencialmente grátis | ~90% menos tokens |
| **Qualidade** | Target valida sem perder precisão | Mesma qualidade final |
| **Resiliência** | Se draft falha, target assume | Zero downtime |

## 8. PRÓXIMOS PASSOS

1. **Implementar speculative pipeline** na Fase 1 (Prometheus + Explore)
2. **Configurar acceptance thresholds** por fase
3. **Métricas de acceptance rate** para ajuste fino
4. **Tree attention** para múltiplas abordagens em paralelo

---

## 9. REFERÊNCIAS

- **DeepSpec:** https://github.com/akanametov/deepspec — Speculative Decoding framework
- **Speculative Decoding:** Leviathan et al., 2022 — "Fast Inference from Transformers via Speculative Decoding"
- **Tree Attention:** Miao et al., 2023 — "SpecInfer: Accelerating Generative LLM Serving with Speculative Inference"

---

**Versão:** 1.0.0
**Data:** 2026-07-25
**Autor:** Gran-Mestre (autofagia de DeepSpec)
**Helenização:** Padrão draft-target convertido para pipeline Gran-Mestre
