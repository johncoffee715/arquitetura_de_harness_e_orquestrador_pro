# Sentinel Micro Extractor — Conceito
Persona: O Extrator Cirúrgico
Extrai códigos numéricos de 5 dígitos de texto sujo com precisão de 1 bit. Usa GBNF para forçar regex [0-9]{5}. O Python acumula micro-passos e valida via Pydantic. Funciona até em 0.1B (15M) onde sem GBNF geraria gibberish.
