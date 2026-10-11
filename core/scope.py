"""
Regras puras de escopo — o contrato ético do CYMAG, sem dependência de framework.

Estas funções não conhecem Flask nem o banco: apenas decidem se um alvo está
dentro de um escopo autorizado (lista de IPs/CIDRs). A camada web (app/scope.py)
reusa isto e adiciona a resolução do Engagement via banco.

Manter a lógica de contenção aqui permite que TANTO o scan manual QUANTO o motor
autônomo filtrem hosts pela mesma regra — a autorização não pode ser contornada
por uma rota que "esqueceu" de validar.
"""

import ipaddress
import os
from typing import List, Tuple

MAX_CANDIDATES = 64
_FORBIDDEN = tuple(ipaddress.ip_network(n) for n in (
    "0.0.0.0/8", "127.0.0.0/8", "169.254.0.0/16", "224.0.0.0/4", "240.0.0.0/4"))


def candidate_count(target: str) -> int:
    net = ipaddress.ip_network(str(target), strict=False)
    if net.version != 4:
        raise ValueError("IPv6 execution is not supported.")
    return net.num_addresses if net.prefixlen >= 31 else net.num_addresses - 2


def _policy_networks(name: str):
    return [ipaddress.ip_network(entry.strip(), strict=False)
            for entry in os.environ.get(name, "").split(",") if entry.strip()]


def assert_safe_target(target: str, hosted=None):
    """Validate execution policy before any probe; never expand large networks."""
    net = ipaddress.ip_network(str(target), strict=False)
    if net.version != 4:
        raise ValueError("IPv6 execution is not supported.")
    if candidate_count(target) > MAX_CANDIDATES:
        raise ValueError("Target exceeds the 64 candidate execution limit; select a smaller range.")
    denied = _FORBIDDEN + tuple(_policy_networks("CYMAG_SCOPE_DENY"))
    if any(net.version == block.version and net.overlaps(block) for block in denied):
        raise ValueError("Target intersects a prohibited network.")
    if hosted is None:
        hosted = os.environ.get("CYMAG_ENV", "development").lower() not in ("development", "test", "demo")
    if hosted:
        allowed = _policy_networks("CYMAG_SCOPE_ALLOW")
        if not any(net.version == block.version and net.subnet_of(block) for block in allowed):
            raise ValueError("Target is outside the deployment allowlist.")


def safe_host(host):
    try:
        if ipaddress.ip_network(str(host), strict=False).prefixlen != 32:
            return False
        assert_safe_target(host)
        return True
    except (ValueError, TypeError):
        return False


def valid_scope(scope: list) -> Tuple[bool, str]:
    """Valida que cada entrada do escopo é um IP ou CIDR válido."""
    if not isinstance(scope, list) or not scope:
        return False, "Escopo deve ser uma lista não vazia de IPs/CIDRs."
    for entry in scope:
        try:
            ipaddress.ip_network(str(entry), strict=False)
        except ValueError:
            return False, f"Entrada de escopo inválida: {entry}"
    return True, ""


def target_in_scope(target: str, scope: list) -> bool:
    """True se `target` (IP ou CIDR) estiver contido em alguma faixa do escopo."""
    try:
        tnet = ipaddress.ip_network(str(target), strict=False)
    except ValueError:
        return False
    for entry in scope:
        try:
            if tnet.subnet_of(ipaddress.ip_network(str(entry), strict=False)):
                return True
        except (ValueError, TypeError):
            continue
    return False


def hosts_in_scope(hosts: List[str], scope: list) -> List[str]:
    """Filtra uma lista de hosts, mantendo só os que estão dentro do escopo.

    Usada como segunda barreira: mesmo depois de o alvo ser validado, os hosts
    efetivamente *descobertos* na fase de recon são re-filtrados, para que um
    resultado inesperado do Nmap nunca leve o motor a tocar algo fora do escopo.
    Escopo vazio ainda aplica a politica de seguranca de execucao.
    """
    if not scope:
        return [h for h in hosts if safe_host(h)]
    return [h for h in hosts if safe_host(h) and target_in_scope(h, scope)]
