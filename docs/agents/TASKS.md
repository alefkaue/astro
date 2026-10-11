# TASKS — Coordenação Claude Code + Codex

> Backlog vivo. Prioridade P0 (segurança) → P1 (confiança) → P2 (produto).
> Regras: um arquivo = um dono por vez. Sem commit/push sem autorização do fundador.

## Legenda
- 🔵 Claude Code (arquitetura, segurança, authz, integração)
- 🟢 Codex (motores, honestidade de detecção, testes, refactor independente)
- Estados: `todo` · `doing` · `review` · `done` · `blocked`

## Sprint atual — Fase 0/1 (segurança defensiva)

| ID | Tarefa | Dono | Arquivos | Estado | Dep. |
|----|--------|------|----------|--------|------|
| SEC-001 | Baseline + auditoria + branch + docs | 🔵 | `docs/**` | done | — |
| SEC-002 | Isolamento multi-tenant (account_id em engagements/scans) + migração | 🔵 | `app/db.py` | **done** | SEC-001 |
| SEC-003 | Correção IDOR/BOLA em todas as rotas (scans, findings, engagements, autonomous) | 🔵 | `app/scope.py`, `app/*/routes.py`, `app/auth/decorators.py` | **done** | SEC-002 |
| SEC-004 | Testes adversariais A/B (dois tenants) | 🔵 | `tests/test_tenant_isolation.py` | **done** (11 testes) | SEC-002/003 |
| SEC-005 | Seed fail-closed: produção não semeia demo; secret key obrigatória | 🔵 | `app/config.py`, `app/db.py` | **done** | SEC-001 |
| SEC-006 | Relatórios a partir de dados do backend (scan_id, não payload do cliente) + selo DEMO | 🔵 | `app/reports/*`, `static/cymag.js` | **done** (4 testes) | SEC-002 |
| DET-001 | Honestidade de impacto financeiro: rotular estimativa, sem "garantido" | 🟢→🔵 | `core/business.py`, `tests/test_business.py` | **done** (feito por Claude — Codex bloqueado, ver abaixo) | — |
| DET-002 | Reclassificar achados fracos como observação/suspeita (não "confirmado") | 🟢 | `core/checks/*`, `tests/test_checks_honesty.py` | **done** (Codex, 18 testes, revisado por Claude) | DET-001 |
| A9/A11/A12 | X-Forwarded-For confiável, chave IA em texto puro, quota por conta | 🔵 | auth/aegis/billing | parcial (quota feita) | — |

## ✅ Status do Codex — RESOLVIDO
A execução autônoma falhava porque `~/.codex/config.toml` tinha `[windows] sandbox = "elevated"`,
modo que o `codex.exe` não consegue lançar nesta máquina. Corrigido para `unelevated`
(backup em `config.toml.bak`). Agora `codex exec -s workspace-write` roda normalmente.
Codex executou **DET-002** (reclassificação de achados em `core/checks/`) — ver CHANGELOG.
Invocação usada pelo Claude:
`codex exec -s workspace-write -c 'windows.sandbox="unelevated"' -C <repo> - < tarefa.md`

## Entregue
- SEC-001..005 + DET-001 — ver `docs/audit/2026-10-baseline.md` e `CHANGELOG_AGENTS.md`. 70 testes passam.

## Sessão ASTRO — 2026-10-10 (substitui divisão anterior para novas tarefas)

Codex é coordenador/integrador e dono do frontend. Claude foi acionado para AUTH-008 exclusivamente em decorators e seu novo teste. Processo terminou sem edições por ECONNREFUSED; Codex assumiu após confirmar conclusão. `CLAUDE_SEC007_TASK.txt` é o nome do arquivo enviado, não o SEC-007 de segredos do master plan: novo backlog usa AUTH-008 para evitar colisão.

