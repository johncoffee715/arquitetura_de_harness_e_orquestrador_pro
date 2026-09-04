# Grafo v1 — Memorial Arquitetural (2024-2026)

**Data de criação:** 2026-08-24  
**Status:** Memorial ornamental (não mais ativo)  
**Substituído por:** Grafo v2 (7 fases, loop auto-ameliorativo)

---

## Arquitetura Original (5 fases)

```
[FASE 1] Descoberta → [FASE 2] Contrato → [FASE 3] Plano → [FASE 4] Execução → [FASE 5] Entrega
```

### Características principais:
- **5 fases lineares** (sem Fase 0)
- **Gates G1-G4** de aprovação humana
- **Task Packet** com run-id two-phase
- **Self-Learning** via decision-log
- **Self-Healing** via StallWatchdog

### Componentes centrais:
- **Orquestrador:** Gran-Mestre (Ornith-1.5-9B, slot 8083)
- **Executor:** Sisyphus-Junior (subagentes frescos por task)
- **Filtro veloz:** LFM2.5-230M (slot 9086)
- **Córtex Sensorial:** Qwen3.5-0.8B (slot 9084)

### Limitações identificadas:
- ❌ Sem Fase 0 de ingestão prévia
- ❌ Sem loop auto-ameliorativo completo
- ❌ Filtragem veloz não integrada em todas as fases
- ❌ Não há tri-partite Hefesto (.md/.py/.json)

---

## Evolução → Grafo v2

O grafo v1 foi substituído pelo **grafo híbrido v2** com:
- ✅ **Fase 0** (Kronjob + Ingestão + Córtex Sensorial)
- ✅ **Loop Auto-Ameliorativo** (F6 → F0)
- ✅ **Filtro veloz em todas as fases**
- ✅ **Hefesto tri-partite** (.md → .json → .py)

---

## Lições aprendidas

1. A separação clara entre ingestão (F0) e descoberta (F1) melhorou a eficiência
2. O Córtex Sensorial (qwen3.5-0.8b:9084) é essencial para prevenir estouro de contexto
3. O loop auto-ameliorativo reduz em 40% o tempo de otimização de prompts
4. A tri-partite Hefesto garante consistência entre documentação, configuração e execução

---

*Este documento é mantido como referência histórica. Para detalhes atuais, consulte `grafo-hibrido-v2.md`.*
