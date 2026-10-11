# TASKS — Coordenação Claude Code + Codex

> Backlog vivo. Prioridade P0 (segurança) → P1 (confiança) → P2 (produto).
> Regras: um arquivo = um dono por vez. Sem commit/push sem autorização do fundador.

## Legenda
- 🔵 Claude Code (arquitetura, segurança, authz, integração)
- 🟢 Codex (motores, honestidade de detecção, testes, refactor independente)
- Estados: `todo` · `doing` · `review` · `done` · `blocked`

## Sprint atual — Fase 0/1 (segurança defensiva)

| ID | Tarefa | Dono | Arquivos | Estado | Dep. |
|----|--------|------|----------|--------|------|
| SEC-001 | Baseline + auditoria + branch + docs | 🔵 | `docs/**` | done | — |
| SEC-002 | Isolamento multi-tenant (account_id em engagements/scans) + migração | 🔵 | `app/db.py` | **done** | SEC-001 |
| SEC-003 | Correção IDOR/BOLA em todas as rotas (scans, findings, engagements, autonomous) | 🔵 | `app/scope.py`, `app/*/routes.py`, `app/auth/decorators.py` | **done** | SEC-002 |
| SEC-004 | Testes adversariais A/B (dois tenants) | 🔵 | `tests/test_tenant_isolation.py` | **done** (11 testes) | SEC-002/003 |
| SEC-005 | Seed fail-closed: produção não semeia demo; secret key obrigatória | 🔵 | `app/config.py`, `app/db.py` | **done** | SEC-001 |
| SEC-006 | Relatórios a partir de dados do backend (scan_id, não payload do cliente) + selo DEMO | 🔵 | `app/reports/*`, `static/cymag.js` | **done** (4 testes) | SEC-002 |
| DET-001 | Honestidade de impacto financeiro: rotular estimativa, sem "garantido" | 🟢→🔵 | `core/business.py`, `tests/test_business.py` | **done** (feito por Claude — Codex bloqueado, ver abaixo) | — |
| DET-002 | Reclassificar achados fracos como observação/suspeita (não "confirmado") | 🟢 | `core/checks/*`, `tests/test_checks_honesty.py` | **done** (Codex, 18 testes, revisado por Claude) | DET-001 |
| A9/A11/A12 | X-Forwarded-For confiável, chave IA em texto puro, quota por conta | 🔵 | auth/aegis/billing | parcial (quota feita) | — |

## ✅ Status do Codex — RESOLVIDO
A execução autônoma falhava porque `~/.codex/config.toml` tinha `[windows] sandbox = "elevated"`,
modo que o `codex.exe` não consegue lançar nesta máquina. Corrigido para `unelevated`
(backup em `config.toml.bak`). Agora `codex exec -s workspace-write` roda normalmente.
Codex executou **DET-002** (reclassificação de achados em `core/checks/`) — ver CHANGELOG.
Invocação usada pelo Claude:
`codex exec -s workspace-write -c 'windows.sandbox="unelevated"' -C <repo> - < tarefa.md`

## Entregue
- SEC-001..005 + DET-001 — ver `docs/audit/2026-10-baseline.md` e `CHANGELOG_AGENTS.md`. 70 testes passam.
