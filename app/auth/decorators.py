"""Decorators e helpers de autorização (papéis + planos/entitlements)."""

import functools

from flask import jsonify, request, session

from app import db
from core import plans


def current_user():
    uid = session.get("uid")
    if not uid:
        return None
    return db.get_user(uid)


def current_account_id():
    """account_id (tenant) do usuário logado, revalidado no banco. None se sem conta.

    É a chave de isolamento multiempresa: toda query de recurso de cliente filtra
    por este valor. Lê do banco (não da sessão) para refletir remoção/alteração."""
    user = current_user()
    if not user or "account_id" not in user.keys():
        return None
    return user["account_id"]


def current_plan():
    """Plano EFETIVO do usuário logado = o plano da sua conta (a empresa que contrata)."""
    uid = session.get("uid")
    if not uid:
        return plans.get_plan(None)
    return plans.get_plan(db.plan_key_for_user(uid))


def is_staff() -> bool:
    """True se o usuário logado é da equipe CYMAG. Revalida o papel no banco."""
    user = current_user()
    return bool(user) and user["role"] in db.STAFF_ROLES


def requires_feature(feature: str):
    """Bloqueia a rota se o plano do usuário não incluir a feature (HTTP 402)."""
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            if not session.get("uid"):
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
        if not uid:
            return jsonify({"error": "Não autenticado"}), 401
        limit = current_plan().scans_per_month
        if limit is not None:
            used = db.count_scans_this_month(current_account_id())
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
        if not session.get("uid"):
            return jsonify({"error": "Não autenticado"}), 401
        return fn(*args, **kwargs)
    return wrapper


def role_required(*roles):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            # Revalida o papel no banco (não confia só na sessão): usuário removido
            # ou desativado, ou com papel alterado, é barrado na hora.
            user = current_user()
            if not user:
                return jsonify({"error": "Não autenticado"}), 401
            role = user["role"]
            if role not in roles and role != "admin":
                return jsonify({"error": "Acesso negado para o seu perfil"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def client_ip() -> str:
    return request.headers.get("X-Forwarded-For", request.remote_addr or "").split(",")[0].strip()
