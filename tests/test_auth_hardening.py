"""Regression tests without DB or network for authentication gates."""
import pytest
from flask import Flask, session
from app.auth import decorators as auth


@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = "local-test"
    return app


@pytest.mark.parametrize("gate", [auth.login_required, auth.enforce_scan_quota, auth.requires_feature("ai")])
def test_stale_user_is_rejected(app, monkeypatch, gate):
    monkeypatch.setattr(auth.db, "get_user", lambda uid: None)
    with app.test_request_context():
        session["uid"] = 999
        response, code = gate(lambda: "must not execute")()
        assert code == 401


def test_inactive_user_is_rejected(app, monkeypatch):
    monkeypatch.setattr(auth.db, "get_user", lambda uid: {"active": 0})
    with app.test_request_context():
        session["uid"] = 999
        assert auth.current_user() is None
        assert auth.login_required(lambda: "must not execute")()[1] == 401


def test_spoofed_ip_header_is_ignored(app):
    with app.test_request_context(headers={"X-Forwarded-For":"203.0.113.7"}, environ_base={"REMOTE_ADDR":"192.0.2.9"}):
        assert auth.client_ip() == "192.0.2.9"


def test_user_without_organization_is_denied(app, monkeypatch):
    monkeypatch.setattr(auth.db, "get_user", lambda uid: {"active":1,"account_id":None})
    with app.test_request_context():
        session["uid"] = 999
        assert auth.login_required(lambda: "must not execute")()[1] == 403


@pytest.mark.parametrize("role", ["viewer", "owner"])
@pytest.mark.parametrize("path", ["/api/scan", "/api/autonomous/run"])
def test_readonly_and_owner_cannot_start_network_jobs(app, monkeypatch, role, path):
    from app.scans.routes import scans_bp
    from app.autonomous.routes import autonomous_bp
    app.register_blueprint(scans_bp)
    app.register_blueprint(autonomous_bp)
    monkeypatch.setattr(auth.db, "get_user", lambda uid: {"active":1,"account_id":42,"role":role})
    with app.test_client() as client:
        with client.session_transaction() as session:
            session["uid"] = 999
        assert client.post(path, json={}).status_code == 403
