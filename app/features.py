"""Deployment gates independent of commercial plan entitlements."""
import os
from flask import jsonify, request
from app.config import config


def enabled(feature):
    value = os.environ.get("CYMAG_ENABLE_" + feature.upper())
    if value is not None:
        return value.strip().lower() in ("1", "true", "yes", "on")
    return config.ENV in ("development", "test", "demo")


def init_app(app):
    @app.before_request
    def deployment_gate():
        path = request.path.rstrip("/")
        if path == "/api/exploit_chain":
            return jsonify(error="Recurso indisponivel."), 404
        feature = None
        if path == "/api/account/plan" and request.method != "GET":
            if config.ENV not in ("development", "test", "demo"):
                return jsonify(error="Contratacao requer atendimento comercial."), 403
            feature = "self_billing"
        elif path == "/api/auto_discover":
            if config.ENV not in ("development", "test", "demo"):
                return jsonify(error="Recurso indisponivel."), 404
            feature = "auto_discover"
        elif path.startswith("/api/autonomous/"):
            feature = "autonomous"
        elif path.startswith("/api/admin/ai/") and request.method != "GET":
            feature = "ai"
        if feature and not enabled(feature):
            return jsonify(error="Recurso desabilitado neste ambiente."), 403
