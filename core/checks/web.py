"""Área Web / OWASP — checagens sobre HTTP/HTTPS."""

from typing import Dict, List

import requests

from core.checks.base import HTTP_TIMEOUT, ScanContext, ServiceCheck, make_finding, register

requests.packages.urllib3.disable_warnings()


@register
class HTTPCheck(ServiceCheck):
    name = "http"
    category = "web"
    ports = [80, 443, 8080, 8443]

    def run(self, ctx: ScanContext) -> List[Dict]:
        findings: List[Dict] = []
        host, port, banner = ctx.host, ctx.port, ctx.banner
        scheme = "https" if port in (443, 8443) else "http"
        base = f"{scheme}://{host}:{port}"

        findings += self._sqli(ctx, base, banner)
        findings += self._traversal(base, banner)
        findings += self._sensitive_files(base, banner)
        findings += self._default_creds(base, banner)
        return findings

    def _sqli(self, ctx, base, banner) -> List[Dict]:
        candidates = [
            "/api/collaborators?name='", "/api/users?id=1'", "/search?q='",
            "/?id=1'--", "/index.php?id=1'", "/products?category=1'",
        ]
        strategies = [
            (path, lambda p=path: requests.get(
                base + p, timeout=HTTP_TIMEOUT, verify=False, allow_redirects=False))
            for path in candidates
        ]
        resp, used_path = ctx.chain.run(strategies)
        if resp is None:
            return []
        body = resp.text.lower()
        if any(kw in body for kw in ["sql", "syntax error", "mysql", "ora-",
                                     "pg_", "sqlite", "odbc", "unclosed quotation"]):
            return [make_finding(
                "Possivel SQL Injection - indicio em resposta HTTP",
                f"Endpoint {used_path!r} retornou texto relacionado a SQL. SQLi exploravel requer validacao.",
                "med", 5.0, "CWE-89", evidence=resp.text[:300], banner=banner,
                verification_status="suspected", confidence="low",
            )]
        return []

    def _traversal(self, base, banner) -> List[Dict]:
        for path in ["/../../etc/passwd", "/../etc/passwd", "/etc/passwd",
                     "/api/../../../../etc/passwd"]:
            try:
                r = requests.get(base + path, timeout=HTTP_TIMEOUT, verify=False)
                if "root:" in r.text and "nologin" in r.text:
                    return [make_finding(
                        "Possivel exposicao de /etc/passwd",
                        "Resposta contem padroes de /etc/passwd. Origem e leitura arbitraria via traversal requerem validacao.",
                        "high", 7.5, "CWE-22", evidence=r.text[:200], banner=banner,
                        verification_status="suspected", confidence="medium",
                    )]
            except Exception:
                pass
        return []

    def _sensitive_files(self, base, banner) -> List[Dict]:
        findings: List[Dict] = []
        sensitive = [
            "/.env", "/.env.local", "/.env.production",
            "/config.php", "/wp-config.php", "/config.yml", "/config.yaml",
            "/.git/config", "/.git/HEAD",
            "/backup.zip", "/backup.sql", "/db.sql", "/dump.sql",
            "/phpinfo.php", "/info.php", "/server-status", "/server-info",
        ]
        for path in sensitive:
            try:
                r = requests.get(base + path, timeout=HTTP_TIMEOUT, verify=False)
                if r.status_code == 200 and len(r.text) > 20:
                    findings.append(make_finding(
                        f"Possivel arquivo sensivel: {path}",
                        "HTTP 200 no caminho de configuracao/backup. Pode ser pagina generica; exposicao requer validacao.",
                        "low", 3.0, "CWE-200", evidence=r.text[:300], banner=banner,
                        verification_status="observation", confidence="low",
                    ))
            except Exception:
                pass
        return findings

    def _default_creds(self, base, banner) -> List[Dict]:
        findings: List[Dict] = []
        admin_panels = [
            ("/admin",        [("admin", "admin"), ("admin", "password"), ("admin", "123456")]),
            ("/manager/html", [("tomcat", "tomcat"), ("tomcat", "s3cret"), ("admin", "admin")]),
            ("/wp-login.php", [("admin", "admin"), ("wordpress", "wordpress")]),
            ("/login",        [("admin", "admin"), ("root", "root"), ("admin", "password")]),
            ("/phpmyadmin/",  [("root", ""), ("root", "root"), ("admin", "admin")]),
        ]
        for path, creds in admin_panels:
            try:
                r = requests.get(base + path, timeout=HTTP_TIMEOUT, verify=False)
                if r.status_code != 200:
                    continue
                rl = r.text.lower()
                if not any(kw in rl for kw in ["login", "password", "username", "sign in", "entrar"]):
                    continue
                for user, passwd in creds:
                    try:
                        r2 = requests.post(
                            base + path,
                            data={"username": user, "password": passwd,
                                  "user": user, "pass": passwd, "log": user, "pwd": passwd},
                            timeout=HTTP_TIMEOUT, verify=False, allow_redirects=True,
                        )
                        rl2 = r2.text.lower()
                        if any(kw in rl2 for kw in ["dashboard", "logout", "welcome",
                                                    "bienvenido", "painel", "admin"]):
                            findings.append(make_finding(
                                f"Possivel aceitacao de credenciais padrao - {path}",
                                f"Resposta apos tentativa com {user}:{passwd} contem termos de painel em {path}. Sessao autenticada requer validacao.",
                                "med", 5.0, "CWE-798",
                                verification_status="suspected", confidence="low",
                                evidence=f"POST {base}{path} com {user}:{passwd} → HTTP {r2.status_code}",
                                banner=banner,
                            ))
                            break
                    except Exception:
                        pass
            except Exception:
                pass
        return findings
