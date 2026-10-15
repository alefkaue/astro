"""
Camada de dados do CYMAG Enterprise (SQLite via stdlib).

Fornece:
  - init_db(): cria o schema e semeia usuários padrão.
  - get_conn(): conexão por chamada, com Row factory e WAL.
  - Repositórios finos: users, engagements, scans, findings, audit.

Escolha por sqlite3 puro (sem ORM) para manter a base leve e portável.
O modelo já contempla o conceito de *Engagement* — o escopo autorizado que
delimita eticamente o que o pentester autônomo pode tocar.
"""

import json
import logging
import sqlite3
import threading
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from werkzeug.security import generate_password_hash

from app.config import config
from flask import has_request_context, session

logger = logging.getLogger("cymag.db")

_LOCK = threading.Lock()

# Papéis DENTRO do cliente (PME): owner (dono, contrata/gerencia), operator
# (profissional interno que usa a plataforma), viewer (só relatórios executivos).
# Papéis da EQUIPE CYMAG: cymag (consultor que entrega pentest gerenciado),
# admin (superadmin da plataforma).
ROLES = ("admin", "owner", "operator", "viewer", "cymag")
STAFF_ROLES = ("admin", "cymag")


def get_membership(user_id, organization_id):
    with get_conn() as conn:
        return conn.execute('''SELECT m.* FROM memberships m JOIN users u ON u.id=m.user_id
            WHERE m.user_id=? AND m.organization_id=? AND m.active=1 AND u.active=1''',
            (user_id, organization_id)).fetchone()


def _tenant(organization_id=None):
    """No implicit global scope. Requests derive tenant from live membership."""
    if has_request_context():
        user = get_user(session.get('uid'))
        if not user or not user['active'] or user['session_version'] != session.get('session_version', 0) or not get_membership(user['id'], user['account_id']):
            raise PermissionError('Active membership required')
        if organization_id is not None and organization_id != user['account_id']:
            raise PermissionError('Cross-organization operation')
        return user['account_id']
    if organization_id is None:
        raise PermissionError('Explicit organization required outside requests')
    return organization_id


def _creator_tenant(user_id):
    user = get_user(user_id)
    if not user or not user['active'] or not get_membership(user_id, user['account_id']):
        raise PermissionError('Creator membership required')
    return _tenant(user['account_id'])


def _require_permission(permission):
    if has_request_context():
        from app.auth.decorators import has_permission
        if not has_permission(permission):
            raise PermissionError('Permission required')

