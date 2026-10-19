# ASTRO Cyber — Auditoria do Estado Atual

Data: 2026-10-18. Baseado em leitura de código e testes. Sem QA visual, auditoria externa ou clientes reais.

**Legenda de estados:**
- ✅ Implementado e verificado (código + testes passando)
- ⚠️ Implementado sem verificação suficiente (código existe, testes insuficientes ou QA não executado)
- 🔶 Parcial (implementação começou, há buracos)
- ❌ Planejado ou ausente

---

## Autenticação e Sessões

| Capacidade | Estado | Detalhe |
|---|---|---|
| Login / logout | ✅ | `app/auth/routes.py`; sessão assinada Flask |
| Hash de senhas | ✅ | werkzeug.security; não texto puro |
| Papel revalidado no banco | ✅ | `current_user()` do DB, não só sessão (D-003) |
| Usuário sem conta/inativo negado | ✅ | `login_required` revalida ativo |
| Rate-limit de login | ✅ | `app/auth/ratelimit.py`; 5 tentativas/email, 20/IP em 15 min (SEC-009b) |
| CSRF | ✅ | `app/csrf.py`; header `X-Requested-With` verificado (SEC-009a) |
| MFA (TOTP/SMS) | ❌ | Planejado |
| Recuperação de senha | ❌ | Ausente |
| Convite de usuário | ❌ | Ausente; seed manual em `db.py` |
| Sessões revogáveis (lista de sessões ativas) | ❌ | Ausente |

---

## Isolamento Multi-tenant

| Capacidade | Estado | Detalhe |
|---|---|---|
| `account_id` em engagements e scans | ✅ | Migração SEC-002 |
| Filtro `(account_id, id)` em todas as rotas | ✅ | SEC-003; IDOR/BOLA fechados |
| Testes adversariais cross-tenant | ✅ | `tests/test_tenant_isolation.py` (11 testes) |
| Audit log por organização | ⚠️ | Tabela existe; cobertura de ações auditadas não verificada |
| Isolamento em armazenamento/cache/logs | ❌ | Rate-limit em memória (não por tenant); logs não segmentados |

---

## Scanner e Coleta

| Capacidade | Estado | Detalhe |
|---|---|---|
| Scanner TCP socket puro | ✅ | Fallback funcional sem dependências |
| Fallback Go → Nmap → socket | ✅ | Orquestrador em `core/scanner.py` |
| Escopo via engagement autorizado | ✅ | `resolve_authorized_target` vincula ao tenant |
| Bloqueio loopback / link-local / metadata / OT | ✅ | `SCOPE_SAFETY.md`; 139 testes |
| CYMAG_SCOPE_ALLOW / DENY configuráveis | ✅ | Variáveis de ambiente obrigatórias fora de dev |
| Limite 64 candidatos sem expandir CIDR | ✅ | Aritmética sem materializar rede |
| Max IPs por plano | ✅ | Aplicado pós-resolução tenant |
| Cobertura estruturada (o que foi testado vs o que não foi) | ❌ | Ausente; zero achados ≠ sem vulnerabilidades |
| Jobs duráveis (persistem após reinício) | ❌ | Threads em memória; reinício perde estado |
| Cancelamento real de job | ❌ | Ausente |
| Timeout global de job | 🔶 | Timeout de socket existe; timeout global do job ausente |
| Leases / deduplicação de tentativas | ❌ | Ausente |
| IPv6 | ❌ | Rejeitado explicitamente (planejado posterior) |

---

## Achados e Evidências

| Capacidade | Estado | Detalhe |
|---|---|---|
| Persistência em SQLite | ✅ | Tabela `findings` com scan_id, host, port, severity, evidence |
| Classificação: observação / suspeita / confirmado | ✅ | DET-002; sem "confirmado" automático |
| Estimativa financeira com disclaimer obrigatório | ✅ | `core/business.py`; ESTIMATE_DISCLAIMER em todo valor R$ |
| Observações e info não recebem valor financeiro | ✅ | DET-001; `loss_estimate` retorna (0,0) para info/observação |
| IDs estáveis de achados (finding_id único entre avaliações) | ❌ | ID por scan; sem fingerprint entre avaliações |
| Enriquecimento CVE/CVSS verificado | 🔶 | Campo CVE existe; sem parser de feed NVD/CISA KEV |
| Evidência com proveniência (detector, versão, método) | ❌ | Banner existe; metadata de detector ausente |
| Histórico de revalidação (antes/depois) | ❌ | Ausente |

---

## AEGIS (IA)

