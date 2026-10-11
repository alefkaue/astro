"""SEC-009a: barreira CSRF da API JSON (origem + formato)."""
import pytest
from flask import Flask, jsonify

from app import csrf


@pytest.fixture
def client(monkeypatch):
    monkeypatch.delenv("CYMAG_TRUSTED_ORIGINS", raising=False)
    app = Flask(__name__)
    csrf.init_app(app)
    app.add_url_rule("/api/action", "action", lambda: jsonify(ok=True), methods=["GET", "POST", "DELETE"])
    app.add_url_rule("/static-form", "form", lambda: "ok", methods=["POST"])
    with app.test_client() as c:
        yield c


def test_json_same_origin_allowed(client):
    r = client.post("/api/action", json={}, headers={"Origin": "http://localhost"})
    assert r.status_code == 200


def test_json_without_origin_allowed(client):
    assert client.post("/api/action", json={}).status_code == 200


def test_cross_site_text_plain_form_blocked(client):
    # O ataque clássico: <form enctype="text/plain"> que get_json(force=True) aceitaria.
    r = client.post("/api/action", data='{"a":1}', content_type="text/plain",
                    headers={"Origin": "https://evil.example"})
    assert r.status_code == 403


def test_text_plain_without_header_blocked_even_without_origin(client):
    r = client.post("/api/action", data='{"a":1}', content_type="text/plain")
    assert r.status_code == 403


def test_urlencoded_form_blocked(client):
    assert client.post("/api/action", data={"a": "1"}).status_code == 403


def test_cross_origin_json_blocked(client):
    r = client.post("/api/action", json={}, headers={"Origin": "https://evil.example"})
    assert r.status_code == 403


def test_null_origin_blocked(client):
    r = client.post("/api/action", json={}, headers={"Origin": "null"})
    assert r.status_code == 403


def test_cross_site_referer_blocked_when_no_origin(client):
    r = client.post("/api/action", json={}, headers={"Referer": "https://evil.example/page"})
    assert r.status_code == 403


def test_same_site_referer_allowed(client):
    r = client.post("/api/action", json={}, headers={"Referer": "http://localhost/app"})
    assert r.status_code == 200


def test_bodyless_post_needs_custom_header(client):
    assert client.post("/api/action").status_code == 403
    assert client.post("/api/action", headers={"X-Requested-With": "ASTRO"}).status_code == 200
    assert client.delete("/api/action", headers={"X-Requested-With": "ASTRO"}).status_code == 200


def test_safe_methods_and_non_api_paths_untouched(client):
    assert client.get("/api/action", headers={"Origin": "https://evil.example"}).status_code == 200
    assert client.post("/static-form", data={"a": "1"}).status_code == 200


def test_trusted_origins_env(client, monkeypatch):
    monkeypatch.setenv("CYMAG_TRUSTED_ORIGINS", "https://app.astro.example, https://other.example")
    r = client.post("/api/action", json={}, headers={"Origin": "https://app.astro.example"})
    assert r.status_code == 200
    r = client.post("/api/action", json={}, headers={"Origin": "https://app.astro.example.evil"})
    assert r.status_code == 403


def test_real_app_blocks_cross_site_login(tmp_path, monkeypatch):
    from app import create_app, db
    monkeypatch.setattr(db.config, "DB_PATH", str(tmp_path / "csrf.db"))
    app = create_app()
    assert csrf.check_request in app.before_request_funcs.get(None, [])
    with app.test_client() as c:
        r = c.post("/api/login", data='{"email":"x@y.z","password":"p"}', content_type="text/plain",
                   headers={"Origin": "https://evil.example"})
        assert r.status_code == 403
        assert c.post("/api/logout").status_code == 403
        assert c.post("/api/logout", headers={"X-Requested-With": "ASTRO"}).status_code == 200