SCHEMA = """
CREATE TABLE IF NOT EXISTS accounts (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    name                 TEXT NOT NULL,                     -- nome da empresa (PME) ou "CYMAG"
    plan                 TEXT NOT NULL DEFAULT 'comunidade',-- o plano é da CONTA (ver core/plans.py)
    is_staff             INTEGER NOT NULL DEFAULT 0,        -- 1 = conta interna da equipe CYMAG
    onboarding_done      INTEGER NOT NULL DEFAULT 0,        -- treinamento/"aula rápida" concluído
    managed_cadence_days INTEGER NOT NULL DEFAULT 0,        -- 0 = sem pentest gerenciado
    next_managed_at      TEXT,                              -- próximo pentest entregue pela CYMAG
    created_at           TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    email         TEXT UNIQUE NOT NULL,
    name          TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role          TEXT NOT NULL DEFAULT 'operator',
    account_id    INTEGER REFERENCES accounts(id),         -- o usuário herda o plano da conta
    active        INTEGER NOT NULL DEFAULT 1,
    created_at    TEXT NOT NULL,
    last_login    TEXT
);

CREATE TABLE IF NOT EXISTS engagements (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    name           TEXT NOT NULL,
    client         TEXT,
    scope          TEXT NOT NULL DEFAULT '[]',   -- JSON: lista de CIDRs/IPs autorizados
    status         TEXT NOT NULL DEFAULT 'draft', -- draft|authorized|active|closed
    created_by     INTEGER REFERENCES users(id),
    authorized_by  INTEGER REFERENCES users(id),
    created_at     TEXT NOT NULL,
    authorized_at  TEXT
);

CREATE TABLE IF NOT EXISTS scans (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    engagement_id  INTEGER REFERENCES engagements(id),
    target         TEXT NOT NULL,
    status         TEXT NOT NULL DEFAULT 'running', -- running|done|error
    risk_score     INTEGER DEFAULT 0,
    findings_count INTEGER DEFAULT 0,
    created_by     INTEGER REFERENCES users(id),
    started_at     TEXT NOT NULL,
    finished_at    TEXT,
    review_status  TEXT NOT NULL DEFAULT 'none',  -- none|pending|reviewed|signed (plano Gerenciado+)
    reviewed_by    INTEGER REFERENCES users(id),
    reviewed_at    TEXT,
    review_notes   TEXT
);

CREATE TABLE IF NOT EXISTS findings (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id     INTEGER NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
    host        TEXT,
    port        INTEGER,
    title       TEXT,
    severity    TEXT,
    cvss        REAL,
    cve         TEXT,
    category    TEXT,
    description TEXT,
    evidence    TEXT,
    banner      TEXT,
    raw         TEXT,          -- JSON do finding completo
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER REFERENCES users(id),
    action     TEXT NOT NULL,
    detail     TEXT,
    ip         TEXT,
    created_at TEXT NOT NULL
);

-- Decisões de ORÇAMENTO do dono sobre um problema (finding).
-- É o "embargo financeiro": o dono autoriza (ou dispensa) a verba para corrigir.
CREATE TABLE IF NOT EXISTS budget_decisions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id  INTEGER NOT NULL REFERENCES accounts(id),
    finding_id  INTEGER NOT NULL REFERENCES findings(id) ON DELETE CASCADE,
    status      TEXT NOT NULL DEFAULT 'authorized',  -- authorized|dismissed
    budget      REAL,                                -- verba aprovada (BRL), opcional
    note        TEXT,
    decided_by  INTEGER REFERENCES users(id),
    decided_at  TEXT NOT NULL,
    UNIQUE(finding_id)
);

CREATE INDEX IF NOT EXISTS idx_findings_scan ON findings(scan_id);
CREATE INDEX IF NOT EXISTS idx_scans_engagement ON scans(engagement_id);
CREATE INDEX IF NOT EXISTS idx_budget_account ON budget_decisions(account_id);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class _Connection(sqlite3.Connection):
    def __exit__(self, *args):
        try:
            return super().__exit__(*args)
        finally:
            self.close()


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(config.DB_PATH, timeout=10, check_same_thread=False, factory=_Connection)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def _column_exists(conn: sqlite3.Connection, table: str, col: str) -> bool:
    cols = [r["name"] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()]
    return col in cols


def _migrate(conn: sqlite3.Connection) -> None:
    """Adiciona colunas novas a bancos já existentes (idempotente, forward-only)."""
    if not _column_exists(conn, "users", "account_id"):
        conn.execute("ALTER TABLE users ADD COLUMN account_id INTEGER REFERENCES accounts(id)")
        logger.info("[db] migração: users.account_id adicionada")
    if not _column_exists(conn, 'users', 'session_version'):
        conn.execute('ALTER TABLE users ADD COLUMN session_version INTEGER NOT NULL DEFAULT 0')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_users_account ON users(account_id)')
    for col, ddl in (
        ("review_status", "TEXT NOT NULL DEFAULT 'none'"),
        ("reviewed_by", "INTEGER"),
        ("reviewed_at", "TEXT"),
        ("review_notes", "TEXT"),
    ):
        if not _column_exists(conn, "scans", col):
            conn.execute(f"ALTER TABLE scans ADD COLUMN {col} {ddl}")
            logger.info("[db] migração: scans.%s adicionada", col)
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY REFERENCES accounts(id), name TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS memberships (
            organization_id INTEGER NOT NULL REFERENCES organizations(id),
            user_id INTEGER NOT NULL REFERENCES users(id),
            role TEXT NOT NULL CHECK(role IN ('owner','admin','analyst','viewer')),
            active INTEGER NOT NULL DEFAULT 1,
            PRIMARY KEY(organization_id,user_id)
        );
    ''')
    for table in ('engagements', 'scans', 'findings', 'audit_log', 'budget_decisions'):
        if not _column_exists(conn, table, 'organization_id'):
            conn.execute(f'ALTER TABLE {table} ADD COLUMN organization_id INTEGER REFERENCES organizations(id)')
        conn.execute(f'CREATE INDEX IF NOT EXISTS idx_{table}_organization ON {table}(organization_id)')
    conn.execute('INSERT OR IGNORE INTO organizations SELECT id,name,created_at FROM accounts WHERE is_staff=0')
    conn.execute('''INSERT OR IGNORE INTO memberships
        SELECT u.account_id,u.id,CASE WHEN u.role='operator' THEN 'analyst' ELSE u.role END, u.active
        FROM users u JOIN organizations o ON o.id=u.account_id
        WHERE u.role IN ('owner','operator','analyst','viewer')''')
    if conn.execute('SELECT 1 FROM schema_migrations WHERE version=1').fetchone():
        return
    # Only migrate ownership proved by immutable creator/account relationships.
    conn.execute('''UPDATE engagements SET organization_id=(
        SELECT o.id FROM users u JOIN organizations o ON o.id=u.account_id WHERE u.id=engagements.created_by
    ) WHERE organization_id IS NULL''')
    conn.execute('''UPDATE scans SET organization_id=(
        SELECT o.id FROM users u JOIN organizations o ON o.id=u.account_id WHERE u.id=scans.created_by
        AND (scans.engagement_id IS NULL OR EXISTS (
            SELECT 1 FROM engagements e WHERE e.id=scans.engagement_id AND e.organization_id=o.id))
    ) WHERE organization_id IS NULL''')
    conn.execute('''UPDATE findings SET organization_id=(SELECT organization_id FROM scans WHERE id=findings.scan_id)
        WHERE organization_id IS NULL''')
    conn.execute('''UPDATE audit_log SET organization_id=(
        SELECT o.id FROM users u JOIN organizations o ON o.id=u.account_id WHERE u.id=audit_log.user_id)
        WHERE organization_id IS NULL''')
    conn.execute('''UPDATE budget_decisions SET organization_id=(
        SELECT organization_id FROM findings WHERE id=budget_decisions.finding_id AND organization_id=budget_decisions.account_id)
        WHERE organization_id IS NULL''')
    conn.execute('INSERT INTO schema_migrations VALUES(1,?)', (_now(),))


def init_db() -> None:
    """Cria o schema, migra colunas novas e semeia os usuários padrão (idempotente)."""
    # Online SQLite backup includes committed WAL content. Never copy just .db.
    path = Path(config.DB_PATH)
    if path.exists():
        with get_conn() as source:
            ready = source.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='organizations'").fetchone()
            if not ready:
                backup_path = path.with_name(path.name + '.pre-tenant-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f') + '.bak')
                destination = sqlite3.connect(backup_path)
                try:
                    source.backup(destination)
                finally:
                    destination.close()
    with _LOCK, get_conn() as conn:
        conn.executescript(SCHEMA)
        _migrate(conn)
        conn.commit()
    if config.DEMO:
        _seed_users()
        with get_conn() as conn:
            _migrate(conn)


def _seed_users() -> None:
    """Semeia contas e usuários de demonstração (idempotente).

    A história que os dados contam:
      • CYMAG (equipe)  — conta interna que ENTREGA os serviços gerenciados.
      • PME Demo Ltda    — cliente no plano Profissional: dono contrata, o TI usa.
      • Loja Verde       — cliente no plano Gerenciado: a CYMAG faz o pentest.
    """
    admin_pw = config.ADMIN_PASSWORD or "cymag-admin"

    # (nome da conta, plano, is_staff, cadência_dias) -> lista de usuários (email, nome, senha, papel)
    accounts = [
        ("CYMAG (equipe)", "enterprise", 1, 0, [
            (config.ADMIN_EMAIL,   "Administrador",     admin_pw,        "admin"),
            ("consultor@cymag.com", "Consultor CYMAG",  "cybersecurity", "cymag"),
        ]),
        ("PME Demo Ltda", "profissional", 0, 0, [
            ("dono@pme.com", "Dono da PME",           "cybersecurity", "owner"),
            ("ti@pme.com",   "Analista de TI (único)", "cybersecurity", "operator"),
        ]),
        ("Loja Verde", "gerenciado", 0, 60, [
            ("dono@lojaverde.com", "Dona da Loja Verde", "cybersecurity", "owner"),
        ]),
    ]
    with _LOCK, get_conn() as conn:
        for acc_name, plan, is_staff, cadence, users in accounts:
            row = conn.execute("SELECT id FROM accounts WHERE name=?", (acc_name,)).fetchone()
            if row:
                acc_id = row["id"]
            else:
                next_managed = None
                if cadence:
                    next_managed = (datetime.now(timezone.utc)).isoformat(timespec="seconds")
                cur = conn.execute(
                    "INSERT INTO accounts (name, plan, is_staff, onboarding_done, "
                    "managed_cadence_days, next_managed_at, created_at) VALUES (?,?,?,?,?,?,?)",
                    (acc_name, plan, is_staff, 1 if plan != "comunidade" else 0,
                     cadence, next_managed, _now()),
                )
                acc_id = cur.lastrowid
                logger.info("[db] Conta semeada: %s (plano %s)", acc_name, plan)
            for email, name, pw, role in users:
                if conn.execute("SELECT 1 FROM users WHERE email=?", (email,)).fetchone():
                    continue
                conn.execute(
                    "INSERT INTO users (email, name, password_hash, role, account_id, active, created_at) "
                    "VALUES (?,?,?,?,?,1,?)",
                    (email, name, generate_password_hash(pw), role, acc_id, _now()),
                )
                logger.info("[db] Usuário semeado: %s (%s @ %s)", email, role, acc_name)
        conn.commit()


# ─── USERS ─────────────────────────────────────────────────────────────────────

def get_user_by_email(email: str) -> Optional[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE email=? AND active=1", (email.strip().lower(),)
        ).fetchone()


def get_user(user_id: int) -> Optional[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()


def touch_last_login(user_id: int) -> None:
    with _LOCK, get_conn() as conn:
        conn.execute("UPDATE users SET last_login=? WHERE id=?", (_now(), user_id))
        conn.commit()


def rotate_sessions(user_id):
    with _LOCK, get_conn() as conn:
        conn.execute('UPDATE users SET session_version=session_version+1 WHERE id=?', (user_id,))
        version = conn.execute('SELECT session_version FROM users WHERE id=?', (user_id,)).fetchone()
    return version['session_version']


def create_user(email: str, name: str, password: str, role: str = "operator",
                account_id: Optional[int] = None) -> int:
    if role not in ROLES + ('analyst',):
        raise ValueError(f"Papel inválido: {role}")
    with _LOCK, get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO users (email, name, password_hash, role, account_id, active, created_at) "
            "VALUES (?,?,?,?,?,1,?)",
            (email.strip().lower(), name, generate_password_hash(password), role, account_id, _now()),
        )
        if account_id is not None and role in ('owner', 'operator', 'analyst', 'viewer'):
            conn.execute('INSERT INTO memberships(organization_id,user_id,role) VALUES(?,?,?)',
                         (account_id, cur.lastrowid, 'analyst' if role == 'operator' else role))
        conn.commit()
        return cur.lastrowid


# ─── ACCOUNTS (a empresa que contrata — dona do plano) ─────────────────────────────

def create_account(name: str, plan: str = "comunidade", is_staff: int = 0,
                   managed_cadence_days: int = 0) -> int:
    with _LOCK, get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO accounts (name, plan, is_staff, managed_cadence_days, created_at) "
            "VALUES (?,?,?,?,?)",
            (name, plan, is_staff, managed_cadence_days, _now()),
        )
        if not is_staff:
            conn.execute('INSERT INTO organizations(id,name,created_at) VALUES(?,?,?)', (cur.lastrowid, name, _now()))
        conn.commit()
        return cur.lastrowid


def get_account(account_id: Optional[int]) -> Optional[Dict]:
    if account_id is None:
        return None
    if has_request_context():
        user = get_user(session.get('uid'))
        if not user or user['account_id'] != account_id:
            raise PermissionError('Account not found')
    with get_conn() as conn:
        r = conn.execute("SELECT * FROM accounts WHERE id=?", (account_id,)).fetchone()
    return dict(r) if r else None


def list_accounts(limit: int = 100) -> List[Dict]:
    """Contas de clientes (exclui as internas da CYMAG) — para o console da equipe."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id,name,plan,managed_cadence_days,next_managed_at FROM accounts WHERE is_staff=0 ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def set_account_plan(account_id: int, plan: str) -> None:
    _tenant(account_id)
    with _LOCK, get_conn() as conn:
        conn.execute("UPDATE accounts SET plan=? WHERE id=?", (plan, account_id))
        conn.commit()


