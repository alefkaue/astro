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
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from werkzeug.security import generate_password_hash

from app.config import config

logger = logging.getLogger("cymag.db")

_LOCK = threading.Lock()
_RL_LOCK = threading.Lock()  # serializa writes de rate-limit dentro do processo

# Papéis DENTRO do cliente (PME): owner (dono, contrata/gerencia), operator
# (profissional interno que usa a plataforma), viewer (só relatórios executivos).
# Papéis da EQUIPE CYMAG: cymag (consultor que entrega pentest gerenciado),
# admin (superadmin da plataforma).
ROLES = ("admin", "owner", "operator", "viewer", "cymag")
STAFF_ROLES = ("admin", "cymag")

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
    account_id     INTEGER REFERENCES accounts(id),  -- tenant dono (isolamento multiempresa)
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
    account_id     INTEGER REFERENCES accounts(id),  -- tenant dono (isolamento multiempresa)
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
CREATE INDEX IF NOT EXISTS idx_users_account ON users(account_id);
CREATE INDEX IF NOT EXISTS idx_budget_account ON budget_decisions(account_id);

-- Rate-limit de login compartilhado entre workers (G0-S14).
-- key = "email:<email>" ou "ip:<ip>"; ts_json guarda os timestamps da janela deslizante.
CREATE TABLE IF NOT EXISTS login_attempts (
    key           TEXT PRIMARY KEY,
    ts_json       TEXT NOT NULL DEFAULT '[]',  -- JSON list de timestamps de falha na janela
    blocked_until REAL NOT NULL DEFAULT 0
);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(config.DB_PATH, timeout=10, check_same_thread=False)
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
    for col, ddl in (
        ("review_status", "TEXT NOT NULL DEFAULT 'none'"),
        ("reviewed_by", "INTEGER"),
        ("reviewed_at", "TEXT"),
        ("review_notes", "TEXT"),
    ):
        if not _column_exists(conn, "scans", col):
            conn.execute(f"ALTER TABLE scans ADD COLUMN {col} {ddl}")
            logger.info("[db] migração: scans.%s adicionada", col)

    # ── Isolamento multiempresa (SEC-002): account_id em engagements e scans ──
    # Colunas nullable + backfill a partir do criador (user.account_id). Registros
    # cujo criador não tem conta ficam NULL (órfãos) e nunca casam com um tenant
    # real nas queries filtradas — isolamento fail-safe, sem inferência silenciosa.
    for table in ("engagements", "scans"):
        if not _column_exists(conn, table, "account_id"):
            conn.execute(f"ALTER TABLE {table} ADD COLUMN account_id INTEGER REFERENCES accounts(id)")
            conn.execute(
                f"UPDATE {table} SET account_id = ("
                f"  SELECT u.account_id FROM users u WHERE u.id = {table}.created_by"
                f") WHERE account_id IS NULL"
            )
            logger.info("[db] migração: %s.account_id adicionada e backfilled", table)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_engagements_account ON engagements(account_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_scans_account ON scans(account_id)")


def init_db() -> None:
    """Cria o schema, migra colunas novas e (só fora de produção) semeia demo.

    Fail-closed: em produção/staging NÃO semeia contas/credenciais de demonstração.
    Um boot produtivo começa sem usuários — o admin real é provisionado à parte."""
    with _LOCK, get_conn() as conn:
        conn.executescript(SCHEMA)
        _migrate(conn)
        conn.commit()
    if config.seeding_allowed():
        _seed_users()
    else:
        logger.info("[db] ENV=%s: seed de demonstração desativado (fail-closed).", config.ENV)


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


def create_user(email: str, name: str, password: str, role: str = "operator",
                account_id: Optional[int] = None) -> int:
    if role not in ROLES:
        raise ValueError(f"Papel inválido: {role}")
    with _LOCK, get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO users (email, name, password_hash, role, account_id, active, created_at) "
            "VALUES (?,?,?,?,?,1,?)",
            (email.strip().lower(), name, generate_password_hash(password), role, account_id, _now()),
        )
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
        conn.commit()
        return cur.lastrowid