| ID | Prioridade / fase | Responsável | Estado | Aceite / dependência |
| --- | --- | --- | --- | --- |
| MAT-001 | P0 / 0 | Codex | done | 3 ZIPs inventariados/extraídos separadamente; hashes e listagens; documentos e SVGs |
| DS-001 | P1 / 1 | Codex | done parcial | Identidade, temas, SVG, console e decisões em DESIGN_MERGE; QA visual pendente |
| AUTH-008 | P0 / 2 | Claude → Codex | done | Usuário ativo, IP não forjável, sem tenant negado, viewer/owner não iniciam jobs; regressões |
| SCAN-008 | P0 / 3 | Codex | done parcial | Despacho somente inventário TCP, 64 candidatos; sem checks intrusivos; cobertura/timeout parcial pendentes |
| DASH-001 | P1 / 1–3 | Codex | done | Dashboard da persistência por tenant, demo separada, estado vazio/erro, limites explícitos |
| UI-002 | P1 / 3 | Codex | done | Classificação/evidência, análise do histórico correta, scan_id autônomo usado no PDF |
| SEC-009 | P0 / 2 | Claude (CSRF) + Codex (rate-limit) | parcial | **feito 2026-10-11:** CSRF (origem+formato) e rate-limit/bloqueio de login. Pendente: segredo IA cifrado, suporte/admin auditado, matriz RBAC completa |
| SCOPE-010 | P0 / 2–3 | Backend | todo | Propriedade, RoE temporal, bloqueio OT/metadados/link-local, budgets globais e egress |
| JOB-001 | P1 / 2–3 | Backend | todo | Fila durável, cancelamento real, sequência de eventos, recovery/retries; depende schema |
| DATA-001 | P1 / 2–3 | Backend | todo | Ativos, evidências, detector/método/versionamento, finding_id estável; depois PostgreSQL |
| FIX-001 | P1 / 3–4 | Backend + UI | todo | Responsável/prazo/status e revalidação que não confunde falta de cobertura com correção |
| AI-001 | P1 / 4 | Backend | todo | AEGIS recebe IDs/evidências do tenant; fatos/hipóteses/sugestões separados e validados |
| QA-001 | P1 / 5 | Codex + Claude | todo | Browser E2E, responsividade, teclado/contraste, regressão PDF, operação e deploy |

### Diferenciais comerciais — classificação de engenharia, não validação de mercado

| Diferencial | Valor esperado | Complexidade | Risco técnico | Dependências / ordem |
| --- | --- | --- | --- | --- |
| Correção assistida em português com evidências | Alto | Média | Médio | finding_id, templates revisados; primeiro incremento comercial |
| Revalidação com prova antes/depois | Alto | Alta | Alto | JOB/DATA, mesma metodologia e cobertura; prioridade seguinte |
| Histórico de mudanças e regressões | Alto | Média | Alto | fingerprint estável, avaliações comparáveis, distinção não observado/não testado |
| Priorização contextual explicável | Alto | Média | Médio | ativos/criticidade/exposição/proveniência; sem score financeiro inventado |
| Relatórios acessíveis gestor/técnico | Alto | Baixa–média | Médio | PDF existente; ampliar metodologia/limitações/revisão |
| Experiência simples para PMEs | Alto | Média | Baixo | QA/onboarding e escopo com comprovação; contínuo |
| AEGIS histórico vinculado a evidências | Médio–alto | Alta | Alto | AI/DATA, segurança de provedor e limites de contexto |
| Monitoramento contínuo | Alto | Alta | Alto | JOB, scheduler, autorização válida, custos/alertas; após pilotos |

