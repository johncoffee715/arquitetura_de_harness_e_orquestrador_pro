---
name: security-methodology
description: >-
  Revisão de segurança de código gerado por IA baseada em metodologia de
  segurança para agentes de código (helenizada de codex-security) + as 5
  vacilações clássicas de apps vibe-coded (helenizada do vídeo Mano Devin).
  Use ao pedir auditoria de segurança, review de app recém-gerado por IA,
  checagem pré-deploy de SAS, ou quando o usuário pedir "está seguro?",
  "acha as brechas", "vulnerabilidades". NÃO substitui o security-research
  (Team Mode) — é a camada rápida de triagem por checklist determinístico.
---
# Security Methodology (helenizada)

## Origem (antropofagia)
- **codex-security** — metodologia de segurança para agentes de código: prompt
  hardening, escopo de permissões, revisão de dependências, threat modeling.
- **Vídeo "Seu SAS feito com IA tá seguro?" (Mano Devin / Yuri Dev)** — 5
  vacilações reais de apps gerados por IA + ferramentas open source.

## As 5 Vacilações (checklist de triagem — SEMPRE rodar nesta ordem)

| # | Vacilação | Onde procurar | Como detectar |
|---|-----------|---------------|---------------|
| 1 | **Banco sem tranca (RLS off)** | Supabase/Firebase/Postgres acessado direto do front | RLS desligado por padrão; front falando com o banco sem backend intermediário; 83% dos vazamentos Supabase |
| 2 | **Permissão decidida no navegador** | localStorage/sessionStorage/cookies contendo role/admin | `admin: true` gravado no front; rota protegida só por `if (isAdmin)` no client |
| 3 | **Rota entregando dado pelo ID (IDOR)** | endpoints REST com id sequencial (`/users/3`, `/orders/105`) | Trocar o ID devolve dados de outro usuário; sem checagem de ownership; sem rate limit (nº 1 do OWASP API) |
| 4 | **Segredo exposto (hardcoded)** | variáveis `API_KEY`, `SECRET`, `sk-...` no código frontend/Git | Build do front expõe TUDO como JS legível; bots varrem GitHub em tempo real (24M segredos vazados em 2024) |
| 5 | **Input sem tratamento (XSS)** | campos que aceitam HTML/arquivos; "HTML personalizado"; upload de imagem | `45%` do código gerado por IA tem falha XSS (Veracode); script escondido em imagem rouba sessão de admin |

## Regras de Ouro (doutrina do vídeo, internalizadas)

1. **Regra de negócio é backend. Front só renderiza.** Nunca `if` de permissão no client.
2. **Segredo nunca vai pro frontend.** Nem escondido — build do front é JS legível por qualquer um.
3. **Tudo que o usuário digita é mentira até prova em contrário.** Validar, limpar, limitar.
4. **Não confie cegamente no navegador.** Script kiddies automatizam; não precisam de sofisticação.
5. **IA abre buracos, mas também acha buracos — se você mandar especificamente.** Prompt genérico "revisa aí" não funciona.

## Prompt de Auditoria (para agentes de código)

```
Revisa este código atrás das 5 falhas de segurança de apps vibe-coded:
1) banco sem tranca (RLS off / acesso direto front→DB)
2) permissão decidida no navegador (admin no localStorage)
3) rota entregando dado pelo ID (IDOR, sem ownership check, sem rate limit)
4) chave/segredo exposto (hardcoded, no build do front, no git)
5) inputs sem tratamento (XSS, HTML personalizado, upload com script)
Liste arquivo por arquivo, linha por linha. NÃO corrija ainda — só reporte.
```

## Ferramentas Open Source (camada automática)

| Ferramenta | Uso | Quando |
|------------|-----|--------|
| **OWASP ZAP** | Scanner de app no ar (DAST) | App já deployado; bater em tudo procurando porta aberta |
| **Gitleaks** | Acha segredos no histórico do Git | Sempre em repositórios; histórico nunca morre |
| **Bandit** | SAST para Python | Código Python |
| **Semgrep** | SAST multi-linguagem (fork gratuito de Snyk/CodeQL) | Código qualquer linguagem; regras custom |

## Integração com o harness
- Rodar o checklist nas fases F4/F5 do Gran-Mestre para código de apps web.
- Seguir os [Security Gates](/security-review) para aprovação de PR.
- Rotacionar segredos expostos IMEDIATAMENTE (regra §6 do AGENTS.md global).