def get_account(account_id: Optional[int]) -> Optional[Dict]:
    if account_id is None:
        return None
    with get_conn() as conn:
        r = conn.execute("SELECT * FROM accounts WHERE id=?", (account_id,)).fetchone()
    return dict(r) if r else None


def list_accounts(limit: int = 100) -> List[Dict]:
    """Contas de clientes (exclui as internas da CYMAG) — para o console da equipe."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM accounts WHERE is_staff=0 ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def set_account_plan(account_id: int, plan: str) -> None:
    with _LOCK, get_conn() as conn:
        conn.execute("UPDATE accounts SET plan=? WHERE id=?", (plan, account_id))
        conn.commit()


def subscribe_account(account_id: int, plan: str, managed_cadence_days: int) -> None:
    """Troca o plano da conta e ajusta a cadência/próxima entrega do serviço gerenciado.

    É a operação por trás do "assinar/trocar de plano" (self-service do dono).
    Quando o novo plano é gerenciado, agenda a próxima entrega; quando não é,
    zera a cadência. O onboarding passa a 'feito' em qualquer plano pago.
    """
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

def create_engagement(name: str, client: str, scope: List[str], created_by: Optional[int],
                       account_id: Optional[int] = None) -> int:
    with _LOCK, get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO engagements (account_id, name, client, scope, status, created_by, created_at) "
            "VALUES (?,?,?,?, 'draft', ?, ?)",
            (account_id, name, client, json.dumps(scope), created_by, _now()),
        )
        conn.commit()
        return cur.lastrowid


def _row_to_engagement(r: sqlite3.Row) -> Dict:
    d = dict(r)
    try:
        d["scope"] = json.loads(d.get("scope") or "[]")
    except (TypeError, json.JSONDecodeError):
        d["scope"] = []
    return d


def list_engagements(account_id: Optional[int], limit: int = 100) -> List[Dict]:
    """Engagements do tenant. `account_id=None` (usuário sem conta) → lista vazia."""
    if account_id is None:
        return []
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM engagements WHERE account_id=? ORDER BY id DESC LIMIT ?",
            (account_id, limit),
        ).fetchall()
    return [_row_to_engagement(r) for r in rows]


def get_engagement(engagement_id: int, account_id: Optional[int] = None) -> Optional[Dict]:
    """Devolve o engagement. Se `account_id` for informado, só devolve se pertencer
    a esse tenant (caso contrário None → a rota responde 404, sem revelar existência)."""
    with get_conn() as conn:
        if account_id is None:
            r = conn.execute("SELECT * FROM engagements WHERE id=?", (engagement_id,)).fetchone()
        else:
            r = conn.execute(
                "SELECT * FROM engagements WHERE id=? AND account_id IS ?",
                (engagement_id, account_id),
            ).fetchone()
    return _row_to_engagement(r) if r else None


def authorize_engagement(engagement_id: int, authorized_by: int, account_id: Optional[int] = None) -> bool:
    # Legacy internal callers derive tenant from the authorizer, never unscoped.
    authorizer = get_user(authorized_by)
    if not authorizer or not authorizer["active"] or authorizer["account_id"] is None:
        return False
    if account_id is None:
        account_id = authorizer["account_id"]
    if account_id != authorizer["account_id"]:
        return False
    with _LOCK, get_conn() as conn:
        updated = conn.execute(
            "UPDATE engagements SET status='authorized', authorized_by=?, authorized_at=? WHERE id=? AND account_id=?",
            (authorized_by, _now(), engagement_id, account_id),
        )
        conn.commit()
        return updated.rowcount == 1


# ─── SCANS / FINDINGS ───────────────────────────────────────────────────────────

def create_scan(target: str, created_by: Optional[int], engagement_id: Optional[int] = None,
                account_id: Optional[int] = None) -> int:
    with _LOCK, get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO scans (account_id, engagement_id, target, status, created_by, started_at) "
            "VALUES (?,?,?, 'running', ?, ?)",
            (account_id, engagement_id, target, created_by, _now()),
        )
        conn.commit()
        return cur.lastrowid


def finish_scan(scan_id: int, findings: List[Dict[str, Any]], risk_score: int, status: str = "done") -> None:
    with _LOCK, get_conn() as conn:
        for f in findings:
            conn.execute(
                "INSERT INTO findings (scan_id, host, port, title, severity, cvss, cve, "
                "category, description, evidence, banner, raw, created_at) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    scan_id, f.get("host"), f.get("port"), f.get("title"),
                    f.get("sev"), f.get("cvss"), f.get("cve"), f.get("category"),
                    f.get("desc"), (f.get("evidence") or "")[:2000], f.get("banner"),
                    json.dumps(f, ensure_ascii=False), _now(),
                ),
            )
        conn.execute(
            "UPDATE scans SET status=?, risk_score=?, findings_count=?, finished_at=? WHERE id=?",
            (status, risk_score, len(findings), _now(), scan_id),
        )
        conn.commit()


def list_scans(limit: int = 50, account_id: Optional[int] = None) -> List[Dict]:
    """Scans do tenant. `account_id=None` (sem conta) → lista vazia (fail-safe)."""
    if account_id is None:
        return []
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM scans WHERE account_id=? ORDER BY id DESC LIMIT ?",
            (account_id, limit),
        ).fetchall()]


def get_scan(scan_id: int, account_id: Optional[int] = None) -> Optional[Dict]:
    """Scan por id. Com `account_id`, só devolve se pertencer ao tenant (senão None)."""
    with get_conn() as conn:
        if account_id is None:
            r = conn.execute("SELECT * FROM scans WHERE id=?", (scan_id,)).fetchone()
        else:
            r = conn.execute(
                "SELECT * FROM scans WHERE id=? AND account_id=?", (scan_id, account_id)
            ).fetchone()
    return dict(r) if r else None


def get_scan_findings(scan_id: int, account_id: Optional[int] = None) -> Optional[List[Dict]]:
    """Achados de um scan, mas só se o scan pertencer ao tenant.

    Retorna `None` quando o scan não existe ou não é do tenant (a rota responde 404);
    lista (possivelmente vazia) quando autorizado. Com `account_id=None` não filtra
    (uso interno/staff) — rotas de cliente SEMPRE passam o account_id.
    """
    with get_conn() as conn:
        if account_id is None:
            owns = conn.execute("SELECT 1 FROM scans WHERE id=?", (scan_id,)).fetchone()
        else:
            owns = conn.execute(
                "SELECT 1 FROM scans WHERE id=? AND account_id=?", (scan_id, account_id)
            ).fetchone()
        if not owns:
            return None
        rows = conn.execute(
            "SELECT raw FROM findings WHERE scan_id=? ORDER BY cvss DESC", (scan_id,)
        ).fetchall()
    return [json.loads(r["raw"]) for r in rows if r["raw"]]


def get_scan_findings_with_ids(scan_id: int) -> List[Dict]:
    """Como get_scan_findings, mas cada finding vem com sua 'finding_id' (id da linha).

    Necessário para a visão do dono, que anexa decisões de orçamento por finding.
    """
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, raw FROM findings WHERE scan_id=? ORDER BY cvss DESC", (scan_id,)
        ).fetchall()
    out = []
    for r in rows:
        if not r["raw"]:
            continue
        f = json.loads(r["raw"])
        f["finding_id"] = r["id"]
        out.append(f)
    return out


def get_finding_by_id(finding_id: int, account_id: int) -> Optional[Dict]:
    """Retorna um finding pelo seu id verificando que pertence ao tenant.

    Usa JOIN com scans para garantir isolamento: um tenant só vê seus próprios
    achados, mesmo conhecendo IDs de outros tenants (previne IDOR/AI-001).
    Devolve None se o finding não existir ou não pertencer ao tenant.
    """
    with get_conn() as conn:
        r = conn.execute(
            """
            SELECT f.id, f.raw
              FROM findings f
              JOIN scans s ON s.id = f.scan_id
             WHERE f.id = ? AND s.account_id = ?
            """,
            (finding_id, account_id),
        ).fetchone()
    if not r or not r["raw"]:
        return None
    finding = json.loads(r["raw"])
    finding["finding_id"] = r["id"]
    return finding


# ─── ORÇAMENTO / EMBARGO FINANCEIRO (decisões do dono) ─────────────────────────────

def latest_account_scan(account_id: int) -> Optional[Dict]:
    """Scan concluído mais recente da conta (para o painel do dono).

    Usa o `account_id` próprio do scan (tenant dono), não a conta atual do criador."""
    with get_conn() as conn:
        r = conn.execute(
            "SELECT * FROM scans WHERE account_id=? AND status='done' "
            "ORDER BY id DESC LIMIT 1",
            (account_id,),
        ).fetchone()
    return dict(r) if r else None


def finding_account_id(finding_id: int) -> Optional[int]:
    """Conta dona de um finding (via scan.account_id). None se órfão/inexistente."""
    with get_conn() as conn:
        r = conn.execute(
            "SELECT s.account_id AS aid FROM findings f "
            "JOIN scans s ON s.id = f.scan_id WHERE f.id=?",
            (finding_id,),
        ).fetchone()
    return r["aid"] if r else None


def set_budget_decision(account_id: int, finding_id: int, status: str,
                        budget: Optional[float], decided_by: Optional[int],
                        note: Optional[str] = None) -> None:
    """Grava (ou substitui) a decisão de orçamento do dono sobre um problema."""
    with _LOCK, get_conn() as conn:
        conn.execute(
            "INSERT INTO budget_decisions (account_id, finding_id, status, budget, note, decided_by, decided_at) "
            "VALUES (?,?,?,?,?,?,?) "
            "ON CONFLICT(finding_id) DO UPDATE SET "
            "status=excluded.status, budget=excluded.budget, note=excluded.note, "
            "decided_by=excluded.decided_by, decided_at=excluded.decided_at",
            (account_id, finding_id, status, budget, note, decided_by, _now()),
        )
        conn.commit()


def budget_decisions_for_account(account_id: int) -> Dict[int, Dict]:
    """Mapa finding_id → decisão (com nome de quem decidiu), para a conta."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT b.*, u.name AS decided_by_name FROM budget_decisions b "
            "LEFT JOIN users u ON u.id = b.decided_by WHERE b.account_id=?",
            (account_id,),
        ).fetchall()
    return {r["finding_id"]: dict(r) for r in rows}


