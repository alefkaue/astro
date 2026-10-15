"""Decorators e helpers de autorização (papéis + planos/entitlements)."""

import functools

from flask import jsonify, request, session

from app import db
from core import plans

PERMISSIONS = {
    'owner': {'scope:write', 'scope:approve', 'scan:execute', 'report:export', 'finding:write', 'billing:manage'},
    'admin': {'scope:write', 'scope:approve', 'scan:execute', 'report:export', 'finding:write', 'billing:manage'},
    'analyst': {'scope:write', 'scan:execute', 'report:export', 'finding:write'},
    'viewer': set(),
}


def has_permission(permission):
    user = current_user()
    membership = db.get_membership(user['id'], user['account_id']) if user else None
    return bool(membership and permission in PERMISSIONS.get(membership['role'], set()))


def current_user():
    uid = session.get("uid")
    if not uid:
        return None
    user = db.get_user(uid)
    if not user or not user['active'] or user['session_version'] != session.get('session_version', 0):
        return None
    return user


def current_plan():
    """Plano EFETIVO do usuário logado = o plano da sua conta (a empresa que contrata)."""
    uid = session.get("uid")
    if not uid:
        return plans.get_plan(None)
    return plans.get_plan(db.plan_key_for_user(uid))


def is_staff() -> bool:
    """True se o usuário logado é da equipe CYMAG (entrega serviços gerenciados)."""
    user = current_user()
    return bool(user and user['role'] in db.STAFF_ROLES)


def requires_feature(feature: str):
    """Bloqueia a rota se o plano do usuário não incluir a feature (HTTP 402)."""
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user():
                return jsonify({"error": "Não autenticado"}), 401
            plan = current_plan()
            if not plan.has(feature):
                return jsonify({
                    "error": f"Recurso indisponível no plano {plan.name}.",
                    "feature": feature,
                    "plano_atual": plan.key,
                    "upgrade_para": plans.min_plan_with(feature),
                }), 402  # Payment Required — sinaliza upsell
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def enforce_scan_quota(fn):
    """Barra a rota se o usuário estourou a quota mensal de scans do plano (HTTP 429)."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        uid = session.get("uid")
        if not current_user():
            return jsonify({"error": "Não autenticado"}), 401
        limit = current_plan().scans_per_month
        if limit is not None:
            used = db.count_scans_this_month(uid)
            if used >= limit:
                return jsonify({
                    "error": f"Limite de {limit} scan(s)/mês do seu plano atingido.",
                    "usado": used, "limite": limit,
                }), 429
        return fn(*args, **kwargs)
    return wrapper


def login_required(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user():
            return jsonify({"error": "Não autenticado"}), 401
        return fn(*args, **kwargs)
    return wrapper


def role_required(*roles):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            user = current_user()
            if not user:
                return jsonify({"error": "Não autenticado"}), 401
            if user['role'] not in roles:
                return jsonify({"error": "Acesso negado para o seu perfil"}), 403
            if user['role'] == 'owner':
                membership = db.get_membership(user['id'], user['account_id'])
                if not membership or membership['role'] != 'owner':
                    return jsonify({'error': 'Papel organizacional insuficiente'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def client_ip() -> str:
    return request.remote_addr or ''


def permission_required(permission):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            user = current_user()
            if not user:
                return jsonify({'error': 'Não autenticado'}), 401
            if not has_permission(permission):
                return jsonify({'error': 'Permissão insuficiente'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
