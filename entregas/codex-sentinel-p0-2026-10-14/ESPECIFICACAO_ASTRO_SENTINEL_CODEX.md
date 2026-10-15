# ASTRO SENTINEL — ESPECIFICAÇÃO DE PRODUTO E ORDEM DE IMPLEMENTAÇÃO PARA CODEX

> **Status:** direção de produto e decisões técnicas definidas pelo responsável pela especificação. A Codex é a implementadora, auditora das alterações e responsável pelos testes.  
> **Repositório de origem:** https://github.com/alefkaue/astro.git  
> **Data-base:** 14/10/2026.  
> **Escopo da missão:** amadurecer **o produto e o código**, não constituir uma empresa, criar um banco, nem substituir tudo por um novo projeto.  
> **Aviso:** esta especificação é um plano de engenharia. Ela não certifica o sistema como pronto para produção. A conformidade e a segurança só serão consideradas verificadas após evidências, testes e revisão independente apropriada.

---

## 0. LEIA ISTO PRIMEIRO: PAPEL DA CODEX

Você é responsável por **IMPLEMENTAR** uma especificação já definida. Não volte à fase genérica de brainstorming. Não responda apenas com ideias, PDFs, tabelas e relatórios: **faça alterações reais no repositório e execute os testes**.

1. Inspecione a **cópia local atual**, seus commits, arquivos, testes, esquemas, rotas, dependências e `README.md`, `PLATAFORMA.md`, `INSTALL.md` e documentos adicionais; **não confie somente no GitHub ou nesta especificação**, que representam um retrato anterior.
2. Crie um baseline de funcionamento, inventário e testes existentes antes de editar. **Não descarte trabalho não commitado**. Registre o hash do commit de origem, modificações existentes, ambiente e testes executados.
3. **Preserve o que funciona**. Prefira refatoração incremental com testes de regressão em vez de reescrita total. Nunca remova funcionalidades sem explicar a migração e a alternativa.
4. Execute a missão por **fases em ordem**, completando e testando cada incremento. Crie commits pequenos e descritivos em branch de trabalho se o ambiente permitir; **não dê push, faça deploy público ou rode scans externos sem autorização**.
5. Ao encontrar uma divergência entre código real e descrição abaixo, trate o código como evidência de implementação, mas mantenha **as decisões de produto e segurança deste documento**. Registre a divergência em `docs/IMPLEMENTATION_LOG.md`.
6. Se algo depender de domínio, pagamentos, certificado, provedor de nuvem, credenciais ou aprovação humana, **implemente interfaces/configuração de forma segura**, documente o bloqueio e use fixtures locais. Não invente êxito, cliente, preço, integração ou deploy.
7. Se uma tarefa não puder ser concluída, encerre a fase com código compilável, testes pertinentes e um registro exato de pendências, não com falsa conclusão de “100% pronto”.
8. **Codex trabalha em todas as áreas AGORA**; três desenvolvedores humanos assumirão áreas específicas DEPOIS. Não separe o produto em três repositórios/microsserviços apenas por isso.

### Critério de sucesso da missão

Um usuário de demonstração percorre o fluxo completo, com dados fictícios e sem acesso externo: **criar organização → aprovar ativos e escopo → vincular agente simulado → solicitar avaliação de laboratório → acompanhar execução → visualizar evidências → priorizar achados → atribuir correção → revalidar → gerar relatório**. Todo recurso real é isolado por organização, auditado e controlado por permissão. Os testes de segurança devem falhar com acesso cruzado e devem passar após as correções. O produto deve permanecer utilizável sem IA e sem integração de cobrança.

---

## 1. DECISÕES FECHADAS DE PRODUTO

### 1.1 Identidade e posicionamento

- **Empresa/marca-guarda-chuva proposta:** ASTRO. **Linha:** ASTRO Cyber. **Nome comercial do produto:** **ASTRO Sentinel**.
- **`cymag_saas` permanece como nome do repositório e identificador legado durante a migração**. É aceitável preservar rotas, arquivos e nomes internos `cymag` onde removê-los causaria quebra. Crie um plano de rebranding gradual, incluindo arquivos de tradução e configuração de nome. Não faça alterações destrutivas nem finja que houve registro de marca/domínio.
- **Frase de produto:** “Visibilidade contínua da exposição, priorização baseada em evidências e acompanhamento da correção para empresas que não têm um grande time de segurança.”
- **Cliente inicial:** PMEs com infraestrutura própria/híbrida e/ou pequeno time de TI, e consultorias que atendem essas empresas. Não construir simultaneamente uma plataforma para consumidor doméstico, SIEM completo, EDR, antivírus ou um banco.
- **Valor principal:** inventário técnico, avaliações autorizadas, evidências verificáveis, priorização acionável, responsável/prazo e revalidação. **Não prometer prevenção de incidentes, pentest completo automático nem previsão monetária precisa**.
- **Diferencial verificável:** mesma descoberta traduzida para analista (evidência técnica), TI (plano de correção) e gestor (prioridade, exposição e andamento). Evitar marketing de ROI automático baseado em números arbitrários.

### 1.2 Formatos de entrega — DECISÃO DEFINITIVA

| Superfície | Público | Decisão | Escopo |
|---|---|---|---|
| **Web SaaS responsivo** | Clientes, equipe técnica, gestores, consultores autorizados | **Obrigatória e principal** | Administração, ativos, escopo, jobs, achados, remediação, relatórios, IA, equipes, configuração |
| **Agente local Windows** (`.exe`) | TI/administrador do cliente | **Obrigatório no produto-alvo; protótipo verificável antes de distribuição** | Executa verificações autorizadas na rede do cliente e reporta resultados; sem GUI própria |
| **Agente local Linux** (binário/pacote) | TI/administrador do cliente | **Obrigatório no produto-alvo** | Mesma interface/protocolo e segurança do agente Windows |
| **CLI técnica** (`astro-sentinel` ou nome legado temporário) | Analistas e devs | **Obrigatória** | Diagnóstico do agente, inscrição, status, testes em laboratório, logs redigidos; sem bypass de autorização |
| **Desktop gráfico próprio** | — | **Não construir na primeira versão** | Evita duplicação do painel web; reconsiderar só após demanda real |
| **API versionada** (`/api/v1`) | Web e agentes/integrações | **Obrigatória** | Contratos, autenticação, autorização, versionamento, documentação e testes |
| **Demo isolada** | Professores, prospects | **Obrigatória** | Dados inteiramente falsos, sem credenciais reais e sem chamadas de execução a alvos externos |

