"""Testes TDD para sentinel_guard (helenizado de sentinel-guard original).

Cada teste referencia as falhas F-xxx da auditoria adversarial que corrige.
origin: helenizado:/tmp/opencode/forno/sentinel-guard (2026-08-26)
"""
import sqlite3
import sys
import types

import pytest

sys.path.insert(0, "/mnt/dados/Assistente Pessoal/opencode/config/opencode/scripts/sentinel-guard")

import sentinel_guard  # noqa: E402
from sentinel_guard import SentinelGuard, SentinelGuardError, audit_all, sync_vault  # noqa: E402

VALID_TOKEN = "sk-live-" + "a" * 32


@pytest.fixture()
def db(tmp_path):
    path = tmp_path / "vault.db"
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, role TEXT)")
    conn.executemany(
        "INSERT INTO users (id, name, role) VALUES (?, ?, ?)",
        [(1, "bob", "admin"), (2, "alice", "viewer"), (3, "carol", "editor")],
    )
    conn.commit()
    conn.close()
    return str(path)


@pytest.fixture()
def guard(db):
    g = SentinelGuard(db)
    yield g
    g.close()


class TestIntake:
    def test_db_inexistente_falha_rapido(self, tmp_path):  # F-010
        with pytest.raises(SentinelGuardError):
            SentinelGuard(str(tmp_path / "fantasma.db"))

    def test_db_path_invalido(self):  # F-010
        with pytest.raises(SentinelGuardError):
            SentinelGuard("")
        with pytest.raises(SentinelGuardError):
            SentinelGuard(None)


class TestFindUser:
    def test_usuario_legitimo(self, guard):
        rows = guard.find_user("bob")
        assert rows == [(1, "admin")]

    def test_sql_injection_bloqueada(self, guard):  # F-001/F-008
        assert guard.find_user("bob' OR '1'='1") == []
        assert guard.find_user("'; DROP TABLE users;--") == []
        # tabela sobreviveu
        assert guard.find_user("bob") == [(1, "admin")]

    def test_entrada_invalida_levanta(self, guard):  # F-010
        with pytest.raises(SentinelGuardError):
            guard.find_user("")
        with pytest.raises(SentinelGuardError):
            guard.find_user(123)
        with pytest.raises(SentinelGuardError):
            guard.find_user("x" * 129)

    def test_inexistente_vazio(self, guard):
        assert guard.find_user("nobody") == []


class TestCheckAccess:
    def test_admin_escreve(self, guard):
        assert guard.check_access(1, "write") is True

    def test_viewer_le_mas_nao_escreve(self, guard):
        assert guard.check_access(2, "read") is True
        assert guard.check_access(2, "write") is False

    def test_id_desconhecido_negado(self, guard):
        assert guard.check_access(999, "read") is False  # deny by default

    def test_injecao_via_id_negada(self, guard):  # F-002
        assert guard.check_access("1' OR '1'='1", "read") is False

    def test_resource_invalido_levanta(self, guard):  # F-010
        with pytest.raises(SentinelGuardError):
            guard.check_access(1, "")
        with pytest.raises(SentinelGuardError):
            guard.check_access(1, None)
        with pytest.raises(SentinelGuardError):
            guard.check_access(1, "drop table")


class TestValidateToken:
    @pytest.fixture(autouse=True)
    def _env(self, monkeypatch):
        monkeypatch.setenv("SENTINEL_API_KEY", VALID_TOKEN)  # F-003 fix

    def test_env_ausente_falha_fechada(self, monkeypatch):  # F-003
        monkeypatch.delenv("SENTINEL_API_KEY", raising=False)
        with pytest.raises(SentinelGuardError):
            SentinelGuard.__new__(SentinelGuard).validate_token(VALID_TOKEN)

    def test_token_valido_sem_score_magico(self, guard):  # F-004/F-005
        result = guard.validate_token(VALID_TOKEN)
        assert result == {"valid": True}
        assert "score" not in result

    def test_token_ausente(self, guard):
        assert guard.validate_token("") == {"valid": False, "reason": "missing"}
        assert guard.validate_token(None) == {"valid": False, "reason": "missing"}

    def test_token_malformado(self, guard):
        bad = {"valid": False, "reason": "malformed"}
        assert guard.validate_token("abc") == bad
        assert guard.validate_token("sk-x-short") == bad
        assert guard.validate_token(VALID_TOKEN + "; rm -rf /") == bad

    def test_token_errado_rejeitado(self, guard):
        wrong = "sk-live-" + "b" * 32
        result = guard.validate_token(wrong)
        assert result["valid"] is False and result["reason"] == "mismatch"

    def test_comparacao_constante_sobrevive_env_nao_ascii(self, guard, monkeypatch):
        monkeypatch.setenv("SENTINEL_API_KEY", "chave-não-ascii-" + "ç" * 20)
        result = guard.validate_token(VALID_TOKEN)
        assert result["valid"] is False  # não explode com TypeError


