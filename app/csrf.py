"""
Proteção CSRF para a API JSON (SEC-009a).

A API usa cookie de sessão; várias rotas leem o corpo com `get_json(force=True)`,
que aceitaria um `<form>` text/plain vindo de outro site. Defesa em camadas, sem
token por formulário (o frontend é uma SPA que só fala JSON):

1. Origem: se o navegador enviar `Origin` (ou, na falta dele, `Referer`), ela
   precisa ser a própria origem do app ou estar em CYMAG_TRUSTED_ORIGINS.
2. Formato: requisição mutável em /api/ precisa ser `application/json` ou trazer
   o header `X-Requested-With`. Nenhum dos dois pode ser enviado cross-site sem
   preflight CORS — e o app não responde a CORS.

SameSite=Lax no cookie continua ativo; isto é a segunda barreira.
"""

import logging
import os
from urllib.parse import urlsplit

from flask import jsonify, request

logger = logging.getLogger("cymag.csrf")

UNSAFE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})


def _origin_of(url: str) -> str:
    parts = urlsplit(url or "")
    if not parts.scheme or not parts.netloc:
        return ""
    return f"{parts.scheme}://{parts.netloc}".lower()


def _trusted_origins() -> set:
    extra = os.environ.get("CYMAG_TRUSTED_ORIGINS", "")
    trusted = {_origin_of(o.strip()) for o in extra.split(",") if o.strip()}
    trusted.add(_origin_of(request.host_url))
    trusted.discard("")
    return trusted


def check_request():
    """Devolve uma resposta 403 se a requisição falhar na verificação, senão None."""
    if request.method not in UNSAFE_METHODS or not request.path.startswith("/api/"):
        return None

    origin = request.headers.get("Origin")
    if origin is None and request.headers.get("Referer"):
        origin = _origin_of(request.headers["Referer"])
    if origin is not None:
        # "null" (iframe sandbox, file://) nunca é confiável.
        if _origin_of(origin) not in _trusted_origins():
            logger.warning("CSRF: origem recusada %r em %s %s", origin, request.method, request.path)
            return jsonify({"error": "Origem da requisição não permitida."}), 403

    if not request.is_json and not request.headers.get("X-Requested-With"):
        logger.warning("CSRF: requisição sem JSON/X-Requested-With em %s %s", request.method, request.path)
        return jsonify({"error": "Requisição recusada: formato não permitido."}), 403
    return None


def init_app(app):
    app.before_request(check_request)
