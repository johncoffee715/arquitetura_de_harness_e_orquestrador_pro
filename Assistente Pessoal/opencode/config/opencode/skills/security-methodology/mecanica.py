#!/usr/bin/env python3
"""
Mecânica de auditoria de segurança para apps gerados por IA.
Executa a auditoria em fases de desenvolvimento usando a checklist das 5 vacilações.
Relata apenas as falhas sem corrigir o código.
"""

import json
import sys
from typing import Any, Dict

# Importar schema GBNF (usado pelo bridge de constrained decoding)
try:
    import pydantic_gbnf
except ImportError:
    pydantic_gbnf = None

# Schema de auditoria (usado por ferramentas como OWASP ZAP)
def audit_security(code: str) -> Dict[str, Any]:
    """
    Executa a auditoria de segurança em fases de desenvolvimento.
    Usa a checklist das 5 vacilações em ordem.
    Relata apenas as falhas sem corrigir o código.
    """
    # Lista as 5 vacilações em ordem
    checklist = [
        {
            "name": "Banco sem tranca (RLS off)",
            "description": "A aplicação acessa o banco de dados diretamente do frontend sem middleware de backend intermediário (RLS off).",
            "check": lambda code: "RLS off" in code or "acessar" in code.lower()
        },
        {
            "name": "Permissão decisiva no navegador",
            "description": "O frontend verifica diretamente se o usuário é administrador (ex: admin: true no localStorage).",
            "check": lambda code: "admin" in code.lower() and ("localStorage" in code or "sessionStorage" in code)
        },
        {
            "name": "Rota entregando dado pelo ID (IDOR)",
            "description": "A rota recebe um ID (ex: /users/3) e retorna dados de outro usuário sem verificação de ownership ou rate limiting.",
            "check": lambda code: ("id" in code.lower() or "route" in code.lower()) and "owner" not in code.lower() and "rate" not in code.lower()
        },
        {
            "name": "Segredo exposto (hardcoded)",
            "description": "Variáveis de segredo (API_KEY, SECRET, sk-) são expostas no código frontend ou em arquivos de configuração.",
            "check": lambda code: ("API_KEY" in code.upper() or "SECRET" in code.upper() or "sk-" in code.upper() or "KEY" in code.upper())
        },
        {
            "name": "Input sem tratamento (XSS)",
            "description": "Campos que aceitam HTML/arquivos ou uploads sem validação podem causar XSS.",
            "check": lambda code: ("html" in code.lower() or "upload" in code.lower() or "escape" not in code.lower())
        }
    ]
    
    result = {}
    
    # Verifica cada vacilacao em ordem
    for i, vacilacao in enumerate(checklist, 1):
        name = vacilacao["name"]
        desc = vacilacao["description"]
        check_result = vacilacao["check"](code)
        
        if check_result:
            result[f"vacilias[{i}]"] = {
                "issue": name,
                "description": desc,
                "severity": "HIGH" if i <= 3 else "CRITICAL"
            }
        else:
            result[f"vacilias[{i}]"] = {
                "issue": "OK",
                "description": desc,
                "severity": "LOW"
            }
            
    return {
        "status": "AUDIT_COMPLETED",
        "results": result,
        "timestamp": "2026-08-23T00:00:00Z"
    }

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Mecânica de auditoria de segurança - Executa a auditoria em fases de desenvolvimento.")
        print("Uso: python3 mecanica.py <code>")
        return
    
    if len(sys.argv) < 2:
        print("ERRO: código não fornecido")
        sys.exit(1)
        
    code = sys.argv[1]
    result = audit_security(code)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Verificar se o código é válido JSON (para ferramentas)
    try:
        # O resultado deve ser JSON válido
        json.loads(result)
    except json.JSONDecodeError:
        print("ERRO: Resultado não é JSON válido")
        sys.exit(1)

if __name__ == "__main__":
    main()