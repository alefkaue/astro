"""Login throttling regressions with an isolated database and clock."""

from concurrent.futures import ThreadPoolExecutor

import pytest
from flask import Flask

from app import db
from app.auth import ratelimit, routes


@pytest.fixture(autouse=True)
def reset_limiter():
    ratelimit.reset()
    yield
    ratelimit.reset()


@pytest.fixture
def login_client(tmp_path, monkeypatch):
    monkeypatch.setattr(db.config, "DB_PATH", str(tmp_path / "login.db"))
    monkeypatch.setattr(db.config, "ENV", "test")
    db.init_db()
    account = db.create_account("Login tests", plan="profissional")
    db.create_user("owner@example.com", "Owner", "correct-password",
                   role="owner", account_id=account)
    now = [1000.0]
    limiter = ratelimit.LoginRateLimiter(3, 8, 60, clock=lambda: now[0])
    monkeypatch.setattr(ratelimit, "limiter", limiter)
    app = Flask(__name__)
    app.config.update(TESTING=True, SECRET_KEY="login-test")
    app.register_blueprint(routes.auth_bp)
    return app.test_client(), limiter, now


def login(client, email="owner@example.com", password="wrong", ip="192.0.2.1"):
    return client.post("/api/login", json={"email": email, "password": password},
                       environ_overrides={"REMOTE_ADDR": ip})


def test_email_block_and_correct_password_are_limited(login_client, monkeypatch):
    client, _, _ = login_client
    events = []
    monkeypatch.setattr(db, "audit", lambda *args: events.append(args))
    for _ in range(3):
        assert login(client, email=" OWNER@EXAMPLE.COM ").status_code == 401
    monkeypatch.setattr(routes, "check_password_hash",
                        lambda *args: pytest.fail("Blocked request checked password"))
    for password in ("wrong", "correct-password"):
        response = login(client, password=password, ip="192.0.2.2")
        assert response.status_code == 429
        assert response.json == {"error": "Muitas tentativas. Tente novamente mais tarde."}
        assert response.headers["Retry-After"] == "60"
    assert events[-1][0:2] == (None, "login_rate_limited")


def test_block_expires_from_threshold_time(login_client):
    client, _, now = login_client
    assert login(client).status_code == 401
    now[0] += 20
    assert login(client).status_code == 401
    now[0] += 20
    assert login(client).status_code == 401
    now[0] += 59.2
    response = login(client, password="correct-password")
    assert response.status_code == 429
    assert response.headers["Retry-After"] == "1"
    now[0] += 0.8
    assert login(client, password="correct-password").status_code == 200


def test_success_clears_email_but_preserves_ip(login_client):
    client, limiter, _ = login_client
    for _ in range(2):
        assert login(client).status_code == 401
    assert login(client, password="correct-password").status_code == 200
    for _ in range(2):
        assert login(client).status_code == 401
    assert limiter.retry_after("owner@example.com", "192.0.2.2") == 0
    for i in range(4):
        assert login(client, email=f"missing{i}@example.com").status_code == 401
    assert login(client, email="another@example.com").status_code == 429


def test_ip_block_with_different_emails(login_client):
    client, _, _ = login_client
    for i in range(8):
        assert login(client, email=f"missing{i}@example.com").status_code == 401
    response = login(client, password="correct-password")
    assert response.status_code == 429
    assert response.headers["Retry-After"] == "60"
    assert login(client, password="correct-password", ip="192.0.2.2").status_code == 200


def test_missing_and_existing_email_have_same_responses(login_client, monkeypatch):
    client, _, _ = login_client
    checked = []
    original = routes.check_password_hash

    def check(hash_value, password):
        checked.append(hash_value)
        return original(hash_value, password)

    monkeypatch.setattr(routes, "check_password_hash", check)
    for _ in range(3):
        existing = login(client)
        missing = login(client, email="missing@example.com", ip="192.0.2.2")
        assert (existing.status_code, existing.json) == (missing.status_code, missing.json)
    assert checked.count(routes._DUMMY_PASSWORD_HASH) == 3
    existing = login(client)
    missing = login(client, email="missing@example.com", ip="192.0.2.2")
    assert (existing.status_code, existing.json, existing.headers["Retry-After"]) == (
        missing.status_code, missing.json, missing.headers["Retry-After"])


def test_sliding_window_discards_old_failures():
    now = [0]
    limiter = ratelimit.LoginRateLimiter(3, 20, 60, clock=lambda: now[0])
    limiter.record_failure("email", "ip")
    now[0] = 30
    limiter.record_failure("email", "ip")
    now[0] = 60
    limiter.record_failure("email", "ip")
    assert limiter.retry_after("email", "ip") == 0
    now[0] = 61
    limiter.record_failure("email", "ip")
    assert limiter.retry_after("email", "ip") == 60


def test_memory_bound_and_expired_cleanup():
    now = [0]
    limiter = ratelimit.LoginRateLimiter(clock=lambda: now[0], max_keys=10)
    for i in range(100):
        limiter.record_failure(str(i), str(i))
        assert len(limiter._entries) <= 10
    assert ("email", "0") not in limiter._entries
    now[0] = ratelimit.WINDOW_SECONDS
    assert limiter.retry_after("99", "99") == 0
    assert not limiter._entries


def test_concurrent_failures_are_counted():
    limiter = ratelimit.LoginRateLimiter(5, 20, 60, clock=lambda: 0)
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(lambda i: limiter.record_failure(str(i), "shared-ip"), range(40)))
    assert limiter.retry_after("fresh-email", "shared-ip") == 60
    limiter.reset()
    assert limiter.retry_after("fresh-email", "shared-ip") == 0
