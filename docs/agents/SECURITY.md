# SECURITY — problemas e status das correções

Fonte dos achados: `docs/audit/2026-10-baseline.md`. OWASP ASVS v5 / API Top 10 (BOLA).

| # | Achado | OWASP | Status | Correção |
|---|--------|-------|--------|----------|
| A1 | Sem account_id em engagements/scans | API1 | DONE | SEC-002 migração |
| A2 | IDOR findings | API1 | DONE | SEC-003 filtro por tenant |
| A3 | BOLA listagem/detalhe engagements | API1 | DONE | SEC-003 |
| A4 | Escopo não vinculado ao tenant | API1/API5 | DONE | SEC-003 |
| A5 | IDOR autonomous run | API1 | DONE | SEC-003 |
| A6 | Seed inseguro em produção | ASVS V1/V2 | DONE | SEC-005 |
| A7 | Secret key não fail-closed | ASVS V2 | DONE | SEC-005 |
| A8 | Relatório de payload do cliente | ASVS V5 | DONE | SEC-006 (scan_id + selo DEMO) |
| A9 | X-Forwarded-For confiável | ASVS V1 | todo | hardening |
| A10 | role só da sessão | ASVS V3 | DONE | SEC-003 (current_user) |
| A11 | Chave IA em texto puro | ASVS V6 | todo | P1 secret mgr |
| A12 | Quota por usuário, não conta | lógica | DONE | SEC-003 (por conta) |

Cada correção exige teste de regressão antes de marcar `done`.
