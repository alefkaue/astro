"""Área SMB / Active Directory — signing, EternalBlue, enumeração de shares.

Usa scripts NSE do Nmap quando o binário está disponível; se o Nmap não estiver
instalado, os checks simplesmente não geram findings (degradação silenciosa).
"""

import logging
import re
import subprocess
from typing import Dict, List

from core.checks.base import ScanContext, ServiceCheck, make_finding, register

logger = logging.getLogger("cymag.checks.smb")


@register
class SMBCheck(ServiceCheck):
    name = "smb"
    category = "smb_ad"
    ports = [139, 445]

    def run(self, ctx: ScanContext) -> List[Dict]:
        findings: List[Dict] = []
        host, port, banner = ctx.host, ctx.port, ctx.banner
        nmap_checks = [
            ("signing",     f"nmap -Pn -p {port} --script smb-security-mode {host}"),
            ("eternalblue", f"nmap -Pn -p {port} --script smb-vuln-ms17-010 {host}"),
            ("enum_shares", f"nmap -Pn -p {port} --script smb-enum-shares {host}"),
        ]
        for name, cmd in nmap_checks:
            try:
                r = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=25)
                out = r.stdout.lower()

                if name == "signing" and ("disabled" in out or "not required" in out
                                          or "message_signing: disabled" in out):
                    findings.append(make_finding(
                        "Indicio de assinatura SMB nao obrigatoria",
                        "Saida do script sugere assinatura SMB desabilitada ou nao obrigatoria. Possivel risco de relay; exploracao requer validacao.",
                        "high", 7.5, "CWE-300", evidence=r.stdout[:400], banner=banner,
                        verification_status="suspected", confidence="medium",
                    ))

                if name == "eternalblue" and "ms17-010" in out and re.search(
                        r"(?m)^\s*(?:[|+]\s*)?State:\s*VULNERABLE\s*$", r.stdout, re.IGNORECASE):
                    findings.append(make_finding(
                        "Possivel vulnerabilidade SMB MS17-010",
                        "Script reportou estado VULNERABLE para MS17-010. CVE especifica e execucao remota de codigo requerem validacao.",
                        "high", 8.0, "CVE-2017-0144", evidence=r.stdout[:400], banner=banner,
                        verification_status="suspected", confidence="medium",
                    ))
            except Exception as e:
                logger.debug("[smb] %s: %s", name, e)

        return findings