**Regra:** nunca tratar arquivo `.exe` como “scanner público sem restrições”. O agente não se comunica com um banco de dados remotamente e não aceita comandos arbitrários enviados pela web. Um processo técnico explicitamente registrado pode executar somente tipos de jobs permitidos.

### 1.3 Catálogo fechado de serviços

**Produto de software (funcionalidades recorrentes):**

| Código | Serviço | Resultado mensurável | Inclui | Exclui |
|---|---|---|---|---|
| S1 | **Inventário e exposição** | Ativos identificados, serviços expostos, evolução histórica | Cadastro, descoberta autorizada, identificação técnica, tags, criticidade, comparação entre execuções | Exploração invasiva |
| S2 | **Avaliação contínua de vulnerabilidades** | Achados evidenciados, acompanhados e datados | Verificações de baixo risco, classificação, deduplicação, programação e limite de carga | Garantia de ausência de falhas; exploração agressiva |
| S3 | **Gestão de remediação** | Achados com dono, prazo e status de correção | Backlog, recomendações, responsável, exceções justificadas, validação/reteste | Correção autônoma de máquinas/servidores sem aprovação |
| S4 | **Relatórios técnicos e executivos** | PDF/JSON auditáveis | Método, escopo, limitações, evidências, tendências, recomendações, histórico | “R$ X de prejuízo inevitável” sem fonte/modelo robusto |
| S5 | **AEGIS — copiloto** | Texto explicativo rastreável aos achados | Resumos, sugestões, consultas, rascunhos de correção e explicações para gestores | Execução autônoma de comandos, mudança de escopo, aprovação de risco |

**Serviços humanos, separados do SaaS:**

- **H1 — Diagnóstico assistido / implantação**: consultor ajuda a cadastrar escopo, implantar o agente, interpretar e priorizar resultados; com termo de serviço e aceite.
- **H2 — Pentest sob contrato e regras de engajamento específicas**: processo profissional distinto, com pessoa responsável, planejamento, janelas aprovadas, relatório e critérios de parada. O scanner **não vira automaticamente “pentest completo”**.
- **H3 — Reteste e validação especializada**: confirmação humana de correções críticas, com evidência e parecer.

**Não oferecer agora:** SOC 24/7, MDR, SIEM completo, bug bounty público, red team irrestrito, IA capaz de efetuar exploração sem operador, auto-remediação indiscriminada, scanner externo de qualquer domínio. Registrar esses itens em `docs/ROADMAP_FUTURO.md`, sem fingir que foram implementados.

### 1.4 Planos comerciais sem “cobrança fake”

A plataforma pode apresentar **três pacotes de valor** para estudo de mercado, sem preços inventados:

- **Essencial:** S1 + avaliações manuais de baixo impacto S2 + relatórios básicos S4, limites configuráveis.
- **Profissional:** Essencial + agendamento/monitoramento S2 + fluxo completo S3 + AEGIS S5, se habilitado.
- **Acompanhado:** Profissional + pacote de horas de H1/H3, acordado separadamente; H2 mediante proposta e contrato.

Os limites precisam existir como **entitlements explícitos** (número de ativos, agentes, avaliações, usuários, retenção, uso de IA). A Codex deve deixar preços **“sob validação comercial”**, não inventar valores ou clientes. Não liberar recursos de produção por uma chamada de “trocar plano”. O **modo demonstração** pode simular um checkout, claramente rotulado como simulação; em produção, integrações reais com provedor de pagamentos e webhooks verificados exigirão etapa própria.

---

## 2. ARQUITETURA DEFINIDA (EVOLUIR, NÃO REESCREVER)

### 2.1 Estilo

**Monólito modular Flask** para regras de negócio e API, combinado a **processo worker isolado** para execução assíncrona e **agente local opcional/necessário para redes internas**. PostgreSQL é o banco-alvo de produção; SQLite pode continuar para testes ou transição. Redis + RQ (ou fila de complexidade equivalente **somente se já existir uma tecnologia adequada**) é a escolha preferencial para jobs duráveis. Não exigir Kubernetes, microsserviços, AWS+Azure nem Next.js/React agora.

```text
[Browser - Web App]
        |
       HTTPS
        v
[Flask API / Auth / Tenant / RBAC / Auditoria]---->[PostgreSQL]
        |                      |                        
        +---->[Fila de jobs]---+--->[Worker isolado para tarefas permitidas]
        |                                           |
        +---->[Serviço AEGIS com dados filtrados]   +---->[Scanner Go/Python controlado]
        |
        +---->[API de registro/comunicação segura de agentes]
                                  ^
                                  | TLS + autenticação por agente + polling outbound
                          [Agente Windows / Linux]
                          [rede autorizada do cliente]
```

Se não existir worker, implementá-lo incrementalmente e remover a dependência de threads de requisição como fila principal; se já houver fila persistente, adaptá-la. **Nunca bloquear worker web em scan prolongado**. A API armazena metadados e resultados validados, não aceita resultado com organização arbitrária fornecida pelo agente.

### 2.2 Dependências e fronteiras

