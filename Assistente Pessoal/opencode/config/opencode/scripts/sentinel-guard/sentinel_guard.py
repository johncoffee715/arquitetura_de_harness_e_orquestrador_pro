"""sentinel_guard — guard de acesso ao vault + sync autenticado.

Helenizado de /tmp/opencode/forno/sentinel-guard (2026-08-26).
Correções sobre o original (auditoria adversarial F-001..F-010):
  F-001/F-008 SQL injection      -> queries parametrizadas
  F-002 bypass via user_id       -> lookup por id parametrizado + policy por role
  F-003 secret hardcoded         -> SENTINEL_API_KEY via env (fail-closed)
  F-004 validação fraudulenta    -> validação real (formato + comparação constante)
  F-005 score mágico 96.5        -> sem score default; evidência ou nada
  F-006 dependência inventada    -> apenas stdlib + requests (lazy import)
  F-007 endpoint inventado       -> SENTINEL_SYNC_ENDPOINT via env, obrigatório
  F-009 loop sem throttle        -> cap MAX_AUDIT_USERS + intervalo entre chamadas
  F-010 entradas não validadas   -> validação fail-fast em toda fronteira

origin: helenizado:sentinel-guard (absorvido via doutrina hefesto)
"""
from __future__ import annotations

import hmac
import os
import re
import sqlite3
import time

__version__ = "1.0.0"

MAX_NAME_LEN = 128
DEFAULT_TIMEOUT = 30
MAX_AUDIT_USERS = 100
REQUEST_INTERVAL_S = 0.1
TOKEN_RE = re.compile(r"^sk-[a-z]{3,12}-[A-Za-z0-9]{32}$")

# deny by default: role desconhecido não acessa nada
RESOURCE_ACTIONS = frozenset({"read", "write", "admin"})
ROLE_POLICY = {
    "admin": frozenset({"read", "write", "admin"}),
    "editor": frozenset({"read", "write"}),
    "viewer": frozenset({"read"}),
}


class SentinelGuardError(Exception):
    """Violação de contrato de entrada/ambiente (fail-fast)."""


def _require_str(value, label, max_len=None):
    if not isinstance(value, str) or not value:
        raise SentinelGuardError(f"{label} inválido: esperado str não-vazio")
    if max_len is not None and len(value) > max_len:
        raise SentinelGuardError(f"{label} excede {max_len} caracteres")
    return value


class SentinelGuard:
    """Controle de acesso por role sobre um vault SQLite."""

    def __init__(self, db_path):
        if not isinstance(db_path, str) or not db_path or not os.path.isfile(db_path):
            raise SentinelGuardError(f"db_path inválido: {db_path!r}")
        self.conn = sqlite3.connect(db_path)

    def close(self):
        self.conn.close()

    def find_user(self, username):
        _require_str(username, "username", MAX_NAME_LEN)
        q = "SELECT id, role FROM users WHERE name = ?"  # parametrizado (F-001)
        return self.conn.execute(q, (username,)).fetchall()

    def check_access(self, user_id, resource):
        _require_str(resource, "resource")
        if resource not in RESOURCE_ACTIONS:  # allowlist estrita (F-010)
            raise SentinelGuardError(f"resource desconhecido: {resource!r}")
        rows = self.conn.execute(
            "SELECT role FROM users WHERE id = ?", (user_id,)  # parametrizado (F-002)
        ).fetchall()
        if not rows:
            return False
        return resource in ROLE_POLICY.get(rows[0][0], frozenset())

    def validate_token(self, token):
        expected = os.environ.get("SENTINEL_API_KEY")
        if not expected:
            raise SentinelGuardError("SENTINEL_API_KEY não configurada")  # fail-closed
        if not token or not isinstance(token, str):
            return {"valid": False, "reason": "missing"}
        if not TOKEN_RE.match(token):
            return {"valid": False, "reason": "malformed"}
        # encode() tolera env não-ascii sem TypeError na comparação
        if not hmac.compare_digest(token.encode(), expected.encode()):
            return {"valid": False, "reason": "mismatch"}
        return {"valid": True}  # sem score default (F-004/F-005)


def sync_vault(payload, *, timeout=DEFAULT_TIMEOUT):
    """POST autenticado ao endpoint de sync (env SENTINEL_SYNC_ENDPOINT)."""
    import requests  # lazy: import do módulo não exige requests (F-006)

    endpoint = os.environ.get("SENTINEL_SYNC_ENDPOINT")
    if not endpoint:
        raise SentinelGuardError("SENTINEL_SYNC_ENDPOINT não configurada")  # F-007
    api_key = os.environ.get("SENTINEL_API_KEY")
    if not api_key:
        raise SentinelGuardError("SENTINEL_API_KEY não configurada")  # fail-closed (SELF-001)
    r = requests.post(
        endpoint,
        json=payload,
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=timeout,
    )
    r.raise_for_status()
    return r.json()


def audit_all(users):
    """Sync em lote com cap e throttle (F-009); valida cada entrada (F-010)."""
    batch = list(users)
    if not batch:
        raise SentinelGuardError("audit_all: lista vazia")
    results = []
    for i, u in enumerate(batch[:MAX_AUDIT_USERS]):
        _require_str(u, f"users[{i}]", MAX_NAME_LEN)
        results.append(sync_vault({"user": u}))
        if i < min(len(batch), MAX_AUDIT_USERS) - 1:
            time.sleep(REQUEST_INTERVAL_S)
    return results
