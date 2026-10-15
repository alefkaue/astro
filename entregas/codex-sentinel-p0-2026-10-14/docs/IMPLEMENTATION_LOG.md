# Registro de implementação

## Fase 0 — baseline (parcial)

Código local recuperado de cópia identificada, preservada e sem alterações na origem. Arquivos trazidos: 65 arquivos de código/documentação/recursos; exclusões em BASELINE_2026.md. Documentos novos: BASELINE_2026.md, FEATURE_MATRIX.md, ADR/0001-product-and-architecture.md, inventários de hashes/rotas.

Testes baseline: 49 passaram com banco isolado; execução padrão 42 passaram/7 erros de ambiente. Go indisponível. Divergência: workspace fornecido não continha código; origem encontrada usa remote cymag_saas e commit b888fb9. Não foi possível consultar astro.git por rede. Git no destino ausente, não foi criado histórico artificial.

## Fase 1 — incremento P0 (parcial)

Implementação real: organizations/memberships com papéis organizacionais separados dos papéis de plataforma; organization_id/FK/index nos recursos existentes; consultas/listas e mutações com contexto de tenant e checagem de permissão; quarentena dos dados legados ambíguos; backup online e restore frio; fechamento efetivo das conexões SQLite. Identidade/papel/membership são consultados no banco. Não há bypass global de admin. Login/logout rotacionam versão de sessão e invalidam cookies anteriores.

CSRF inclui token anônimo para login, rotação e integração JS/PDF. Controle de Origin, limite de corpo, validação de tipos, headers seguros e erros coerentes. Rate limit persistente de 10 tentativas/15 minutos por email e IP, com buckets hash e sem confiar em header de proxy. Seed previsível e checkout fictício apenas DEMO explícito. Produção/staging recusados. Bootstrap local interativo sem senha default.

PDF e AEGIS selecionam dados autorizados no servidor por scan_id/finding_id; conteúdo forjado não substitui evidência persistida. AEGIS externo está desativado até consentimento/limites/schemas; fallback somente sugestão, sem comandos automáticos. Redaction conservadora para evidências/audit novos. API não demo deixa valores financeiros não estimados e preços sob validação. Alterações JS acompanham CSRF, JSON em ações sem payload e identificação de dados persistidos.

Execução web legada síncrona/autônoma, exploit_chain e descoberta da rede do servidor estão bloqueadas explicitamente. O runner também recusa start. Código técnico legado foi preservado para adaptação controlada, sem novas capacidades de scanner. Alternativa atual é demo client-side fictícia; execução futura exige worker/agente autorizado. Não houve chamadas a alvos externos, push, deploy ou compra.

### Arquivos

Modificados: `.env.example`, `.gitignore`, `app/__init__.py`, `app/config.py`, `app/db.py`, `app/auth/{decorators,routes}.py`, `app/engagements/routes.py`, `app/scans/routes.py`, `app/scope.py`, `app/autonomous/runner.py`, `app/billing/routes.py`, `app/main.py`, `app/owner/routes.py`, `app/reports/routes.py`, `app/ai/aegis.py`, `core/scope.py`, `static/cymag.js`, `tests/test_billing.py`, `README.md`, `INSTALL.md`.

Novos de código/teste: `app/security.py`, `app/login_limits.py`, `core/redaction.py`, `tools/bootstrap_local.py`, `tools/restore_sqlite.py`, `tests/test_security.py`, `tests/test_migration.py`, `tests/frontend-api.test.cjs`. Documentos deste incremento: DATA_MODEL, API_CONTRACTS, SECURITY_REQUIREMENTS, ARCHITECTURE, THREAT_MODEL, RELEASE_READINESS, NEXT_STEPS e este registro. Inventário detalhado: `docs/changed_files.json` (comparação com SHA-256 do baseline, 21 arquivos modificados).

### Testes e resultados