- `app/` = APIs, identidade, domínio SaaS, persistência, autorização, apresentação de dados.
- `core/` = lógica técnica pura de verificação, normalização e pontuação, independente de Flask.
- `scanner_go/` = probes e operações permitidas, com entradas/saídas JSON padronizadas; não construir um segundo backend de contas.
- `agent/` (novo, após validar base) = enrollment, polling seguro, execução local, heartbeats, filas limitadas, geração de evidências.
- `worker/` (novo) = consumo controlado de jobs em background, exceções, timeout e retry.
- `static/` = frontend modular; manter JavaScript atual se possível, extrair gradualmente roteador, API client e componentes. Migração de framework só com decisão registrada e benefício comprovado.
- `tests/` = unitários, integração, autorização, contratos, fluxo e2e, segurança e regressão.

**Contrato único de output do scanner:** JSON versionado com `job_id`, `agent_id` opcional, `asset_id`, janela de execução, escopo efetivo, modalidade, check_id/version, estado, achados, `confidence`, referências, evidências saneadas e checksum. Validar schema na origem e no servidor. Não confiar em IDs e `tenant_id` do payload.

### 2.3 Ambientes

- **Local:** dev com `.env.example`, fixtures fictícias, banco local, agente simulado, verificações contra alvo de teste explicitamente isolado, sem Internet obrigatória.
- **CI:** dependências pinadas/lock, testes sem rede pública, análise estática e migrações de banco.
- **Staging:** tenant fictício, HTTPS, logs, observabilidade, backup/restore, integrações sandbox.
- **Produção:** somente após checklist, contrato, infraestrutura, gestão de segredos, testes independentes e autorização do time.

**Containers:** mínimo recomendado para desenvolvimento/implantação: app/API, worker, PostgreSQL e Redis; agente rodando separadamente na rede do cliente; reverse proxy/TLS na implantação adequada. Não fingir que a necessidade de quatro processos significa quatro empresas ou quatro “serviços comerciais”. `docker compose` para uso local/staging, com perfis e healthchecks. Proibir debugger do Flask e segredos padrão em produção.

---

## 3. SEGURANÇA — TAREFAS P0 QUE BLOQUEIAM TODO O RESTO

A inspeção pública do repositório anterior mostrou **sinais concretos de falhas de autorização**. CONFIRME NA CÓPIA ATUAL ANTES DE ALTERAR:

- `app/db.py`: `list_engagements()` aparentemente enumera engagements de forma global, sem organização.
- `app/engagements/routes.py`: `GET /api/engagements` e `GET /api/engagements/<id>` verificam login mas não demonstram filtragem por tenant ou propriedade.
- `app/db.py`: `get_scan_findings(scan_id)` aparentemente busca por ID sem contexto de organização.
- `app/scans/routes.py`: rota de findings aparentemente não valida propriedade do scan antes da consulta.
- Os documentos mencionam **contas e senhas de demonstração previsíveis**, **checkout simulado**, scanner autônomo e API key do AEGIS configurada no painel. Esses recursos não podem atravessar a fronteira de produção sem revisão.

**Não considere a lista exaustiva e não anuncie uma vulnerabilidade confirmada sem reproduzir em testes isolados.**

### P0.1 Identidade, isolamento e permissões

1. Introduzir `organization_id` em **todos** os recursos vinculados a cliente: ativos, agentes, escopos/engagements, jobs, scans, findings, evidências, relatórios, recomendações, decisões, integrações, chaves, assinaturas e auditoria. Migrar dados com plano que não crie associação arbitrária.
2. No acesso a qualquer objeto, exigir `tenant ativo + usuário com vínculo e permissão + recurso pertencente ao tenant`, na camada de serviço e de consulta; 404/403 padronizados sem revelar dados externos. UUID não substitui autorização. Nunca aceitar `organization_id` enviado pelo cliente como autoridade de acesso.
3. Definir papéis da ORGANIZAÇÃO: `owner` (responsável), `admin` (gestão de equipe/escopo), `analyst` (triagem/verificação autorizada), `viewer` (somente leitura). Funções específicas exigem permissões adicionais como `scan:execute`, `scope:approve`, `report:export`, `billing:manage`. **Admin da plataforma** é outro domínio, com acesso auditado e sem acesso irrestrito a conteúdos de clientes por padrão.
4. Consultor externo deve receber **delegação com organização, permissões, prazo de validade, justificativa e revogação**, não `staff=true` com acesso global.
5. Sessões seguras (HttpOnly, Secure em HTTPS, SameSite apropriado, rotação após login, logout/invalidação, CSRF em ações com cookie), rate limiting, proteção contra brute force, política de senha, recuperação segura e MFA para funções críticas antes do piloto real.
6. E-mails, senhas padrão e `seed_demo` só no modo explicitamente marcado `DEMO=true`/fixtures; produção **falha ao iniciar** se houver segredo padrão, debug ligado, demo habilitada ou banco incompatível com exigências de produção.

### P0.2 Escopo e execução — três checagens independentes

Cada job exige: (a) comprovação/documentação de titularidade/autorização dos alvos; (b) escopo CIDR/host/protocolo válido, janela, responsáveis, intensidade e expiração; (c) autorização específica do usuário e tenant; (d) validação pelo **backend antes de enfileirar**, pelo **worker antes de despachar** e pelo **agente imediatamente antes de cada conexão**. Revogações param jobs pendentes/ativos (kill switch).

