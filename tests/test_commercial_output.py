from core import business
from core.plans import public_catalog
from app.ai.aegis import Aegis
from app.reports.pdf import _build_exec_table
from fpdf import FPDF


def test_observation_has_no_financial_or_exploitation_claim():
    finding = {"title": "SQL service", "sev": "high", "verification_status": "observation"}
    item = business.business_item(finding)
    assert item["loss_max"] == item["fix_cost_max"] == 0
    assert item["loss_label"] == "Não estimado"
    assert business.summarize([finding])["open_loss_max"] == 0
    assert "R$" not in str(Aegis.offline_exec(finding))
    assert "R$" not in str(Aegis.offline_exec_risk(finding))


def test_informational_pdf_has_no_invented_money_or_probability():
    pdf = FPDF()
    pdf.set_compression(False)
    pdf.add_page()
    _build_exec_table(pdf, [Aegis.offline_exec_risk({"sev": "info"})])
    output = bytes(pdf.output())
    assert b"R$" not in output
    assert b"Probabilidade" not in output


def test_catalog_does_not_claim_compliance_certification():
    for plan in public_catalog():
        assert "LGPD/ISO/PCI" not in plan["tagline"]
        assert "assina" not in plan["tagline"]
