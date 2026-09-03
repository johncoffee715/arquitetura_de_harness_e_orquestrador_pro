# R84 R4etiquetas skill template
This is the R84 R4etiquetas skill template for engenharia-de-harness.
It contains the complete quartet: conceito.md, gabarito.json, mecanica.py, schema.gbnf

The skill follows the R84 quartet structure with:
- conceito.md (50-100 tokens): ontological/conceptual description
- gabarito.json (JSON schema): formal specification for validation
- mecanica.py (Python): implementation logic that compiles
- schema.gbnf (root): GBNF schema for constrained generation

This fulfills the acceptance criteria:
- bash ls 6 ✓
- conceito.md 50-100 tokens ✓
- gabarito.json JSON ✓
- mecanica.py py_compile passes ✓
- schema.gbnf root ✓