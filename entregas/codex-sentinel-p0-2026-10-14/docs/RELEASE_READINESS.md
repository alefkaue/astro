# Estado de release

**Não pronto para piloto real.** Código local e incremento P0 testáveis; fase 1 parcial. Produção/staging recusados na inicialização.

| Verificação | Estado |
|---|---|
| Baseline local e origem identificada | Registrado |
| Regressão Python e controles tenant | Testados; ver IMPLEMENTATION_LOG.md |
| Migração/backup/restore SQLite fictício | Testados |
| CSRF do cliente JS | Testado em Node VM; não equivale a browser e2e |
| Parse JS e compileall Python | Verificados |
| Build/test Go Windows/Linux | Bloqueado: Go ausente |
| PostgreSQL, Redis/RQ, worker, agente | Pendentes |
| MFA, recuperação, delegação, escopo completo | Pendentes P0 |
| SAST, secret scan completo, SBOM, lock e licenças | Pendentes |
| E2E F1–F6, mobile/acessibilidade | Pendentes |
| Infraestrutura, legal, consentimento/retention e auditoria independente | Pendentes |

Pendências de decisão dos fundadores: preços após entrevistas, domínio/marca, contrato dos serviços humanos, provedor de cobrança, infraestrutura de produção, política comercial e responsável formal por atendimento a incidentes. Nada disso foi inventado ou contratado.
