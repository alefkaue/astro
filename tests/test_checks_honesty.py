"""Synthetic evidence tests; all network and subprocess access is blocked."""

from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from core.checks import databases, iot_ot, remote, smb, web
from core.checks.base import ScanContext, make_finding


@pytest.fixture(autouse=True)
def block_external_access(monkeypatch):
    def blocked(*args, **kwargs):
        raise AssertionError("External access is forbidden in synthetic tests")

    monkeypatch.setattr("socket.socket", blocked)
    monkeypatch.setattr("requests.sessions.Session.request", blocked)
    monkeypatch.setattr("subprocess.run", blocked)
    monkeypatch.setattr(ScanContext, "read_banner", lambda self, **kw: self.banner)


def context(port, banner="", result=None, used="synthetic"):
    ctx = ScanContext("synthetic.invalid", port, banner)
    ctx.chain = SimpleNamespace(run=Mock(return_value=(result, used)))
    return ctx


def assert_weak(findings):
    assert findings
    for finding in findings:
        assert finding["verification_status"] in {"observation", "suspected"}
        assert finding["confidence"] in {"low", "medium"}
        assert {"title", "desc", "sev", "cvss", "cve", "evidence", "banner"} <= finding.keys()


def test_sql_text_is_not_confirmed_sqli():
    response = SimpleNamespace(text="<html>MySQL documentation: syntax error</html>")
    ctx = context(80, result=response)
    findings = web.HTTPCheck()._sqli(ctx, "http://synthetic.invalid", "")
    assert_weak(findings)
    assert "Confirmado" not in findings[0]["title"]


def test_generic_http_200_is_not_confirmed_sensitive_file(monkeypatch):
    response = SimpleNamespace(status_code=200, text="<html>Generic application home page</html>")
    monkeypatch.setattr(web.requests, "get", Mock(return_value=response))
    findings = web.HTTPCheck()._sensitive_files("http://synthetic.invalid", "")
    assert len(findings) == 17
    assert_weak(findings)


def test_mongodb_handshake_is_not_unauthenticated_data_access(monkeypatch):
    sock = Mock()
    sock.recv.return_value = b"synthetic handshake response" * 2
    monkeypatch.setattr(databases.socket, "socket", Mock(return_value=sock))
    assert_weak(databases.MongoDBCheck().run(context(27017)))


def test_mysql_version_does_not_establish_specific_cve(monkeypatch):
    import sys

    monkeypatch.setitem(sys.modules, "pymysql", SimpleNamespace(connect=Mock(side_effect=RuntimeError("Denied"))))
    findings = databases.MySQLCheck().run(context(3306, banner="5.5.62"))
    assert_weak(findings)
    assert findings[0]["cve"] == ""


def test_redis_pong_does_not_establish_lua_cve():
    findings = databases.RedisCheck().run(context(6379, result=("6.0.0", "redis_version:6.0.0")))
    assert_weak(findings)
    assert findings[0]["cve"] == ""


def test_vnc_banner_does_not_establish_no_password():
    assert_weak(remote.VNCCheck().run(context(5900, banner="RFB 003.008")))


def test_login_keywords_do_not_establish_authenticated_session(monkeypatch):
    monkeypatch.setattr(web.requests, "get", Mock(return_value=SimpleNamespace(status_code=200, text="login password")))
    monkeypatch.setattr(web.requests, "post", Mock(return_value=SimpleNamespace(status_code=200, text="admin login failed")))
    assert_weak(web.HTTPCheck()._default_creds("http://synthetic.invalid", ""))


def test_passwd_patterns_do_not_establish_arbitrary_file_read(monkeypatch):
    monkeypatch.setattr(web.requests, "get", Mock(return_value=SimpleNamespace(text="root:x:0:0 /usr/sbin/nologin")))
    assert_weak(web.HTTPCheck()._traversal("http://synthetic.invalid", ""))


def test_elasticsearch_metadata_does_not_establish_cve_or_all_data(monkeypatch):
    response = SimpleNamespace(status_code=200, text='{"cluster_name":"test"}', json=lambda: {"cluster_name": "test"})
    monkeypatch.setattr(databases.requests, "get", Mock(return_value=SimpleNamespace(text="Unauthorized", status_code=401)))
    findings = databases.ElasticsearchCheck().run(context(9200, result=response))
    assert_weak(findings)
    assert findings[0]["cve"] == ""


def test_nodered_generic_http_200_is_only_observation():
    response = SimpleNamespace(status_code=200, text="Generic proxy page")
    assert_weak(iot_ot.NodeREDCheck().run(context(1880, result=response, used="settings JSON")))


@pytest.mark.parametrize("check,port,banner", [(remote.SSHCheck, 22, "SSH-2.0-OpenSSH_5.0"), (remote.TelnetCheck, 23, "")])
def test_remote_banner_or_port_is_weak(check, port, banner):
    assert_weak(check().run(context(port, banner)))


@pytest.mark.parametrize("check,port,label", [(remote.RDPCheck, 3389, "rdp-vuln-ms12-020"), (smb.SMBCheck, 445, "smb-vuln-ms17-010")])
@pytest.mark.parametrize("state", ["NOT VULNERABLE", "VULNERABLE"])
def test_script_state_is_not_substring_confirmation(monkeypatch, check, port, label, state):
    output = f"| {label}:\n|   State: {state}\n"
    monkeypatch.setattr(remote.subprocess, "run", Mock(return_value=SimpleNamespace(stdout=output)))
    findings = check().run(context(port))
    if state == "NOT VULNERABLE":
        assert findings == []
    else:
        assert_weak(findings)


def test_finding_preserves_existing_keys_and_extra():
    finding = make_finding("title", "desc", "low", 1, "", extra={"custom": True})
    assert_weak([finding])
    assert finding["custom"] is True


def test_actual_mysql_login_confirms_only_login(monkeypatch):
    import sys

    monkeypatch.setitem(sys.modules, "pymysql", SimpleNamespace(connect=Mock(return_value=Mock())))
    finding = databases.MySQLCheck().run(context(3306))[0]
    assert finding["verification_status"] == "confirmed"
    assert finding["confidence"] == "high"
    assert "Acesso total" not in finding["desc"]