- Antes das correções: **10 falhas de segurança reproduzidas** em fixtures A/B; 10 erros adicionais de teardown revelaram conexões SQLite não fechadas. Corrigidos ambos os problemas.
- Suíte final: `python -m pytest tests -q -p no:cacheprovider --tb=short`: **100 passaram em 57,36 s**. Conservados os 49 testes originais, ajustando somente isolamento/mode demo/CSRF do billing; adicionados 51 cenários de segurança/migração.
- Cobertura adicional: BOLA de escopos/achados/progresso, autorização/review/budget/export/IA, viewer/analyst/admin, revogação/downgrade de membership, usuário desativado, cookie copiado após logout, rate limit e CSRF login, inputs malformados, ausência de seed, guards de produção, scanner nunca chamado, redaction, preservação de posse após mudança do criador, PDF real com fixture e ausência de dinheiro inventado.
- Migração: vínculo legado consistente, quarentena de órfãos/conflitos, backfill único, FK check, reinicialização idempotente, backup único, restore e integrity_check. Dados inteiramente fictícios, sem tocar banco da origem.
- `node --test --test-isolation=none tests/frontend-api.test.cjs`: **3 passaram** (rotação CSRF, JSON/CSRF no logout, leitura sem chamada extra). Execução padrão com subprocesso falhou por `spawn EPERM`; isolamento in-process funcionou. Não equivale a browser e2e.
- `node --check static/cymag.js`, `node --check static/cymag-demo.js` e `python -m compileall -q app core tools tests`: passaram.
- Smoke final da aplicação com banco fictício removido ao terminar: index 200, health 200/AEGIS offline, me 401, csrf 200. Inicialização funcional local; nenhum servidor ficou aberto. Warnings de dependências opcionais paho-mqtt/python-nmap ausentes, com execução real bloqueada. Git da origem permaneceu limpo após o trabalho.
- Há **10 warnings de depreciação fpdf2** sobre `ln`; PDF foi gerado corretamente. Correção da API PDF permanece débito, sem reescrita do gerador.
- Go/build e PostgreSQL não executados: toolchain/infraestrutura ausentes. Nenhuma readiness comercial, jurídica ou de produção foi alegada.

### Pendências de fase 1

MFA/recuperação segura, delegação com prazo/justificativa/revogação, prova/janela/expiração/revogação de escopo, política/checagem por conexão, retenção/criptografia/ACL de backups, saneamento histórico, auditoria append-only, constraints adicionais e matriz completa com os recursos futuros. A aprovação de escopo legada continua parcial; não libera execução real. Requisitos não foram substituídos por mocks declarados como completos.

## Estado por fase

| Fase | Mudança real | Arquivos | Testes executados/resultados | Risco residual | Status |
|---|---|---|---|---|---|
| 0 | Código recuperado e auditado, baseline anterior às edições | BASELINE_2026, FEATURE_MATRIX, ADR, hashes/rotas | 49 passaram; execução padrão inicial 42/7 erros de ambiente | Go ausente, dependências não pinadas | Parcial |
| 1 | Isolamento/RBAC/sessão/demo/export/IA/backup e controles de execução | Lista acima e changed_files.json | 100 Python + 3 JS; parse/compileall verdes | Pendências P0 acima e revisão independente | Parcial |
| 2 | Nenhuma; contratos atuais apenas documentados | Nenhum incremento de fase 2 | Não executados | Fluxo integral/API v1 ausentes | Bloqueado pelo aceite P0 |
| 3 | Nenhuma; runner legado somente bloqueado na fase 1 | Nenhum incremento de fase 3 | Build Go indisponível | Worker/agente/CLI ainda ausentes | Bloqueado pelo aceite P0 |
| 4 | Nenhuma; compatibilidade CSRF/IDs no frontend corrigida na fase 1 | Nenhum incremento de fase 4 | Sem browser e2e | UX completa/F1–F6 pendentes | Bloqueado pelo aceite P0 |
| 5 | Nenhuma; barreiras de IA/billing e valores inventados corrigidas na fase 1 | Nenhum incremento de fase 5 | Sem aceite de fase 5 | Relatórios versionados/dedup/entitlements pendentes | Bloqueado pelo aceite P0 |
| 6 | Nenhuma release/deploy | RELEASE_READINESS registra bloqueios | Sem infraestrutura/release | Piloto real não aprovado | Bloqueado pelo aceite P0 |

Checkpoint operacional e comandos Windows/Linux em `docs/NEXT_STEPS.md`. Nenhuma continuação autônoma em segundo plano.
