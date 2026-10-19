"""
G0-S13 — AEGIS recebe finding_id autenticado com isolamento de tenant (AI-001).

Verifica que:
  - finding_id de outro tenant → 404 (não vaza dados cross-tenant)
  - finding_id inválido (não existe) → 404
  - finding_id do próprio tenant → 200 (AEGIS offline devolve fallback)
  - sem finding_id → 200 via caminho legado (compatibilidade)

    pytest tests/test_remediation_isolation.py
"""

import os
import tempfile

_TMP_DB = os.path.join(tempfile.mkdtemp(prefix="cymag_rem_"), "rem.db")
os.environ["CYMAG_DB_PATH"] = _TMP_DB
os.environ["CYMAG_SECRET_KEY"] = "test-secret-remediation"
os.environ["CYMAG_ENV"] = "test"

import pytest

from app import create_app, db

XRW = {"X-Requested-With": "test"}


@pytest.fixture(scope="module")
def app_ctx():
    db.config.DB_PATH = _TMP_DB
    app = create_app()
    app.config.update(TESTING=True)
    return app


def _mk_tenant(name, email):
    acc = db.create_account(name, plan="profissional")
    uid = db.create_user(email, f"Dono {name}", "cybersecurity",
                         role="operator", account_id=acc)
    return acc, uid


def _mk_scan_with_finding(account_id, user_id):
    eid = db.create_engagement("Eng", "", ["192.0.2.0/24"], created_by=user_id,
                               account_id=account_id)
    db.authorize_engagement(eid, authorized_by=user_id)
    scan_id = db.create_scan("192.0.2.10", created_by=user_id,
                             engagement_id=eid, account_id=account_id)
    db.finish_scan(scan_id, [{"host": "192.0.2.10", "port": 443, "title": "TLS Expired",
                              "sev": "medium", "cvss": 5.3}], risk_score=40)
    return scan_id


@pytest.fixture(scope="module")
def tenants(app_ctx):
    a_acc, a_uid = _mk_tenant("Alpha", "opA@alpha.com")
    b_acc, b_uid = _mk_tenant("Beta", "opB@beta.com")
    a_scan = _mk_scan_with_finding(a_acc, a_uid)
    b_scan = _mk_scan_with_finding(b_acc, b_uid)
    a_fid = db.get_scan_findings_with_ids(a_scan)[0]["finding_id"]
    b_fid = db.get_scan_findings_with_ids(b_scan)[0]["finding_id"]
    return app_ctx, {
        "acc": a_acc, "uid": a_uid, "scan": a_scan, "fid": a_fid, "email": "opA@alpha.com",
    }, {
        "acc": b_acc, "uid": b_uid, "scan": b_scan, "fid": b_fid, "email": "opB@beta.com",
    }


def _login(client, email, password="cybersecurity"):
    return client.post("/api/login", json={"email": email, "password": password})


# ─── G0-S13: isolamento finding_id em /api/remediation ──────────────────────

def test_remediation_cross_tenant_finding_id_blocked(tenants):
    """Tenant A não pode usar finding_id de B na rota de remediação."""
    app, a, b = tenants
    with app.test_client() as c:
        _login(c, a["email"])
        r = c.post("/api/remediation",
                   json={"finding_id": b["fid"]},
                   headers=XRW)
        assert r.status_code == 404, f"Esperado 404, recebido {r.status_code}: {r.get_json()}"


def test_remediation_invalid_finding_id_returns_404(tenants):
    """finding_id que não existe → 404."""
    app, a, _ = tenants
    with app.test_client() as c:
        _login(c, a["email"])
        r = c.post("/api/remediation",
                   json={"finding_id": 999999},
                   headers=XRW)
        assert r.status_code == 404


def test_remediation_own_finding_id_returns_ok(tenants):
    """Tenant A usa o próprio finding_id → 200 (AEGIS offline retorna fallback)."""
    app, a, _ = tenants
    with app.test_client() as c:
        _login(c, a["email"])
        r = c.post("/api/remediation",
                   json={"finding_id": a["fid"], "persona": "secops"},
                   headers=XRW)
        assert r.status_code == 200
        data = r.get_json()
        # AEGIS offline: sempre retorna steps ou rationale
        assert "steps" in data or "rationale" in data or "risk" in data, \
            f"Resposta offline inesperada: {data}"


def test_remediation_own_finding_id_exec_persona(tenants):
    """Tenant B usa finding_id próprio com persona exec → 200."""
    app, _, b = tenants
    with app.test_client() as c:
        _login(c, b["email"])
        r = c.post("/api/remediation",
                   json={"finding_id": b["fid"], "persona": "exec"},
                   headers=XRW)
        assert r.status_code == 200


def test_remediation_legacy_path_still_works(tenants):
    """Caminho legado (vuln dict, sem finding_id) continua funcionando."""
    app, a, _ = tenants
    with app.test_client() as c:
        _login(c, a["email"])
        r = c.post("/api/remediation",
                   json={"vuln": {"title": "SSH Old", "host": "192.0.2.1",
                                  "port": 22, "cvss": 7.2}},
                   headers=XRW)
        assert r.status_code == 200


def test_remediation_unauthenticated_blocked(tenants):
    """Sem login → 401."""
    app, _, _ = tenants
    with app.test_client() as c:
        r = c.post("/api/remediation",
                   json={"finding_id": 1},
                   headers=XRW)
        assert r.status_code == 401