# ─── QUOTA (limite de scans por plano) ────────────────────────────────────────────

def count_scans_this_month(account_id: Optional[int]) -> int:
    """Scans iniciados pela CONTA no mês corrente (UTC) — base da quota.

    A quota é do plano, que pertence à conta; contar por conta impede contornar o
    limite criando vários usuários. Sem conta → 0 (o enforcement barra à parte)."""
    if account_id is None:
        return 0
    ym = datetime.now(timezone.utc).strftime("%Y-%m")
    with get_conn() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS n FROM scans WHERE account_id=? AND substr(started_at,1,7)=?",
            (account_id, ym),
        ).fetchone()
    return int(row["n"]) if row else 0


# ─── REVISÃO HUMANA (plano Gerenciado+) ───────────────────────────────────────────

def set_review_status(scan_id: int, status: str, reviewed_by: Optional[int] = None,
                      notes: Optional[str] = None) -> None:
    """Move um scan pela esteira de revisão: none→pending→reviewed→signed."""
    with _LOCK, get_conn() as conn:
        if status in ("reviewed", "signed"):
            conn.execute(
                "UPDATE scans SET review_status=?, reviewed_by=?, reviewed_at=?, review_notes=? WHERE id=?",
                (status, reviewed_by, _now(), notes, scan_id),
            )
        else:
            conn.execute("UPDATE scans SET review_status=? WHERE id=?", (status, scan_id))
        conn.commit()


