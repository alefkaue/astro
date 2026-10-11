"""
Rotas de geração de relatório PDF.

/api/report/quick     — PDF rápido (sem IA)
/api/report/detailed  — PDF com narrativa gerada pelo AEGIS
"""

import json
import logging
from datetime import datetime

from flask import Blueprint, jsonify, make_response, request

from app import db
from app.ai.aegis import AEGIS_SECOPS, aegis, sanitize_untrusted
from app.auth.decorators import current_account_id, current_user, login_required
from app.config import config

logger = logging.getLogger("cymag.reports")

reports_bp = Blueprint("reports", __name__)

# Selo aplicado quando o ambiente é de demonstração (dados sintéticos).
_DEMO_WATERMARK = "DADOS FICTICIOS - DEMONSTRACAO (nao representa avaliacao real)"


def _load_authorized_scan(body):
    """Resolve o scan pedido garantindo posse pelo tenant e monta os dados do laudo.

    SEC-006: o relatório é SEMPRE construído a partir dos dados persistidos do scan
    (do tenant), nunca de findings arbitrários enviados pelo cliente. Devolve
    `(erro_json, status)` em caso de falha, ou `(dados, None)` em caso de sucesso.
    """
    scan_id = body.get("scan_id")
    if not isinstance(scan_id, int):
        return {"error": "scan_id (inteiro) é obrigatório para gerar o laudo."}, 400

    account_id = current_account_id()
    scan = db.get_scan(scan_id, account_id=account_id)
    if scan is None:
        return {"error": "Scan não encontrado."}, 404

    findings = db.get_scan_findings(scan_id, account_id=account_id) or []
    # Riscos executivos são derivados no backend (determinístico), não vêm do cliente.
    exec_risks = [aegis.offline_exec_risk(f) for f in findings]

    user = current_user()
    provenance = (
        f"scan_id={scan_id} | gerado_por={user['email'] if user else '—'} | "
        f"findings={len(findings)} | risk_score={scan.get('risk_score', 0)}"
    )
    data = {
        "scan": scan,
        "target": scan.get("target", "N/A"),
        "findings": findings,
        "exec_risks": exec_risks,
        "score": int(scan.get("risk_score") or 0),
        "watermark": _DEMO_WATERMARK if config.ENV == "demo" else "",
        "provenance": provenance,
    }
    return data, None


def _pdf_response(pdf_bytes: bytes, prefix: str):
    filename = f"cymag_{prefix}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    resp = make_response(pdf_bytes)
    resp.headers["Content-Type"] = "application/pdf"
    resp.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    resp.headers["Content-Length"] = len(pdf_bytes)
    return resp


@reports_bp.route("/api/report/quick", methods=["POST"])
@login_required
def api_report_quick():
    """Gera PDF rápido a partir de um scan do tenant. Body: { scan_id }.

    SEC-006: o laudo é montado no backend com os findings persistidos do scan
    (verificando posse pelo tenant). Não aceita mais findings do cliente."""
    from app.reports.pdf import build_quick_pdf

    body = request.get_json(force=True) or {}
    data, status = _load_authorized_scan(body)
    if status:
        return jsonify(data), status

    logger.info("[PDF Quick] scan=%s alvo='%s' — %d vuln(s)",
                body.get("scan_id"), data["target"], len(data["findings"]))
    try:
        pdf_bytes = build_quick_pdf(
            data["target"], data["findings"], data["exec_risks"], data["score"],
            watermark=data["watermark"], provenance=data["provenance"],
        )
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logger.exception("[PDF Quick] Erro ao gerar PDF")
        return jsonify({"error": f"Erro interno: {e}"}), 500

    return _pdf_response(pdf_bytes, "report")


