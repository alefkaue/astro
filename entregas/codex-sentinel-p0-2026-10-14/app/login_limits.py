"""Persistent rate limit without logging email addresses or trusting proxy headers."""
import hashlib
import time

from app import db


def allowed(email, ip):
    now = int(time.time())
    keys = [hashlib.sha256(value.encode()).hexdigest() for value in ('email:' + email, 'ip:' + ip)]
    with db._LOCK, db.get_conn() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS login_limits (
            bucket TEXT PRIMARY KEY, started INTEGER NOT NULL, count INTEGER NOT NULL)''')
        conn.execute('DELETE FROM login_limits WHERE started < ?', (now - 900,))
        for key in keys:
            row = conn.execute('SELECT count FROM login_limits WHERE bucket=?', (key,)).fetchone()
            if row and row['count'] >= 10:
                return False
        for key in keys:
            conn.execute('''INSERT INTO login_limits VALUES(?,?,1)
                ON CONFLICT(bucket) DO UPDATE SET count=count+1''', (key, now))
    return True
