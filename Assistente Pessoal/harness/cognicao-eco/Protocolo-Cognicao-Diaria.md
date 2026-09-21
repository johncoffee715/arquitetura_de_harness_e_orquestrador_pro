# Gran-Mestre — Protocolo de Cognição Diária

## Conceito
O Obsidian é o **cérebro cognitivo** do Gran-Mestre. Toda operação deve passar pelo sistema de cognição diária.

## Fluxo Cognitivo Diário

### Manhã (Início do Dia)
1. **Atenção**: Ler `diario/YYYY-MM-DD/log.md` do dia anterior
2. **Percepção**: Analisar `tarefas/pendentes.md`
3. **Memória**: Verificar `memoria/` para decisões pendentes
4. **Raciocínio**: Priorizar tarefas do dia

### Durante o Dia (Operações)
1. **Atenção**: Verificar `sessions/` antes de qualquer task
2. **Percepção**: Consultar `referencias/` para documentação
3. **Memória**: Atualizar `diario/YYYY-MM-DD/log.md` em tempo real
4. **Linguagem**: Documentar decisões em `decisoes/`
5. **Raciocínio**: Usar pipeline Gran-Mestre

### Noite (Fim do Dia)
1. **Atenção**: Revisar `diario/YYYY-MM-DD/log.md`
2. **Percepção**: Analisar `diario/YYYY-MM-DD/reflexao.md`
3. **Memória**: Atualizar `memoria/` com aprendizados
4. **Linguagem**: Documentar insights em `ideias/YYYY-MM-DD.md`
5. **Raciocínio**: Planejar próximo dia

## Estrutura do Vault

```
ObsidianGranMestre/
├── cognicao/              # Sistema cognitivo
├── sessions/              # Sessions (memória de curto prazo)
├── memoria/               # Memória persistente (longo prazo)
├── referencias/           # Referências técnicas
├── historico/             # Histórico de decisões
├── analise/               # Análises de dados
├── diario/                # Logs diários
│   └── YYYY-MM-DD/
│       ├── log.md         # Log do dia
│       └── reflexao.md    # Reflexão do dia
├── tarefas/               # Gerenciamento de tarefas
│   └── pendentes.md       # Tarefas pendentes
├── ideias/                # Ideias e insights
│   └── YYYY-MM-DD.md      # Ideias do dia
├── decisoes/              # Decisões tomadas
└── MAPA-COGNITIVO.md      # Mapa do vault
```

## Regras de Cognição

### Regra 1: Atenção Primeiro
> **ANTES de qualquer task, verificar `sessions/` e `memoria/`.**
> Isso evita alucinações e perda de contexto.

### Regra 2: Memória em Tempo Real
> **DURANTE a task, atualizar `diario/YYYY-MM-DD/log.md`.**
> Isso mantém o registro atualizado.

### Regra 3: Reflexão Diária
> **NO FIM do dia, preencher `diario/YYYY-MM-DD/reflexao.md`.**
> Isso gera aprendizados contínuos.

### Regra 4: Decisões Documentadas
> **TODA decisão deve ser documentada em `decisoes/`.**
> Isso mantém o histórico completo.

### Regra 5: Ideias Capturadas
> **TODA ideia deve ser capturada em `ideias/YYYY-MM-DD.md`.**
> Isso preserva insights valiosos.

## Comandos Diários

### Início do Dia
```bash
~/obsidian-daily-finetuning.sh
```

### Durante o Dia
```bash
~/obsidian-session-saver.sh save <session_id>
```

### Fim do Dia
```bash
# Editar reflexão
vim ~/ObsidianGranMestre/diario/$(date +%Y-%m-%d)/reflexao.md

# Atualizar memória
vim ~/ObsidianGranMestre/memoria/aprendizados.md
```

## Integração com Gran-Mestre

### Para o Gran-Mestre
1. **ANTES**: Verificar `sessions/` e `memoria/`
2. **DURANTE**: Atualizar `diario/YYYY-MM-DD/log.md`
3. **DEPOIS**: Atualizar `memoria/`, `historico/`, `decisoes/`

### Para o Usuário
1. **Manhã**: Revisar `tarefas/pendentes.md`
2. **Durante**: Adicionar notas em `diario/YYYY-MM-DD/log.md`
3. **Noite**: Preencher `diario/YYYY-MM-DD/reflexao.md`

## Tags do Sistema
- `#cognicao` — Sistema cognitivo
- `#diario` — Log diário
- `#tarefa` — Tarefa pendente
- `#ideia` — Ideia ou insight
- `#decisao` — Decisão tomada
- `#aprendizado` — Lição aprendida
- `#referencia` — Referência técnica
- `#session` — Session do Gran-Mestre

## Métricas de Cognição

### Diário
- Tarefas concluídas
- Decisões tomadas
- Aprendizados gerados
- Ideias capturadas

### Semanal
- Padrões identificados
- Tendências observadas
- Melhorias implementadas
- Insights gerados

### Mensal
- Evolução do sistema
- Lições aprendidas
- Próximos passos
- Visão de futuro

## Conclusão

O Obsidian é o **cérebro cognitivo** do Gran-Mestre. Toda operação deve passar pelo sistema de cognição diária para garantir:
- **Atenção**: Foco no que é importante
- **Percepção**: Contexto completo
- **Memória**: Persistência de informações
- **Linguagem**: Documentação clara
- **Raciocínio**: Decisões informadas

**Usar o Obsidian como fine-tuning diário é essencial para o Gran-Mestre funcionar como um sistema cognitivo completo.**
