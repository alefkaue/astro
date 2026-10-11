"""
Testes adversariais de isolamento multiempresa (SEC-004).

Monta dois tenants A e B com usuários, engagements, scans e findings próprios e
prova que um usuário de A NÃO alcança recursos de B — mesmo conhecendo os IDs.
Tudo offline: nenhum scan real é disparado; os dados entram direto pela camada db.

    pytest tests/test_tenant_isolation.py
"""

import os
import tempfile

# Banco temporário isolado — precisa estar no ambiente ANTES de importar o app.
_TMP_DB = os.path.join(tempfile.mkdtemp(prefix="cymag_iso_"), "iso.db")
os.environ["CYMAG_DB_PATH"] = _TMP_DB
os.environ["CYMAG_SECRET_KEY"] = "test-secret-isolation"
os.environ["CYMAG_ENV"] = "test"

import pytest

from app import create_app, db


@pytest.fixture(scope="module")
def app_ctx():
    # Força um banco próprio independentemente da ordem de import entre módulos de
    # teste (config.DB_PATH é capturado no import; sobrescrevemos no objeto config).
    db.config.DB_PATH = _TMP_DB
    app = create_app()
    app.config.update(TESTING=True)
    return app


def _mk_tenant(name, owner_email):
    """Cria conta + um owner, devolve (account_id, owner_id)."""
    acc_id = db.create_account(name, plan="profissional")
    owner_id = db.create_user(owner_email, f"Dono {name}", "cybersecurity",
                              role="owner", account_id=acc_id)
    return acc_id, owner_id


def _mk_scan_with_finding(account_id, user_id):
    """Cria um engagement autorizado + scan concluído com 1 finding para o tenant."""
    eid = db.create_engagement("Eng", "", ["192.0.2.0/24"], created_by=user_id,
                               account_id=account_id)
    db.authorize_engagement(eid, authorized_by=user_id)
    scan_id = db.create_scan("192.0.2.10", created_by=user_id, engagement_id=eid,
                             account_id=account_id)
    db.finish_scan(scan_id, [{"host": "192.0.2.10", "port": 80, "title": "x",
                              "sev": "low", "cvss": 2.0}], risk_score=10)
    return eid, scan_id


@pytest.fixture(scope="module")
def tenants(app_ctx):
    a_acc, a_owner = _mk_tenant("Tenant A", "ownerA@a.com")
    b_acc, b_owner = _mk_tenant("Tenant B", "ownerB@b.com")
    a = dict(zip(("acc", "owner", "eng", "scan"), (a_acc, a_owner, *_mk_scan_with_finding(a_acc, a_owner))))
    b = dict(zip(("acc", "owner", "eng", "scan"), (b_acc, b_owner, *_mk_scan_with_finding(b_acc, b_owner))))
    return app_ctx, a, b


def _login(client, email, password="cybersecurity"):
    return client.post("/api/login", json={"email": email, "password": password})


# ─── Camada db: filtros por tenant ────────────────────────────────────────────

def test_db_get_engagement_cross_tenant_is_none(tenants):
    _, a, b = tenants
    assert db.get_engagement(b["eng"], account_id=a["acc"]) is None
    assert db.get_engagement(b["eng"], account_id=b["acc"]) is not None


def test_db_get_scan_cross_tenant_is_none(tenants):
    _, a, b = tenants
    assert db.get_scan(b["scan"], account_id=a["acc"]) is None
    assert db.get_scan(b["scan"], account_id=b["acc"]) is not None


def test_db_findings_cross_tenant_is_none(tenants):
    _, a, b = tenants
    assert db.get_scan_findings(b["scan"], account_id=a["acc"]) is None
    assert db.get_scan_findings(b["scan"], account_id=b["acc"]) == [
        {"host": "192.0.2.10", "port": 80, "title": "x", "sev": "low", "cvss": 2.0}
    ]


def test_db_list_scoped_to_tenant(tenants):
    _, a, b = tenants
    a_scan_ids = {s["id"] for s in db.list_scans(account_id=a["acc"])}
    assert a["scan"] in a_scan_ids and b["scan"] not in a_scan_ids
    a_eng_ids = {e["id"] for e in db.list_engagements(a["acc"])}
    assert a["eng"] in a_eng_ids and b["eng"] not in a_eng_ids


def test_db_no_account_sees_nothing(tenants):
    assert db.list_scans(account_id=None) == []
    assert db.list_engagements(None) == []


# ─── Camada HTTP: IDOR/BOLA ───────────────────────────────────────────────────

def test_http_findings_idor_blocked(tenants):
    app, a, b = tenants
    with app.test_client() as c:
        _login(c, "ownerA@a.com")
        r = c.get(f"/api/scans/{b['scan']}/findings")
        assert r.status_code == 404
        r_own = c.get(f"/api/scans/{a['scan']}/findings")
        assert r_own.status_code == 200


def test_http_engagement_detail_idor_blocked(tenants):
    app, a, b = tenants
    with app.test_client() as c:
        _login(c, "ownerA@a.com")
        assert c.get(f"/api/engagements/{b['eng']}").status_code == 404
        assert c.get(f"/api/engagements/{a['eng']}").status_code == 200


def test_http_engagement_list_scoped(tenants):
    app, a, b = tenants
    with app.test_client() as c:
        _login(c, "ownerA@a.com")
        ids = {e["id"] for e in c.get("/api/engagements").get_json()["engagements"]}
        assert a["eng"] in ids and b["eng"] not in ids


def test_http_cannot_authorize_other_tenant_engagement(tenants):
    app, a, b = tenants
    with app.test_client() as c:
        _login(c, "ownerA@a.com")
        # B começa autorizado no fixture; reautorizar via A deve dar 404 (não revela).
        assert c.post(f"/api/engagements/{b['eng']}/authorize").status_code == 404


def test_http_scans_list_scoped(tenants):
    app, a, b = tenants
    with app.test_client() as c:
        _login(c, "ownerB@b.com")
        ids = {s["id"] for s in c.get("/api/scans").get_json()["scans"]}
        assert b["scan"] in ids and a["scan"] not in ids


def test_http_unauthenticated_denied(tenants):
    app, a, _ = tenants
    with app.test_client() as c:
        assert c.get(f"/api/scans/{a['scan']}/findings").status_code == 401
