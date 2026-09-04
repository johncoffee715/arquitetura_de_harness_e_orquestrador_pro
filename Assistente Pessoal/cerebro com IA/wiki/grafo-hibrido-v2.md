# Grafo Híbrido v2 — Arquitetura de 7 Fases

**Data:** 2026-08-27  
**Status:** ATIVO (substitui grafo v1)  
**Autor:** Gran-Mestre via Hefesto tri-partite

---

## Visão Geral

```
[FASE 0 — KRONJOB & INGESTÃO]
        │
        ▼
[FASE 1 — DESCOBERTA] → [FASE 2 — CONTRATO] → [FASE 3 — PLANO]
        │                                           │
        └───────────────────┬───────────────────────┘
                            ▼
                     [FASE 4 — EXECUÇÃO]
                            │
                            ▼
                     [FASE 5 — REVISÃO]
                            │
                            ▼
                     [FASE 6 — ENTREGA]
                            │
                            ▼
                     [LOOP AUTO-AMELIORATIVO]
                            │
                            ▼
                     [FASE 0 — KRONJOB & INGESTÃO]
```

---

## FASE 0 — KRONJOB & INGESTÃO

**Propósito:** Filtragem ultraveloz + economia de contexto

**Componentes:**
- **Kronjob:** `context-input-economizer-guardrail`
- **Córtex Sensorial Primário:** qwen3.5-0.8b:9084
- **Filtragem:** LLM mais veloz da stack (lfm230m 399 t/s)

**Fluxo:**
1. Intercepta prompt + contexto + harness + logs
2. Compacta histórico do Obsidian (remover metadados redundantes)
3. Entrega pacote limpo ao Orquestrador (previne estouro de cxt)

---

## FASES 1-6 — Pipeline com Filtro Veloz

### Padrão por fase:

| Fase | Nome | LLM Primário | Filtragem Veloz | Gate |
|------|------|--------------|-----------------|------|
| F1 | Descoberta | Ornith (8083) | LFM230M (9086) | G1 |
| F2 | Contrato | Granite (9087) | LFM230M (9086) | G2 |
| F3 | Plano | Qwen3.8-4B (9088) | LFM230M (9086) | G3 |
| F4 | Execução | Ornith (8083) | LFM230M (9086) | — |
| F5 | Revisão | Judge (9085) | LFM230M (9086) | — |
| F6 | Entrega | Ornith (8083) | LFM230M (9086) | G4 |

### Filtragem Veloz (LFM230M):
- **Propósito:** Limpar/compactar antes de enviar ao LLM primário
- **Técnica:** Remover tokens redundantes, history limpo, prompts pré-compilados
- **Performance:** ~399 t/s (ultraveloz)

---

## LOOP AUTO-AMELIORATIVO (F6 → F0)

**Mecanismo de Scaffold Tri-Partite:**

```
[F6: Métricas da Rodada] → [Orquestrador: Análise Crítica]
                                      │
                    ┌─────────────────┴─────────────────┐
                    ▼                                 ▼
         [.md / Obsidian]                    [.json / Config]
         Memória Epistêmica                  Esquemas de Ferramentas
                    │                                 │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
                           [🤖 SUBAGENTE HEFESTO]
                                      │
                               (Executa .py)
                                      │
                                      ▼
           [SCAFFOLD MUTADO E RECONFIGURADO PARA O FILTRO]
```

### Componentes Tri-Partite:

1. **`.md` — Memória Epistêmica**
   - Local: `cerebro com IA/aprendizados/`
   - Conteúdo: Diagnóstico clínico, lições, padrões

2. **`.json` — Esquemas e Parâmetros**
   - Local: `config/opencode/harness/`
   - Conteúdo: manifest_llm.json, guardrails-schema.json

3. **`.py` — Mecanismo de Execução**
   - Local: `scripts/hefesto_motor.py`
   - Conteúdo: Lógica de mutação, validação, atualização

---

## HARDWARE MAPEAMENTO (AeC)

| Área Cerebral | Função | Hardware | LLM |
|--------------|--------|----------|-----|
| Córtex Filtro | Ingestão ultraveloz | Xeon + RAM | LFM2.5-230M-Q4_0 |
| Hipocampo | Memória semântica | SSD 128GB | Qwen3.5-0.8B (embeddings) |
| Cerebelo | Cache/Compressão | DDR4 | DeepSeek-0.5B |
| Pré-frontal | Raciocínio macro | MI50 | Gran-Mestre (Ornith) |
| Lóbulo Parietal | Validação A2A | MI50 | Refutador (Bonsai) |
| Lóbulo Temporal | Observação/multimodal | MI50 | SilverHawk (LFM-VL) |

---

## REGRAS DE OURO

1. **Filtro veloz em TODAS as fases** (exceto F4 se executor)
2. **Córtex Sensorial** sempre primeiro para input context bruto
3. **Tri-partite Hefesto** sincroniza .md → .json → .py
4. **v1 → memorial** (histórico arquitetural)
5. **NUNCA** criar recurso que já existe no catálogo (R8)

---

## Métricas de Validação

- **Performance:** ≤ 5s por ciclo completo
- **Qualidade:** Média dos validadores ≥ 95 (R34)
- **Convergência:** PASSOU_CATEGORICO (R28)
- **Impressão:** ≥ 90 + elogios concretos (R40)

---

## Próximos passos

- [ ] Validar pipeline Hefesto no novo grafo
- [ ] Testar filtro veloz em F1-F3
- [ ] Atualizar decision-log com novo fluxo
- [ ] Registrar lições no vault Obsidian
