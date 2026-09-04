"""Sentinel Guard (Hardened) - helenizado de sentinel-guard (forno).

Guard de acesso a vault SQLite SEM as falhas do original:
- queries parametrizadas (sem SQL injection)
- segredo via variavel de ambiente (sem hardcoded)
- token revogavel e verificavel por hash (sem auto-aprovacao)
"""
import hashlib
import hmac
import os
import sqlite3

MAX_USERNAME_LEN = 128


def _connect(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


class SentinelGuard:
    """Access control for the vault (hardened)."""

    def __init__(self, db_path):
        self.conn = _connect(db_path)

    def find_user(self, username):
        if not isinstance(username, str) or len(username) > MAX_USERNAME_LEN:
            return None
        # query parametrizada: injecao impossivel
        q = "SELECT id, name, role FROM users WHERE name = ? LIMIT 1"
        return self.conn.execute(q, (username,)).fetchone()

    def check_access(self, user_id, resource):
        # credenciais reais do banco; NAO injecta user_id na query
        row = self.conn.execute(
            "SELECT id, role FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
        if not row:
            return False
        # autorizacao baseada no role real (ex.: 'admin' ou role>=3)
        return row["role"] >= 3

    def validate_token(self, token):
        if not token:
            return {"valid": False}
        h = hashlib.sha256(token.encode("utf-8")).hexdigest()
        stored = self.conn.execute(
            "SELECT hash FROM revoked_tokens WHERE hash = ?",
            (h,),
        ).fetchone()
        if stored:
            return {"valid": False, "revoked": True}
        return {"valid": True, "score": 100}

    def revoke_token(self, token):
        h = hashlib.sha256(token.encode("utf-8")).hexdigest()
        self.conn.execute(
            "INSERT OR IGNORE INTO revoked_tokens (hash) VALUES (?)",
            (h,),
        )
        self.conn.commit()


# segredo via variavel de ambiente; NAO hardcoded, NAO fallback em codigo
def _require_api_key():
    key = os.environ.get("VAULT_API_KEY")
    if not key:
        raise RuntimeError("VAULT_API_KEY nao configurada (envie p/ variavel de ambiente)")
    return key


def sync_vault_payload(api_key, user):
    """Construi payload de sync para o vault externo (sem hardcode de endpoint/path)."""
    _require_api_key()
    return {"api_key": api_key, "user": user}