def review_scan_scoped(scan_id: int, account_id: Optional[int], status: str,
                       reviewed_by: int, notes: Optional[str] = None) -> bool:
    """Atomic tenant-filtered transition; signing requires prior human review."""
    if account_id is None or status not in ("reviewed", "signed"):
        return False
    expected = "pending" if status == "reviewed" else "reviewed"
    with _LOCK, get_conn() as conn:
        changed = conn.execute(
            "UPDATE scans SET review_status=?, reviewed_by=?, reviewed_at=?, review_notes=? "
            "WHERE id=? AND account_id=? AND status='done' AND review_status=?",
            (status, reviewed_by, _now(), notes, scan_id, account_id, expected),
        )
        conn.commit()
        return changed.rowcount == 1


def list_review_queue(limit: int = 50, account_id: Optional[int] = None) -> List[Dict]:
    """Scans aguardando validação humana (mais recentes primeiro)."""
    if account_id is None:
        return []
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM scans WHERE review_status='pending' AND status='done' "
            "AND account_id=? ORDER BY id DESC LIMIT ?",
            (account_id, limit),
        ).fetchall()
    return [dict(r) for r in rows]


# ─── RATE-LIMIT DE LOGIN (compartilhado entre workers — G0-S14) ───────────────────
#
# Usa BEGIN IMMEDIATE para read-modify-write atômico em ambientes multi-worker.
# _RL_LOCK serializa dentro do processo; SQLite serializa entre processos.

