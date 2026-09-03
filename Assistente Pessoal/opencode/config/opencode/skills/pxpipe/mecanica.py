# pxpipe mecanica - Ignição e validação para quarteto R84

import json
import os
from pathlib import Path

def validate_skill_files(skill_dir: str) -> bool:
    """
    Verifica se todos os arquivos exigidos para o quarteto estão presentes.
    """
    required_files = {
        "SKILL.md": True,
        "conceito.md": True,
        "gabarito.json": True,
        "mecanica.py": True,
        "schema.gbnf": True
    }
    
    for file_path in required_files.keys():
        full_path = os.path.join(skill_dir, file_path)
        if os.path.isfile(full_path):
            print(f"✓ {file_path} encontrado")
            return True
        else:
            print(f"✗ {file_path} NÃO encontrado em {skill_dir}")
            return False
    
    return True

def main():
    """
    Mecânica de ignição para o quarteto R84.
    Verifica se todos os arquivos exigidos estão presentes antes de iniciar o fluxo.
    """
    skill_dir = "/mnt/dados/Assistente Pessoal/opencode/config/opencode/skills/pxpipe"
    
    print("=== PXPIPE MECÂNICA - IGNÍTION CHECK ===")
    
    if validate_skill_files(skill_dir):
        print("\n✅ Verificação completa - Todos os arquivos presentes")
        print("✅ Quarteto R84 pronta para execução")
        return True
    else:
        print("\n❌ Falha na verificação - Alguns arquivos faltam")
        return False


if __name__ == "__main__":
    main()
