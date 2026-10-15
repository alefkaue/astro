# Evidências e limites de segurança

Testes locais offline em `tests/test_security.py`, `tests/test_migration.py` e `tests/frontend-api.test.cjs`. A primeira bateria negativa reproduziu 10 falhas no código original: listas e objetos entre tenants, progresso de outro tenant, bypass de admin, usuário desativado, escrita viewer, CSRF ausente, seed demo indiscriminado e checkout fictício sem modo demo. Também revelou vazamento de conexões SQLite no teardown Windows, corrigido fechando conexões ao sair do contexto.

Controles implementados: tenant/membership ativo, filtros no SQL, RBAC sem superadmin implícito, revogação de cookies por versão de sessão, CSRF com token rotacionado e verificação de Origin, limitação persistente por email/IP sem confiar em X-Forwarded-For, demo explícita, produção/staging recusados, export/IA derivados de objetos autorizados, redaction conservadora de segredos e bloqueio do executor inseguro.

Redaction não é classificador completo de dados pessoais. Dados legados de evidência não foram automaticamente reescritos: migração/redaction histórica e retenção ainda precisam de revisão com backup. Backup contém dados sensíveis e exige armazenamento/ACL protegidos. Dados de tenants reais não foram usados nos testes.

Aceite completo da fase 1 **pendente**: MFA e recuperação segura, delegação temporal/justificativa/revogação, comprovantes e janela/expiração/revogação de escopo, controle por conexão, criptografia/retention, auditoria append-only, matriz completa das novas rotas e revisão independente. Não há aprovação de piloto ou conformidade legal.

Algumas features antigas estão explicitamente indisponíveis por risco: scan síncrono, pentest autônomo por threads, descoberta da rede da plataforma, LLM externo sem consentimento e checkout real. Migração funcional prevista: avaliação simulada contratual (fase 2) e worker/agente com plugins permitidos (fase 3). Demo client-side permanece fictícia e não executa scanner.
