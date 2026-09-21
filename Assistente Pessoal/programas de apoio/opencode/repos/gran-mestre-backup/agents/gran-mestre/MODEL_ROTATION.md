# MODELO DE ROTAÇÃO AUTOMÁTICA — Gran-Mestre
## Sistema de Fallback para não quebrar o workflow

---

## 1. MODELOS DISPONÍVEIS NO HARNESS

### Modelos por Tier

| Tier | Modelo | Provider | Variante | Status |
|------|--------|----------|----------|--------|
| **T1 - Máximo** | claude-opus-4.7 | github-copilot | max | ✅ Disponível |
| **T1 - Máximo** | claude-opus-4-7 | opencode | max | ✅ Disponível |
| **T2 - Alto** | gpt-5.5 | github-copilot | high | ✅ Disponível |
| **T2 - Alto** | gpt-5.5 | opencode | high | ✅ Disponível |
| **T2 - Alto** | gemini-3.1-pro-preview | github-copilot | high | ✅ Disponível |
| **T2 - Alto** | gemini-3.1-pro | opencode | high | ✅ Disponível |
| **T3 - Médio** | claude-sonnet-4.6 | github-copilot | - | ✅ Disponível |
| **T3 - Médio** | claude-sonnet-4-6 | opencode | - | ✅ Disponível |
| **T3 - Médio** | kimi-k2.5 | opencode | - | ✅ Disponível |
| **T4 - Baixo** | gpt-5-nano | opencode | - | ✅ Disponível |
| **T4 - Baixo** | claude-haiku-4.5 | github-copilot | - | ✅ Disponível |
| **T4 - Baixo** | glm-5 | opencode | - | ✅ Disponível |
| **T4 - Baixo** | big-pickle | opencode | - | ✅ Disponível |

---

## 2. ROTAÇÃO POR CATEGORIA DE AGENT

### Agents CRÍTICOS (Héstia, Atena, Prometheus)

```yaml
# Modelo principal + fallback chain
primary: github-copilot/claude-opus-4.7 (max)
fallback_chain:
  1. opencode/claude-opus-4-7 (max)
  2. github-copilot/gpt-5.5 (high)
  3. opencode/gpt-5.5 (high)
  4. github-copilot/gemini-3.1-pro-preview (high)
  5. opencode/gemini-3.1-pro (high)
  6. github-copilot/claude-sonnet-4.6
  7. opencode/claude-sonnet-4-6
  8. opencode/kimi-k2.5
```

### Agents de EXECUÇÃO (Atlas, Implementer)

```yaml
# Modelo principal + fallback chain
primary: github-copilot/claude-sonnet-4.6
fallback_chain:
  1. opencode/claude-sonnet-4-6
  2. github-copilot/gpt-5.5 (medium)
  3. opencode/gpt-5.5 (medium)
  4. opencode/kimi-k2.5
```

### Agents de ANÁLISE (Oracle, Momus, Metis)

```yaml
# Modelo principal + fallback chain
primary: github-copilot/gpt-5.5 (high)
fallback_chain:
  1. opencode/gpt-5.5 (high)
  2. github-copilot/claude-opus-4.7 (max)
  3. opencode/claude-opus-4-7 (max)
  4. github-copilot/gemini-3.1-pro-preview (high)
  5. opencode/gemini-3.1-pro (high)
```

### Agents de EXPLORAÇÃO (Explore, Librarian)

```yaml
# Modelo principal + fallback chain
primary: opencode/gpt-5-nano
fallback_chain:
  1. github-copilot/claude-haiku-4.5
  2. opencode/glm-5
  3. opencode/big-pickle
```

---

## 3. LÓGICA DE ROTAÇÃO

### Regras de Rotação

1. **Tentar modelo principal** — Sempre tentar o modelo definido primeiro
2. **Se falhar, tentar fallback** — Usar o próximo da lista
3. **Máximo 3 tentativas por modelo** — Após 3 falhas no mesmo modelo, pular para o próximo
4. **Escalar ao usuário** — Notificar sobre rotação, MAS continuar tentando
5. **Nunca parar** — Continuar rotacionando entre todos os modelos (pagos e free) até concluir
6. **Log de rotação** — Registrar cada rotação para auditoria
7. **Não quebrar workflow** — Rotação é transparente para o usuário