def subscribe_account(account_id: int, plan: str, managed_cadence_days: int) -> None:
    """Troca o plano da conta e ajusta a cadência/próxima entrega do serviço gerenciado.

    É a operação por trás do "assinar/trocar de plano" (self-service do dono).
    Quando o novo plano é gerenciado, agenda a próxima entrega; quando não é,
    zera a cadência. O onboarding passa a 'feito' em qualquer plano pago.
    """
    _tenant(account_id)
    if not config.DEMO:
        raise PermissionError('Simulated checkout requires DEMO')
    next_managed = None
    if managed_cadence_days:
        next_managed = (datetime.now(timezone.utc)
                        + timedelta(days=managed_cadence_days)).isoformat(timespec="seconds")
    with _LOCK, get_conn() as conn:
        conn.execute(
            "UPDATE accounts SET plan=?, managed_cadence_days=?, next_managed_at=?, "
            "onboarding_done=? WHERE id=?",
            (plan, managed_cadence_days, next_managed,
             1 if plan != "comunidade" else 0, account_id),
        )
        conn.commit()


def account_users(account_id: int) -> List[Dict]:
    _tenant(account_id)
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, email, name, role, last_login FROM users WHERE account_id=? ORDER BY id",
            (account_id,),
        ).fetchall()
    return [dict(r) for r in rows]


