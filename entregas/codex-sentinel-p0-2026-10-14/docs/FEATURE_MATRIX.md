# Matriz de funcionalidades

| Área | Baseline | Validação restante |
|---|---|---|
| Login/contas/papéis | Implementado, segurança parcial | CSRF, sessões revogáveis, MFA, recuperação, rate limit |
| Organizações | accounts legado parcial | Tenant explícito, memberships e delegação |
| Escopos | Implementado parcial | Posse, janela, provas, expiração/revogação |
| Scan manual | Implementado, síncrono | Bloqueado até controles seguros de executor |
| Autônomo | Threads/memória | Bloqueado; pentest automático não permitido pelo produto |
| Achados/histórico | Implementado parcial | BOLA, dedup, remediação/timeline |
| Relatórios | PDF existente | Posse, contrato persistido, permissionamento e versionamento |
| AEGIS | Online opcional/fallback | Consentimento, seleção de dados e ausência de valores inventados |
| Billing | Simulado | Exclusividade DEMO; preços sob validação |
| Frontend | SPA existente/demo local | Integração CSRF e contratos; F1–F6 e2e pendentes |
| Agente/CLI | Ausente | Fase 3 após P0 |
| PostgreSQL/Redis/RQ | Ausente | Migrações/fila e testes de infraestrutura |
| Release/piloto | Não pronto | Fase 6 e revisão independente |

Após incremento P0: tenant/membership e queries scoped implementados nos recursos existentes; CSRF/RBAC/sessão e guards demo/produção testados; PDF e AEGIS usam dados persistidos autorizados. Scan/threads/LLM externo suspensos explicitamente. Isso não conclui as fases de produto, motor, experiência web ou release. Resultado final: 100 testes Python + 3 testes JS verdes, com limitações no IMPLEMENTATION_LOG.md.
