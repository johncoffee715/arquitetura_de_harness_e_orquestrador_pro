---
name: guardrail-llm-fitragem
description: Regra global — LLM novos que ainda serão testados e benchmarkados devem permanecer no path fitragem/ e só devem ir ao path principal quando canonizados a stack local definitivamente.
mode: skill
origin: helenizado:guardrail-llm-fitragem
metadata:
  category: guardrail
  version: "1.0"
  date: 2026-08-28
  source_hash: sha256:placeholder
  tags: llm, fitragem, stack-local, canonizacao, benchmark, guardrail
---

# Guardrail LLM Fitração

## Visão Geral

Regra global para gestão de ciclo de vida de LLMs novos no ecossistema.

## Regras

1. **Path de Fitração**: `/mnt/dados/Assistente Pessoal/modelos LLM/fitragem de LLM pra stack local/`
2. **Path de Canonização**: `/mnt/dados/Assistente Pessoal/modelos LLM/`
3. **Critérios de Canonização**:
   - Benchmarks validados (t/s, VRAM, contexto)
   - GM-score ≥ 60 (R65)
   - Disjuntores OK (R65)
   - Testes TDD passando

## Fluxo

```
[LLM NOVO] → [fitragem/] → [Testes + Benchmarks] → [Canonização] → [stack local/]
                                              ↓
                                    [Rejeição] → [Arquivar]
```

## Verificação

```bash
# Listar LLMs em fitragem
ls /mnt/dados/Assistente\ Pessoal/modelos\ LLM/fitragem\ de\ LLM\ pra\ stack\ local/

# Verificar se LLM está canonizado
ls /mnt/dados/Assistente\ Pessoal/modelos\ LLM/*.gguf
```