- Tratar DNS rebinding, CNAME, redirects e resolução dinâmica: revalidar destino efetivo a cada conexão/redirecionamento. A API SaaS de nuvem não deve acessar IP privado, loopback, link-local, metadata/cloud endpoints ou namespaces internos, salvo mecanismos isolados e autorizados para o caso de uso; **redes privadas autorizadas são examinadas pelo agente local**, não via SSRF do servidor da plataforma.
- Jobs têm allowlist de **tipos de verificação**, orçamento de pacotes/requests, concurrency, timeout, TTL, janela, IDs únicos, replay protection e modo cancelável. Sem shell arbitrário, credenciais embutidas, payloads exploratórios agressivos padrão ou execuções desassistidas invasivas.
- Modos **`inventory`**, **`safe_assessment`**, **`manual_pentest`**: somente os dois primeiros automatizados no SaaS inicial. `manual_pentest` representa workflow contratado/humano e **não libera exploração automatizada**.
- Evidências podem conter IPs, nomes de usuário e banners sensíveis: minimização, redaction, acesso restrito, retenção curta configurável, criptografia de dados sensíveis e trilha de auditoria. Logs não contêm tokens, senha, payloads confidenciais ou resposta integral de sistemas.
- Teste de laboratório obrigatório: job rejeitado por alvo fora do escopo, tenant errado, autorização vencida, janela fechada, agente revogado ou usuário sem permissão.

### P0.3 API, arquivos e IA

- Validação estrita de entrada e esquema, limites de tamanho, validação de upload, headers e CORS restritos, controles para SSRF/SQL injection/XSS/template injection/CSRF, gestão de dependências e erros sem stack trace.
- Relatórios, exports, prints/evidências e downloads precisam de autorização **no objeto** e links temporários, nunca URL previsível pública. Incluir testes de acesso cruzado aos anexos.
- AEGIS é **somente leitura e sugestão** na versão inicial: não executa shell, altera escopo, autoriza pentest, fecha achado ou modifica contas. Dados externos são **entrada não confiável**. Tratar prompt injection, disclosure, custos e retenção do provedor. Toda resposta técnica deve indicar fonte, confiança/limitações e referências aos `finding_id` reais; nunca fabricar CVE, evidência ou risco monetário. API keys cifradas com segredo gerenciado ou preferencialmente variáveis/secret manager, nunca JSON plaintext exposto ou incluído em export/log.
- Política de consentimento para envio de evidências a LLM externo. **Sem IA configurada, o fluxo completo de scan/triagem/relatórios ainda funciona** com análise determinística identificada como tal.

### Testes P0 mínimos (AUTOMATIZE)

```
Tenant A não lista, lê, edita, cancela, exporta nem obtém metadados de recursos do Tenant B;
User viewer não inicia scans; analyst não aprova próprio escopo sem permissão;
Owner A não acessa admin da plataforma;
Consultor com delegação vencida não acessa recursos;
User sem login não obtém achados, pdfs, artefatos ou links;
Alterar scan_id/engagement_id/report_id/agente_id não altera o tenant efetivo;
Escopo revogado e target fora do escopo nunca chegam ao executor;
Agente revogado, token expirado e job assinado com alvo diferente são rejeitados;
Demo e senhas padrão não carregam em modo produção;
Chave de IA, cookie e token não aparecem em response JSON nem logs.
```

**Regra de interrupção:** falhou qualquer teste crítico de isolamento, escopo ou credenciais? Não adicionar novas capacidades de scanner, não abrir acesso externo e não anunciar “pronto”.

---

## 4. EXPERIÊNCIA DO USUÁRIO E DESIGN: NAVEGAÇÃO DEFINIDA

### 4.1 Design estrutural (mais importante que “deixar bonito”)

Interface em **português do Brasil**, responsiva, sóbria e técnica, preferencialmente conservando a paleta/identidade visual boa já existente. Usar padrão: **barra superior** (organização ativa, status de agente, notificações, perfil), **menu lateral** com seções agrupadas, **conteúdo principal** com breadcrumbs/título/ação contextual, filtros persistentes e estados de carregamento/vazio/erro/sucesso. Sem tudo espremido em um dashboard monolítico. O contexto de organização é sempre visível.

**Site público — sem dados reais:** `/` Início, `/produto`, `/solucoes`, `/planos`, `/seguranca`, `/documentacao`, `/contato`, `/login`, `/demo`. Nunca misturar o site institucional com a app autenticada.

**App do cliente (`/app` e rotas equivalentes):**

| Seção | Páginas obrigatórias | Pergunta respondida / ação |
|---|---|---|
| **Visão geral** | Resumo, tendência e pendências | O que mudou? Quais 3 ações são prioritárias? |
| **Ativos** | Lista, detalhe, tags, criticidade, histórico | O que pertence ao escopo? Onde está exposto? |
| **Agentes** | Lista, instalar/vincular, saúde, logs limitados, revogar | Há executor autorizado e saudável? |
| **Avaliações** | Criar, agendar, histórico, detalhe, execução ao vivo | O que foi verificado, quando, por quem e sob qual autorização? |
| **Achados** | Tabela com filtros, detalhe/evidência, triagem, exceções | Qual problema, qual evidência, qual impacto e confiança? |
| **Correções** | Backlog, responsável, SLA, checklist, solicitar reteste | Quem corrige, até quando, e como comprovar? |
| **Relatórios** | Executivo, técnico, exportar, histórico e versões | O que foi descoberto, corrigido e ainda é risco? |
| **AEGIS** | Assistente contextual, histórico permitido e citações | O que significa este achado e como priorizar? |
| **Atividade** | Eventos filtráveis e trilha de auditoria (perm.) | Quem fez o quê e quando? |
| **Configurações** | Empresa, membros/papéis, escopos, integrações, plano, retenção | Quais regras e limites estão em vigor? |

**Painel interno da plataforma** em `/platform-admin` separado e restrito: status técnico/saúde, tenants (metadados mínimos), falhas operacionais, planos, assistência com acesso just-in-time e auditoria. **Nunca** servir console de suporte como se fosse conta cliente global.

### 4.2 Fluxos ponta a ponta obrigatórios

**F1 — Primeira utilização:** registro/login → criar/selecionar organização → confirmar responsável → aceitar termos → adicionar escopo e comprovar autorização → cadastrar ativos → escolha entre agente ou demo → avaliação de laboratório. Wizard com progresso, validações e salvamento.

