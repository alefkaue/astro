# Plano conjunto integrado — 2026-10-11

Claude concluiu PLAN-CLAUDE-01 (subtype success, is_error false, terminal_reason completed). Fonte original: CLAUDE_PRODUCT_PLAN_RESULT.json. A ferramenta Write do Claude foi negada porque exigia aprovação indisponível; ele retornou o parecer no resultado. Codex salvou o conteúdo em CLAUDE_PRODUCT_PLAN_REVIEW.md. Não modificar permissões ou alegar que Claude gravou/implementou código.

## Decisões adotadas

1. SaaS web + conector por rede; agente endpoint posterior e CLI complementar.
2. Jobs duráveis com leases no banco primeiro. Não adicionar Redis/Celery sem necessidade medida.
3. Migrações versionadas inicialmente no SQLite; migração PostgreSQL com fixtures/backup/restore e gate antes de escala comercial. Não bloquear o primeiro spike de jobs por troca do banco.
4. Worker interno e conector futuro compartilham contrato de tarefa/attempt/lease/evidência; apenas identidade e transporte mudam.
5. S0 ampliado: isolamento de revisões, helpers scoped, capacidades explícitas, CSRF/content-type, atribuições gerenciadas, quota atômica e limites reais de plano.

## Implementado e verificado por Codex nesta integração

- GET /api/reviews exige organização e filtra fila por tenant e avaliação concluída. Helper sem tenant retorna lista vazia.
- POST /api/scans/:id/review exige organização, busca scan pelo tenant e atualiza atomicamente por tenant/estado anterior.
- Transições: pending → reviewed → signed, somente scan done. Assinar diretamente, repetir ou regredir devolve 409; scan estrangeiro devolve 404; usuário sem tenant devolve 403.
- Orçamento de correção devolve o mesmo 404 para achado ausente ou de outro tenant; não revela existência.
- Regressão real HTTP+DB inclui staff, admin sem tenant, operator, dois tenants, running, transições inválidas e tentativa de escrita cross-tenant.

Relatórios existentes foram inspecionados: usam login_required e scan_id filtrado pelo tenant; regressões PDF/cross-tenant existentes são executadas na suíte. Isso não é auditoria completa do módulo.

## Limites e próximos responsáveis

As correções acima restringem serviço gerenciado ao mesmo tenant. Não existe ainda atribuição temporária de equipe externa. Implementar assignments auditados antes de autorizar atendimento cross-tenant. Também faltam a verificação de contrato managed e o novo RBAC por capacidades; não declarar S0 concluída.

| Próxima tarefa | Responsável proposto | Arquivos exclusivos / critérios |
| --- | --- | --- |
| SEC-SCOPED | Claude implementa, Codex revisa | app/db.py e chamadores: APIs scoped distintas, inventário dos usos internos e regressões sem tenant |
| SEC-RBAC | Claude implementa, Codex integra UX | app/auth/decorators.py + módulo capabilities: remover bypass global mantendo política explícita; testes por ação/perfil |
| SEC-REVIEW | Claude implementa, Codex revisa | assignments/model/rotas de review: contrato managed, expiração, concessão e auditoria |
| SEC-CSRF | Claude backend, Codex frontend após contrato | Token sessão/content-type; login/logout/POST/PUT/DELETE e compatibilidade de clientes |
| DATA-MIGRATIONS | Claude spike, Codex integra | novo app/migrations/ e testes; aplicação idempotente, rollback e preservação de banco existente |
| JOB-CORE | Claude backend, Codex UI | jobs/attempts/events e worker interno; leases, idempotência, cancelamento e quota no mesmo commit transacional |
| UX-PERSONAS | Codex | frontend: layouts executivo/operador e ações conforme capacidades reais; sem métricas ou módulos fictícios |

Tarefas propostas, não enviadas/implementadas automaticamente no terminal do usuário. Fechar contratos e disponibilizar prompt específico antes de cada execução; nenhum arquivo com dois donos simultâneos. Preferir spike de migrações em arquivos novos para permitir trabalho independente enquanto S0 é integrada.

Validacao desta integracao: 115 testes Python passaram (13 avisos legados fpdf); contratos frontend e boot passaram; git diff --check passou. Nenhuma varredura real executada.
