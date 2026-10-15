"""
Testes do fluxo de assinatura/troca de plano (app/billing).

Usa um banco SQLite temporário (definido ANTES de importar o app, pois a
configuração lê o caminho no import) e exercita o endpoint pela ótica do dono.
"""

import uuid
from pathlib import Path

import pytest

from app import create_app
from app.config import config


@pytest.fixture()
def client(monkeypatch):
    path = Path('instance') / f'billing-{uuid.uuid4().hex}.db'
    monkeypatch.setattr(config, 'DB_PATH', str(path))
    monkeypatch.setattr(config, 'DEMO', True)
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as c:
        c.environ_base['HTTP_X_CSRF_TOKEN'] = c.get('/api/csrf').get_json()['csrf_token']
        yield c
    path.unlink(missing_ok=True)


def _login(client, email="dono@pme.com", password="cybersecurity"):
    r = client.post("/api/login", json={"email": email, "password": password})
    if r.status_code == 200:
        client.environ_base['HTTP_X_CSRF_TOKEN'] = r.get_json()['csrf_token']
    return r


def test_owner_can_switch_plan(client):
    assert _login(client).status_code == 200
    r = client.post("/api/account/plan", json={"plan": "gerenciado", "cycle": "year"})
    assert r.status_code == 200
    data = r.get_json()
    assert data["ok"] is True
    assert data["plan"]["key"] == "gerenciado"
    assert data["plan"]["managed"] is True          # plano gerenciado habilita a feature
    assert data["managed_cadence_days"] == 60        # cadência veio do catálogo
    assert data["amount"] == 39000.0                 # preço anual do catálogo


def test_billing_summary_reflects_current_plan(client):
    _login(client)
    client.post("/api/account/plan", json={"plan": "essencial", "cycle": "month"})
    r = client.get("/api/billing/summary")
    assert r.status_code == 200
    s = r.get_json()
    assert s["plan"]["key"] == "essencial"
    assert s["amount"] == 297.0
    assert s["next_charge_at"]                        # plano pago tem próxima cobrança


def test_enterprise_requires_sales(client):
    _login(client)
    r = client.post("/api/account/plan", json={"plan": "enterprise"})
    assert r.status_code == 409
    assert r.get_json().get("contact") is True


def test_invalid_plan_rejected(client):
    _login(client)
    r = client.post("/api/account/plan", json={"plan": "inexistente"})
    assert r.status_code == 400


def test_same_plan_rejected(client):
    _login(client)
    client.post("/api/account/plan", json={"plan": "essencial"})
    r = client.post("/api/account/plan", json={"plan": "essencial"})
    assert r.status_code == 409


def test_non_owner_cannot_change_plan(client):
    # Operador (TI interno) não troca o plano da conta — é decisão do dono.
    assert _login(client, "ti@pme.com").status_code == 200
    r = client.post("/api/account/plan", json={"plan": "gerenciado"})
    assert r.status_code == 403


def test_change_requires_auth(client):
    r = client.post("/api/account/plan", json={"plan": "essencial"})
    assert r.status_code == 401
