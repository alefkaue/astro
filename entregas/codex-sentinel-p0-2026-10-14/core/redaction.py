"""Conservative recursive secret removal for persisted scanner evidence."""
import re

_SECRET_KEYS = {'password', 'passwd', 'secret', 'token', 'api_key', 'apikey', 'authorization',
                'cookie', 'set-cookie', 'access_token', 'refresh_token', 'private_key'}
_ASSIGNMENT = re.compile(r'(?i)\b(password|passwd|secret|token|api[_-]?key)\s*[:=]\s*[^\s,;]+')
_BEARER = re.compile(r'(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+')
_CREDENTIAL_URL = re.compile(r'(https?://)[^/\s:@]+:[^/\s@]+@')


def redact(value):
    if isinstance(value, dict):
        return {k: '[REDACTED]' if str(k).lower() in _SECRET_KEYS else redact(v) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    if isinstance(value, str):
        text = _ASSIGNMENT.sub(r'\1=[REDACTED]', value)
        text = _BEARER.sub('Bearer [REDACTED]', text)
        return _CREDENTIAL_URL.sub(r'\1[REDACTED]@', text)
    return value
