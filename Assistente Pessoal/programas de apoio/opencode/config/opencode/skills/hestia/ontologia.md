# Hestia Skill - Hestia Fix for Executor-F4 Loop Failure

This skill fixes the loop failure in Executor-F4 for the hestia skill.

The executor is stuck in a loop checking firewall vs ontology repeatedly without progressing.

The fix creates aliases and completes the quarteto R84.

- firewall.json: firewall rules (gabarito.json)
- ontologia.md: ontology concept definition
- mecanica.py: mechanism with Pydantic + filelock
- schema.gbnf: GBNF schema definition