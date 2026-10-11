"""Área IoT / OT / SCADA — brokers MQTT e painéis Node-RED."""

from typing import Dict, List

import requests

from core.checks.base import HTTP_TIMEOUT, ScanContext, ServiceCheck, make_finding, register
from core.mqtt_explorer import MQTTExplorer

requests.packages.urllib3.disable_warnings()


@register
class MQTTCheck(ServiceCheck):
    name = "mqtt"
    category = "iot_ot"
    ports = [1883, 8883, 9001]

    def run(self, ctx: ScanContext) -> List[Dict]:
        data = MQTTExplorer(ctx.host, ctx.port, capture_secs=7).explore()
        if not data["anonymous_access"]:
            return []

        if data["exploit_evidence"]:
            evidence = "\n".join(data["exploit_evidence"])
        elif data["topics_captured"]:
            sample = data["topics_captured"][:8]
            evidence = f"Tópicos capturados: {', '.join(sample)}"
            if data["broker_info"]:
                bi = data["broker_info"]
                evidence += f"\nBroker: {bi.get('version','?')} | Clientes: {bi.get('clients/connected','?')}"
        else:
            evidence = "Conexão anônima aceita pelo broker."

        return [make_finding(
            "Broker MQTT Sem Autenticação",
            data["description"], data["severity"], data["cvss"], "CWE-306",
            evidence=evidence, banner=ctx.banner, extra={"mqtt_data": data},
            verification_status="confirmed", confidence="high",
        )]


@register
class NodeREDCheck(ServiceCheck):
    name = "nodered"
    category = "iot_ot"
    ports = [1880]

    def run(self, ctx: ScanContext) -> List[Dict]:
        host, port, banner = ctx.host, ctx.port, ctx.banner
        endpoints = [
            ("/settings", "settings JSON"),
            ("/flows", "lista de flows"),
            ("/nodes", "lista de nodes"),
        ]
        strategies = [
            (name, lambda url=f"http://{host}:{port}{path}": requests.get(url, timeout=HTTP_TIMEOUT))
            for path, name in endpoints
        ]
        resp, used = ctx.chain.run(strategies)
        if resp is None or resp.status_code != 200:
            return []

        extra = ""
        if "flows" in used:
            try:
                extra = f" {len(resp.json())} fluxo(s) mapeado(s)."
            except Exception:
                pass

        return [make_finding(
            "Possivel endpoint Node-RED acessivel",
            f"Endpoint candidato Node-RED ({used}) respondeu HTTP 200.{extra} Identidade do servico e acesso sem autenticacao requerem validacao.",
            "low", 3.0, "CWE-306", evidence=resp.text[:400], banner=banner,
            verification_status="observation", confidence="low",
        )]
