# DECISIONS — decisões técnicas e justificativas

## D-001 — Manter SQLite nesta fase; preparar tenant como 1ª classe
Migrar para PostgreSQL (OPS-001) é P1. Antes disso, a correção de isolamento
não exige troca de banco. Decisão: adicionar `account_id` a `engagements`/`scans`
via migração forward-only idempotente no próprio SQLite e filtrar toda query por
`(account_id, id)`. Rollback: colunas novas são nullable; código antigo ignora.

## D-002 — Autorização filtra na query, não `get(id)` + checagem opcional
Padrão OWASP (BOLA): toda leitura/escrita de recurso de cliente passa a resolver
pelo par `(account_id_do_usuário, resource_id)`. Recurso de outro tenant → 404
(não 403) para não revelar existência.

## D-003 — Papel revalidado no banco
`is_staff`/role continuam disponíveis em sessão para UX, mas as checagens
sensíveis usam o usuário ativo do banco (`current_user()`), não apenas
`session['role']`. Usuário desativado/sem conta → negado.

## D-004 — Relatórios montados no backend (SEC-006)
`POST /api/report/*` passará a receber `scan_id` autorizado e montar o laudo a
partir dos findings persistidos do tenant, não de payload do cliente. Demo recebe
selo "DADOS FICTÍCIOS". (A implementar após SEC-002/003.)

## D-005 — Estratégia de marca CYMAG→ASTRO adiada para depois do P0
Nenhum identificador interno/tabela/rota renomeado agora (evita quebra). Rebrand
público é P2 (ver plano). Nesta etapa só segurança defensiva.