Pesquisa em fontes primárias: [Tenable VPR](https://docs.tenable.com/vulnerability-management/best-practices/security/Content/VulnerabilityPriorityRating.htm) já prioriza por impacto/ameaça; [NodeZero](https://horizon3.ai/nodezero/) já orienta correção/verificação. Portanto esses conceitos isolados não são exclusivos. Hipótese ASTRO: clareza em português, evidência transparente, acompanhamento assistido e continuidade da correção para PME. [NIST para PMEs](https://www.nist.gov/itl/smallbusinesscyber/nist-cybersecurity-framework-0) informa o enquadramento; não implica certificação ou cobertura total.

## Atualização 2026-10-11 — pacote de redesign

Integração detalhada e resultados em [REDESIGN.md](REDESIGN.md): navegação por URLs, avaliações com wizard/detalhe, API tenant-scoped, escopos com autorização owner e viewer somente leitura. Implementação por Codex. Claude executado pelo shell terminou exit 1 / ECONNREFUSED, sem alterações. 113 testes Python e contratos frontend passaram. QA visual continua pendente: Edge falhou por acesso negado e exibiu 0x80000003; não contornar proteções do ambiente. Scanner e dados reais preservados nesta etapa.

Revisao conjunta concluida: Claude revisou, Codex corrigiu isolamento de autorizacao e bugs frontend. Ver CLAUDE_REVIEW_INTEGRATION.md; F2 (helpers scoped/unscoped) e QA visual pendentes.

## Plano de produto pesquisado — 2026-10-11

Referencia: PRODUCT_PLAN.md. Arquitetura proposta: SaaS web + conector por ambiente; CLI complementar; agente endpoint posterior.

| ID | Dono | Entrega / arquivos | Estado | Dependencia |
| --- | --- | --- | --- | --- |
| PLAN-01 | Codex | Pesquisa oficial, arquitetura e mapa de telas: PRODUCT_PLAN.md | done | Inspecao do backend |
| PLAN-CLAUDE-01 | Claude | Revisao independente, schema/jobs/API/threat model: CLAUDE_PRODUCT_PLAN_REVIEW.md somente | preparada, nao executada | Terminal normal do usuario |
| PLAN-02 | Codex | Integrar parecer e fechar contratos/backlog por arquivo | todo | PLAN-CLAUDE-01 |
| S0 | Claude implementa, Codex revisa | Helpers tenant explicitos, managed review, sessoes/CSRF e testes | proposta | PLAN-02 |
| S1 | Claude backend, Codex UI | Jobs/eventos/cobertura duraveis e recuperacao | proposta | S0 |
| S2 | Claude dados, Codex paginas | Networks/ativos/achados estaveis e migracoes | proposta | S1 |
| S3 | Codex frontend, Claude RBAC/API | Experiencias por perfil, correcoes e AEGIS contextual | proposta | S2 |
| S4 | Claude conector, Codex onboarding | Prototipo local em laboratorio, enrollment e revogacao | proposta | S1/S2 + contrato seguro |

Nao editar os mesmos arquivos em paralelo. Novas telas/conector nao estao implementados. QA visual permanece pendente.

PLAN-CLAUDE-01 e PLAN-02 concluidos: parecer Claude recebido e integrado em PRODUCT_PLAN_INTEGRATION.md. Job queue inicial sera tabela com leases, sem Redis/Celery; worker interno antes do conector. Codex corrigiu revisoes cross-tenant e transicoes invalidas. S0 ainda pendente: helpers scoped, capacidades, CSRF e assignments managed.

UX-PERSONAS: primeira implementacao concluida por Codex (menu/dashboards/relatorios/escopos); ver EXPERIENCE_UI.md. Revisao Claude experience e QA visual pendentes. Gestao de ativos/achados/correcoes global ainda depende de modelos reais.

## Prontidao comercial — 2026-10-11

COMMERCIAL_READINESS.md define jornada, ofertas de servico, gaps de configuracao/UX/operacao e gates G0-G3. Proximo foco P0: capacidades/tenant/CSRF/MFA/sessoes, migracoes/jobs/coverage/limites, backup/restore e onboarding. Produto nao pronto para venda ampla. Ciclo de correcao/revalidacao e conector ainda ausentes. UX-CONT-01 feito por Codex: texto monocromatico nas etiquetas semanticas/erros, fonte auxiliar ampliada e espaco para seletor de tema; cores oficiais preservadas. QA visual/teclado/leitor/zoom ainda pendente. Claude commercial: revisao preparada, nao executada.

Prioridade comercial revista: controle de alvos/escopos, gates de producao/IA/billing, auth/CSRF, cobertura e jobs duraveis, ciclo de dados e QA acessivel. Primeiro piloto assistido, portal opcional somente leitura. Ver COMMERCIAL_REVIEW_INTEGRATION.md.

PILOT-GATES implementado por Codex; SCOPE-DENY delegado como patch revisavel ao Claude via -Task pilot-security (pendente execucao local). UI de capacidades de implantacao pendente. Pilot hospedado permanece bloqueado.

SCOPE-DENY implementado por Codex; Claude entregou observacoes sem patch por bloqueio interno de seguranca. 139 testes passaram. Validacao de contratos, cobertura/jobs e auth permanecem pendentes. Ver SCOPE_SAFETY.md.
