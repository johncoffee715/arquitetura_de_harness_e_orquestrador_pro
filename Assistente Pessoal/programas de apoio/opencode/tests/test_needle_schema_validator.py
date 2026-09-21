#!/usr/bin/env python3
"""
Testes TDD para needle-schema-validator
Teste caso por caso. Cada teste deve passar.
"""
import json
import jsonschema
import pytest
import requests
from unittest.mock import patch, MagicMock
from scripts.needle_schema_validator import validate_schema


class TestNeedleSchemaValidator:
    """Testes TDD para needle-schema-validator"""

    def test_payload_valid_schema_ok(self):
        """Teste 1: payload válido contra schema válido → PASSOU_CATEGORICO"""
        payload = {"name": "John", "age": 30}
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name", "age"]
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "PASSOU_CATEGORICO"
        assert result["nota"] >= 90
        assert len(result["bugs"]) == 0

    def test_payload_missing_required_field(self):
        """Teste 2: payload inválido (campo faltando) → NAO_PASSOU"""
        payload = {"name": "John"}  # age é obrigatório
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name", "age"]
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"
        assert result["nota"] < 90
        assert len(result["bugs"]) > 0
        assert "age" in str(result["bugs"])

    def test_payload_wrong_type(self):
        """Teste 3: payload com tipo errado → NAO_PASSOU"""
        payload = {"name": "John", "age": "thirty"}  # age é string, não integer
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name", "age"]
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"
        assert result["nota"] < 90
        assert "type" in str(result["bugs"])

    def test_schema_malformed(self):
        """Teste 4: schema inválido → erro claro"""
        payload = {"name": "John", "age": 30}
        schema = "this is not a valid schema"
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"
        assert result["nota"] < 90
        assert "malformed" in str(result["bugs"]).lower() or "invalid" in str(result["bugs"]).lower()

    def test_payload_with_enum(self):
        """Teste 5: enum constraint"""
        payload = {"status": "active"}
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["active", "inactive", "pending"]}
            },
            "required": ["status"]
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "PASSOU_CATEGORICO"
        assert result["nota"] >= 90

    def test_payload_outside_enum(self):
        """Teste 6: valor fora do enum → NAO_PASSOU"""
        payload = {"status": "deleted"}
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["active", "inactive", "pending"]}
            },
            "required": ["status"]
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"
        assert result["nota"] < 90
        assert "enum" in str(result["bugs"])

    def test_nested_object_valid(self):
        """Teste 7: objeto aninhado válido"""
        payload = {
            "user": {"name": "Alice", "age": 25},
            "address": {"street": "Rua A", "city": "São Paulo"}
        }
        schema = {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"}
                    },
                    "required": ["name", "age"]
                },
                "address": {
                    "type": "object",
                    "properties": {
                        "street": {"type": "string"},
                        "city": {"type": "string"}
                    }
                }
            },
            "required": ["user"]
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "PASSOU_CATEGORICO"
        assert result["nota"] >= 90

    def test_nested_object_missing_field(self):
        """Teste 8: objeto aninhado com campo faltando → NAO_PASSOU"""
        payload = {
            "user": {"name": "Alice"}  # age é obrigatório
        }
        schema = {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"}
                    },
                    "required": ["name", "age"]
                }
            },
            "required": ["user"]
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"

    def test_fallback_jsonschema_needle_offline(self):
        """Teste 9: Needle offline (timeout) → fallback jsonschema"""
        payload = {"name": "John", "age": 30}
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name", "age"]
        }

        # Simular Needle offline
        with patch("requests.post", side_effect=requests.exceptions.ConnectionError("Needle offline")):
            result = validate_schema(payload, schema)
            # Se Needle offline, usa jsonschema fallback
            assert result["veredito"] == "PASSOU_CATEGORICO"
            assert result["nota"] >= 90

    def test_fallback_jsonschema_payload_invalid(self):
        """Teste 10: Needle offline + payload inválido → fallback detecta erro"""
        payload = {"name": "John"}  # age faltando
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name", "age"]
        }

        with patch("requests.post", side_effect=requests.exceptions.ConnectionError("Needle offline")):
            result = validate_schema(payload, schema)
            assert result["veredito"] == "NAO_PASSOU"
            assert result["nota"] < 90
            assert "age" in str(result["bugs"])

    def test_complex_schema_with_all_constraints(self):
        """Teste 11: schema complexo com múltiplas restrições"""
        payload = {
            "id": 12345,
            "name": "Alice",
            "email": "alice@example.com",
            "tags": ["admin", "user", "active"],
            "metadata": {
                "created_at": "2026-01-01T00:00:00Z",
                "version": 1
            }
        }
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "minimum": 1, "maximum": 999999},
                "name": {"type": "string", "minLength": 1, "maxLength": 100},
                "email": {"type": "string", "format": "email"},
                "tags": {"type": "array", "items": {"type": "string"}},
                "metadata": {
                    "type": "object",
                    "properties": {
                        "created_at": {"type": "string", "format": "date-time"},
                        "version": {"type": "integer", "minimum": 1}
                    }
                }
            },
            "required": ["id", "name", "email"]
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "PASSOU_CATEGORICO"
        assert result["nota"] >= 90

    def test_complex_schema_missing_required(self):
        """Teste 12: schema complexo com campo obrigatório faltando"""
        payload = {
            "id": 12345,
            "name": "Alice"
            # email faltando
        }
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string", "format": "email"}
            },
            "required": ["id", "name", "email"]
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"

    def test_invalid_json_payload(self):
        """Teste 13: payload não é JSON válido"""
        payload = "not a json object"
        schema = {"type": "object", "properties": {"name": {"type": "string"}}}
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"
        assert result["nota"] < 90

    def test_invalid_schema_json(self):
        """Teste 14: schema não é JSON válido"""
        payload = {"name": "John"}
        schema = "this is not a schema"
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"
        assert result["nota"] < 90

    def test_pattern_constraint(self):
        """Teste 15: pattern constraint"""
        payload = {"phone": "+1-555-1234"}
        schema = {
            "type": "object",
            "properties": {
                "phone": {"type": "string", "pattern": r"^\\+?\\d{1,3}-?\\d{3}-?\\d{4}$"}
            },
            "required": ["phone"]
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "PASSOU_CATEGORICO"

    def test_pattern_constraint_violated(self):
        """Teste 16: pattern constraint violado"""
        payload = {"phone": "invalid-phone"}
        schema = {
            "type": "object",
            "properties": {
                "phone": {"type": "string", "pattern": r"^\\+?\\d{1,3}-?\\d{3}-?\\d{4}$"}
            },
            "required": ["phone"]
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"
        assert result["nota"] < 90

    def test_one_of_constraint(self):
        """Teste 17: oneOf constraint"""
        payload = {"mode": "production"}
        schema = {
            "type": "object",
            "properties": {
                "mode": {"oneOf": [
                    {"type": "string", "enum": ["production", "staging"]},
                    {"type": "string", "enum": ["development"]}
                ]}
            },
            "required": ["mode"]
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "PASSOU_CATEGORICO"
        assert result["nota"] >= 90

    def test_one_of_constraint_violated(self):
        """Teste 18: oneOf constraint violado"""
        payload = {"mode": "testing"}
        schema = {
            "type": "object",
            "properties": {
                "mode": {"oneOf": [
                    {"type": "string", "enum": ["production", "staging"]},
                    {"type": "string", "enum": ["development"]}
                ]}
            },
            "required": ["mode"]
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"
        assert result["nota"] < 90

    def test_all_of_constraint(self):
        """Teste 19: allOf constraint"""
        payload = {"name": "John", "age": 30, "active": True}
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "active": {"type": "boolean"}
            },
            "required": ["name", "age", "active"]
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "PASSOU_CATEGORICO"
        assert result["nota"] >= 90

    def test_not_constraint(self):
        """Teste 20: not constraint"""
        payload = {"status": "active"}
        schema = {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "not": {"type": "string", "enum": ["deleted", "archived"]}
                }
            },
            "required": ["status"]
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "PASSOU_CATEGORICO"
        assert result["nota"] >= 90

    def test_not_constraint_violated(self):
        """Teste 21: not constraint violado"""
        payload = {"status": "deleted"}
        schema = {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "not": {"type": "string", "enum": ["deleted", "archived"]}
                }
            },
            "required": ["status"]
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"
        assert result["nota"] < 90

    def test_additional_properties_allowed(self):
        """Teste 22: additionalProperties: true"""
        payload = {"name": "John", "extra": "field", "age": 30}
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name", "age"],
            "additionalProperties": True
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "PASSOU_CATEGORICO"
        assert result["nota"] >= 90

    def test_additional_properties_denied(self):
        """Teste 23: additionalProperties: false"""
        payload = {"name": "John", "extra": "field", "age": 30}
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name", "age"],
            "additionalProperties": False
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"

    def test_items_array_constraint(self):
        """Teste 24: items constraint em arrays"""
        payload = {"items": [1, 2, 3, "string"]}
        schema = {
            "type": "object",
            "properties": {
                "items": {"type": "array", "items": {"type": "integer"}}
            }
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"

    def test_multipleOf_constraint(self):
        """Teste 25: multipleOf constraint"""
        payload = {"price": 10.5}
        schema = {
            "type": "object",
            "properties": {
                "price": {"type": "number", "multipleOf": 0.1}
            }
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "PASSOU_CATEGORICO"

    def test_multipleOf_constraint_violated(self):
        """Teste 26: multipleOf constraint violado"""
        payload = {"price": 10.35}  # 10.35 / 0.1 = 103.5 não é inteiro
        schema = {
            "type": "object",
            "properties": {
                "price": {"type": "number", "multipleOf": 0.1}
            }
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"

    def test_minMax_constraints(self):
        """Teste 27: min e max constraints"""
        payload = {"value": 42}
        schema = {
            "type": "object",
            "properties": {
                "value": {"type": "integer", "minimum": 10, "maximum": 100}
            }
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "PASSOU_CATEGORICO"

    def test_minMax_constraints_violated(self):
        """Teste 28: min ou max violado"""
        payload = {"value": 150}
        schema = {
            "type": "object",
            "properties": {
                "value": {"type": "integer", "minimum": 10, "maximum": 100}
            }
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"

    def test_minMax_exclusive_constraints(self):
        """Teste 29: exclusiveMinimum e exclusiveMaximum"""
        payload = {"value": 99}
        schema = {
            "type": "object",
            "properties": {
                "value": {"type": "integer", "exclusiveMinimum": 10, "exclusiveMaximum": 100}
            }
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "PASSOU_CATEGORICO"

    def test_minMax_exclusive_violated(self):
        """Teste 30: exclusiveMinimum violado"""
        payload = {"value": 10}
        schema = {
            "type": "object",
            "properties": {
                "value": {"type": "integer", "exclusiveMinimum": 10, "exclusiveMaximum": 100}
            }
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"

    def test_ref_constraint(self):
        """Teste 31: $ref constraint"""
        payload = {"name": "John", "address": {"street": "Rua A", "city": "São Paulo"}}
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "address": {"$ref": "#/definitions/address"}
            },
            "required": ["name"]
        },
        "definitions": {
            "address": {
                "type": "object",
                "properties": {
                    "street": {"type": "string"},
                    "city": {"type": "string"}
                }
            }
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "PASSOU_CATEGORICO"

    def test_ref_constraint_violated(self):
        """Teste 32: $ref constraint violado"""
        payload = {"name": "John", "address": {"street": "Rua A"}}  # city faltando
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "address": {"$ref": "#/definitions/address"}
            },
            "required": ["name"]
        },
        "definitions": {
            "address": {
                "type": "object",
                "properties": {
                    "street": {"type": "string"},
                    "city": {"type": "string"}
                }
            }
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"

    def test_invalid_json_string(self):
        """Teste 33: payload é string inválida"""
        payload = "not a json object"
        schema = {"type": "object", "properties": {"name": {"type": "string"}}}
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"
        assert result["nota"] < 90

    def test_empty_payload(self):
        """Teste 34: payload vazio contra schema com required"""
        payload = {}
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name", "age"]
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"

    def test_empty_payload_optional_fields(self):
        """Teste 35: payload vazio sem required fields"""
        payload = {}
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "PASSOU_CATEGORICO"

    def test_nullable_field(self):
        """Teste 36: field com nullable"""
        payload = {"name": None}
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string", "nullable": True}
            }
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "PASSOU_CATEGORICO"

    def test_invalid_schema_type(self):
        """Teste 37: schema com type inválido"""
        payload = {"name": "John"}
        schema = {"type": "object"}  # schema válido
        # Teste com schema malformado
        result = validate_schema({"name": "John"}, "not a schema")
        assert result["veredito"] == "NAO_PASSOU"
        assert result["nota"] < 90

    def test_large_payload(self):
        """Teste 38: payload grande (performance)"""
        import time
        payload = {"data": [i for i in range(1000)]}
        schema = {
            "type": "object",
            "properties": {
                "data": {"type": "array", "items": {"type": "integer"}}
            }
        }
        start = time.time()
        result = validate_schema(payload, schema)
        elapsed = time.time() - start
        assert result["veredito"] == "PASSOU_CATEGORICO"
        assert elapsed < 5.0  # deve ser rápido

    def test_unicode_payload(self):
        """Teste 39: payload com unicode"""
        payload = {"name": "José", "name2": "Müller", "emoji": "🎉"}
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "name2": {"type": "string"},
                "emoji": {"type": "string"}
            }
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "PASSOU_CATEGORICO"
        assert result["nota"] >= 90

    def test_deeply_nested(self):
        """Teste 40: deeply nested schema"""
        payload = {
            "level1": {
                "level2": {
                    "level3": {
                        "level4": {
                            "level5": {"value": 42}
                        }
                    }
                }
            }
        }
        schema = {
            "type": "object",
            "properties": {
                "level1": {
                    "type": "object",
                    "properties": {
                        "level2": {
                            "type": "object",
                            "properties": {
                                "level3": {
                                    "type": "object",
                                    "properties": {
                                        "level4": {
                                            "type": "object",
                                            "properties": {
                                                "level5": {
                                                    "type": "object",
                                                    "properties": {
                                                        "value": {"type": "integer"}
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "PASSOU_CATEGORICO"

    def test_invalid_json_string(self):
        """Teste 41: payload inválido como JSON"""
        result = validate_schema("not a json object", {"type": "object"})
        assert result["veredito"] == "NAO_PASSOU"
        assert result["nota"] < 90

    def test_invalid_schema_json(self):
        """Teste 42: schema inválido como JSON"""
        result = validate_schema({"name": "John"}, "not a schema")
        assert result["veredito"] == "NAO_PASSOU"
        assert result["nota"] < 90

    def test_round_trip_valid(self):
        """Teste 43: round-trip valid (payload → schema → payload)"""
        payload = {
            "id": 12345,
            "name": "Alice",
            "email": "alice@example.com",
            "tags": ["admin", "user", "active"],
            "metadata": {
                "created_at": "2026-01-01T00:00:00Z",
                "version": 1
            }
        }
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "minimum": 1, "maximum": 999999},
                "name": {"type": "string", "minLength": 1, "maxLength": 100},
                "email": {"type": "string", "format": "email"},
                "tags": {"type": "array", "items": {"type": "string"}},
                "metadata": {
                    "type": "object",
                    "properties": {
                        "created_at": {"type": "string", "format": "date-time"},
                        "version": {"type": "integer", "minimum": 1}
                    }
                }
            },
            "required": ["id", "name", "email"]
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "PASSOU_CATEGORICO"
        assert result["nota"] >= 90

    def test_empty_string_value(self):
        """Teste 44: string vazia"""
        payload = {"name": ""}
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string", "minLength": 1}
            },
            "required": ["name"]
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"

    def test_null_value(self):
        """Teste 45: null como valor"""
        payload = {"value": None}
        schema = {
            "type": "object",
            "properties": {
                "value": {"type": "integer"}
            },
            "required": ["value"]
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"

    def test_boolean_value(self):
        """Teste 46: boolean como valor"""
        payload = {"active": True, "flag": False}
        schema = {
            "type": "object",
            "properties": {
                "active": {"type": "boolean"},
                "flag": {"type": "boolean"}
            }
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "PASSOU_CATEGORICO"
        assert result["nota"] >= 90

    def test_array_of_objects(self):
        """Teste 47: array de objetos"""
        payload = {
            "items": [
                {"id": 1, "name": "Item 1"},
                {"id": 2, "name": "Item 2"},
                {"id": 3, "name": "Item 3"}
            ]
        }
        schema = {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "name": {"type": "string"}
                        },
                        "required": ["id", "name"]
                    }
                }
            }
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "PASSOU_CATEGORICO"
        assert result["nota"] >= 90

    def test_array_of_objects_invalid(self):
        """Teste 48: array de objetos inválido"""
        payload = {
            "items": [
                {"id": 1, "name": "Item 1"},
                {"id": 2, "name": "Item 2"},
                {"id": 3, "name": "Item 3", "extra": "field"}
            ]
        }
        schema = {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "name": {"type": "string"}
                        },
                        "required": ["id", "name"],
                        "additionalProperties": False
                    }
                }
            }
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"

    def test_required_field_missing(self):
        """Teste 49: campo required faltando"""
        payload = {"name": "John"}
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name", "age"]
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"
        assert "age" in str(result["bugs"])

    def test_success_rate(self):
        """Teste 50: taxa de sucesso em payloads válidos"""
        valid_payloads = [
            {"name": "John", "age": 30},
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"items": [1, 2, 3]},
            {"name": "José", "emoji": "🎉"},
        ]
        valid_schemas = [
            {"type": "object", "properties": {"name": {"type": "string"}, "age": {"type": "integer"}}, "required": ["name", "age"]},
            {"type": "object", "properties": {"id": {"type": "integer"}, "name": {"type": "string"}, "email": {"type": "string", "format": "email"}}, "required": ["id", "name", "email"]},
            {"type": "object", "properties": {"items": {"type": "array", "items": {"type": "integer"}}}},
            {"type": "object", "properties": {"name": {"type": "string"}, "emoji": {"type": "string"}}},
        ]
        success_count = 0
        for payload in valid_payloads:
            for schema in valid_schemas:
                result = validate_schema(payload, schema)
                if result["veredito"] == "PASSOU_CATEGORICO":
                    success_count += 1
        assert success_count == len(valid_payloads) * len(valid_schemas)

    def test_error_message_clarity(self):
        """Teste 51: erro de validação deve ser claro e acionável"""
        payload = {"name": "John", "age": "thirty"}
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name", "age"]
        }
        result = validate_schema(payload, schema)
        assert result["veredito"] == "NAO_PASSOU"
        assert len(result["bugs"]) > 0
        assert "age" in str(result["bugs"])
        assert "integer" in str(result["bugs"])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