**F2 — Avaliação:** ativo autorizado → política/método `inventory` ou `safe_assessment` → visualizar custo/impacto estimado da execução (não custo de incidente) → autorizar e agendar → job criado → atualizações estado → finalizar/cancelar → achados deduplicados → logs e evidências.

**F3 — Correção:** achado confirmado ou potencial → responsável e prazo → plano concreto → em progresso → resolução declarada → reteste → resolvido ou reaberto. Exceção de risco requer motivo/aprovador/prazo e registro.

**F4 — Gestor:** tela não técnica → ativos cobertos vs não cobertos, maiores riscos confiáveis, tendência, correções atrasadas, aprovações pendentes e exportação. Não apresentar falsa precisão de perda financeira.

**F5 — Cliente de consultoria:** convite/relação de escopo por prazo → acesso limitado aos artefatos permitidos → comentários e entregas com trilha de auditoria → revogação.

**F6 — Demonstração:** `static/cymag-demo.js` ou fixture equivalente deve reproduzir os contratos do backend, sempre com **banner DEMONSTRAÇÃO — DADOS FICTÍCIOS**, sem misturar tokens, banco, documentos ou agentes reais. Não usar senhas fixas em produção.

### 4.3 Componentes e regras de interface

- Filtros por status, severidade, ativo, projeto, responsável e período; navegação teclado, acessibilidade, contraste e layouts mobile/tablet/desktop.
- Tabela de achados: título, ativo, severidade, confiança, evidência, KEV/EPSS quando há CVE validado, status, responsável, detectado em, próxima ação.
- Detalhe do achado: resumo executivo, evidência reproduzível **não sensível**, regra usada e versão, referências, impacto e alcance, recomendação, exceções, timeline e reteste. Mostrar “hipótese / requer validação” quando não confirmado.
- Falha na IA não esconde relatórios ou dados da avaliação.
- Não exibir números de negócio sintéticos como se fossem perdas comprovadas. Em demonstração, rotular valores como ilustrativos.
- Design system com tokens, componentes compartilhados, cabeçalho/estados padronizados. Preservar cores existentes quando adequadas; mudar arquitetura de páginas antes de reconstruir estética por impulso.

---

## 5. CONTRATOS DE DADOS, API E ESTADOS

### 5.1 Modelo de dados sugerido (migrar progressivamente)

`organizations`, `users`, `memberships`, `roles/permissions`, `invites`, `api_tokens` (hash), `agents`, `agent_credentials`, `assets`, `scope_authorizations`, `engagements`, `assessments`, `jobs`, `job_events`, `scan_results`, `findings`, `finding_evidence`, `remediation_tasks`, `finding_status_history`, `risk_exceptions`, `reports`, `report_versions`, `integrations`, `plans`, `subscriptions`, `entitlements`, `usage_events`, `audit_events`, `ai_requests` (sem conteúdo sensível desnecessário).

Regras: FK/index para `organization_id` onde aplicável; unicidade por tenant quando apropriado; timestamps timezone-aware; deleção/retention previsível; logs append-only protegidos; migração do banco existente com backup e rollback/testes; nenhum recurso órfão atribuído silenciosamente a tenant.

### 5.2 Estados fixos

- **Autorização/escopo:** `draft -> pending_approval -> approved -> revoked|expired` (edições exigem nova aprovação; aprovar escopo não concede permissão automática a executar).
- **Agente:** `pending -> active -> degraded|offline -> revoked`.
- **Job:** `queued -> dispatched -> running -> succeeded|partially_succeeded|failed|cancelled|expired`, com transições idempotentes e evento auditado; erro e retry não duplicam a execução.
- **Finding:** `open -> acknowledged -> in_progress -> pending_retest -> resolved`; alternativas `accepted_risk` (prazo e autoridade), `false_positive` (justificativa), `reopened`. Guardar histórico, não apagar evidências.

### 5.3 API versionada mínima

Não duplicar rotas sem migração. Introduzir `/api/v1` e deprecar endpoints legados com adaptadores temporários e testes de compatibilidade. Recursos desejados:

```
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
GET    /api/v1/me
GET    /api/v1/organizations
POST   /api/v1/organizations
GET    /api/v1/organizations/{id}/members
POST   /api/v1/organizations/{id}/invites
GET    /api/v1/assets
POST   /api/v1/assets
GET    /api/v1/scopes
POST   /api/v1/scopes
POST   /api/v1/scopes/{id}/request-approval
POST   /api/v1/scopes/{id}/approve
POST   /api/v1/scopes/{id}/revoke
GET    /api/v1/agents
POST   /api/v1/agents/enrollment-tokens
POST   /api/v1/agents/enroll
POST   /api/v1/agents/{id}/revoke
GET    /api/v1/assessments
POST   /api/v1/assessments
POST   /api/v1/assessments/{id}/runs
GET    /api/v1/jobs/{id}
POST   /api/v1/jobs/{id}/cancel
GET    /api/v1/findings
GET    /api/v1/findings/{id}
PATCH  /api/v1/findings/{id}
POST   /api/v1/findings/{id}/retest
GET    /api/v1/remediations
PATCH  /api/v1/remediations/{id}
GET    /api/v1/reports
POST   /api/v1/reports
GET    /api/v1/reports/{id}/download
POST   /api/v1/aegis/explain
GET    /api/v1/audit-events
GET    /api/v1/entitlements
```

Todos os recursos são **tenant-scoped**, com esquema de erro coerente (`code`, `message`, `request_id`) e paginação/filtros. Separar **endpoints de controle de agente** em namespace próprio e política de autenticação própria. Gerar OpenAPI e testes de contrato antes de refatorar profundamente o cliente JS. O exemplo acima descreve **funções pretendidas**, não afirma que essas rotas já existem.

### 5.4 Pontuação e deduplicação

