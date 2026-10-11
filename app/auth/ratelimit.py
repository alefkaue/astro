"""Process-local login failure limits (each worker has its own state)."""

import math
import os
import threading
import time
from collections import OrderedDict, deque
from dataclasses import dataclass, field


MAX_FAILS_EMAIL = max(1, int(os.getenv("CYMAG_LOGIN_MAX_FAILS_EMAIL", "5")))
MAX_FAILS_IP = max(1, int(os.getenv("CYMAG_LOGIN_MAX_FAILS_IP", "20")))
WINDOW_SECONDS = max(1, int(os.getenv("CYMAG_LOGIN_WINDOW_SECONDS", "900")))


@dataclass
class _Entry:
    failures: deque = field(default_factory=deque)
    blocked_until: float = 0


class LoginRateLimiter:
    def __init__(self, max_fails_email=MAX_FAILS_EMAIL, max_fails_ip=MAX_FAILS_IP,
                 window_seconds=WINDOW_SECONDS, clock=time.monotonic, max_keys=10000):
        if min(max_fails_email, max_fails_ip, window_seconds, max_keys) <= 0:
            raise ValueError("Login limits must be positive")
        self.max_fails_email = max_fails_email
        self.max_fails_ip = max_fails_ip
        self.window_seconds = window_seconds
        self.clock = clock
        self.max_keys = max_keys
        self._entries = OrderedDict()
        self._lock = threading.Lock()

    def _prune(self, now):
        for key, entry in list(self._entries.items()):
            while entry.failures and entry.failures[0] <= now - self.window_seconds:
                entry.failures.popleft()
            if entry.blocked_until <= now and not entry.failures:
                del self._entries[key]

    def retry_after(self, email, ip):
        with self._lock:
            now = self.clock()
            self._prune(now)
            remaining = max((self._entries[key].blocked_until - now
                             for key in (("email", email.strip().lower()), ("ip", ip))
                             if key in self._entries), default=0)
            return max(0, math.ceil(remaining))

    def record_failure(self, email, ip):
        with self._lock:
            now = self.clock()
            self._prune(now)
            for key, limit in ((("email", email.strip().lower()), self.max_fails_email),
                               (("ip", ip), self.max_fails_ip)):
                entry = self._entries.get(key)
                if entry is None:
                    while len(self._entries) >= self.max_keys:
                        self._entries.popitem(last=False)
                    entry = self._entries[key] = _Entry()
                self._entries.move_to_end(key)
                # Requests already in flight must not extend an existing block.
                if entry.blocked_until > now:
                    continue
                entry.failures.append(now)
                if len(entry.failures) >= limit:
                    entry.blocked_until = now + self.window_seconds

    def clear_email(self, email):
        with self._lock:
            self._entries.pop(("email", email.strip().lower()), None)

    def reset(self):
        with self._lock:
            self._entries.clear()


limiter = LoginRateLimiter()


def reset():
    """Clear the shared limiter between tests."""
    limiter.reset()
