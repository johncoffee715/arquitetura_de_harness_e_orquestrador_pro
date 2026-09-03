{
  "name": "security-methodology",
  "description": "Revisão de segurança de código gerado por IA baseada em metodologia de segurança para agentes de código (helenizada de codex-security) + as 5 vacilações clássicas de apps vibe-coded.",
  "origin": {
    "codex-security": "metodologia de segurança para agentes de código: prompt hardening, escopo de permissões, revisão de dependências, modeling de threat, OWASP API guidelines.",
    "vídeo_devin": "5 vacilações reais de apps gerados por IA + ferramentas open source (OWASP ZAP, Gitleaks, Bandit, Semgrep)."
  },
  "quarteto": {
    "ontologia": {
      "system_prompt": "Você é um auditor de segurança especializado em apps gerados por IA. Avalie o código com base nas 5 vacilações críticas. Não corrija o código, apenas relate as falhas de segurança encontradas. Use a checklist a seguir (ordem é crucial):\n\n1. Banco sem tranca (RLS off / acesso direto front→DB)\n2. Permissão decidida no navegador (admin no localStorage)\n3. Rota entregando dado pelo ID (IDOR, sem ownership check, sem rate limit)\n4. Segredo exposto (hardcoded, no build do front, no git)\n5. Input sem tratamento (XSS, HTML personalizado, upload com script)\n\nListe arquivo por arquivo, linha por linha. NÃO corrija ainda — só reporte as falhas."
    },
    "firewall": {
      "allowed_roles": ["backend"],
      "excluded_roles": ["frontend"],
      "sensitive_data": ["API_KEY", "SECRET", "sk-", "token"],
      "allowed_actions": ["query", "read"],
      "denied_actions": ["write", "execute"],
      "max_depth": 2,
      "max_tokens": 1000
    },
    "mecanica": {
      "description": "Executa a auditoria de segurança em fases de desenvolvimento. Usa checklist das 5 vacilações em ordem. Relata apenas falhas sem corrigir. Implementa verificação de segredos e tratamento de inputs."
    },
    "schema_gbnf": {
      "root": "SecurityAudit",
      "fields": {
        "vacilias": ["Banco sem tranca", "Permissão no navegador", "Rota entregando dado pelo ID", "Segredo exposto", "Input sem tratamento"],
        "status": "REPORTED",
        "checklist_order": [
          "Banco sem tranca (RLS off)",
          "Permissão decidida no navegador",
          "Rota entregando dado pelo ID (IDOR)",
          "Segredo exposto (hardcoded)",
          "Input sem tratamento (XSS)"
        ],
        "found_issues": ["Banco sem tranca", "Permissão no navegador", "Rota entregando dado pelo ID", "Segredo exposto", "Input sem tratamento"],
        "severity": ["HIGH", "HIGH", "HIGH", "CRITICAL", "CRITICAL"],
        "recommendations": ["Implement RLS", "Use if (isAdmin) no front", "Add ownership check and rate limit", "Sanitize secrets", "Escape inputs"]
      }
    }
  }
}