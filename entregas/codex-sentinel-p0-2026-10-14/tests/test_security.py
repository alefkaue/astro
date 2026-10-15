"""Offline regressions: two organizations, persisted objects and no network."""
import uuid
from pathlib import Path

import pytest

from app import create_app, db
from app.config import config


@pytest.fixture
def security_env(monkeypatch):
    path = Path('instance') / f'security-{uuid.uuid4().hex}.db'
    monkeypatch.setattr(config, 'DB_PATH', str(path))
    monkeypatch.setattr(config, 'DEMO', False, raising=False)
    app = create_app()
    app.config['TESTING'] = True
    a = db.create_account('Organization A')
    b = db.create_account('Organization B')
    ua = db.create_user('a@example.test', 'A', 'Strong-local-password-123', 'owner', a)
    ub = db.create_user('b@example.test', 'B', 'Strong-local-password-123', 'owner', b)
    viewer = db.create_user('viewer@example.test', 'Viewer', 'Strong-local-password-123', 'viewer', a)
    staff = db.create_user('staff@example.test', 'Staff', 'Strong-local-password-123', 'admin', a)
    analyst = db.create_user('analyst@example.test', 'Analyst', 'Strong-local-password-123', 'operator', a)
    ea = db.create_engagement('A scope', '', ['192.0.2.1'], ua)
    eb = db.create_engagement('B scope', '', ['192.0.2.2'], ub)
    sb = db.create_scan('192.0.2.2', ub, eb)
    db.finish_scan(sb, [{'title': 'Private B evidence', 'host': '192.0.2.2', 'cvss': 0}], 0, organization_id=b)
    sa = db.create_scan('192.0.2.1', ua, ea)
    db.finish_scan(sa, [{'title': 'Local A evidence', 'host': '192.0.2.1', 'port': 443,
                        'sev': 'high', 'cvss': 0, 'desc': 'Laboratory fixture',
                        'evidence': 'token=fixture-secret'}], 0, organization_id=a)
    with db.get_conn() as conn:
        fa = conn.execute('SELECT id FROM findings WHERE scan_id=?', (sa,)).fetchone()['id']
        fb = conn.execute('SELECT id FROM findings WHERE scan_id=?', (sb,)).fetchone()['id']
    yield app, {'a': a, 'b': b, 'ua': ua, 'ub': ub, 'viewer': viewer, 'staff': staff,
                'ea': ea, 'eb': eb, 'sb': sb, 'sa':sa, 'fa':fa, 'fb':fb, 'analyst':analyst}
    for suffix in ('', '-wal', '-shm'):
        Path(str(path) + suffix).unlink(missing_ok=True)


def signed_client(app, uid):
    c = app.test_client()
    with c.session_transaction() as s:
        s['uid'] = uid
        s['role'] = db.get_user(uid)['role']
        s['csrf_token'] = 'security-test-csrf'
    return c


def test_engagement_list_isolated(security_env):
    app, ids = security_env
    c = signed_client(app, ids['ua'])
    rows = c.get('/api/engagements').get_json()['engagements']
    assert [r['id'] for r in rows] == [ids['ea']]


@pytest.mark.parametrize('resource', ['engagement', 'findings'])
def test_cross_tenant_read_is_hidden(security_env, resource):
    app, ids = security_env
    c = signed_client(app, ids['ua'])
    path = f"/api/engagements/{ids['eb']}" if resource == 'engagement' else f"/api/scans/{ids['sb']}/findings"
    assert c.get(path).status_code == 404


def test_platform_admin_does_not_bypass_owner(security_env):
    app, ids = security_env
    c = signed_client(app, ids['staff'])
    assert c.get('/api/owner/summary').status_code == 403


def test_disabled_user_session_rejected(security_env):
    app, ids = security_env
    c = signed_client(app, ids['ua'])
    with db.get_conn() as conn:
        conn.execute('UPDATE users SET active=0 WHERE id=?', (ids['ua'],))
    assert c.get('/api/engagements').status_code == 401


def test_viewer_cannot_create_scope(security_env):
    app, ids = security_env
    c = signed_client(app, ids['viewer'])
    r = c.post('/api/engagements', json={'name':'Forbidden','scope':['192.0.2.1']},
               headers={'X-CSRF-Token':'security-test-csrf'})
    assert r.status_code == 403


def test_missing_csrf_denied(security_env):
    app, ids = security_env
    c = signed_client(app, ids['ua'])
    assert c.post('/api/engagements', json={'name':'No CSRF','scope':['192.0.2.1']}).status_code == 403


def test_no_seed_without_demo(security_env):
    assert db.get_user_by_email('dono@pme.com') is None


def test_non_demo_checkout_disabled(security_env):
    app, ids = security_env
    c = signed_client(app, ids['ua'])
    r = c.post('/api/account/plan', json={'plan':'essencial'}, headers={'X-CSRF-Token':'security-test-csrf'})
    assert r.status_code == 403


