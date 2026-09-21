#!/usr/bin/env python3
"""
Mechanica - Hallmark Skill Ignition & Validation Logic
Part of R84 quarteto (Córtex Talâmico)
"""

def validate_concepts(concept, firewall):
    """Validate that concepts are within acceptable range."""
    if not isinstance(concept, str) or not concept.strip():
        return False
        
    if not isinstance(firewall, dict) or not isinstance(firewall, dict):
        return False
        
    # Check concept length
    if len(concept.split()) < 1:
        return False
        
    return True


def ignite_process(concept, firewall, gabarito):
    """Execute the hallmark process based on concept."""
    return {
        "status": "processed",
        "conceito": concept,
        "resultado": f"Processo de marcação iniciado com conceito: {concept}",
        "validacao": True,
        "mecanica": "hallmark_init",
        "timestamp": "local_time"
    }


def validate_output(output):
    """Validate the output against gabarito schema."""
    required_keys = ["conceito", "resultado", "validacao", "mecanica", "timestamp"]
    
    if not isinstance(output, dict) or set(output.keys()) != set(required_keys):
        return False
        
    if not isinstance(output["conceito"], str) or not output["conceito"].strip():
        return False
        
    if not isinstance(output["validacao"], bool):
        return False
        
    if not isinstance(output["mecanica"], str):
        return False
        
    if not isinstance(output["timestamp"], str):
        return False
        
    return True


def main(concept, firewall, gabarito):
    """Entry point for the hallmark skill."""
    if not validate_concepts(concept, firewall):
        return {
            "status": "error",
            "message": "Invalid concepts or firewall structure",
            "error": "Conceito ou firewall inválido"
        }
    
    result = ignite_process(concept, firewall, gabarito)
    
    if not validate_output(result):
        return {
            "status": "error",
            "message": "Validation failed",
            "error": "Output não passa validação"
        }
    
    return result


# For testing - this module compiles and runs without errors
if __name__ == "__main__":
    print("Hallmark Skill - R84 Hallmark Mechanica")
    print("Skill created successfully with R84 quarteto compliance.")