def plan_key_for_user(user_id: int) -> str:
    """Plano efetivo de um usuário = plano da sua conta (default se sem conta)."""
    with get_conn() as conn:
        r = conn.execute(
            "SELECT a.plan AS plan FROM users u LEFT JOIN accounts a ON a.id = u.account_id "
            "WHERE u.id=?", (user_id,),
        ).fetchone()
    return (r["plan"] if r and r["plan"] else "comunidade")


# ─── ENGAGEMENTS ────────────────────────────────────────────────────────────────

def create_engagement(name: str, client: str, scope: List[str], created_by: Optional[int]) -> int:
    _require_permission('scope:write')
    organization_id = _creator_tenant(created_by)
    with _LOCK, get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO engagements (name, client, scope, status, created_by, created_at, organization_id) "
            "VALUES (?,?,?, 'draft', ?, ?, ?)",
            (name, client, json.dumps(scope), created_by, _now(), organization_id),
        )
        conn.commit()
        return cur.lastrowid


def list_engagements(limit: int = 100, *, organization_id=None) -> List[Dict]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM engagements WHERE organization_id=? ORDER BY id DESC LIMIT ?", (_tenant(organization_id), limit)
        ).fetchall()
    out = []
    for r in rows:
        d = dict(r)
        try:
            d["scope"] = json.loads(d.get("scope") or "[]")
        except (TypeError, json.JSONDecodeError):
            d["scope"] = []
        out.append(d)
    return out


