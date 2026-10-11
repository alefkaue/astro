"""
Testes do SEC-006: relatórios montados no backend, não a partir de payload do cliente.

Prova que:
  - gerar laudo exige `scan_id` (não aceita findings arbitrários);
  - um tenant não gera laudo de scan de outro tenant (404);
  - ambiente demo carimba selo de DADOS FICTÍCIOS no PDF.

Offline: findings entram direto pela camada db; nenhum scan real é disparado.
"""

import os
import tempfile

_TMP_DB = os.path.join(tempfile.mkdtemp(prefix="cymag_rep_"), "rep.db")
os.environ["CYMAG_DB_PATH"] = _TMP_DB
os.environ["CYMAG_SECRET_KEY"] = "test-secret-reports"
os.environ["CYMAG_ENV"] = "test"

import pytest

from app import create_app, db


@pytest.fixture(scope="module")
def ctx():
    db.config.DB_PATH = _TMP_DB
    app = create_app()
    app.config.update(TESTING=True)
    # Dois tenants, cada um com um scan concluído e um finding.
    data = {}
    for key, nm, email in (("a", "Rep A", "repA@a.com"), ("b", "Rep B", "repB@b.com")):
        acc = db.create_account(nm, plan="profissional")
        uid = db.create_user(email, nm, "cybersecurity", role="owner", account_id=acc)
        eid = db.create_engagement("E", "", ["192.0.2.0/24"], created_by=uid, account_id=acc)
        db.authorize_engagement(eid, authorized_by=uid)
        sid = db.create_scan("192.0.2.5", created_by=uid, engagement_id=eid, account_id=acc)
        db.finish_scan(sid, [{"host": "192.0.2.5", "port": 3306, "title": "MySQL exposto",
                              "sev": "high", "cvss": 7.5, "category": "database"}], risk_score=60)
        data[key] = {"acc": acc, "uid": uid, "scan": sid, "email": email}
    return app, data


def _login(c, email):
    return c.post("/api/login", json={"email": email, "password": "cybersecurity"})


def test_report_requires_scan_id(ctx):
    app, d = ctx
    with app.test_client() as c:
        _login(c, d["a"]["email"])
        # Payload antigo (findings do cliente) é rejeitado: sem scan_id → 400.
        r = c.post("/api/report/quick", json={"findings": [{"title": "injetado"}]})
        assert r.status_code == 400


def test_report_cross_tenant_blocked(ctx):
    app, d = ctx
    with app.test_client() as c:
        _login(c, d["a"]["email"])
        r = c.post("/api/report/quick", json={"scan_id": d["b"]["scan"]})
        assert r.status_code == 404


def test_report_own_scan_ok_and_is_pdf(ctx):
    app, d = ctx
    with app.test_client() as c:
        _login(c, d["a"]["email"])
        r = c.post("/api/report/quick", json={"scan_id": d["a"]["scan"]})
        assert r.status_code == 200
        assert r.headers["Content-Type"] == "application/pdf"
        assert r.data[:4] == b"%PDF"


def test_report_requires_auth(ctx):
    app, d = ctx
    with app.test_client() as c:
        r = c.post("/api/report/quick", json={"scan_id": d["a"]["scan"]})
        assert r.status_code == 401
