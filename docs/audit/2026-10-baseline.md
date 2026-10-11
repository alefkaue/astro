# Baseline de auditoria — 2026-10-10

> Auditoria somente-leitura do checkout real (branch `main`), confrontada com as hipóteses
> do `ASTRO_02_CLAUDE_CODE_PLANO_TECNICO.md`. Achados exigem confirmação por testes locais;
> nenhuma varredura foi executada contra terceiros.

## Ambiente verificado
- Python 3.14.6 (venv local `.venv/`). Go presente (`scanner_go/`, não compilado).
- Deps: Flask 3.1.3, Werkzeug 3.1.9, groq 1.7.0, fpdf2 2.8.9, requests 2.34.2, pytest 9.1.1.
- `pytest`: **55 passed** em ~1.8s (puros: escopo, severidade, planos, billing, sanitize, business, aegis_config). Nenhum teste de autorização cruzada.
- Git limpo em `main`; branch de trabalho `seguranca/p0-tenant-isolation`.

## Arquitetura (resumo)
- App factory Flask (`app/__init__.py`) + blueprints: auth, scans, engagements, autonomous, owner, billing, reports, admin, main.
- Persistência: SQLite stdlib (`app/db.py`), sem ORM. Tabelas: accounts, users, engagements, scans, findings, audit_log, budget_decisions.
- Sessão Flask (cookie). Papéis em `session['role']`. Planos/entitlements em `core/plans.py`.
- IA "AEGIS" (`app/ai/aegis.py`) via Groq; fallback offline determinístico.
- Scanner em `core/` + `scanner_go/`. **Componente de teste ativo** — nesta etapa apenas documentado; sem alterações ofensivas.

## Achados P0 (confirmados no código)

| # | Severidade | Local | Problema |
|---|-----------|-------|----------|
| A1 | **Crítico** | `app/db.py` (schema) | `engagements`/`scans` **não têm `account_id`**. Propriedade do tenant é inferida por `scan.created_by → user.account_id` (frágil, quebra para recursos de outros usuários do mesmo tenant). |
| A2 | **Crítico (IDOR)** | `app/scans/routes.py:228` | `GET /api/scans/<id>/findings` **não verifica dono** — qualquer usuário autenticado lê achados de qualquer scan. |
| A3 | **Crítico (BOLA)** | `app/engagements/routes.py:28,56` | `GET /api/engagements` lista **todos** os engagements globalmente; `GET /api/engagements/<id>` devolve qualquer um, sem filtro de tenant. |
| A4 | **Crítico** | `app/scope.py:33` | `resolve_authorized_target` valida escopo mas **não vincula o engagement ao tenant/usuário** — tenant A pode disparar scan usando engagement autorizado do tenant B. |
| A5 | **Alto (IDOR)** | `app/autonomous/routes.py:88` | `GET /api/autonomous/<run_id>` devolve run de qualquer usuário (sem checagem de dono). |
| A6 | **Alto** | `app/db.py:_seed_users`, `app/config.py:52` | Seeds de demo em **todo boot**, inclusive produção; senha admin padrão `cymag-admin`; senhas demo fixas publicadas no README. |
| A7 | **Alto** | `app/config.py:55` | `resolve_secret_key` gera/persiste chave silenciosamente; produção **não falha** sem `CYMAG_SECRET_KEY`. |
| A8 | **Alto** | `app/reports/routes.py:31,60` | `POST /api/report/*` monta PDF a partir de **findings arbitrários do cliente**; sem proveniência, sem selo DEMO/DADOS FICTÍCIOS. |
| A9 | Médio | `app/auth/decorators.py:93` | `client_ip()` confia em `X-Forwarded-For` sem proxy confiável (spoof de IP em auditoria/futuro rate-limit). |
| A10 | Médio | `app/auth/decorators.py:83` | `role_required` e `is_staff` confiam em `session['role']` (cópia do login); sem revalidação contra o banco a cada request (role pode ficar obsoleto após mudança/desativação). |
| A11 | Médio | `app/ai/aegis.py:214` | Chave de API persistida em texto puro em `instance/ai_config.json`. |
| A12 | Médio | `app/auth/decorators.py:51` | Quota de scans contada **por usuário**, mas o plano é **da conta** — contorna limite com múltiplos usuários. |

## Achados P1 (confiança/honestidade) — delegados ao Codex
- `core/business.py`: faixas financeiras fixas em R$ apresentadas de forma categórica; precisam ser opt-in, rotuladas como estimativa, sem "garantido".
- `app/ai/aegis.py` prompts (`AEGIS_EXEC`) induzem valores financeiros/CVE inventados.
- `core/checks/*`: inferências fracas tratadas como vulnerabilidade confirmada (ver DET-002).

## Plano P0 (ordem)
SEC-002 (tenant como 1ª classe) → SEC-003 (filtro em toda rota) → SEC-004 (testes A/B) → SEC-005 (seed fail-closed) → SEC-006 (relatórios do backend). Cada um com teste de regressão.
