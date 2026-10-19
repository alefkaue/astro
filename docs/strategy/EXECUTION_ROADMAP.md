# ASTRO Cyber — Roadmap de Execução

Data: 2026-10-18. Baseado no estado atual verificado do código e nos gates de `SECURITY_RELEASE_GATES.md`.

**Prioridade:** Risco → Valor para o cliente → Dependências → Custo de manutenção.

**Datas são estimativas de esforço, não compromissos. Definir prazo real com disponibilidade dos fundadores.**

---

## Estado atual resumido

| Gate | Estado |
|---|---|
| G0 — Laboratório | 🔶 Parcial — 11/14 itens de segurança; 1/5 itens de operação |
| G1 — Piloto assistido | ❌ Bloqueado por G0 |
| G2 — Oferta recorrente | ❌ Bloqueado por G1 |
| G3 — SaaS autogerenciado | ❌ Bloqueado por G2 |

**Pendentes G0 (bloqueadores de qualquer dado real de cliente):**
- G0-S12 ✅ FEITO hoje (chave IA cifrada com Fernet — A11)
- G0-S13 🔶 Parcial (`finding_id` suportado na rota; testes de contrato pendentes)
- G0-S14 ❌ Rate-limit em SQLite para multi-worker
- G0-O01 ❌ Servidor de produção (gunicorn/waitress)
- G0-O02 ❌ HTTPS
- G0-O03 ❌ Backup verificado
- G0-O05 ❌ Scanner não roda com permissão do processo web

---

## Fase 1 — Fechar G0 (próximas 2–4 semanas)

Objetivo: ambiente capaz de receber dados reais de um único cliente interno/laboratório.

| ID | Tarefa | Responsável | Arquivos | Evidência de conclusão | Esforço |
|---|---|---|---|---|---|
| G0-T01 | Finalizar G0-S13: adicionar teste que garante rejeição de remediação sem `finding_id` válido do tenant | Backend | `tests/test_remediation_isolation.py` | Teste passa: `finding_id` de outro tenant retorna 404 | 2–3h |
| G0-T02 | Rate-limit em SQLite: tabela `login_attempts(key, count, window_start)`, migrar `ratelimit.py` | Backend | `app/auth/ratelimit.py`, `app/db.py` | Testes passam com 2 workers; rate-limit não reseta entre processos | 3–5h |
| G0-T03 | Deploy com gunicorn (Windows: waitress): adicionar `requirements.txt`, documentação mínima de deploy | Ops | `requirements.txt`, `docs/DEPLOY.md` | App sobe com waitress; logs em stdout | 1–2h |
| G0-T04 | HTTPS: documentar configuração com nginx/caddy como proxy reverso | Ops | `docs/DEPLOY.md` | HTTP redireciona para HTTPS; certificado válido (Let's Encrypt ou self-signed para lab) | 2–4h |
| G0-T05 | Backup do SQLite: script de cópia datada + teste de restore | Ops | `scripts/backup.sh` ou `.ps1` | Restore funciona com cópia de 24h atrás; RPO documentado | 2–3h |
| G0-T06 | Scanner em subprocesso sem permissão do processo web | Ops/Backend | Documentação de deploy | Processo web não tem sudo; scanner chama nmap com timeout via subprocess | 1–2h |
| G0-T07 | Commitar tudo e passar os 166+ testes | Backend | — | `pytest -q` verde | 30min |

**Bloqueadores para piloto:** G0-T01, G0-T02 (segurança) + G0-T03, G0-T04, G0-T05 (operação).

---

## Fase 2 — Validação comercial (paralela à Fase 1)

Objetivo: entender se alguém paga pela entrega antes de construir mais produto.

| ID | Tarefa | Responsável | Entrega | Critério de sucesso |
|---|---|---|---|---|
| COM-01 | Redigir proposta-padrão e RoE (1–2 páginas) | F1 | Documento Word/PDF | Revisado por advogado |
| COM-02 | Listar 5–10 empresas candidatas a piloto (rede pessoal, faculdade, clientes de TI conhecidos) | F1 | Planilha de prospecção | Lista com contato e dor identificada |
| COM-03 | Roteiro de demonstração: 30 minutos mostrando escopo → avaliação → relatório | F1+F2 | Script + ambiente de demo limpo | Demonstrado internamente sem erro |
| COM-04 | Realizar 3 entrevistas de descoberta (problema, solução atual, disposição a pagar) | F1 | Notas estruturadas | Pelo menos 1 entrevista com quem aprova compra de TI |
| COM-05 | Fechar primeiro piloto (gratuito ou subsidiado) | Todos | Contrato assinado + RoE assinado | Piloto com G0 completo |

---

## Fase 3 — G1: Piloto assistido (4–8 semanas após G0)

Objetivo: entregar avaliação real para um cliente com dados reais e aprender.

| ID | Tarefa | Responsável | Evidência |
|---|---|---|---|
| G1-T01 | Jobs duráveis: tabela `jobs` com leases, status, recovery | Backend | Job em andamento sobrevive a reinício |
| G1-T02 | Cancelamento real de job | Backend | `POST /api/scans/{id}/cancel` para worker |
| G1-T03 | Cobertura estruturada por job (tentados/testados/erros) | Backend | Resultado inclui metadados de cobertura |
| G1-T04 | Timeout global de job | Backend | Job com >10min é cancelado; estado persiste |
| G1-T05 | MFA para contas admin | Backend | Admin sem MFA bloqueado em produção |
| G1-T06 | Expiração de engagement (validade do escopo) | Backend | Scan com engagement expirado retorna 403 |
| G1-T07 | Logging estruturado com correlation_id | Backend/Ops | Log de erro rastreável por request_id |
| G1-T08 | Backup automático diário + alerta de falha | Ops | Backup executado; alerta em <5min |
| G1-T09 | Política de retenção de dados + consentimento para AEGIS | Backend/Legal | Configuração por organização |

---

## Fase 4 — G2: Oferta recorrente (após 2+ pilotos com Diagnóstico)

Objetivo: ciclo completo descoberta → correção → revalidação.

| ID | Tarefa | Evidência |
|---|---|---|
| G2-T01 | IDs estáveis de achados (fingerprint entre avaliações) | Mesmo achado em 2 avaliações tem mesmo ID |
| G2-T02 | Ciclo de correção: responsável, prazo, status, revalidação | Cliente fecha loop sem intervenção ASTRO |
| G2-T03 | Histórico comparável (ausência ≠ correção) | Ausência mostra "não detectado", não "corrigido" |
| G2-T04 | Métricas de custo por cliente (infra + IA + suporte) | Planilha com custo real após 3 clientes |
| G2-T05 | RPO/RTO documentados e testados | Restore completo em <X horas comprovado |

---

## Fase 5 e além — G3 (somente após G2 validado com clientes)

Itens que não bloquam nada agora:
- Conector local (enrollment, revogação)
- Billing real (Stripe)
- Onboarding autônomo
- Migração SQLite → PostgreSQL (somente se volume exigir)
- Multi-worker estável
- E2E browser tests

**Não planejar datas para G3 antes de ter pelo menos 3 clientes pagantes em G2.**

---

## O que não fazer agora

- Não migrar para PostgreSQL, React, FastAPI, Redis, Celery sem requisito real
- Não implementar MFA antes de G0 completo
- Não abrir cadastro público antes de G1
- Não integrar Stripe antes de 3 clientes pagando manualmente
- Não construir conector antes de G2 validado
