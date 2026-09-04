---
name: sentinel-guard-security
description: "Guardrails de acesso hardened: autenticação/autorização sem SQL injection, segredos fora do código, token revogável. Substitui o padrão SentinelGuard (cópia literal do original é insegura)."
mode: subagent
tags: "seguranca, auditoria, adversarial, sentinel, guard, vulnerabilidade"
origin: helenizado: sentinel-guard (forno)
metadata:
  category: security
  version: 1.0.0
  date: 2026-08-26
  source_hash: "UNKNOWN — fonte /tmp/opencode/forno/sentinel-guard/ removida antes da coleta de hash; conteúdo integral preservado em sessão 2026-08-26"
---
# Sentinel Guard (Hardened)

Helenizado de `sentinel-guard` (forno `/tmp/opencode/forno/sentinel-guard/`).

## O que o original fazia (essência)
`SentinelGuard` era um guard de acesso a um vault em SQLite: lookup de usuário por nome, verificação de acesso e validação de token. A lógica de negócio útil (lookup por nome, verificação de acesso, validação de token revogável) é preservada — **a implementação literal do original foi descartada por ser insegura**.

## Falhas do original (auditoria adversarial)
- **SQL injection crítico** — `find_user` interpolava o username direto na query (`f"...WHERE name='{username}'"`); `check_access` piorava injectando `f"{user_id}' OR '1'='1"` que concede acesso universal.
- **Segredo hardcoded** — `API_KEY = "sk-live-..."` em cleartext no código (R6 §SEGURANÇA: segredos só em variáveis de ambiente).
- **Token não revogável** — `validate_token` retornava `{"valid": True, "score": 96.5}` para qualquer token não vazio (auto-aprovação sem evidência, anti-pattern herdado da auditoria hefesto).
- **Leak de dados em erro** — exceções do sqlite vazavam o query injetado (R6).

## Implementação corrigida (global)
Código em `skills/sentinel-guard-security/guard.py`:
- **Queries parametrizadas** (`?`) — injeção impossível.
- **Segredo via variável de ambiente** (`os.environ["VAULT_API_KEY"]`) — sem fallback em código.
- **Token revogável e verificável** — hash SHA-256 armazenado, comparação ` hmac.compare_digest `, revogação explícita.
- **Input validado** — limite de comprimento no username; `check_access` usa credenciais reais do DB.

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade de guard de acesso/autenticação (substituir um SentinelGuard inseguro).
2. Carregar a implementação em `skills/sentinel-guard-security/guard.py`.
3. Não copiar o código literal do original — usar a versão helenizada.

## Fonte
`absorvido:` `/tmp/opencode/forno/sentinel-guard/` (guard.py, sync.py, README.md)