- Severidade técnica baseada em CVSS **quando há CVE/avaliação pertinente e fonte confiável**; registrar a versão do CVSS e vetor se disponíveis.
- Priorização de trabalho combina criticidade do ativo, exposição, confiança da detecção, CISA KEV quando verificado, probabilidade EPSS quando disponível, compensações e impacto de negócio descrito qualitativamente. Documentar pesos, fontes e comportamento sem dados; não usar um escore mágico sem explicação.
- `finding_fingerprint = tenant + asset + service/protocol + check_id + condição técnica normalizada`, com CVE quando aplicável, preservando eventos de observação. Não criar 30 cards iguais toda vez que um scan roda.
- Estimativa financeira de incidentes só quando o próprio cliente fornecer valores/premissas e o modelo tiver justificativa; caso contrário mostrar **faixas ilustrativas explicitamente marcadas** ou somente priorização ordinal. Não anunciar “cada R$1 economiza R$X” como dado real.

---

## 6. AGENTE LOCAL E CLI — ESPECIFICAÇÃO DE COMPORTAMENTO

### 6.1 Agente

- **Preferência:** agente multiplataforma em Go (binário Windows/Linux) porque o repositório já dispõe de motor Go. O Python existente permanece útil para orquestração/checks no worker. Primeiro criar interface/protocolo simulado local; então binário, testes e empacotamento. Se houver impedimento material, documentar e implementar versão funcional equivalente com plano de migração; **não abandonar a exigência de agente remoto seguro**.
- Inscrição com token de uso único/TTL curto gerado por um admin da organização, que obtém credencial própria rotacionável e vinculada ao tenant, revogável. Nunca incluir segredo mestre ou senha de cliente no executável.
- Comunicação **somente outbound** para API aprovada via TLS, verificação de certificado, sem porta de gestão escutando aberta no cliente por padrão.
- Heartbeats, versão, OS, último status, tempo de execução e capacidades suportadas; **não coletar arquivos do cliente sem propósito/autorização**.
- Busca de job com tenant/agent/escopo vinculados, expiração/nonce/assinatura ou autenticação equivalente, checagem local de alvo e modalidade; execução por plugins allowlisted, timeout e rate limit; retorno de progresso e evidências saneadas; cancelamento idempotente.
- Instalação manual documentada, execução em modo de menor privilégio possível, configuração segura em diretório protegido e descarte/rotação de credenciais. Windows Service/systemd pode ficar como endurecimento da fase de distribuição, sem exigir privilégio administrativo injustificado.
- MVP do agente deve compilar em Windows e Linux, ou ter evidência clara e rastreável dos obstáculos de cross-compile; não declarar `.exe` pronto apenas por gerar um arquivo.

### 6.2 CLI

Comandos de produto definidos (ajustar nomenclatura por compatibilidade, com documentação):

```
astro-sentinel version
astro-sentinel doctor
astro-sentinel enroll --url https://... --token <token_curto>
astro-sentinel status
astro-sentinel logs --redact
astro-sentinel test-connection
astro-sentinel run --fixture ./fixtures/lab.json   # APENAS modo de laboratório
astro-sentinel revoke-local
```

Sem `scan --target <qualquer-coisa>` irrestrito. Se existir CLI legada de scanner, encapsular exigência de arquivo de autorização/ambiente de laboratório e respeitar escopo. Instruções de instalação específicas para Windows e Linux, versões, checksums e assinatura de binário como etapa posterior de release.

---

## 7. AEGIS — COPILOTO, NÃO OPERADOR AUTÔNOMO

AEGIS possui quatro modos fechados: (1) **Explicar achado** em linguagem acessível; (2) **Sugerir remediação** com referências; (3) **Priorizar backlog** com dados reais e hipóteses explícitas; (4) **Rascunhar relatório** mantendo controle humano antes da publicação. O modelo pode recomendar testes adicionais, mas **jamais executá-los**.

- Backend escolhe previamente quais dados autorizados enviar; LLM não recebe `tenant_id` arbitrário e não consulta outras organizações.
- Saídas estruturadas e validadas, sem HTML/JS bruto não saneado; prompt injection tests com banners/webpages maliciosos tratados como dados, não instruções.
- Mostrar provedor, status habilitado, custo/limite configurado e quando resposta é fallback determinístico. Limites de tokens, timeout e fallback.
- Nenhum “resultado descoberto pela IA” vira achado confirmado sem check/evidência real; IA não inventa CVEs, timestamps, provas nem economias.
- Registro de consentimento, minimização, mascaramento e exclusão de conteúdo sensível. Prompt e resposta em logs só se política permitir, com retenção curta e saneamento.

---

## 8. FASES DE IMPLEMENTAÇÃO — EXECUTE NA ORDEM

### FASE 0 — BASELINE E MAPA DE DÍVIDA (não parar aqui)

**Faça:** levantar árvore, versões, dependências, rotas, RBAC, tabelas, frontend, funcionalidades reais versus demo, testes, limites de execução e documentação atual. Rodar `pytest`, build Go e checks existentes. Criar `docs/BASELINE_2026.md`, `docs/FEATURE_MATRIX.md`, `docs/ADR/0001-product-and-architecture.md` e backlog priorizado com referência a caminho/linha. Medir riscos, não apenas opinar. **Entregar:** baseline + testes reproduzíveis + tarefas P0/P1/P2.

### FASE 1 — P0 SEGURANÇA + MULTITENANCY (bloqueia todas as demais)

**Faça:** adicionar tenant real, migrar o banco, revisar handlers/consultas de object authorization, segregação de papel de suporte, sessão, demo, segredos, RBAC de recursos, escopos, isolamento da IA e exportação. **Teste:** matriz de acesso cruzado e casos negativos, fixtures com 2+ organizações. **Aceite:** 0 bypass crítico reproduzível nesses testes; testes verdes; migração reversível/backup; demo separado.

### FASE 2 — PRODUTO E CONTRATOS DE DADOS