def get_engagement(engagement_id: int, *, organization_id=None) -> Optional[Dict]:
    with get_conn() as conn:
        r = conn.execute("SELECT * FROM engagements WHERE id=? AND organization_id=?", (engagement_id, _tenant(organization_id))).fetchone()
    if not r:
        return None
    d = dict(r)
    try:
        d["scope"] = json.loads(d.get("scope") or "[]")
    except (TypeError, json.JSONDecodeError):
        d["scope"] = []
    return d


def authorize_engagement(engagement_id: int, authorized_by: int, *, organization_id=None) -> None:
    _require_permission('scope:approve')
    with _LOCK, get_conn() as conn:
        conn.execute(
            "UPDATE engagements SET status='authorized', authorized_by=?, authorized_at=? WHERE id=? AND organization_id=?",
            (authorized_by, _now(), engagement_id, _tenant(organization_id)),
        )
        conn.commit()


# ─── SCANS / FINDINGS ───────────────────────────────────────────────────────────

def create_scan(target: str, created_by: Optional[int], engagement_id: Optional[int] = None) -> int:
    _require_permission('scan:execute')
    organization_id = _creator_tenant(created_by)
    if engagement_id is not None and not get_engagement(engagement_id, organization_id=organization_id):
        raise PermissionError('Scope ownership mismatch')
    with _LOCK, get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO scans (engagement_id, target, status, created_by, started_at, organization_id) "
            "VALUES (?,?, 'running', ?, ?, ?)",
            (engagement_id, target, created_by, _now(), organization_id),
        )
        conn.commit()
        return cur.lastrowid


