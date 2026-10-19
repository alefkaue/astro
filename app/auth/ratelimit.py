"""Login rate-limiting backed by SQLite (G0-S14).

State persists across restarts and is shared between workers.
Each worker serialises its own writes with _RL_LOCK (db.py); SQLite
serialises across workers via BEGIN IMMEDIATE.

The injectable `clock` parameter keeps all existing time-based tests working.
"""

import math
import os
import time as _time

MAX_FAILS_EMAIL = max(1, int(os.getenv("CYMAG_LOGIN_MAX_FAILS_EMAIL", "5")))
MAX_FAILS_IP = max(1, int(os.getenv("CYMAG_LOGIN_MAX_FAILS_IP", "20")))
WINDOW_SECONDS = max(1, int(os.getenv("CYMAG_LOGIN_WINDOW_SECONDS", "900")))


class LoginRateLimiter:
    def __init__(self, max_fails_email=MAX_FAILS_EMAIL, max_fails_ip=MAX_FAILS_IP,
                 window_seconds=WINDOW_SECONDS, clock=_time.monotonic, **_ignored):
        if min(max_fails_email, max_fails_ip, window_seconds) <= 0:
            raise ValueError("Login limits must be positive")
        self.max_fails_email = max_fails_email
        self.max_fails_ip = max_fails_ip
        self.window_seconds = window_seconds
        self.clock = clock

    def _email_key(self, email: str) -> str:
        return "email:" + email.strip().lower()

    def _ip_key(self, ip: str) -> str:
        return "ip:" + ip

    def retry_after(self, email: str, ip: str) -> int:
        from app import db
        now = self.clock()
        keys = [self._email_key(email), self._ip_key(ip)]
        secs = db.rl_retry_after(keys, now)
        return max(0, math.ceil(secs))

    def record_failure(self, email: str, ip: str) -> None:
        from app import db
        now = self.clock()
        db.rl_record_failure(self._email_key(email), self.max_fails_email,
                             self.window_seconds, now)
        db.rl_record_failure(self._ip_key(ip), self.max_fails_ip,
                             self.window_seconds, now)

    def clear_email(self, email: str) -> None:
        from app import db
        db.rl_clear(self._email_key(email))

    def reset(self) -> None:
        from app import db
        db.rl_reset()


limiter = LoginRateLimiter()


def reset() -> None:
    """Clear all rate-limit state (tests and maintenance)."""
    limiter.reset()