**Faça:** implantar modelo de ativos, escopo, agente, avaliação, job, finding, remediação, relatório e auditoria; APIs versionadas, contratos JSON/OpenAPI, state machines, validações, saneamento e feature flags. Adaptar interfaces existentes em vez de duplicar. **Aceite:** fluxo completo via API simulada com dados de laboratório, sem scanner real; respostas 403/404 conforme política; esquema validado.

### FASE 3 — MOTOR / WORKER / AGENTE / CLI

**Faça:** separar jobs de requisições web, fila persistente, retries idempotentes, kill switch, controles de escopo em três etapas, scanner Go/Python normalizado, agente simulado antes do binário, binário Windows/Linux e CLI com enrollment seguro. **Aceite:** avaliações de laboratório autorizadas, canceláveis e observáveis; agente revogado não recebe jobs; resultado não altera tenant; sem varredura externa não autorizada; build/teste agent/CLI.

### FASE 4 — EXPERIÊNCIA WEB COMPLETA

**Faça:** separar marketing/app/admin; navegação especificada, wizard onboarding, assets, agents, assessments, findings, remediations, reports, AEGIS, teams/settings e trilha de auditoria. Reaproveitar UI válida. Garantir estados vazios/error/loading, acessibilidade e mobile. **Aceite:** teste e2e dos fluxos F1-F6 com browser, tela demonstrativa idêntica no contrato mas isolada; nenhum botão sem função ou erro silencioso.

### FASE 5 — INTELIGÊNCIA, RELATÓRIOS E PRODUTO COMERCIAL

**Faça:** AEGIS read-only, priorização explicável, dedup, scores respaldados, relatórios técnico/executivo versionados, catálogos/entitlements, propostas para serviço humano sem API falsa de cobrança. **Aceite:** relatório vinculável à avaliação e escopo; histórico de alteração; export apenas com permissão; checkout fictício só em demo; cálculos explicitamente fundamentados e testados.

### FASE 6 — RELEASE CANDIDATE E PREPARAÇÃO PARA PILOTO

**Faça:** testes completos, Compose local, configuração staging, guides Windows/Linux, documentação admin/operador/cliente, logging, métricas, backup/restore testado, threat model, dependências, licenças, SAST, scans de segredos e artefatos de release versionados. Verificar requisitos LGPD aplicáveis. **Aceite:** checklist de piloto preenchido com evidências + pendências; somente recomendar acesso de clientes reais quando os bloqueios forem resolvidos. **NÃO efetuar deploy real, comprar serviços ou afirmar conformidade legal automaticamente**.

**A cada fase:** implementar → executar testes → corrigir regressões → atualizar documentação e contratos → registrar mudanças e pendências em `docs/IMPLEMENTATION_LOG.md` → seguir para próxima fase dentro das capacidades da sessão. Se a sessão terminar, deixar checkpoint reentrante em `docs/NEXT_STEPS.md` (estado do trabalho e comandos), sem alegar continuidade autônoma em segundo plano.

---

## 9. BATERIA DE QUALIDADE / DEFINITION OF DONE

**Automatizar onde couber:** Python `pytest`, `ruff`, análise de dependências, scanner de segredos, Go `go test ./...`, `gofmt`, `govulncheck` se disponível e apropriado; teste de migração PostgreSQL e SQLite de desenvolvimento; contratos API, autorização, filesystem, frontend e2e Playwright ou ferramenta já existente; CI GitHub Actions com segredos protegidos. Fixar dependências e gerar SBOM se viável.

**Conjunto de cenários E2E mínimos:**

1. Criar dois tenants A/B e logins de owner/analyst/viewer; demonstrar 100% das rotas tenant-scoped com teste parametrizado BOLA/IDOR.
2. Onboarding com escopo válido/ inválido, aprovar/revogar, agent enrollment/revoke, pedido de job autorizado/desautorizado.
3. Executar inventário e avaliação segura no laboratório, cancelar, falhar, retry, timeouts, retorno de resultados e evidência.
4. Triar finding, atribuir tarefa, aceitar risco com expiração, retestar, reabrir e registrar timeline.
5. Relatório técnico/executivo sem dados cruzados; export permissionado; auditoria de decisão.
6. IA ligada/desligada/timeout/prompt injection de banner sem privilegiar texto malicioso; sem vazamento de secrets.
7. Demo sem backend, sem chamadas externas e com rótulos; modo produção recusa fixtures e senha padrão.
8. Build CLI/agente Windows/Linux e instruções verificadas; logs redigidos.

**Metas de engenharia propostas, não promessas comerciais:** tempo de API interativa observado em ambiente de teste com p95 razoável documentado, worker com limites/retries, monitoramento de falhas, dados íntegros após reinício, restore demonstrado, aplicação que inicializa por instruções reproduzíveis. Mensurar em vez de inventar SLO.

**Regra de pronto por entrega:** funcionalidade na UI + autorização backend + persistência e migração + logs mínimos + testes positivos/negativos + documentação de operação + e2e quando aplicável. Endpoint “existe” não é funcionalidade pronta. Screenshot bonito não é produto pronto. Testes verdes não equivalem a auditoria independente.

---

## 10. DIVISÃO FUTURA DO CÓDIGO ENTRE TRÊS PESSOAS

**AGORA: CODEX IMPLEMENTA TODAS AS ÁREAS.** Nenhum dos três estudantes precisa assumir algo durante esta missão. Prepare o repositório para atribuições futuras:

| Área | Futuro DEV 1 | Futuro DEV 2 | Futuro DEV 3 |
|---|---|---|---|
| **Responsabilidade principal** | Backend, dados, APIs, identidade, segurança do produto | Motor técnico, agente Go/Python, fila de execução técnica, IA | Frontend, UX, sistema de design, integração UI/API |
| **Ownership provável** | `app/`, migrações, auth, scopes, tenants, billing, reports backend | `core/`, `scanner_go/`, `agent/`, `worker/` (executor), `app/ai/` (lógica) | `index.html`, `static/`, componentes, dashboards, e2e de UI |
| **Interfaces compartilhadas** | OpenAPI, banco, contrato de job | schemas de job/result/evidência, limites | consumidores OpenAPI, estados da interface |
| **Responsabilidade cruzada** | Reviewer de segurança | Reviewer de risco técnico e evidências | Reviewer de usabilidade e contratos |