### Pseudocódigo (v2)

```python
def get_model_with_fallback(agent_name, primary_model, fallback_chain):
    """
    Tenta o modelo principal, se falhar tenta os fallbacks.
    NUNCA para — continua rotacionando até concluir a task.
    Reinicia pelos FREE + modelos que já pago.
    """
    # Ordem: principal → fallback → FREE + PAGOS (reinício)
    paid_models = [
        "github-copilot/claude-sonnet-4.6",
        "opencode/claude-sonnet-4-6",
        "github-copilot/gpt-5.5",
        "opencode/gpt-5.5",
        "opencode/kimi-k2.5"
    ]
    free_models = [
        "opencode/gpt-5-nano",
        "github-copilot/claude-haiku-4.5",
        "opencode/glm-5",
        "opencode/big-pickle"
    ]
    
    all_models = [primary_model] + fallback_chain
    cycle = 0
    
    while True:  # Loop infinito — NUNCA PARA
        cycle += 1
        
        if cycle == 1:
            # Primeiro ciclo: tentar ordem normal
            models_to_try = all_models
        else:
            # Ciclos seguintes: FREE + PAGOS primeiro
            models_to_try = free_models + paid_models + [primary_model]
        
        for model in models_to_try:
            try:
                # Falha em 1x → escalar + próximo
                if is_model_available(model):
                    log_success(agent_name, model, cycle)
                    return model
                else:
                    # Falhou 1 vez — escalar ao usuário
                    escalate_to_user(
                        agent_name,
                        message=f"[Ciclo {cycle}] Modelo {model} falhou. Tentando próximo...",
                        continue=True
                    )
                    log_failure(agent_name, model, cycle)
            except ModelUnavailableError:
                escalate_to_user(
                    agent_name,
                    message=f"[Ciclo {cycle}] Modelo {model} indisponível. Tentando próximo...",
                    continue=True
                )
                log_failure(agent_name, model, cycle)
        
        # Todos falharam neste ciclo — reiniciar
        log_cycle(agent_name, f"Ciclo {cycle} completo — reiniciando com FREE + PAGOS")
```

### Critérios de Disponibilidade

```python
def is_model_available(model):
    """
    Verifica se o modelo está disponível.
    """
    # 1. Verificar se o provider está acessível
    if not check_provider_health(model.provider):
        return False
    
    # 2. Verificar se há quota disponível
    if not check_quota_available(model):
        return False
    
    # 3. Verificar se o modelo está respondendo
    if not check_model_responding(model):
        return False
    
    return True
```

---

## 4. CONFIGURAÇÃO POR AGENT

### Héstia — Guardiã da Conformidade

```yaml
agent: hestia
category: CRITICAL
primary: github-copilot/claude-opus-4.7 (max)
fallback:
  - opencode/claude-opus-4-7 (max)
  - github-copilot/gpt-5.5 (high)
  - opencode/gpt-5.5 (high)
  - github-copilot/claude-sonnet-4.6
  - opencode/claude-sonnet-4-6
max_retries: 3
escalate_on_failure: true
```

### Atena — Revisão Macro

```yaml
agent: atena
category: CRITICAL
primary: github-copilot/claude-opus-4.7 (max)
fallback:
  - opencode/claude-opus-4-7 (max)
  - github-copilot/gpt-5.5 (high)
  - opencode/gpt-5.5 (high)
  - github-copilot/claude-sonnet-4.6
  - opencode/claude-sonnet-4-6
max_retries: 3
escalate_on_failure: true
```

### Prometheus — Planejador

```yaml
agent: prometheus
category: CRITICAL
primary: github-copilot/claude-opus-4.7 (max)
fallback:
  - opencode/claude-opus-4-7 (max)
  - github-copilot/gpt-5.5 (high)
  - opencode/gpt-5.5 (high)
  - github-copilot/gemini-3.1-pro-preview (high)
  - opencode/gemini-3.1-pro (high)
max_retries: 3
escalate_on_failure: true
```

