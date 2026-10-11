"""Managed-review APIs must not act as an unscoped staff backdoor."""
from uuid import uuid4
from flask import Flask
from app import db
from app.scans.routes import scans_bp
from tests.test_dashboard import tenants


def test_review_queue_and_signing_are_tenant_scoped(tenants):
    a, b, uid, own = tenants
    staff = db.create_user(uuid4().hex+"@example.com", "Staff A", "test-password", role="cymag", account_id=a)
    orphan = db.create_user(uuid4().hex+"@example.com", "Admin", "test-password", role="admin")
    foreign = db.create_scan("203.0.113.42", uid, account_id=b)
    db.finish_scan(foreign, [], 0)
    db.set_review_status(own, "pending")
    db.set_review_status(foreign, "pending")
    running = db.create_scan("192.0.2.55", uid, account_id=a)
    db.set_review_status(running, "pending")
    app = Flask(__name__)
    app.secret_key = "review-test"
    app.register_blueprint(scans_bp)
    with app.test_client() as client:
        assert client.get("/api/reviews").status_code == 401
        with client.session_transaction() as session:
            session["uid"] = orphan
        assert client.get("/api/reviews").status_code == 403
        assert client.post(f"/api/scans/{foreign}/review", json={"status":"reviewed"}).status_code == 403
        with client.session_transaction() as session:
            session["uid"] = staff
        assert [s["id"] for s in client.get("/api/reviews").json["queue"]] == [own]
        assert client.post(f"/api/scans/{foreign}/review", json={"status":"reviewed"}).status_code == 404
        assert client.post(f"/api/scans/{running}/review", json={"status":"reviewed"}).status_code == 409
        assert client.post(f"/api/scans/{own}/review", json={"status":"signed"}).status_code == 409
        assert client.post(f"/api/scans/{own}/review", json={"status":"reviewed"}).status_code == 200
        assert client.post(f"/api/scans/{own}/review", json={"status":"reviewed"}).status_code == 409
        assert client.post(f"/api/scans/{own}/review", json={"status":"signed"}).status_code == 200
        assert client.post(f"/api/scans/{own}/review", json={"status":"reviewed"}).status_code == 409
        assert db.get_scan(foreign, account_id=b)["review_status"] == "pending"
        with client.session_transaction() as session:
            session["uid"] = uid
        assert client.get("/api/reviews").status_code == 403
    assert db.list_review_queue() == []
    assert db.review_scan_scoped(foreign, None, "reviewed", staff) is False
    assert db.review_scan_scoped(foreign, a, "reviewed", staff) is False