**Cuidado com as fronteiras:** `app/scans/` deve ter proprietários claros por função: DEV 1 controla **rota/autorização/persistência**, DEV 2 controla **orquestração/checks/resultado**. AEGIS: DEV 1 guarda credenciais/limites/autorização, DEV 2 cuida da lógica do copiloto, DEV 3 da tela. Não criar um papel “o dev que faz toda a segurança”: todos respondem por segurança do que desenvolvem.

**Preparação requerida:** `docs/DIVISAO_DESENVOLVIMENTO.md`, `docs/CONTRATOS_ENTRE_MODULOS.md`, `CONTRIBUTING.md` com branch por feature, PR pequeno, CI antes de merge, pelo menos uma revisão cruzada, checklist de segurança, padrões de commit, criação de issues, doc para onboarding. Não preencher `CODEOWNERS` com identidades não confirmadas e não criar três serviços independentes só para facilitar divisão.

**Princípio de conhecimento:** todos sabem rodar app + testes + demo; cada um domina seu módulo, mas no mínimo um colega consegue revisá-lo. Nas primeiras semanas do time, fazer pairing entre áreas e rodízio de suporte.

---

## 11. RELATÓRIOS/ARQUIVOS QUE A CODEX DEVE DEIXAR NO REPOSITÓRIO

Produzir e **manter atualizados**:

```
docs/
  PRODUCT_VISION.md                # objetivo, público, promessa e limites
  SERVICE_CATALOG.md               # S1-S5, H1-H3, entregas e exclusões
  USER_JOURNEYS.md                 # F1-F6, papéis, permissões, acceptance tests
  INFORMATION_ARCHITECTURE.md      # sitemap/menu/telas/estados e design tokens
  ARCHITECTURE.md                   # visão de componentes e trade-offs
  ADR/0001-product-and-architecture.md
  DATA_MODEL.md                    # entidades, FKs, multi-tenant, migrações
  API_CONTRACTS.md                 # links OpenAPI, formatos e erros
  THREAT_MODEL.md                  # ativos, agentes maliciosos, SSRF, BOLA, IA
  SECURITY_REQUIREMENTS.md         # testes/mitigações/links para padrões
  AGENT_CLI_SPEC.md                # protocolo, enrollment, build e operação
  AEGIS_SPEC.md                    # limites, validação e privacidade
  RELEASE_READINESS.md             # checklist com aprovado/pendente/evidências
  BASELINE_2026.md                 # código e testes de origem
  FEATURE_MATRIX.md                # existe/parcial/mock/ausente/bloqueado
  DIVISAO_DESENVOLVIMENTO.md
  CONTRATOS_ENTRE_MODULOS.md
  IMPLEMENTATION_LOG.md            # alterações, decisões e testes por fase
  NEXT_STEPS.md                    # checkpoint para retomar com Codex
CONTRIBUTING.md
.env.example                       # nenhuma credencial válida
```

**No relatório final da execução**, apresentar tabela por fase: `mudança real`, `arquivos`, `testes executados`, `resultados`, `risco residual`, `status (feito/parcial/bloqueado)`. Traga comandos de execução em Windows e Linux e não marque como feito o que for apenas mock. Se não houver tempo/recursos para implementar tudo, **não substitua código por texto**: entregue incrementos completos que rodem, priorizando segurança e fluxo integral de laboratório.

---

## 12. REFERÊNCIAS PARA INTERPRETAR REQUISITOS (NÃO COPIAR IMPLEMENTAÇÕES SEM ANÁLISE)

- Repositório original e documentação: https://github.com/alefkaue/cymag_saas
- OWASP API Security Top 10 — object-level authorization: https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/
- OWASP ASVS 5.0 (padrão de requisitos verificáveis): https://github.com/OWASP/ASVS
- OWASP Top 10 for LLM Applications 2025: https://genai.owasp.org/llm-top-10/
- NIST SP 800-115 — planejamento e condução de testes técnicos: https://csrc.nist.gov/pubs/sp/800/115/final
- CISA KEV — catálogo oficial de vulnerabilidades exploradas: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- FIRST EPSS — probabilidade de exploração; consultar referência oficial e API vigente: https://www.first.org/epss/
- ANPD — guia de segurança para agentes de pequeno porte: https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-sobre-seguranca-da-informacao-para-agentes-de-tratamento-de-pequeno-porte

Se referenciar padrões ou APIs, conferir a versão atual e inserir data da consulta. Não alegar homologação OWASP, conformidade legal plena ou garantia contra invasões.

---

## 13. PRIMEIRA RESPOSTA E ORDEM DE EXECUÇÃO

**A resposta inicial da Codex deve ser curta e operacional**: citar o commit atual, a árvore/arquitetura encontrada, o baseline de testes, os 5 riscos mais urgentes e **começar a implementar a Fase 1 após registrar a Fase 0**. Não devolver apenas uma proposta ou pedir autorização para executar análise normal do código. Não realizar ações destrutivas, acesso externo a alvos, implantação paga ou merge irreversível.

**Ordem firme de prioridade:** (1) isolamento e autorização; (2) contratos de produto/dados; (3) execução autorizada e agentes; (4) páginas/fluxos utilizáveis; (5) IA e relatórios robustos; (6) release candidate; (7) documentação de equipe futura.

Ao final, preservar uma lista objetiva de pendências que só os fundadores poderão decidir: preço após entrevistas, domínio/marca, contrato de prestação de serviços, provedor de cobrança, infraestrutura de produção, política comercial e responsável formal por atendimento a incidentes.

**Execute a missão agora no repositório local.**
