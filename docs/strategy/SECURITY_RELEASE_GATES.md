# ASTRO Cyber — Gates de Segurança e Operação

Data: 2026-10-18. Requisitos obrigatórios por gate antes de operar com dados reais de clientes.

**Legenda:** ✅ done | 🔶 parcial | ❌ pendente

---

## Gate G0 — Laboratório (antes de qualquer dado real)

### Segurança obrigatória

| ID | Requisito | Estado | Arquivo(s) | Evidência exigida |
|---|---|---|---|---|
| G0-S01 | Isolamento multi-tenant: `(account_id, resource_id)` em todas as rotas | ✅ | `app/scope.py`, `app/*/routes.py` | `tests/test_tenant_isolation.py` 11 testes passam |
| G0-S02 | IDOR/BOLA fechado; recurso de outro tenant retorna 404 | ✅ | `app/scope.py` | Testes adversariais passam |
| G0-S03 | Papel revalidado no banco, não só sessão | ✅ | `app/auth/decorators.py` | D-003; `current_user()` |
| G0-S04 | CSRF protegido com `X-Requested-With` | ✅ | `app/csrf.py` | `tests/test_csrf.py` 13 testes |
| G0-S05 | Rate-limit de login (5/email, 20/IP em 15min) | ✅ | `app/auth/ratelimit.py` | `tests/test_login_rate_limit.py` 8 testes |
| G0-S06 | Seed fail-closed: produção não semeia demo | ✅ | `app/db.py`, `app/config.py` | SEC-005 |
| G0-S07 | Secret key obrigatória em produção | ✅ | `app/config.py` | SEC-005; falha se CYMAG_ENV=production e sem chave |
| G0-S08 | Viewer/owner não iniciam scans | ✅ | `app/auth/decorators.py` | AUTH-008 |
| G0-S09 | X-Forwarded-For não confiável (IP real do socket) | ✅ | `app/auth/` | AUTH-008 |
| G0-S10 | Relatórios montados do backend (scan_id, não payload) | ✅ | `app/reports/routes.py` | SEC-006; `tests/test_reports.py` |
| G0-S11 | Bloqueio redes especiais: loopback, link-local, metadata, OT | ✅ | `core/scanner.py` | `tests/test_scope_safety.py`; 139 testes |
| G0-S12 | Chave IA cifrada em repouso (não texto puro) | ✅ | `app/ai/aegis.py` | Fernet + PBKDF2-HMAC-SHA256; `api_key_enc` no JSON; 4 testes passam (A11 — 2026-10-18) |
| G0-S13 | AEGIS recebe finding_id autenticado, não payload livre | 🔶 | `app/scans/routes.py`, `app/db.py` | `finding_id` suportado com isolamento; caminho legado ativo; teste de rejeição sem ID válido pendente (AI-001 — 2026-10-18) |
| G0-S14 | Rate-limit em SQLite (não memória) para multi-worker | ❌ | `app/auth/ratelimit.py` | Teste com 2 workers simultâneos |

### Operação obrigatória

| ID | Requisito | Estado | Arquivo(s) | Evidência exigida |
|---|---|---|---|---|
| G0-O01 | Servidor de produção (gunicorn/waitress), não Flask dev | ❌ | `requirements.txt`, documentação de deploy | Deploy funciona com gunicorn; logs estruturados |
| G0-O02 | HTTPS obrigatório (TLS terminado no proxy ou app) | ❌ | nginx/caddy config ou similar | Certificado válido; HTTP redireciona para HTTPS |
| G0-O03 | Backup do SQLite com teste de restore verificado | ❌ | Script de backup | Restore testado com dados reais; RPO documentado |
| G0-O04 | Variáveis de ambiente em arquivo `.env` fora do repositório | ✅ | `.gitignore` cobre `instance/` e `.env` | `git status` não mostra segredos |
| G0-O05 | Binário Go e Nmap não rodam com permissão do processo web | ❌ | Configuração de deploy | Processo web não tem sudo; scanners em subprocess com timeout |

---

## Gate G1 — Piloto assistido (antes de cliente com dados reais)

Todos os itens G0 mais os abaixo.

