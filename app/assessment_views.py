"""Read-only persisted assessment detail, scoped to the authenticated tenant."""
from flask import Blueprint, jsonify
from app import db
from app.auth.decorators import current_account_id, login_required

assessment_views_bp = Blueprint("assessment_views", __name__)


@assessment_views_bp.get("/api/assessments/<int:scan_id>")
@login_required
def assessment_detail(scan_id):
    account_id = current_account_id()
    scan = db.get_scan(scan_id, account_id=account_id)
    if scan is None:
        return jsonify({"error": "Avaliação não encontrada."}), 404
    findings = db.get_scan_findings(scan_id, account_id=account_id)
    return jsonify({
        "assessment": {key: scan.get(key) for key in (
            "id", "target", "engagement_id", "status", "findings_count",
            "risk_score", "started_at", "finished_at", "review_status")},
        "findings": findings or [],
        "source": "persisted_assessment",
        "coverage": {"status": "not_measured", "limitations": [
            "O histórico não registra modo e cobertura completos por check.",
            "Eventos autônomos são mantidos em memória e podem ser perdidos após reinício.",
            "Ausência de achados não comprova segurança ou correção."]},
    })