def test_cross_tenant_run_hidden(security_env):
    from app.autonomous import runner
    app, ids = security_env
    run_id = runner.create_run('192.0.2.2', ids['eb'], ids['ub'], ids['sb'])
    c = signed_client(app, ids['ua'])
    try:
        assert c.get(f'/api/autonomous/{run_id}').status_code == 404
    finally:
        runner._RUNS.pop(run_id, None)


@pytest.mark.parametrize('kind', ['quick', 'detailed'])
def test_export_cannot_use_cross_tenant_or_forged_data(security_env, kind):
    app, ids = security_env
    c = signed_client(app, ids['ua'])
    r = c.post('/api/report/' + kind, json={'scan_id':ids['sb'], 'findings':[{'title':'Forged'}]},
               headers={'X-CSRF-Token':'security-test-csrf'})
    assert r.status_code == 404


def test_own_pdf_uses_persisted_data(security_env):
    app, ids = security_env
    c = signed_client(app, ids['ua'])
    r = c.post('/api/report/quick', json={'scan_id': ids['sa'], 'target':'Forged', 'findings':[]},
               headers={'X-CSRF-Token':'security-test-csrf'})
    assert r.status_code == 200
    assert r.data.startswith(b'%PDF')


@pytest.mark.parametrize('endpoint,body_key', [('/api/remediation','finding_id'),
    ('/api/owner/budget','finding_id'), ('/api/report/quick','scan_id')])
def test_cross_tenant_mutation_and_ai_hidden(security_env, endpoint, body_key):
    app, ids = security_env
    c = signed_client(app, ids['ua'])
    obj = ids['sb'] if body_key == 'scan_id' else ids['fb']
    r = c.post(endpoint, json={body_key:obj,'status':'authorized'},
               headers={'X-CSRF-Token':'security-test-csrf'})
    assert r.status_code == 404


def test_cross_tenant_authorization_and_review_hidden(security_env):
    app, ids = security_env
    c = signed_client(app, ids['ua'])
    for path, body in [(f"/api/engagements/{ids['eb']}/authorize", {}),
                       (f"/api/scans/{ids['sb']}/review", {'status':'signed'})]:
        assert c.post(path, json=body, headers={'X-CSRF-Token':'security-test-csrf'}).status_code == 404


@pytest.mark.parametrize('role', ['viewer','staff'])
def test_restricted_roles_cannot_export(security_env, role):
    app, ids = security_env
    c = signed_client(app, ids[role])
    r = c.post('/api/report/quick', json={'scan_id':ids['sa']},
               headers={'X-CSRF-Token':'security-test-csrf'})
    assert r.status_code == 403


def test_analyst_cannot_approve_scope(security_env):
    app, ids = security_env
    c = signed_client(app, ids['analyst'])
    r = c.post(f"/api/engagements/{ids['ea']}/authorize", json={},
               headers={'X-CSRF-Token':'security-test-csrf'})
    assert r.status_code == 403


@pytest.mark.parametrize('endpoint', ['/api/scan','/api/autonomous/run','/api/exploit_chain','/api/auto_discover'])
def test_legacy_executor_never_called(security_env, endpoint, monkeypatch):
    from app.scans.routes import CYMAGScanner
    from app.autonomous import runner
    def forbidden(*_args, **_kwargs):
        pytest.fail('Network executor must not run')
    monkeypatch.setattr(CYMAGScanner, 'run', forbidden)
    monkeypatch.setattr(runner, 'start', forbidden)
    app, ids = security_env
    c = signed_client(app, ids['ua'])
    headers = {'X-CSRF-Token':'security-test-csrf'}
    r = c.get(endpoint) if endpoint.endswith('auto_discover') else c.post(endpoint,json={'engagement_id':ids['ea']},headers=headers)
    assert r.status_code == 403
    assert r.get_json()['code'] == 'execution_disabled'


def test_db_no_implicit_global_scope(security_env):
    for operation in (db.list_engagements, db.list_scans, db.list_review_queue):
        with pytest.raises(PermissionError):
            operation()


def test_cross_tenant_scan_creation_denied(security_env):
    _, ids = security_env
    with pytest.raises(PermissionError):
        db.create_scan('192.0.2.2', ids['ua'], ids['eb'])


def test_membership_revocation_takes_effect(security_env):
    app, ids = security_env
    c = signed_client(app, ids['ua'])
    with db.get_conn() as conn:
        conn.execute('UPDATE memberships SET active=0 WHERE user_id=?', (ids['ua'],))
    assert c.get('/api/engagements').status_code == 404


def test_role_is_loaded_from_database(security_env):
    app, ids = security_env
    c = signed_client(app, ids['ua'])
    with db.get_conn() as conn:
        conn.execute("UPDATE users SET role='viewer' WHERE id=?", (ids['ua'],))
    assert c.get('/api/owner/summary').status_code == 403


