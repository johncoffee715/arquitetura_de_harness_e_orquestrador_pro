---
name: self-healing-audit
description: "Template de auditoria e auto-cura do ecossistema Gran-Mestre. Metodologia 14 etapas para análise de skills, subagents, scripts e integrações."
mode: template
version: 1.0.0
author: Gran-Mestre
tags: [audit, self-healing, security, antropofagia, helenizacao]
---

# SELF-HEALING AUDIT — Template 14 Etapas

## Instruções
Para cada skill/subagent/script auditado, preencher as 14 seções abaixo.
Aplicar antropofagia (devorar tecnologia externa) + helenização (converter para OpenCode).

---

## 1. Visão Geral da Arquitetura
### Estado Atual
- Nome do componente:
- Tipo (skill/subagent/script/MCP/hook):
- Localização:
- Tamanho (LOC):
- Linguagem:
- Última atualização:

### Funcionamento
- O que faz:
- Como funciona:
- Input/Output esperados:

### Dependências
- Internas (outras skills/agents):
- Externas (APIs, binários, serviços):
- Runtime requerido (Python/Node/Rust):

---

## 2. Auditoria Técnica

### Pontos Fortes
1.
2.
3.

### Pontos Fracos
1.
2.
3.

### Inconsistências
- [ ] Documentação desatualizada
- [ ] Comportamento divergente da spec
- [ ] Erros de lógica

### Redundâncias
- [ ] Sobreposição com outra skill
- [ ] Funcionalidade duplicada
- [ ] Dead code detectado

---

## 3. Engenharia Reversa

### Reconstrução da Arquitetura
```
Diagrama de fluxo do componente:
```
(ASCII ou referência ao diagrama archify)

### Identificação da Lógica
- Padrão principal:
- Algoritmo central:
- Estruturas de dados:

### Fluxo Operacional
```
1. Trigger → 2. Processamento → 3. Decisão → 4. Saída
```

---

## 4. Análise de Problemas

### Causa Raiz
- Problema identificado:
- Por que ocorre:
- Evidência:

### Impacto
- Severidade (CRÍTICA/IMPORTANTE/OPCIONAL):
- Afeta quantos componentes:
- Usuários afetados:

### Risco
- Probabilidade (Alta/Média/Baixa):
- Facilidade de exploração:
- Mitigação atual:

### Efeito Cascata
- [ ] Bloqueia outras skills
- [ ] Corrompe dados
- [ ] Degrada performance
- [ ] Causa falha silenciosa

---

## 5. Predição

### Possíveis Gargalos Futuros
- [ ] Escalabilidade limitada
- [ ] Dependência de API externa
- [ ] Lock em recurso compartilhado

### Limitações Conhecidas
1.
2.

### Escalabilidade
- Estado atual:
- Limite estimado:
- Estratégia de escala:

### Pontos de Falha
- [ ] Single point of failure
- [ ] Falta de timeout
- [ ] Sem fallback
- [ ] Sem retry logic

---

## 6. Prevenção

### Medidas Preventivas
1.
2.
3.

### Boas Práticas
- [ ] Input validation
- [ ] Error handling
- [ ] Logging estruturado
- [ ] Timeout configurável
- [ ] Retry com backoff

### Validações
- [ ] Validação de entrada
- [ ] Validação de saída
- [ ] Testes de contrato

### Testes Recomendados
- [ ] Unit tests
- [ ] Integration tests
- [ ] Security tests
- [ ] Performance tests

---

## 7. Correção

### Soluções Objetivas
| # | Problema | Solução | Esforço | Prioridade |
|---|----------|---------|---------|------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

### Justificativa Técnica
- Por que esta solução:
- Alternativas consideradas:
- Trade-offs:

### Impacto Esperado
- [ ] Performance: (melhora/piora/neutro)
- [ ] Segurança: (melhora/piora/neutro)
- [ ] Manutenibilidade: (melhora/piora/neutro)

---

## 8. Refatoração

### Simplificação
- [ ] Redução de condicionais aninhadas
- [ ] Extração de funções puras
- [ ] Eliminação de código morto

### Modularização
- [ ] Separação por responsabilidade
- [ ] Interfaces bem definidas
- [ ] Injeção de dependências

### Redução de Complexidade
- Complexidade ciclomática atual:
- Alvo:
- Métrica:

### Melhoria Arquitetural
- [ ] Padrão de design aplicado
- [ ] Acoplamento reduzido
- [ ] Coesão aumentada

---

## 9. Integração

### Compatibilidade com o Projeto
- [ ] OpenCode v1.18.9+
- [ ] Gran-Mestre v7+
- [ ] Modo MIX
- [ ] Dev Loop N1/N2/N3
- [ ] Registry de subagents

### Impacto nos Módulos Existentes
- [ ] SKILL.md do Gran-Mestre
- [ ] REGISTRY_SUBAGENTS.md
- [ ] OBSIDIAN_COGNITIVE_BRAIN.md
- [ ] PIPELINE_MODES.md
- [ ] INVENTORY.md

### Plano de Migração
```
1. Backup: cp target target.bak
2. Patch: aplicar correção
3. Test: validar funcionalidade
4. Verify: fable-judge adversarial
5. Archive: neurônio de decisão no Obsidian
```

---

## 10. Comparação

### Original vs Corrigido

| Aspecto | Original | Corrigido | Benefício |
|---------|----------|-----------|-----------|
| Segurança | | | |
| Performance | | | |
| Manutenibilidade | | | |
| Conformidade | | | |

### Benefícios Obtidos
1.
2.
3.

---

## 11. Melhorias Técnicas

### Imediatas (dias)
1.
2.
3.

### Médio Prazo (semanas)
1.
2.
3.

### Longo Prazo (meses)
1.
2.
3.

---

## 12. Roadmap

### Próxima Evolução Recomendada
- Curto prazo:
- Médio prazo:
- Longo prazo:

### Dependências para Evolução
1.
2.

---

## 13. Checklist

### Implementado ✅
- [ ] Item 1
- [ ] Item 2

### Corrigido 🔧
- [ ] Item 1
- [ ] Item 2

### Pendente ⏳
- [ ] Item 1
- [ ] Item 2

### Futuro 📅
- [ ] Item 1
- [ ] Item 2

---

## 14. Entrega

### Resultado Plug-and-Play
```
Ctrl+A → Ctrl+C → Ctrl+V → Ctrl+S
```

### Script de Auto-Cura
```bash
# Comando para aplicar correção automaticamente
```

### Verificação Pós-Implantação
```bash
# Comando para verificar se correção foi aplicada
```

### Neurônios Criados/Atualizados
- [ ] Decisão em `/decisoes/`
- [ ] Aprendizado em `/aprendizados/`
- [ ] Sinapses atualizadas

---

*Template v1.0.0 — Antropofagia + Helenização + Self-Healing*
*Gerado em: {{date}} | Auditado por: Gran-Mestre*
