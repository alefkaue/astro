"""Tenant-scoped overview derived exclusively from persisted assessments."""
import json
from datetime import datetime, timezone
from flask import Blueprint, jsonify
from app import db
from app.auth.decorators import current_account_id, login_required

dashboard_bp = Blueprint("dashboard", __name__)


def build_summary(account_id):
    counts = {"assessments": 0, "running": 0, "completed": 0, "failed": 0,
              "observed_hosts": 0, "confirmed": 0, "pending_validation": 0,
              "observations": 0, "unclassified": 0}
    severity = dict.fromkeys(("crit", "high", "med", "low", "info"), 0)
    recent = []
    if account_id is not None:
        with db.get_conn() as conn:
            rows = conn.execute("SELECT status, COUNT(*) AS n FROM scans WHERE account_id=? GROUP BY status", (account_id,)).fetchall()
            for row in rows:
                counts["assessments"] += row["n"]
                key = {"running": "running", "done": "completed", "error": "failed"}.get(row["status"])
                if key:
                    counts[key] += row["n"]
            recent = [dict(r) for r in conn.execute("SELECT id, target, status, findings_count, started_at, finished_at FROM scans WHERE account_id=? ORDER BY id DESC LIMIT 8", (account_id,))]
            findings = conn.execute("""SELECT f.raw FROM findings f JOIN scans s ON s.id=f.scan_id
                WHERE s.account_id=? AND s.status='done' AND s.id IN
                (SELECT MAX(id) FROM scans WHERE account_id=? AND status='done' GROUP BY target)""", (account_id, account_id)).fetchall()
            hosts = set()
            for row in findings:
                try:
                    f = json.loads(row["raw"])
                except (ValueError, TypeError):
                    counts["unclassified"] += 1
                    continue
                if not isinstance(f, dict):
                    counts["unclassified"] += 1
                    continue
                if f.get("host"):
                    hosts.add(str(f["host"]))
                severity[f.get("sev") if f.get("sev") in severity else "info"] += 1
                status = f.get("verification_status")
                key = {"confirmed": "confirmed", "suspected": "pending_validation", "observation": "observations"}.get(status, "unclassified")
                counts[key] += 1
            counts["observed_hosts"] = len(hosts)
    return {"source": "persisted_assessments", "generated_at": datetime.now(timezone.utc).isoformat(),
            "counts": counts, "severity": severity, "recent": recent,
            "coverage": "Achados da última avaliação concluída de cada alvo. Hosts contados apenas quando há achados; não representa inventário completo. Alvos sobrepostos podem repetir achados.",
            "limitations": ["Sem comprovação de correção ou evolução temporal nesta versão.", "Achados legados sem status não são considerados confirmados."]}


@dashboard_bp.get("/api/dashboard")
@login_required
def dashboard():
    return jsonify(build_summary(current_account_id()))
