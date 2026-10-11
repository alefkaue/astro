"""Detail routes must never disclose a different organization's assessment."""
from flask import Flask
from app import db
from app.assessment_views import assessment_views_bp
from tests.test_dashboard import tenants


def test_detail_is_authenticated_and_tenant_scoped(tenants):
    a, b, uid, sid = tenants
    foreign = db.create_scan("203.0.113.42", created_by=uid, account_id=b)
    app = Flask(__name__)
    app.secret_key = "assessment-test"
    app.register_blueprint(assessment_views_bp)
    with app.test_client() as client:
        assert client.get(f"/api/assessments/{sid}").status_code == 401
        with client.session_transaction() as session:
            session["uid"] = uid
        response = client.get(f"/api/assessments/{sid}?account_id={b}")
        assert response.status_code == 200
        assert response.json["assessment"]["id"] == sid
        assert len(response.json["findings"]) == 3
        assert response.json["coverage"]["status"] == "not_measured"
        assert client.get(f"/api/assessments/{foreign}").status_code == 404
        assert client.get("/api/assessments/999999").status_code == 404


def test_empty_running_assessment_and_direct_frontend_routes(tenants):
    from app import create_app
    a, _, uid, _ = tenants
    sid = db.create_scan("192.0.2.42", created_by=uid, account_id=a)
    app = create_app()
    with app.test_client() as client:
        with client.session_transaction() as session:
            session["uid"] = uid
        response = client.get(f"/api/assessments/{sid}")
        assert response.status_code == 200
        assert response.json["findings"] == []
        for route in ("/login", "/demo", "/app/assessments", "/app/assessments/new", f"/app/assessments/{sid}"):
            page = client.get(route)
            assert page.status_code == 200
            assert b"astro-workspace.js" in page.data
        assert client.get("/api/nonexistent").status_code == 404
        misplaced_asset = client.get("/app/assessments/1/static/cymag.js")
        assert misplaced_asset.status_code == 404
        assert misplaced_asset.is_json
        assert client.get("/static/astro-workspace.js").status_code == 200


def test_viewer_cannot_create_scope_and_owner_can_authorize(tenants):
    from app.engagements.routes import engagements_bp
    from uuid import uuid4
    a, _, _, _ = tenants
    viewer = db.create_user(uuid4().hex+"@example.com", "Viewer", "test-password", role="viewer", account_id=a)
    owner = db.create_user(uuid4().hex+"@example.com", "Owner", "test-password", role="owner", account_id=a)
    app = Flask(__name__)
    app.secret_key = "scope-permissions"
    app.register_blueprint(engagements_bp)
    with app.test_client() as client:
        with client.session_transaction() as session:
            session["uid"] = viewer
        assert client.post("/api/engagements", json={"name":"Test", "scope":["192.0.2.1"]}).status_code == 403
        with client.session_transaction() as session:
            session["uid"] = owner
        created = client.post("/api/engagements", json={"name":"Test", "scope":["192.0.2.1"]})
        assert created.status_code == 201
        assert client.post(f"/api/engagements/{created.json['id']}/authorize").status_code == 200


def test_scope_authorization_rejects_missing_or_foreign_tenant(tenants):
    from app.engagements.routes import engagements_bp
    from uuid import uuid4
    a, b, uid, _ = tenants
    foreign = db.create_engagement("Foreign", "", ["203.0.113.1"], created_by=uid, account_id=b)
    own = db.create_engagement("Own", "", ["192.0.2.1"], created_by=uid, account_id=a)
    orphan = db.create_user(uuid4().hex+"@example.com", "Admin", "test-password", role="admin")
    owner = db.create_user(uuid4().hex+"@example.com", "Owner", "test-password", role="owner", account_id=a)
    app = Flask(__name__)
    app.secret_key = "scope-isolation"
    app.register_blueprint(engagements_bp)
    with app.test_client() as client:
        with client.session_transaction() as session:
            session["uid"] = orphan
        assert client.post(f"/api/engagements/{foreign}/authorize").status_code == 403
        assert db.authorize_engagement(foreign, orphan) is False
        with client.session_transaction() as session:
            session["uid"] = owner
        assert client.post(f"/api/engagements/{foreign}/authorize").status_code == 404
        assert db.authorize_engagement(foreign, owner, account_id=b) is False
        assert db.authorize_engagement(foreign, owner, account_id=a) is False
        assert db.get_engagement(foreign, account_id=b)["status"] == "draft"
        with client.session_transaction() as session:
            session["uid"] = uid
        assert client.post(f"/api/engagements/{own}/authorize").status_code == 403
