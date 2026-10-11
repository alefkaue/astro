import pytest
from flask import Flask
from app import features
from app.ai.aegis import Aegis


@pytest.mark.parametrize("environment", ["staging", "production", "unknown"])
def test_hosted_gates_do_not_execute_handlers(monkeypatch, environment):
    monkeypatch.setattr(features.config, "ENV", environment)
    for feature in ("ai", "autonomous", "self_billing", "auto_discover"):
        monkeypatch.delenv("CYMAG_ENABLE_" + feature.upper(), raising=False)
    app = Flask(__name__)
    features.init_app(app)
    def forbidden():
        raise AssertionError("Disabled handler executed")
    routes = [("/api/account/plan", "POST"), ("/api/auto_discover", "GET"),
                         ("/api/exploit_chain", "POST"), ("/api/autonomous/run", "POST"),
                         ("/api/admin/ai/test", "POST")]
    for path, method in routes:
        app.add_url_rule(path, path, forbidden, methods=[method])
    with app.test_client() as client:
        for path, method in routes:
            assert client.open(path, method=method).status_code in (403, 404)


def test_ai_gate_prevents_network_even_with_initialized_client(monkeypatch):
    monkeypatch.setattr(features.config, "ENV", "production")
    monkeypatch.delenv("CYMAG_ENABLE_AI", raising=False)
    ai = Aegis()
    ai._client = object()
    assert ai.online is False
    assert ai.call("system", "sensitive evidence") is None
    assert ai.test_key("synthetic-key")["ok"] is False


def test_simulated_billing_and_server_discovery_cannot_be_enabled_in_prod(monkeypatch):
    monkeypatch.setattr(features.config, "ENV", "production")
    monkeypatch.setenv("CYMAG_ENABLE_SELF_BILLING", "1")
    monkeypatch.setenv("CYMAG_ENABLE_AUTO_DISCOVER", "1")
    app = Flask(__name__)
    features.init_app(app)
    with app.test_client() as client:
        assert client.post("/api/account/plan").status_code == 403
        assert client.get("/api/auto_discover").status_code == 404


def test_local_feature_override_and_default(monkeypatch):
    monkeypatch.setattr(features.config, "ENV", "development")
    monkeypatch.delenv("CYMAG_ENABLE_AI", raising=False)
    assert features.enabled("ai")
    monkeypatch.setenv("CYMAG_ENABLE_AI", "0")
    assert not features.enabled("ai")