@reports_bp.route("/api/report/detailed", methods=["POST"])
@login_required
def api_report_detailed():
    """Gera PDF detalhado (com narrativa do AEGIS) a partir de um scan do tenant.

    Body: { scan_id, instructions?, template? }. Os dados técnicos vêm do backend;
    `instructions`/`template` são apenas apresentação e são sanitizados."""
    from app.reports.pdf import build_detailed_pdf

    body = request.get_json(force=True) or {}
    data, status = _load_authorized_scan(body)
    if status:
        return jsonify(data), status

    # Opções de apresentação são tratadas como texto não confiável do cliente.
    instructions = sanitize_untrusted(
        body.get("instructions") or "Relatório profissional de segurança.", 600)
    template_str = sanitize_untrusted(body.get("template", ""), 2000)

    logger.info("[PDF Detailed] scan=%s alvo='%s' — %d vuln(s)",
                body.get("scan_id"), data["target"], len(data["findings"]))

    narrative = _generate_narrative(data["target"], data["findings"],
                                    data["exec_risks"], data["score"],
                                    instructions, template_str)
    if not narrative:
        logger.warning("[PDF Detailed] AEGIS sem resposta, gerando sem narrativa.")

    try:
        pdf_bytes = build_detailed_pdf(
            data["target"], data["findings"], data["exec_risks"], data["score"],
            narrative, watermark=data["watermark"], provenance=data["provenance"],
        )
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logger.exception("[PDF Detailed] Erro ao gerar PDF")
        return jsonify({"error": f"Erro interno: {e}"}), 500

    return _pdf_response(pdf_bytes, "detailed")


def _generate_narrative(target, findings, exec_risks, score, instructions, template_str):
    """Chama o AEGIS para gerar a narrativa do relatório detalhado."""
    crits = [f for f in findings if f.get("sev") == "crit"]
    highs = [f for f in findings if f.get("sev") == "high"]
    hosts = list(set(f.get("host", "") for f in findings))

    findings_summary = [
        {k: v for k, v in f.items() if k in ["title", "host", "port", "sev", "cvss", "cve"]}
        for f in findings
    ]
    risks_summary = [
        {k: v for k, v in r.items() if k in ["risk", "category", "probability", "impact"]}
        for r in exec_risks
    ]
    template_section = (
        f"\nO usuario forneceu este template de estrutura para seguir:\n{template_str}\n"
        if template_str else ""
    )

    prompt = f"""Voce e o AEGIS gerando um relatorio profissional de seguranca para o CYMAG Enterprise.

CONTEXTO DO SCAN:
- Alvo: {target}
- Score de risco: {score}/100
- Total de vulnerabilidades: {len(findings)} ({len(crits)} criticas, {len(highs)} altas)
- Hosts afetados: {', '.join(hosts[:10])}

INSTRUCOES DO USUARIO:
{instructions}
{template_section}
VULNERABILIDADES ENCONTRADAS:
{json.dumps(findings_summary, ensure_ascii=False, indent=2)}

RISCOS EXECUTIVOS:
{json.dumps(risks_summary, ensure_ascii=False, indent=2)}

Gere o conteudo narrativo do relatorio em JSON EXATO com esta estrutura:
{{
  "executive_summary": "Sumario executivo em 3-4 paragrafos. Tom e audiencia conforme instrucoes do usuario.",
  "risk_overview": "Visao geral dos riscos em 2-3 paragrafos. Mencione os principais vetores e impactos.",
  "critical_findings": [
    "Analise detalhada da vulnerabilidade critica 1 — o que e, impacto, como explorar, como corrigir.",
    "Analise detalhada da vulnerabilidade critica 2 — ..."
  ],
  "recommendations": [
    "Recomendacao prioritaria 1 com prazo sugerido",
    "Recomendacao prioritaria 2 com prazo sugerido",
    "Recomendacao prioritaria 3 com prazo sugerido",
    "Recomendacao prioritaria 4 com prazo sugerido",
    "Recomendacao prioritaria 5 com prazo sugerido"
  ],
  "conclusion": "Conclusao em 2-3 paragrafos com proximos passos e mensagem de encerramento."
}}

OBRIGATORIO: Responda APENAS com o JSON. Sem markdown, sem explicacoes. Conteudo em portugues."""

    try:
        result = aegis.call(AEGIS_SECOPS, prompt, max_tokens=2000)
        if result and isinstance(result, dict):
            return result
    except Exception as e:
        logger.warning("[PDF Narrative] Erro no AEGIS: %s", e)
    return None
