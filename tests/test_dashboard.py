"""Persisted summary: tenant isolation, missing data and validation semantics."""
from pathlib import Path
from uuid import uuid4
import pytest
from flask import Flask
from app import db
from app.dashboard import build_summary, dashboard_bp


@pytest.fixture
def tenants(monkeypatch):
    root = Path(__file__).resolve().parent.parent / ".test-runtime"
    root.mkdir(exist_ok=True)
    monkeypatch.setattr(db.config, "DB_PATH", str(root / (uuid4().hex + ".db")))
    monkeypatch.setattr(db.config, "ENV", "test")
    db.init_db()
    a = db.create_account("A", plan="profissional")
    b = db.create_account("B", plan="profissional")
    uid = db.create_user(uuid4().hex + "@example.com", "A", "test-password", account_id=a)
    def finish(account, findings, target="192.0.2.1"):
        sid = db.create_scan(target, created_by=uid, account_id=account)
        db.finish_scan(sid, findings, 0)
        return sid
    finish(a, [{"host":"192.0.2.1","sev":"crit","verification_status":"confirmed"}])
    sid = finish(a, [{"host":"192.0.2.1","sev":"info","verification_status":"observation"},
                     {"host":"192.0.2.2","sev":"high","verification_status":"suspected"},
                     {"host":"192.0.2.3","sev":"med"}])
    finish(b, [{"host":"203.0.113.1","sev":"crit","verification_status":"confirmed"}])
    return a, b, uid, sid


def test_latest_completed_per_target_and_tenant_isolation(tenants):
    a, b, _, sid = tenants
    summary = build_summary(a)
    assert summary["counts"]["assessments"] == 2
    assert summary["counts"]["confirmed"] == 0
    assert summary["counts"]["pending_validation"] == 1
    assert summary["counts"]["unclassified"] == 1
    assert summary["counts"]["observed_hosts"] == 3
    assert summary["severity"]["crit"] == 0
    assert summary["recent"][0]["id"] == sid
    assert build_summary(b)["counts"]["confirmed"] == 1


def test_no_tenant_is_empty(tenants):
    assert build_summary(None)["counts"]["assessments"] == 0
    assert build_summary(None)["recent"] == []


def test_summary_http_requires_auth_and_uses_session_tenant(tenants):
    a, _, uid, _ = tenants
    app = Flask(__name__)
    app.secret_key = "test-dashboard"
    app.register_blueprint(dashboard_bp)
    with app.test_client() as client:
        assert client.get("/api/dashboard").status_code == 401
        with client.session_transaction() as session:
            session["uid"] = uid
        response = client.get("/api/dashboard?account_id=999")
        assert response.status_code == 200
        assert response.json["counts"] == build_summary(a)["counts"]


def test_flask_serves_single_frontend_and_official_brand(tenants):
    from app import create_app
    app = create_app()
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert b"static/astro.css" in response.data
        assert b"static/astro-theme.js" in response.data
        for path in ("/static/astro.css", "/static/astro-theme.js", "/static/brand/logo-astro-preto.svg", "/static/brand/logo-astro-branco.svg"):
            assert client.get(path).status_code == 200