| Capacidade | Estado | Detalhe |
|---|---|---|
| Integração Groq API | ✅ | `app/ai/aegis.py`; compatível OpenAI protocol |
| Fallback offline determinístico | ✅ | Plataforma funciona sem chave de API |
| Painel admin: testar/aplicar chave sem reiniciar | ✅ | `app/admin/`; chave nunca devolvida ao cliente |
| Sanitização anti-prompt-injection | ✅ | `tests/test_sanitize.py` |
| Chave IA criptografada em repouso | ✅ | Fernet + PBKDF2-HMAC-SHA256 do SECRET_KEY; `api_key_enc` no JSON; legado sem cifrar ainda carregado (A11 — 2026-10-18) |
| AEGIS recebe finding_id, não payload livre | 🔶 | `/api/remediation` suporta `finding_id` com isolamento de tenant; caminho legado ainda ativo; teste de contrato pendente (AI-001 — 2026-10-18) |
| Limites de tokens / orçamento por cliente | ❌ | Ausente |
| Proteção contra prompt injection de conteúdo externo | ⚠️ | Sanitização existe; não cobre todos os caminhos |

---

## Relatórios

| Capacidade | Estado | Detalhe |
|---|---|---|
| Geração PDF (fpdf2) | ✅ | `app/reports/` |
| Relatório montado a partir de scan_id do backend | ✅ | SEC-006; não aceita payload do cliente |
| Selo DEMO em relatórios demonstração | ✅ | SEC-006 |
| Relatório executivo vs técnico separados | ⚠️ | Código existe; QA de conteúdo não feito |
| Narrativa AEGIS no PDF | ⚠️ | Código existe; qualidade da saída não verificada |
| Metodologia e limitações explícitas no PDF | 🔶 | Parcial; auditoria humana ausente |
| PDFs assinados/versionados | ❌ | Planejado (plano gerenciado) |

---

## UX / Frontend

| Capacidade | Estado | Detalhe |
|---|---|---|
| Dashboard por perfil (owner/operator/admin) | ✅ | Implementado por Codex |
| Temas claro/escuro/sistema | ✅ | cymag.css; toggle funciona |
| Modo demonstração client-side | ✅ | cymag-demo.js; sem backend |
| Navegação por URL (filtros preservados) | ✅ | REDESIGN.md |
| Wizard de avaliação | ✅ | Codex; UX-05 |
| QA visual real (contraste, zoom 200%, leitores de tela) | ❌ | Pendente; Edge falhou por acesso negado |
| Responsividade testada (320–1920px) | ❌ | CSS existe; testes não executados |
| Acessibilidade WCAG 2.2 AA | ❌ | Meta definida; não verificada |
| Contraste: verde #1F9D55 e âmbar #B7791F em branco | ❌ | Medido: ~3.5:1 e ~3.6:1 (abaixo de 4.5:1) |

---

## Billing e Planos

| Capacidade | Estado | Detalhe |
|---|---|---|
| Catálogo de planos (5 planos) | ✅ | `core/plans.py`; preços R$297–R$6.000/mês |
| Gating de features por plano | ✅ | Decorators `requires_feature`, `enforce_scan_quota` |
| Quota de scans por conta (não só usuário) | ✅ | SEC-003 |
| Troca de plano self-service (simulada) | ⚠️ | UI existe; sem integração real de pagamento |
| Checkout / assinatura real | ❌ | Simulado no frontend; não integra Stripe/etc. |
| Billing gate em produção | ❌ | Desabilitar simulação de pagamento antes de qualquer piloto |

---

## Segurança da Plataforma

| Capacidade | Estado | Detalhe |
|---|---|---|
| Seed fail-closed em produção | ✅ | SEC-005; `CYMAG_ENV=production` não semeia demo |
| Secret key obrigatória em produção | ✅ | SEC-005 |
| X-Forwarded-For não confiável | ✅ | SEC-003/AUTH-008 |
| CSRF | ✅ | SEC-009a |
| Rate-limit login | ✅ | SEC-009b (por processo; multi-worker exige SQLite/Redis) |
| Viewer/owner não iniciam scans diretamente | ✅ | AUTH-008 |
| Chave IA em texto puro | ❌ | A11; `instance/ai_config.json` |
| Segredos em `.env` fora do repositório | ✅ | `.gitignore` cobre `instance/` |
| HTTPS obrigatório | ❌ | Flask dev server; sem configuração TLS |
| Servidor de aplicação (não Flask dev) | ❌ | Produção exige gunicorn/waitress |
| Backup e restore verificados | ❌ | Ausente |
| Rate-limit por processo (não compartilhado) | ⚠️ | Multi-worker: mover para SQLite/Redis antes de escalar |

---

## Resumo de Gates

| Gate | Estado |
|---|---|
| G0 laboratório: threat model, isolamento, contratos | 🔶 Parcial — isolamento/CSRF/rate-limit feitos; jobs/cobertura/MFA pendentes |
| G1 piloto assistido: jobs duráveis, backup, onboarding | ❌ Não atingido |
| G2 oferta recorrente: ciclo correção/revalidação | ❌ Não atingido |
| G3 SaaS autogerenciado: conector, billing real | ❌ Não atingido |
