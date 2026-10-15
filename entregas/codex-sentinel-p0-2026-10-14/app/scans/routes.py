"""Rotas de scan, remediação, cadeia de exploração, auto-descoberta e histórico."""

import json
import logging

from flask import Blueprint, jsonify, request, session

from app import db
from app.ai.aegis import (AEGIS_EXEC, AEGIS_SECOPS, aegis, calc_score,
                          sanitize_finding, sanitize_untrusted)
from app.auth.decorators import (current_plan, enforce_scan_quota,
                                 login_required, requires_feature, role_required, permission_required)
from app.scans.network import detect_local_subnets
from app.scope import ScopeError, resolve_authorized_target
from core.exploit_engine import ExploitEngine
from core.plans import FEATURE_AI, FEATURE_MANAGED
from core.scanner import CYMAGScanner

logger = logging.getLogger("cymag.scans")

scans_bp = Blueprint("scans", __name__)


@scans_bp.route("/api/areas")
@login_required
def api_areas():
    """Áreas do pentester cobertas e serviços/portas de cada uma."""
    return jsonify({"areas": ExploitEngine.areas()})


@scans_bp.route("/api/scan", methods=["POST"])
@login_required
@enforce_scan_quota
def api_scan():
    """Scan completo: descoberta → port scan → exploit/enum → risco executivo.

    Toda varredura — inclusive a manual — exige um Engagement autorizado e um
    alvo dentro do escopo. A autorização é a mesma regra do modo autônomo.
    """
    body = request.get_json(force=True) or {}
    uid = session.get("uid")

    try:
        eng, target = resolve_authorized_target(body.get("engagement_id"), body.get("target", ""))
    except ScopeError as e:
        db.audit(uid, "scan_denied", f"reason={e.message}", request.remote_addr or "")
        return jsonify({"error": e.message}), e.status

    scope = eng.get("scope") or []
    logger.info("[/api/scan] Iniciando para alvo: %s (user %s, eng %s)", target, uid, eng["id"])

    scan_id = db.create_scan(target, created_by=uid, engagement_id=eng["id"])
    db.audit(uid, "scan_start", f"scan={scan_id} eng={eng['id']} target={target}",
             request.remote_addr or "")

    try:
        raw = CYMAGScanner(target, scope=scope).run()
    except Exception as e:
        db.finish_scan(scan_id, [], 0, status="error")
        logger.exception("[/api/scan] Falha no scan %s", scan_id)
        return jsonify({"error": f"Falha no scan: {e}", "scan_id": scan_id}), 500

    plan = current_plan()
    ai_enabled = plan.has(FEATURE_AI)

    exec_risks = []
    for v in raw:
        # A análise de IA só roda em planos com a feature; os demais usam o
        # fallback determinístico offline (mesmo formato de saída).
        if ai_enabled:
            sv = sanitize_finding(v)
            quick_prompt = (
                f"Vuln: {sv.get('title')} em {sv.get('host')}:{v.get('port')} | "
                f"CVSS: {v.get('cvss',0)} | {sanitize_untrusted(v.get('desc',''), 120)}\n"
                "JSON: {\"risk\":\"...\",\"category\":\"...\",\"impact\":\"R$ X\",\"probability\":\"Alta|Média|Baixa\"}"
            )
            risk = aegis.call(AEGIS_EXEC, quick_prompt, max_tokens=280) or aegis.offline_exec_risk(v)
        else:
            risk = aegis.offline_exec_risk(v)
        exec_risks.append(risk)

    score = calc_score(raw)
    db.finish_scan(scan_id, raw, score, status="done")

    # Plano Gerenciado+: resultado entra na esteira de validação humana.
    if plan.has(FEATURE_MANAGED) and raw:
        db.set_review_status(scan_id, "pending")

    logger.info("[/api/scan] Concluído: scan=%d | %d vulns | score %d | ia=%s",
                scan_id, len(raw), score, ai_enabled)
    return jsonify({
        "scan_id": scan_id,
        "target": target,
        "engagement_id": eng["id"],
        "cyber_vulns": raw,
        "exec_risks": exec_risks,
        "risk_score": score,
        "ai_enabled": ai_enabled,
        "review_status": "pending" if (plan.has(FEATURE_MANAGED) and raw) else "none",
    })


@scans_bp.route('/api/remediation', methods=['POST'])
@login_required
def api_remediation():
    """Read-only deterministic advice, selected from authorized persisted data."""
    body = request.get_json(force=True) or {}
    finding_id = body.get('finding_id')
    if not isinstance(finding_id, int) or isinstance(finding_id, bool):
        return jsonify({'error': 'finding_id inteiro obrigat?rio'}), 400
    with db.get_conn() as conn:
        row = conn.execute('SELECT raw FROM findings WHERE id=? AND organization_id=?',
                           (finding_id, db._tenant())).fetchone()
    if not row:
        return jsonify({'error': 'Achado n?o encontrado'}), 404
    finding = sanitize_finding(json.loads(row['raw']))
    result = aegis.offline_exec(finding) if body.get('persona') == 'exec' else aegis.offline_secops(finding)
    return jsonify({**result, 'finding_id': finding_id, 'source': 'deterministic',
                    'limitations': 'Sugest?o para revis?o humana; nenhum comando executado.'})