### Atlas — Executor

```yaml
agent: atlas
category: EXECUTION
primary: github-copilot/claude-sonnet-4.6
fallback:
  - opencode/claude-sonnet-4-6
  - github-copilot/gpt-5.5 (medium)
  - opencode/gpt-5.5 (medium)
  - opencode/kimi-k2.5
max_retries: 3
escalate_on_failure: true
```

---

## 5. IMPLEMENTAÇÃO

### Arquivo de Configuração

```json
{
  "gran-mestre": {
    "model_rotation": {
      "enabled": true,
      "max_retries": 3,
      "escalate_on_failure": true,
      "log_rotations": true,
      "agents": {
        "hestia": {
          "category": "CRITICAL",
          "primary": "github-copilot/claude-opus-4.7",
          "fallback": [
            "opencode/claude-opus-4-7",
            "github-copilot/gpt-5.5",
            "opencode/gpt-5.5",
            "github-copilot/claude-sonnet-4.6",
            "opencode/claude-sonnet-4-6"
          ]
        },
        "atena": {
          "category": "CRITICAL",
          "primary": "github-copilot/claude-opus-4.7",
          "fallback": [
            "opencode/claude-opus-4-7",
            "github-copilot/gpt-5.5",
            "opencode/gpt-5.5",
            "github-copilot/claude-sonnet-4.6",
            "opencode/claude-sonnet-4-6"
          ]
        },
        "prometheus": {
          "category": "CRITICAL",
          "primary": "github-copilot/claude-opus-4.7",
          "fallback": [
            "opencode/claude-opus-4-7",
            "github-copilot/gpt-5.5",
            "opencode/gpt-5.5",
            "github-copilot/gemini-3.1-pro-preview",
            "opencode/gemini-3.1-pro"
          ]
        },
        "atlas": {
          "category": "EXECUTION",
          "primary": "github-copilot/claude-sonnet-4.6",
          "fallback": [
            "opencode/claude-sonnet-4-6",
            "github-copilot/gpt-5.5",
            "opencode/gpt-5.5",
            "opencode/kimi-k2.5"
          ]
        }
      }
    }
  }
}
```

---

## 6. LOG DE ROTAÇÃO

### Formato do Log

```json
{
  "timestamp": "2026-07-24T04:30:00Z",
  "agent": "hestia",
  "primary_model": "github-copilot/claude-opus-4.7",
  "used_model": "opencode/claude-opus-4-7",
  "fallback_index": 1,
  "reason": "primary_model_unavailable",
  "retry_count": 1
}
```

### Localização do Log

```
~/.opencode/logs/model-rotation.jsonl
```

---

## 7. RESUMO

### Regras de Rotação (Atualizadas v2)

1. **Falha em 1x** — Modelo falha 1 vez → escalar ao usuário + tentar próximo
2. **Escalar sempre** — Cada falha é notificada ao usuário
3. **Nunca parar** — Continuar rotacionando até concluir a task
4. **Reiniciar ciclo** — Se todos falharam, reiniciar começando pelos FREE + modelos que já pago
5. **Log de cada rotação** — Para auditoria e melhoria
6. **Transparente para o usuário** — Rotação não quebra o workflow

### Ordem de Reinício (FREE + PAGOS)

Quando todos os modelos falharem, reiniciar nesta ordem:
1. **Free primeiro** — opencode/gpt-5-nano, claude-haiku-4.5, glm-5, big-pickle
2. **Pagos que já uso** — claude-sonnet-4.6, gpt-5.5, kimi-k2.5
3. **Máximo** — claude-opus-4.7 (último recurso)

### Benefícios

1. **Não quebra o workflow** — Sempre há um modelo disponível
2. **Auditoria completa** — Cada rotação é registrada
3. **Otimização de custos** — Usa o melhor modelo disponível
4. **Resiliência** — Falha de um modelo não para tudo

---

**Versão:** 1.0.0
**Data:** 2026-07-24
**Autor:** Gran-Mestre