| ID | Requisito | Estado | Arquivo(s) | Evidência exigida |
|---|---|---|---|---|
| G1-S01 | MFA para contas admin e cymag | ❌ | `app/auth/` | Admin sem MFA bloqueado em produção |
| G1-S02 | Sessões revogáveis (listar e invalidar por sessão) | ❌ | `app/auth/` | Token de sessão inválido após revogação |
| G1-S03 | Expiração de engagement (validade do escopo) | ❌ | `app/engagements/routes.py`, `app/db.py` | Scan com engagement expirado retorna 403 |
| G1-S04 | CYMAG_SCOPE_ALLOW obrigatória em produção | ✅ | `core/scanner.py` | Inicia sem allowlist → falha clara |
| G1-J01 | Jobs duráveis: tabela com leases, recuperação após reinício | ❌ | `app/db.py`, novo módulo jobs | Job em andamento sobrevive a reinício; status persiste |
| G1-J02 | Cancelamento real de job | ❌ | Job module | `POST /api/scans/{id}/cancel` muda status; worker para |
| G1-J03 | Cobertura estruturada por job (tentados, testados, erros) | ❌ | `core/scanner.py`, job module | Resultado inclui hosts_tentados, hosts_testados, erros |
| G1-J04 | Timeout global de job | ❌ | Job module | Job com timeout de 10min é cancelado automaticamente; estado persiste |
| G1-O01 | Backup automático programado (diário mínimo) | ❌ | Script + cron/task | Backup executado; restore testado com snapshot de piloto |
| G1-O02 | Logging estruturado com correlation_id | ❌ | `app/__init__.py` | Log de erro rastreável por request_id sem expor dados sensíveis |
| G1-O03 | Alertas para: falha de job, erro de backup, indisponibilidade AEGIS | ❌ | Monitoramento | Alerta chega em <5min após condição |
| G1-D01 | Política de retenção de dados documentada | ❌ | Documentação | Definido: quanto tempo guardamos evidências; como excluímos ao offboarding |
| G1-D02 | Não enviar evidências brutas para AEGIS sem consentimento do cliente | ❌ | `app/ai/aegis.py` | Configuração de consentimento por organização |

---

## Gate G2 — Oferta recorrente

Todos os itens G0+G1 mais os abaixo.

| ID | Requisito | Estado | Evidência exigida |
|---|---|---|---|
| G2-P01 | Ciclo de correção: responsável, prazo, status, revalidação | ❌ | Cliente fecha loop sem intervenção ASTRO |
| G2-P02 | Revalidação com evidência comparável (mesma metodologia) | ❌ | Revalidação usa mesmo perfil; resultado "corrigido" exige ausência confirmada |
| G2-P03 | IDs estáveis de achados entre avaliações | ❌ | Mesmo achado em avaliações diferentes tem fingerprint igual |
| G2-P04 | Histórico comparável (não confunde ausência com correção) | ❌ | Ausência de achado mostra "não detectado" e não "corrigido" |
| G2-O01 | RPO/RTO documentados e testados | ❌ | Restauração completa em <X horas comprovada |
| G2-O02 | Custo por cliente medido (infra + IA + suporte) | ❌ | Planilha com custo real por avaliação |

---

## Gate G3 — SaaS autogerenciado

Todos os itens G0+G1+G2 mais os abaixo.

| ID | Requisito | Evidência exigida |
|---|---|---|
| G3-C01 | Conector com identidade exclusiva, enrollment de uso único, revogação | Teste: revogação do conector bloqueia próxima busca de job |
| G3-C02 | Conector com escopo local verificado (não confia no payload do job) | Conector revalida limites localmente |
| G3-B01 | Billing real integrado (Stripe/etc.) | Assinatura cria conta; cancelamento revoga acesso |
| G3-O01 | Onboarding autônomo testado (cliente entra, configura, executa sem ASTRO) | Teste com usuário externo sem orientação |
| G3-O02 | Tenant isolation revisado para escala | Auditoria cross-tenant com N>10 organizações |

---

## O que não fazer antes dos gates

- Não hospedar em servidor público antes de G0-S12 (chave IA) e G0-O02 (HTTPS)
- Não aceitar dados de cliente real antes de G0-O03 (backup) e G1-J01 (jobs duráveis)
- Não vender SLA de disponibilidade sem G1-O03 (alertas) e G2-O01 (RPO/RTO)
- Não distribuir conector antes de G3-C01
