"""Área Acesso Remoto — FTP, SSH, Telnet, VNC, RDP."""

import ftplib
import logging
import re
import subprocess
from typing import Dict, List

from core.checks.base import SOCKET_TIMEOUT, ScanContext, ServiceCheck, make_finding, register

logger = logging.getLogger("cymag.checks.remote")


@register
class FTPCheck(ServiceCheck):
    name = "ftp"
    category = "remote_access"
    ports = [21]

    def run(self, ctx: ScanContext) -> List[Dict]:
        try:
            ftp = ftplib.FTP()
            ftp.connect(ctx.host, ctx.port, timeout=SOCKET_TIMEOUT)
            raw = ftp.getwelcome()
            ftp.login("anonymous", "cymag@probe.local")
            files: List[str] = []
            try:
                ftp.retrlines("LIST", files.append)
            except Exception:
                pass
            ftp.quit()
            return [make_finding(
                "FTP Login Anônimo Permitido",
                f"Servidor FTP aceita login anônimo. {len(files)} entrada(s) listada(s) no diretório raiz.",
                "high", 7.5, "CWE-306",
                verification_status="confirmed", confidence="high",
                evidence=f"Banner: {raw}\nArquivos:\n" + "\n".join(files[:10]), banner=raw,
            )]
        except ftplib.error_perm:
            pass  # Auth requerida — não vulnerável
        except Exception as e:
            logger.debug("[ftp] %s:%d: %s", ctx.host, ctx.port, e)
        return []


@register
class SSHCheck(ServiceCheck):
    name = "ssh"
    category = "remote_access"
    ports = [22]

    def run(self, ctx: ScanContext) -> List[Dict]:
        raw = ctx.read_banner() or ctx.banner
        if not raw:
            return []
        old_patterns = ["openssh_1.", "openssh_2.", "openssh_3.", "openssh_4.",
                        "openssh_5.", "openssh_6.", "ssh-1."]
        if any(pat in raw.lower() for pat in old_patterns):
            return [make_finding(
                "Indicio de versao SSH antiga no banner",
                "Banner sugere versao SSH antiga. Versao, correcoes e aplicabilidade de CVEs requerem validacao.",
                "med", 5.0, "", evidence=raw[:200], banner=raw,
            )]
        return []


@register
class TelnetCheck(ServiceCheck):
    name = "telnet"
    category = "remote_access"
    ports = [23]

    def run(self, ctx: ScanContext) -> List[Dict]:
        raw = ctx.read_banner(timeout=3) or ctx.banner
        return [make_finding(
            "Possivel servico Telnet - requer validacao",
            "Porta associada a Telnet acessivel. Protocolo requer validacao; se confirmado, Telnet transmite dados sem criptografia.",
            "low", 3.0, "CWE-319",
            verification_status="suspected", confidence="low",
            evidence=raw[:200] if raw else "Porta 23 aberta", banner=raw or "",
        )]


@register
class VNCCheck(ServiceCheck):
    name = "vnc"
    category = "remote_access"
    ports = [5900]

    def run(self, ctx: ScanContext) -> List[Dict]:
        raw = ctx.read_banner() or ctx.banner
        if raw and "rfb" in raw.lower():
            return [make_finding(
                "Indicio de servico VNC no banner",
                "Banner indica RFB (VNC). Nao comprova ausencia de senha nem acesso a area de trabalho; autenticacao requer validacao.",
                "low", 3.0, "CWE-306", evidence=raw[:200], banner=raw,
                verification_status="observation", confidence="medium",
            )]
        return []


@register
class RDPCheck(ServiceCheck):
    name = "rdp"
    category = "remote_access"
    ports = [3389]

    def run(self, ctx: ScanContext) -> List[Dict]:
        try:
            r = subprocess.run(
                ["nmap", "-Pn", "-p", str(ctx.port), "--script", "rdp-vuln-ms12-020", ctx.host],
                capture_output=True, text=True, timeout=20,
            )
            if re.search(r"(?m)^\s*(?:[|+]\s*)?State:\s*VULNERABLE\s*$", r.stdout, re.IGNORECASE):
                return [make_finding(
                    "Possivel vulnerabilidade RDP MS12-020",
                    "Script reportou estado VULNERABLE para RDP. Aplicabilidade de MS12-020 e impacto requerem validacao.",
                    "high", 7.8, "CVE-2012-0152", evidence=r.stdout[:400], banner=ctx.banner,
                    verification_status="suspected", confidence="medium",
                )]
        except Exception:
            pass
        return []
