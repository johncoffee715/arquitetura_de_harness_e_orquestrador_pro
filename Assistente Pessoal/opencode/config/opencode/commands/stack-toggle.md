---
description: "Toggle stack on/off — liga ou desliga a stack híbrida de LLMs via botão no gerenciador de tarefas"
---

## Comando `/stack-toggle`

### Funcionamento

O comando `/stack-toggle` alterna o estado da stack de LLMs:

- **Se a stack estiver desligada**: executa `start-stack.sh` para levantar todos os slots (orquestrador + slots CPU).
- **Se a stack estiver ligada**: executa `stop-all-models.sh` para desligar gracefully todos os slots.

### Como usar

No terminal OpenCode, digite:

```bash
/stack-toggle
```

O sistema detectará automaticamente o estado atual da stack verificando a saúde dos portos (:8083, :9083, :9084, etc.) e executará a ação apropriada.

### Estado atual

- Verifique a saúde dos portos: `curl -sf -m 2 http://127.0.0.1:<port>/health`
- Logs de execução ficam em `/mnt/dados/Assistente Pessoal/opencode/state/watcher/`

### Nota importante

- O primeiro uso ligará a stack (iniciando orquestrador e todos os especialistas)
- O segundo uso desligará gracefully a stack (SIGTERM → 10s timeout → SIGKILL)
- Não use `pkill -9 -f llama-server` diretamente — use este comando em vez disso
- A stack leva alguns segundos para iniciar completamente (health check automático)