class _FakeResponse:
    def __init__(self, payload, status=200):
        self._payload, self.status_code = payload, status

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"http {self.status_code}")


@pytest.fixture()
def fake_requests(monkeypatch):
    calls = []

    def post(url, json=None, headers=None, timeout=None):
        calls.append({"url": url, "json": json, "headers": headers, "timeout": timeout})
        return _FakeResponse({"ok": True, "user": json.get("user") if json else None})

    mod = types.ModuleType("requests")
    mod.post = post
    monkeypatch.setitem(sys.modules, "requests", mod)
    return calls


class TestSyncVault:
    ENDPOINT = "https://sentinel.example.internal/api/vault"

    @pytest.fixture(autouse=True)
    def _key(self, monkeypatch):
        monkeypatch.setenv("SENTINEL_API_KEY", VALID_TOKEN)

    def test_sem_endpoint_falha(self, monkeypatch, fake_requests):  # F-007
        monkeypatch.delenv("SENTINEL_SYNC_ENDPOINT", raising=False)
        with pytest.raises(SentinelGuardError):
            sync_vault({"user": "bob"})

    def test_sem_api_key_fail_closed(self, monkeypatch, fake_requests):  # SELF-001
        monkeypatch.setenv("SENTINEL_SYNC_ENDPOINT", self.ENDPOINT)
        monkeypatch.delenv("SENTINEL_API_KEY", raising=False)
        with pytest.raises(SentinelGuardError):
            sync_vault({"user": "bob"})
        assert fake_requests == []  # nada saiu sem credencial

    def test_post_com_auth_header(self, monkeypatch, fake_requests):  # F-005/F-007
        monkeypatch.setenv("SENTINEL_SYNC_ENDPOINT", self.ENDPOINT)
        monkeypatch.setenv("SENTINEL_API_KEY", VALID_TOKEN)
        out = sync_vault({"user": "bob"})
        assert out["ok"] is True
        call = fake_requests[0]
        assert call["url"] == self.ENDPOINT
        assert call["headers"]["Authorization"] == f"Bearer {VALID_TOKEN}"
        assert call["timeout"] == 30

    def test_endpoint_http_error_propaga(self, monkeypatch):
        monkeypatch.setenv("SENTINEL_SYNC_ENDPOINT", self.ENDPOINT)

        def boom(*a, **kw):
            return _FakeResponse({}, status=500)

        mod = types.ModuleType("requests")
        mod.post = boom
        monkeypatch.setitem(sys.modules, "requests", mod)
        with pytest.raises(RuntimeError):
            sync_vault({"user": "bob"})


class TestAuditAll:
    ENDPOINT = "https://x.example"

    @pytest.fixture(autouse=True)
    def _env(self, monkeypatch):
        monkeypatch.setenv("SENTINEL_SYNC_ENDPOINT", self.ENDPOINT)
        monkeypatch.setenv("SENTINEL_API_KEY", VALID_TOKEN)

    def test_cap_e_throttle(self, monkeypatch, fake_requests):  # F-009
        sleeps = []
        monkeypatch.setattr(sentinel_guard.time, "sleep", sleeps.append)
        users = [f"u{i}" for i in range(sentinel_guard.MAX_AUDIT_USERS + 10)]
        results = audit_all(users)
        assert len(results) == sentinel_guard.MAX_AUDIT_USERS  # cap aplicado
        assert len(fake_requests) == sentinel_guard.MAX_AUDIT_USERS
        assert len(sleeps) == sentinel_guard.MAX_AUDIT_USERS - 1  # throttle entre chamadas
        assert fake_requests[-1]["json"]["user"] == f"u{sentinel_guard.MAX_AUDIT_USERS - 1}"

    def test_lista_vazia_levanta(self, fake_requests):
        with pytest.raises(SentinelGuardError):
            audit_all([])

    def test_usuarios_nao_string_levanta(self, fake_requests):
        with pytest.raises(SentinelGuardError):
            audit_all(["ok", 42])
