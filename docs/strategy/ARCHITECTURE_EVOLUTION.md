# ASTRO Cyber — Evolução da Arquitetura

Data: 2026-10-18. Descreve estado atual verificado e arquitetura alvo com decisões justificadas.

---

## 1. Arquitetura atual (verificada)

```
┌────────────────────────────────────────────────────────┐
│  Browser (SPA)                                         │
│  index.html + static/cymag.js                         │
│  static/cymag-demo.js (modo demo, sem backend)        │
└────────────────┬───────────────────────────────────────┘
                 │ HTTP (Flask dev server)
┌────────────────▼───────────────────────────────────────┐
│  Flask app (run.py → app/__init__.py)                  │
│  Blueprints: auth / scans / autonomous / engagements   │
│              owner / billing / reports / admin / main  │
│  CSRF: app/csrf.py                                     │
│  Rate-limit login: app/auth/ratelimit.py (em memória)  │
│  Scope: app/scope.py (tenant-scoped helpers)           │
├────────────────────────────────────────────────────────┤
│  core/ (sem dependência Flask)                         │
│  scanner.py → Go binary / Nmap / socket fallback       │
│  exploit_engine.py (checks, perfil defensivo ativo)    │
│  business.py (estimativas financeiras)                 │
│  plans.py (catálogo de planos)                         │
│  severity.py (peso de severidade)                      │
├────────────────────────────────────────────────────────┤
│  SQLite (instance/cymag.db)                           │
│  Tabelas: accounts, users, engagements, scans,         │
│           findings, audit_log, budget_decisions        │
│  Jobs: threads em memória (volatil)                    │
├────────────────────────────────────────────────────────┤
│  app/ai/aegis.py → Groq API / fallback offline         │
│  instance/ai_config.json (chave em texto puro — A11)  │
└────────────────────────────────────────────────────────┘
```

**Limitações críticas do estado atual:**
- Jobs em memória: reinício perde avaliação em andamento
- Chave IA em texto puro
- Rate-limit de login em memória (não funciona com múltiplos workers)
- AEGIS aceita payload livre do cliente (não finding_id)
- Sem cobertura estruturada (o que foi testado, o que não foi)
- Servidor Flask dev: não adequado para produção

---

## 2. Arquitetura alvo (incremental)

### Fase S0–S1 (próxima, antes de piloto)

```
┌─────────────────────────────────────────────────────────┐
│  Browser (SPA — sem mudança)                            │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTPS (gunicorn/waitress)
┌─────────────────────▼───────────────────────────────────┐
│  Flask app (mesma estrutura, hardening adicional)       │
│  + jobs_table: tabela SQLite com leases                 │
│  + worker thread interna lê/escreve na jobs_table       │
│  + AEGIS recebe finding_id, não payload livre           │
│  + chave IA cifrada com CYMAG_AI_SECRET env var         │
│  + rate-limit em SQLite (não em memória)                │
├─────────────────────────────────────────────────────────┤
│  SQLite (sem ORM)                                       │
│  + jobs (id, account_id, status, lease_until, attempts, │
│           result, cobertura, started_at, finished_at)   │
│  + migrações versionadas (forward-only idempotente)    │
│  Sem PostgreSQL nesta fase                              │
└─────────────────────────────────────────────────────────┘
```

### Fase S2–S3 (após primeiros pilotos)

```
┌──────────────────────────────────────────────────────────┐
│  Browser (SPA, UX por perfil completo)                   │
└────────────────────┬─────────────────────────────────────┘
                     │ HTTPS
┌────────────────────▼─────────────────────────────────────┐
│  Flask app                                               │
│  + network_id: identificação de rede por organização    │
│  + ativos/serviços/achados com IDs estáveis             │
│  + fingerprint entre avaliações                         │
│  + ciclo correção: responsável, prazo, revalidação      │
├──────────────────────────────────────────────────────────┤
│  PostgreSQL (migração após testes de backup/restore)     │
│  Quando: antes de expansão comercial / múltiplos workers │
│  Requisito: migração verificada e restore testado        │
└──────────────────────────────────────────────────────────┘
```

### Fase S4 (após G2 validado)

