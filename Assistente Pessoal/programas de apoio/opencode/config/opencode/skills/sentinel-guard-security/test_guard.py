"""Testes do Sentinel Guard (Hardened)."""
import os
import sqlite3
import pytest

from guard import SentinelGuard, sync_vault_payload


@pytest.fixture
def db(tmp_path):
    p = tmp_path / "v.db"
    conn = sqlite3.connect(str(p))
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, role INTEGER);
        CREATE TABLE IF NOT EXISTS revoked_tokens (hash TEXT PRIMARY KEY);
        INSERT INTO users (id, name, role) VALUES (1, 'alice', 3), (2, 'bob', 1), (3, 'admin', 4);
        """
    )
    conn.commit()
    conn.close()
    return str(p)


def test_find_user_parametrizado_e_sem_injecao(db):
    g = SentinelGuard(db)
    u = g.find_user("alice")
    assert u is not None and u["name"] == "alice" and u["role"] == 3

    # ataque de injecao deve retornar None (nenhum usuario com esse nome literal)
    malicious = "alice' OR '1'='1"
    assert g.find_user(malicious) is None


def test_check_access_usa_role_reais_sem_injecao(db):
    g = SentinelGuard(db)
    # id real 3 = admin role 4 -> acesso
    assert g.check_access(3, "vault") is True
    # id 2 = bob role 1 -> negado
    assert g.check_access(2, "vault") is False
    # id inexistente -> negado (query parametrizada, sem injectar ' OR '1'='1')
    assert g.check_access(999, "vault") is False


def test_validate_token_revogavel(db):
    g = SentinelGuard(db)
    assert g.validate_token("secret-abc")["valid"] is True
    g.revoke_token("secret-abc")
    assert g.validate_token("secret-abc")["valid"] is False
    assert g.validate_token("secret-abc")["revoked"] is True
    assert g.validate_token("")["valid"] is False


def test_find_user_valida_input(db):
    assert SentinelGuard(db).find_user("") is None
    assert SentinelGuard(db).find_user("x" * 200) is None
    assert SentinelGuard(db).find_user(123) is None


def test_sync_vault_payload_exige_api_key(monkeypatch):
    monkeypatch.delenv("VAULT_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        sync_vault_payload(None, {"user": "alice"})
    monkeypatch.setenv("VAULT_API_KEY", "sk-test-xyz")
    payload = sync_vault_payload("sk-test-xyz", "alice")
    assert payload == {"api_key": "sk-test-xyz", "user": "alice"}
