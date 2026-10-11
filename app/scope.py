"""
Guarda de escopo da camada web — regra única e inescapável para TODA varredura.

Reúsa as regras puras de `core/scope.py` e adiciona a resolução do Engagement
no banco. Qualquer rota que dispare um scan (manual ou autônomo) chama
`resolve_authorized_target()`; assim a autorização vive num só lugar e nenhuma
rota consegue varrer um alvo sem um contrato autorizado que o contenha.
"""

from typing import Dict, Optional, Tuple

from app import db
from app.config import config
from core.plans import get_plan
from core.scope import assert_safe_target, candidate_count
from core.scope import hosts_in_scope, target_in_scope, valid_scope

__all__ = [
    "ScopeError",
    "resolve_authorized_target",
    "target_in_scope",
    "valid_scope",
    "hosts_in_scope",
]


class ScopeError(Exception):
    """Falha de autorização/escopo. `.status` vira o código HTTP na rota."""

    def __init__(self, message: str, status: int = 403):
        super().__init__(message)
        self.message = message
        self.status = status


def resolve_authorized_target(
    account_id: Optional[int], engagement_id: Optional[int], target: str
) -> Tuple[Dict, str]:
    """Valida tenant + Engagement + alvo e devolve (engagement, alvo_resolvido).

    `account_id` é o tenant do usuário que dispara a varredura. O engagement PRECISA
    pertencer a esse tenant — um usuário não pode varrer usando o contrato autorizado
    de outra empresa (BOLA). Engagement de outro tenant responde 404 (não revela
    existência).

    Levanta `ScopeError` (com `.status`) quando:
      - usuário sem conta associada                 → 403
      - falta engagement_id                         → 400
      - engagement não existe OU é de outro tenant  → 404
      - engagement não está 'authorized'            → 403
      - não há alvo nem escopo                       → 400
      - alvo fora do escopo autorizado              → 403

    Se `target` vier vazio, assume a primeira faixa do escopo do engagement.
    """
    if account_id is None:
        raise ScopeError(
            "Usuário sem conta associada não pode disparar varreduras.", 403
        )
    if not engagement_id:
        raise ScopeError(
            "engagement_id é obrigatório: toda varredura exige um contrato autorizado.",
            400,
        )

    eng = db.get_engagement(int(engagement_id), account_id=account_id)
    if not eng:
        raise ScopeError("Engagement não encontrado.", 404)
    if eng.get("status") != "authorized":
        raise ScopeError(
            "Engagement não autorizado. Um admin precisa autorizá-lo antes de qualquer varredura.",
            403,
        )

    scope = eng.get("scope") or []
    target = (target or "").strip()
    if not target:
        target = scope[0] if scope else ""
    if not target:
        raise ScopeError("Sem alvo e sem escopo definido no engagement.", 400)
    if not target_in_scope(target, scope):
        raise ScopeError(
            f"Alvo {target} fora do escopo autorizado do engagement.", 403
        )

    try:
        assert_safe_target(target, hosted=config.ENV not in ("development", "test", "demo"))
    except (ValueError, TypeError):
        raise ScopeError("Alvo proibido, politica invalida ou faixa excede 64 candidatos.", 400)
    account = db.get_account(account_id)
    if not account:
        raise ScopeError("Conta nao encontrada.", 403)
    limit = get_plan(account.get("plan")).max_ips
    if limit is not None and candidate_count(target) > limit:
        raise ScopeError("Alvo excede o limite de IPs do plano.", 403)
    return eng, target
