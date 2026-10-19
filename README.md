<div align="center">

# ASTRO Cyber

**Plataforma SaaS de segurança ofensiva para PMEs**

Scanner de rede + agente IA que transforma vulnerabilidades em decisões de negócio —
_quanto custa **não** corrigir isto?_

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-stdlib-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Tests](https://img.shields.io/badge/tests-173%20passing-16a34a)](tests/)
[![Security](https://img.shields.io/badge/gate-G0%20completo-16a34a)](#seguranca)

</div>

---

## O que é

ASTRO Cyber é uma plataforma multi-tenant que automatiza o ciclo completo de pentest:
descoberta de hosts → enumeração de serviços → identificação de vulnerabilidades →
remediação assistida por IA → laudo PDF.

A camada de negócio traduz cada achado em **prejuízo estimado × custo de correção**,
para que o dono da PME tome decisões de orçamento sem precisar entender cibersegurança.

---

## Stack

| Camada | Tecnologia |
|---|---|
| Web | Python 3.11+ · Flask 3 · Waitress (WSGI produção) |
| Dados | SQLite (stdlib, sem ORM) · multi-tenant por `account_id` |
| IA | Groq LLM · AEGIS copiloto · fallback offline determinístico |
| Scanner | Go (goroutines + banner grabbing) → Nmap → socket puro Python |
| Segurança | Fernet + PBKDF2-HMAC-SHA256 · rate-limit SQLite · RBAC 5 papéis |
| PDF | fpdf2 |
| Testes | pytest (173 testes) |

---

## Estrutura

```
cymag_saas/
├── app/
│   ├── __init__.py          # application factory
│   ├── config.py            # configuração via ambiente / .env
│   ├── db.py                # SQLite: accounts, users, engagements, scans, findings
│   ├── auth/                # login, sessão, RBAC, rate-limit
│   ├── scans/               # scan, remediação IA, cadeia de ataque
│   ├── autonomous/          # agente autônomo (thread + SSE)
│   ├── engagements/         # escopo autorizado (contrato ético)
│   ├── owner/               # visão de negócio + decisões de orçamento
│   ├── billing/             # planos, assinatura, gating por feature
│   ├── reports/             # PDF (laudo rápido e executivo)
│   └── ai/aegis.py          # integração Groq, cifração da chave, sanitização
├── core/
│   ├── scanner.py           # orquestrador com fallback automático
│   ├── exploit_engine.py    # checks por serviço (HTTP, SMB, Redis, MQTT, MySQL…)
│   ├── business.py          # tradução técnico → custo de negócio
│   ├── plans.py             # catálogo de planos e entitlement
│   └── severity.py          # modelo único de severidade e risco
├── scanner_go/              # scanner de portas em Go (opcional; há fallback Python)
├── static/                  # SPA vanilla (HTML + CSS + JS, sem framework)
├── scripts/
│   ├── start_prod.ps1       # servidor waitress (produção Windows)
│   └── backup.ps1           # VACUUM INTO + integrity_check + retenção 30 dias
├── docs/
│   ├── DEPLOY.md            # guia completo de deploy (waitress, nginx, backup)
│   └── strategy/            # 12 documentos estratégicos (roadmap, mercado, GTM…)
├── tests/                   # suíte pytest — 173 testes
└── run.py                   # entrypoint (desenvolvimento)
```

---

## Como rodar

### Desenvolvimento

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Cria .env em instance/ (ver template abaixo)
python run.py      # http://127.0.0.1:5000
```

### Produção (Windows)

```powershell
# Carrega variáveis e inicia waitress
.\scripts\start_prod.ps1 -Host 127.0.0.1 -Port 8080 -Threads 4
```

Ver [docs/DEPLOY.md](docs/DEPLOY.md) para HTTPS (nginx/Caddy), backup agendado e
configuração do serviço Windows (NSSM).

### Variáveis de ambiente (`instance/.env`)

```env
CYMAG_SECRET_KEY=<string aleatória 64+ chars>   # obrigatório
CYMAG_ENV=production
CYMAG_DB_PATH=C:\caminho\absoluto\instance\cymag.db
CYMAG_SCOPE_ALLOW=192.168.1.0/24,10.0.0.0/8    # CIDRs autorizados para scan
GROQ_API_KEY=                                    # opcional; AEGIS fica offline se vazio
```

```powershell
# Gerar SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"
```

### Testes

```powershell
pytest -q        # 173 testes
```

---

## Segurança

Gate G0 completo — pronto para piloto assistido em ambiente controlado:

| Item | Estado |
|---|---|
| Chave IA cifrada em repouso (Fernet + PBKDF2) | Completo |
| Isolamento de tenant em todos os endpoints IA | Completo |
| Rate-limit de login persistido em SQLite (multi-worker) | Completo |
| Servidor WSGI de produção (waitress) | Completo |
| HTTPS configurado (nginx self-signed / Caddy) | Config pronta em DEPLOY.md |
| Backup automático + verificação de integridade | Script pronto em scripts/ |
| Processo sem permissão elevada | Verificar seção 6 do DEPLOY.md |

Gates G1–G3 (piloto pago → oferta recorrente → self-service) detalhados em
[docs/strategy/SECURITY_RELEASE_GATES.md](docs/strategy/SECURITY_RELEASE_GATES.md).

---

## Ética e escopo

Nenhuma varredura ocorre sem um **Engagement autorizado** que contenha o alvo.
O escopo é aplicado em todas as fases do agente. Use apenas em redes e sistemas
com permissão explícita de teste.

---

<div align="center">

Desenvolvido por **[@alefkaue](https://github.com/alefkaue)**

</div>
