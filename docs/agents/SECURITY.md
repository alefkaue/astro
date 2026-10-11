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

## Revisão nesta sessão ASTRO

Corrigido com regressões: X-Forwarded-For não confiável ignorado; autenticação revalida usuário ativo em todas as gates; usuário sem organização não pode usar rotas login_required; viewer/owner não iniciam scans diretamente; achados legados não tratados como confirmados; despacho de checks intrusivos desativado; candidato CIDR limitado sem alocar rede inteira.

Preservado: isolamento existente e relatórios por scan_id; testes cross-tenant aprovados. Nenhuma varredura contra ativos externos executada nesta sessão. SVGs oficiais inspecionados (paths, viewBox, ausência de script/event handler/referência externa).

Riscos abertos: CSRF/rate limiting, chave IA em JSON, remediação com payload do cliente, RBAC administrativo/delegação, autorização temporal/prova de controle, escopo de egress, redes OT/cloud metadata, concorrência/quota atômica, jobs/eventos em memória, limitação/timeout global, partial/skipped por check, falta de cancelamento e recuperação. Nmap/port scan ainda é operação ativa e não deve ser vendido como passivo. Perfil TCP não substitui uma avaliação de vulnerabilidades.

Não declarar produto pronto para produção ou piloto remunerado com base nestes testes. Fontes de planejamento bancário ficam arquivadas; não entram em rotas ou APIs.

## Atualização 2026-10-11 — pacote de redesign

Integração detalhada e resultados em [REDESIGN.md](REDESIGN.md): navegação por URLs, avaliações com wizard/detalhe, API tenant-scoped, escopos com autorização owner e viewer somente leitura. Implementação por Codex. Claude executado pelo shell terminou exit 1 / ECONNREFUSED, sem alterações. 113 testes Python e contratos frontend passaram. QA visual continua pendente: Edge falhou por acesso negado e exibiu 0x80000003; não contornar proteções do ambiente. Scanner e dados reais preservados nesta etapa.

Revisao PLAN-CLAUDE-01: corrigido vazamento cross-tenant na fila/assinatura de revisoes; login_required e UPDATE atomico tenant/status, regressao tests/test_managed_review_isolation.py. Achado estrangeiro no owner/budget agora 404. Assignments, entitlement managed, bypass admin e CSRF continuam abertos. Detalhes em PRODUCT_PLAN_INTEGRATION.md.
