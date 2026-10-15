# Threat model inicial — pendente de revisão independente

| Ameaça | Controle deste incremento | Residual |
|---|---|---|
| BOLA/IDOR de tenant | Membership ativa + SQL com organização + 404 | Cobertura deve crescer junto com API v1 e novas entidades |
| Cookie antigo após logout/desativação | Versão de sessão, usuário/membership atuais | MFA/recuperação e operação de revogação ainda incompletas |
| CSRF/brute force | Token, Origin, rate limit persistente | Operação com proxy confiável e proteção volumétrica pendentes |
| SSRF/rebinding/scan invasivo | Executor web e descoberta local bloqueados | Agente e worker com validação por conexão pendentes |
| Agente malicioso/replay | Nenhum endpoint de agente liberado | Enrollment, autenticação, schema/replay aguardam fase 3 |
| Prompt injection/exfiltração LLM | Provedor externo desativado, seleção autorizada, fallback identificado | Consentimento, budgets e schemas externos pendentes |
| Segredos em evidências/logs | Redaction conservadora em novos findings/audit | Conteúdo histórico, PII, criptografia/retention e ACL de backups pendentes |
| Confusão demo/produção | Seed/checkout DEMO explícito, startup de produção recusado | Demo frontend legado ainda precisa alinhar contratos completos |

Não foram executados scans externos, exploit contra máquinas reais ou consulta de serviços pagos.