def finish_scan(scan_id: int, findings: List[Dict[str, Any]], risk_score: int, status: str = "done", *, organization_id=None) -> None:
    organization_id = _tenant(organization_id)
    if not get_scan(scan_id, organization_id=organization_id):
        raise PermissionError('Scan not found')
    from core.redaction import redact
    findings = [redact(f) for f in findings]
    with _LOCK, get_conn() as conn:
        for f in findings:
            conn.execute(
                "INSERT INTO findings (scan_id, host, port, title, severity, cvss, cve, "
                "category, description, evidence, banner, raw, created_at, organization_id) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    scan_id, f.get("host"), f.get("port"), f.get("title"),
                    f.get("sev"), f.get("cvss"), f.get("cve"), f.get("category"),
                    f.get("desc"), (f.get("evidence") or "")[:2000], f.get("banner"),
                    json.dumps(f, ensure_ascii=False), _now(), organization_id,
                ),
            )
        conn.execute(
            "UPDATE scans SET status=?, risk_score=?, findings_count=?, finished_at=? WHERE id=? AND organization_id=?",
            (status, risk_score, len(findings), _now(), scan_id, organization_id),
        )
        conn.commit()


def list_scans(limit: int = 50, created_by: Optional[int] = None, *, organization_id=None) -> List[Dict]:
    q = "SELECT * FROM scans WHERE organization_id=?"
    params: list = [_tenant(organization_id)]
    if created_by is not None:
        q += " AND created_by=?"
        params.append(created_by)
    q += " ORDER BY id DESC LIMIT ?"
    params.append(limit)
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(q, params).fetchall()]


def get_scan(scan_id: int, *, organization_id=None) -> Optional[Dict]:
    with get_conn() as conn:
        r = conn.execute("SELECT * FROM scans WHERE id=? AND organization_id=?", (scan_id, _tenant(organization_id))).fetchone()
    return dict(r) if r else None


def get_scan_findings(scan_id: int, *, organization_id=None) -> List[Dict]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT raw FROM findings WHERE scan_id=? AND organization_id=? ORDER BY cvss DESC", (scan_id, _tenant(organization_id))
        ).fetchall()
    return [json.loads(r["raw"]) for r in rows if r["raw"]]


def get_scan_findings_with_ids(scan_id: int, *, organization_id=None) -> List[Dict]:
    """Como get_scan_findings, mas cada finding vem com sua 'finding_id' (id da linha).

    Necessário para a visão do dono, que anexa decisões de orçamento por finding.
    """
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, raw FROM findings WHERE scan_id=? AND organization_id=? ORDER BY cvss DESC", (scan_id, _tenant(organization_id))
        ).fetchall()
    out = []
    for r in rows:
        if not r["raw"]:
            continue
        f = json.loads(r["raw"])
        f["finding_id"] = r["id"]
        out.append(f)
    return out


# ─── ORÇAMENTO / EMBARGO FINANCEIRO (decisões do dono) ─────────────────────────────

def latest_account_scan(account_id: int) -> Optional[Dict]:
    """Scan concluído mais recente de qualquer usuário da conta (para o painel do dono)."""
    with get_conn() as conn:
        r = conn.execute(
            "SELECT s.* FROM scans s WHERE s.organization_id=? AND s.status='done' ORDER BY s.id DESC LIMIT 1",
            (_tenant(account_id),),
        ).fetchone()
    return dict(r) if r else None


def finding_account_id(finding_id: int) -> Optional[int]:
    """Conta dona de um finding (via scan → usuário que o criou). None se órfão."""
    with get_conn() as conn:
        r = conn.execute(
            "SELECT organization_id AS aid FROM findings WHERE id=? AND organization_id=?",
            (finding_id, _tenant()),
        ).fetchone()
    return r["aid"] if r else None