```
┌──────────────────────────────────────────────────────────┐
│  ASTRO Web (SaaS)  ←────────────────────────────────┐   │
│                                                     │   │
│  Worker externo isolado ────→ Ativos públicos       │   │
│                                                     │   │
│  ASTRO Connector (VM/container na LAN do cliente)   │   │
│  └─ HTTPS de saída: busca job + envia evidências ───┘   │
│  └─ Scanner local: escopo interno autorizado            │
└──────────────────────────────────────────────────────────┘
```

---

## 3. Decisões técnicas com justificativas

### D-T01: Flask permanece

**Decisão:** Não migrar para FastAPI, Next.js ou microsserviços.
**Justificativa:** Flask funciona, blueprints são organizados, equipe conhece. Migração exigiria reescrever todos os blueprints e testes sem adicionar valor para o cliente.
**Revisão:** Se throughput se tornar gargalo medido (não hipotético) ou time crescer para >5 engenheiros.

### D-T02: SQLite permanece até G1/G2

**Decisão:** Não migrar para PostgreSQL antes de ter pilotos com dados reais.
**Justificativa:** SQLite com WAL suporta carga de PME; migração exige backup/restore testados; risco de regressão alto antes de ter carga real para justificar.
**Condição para PostgreSQL:** múltiplos workers simultâneos medidos OU dados de >5 clientes simultâneos em SQLite causando contenção comprovada.
**Requisitos da migração:** script de migração, test de restore, fixtures de dados, rollback documentado.

### D-T03: Jobs como tabela SQLite (sem Redis/Celery)

**Decisão:** Tabela `jobs` com leases no SQLite; worker thread interna.
**Justificativa:** Redis/Celery adicionam operação (deploy, monitoramento, restart) sem necessidade medida. Tabela com lease resolve durabilidade, deduplicação e recuperação para o volume esperado.
**Limitação:** lease não garante exatamente-uma-vez; implementar idempotência nos workers.
**Revisão:** se múltiplos workers em máquinas diferentes forem necessários.

### D-T04: Conector depois de jobs duráveis

**Decisão:** Não construir conector antes de ter jobs/worker internos funcionando.
**Justificativa:** Conector usa o mesmo protocolo de jobs/eventos. Construir protocolo antes de validar internamente cria dívida técnica.
**Quando:** Após G1 (jobs duráveis comprovados) e após necessidade validada com cliente piloto.

### D-T05: AEGIS recebe finding_id, não payload livre

**Decisão:** Refatorar `app/scans/routes.py` para passar finding_id autorizado ao AEGIS.
**Justificativa:** Payload livre do frontend é vetor de prompt injection; finding_id garante que o conteúdo veio do banco do tenant.
**Implementação:** validar finding_id pertence ao account_id da sessão; buscar dados do banco; montar prompt no backend.

### D-T06: Chave IA cifrada com variável de ambiente

**Decisão:** `instance/ai_config.json` armazena chave cifrada com `CYMAG_AI_SECRET`; nunca em texto puro.
**Justificativa:** Se servidor comprometido, chave IA não vaza sem a env var.
**Implementação:** Fernet (cryptography) ou similar; env var obrigatória em produção como CYMAG_SECRET_KEY.

### D-T07: Servidor gunicorn/waitress em produção

**Decisão:** Flask dev server apenas em desenvolvimento; gunicorn (Linux) ou waitress (Windows) em produção.
**Justificativa:** Flask dev server é single-threaded, sem signal handling, sem logging estruturado.
**Custo:** Baixo; adicionar `requirements.txt` e documentação de deploy.

---

## 4. Migrações planejadas

| Migração | Dependência | Estratégia |
|---|---|---|
| Adicionar `jobs` e `job_events` ao SQLite | Nenhuma | Forward-only; coluna nova nullable |
| Adicionar `network_id` aos scans/engagements | S2 | Nullable; backfill explícito |
| Tabela `assets` e `services` estáveis | S2 | Nova; não altera `findings` existentes |
| `findings` com `finding_fingerprint` | S2 | Coluna nova nullable; preenchida em novas avaliações |
| SQLite → PostgreSQL | G2 | Dump/restore; fixture de teste; cutover com manutenção |

---

## 5. O que não fazer

- Não migrar banco em produção sem backup/restore testado
- Não rodar scanner com as permissões do processo web
- Não expor porta do banco ao exterior
- Não armazenar secrets em arquivos versionados
- Não expandir para microsserviços sem gargalo medido
