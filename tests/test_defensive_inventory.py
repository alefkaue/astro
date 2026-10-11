"""Offline tests proving intrusive legacy mechanisms are not dispatched."""
from core.exploit_engine import ExploitEngine
from core.scanner import CYMAGScanner
from core.autonomous import AutonomousEngine


def test_dispatcher_does_not_invoke_legacy_checks(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Legacy check must never execute")
    monkeypatch.setattr("core.checks.run_checks", forbidden)
    findings = ExploitEngine().check("192.0.2.1", 3306, "synthetic-banner")
    assert len(findings) == 1
    assert findings[0]["verification_status"] == "observation"
    assert findings[0]["cvss"] == 0
    assert findings[0]["cve"] == ""
    assert set(ExploitEngine.areas()) == {"recon"}


def test_large_candidate_network_is_bounded(monkeypatch):
    import pytest
    monkeypatch.setattr(CYMAGScanner, "_make_nmap", staticmethod(lambda: None))
    scanner = CYMAGScanner("10.0.0.0/8", scope=["10.0.0.0/8"])
    with pytest.raises(ValueError, match="64"):
        scanner.discover_hosts()


def test_autonomous_does_not_call_attack_planner(monkeypatch):
    monkeypatch.setattr(CYMAGScanner, "_make_nmap", staticmethod(lambda: None))
    monkeypatch.setattr(CYMAGScanner, "discover_hosts", lambda self: ["192.0.2.1"])
    monkeypatch.setattr(CYMAGScanner, "scan_host_services", lambda self, host: {22:{"banner":"test"}})
    def forbidden(*args):
        raise AssertionError("Attack planning must not run")
    report = AutonomousEngine("192.0.2.1", ai_planner=forbidden, scope=["192.0.2.1"]).run()
    assert report["attack_plan"] is None
    assert report["assessment_profile"] == "defensive_inventory"
    assert report["findings"][0]["verification_status"] == "observation"


def test_pdf_does_not_turn_observations_into_confirmed_vulnerabilities():
    from fpdf import FPDF
    from app.reports.pdf import _build_vulns_table
    pdf = FPDF()
    pdf.set_compression(False)
    pdf.add_page()
    _build_vulns_table(pdf, [
        {"host":"192.0.2.1","port":22,"title":"Service observation","sev":"info","verification_status":"observation"},
        {"host":"192.0.2.2","port":80,"title":"Legacy finding","sev":"low"},
    ])
    output = bytes(pdf.output())
    assert b"OBSERVACAO" in output
    assert b"NAO CLASSIF." in output
    assert b"CONFIRMADO" not in output