def set_budget_decision(account_id: int, finding_id: int, status: str,
                        budget: Optional[float], decided_by: Optional[int],
                        note: Optional[str] = None) -> None:
    """Grava (ou substitui) a decisão de orçamento do dono sobre um problema."""
    _require_permission('billing:manage')
    if _tenant(account_id) != finding_account_id(finding_id):
        raise PermissionError('Finding not found')
    with _LOCK, get_conn() as conn:
        conn.execute(
            "INSERT INTO budget_decisions (account_id, finding_id, status, budget, note, decided_by, decided_at, organization_id) "
            "VALUES (?,?,?,?,?,?,?,?) "
            "ON CONFLICT(finding_id) DO UPDATE SET "
            "status=excluded.status, budget=excluded.budget, note=excluded.note, "
            "decided_by=excluded.decided_by, decided_at=excluded.decided_at",
            (account_id, finding_id, status, budget, note, decided_by, _now(), account_id),
        )
        conn.commit()


def budget_decisions_for_account(account_id: int) -> Dict[int, Dict]:
    """Mapa finding_id → decisão (com nome de quem decidiu), para a conta."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT b.*, u.name AS decided_by_name FROM budget_decisions b "
            "LEFT JOIN users u ON u.id = b.decided_by "
            "JOIN findings f ON f.id=b.finding_id AND f.organization_id=b.organization_id "
            "WHERE b.account_id=? AND b.organization_id=?",
            (_tenant(account_id), _tenant(account_id)),
        ).fetchall()
    return {r["finding_id"]: dict(r) for r in rows}


# ─── QUOTA (limite de scans por plano) ────────────────────────────────────────────

def count_scans_this_month(user_id: int) -> int:
    """Quantos scans o usuário iniciou no mês corrente (UTC) — base da quota."""
    ym = datetime.now(timezone.utc).strftime("%Y-%m")
    with get_conn() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS n FROM scans WHERE created_by=? AND substr(started_at,1,7)=?",
            (user_id, ym),
        ).fetchone()
    return int(row["n"]) if row else 0


# ─── REVISÃO HUMANA (plano Gerenciado+) ───────────────────────────────────────────

def set_review_status(scan_id: int, status: str, reviewed_by: Optional[int] = None,
                      notes: Optional[str] = None) -> None:
    """Move um scan pela esteira de revisão: none→pending→reviewed→signed."""
    _require_permission('finding:write')
    organization_id = _tenant()
    if not get_scan(scan_id, organization_id=organization_id):
        raise PermissionError('Scan not found')
    with _LOCK, get_conn() as conn:
        if status in ("reviewed", "signed"):
            conn.execute(
                "UPDATE scans SET review_status=?, reviewed_by=?, reviewed_at=?, review_notes=? WHERE id=? AND organization_id=?",
                (status, reviewed_by, _now(), notes, scan_id, organization_id),
            )
        else:
            conn.execute("UPDATE scans SET review_status=? WHERE id=? AND organization_id=?", (status, scan_id, organization_id))
        conn.commit()


def list_review_queue(limit: int = 50, *, organization_id=None) -> List[Dict]:
    """Scans aguardando validação humana (mais recentes primeiro)."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM scans WHERE organization_id=? AND review_status='pending' ORDER BY id DESC LIMIT ?",
            (_tenant(organization_id), limit),
        ).fetchall()
    return [dict(r) for r in rows]


# ─── AUDIT ───────────────────────────────────────────────────────────────────────

def audit(user_id: Optional[int], action: str, detail: str = "", ip: str = "") -> None:
    from core.redaction import redact
    detail = redact(detail)[:1000]
    try:
        with _LOCK, get_conn() as conn:
            user = conn.execute('SELECT account_id FROM users WHERE id=?', (user_id,)).fetchone()
            organization = conn.execute('SELECT id FROM organizations WHERE id=?', (user['account_id'],)).fetchone() if user else None
            conn.execute(
                "INSERT INTO audit_log (user_id, action, detail, ip, created_at, organization_id) VALUES (?,?,?,?,?,?)",
                (user_id, action, detail, ip, _now(), organization['id'] if organization else None),
            )
            conn.commit()
    except Exception as e:  # auditoria nunca deve derrubar a requisição
        logger.warning("[db] falha ao auditar '%s' (%s)", action, type(e).__name__)
