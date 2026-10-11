import pytest
from core.scope import assert_safe_target, candidate_count, hosts_in_scope
from app import scope as web_scope


@pytest.fixture(autouse=True)
def clean_policy(monkeypatch):
    monkeypatch.setenv("CYMAG_ENV", "test")
    monkeypatch.delenv("CYMAG_SCOPE_DENY", raising=False)
    monkeypatch.delenv("CYMAG_SCOPE_ALLOW", raising=False)


@pytest.mark.parametrize("target", ["127.0.0.1", "169.254.169.254", "224.0.0.1", "0.0.0.0",
                                   "255.255.255.255", "::1", "fe80::1", "10.0.0.0/8", "192.0.2.0/24"])
def test_unsafe_or_excessive_targets_rejected(target):
    with pytest.raises(ValueError):
        assert_safe_target(target)


def test_count_and_supported_private_ranges():
    assert candidate_count("10.0.0.0/31") == 2
    assert candidate_count("10.0.0.1/32") == 1
    assert candidate_count("10.0.0.0/26") == 62
    assert_safe_target("10.0.0.0/26")


def test_deny_overlap_and_invalid_policy_fail_closed(monkeypatch):
    monkeypatch.setenv("CYMAG_SCOPE_DENY", "10.0.0.15/32")
    with pytest.raises(ValueError):
        assert_safe_target("10.0.0.0/26")
    monkeypatch.setenv("CYMAG_SCOPE_DENY", "invalid")
    with pytest.raises(ValueError):
        assert_safe_target("192.0.2.1")


def test_hosted_allowlist_required_and_deny_wins(monkeypatch):
    with pytest.raises(ValueError):
        assert_safe_target("192.0.2.1", hosted=True)
    monkeypatch.setenv("CYMAG_SCOPE_ALLOW", "192.0.2.0/24")
    assert_safe_target("192.0.2.1", hosted=True)
    monkeypatch.setenv("CYMAG_SCOPE_DENY", "192.0.2.1")
    with pytest.raises(ValueError):
        assert_safe_target("192.0.2.1", hosted=True)


def test_discovered_hosts_are_checked_even_without_scope():
    assert hosts_in_scope(["192.0.2.1", "127.0.0.1", "169.254.169.254", "bad"], []) == ["192.0.2.1"]


def test_tenant_plan_limit_and_default_range(monkeypatch):
    monkeypatch.setattr(web_scope.config, "ENV", "test")
    monkeypatch.setattr(web_scope.db, "get_engagement", lambda eid, account_id: {
        "status": "authorized", "scope": ["192.0.2.0/24"]})
    monkeypatch.setattr(web_scope.db, "get_account", lambda aid: {"plan": "comunidade"})
    with pytest.raises(web_scope.ScopeError) as error:
        web_scope.resolve_authorized_target(1, 1, "192.0.2.0/31")
    assert error.value.status == 403
    assert web_scope.resolve_authorized_target(1, 1, "192.0.2.1")[1] == "192.0.2.1"
    with pytest.raises(web_scope.ScopeError) as error:
        web_scope.resolve_authorized_target(1, 1, "")
    assert error.value.status == 400


def test_scanner_rejects_direct_host_probe_before_network(monkeypatch):
    from core.scanner import CYMAGScanner
    monkeypatch.setattr(CYMAGScanner, "_make_nmap", staticmethod(lambda: None))
    scanner = CYMAGScanner("192.0.2.1", scope=["192.0.2.1"])
    with pytest.raises(ValueError):
        scanner.scan_host_services("127.0.0.1")
    with pytest.raises(ValueError):
        scanner.scan_host_services("192.0.2.2")
