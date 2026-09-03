# DeepAgents Skill

A skill for deepagents that generates optimized, well-structured code.

This skill follows the quarteto R84 pattern with:
- conceito.md (50-100 lines) - ontology/persona description
- gabarito.json (firewall specification) - constraints and allowed inputs
- mecanica.py (mechanics) - Python implementation for code generation/validation
- schema.gbnf (root schema) - GBNF schema root
- SKILL.md (skill definition) - skill metadata

The skill is designed to:
- Generate clean, well-structured Python code
- Apply refactoring and optimization techniques
- Follow best practices for code quality and maintainability
- Handle complex tasks through decomposition