@scans_bp.route("/api/exploit_chain", methods=["POST"])
@login_required
@requires_feature(FEATURE_AI)
def api_exploit_chain():
    """AEGIS planeja o caminho de ataque completo com base em TODOS os achados."""
    body = request.get_json(force=True) or {}
    findings = body.get("findings", [])

    if not findings:
        return jsonify({"error": "Nenhum finding fornecido"}), 400

    logger.info("[/api/exploit_chain] Planejando cadeia com %d vulnerabilidades", len(findings))

    safe_findings = [sanitize_finding(f) for f in findings]
    prompt = (
        f"Achados do scan CYMAG ({len(findings)} vulnerabilidades):\n"
        f"{json.dumps(safe_findings, indent=2, ensure_ascii=False)}\n\n"
        "Planeje o caminho de ataque mais eficiente. Schema obrigatório:\n"
        '{"initial_vector":{"finding_title":"...","host":"...","port":0,"why":"..."},'
        '"attack_steps":[{"step":1,"action":"...","command":"...","expected_result":"..."}],'
        '"blast_radius":"...","critical_path":["host:porta → host:porta"],'
        '"estimated_time_to_root":"X minutos","mitre_chain":["TA0001","TA0003"]}'
    )

    result = aegis.call(AEGIS_SECOPS, prompt, max_tokens=1024)
    if result:
        return jsonify(result)

    # Fallback offline mínimo
    top = max(findings, key=lambda f: f.get("cvss", 0))
    return jsonify({
        "initial_vector": {
            "finding_title": top.get("title"),
            "host": top.get("host"),
            "port": top.get("port"),
            "why": "Maior CVSS score no conjunto de achados.",
        },
        "attack_steps": [
            {"step": 1, "action": "Explorar vetor inicial", "command": f"# Explorar {top.get('title')}", "expected_result": "Acesso inicial"},
            {"step": 2, "action": "Escalação de privilégios", "command": "# Executar enumeração pós-acesso", "expected_result": "Root/SYSTEM"},
        ],
        "blast_radius": "Comprometimento do ativo e potencial movimento lateral",
        "critical_path": [f"{top.get('host')}:{top.get('port')}"],
        "estimated_time_to_root": "15–30 minutos",
        "mitre_chain": ["TA0001", "TA0004", "TA0008"],
    })


@scans_bp.route("/api/auto_discover")
@login_required
def api_auto_discover():
    """Detecta automaticamente as sub-redes locais (cross-platform)."""
    subnets = detect_local_subnets()
    logger.info("[auto_discover] Subnets detectadas: %s", subnets)
    return jsonify({"subnets": subnets})


@scans_bp.route("/api/scans")
@login_required
def api_scans():
    """Lista os scans do usuário atual (histórico persistente)."""
    return jsonify({"scans": db.list_scans(limit=50, created_by=session.get("uid"))})


@scans_bp.route("/api/scans/<int:scan_id>/findings")
@login_required
def api_scan_findings(scan_id: int):
    """Retorna os achados de um scan específico."""
    if not db.get_scan(scan_id):
        return jsonify({'error': 'Scan não encontrado'}), 404
    return jsonify({"scan_id": scan_id, "findings": db.get_scan_findings_with_ids(scan_id)})


# ─── VALIDAÇÃO HUMANA (plano Gerenciado+) ───────────────────────────────────────

@scans_bp.route("/api/reviews")
@permission_required('finding:write')
def api_review_queue():
    """Fila de scans aguardando validação humana (analista/admin)."""
    return jsonify({"queue": db.list_review_queue()})


@scans_bp.route("/api/scans/<int:scan_id>/review", methods=["POST"])
@permission_required('finding:write')
def api_submit_review(scan_id: int):
    """Analista valida um scan: marca como 'reviewed' ou assina o laudo ('signed')."""
    body = request.get_json(force=True) or {}
    status = (body.get("status") or "").strip().lower()
    if status not in ("reviewed", "signed"):
        return jsonify({"error": "status deve ser 'reviewed' ou 'signed'."}), 400

    scan = db.get_scan(scan_id)
    if not scan:
        return jsonify({"error": "Scan não encontrado."}), 404

    uid = session.get("uid")
    notes = (body.get("notes") or "").strip()
    db.set_review_status(scan_id, status, reviewed_by=uid, notes=notes)
    db.audit(uid, "scan_review", f"scan={scan_id} status={status}", request.remote_addr or "")
    return jsonify({"scan_id": scan_id, "review_status": status, "reviewed_by": uid})
