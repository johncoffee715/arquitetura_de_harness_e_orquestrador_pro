# Mecânica
Categoria: descoberta :9093 SmolLM2 400 t/s
GBNF: root ::= "\"codigo\"" ":" "\"" [0-9]{5} "\""
Py: Pydantic Codigo(codigo: str = Field(pattern=r"^[0-9]{5}$")) + filelock
