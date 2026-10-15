# Modelo atual e migração P0

`accounts` é preservado por compatibilidade. `organizations` referencia accounts com o mesmo id, somente contas não internas. `memberships` vincula usuário, organização, papel e estado ativo. `operator` legado mapeia para `analyst`; `admin`/`cymag` legados não recebem associação global a clientes. O papel organizacional `admin` existe no schema, mas provisionamento/UI de equipe ainda não está implementado.

`organization_id` com FK/index foi adicionado a engagements, scans, findings, audit_log e budget_decisions. Scans herdam o tenant do criador ativo, exigindo que o engagement pertença ao mesmo tenant. Findings herdam o scan. Decisões exigem finding/tenant coerentes. Leituras de objetos/listas usam organização na consulta; requisições derivam organização da identidade e membership atuais, não do payload. Chamadas internas fora de requisição precisam de organização explícita. Suporte conserva apenas o endpoint legado de metadados mínimos de contas.

Migração v1 registrada em `schema_migrations`: associação legada apenas via criador/conta comprováveis no banco; scan com engagement de outra organização permanece em quarentena (`NULL`). Órfãos não são distribuídos a um tenant e o backfill não se repete após a migração. A associação histórica não pode provar titularidade legal: revisão humana dos dados legados ainda é obrigatória.

Antes de alterar um banco legado, init_db gera backup online SQLite, incluindo WAL, com sufixo `.pre-tenant-<UTC>.bak`. Rollback é restore frio do backup, conservando snapshot do estado anterior; não há down migration SQL. Teste `tests/test_migration.py` verifica backup, idempotência, quarentena, FKs, integridade e restore. Parar todos os processos antes do restore. Não iniciar código novo durante a validação do rollback, pois ele migraria novamente.

`users.session_version` invalida cookies anteriores no login/logout. `login_limits` armazena buckets SHA-256, início e contagem, com janela de 15 minutos. Auditoria recebe tenant quando identificável e redaction conservadora.

Pendentes: PostgreSQL, constraints compostas adicionais, ferramentas de revisão de órfãos, entidades/estados de produto da fase 2, delegações e proteção append-only da auditoria.
