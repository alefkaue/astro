"""Legacy SQLite migration, quarantine, idempotence and cold rollback evidence."""
import sqlite3
import uuid
from pathlib import Path

from app import db
from app.config import config
from tools.restore_sqlite import restore


def test_legacy_migration_backup_and_restore(monkeypatch):
    path = Path('instance') / f'migration-{uuid.uuid4().hex}.db'
    monkeypatch.setattr(config, 'DB_PATH', str(path))
    monkeypatch.setattr(config, 'DEMO', False)
    conn = sqlite3.connect(path)
    try:
        conn.executescript(db.SCHEMA)
        conn.execute("INSERT INTO accounts(id,name,created_at) VALUES(1,'A','2026-10-14'),(2,'B','2026-10-14')")
        conn.execute("INSERT INTO users(id,email,name,password_hash,role,account_id,created_at) VALUES(1,'a@test','A','fixture','owner',1,'2026-10-14'),(2,'b@test','B','fixture','owner',2,'2026-10-14')")
        conn.execute("INSERT INTO engagements(id,name,created_by,created_at) VALUES(1,'A scope',1,'2026-10-14'),(2,'Orphan',NULL,'2026-10-14')")
        conn.execute("INSERT INTO scans(id,engagement_id,target,created_by,started_at) VALUES(1,1,'192.0.2.1',1,'2026-10-14'),(2,1,'192.0.2.2',2,'2026-10-14')")
        conn.execute("INSERT INTO findings(scan_id,title,created_at) VALUES(1,'A evidence','2026-10-14'),(2,'Ambiguous','2026-10-14')")
        conn.commit()
    finally:
        conn.close()
    try:
        db.init_db()
        assert db.get_engagement(1, organization_id=1)['name'] == 'A scope'
        assert db.get_engagement(1, organization_id=2) is None
        with db.get_conn() as c:
            assert c.execute('SELECT organization_id FROM engagements WHERE id=2').fetchone()[0] is None
            assert c.execute('SELECT organization_id FROM scans WHERE id=2').fetchone()[0] is None
            assert c.execute('SELECT organization_id FROM findings WHERE scan_id=2').fetchone()[0] is None
            assert c.execute('PRAGMA foreign_key_check').fetchall() == []
        backups = list(path.parent.glob(path.name + '.pre-tenant-*.bak'))
        assert len(backups) == 1
        db.init_db()
        with db.get_conn() as c:
            assert c.execute('SELECT COUNT(*) FROM memberships').fetchone()[0] == 2
            assert c.execute('SELECT COUNT(*) FROM findings').fetchone()[0] == 2
            # A later user reassignment cannot silently attach quarantined data.
            c.execute('UPDATE engagements SET created_by=1 WHERE id=2')
        db.init_db()
        with db.get_conn() as c:
            assert c.execute('SELECT organization_id FROM engagements WHERE id=2').fetchone()[0] is None
        assert len(list(path.parent.glob(path.name + '.pre-tenant-*.bak'))) == 1
        restore(backups[0], path)
        with db.get_conn() as c:
            assert c.execute("SELECT 1 FROM sqlite_master WHERE name='organizations'").fetchone() is None
            assert c.execute('SELECT COUNT(*) FROM findings').fetchone()[0] == 2
            assert c.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    finally:
        for p in path.parent.glob(path.name + '*'):
            p.unlink()
