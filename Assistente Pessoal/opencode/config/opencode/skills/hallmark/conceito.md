# Conceito - Hallmark R84 Quarteto (Córtex Talâmico)

Esta habilidade é projetada para gerenciar o ciclo de desenvolvimento de "hallmark" com o quarteto completo de R84. O conceito define a persona, o contexto e as restrições para que a habilidade funcione conforme as exigências do ecossistema.

## Personas Principais
- Hallmark (sistema) - o agente que implementa a habilidade de marcação
- Usuário - o interlocutor que especifica o objetivo de marcação
- Córtex Talâmico - o sistema que processa e organiza o conceito

## Contexto de Operação
- Objetivo: criar e gerenciar habilidades de marcação baseadas em conceitos específicos.
- Limitações: operação limitada ao ambiente de habilidade do harness; nenhum dado sensível é processado sem validação de segurança.
- Métricas de Qualidade: Clareza do conceito (1-100), Adesão ao quarteto R84 (1-100), Coerência estrutural (1-100).

## Exemplos de Uso
1. Usuário especifica um conceito de marcação específico.
2. O sistema avalia o conceito contra as restrições do quarteto R84.
3. O sistema gera a implementação de marcação baseada no conceito.
4. O sistema valida o resultado contra as métricas de qualidade.

## Detalhes de Implementação
- O conceito é mantido em um estado explícito que pode ser revisado e validado por subagentes de revisão.
- O firewall impõe restrições específicas para garantir segurança e conformidade com as políticas de uso.
- A mecanica define o fluxo de ignição e validação, incluindo etapas de compilação e validação.
- O gabarito fornece o schema de definição para o conceito, firewall, mecanica e gabarito.

## Arquitetura de Compatibilidade
- O conceito é compatível com o catálogo global (R8) e os pilares de autorefutação (R40/R41).
- O firewall segue as diretrizes de segurança (R22-R24) e as restrições de janela de contexto (R23/R24).
- A mecanica é projetada para roteamento seguro com helenização e validação estrutural (R14/R17).
- O gabarito é compatível com o contrato de retorno (R35/R36) e os pilares de autorefutação (R40/R41).

## Validations and Checks
- O conceito é estruturado para que o sistema possa gerar e validar a implementação sem depender de arquivos externos.
- O sistema pode gerar implementação completa (helenização) sem depender de código pré-existente.
- O sistema pode validar o resultado contra as métricas definidas ( Clareza, Adesão, Coerência).
- O sistema segue o ciclo de desenvolvimento do Hefesto (Fase 1-4) com decomposição adequada.

## Implementação Detalhada - Conceito
- O conceito contém múltiplas camadas de descrição:
  1. Breve resumo do propósito e alvo da habilidade.
  2. Detalhes técnicos da arquitetura interna (fluxo de dados, etapas, interações).
  3. Restrições de segurança e limitações (exigências de compliance, restrições de janela, limites de VRAM).
  4. Métricas de qualidade e critérios de avaliação (para o usuário entender sucesso).
  5. Casos de uso típicos e exemplos de interação.
  6. Restrições de restação (exigências mínimas de conteúdo, formatação, clareza).
  7. Perguntas frequentes e respostas comuns para o usuário.
  8. Checklist de validação (para garantir completude antes de entregar).
  9. Perguntas de acompanhamento (para guiar o usuário em torno da aplicação).
  10. Documentação de fallback e erro (casos onde a habilidade falha ou requer ajustes).

## Extensões Avançadas
- Suporte a múltiplos quartetos R84 (se houver mais de um tipo de conceito).
- Integração com sistemas de autorefutação (R40/R41) para avaliação de qualidade contínua.
- Configuração dinâmica da métrica (pode ser ajustada conforme o usuário).
- Suporte a diferentes modelos de LLM (para diferentes perfis de usuário).
- Integração com ferramentas de monitoramento (observabilidade, logging).

## Limitações e Considerações
- A habilidade opera dentro dos limites do ambiente do harness (não acessa arquivos de produção sem permissão).
- A validação é baseada em schema e métricas de qualidade; não garante algoritmica perfeita.
- A implementação pode precisar de ajustes adicionais para diferentes tamanhos de contexto ou arquiteturas de modelo.
- A habilidade não gera código bruto diretamente; delega para subagentes quando necessário.
- A validação é baseada em esquemas e métricas, não em testes unitários completos (completa via pipeline Hefesto).

## Referências de Documentação
- R8 - Catálogo Primeiro (regras de categorização e compliance)
- R14 - Ferro (modo MIX + Dev Loop permanente)
- R17 - Ideologia do Meta-Orquestrador: bipolar (polarização de responsabilidade)
- R22 - Decomposição de Tasks Complexas (Dev-Loop)
- R42 - Guardrail de autorefutação (R40/R41)
- R45 - Capacidades (R45: contexto 27K, KV 27.136)
- R46 - Orquestrador NUNCA executa diretamente