def test_logout_revokes_copied_cookie(security_env):
    app, ids = security_env
    c = signed_client(app, ids['ua'])
    copied = c.get_cookie('session').value
    r = c.post('/api/logout', json={}, headers={'X-CSRF-Token':'security-test-csrf'})
    assert r.status_code == 200
    attacker = app.test_client()
    attacker.set_cookie('session', copied)
    assert attacker.get('/api/engagements').status_code == 401


def test_sensitive_evidence_redacted(security_env):
    app, ids = security_env
    c = signed_client(app, ids['ua'])
    r = c.get(f"/api/scans/{ids['sa']}/findings")
    assert r.status_code == 200
    assert b'fixture-secret' not in r.data
    assert b'REDACTED' in r.data


def test_ai_fallback_uses_own_finding(security_env):
    app, ids = security_env
    c = signed_client(app, ids['ua'])
    r = c.post('/api/remediation', json={'finding_id':ids['fa'], 'vuln':{'title':'Forged'}},
               headers={'X-CSRF-Token':'security-test-csrf'})
    assert r.status_code == 200
    assert r.get_json()['source'] == 'deterministic'
    assert r.get_json()['commands'] == ''


def test_login_csrf_and_persistent_rate_limit(security_env):
    app, _ = security_env
    c = app.test_client()
    body = {'email':'bad@example.test','password':'invalid'}
    assert c.post('/api/login', json=body).status_code == 403
    token = c.get('/api/csrf').get_json()['csrf_token']
    for _ in range(10):
        assert c.post('/api/login', json=body, headers={'X-CSRF-Token':token}).status_code == 401
    assert c.post('/api/login', json=body, headers={'X-CSRF-Token':token}).status_code == 429


@pytest.mark.parametrize('endpoint', ['/api/engagements','/api/scans/1/findings','/api/autonomous/nonexistent',
                                      '/api/owner/summary','/api/reviews','/api/account'])
def test_unauthenticated_resources_denied(security_env, endpoint):
    app, _ = security_env
    assert app.test_client().get(endpoint).status_code == 401


def test_production_refuses_initialization(monkeypatch):
    monkeypatch.setattr(config, 'ENVIRONMENT', 'production')
    monkeypatch.setattr(config, 'DEMO', False)
    monkeypatch.setattr(config, 'SECRET_KEY', 'x' * 64)
    monkeypatch.setattr(config, 'SESSION_COOKIE_SECURE', True)
    with pytest.raises(RuntimeError, match='PostgreSQL'):
        create_app()


@pytest.mark.parametrize('setting,value,message', [('DEMO',True,'Demo/debug'),('DEBUG',True,'Demo/debug'),
    ('SECRET_KEY','test-secret','Segredo'),('SESSION_COOKIE_SECURE',False,'Cookies')])
def test_production_rejects_unsafe_config(monkeypatch, setting, value, message):
    monkeypatch.setattr(config, 'ENVIRONMENT', 'production')
    monkeypatch.setattr(config, 'DEMO', False)
    monkeypatch.setattr(config, 'DEBUG', False)
    monkeypatch.setattr(config, 'SECRET_KEY', 'x' * 64)
    monkeypatch.setattr(config, 'SESSION_COOKIE_SECURE', True)
    monkeypatch.setattr(config, setting, value)
    with pytest.raises(RuntimeError, match=message):
        create_app()


@pytest.mark.parametrize('body', [[], {'name':[],'scope':['192.0.2.1']},
    {'name':'Invalid','scope':[123]}, {'name':'Invalid','scope': ['not-an-ip']}])
def test_invalid_input_rejected(security_env, body):
    app, ids = security_env
    c = signed_client(app, ids['ua'])
    r = c.post('/api/engagements', json=body, headers={'X-CSRF-Token':'security-test-csrf'})
    assert r.status_code == 400


def test_database_retains_ownership_when_creator_moves(security_env):
    _, ids = security_env
    with db.get_conn() as conn:
        conn.execute('UPDATE users SET account_id=? WHERE id=?', (ids['b'], ids['ua']))
    assert db.get_scan(ids['sa'], organization_id=ids['a']) is not None
    assert db.get_scan(ids['sa'], organization_id=ids['b']) is None


def test_membership_role_downgrade_blocks_mutation(security_env):
    app, ids = security_env
    c = signed_client(app, ids['ua'])
    with db.get_conn() as conn:
        conn.execute("UPDATE memberships SET role='viewer' WHERE user_id=?", (ids['ua'],))
    r = c.post('/api/engagements', json={'name':'Forbidden','scope':['192.0.2.1']},
               headers={'X-CSRF-Token':'security-test-csrf'})
    assert r.status_code == 403
    assert c.get('/api/owner/summary').status_code == 403


def test_non_demo_does_not_invent_money(security_env):
    app, ids = security_env
    c = signed_client(app, ids['ua'])
    summary = c.get('/api/owner/summary').get_json()['summary']
    assert summary['open_loss_max'] is None
    assert summary['financial_estimate_kind'] == 'not_estimated'
    assert all(p['price_month'] is None for p in c.get('/api/plans').get_json()['plans'])
    assert c.get('/api/billing/summary').get_json()['next_charge_at'] is None