def _rl_conn() -> sqlite3.Connection:
    """Conexão em modo autocommit para transações explícitas de rate-limit."""
    conn = sqlite3.connect(config.DB_PATH, timeout=15, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def rl_retry_after(keys: List[str], now: float) -> float:
    """Segundos restantes de bloqueio para qualquer das chaves; 0 se livre."""
    if not keys:
        return 0.0
    ph = ",".join("?" * len(keys))
    with get_conn() as conn:
        rows = conn.execute(
            f"SELECT blocked_until FROM login_attempts WHERE key IN ({ph}) AND blocked_until > ?",
            (*keys, now),
        ).fetchall()
    if not rows:
        return 0.0
    return max(0.0, max(r["blocked_until"] for r in rows) - now)


def rl_record_failure(key: str, limit: int, window_seconds: int, now: float) -> None:
    """Registra uma falha com janela deslizante e bloqueia se o limite for atingido.

    Janela deslizante: timestamps mais antigos que (now - window_seconds) são
    descartados antes de contar, igual ao comportamento original em memória.
    BEGIN IMMEDIATE garante atomicidade entre workers (G0-S14).
    """
    with _RL_LOCK:
        conn = _rl_conn()
        try:
            conn.execute("BEGIN IMMEDIATE")
            r = conn.execute(
                "SELECT ts_json, blocked_until FROM login_attempts WHERE key=?", (key,)
            ).fetchone()
            if r:
                timestamps = json.loads(r["ts_json"] or "[]")
                blocked_until = r["blocked_until"]
            else:
                timestamps, blocked_until = [], 0.0
            # Não estende um bloqueio já ativo (in-flight requests)
            if blocked_until > now:
                conn.execute("COMMIT")
                return
            # Janela deslizante: descarta falhas fora da janela
            cutoff = now - window_seconds
            timestamps = [t for t in timestamps if t > cutoff]
            timestamps.append(now)
            timestamps = timestamps[-limit:]  # limite de memória: guarda só os últimos `limit`
            new_blocked = (now + window_seconds) if len(timestamps) >= limit else blocked_until
            conn.execute(
                "INSERT OR REPLACE INTO login_attempts (key, ts_json, blocked_until) "
                "VALUES (?, ?, ?)",
                (key, json.dumps(timestamps), new_blocked),
            )
            conn.execute("COMMIT")
        except Exception:
            try:
                conn.execute("ROLLBACK")
            except Exception:
                pass
            raise
        finally:
            conn.close()


def rl_clear(key: str) -> None:
    """Remove o registro de tentativas para uma chave (ex: após login bem-sucedido)."""
    with get_conn() as conn:
        conn.execute("DELETE FROM login_attempts WHERE key=?", (key,))
        conn.commit()


def rl_reset() -> None:
    """Apaga todos os registros de tentativas (testes e manutenção)."""
    with get_conn() as conn:
        conn.execute("DELETE FROM login_attempts")
        conn.commit()


# ─── AUDIT ───────────────────────────────────────────────────────────────────────

def audit(user_id: Optional[int], action: str, detail: str = "", ip: str = "") -> None:
    try:
        with _LOCK, get_conn() as conn:
            conn.execute(
                "INSERT INTO audit_log (user_id, action, detail, ip, created_at) VALUES (?,?,?,?,?)",
                (user_id, action, detail, ip, _now()),
            )
            conn.commit()
    except Exception as e:  # auditoria nunca deve derrubar a requisição
        logger.warning("[db] falha ao auditar '%s': %s", action, e)
