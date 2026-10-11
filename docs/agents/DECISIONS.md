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

## D-006 — Consolidação incremental, 2026-10-10
Adotar agora identidade ASTRO no frontend funcional Flask. Adaptar padrões de ambos os designs sem executar seus projetos ou importar runtimes SSR. Materiais arquivados não são frontends ativos. Preservar endpoints e lógica real; mapa de origem em DESIGN_MERGE.

## D-007 — Perfil defensivo obrigatório no produto
Checks legados incluem autenticação, payloads e publicação em brokers; não são compatíveis com o perfil solicitado. Despachante passa a registrar apenas observações de serviços TCP. Código legado e testes sintéticos preservados para revisão, sem opção de habilitar via request. Consequência: novas avaliações não anunciam detecção abrangente de vulnerabilidades. Revisão de especialistas e perfis separados exigidos antes de qualquer reativação.

## D-008 — Métricas derivadas, não score de segurança
Dashboard usa histórico do tenant e última avaliação concluída por alvo. Não mostrar inventário total, correções verificadas ou curva de exposição sem modelo/cobertura suficientes. Achados legados não viram confirmados automaticamente.

## D-009 — Claude indisponível nesta execução
Versão/auth/help verificados. Invocação não interativa real com escopo limitado e permissões normais terminou código 1 / ECONNREFUSED / zero tokens. Não contornar rede ou permissões. Codex assumiu a tarefa depois do processo terminar; nenhum trabalho novo atribuído a Claude.

## Atualização 2026-10-11 — pacote de redesign

Integração detalhada e resultados em [REDESIGN.md](REDESIGN.md): navegação por URLs, avaliações com wizard/detalhe, API tenant-scoped, escopos com autorização owner e viewer somente leitura. Implementação por Codex. Claude executado pelo shell terminou exit 1 / ECONNREFUSED, sem alterações. 113 testes Python e contratos frontend passaram. QA visual continua pendente: Edge falhou por acesso negado e exibiu 0x80000003; não contornar proteções do ambiente. Scanner e dados reais preservados nesta etapa.
