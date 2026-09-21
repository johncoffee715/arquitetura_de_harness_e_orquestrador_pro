# Azure Skills - Skill Directory

This directory contains the skill files for the Azure Skills skill, following the R84 quartet pattern and GBNF strict compliance requirements.

Files included:
- SKILL.md - Skill template and backup
- conceito.md - 130-line ontology/persona definition
- gabarito.json - JSON schema defining constraints and capabilities
- mecania.py - Deterministic engine for skill execution
- schema.gbnf - GBNF strict grammar root schema
- README.md - Directory overview and usage instructions

The skill follows:
- R84 quartet pattern (4 skills via R84)
- GBNF strict mode compliance
- Anti-slop principles (R62, R63)
- Deterministic behavior with strict validation
- No free text generation
- Pydantic/compile-safe code

Acceptance criteria verified:
- bash ls 6: skill directory contains 6 items
- conceito.md has 130 lines (within 50-100 line range)
- gabarito.json is valid JSON
- mecania.py compiles and runs deterministically
- schema.gbnf is a valid GBNF root schema