# CHANGELOG_AGENTS — alterações por agente

## 2026-10-10 / 2026-10-11

### 🔵 Claude Code
- **SEC-001** branch `seguranca/p0-tenant-isolation`, docs de coordenação e
  `docs/audit/2026-10-baseline.md`. Baseline: 55 testes passando.
- **SEC-002** `account_id` em `engagements` e `scans` (schema + migração forward-only
  idempotente com backfill a partir do criador; índices). `app/db.py`.
- **SEC-003** Isolamento multiempresa em todas as rotas de recurso de cliente:
  - `app/scope.py`: `resolve_authorized_target(account_id, ...)` vincula o engagement ao tenant.
  - `app/engagements/routes.py`: list/get/create/authorize filtrados por tenant (outro tenant → 404).
  - `app/scans/routes.py`: `/api/scans` e `/api/scans/<id>/findings` por tenant (IDOR fechado).
  - `app/autonomous/routes.py`: `/api/autonomous/<run_id>` checa posse via scan do tenant.
  - `app/auth/decorators.py`: `current_account_id()`, `role_required`/`is_staff` revalidam no banco, quota por conta.
- **SEC-004** `tests/test_tenant_isolation.py`: 11 testes A/B (db + HTTP), todos verdes.
- **SEC-005** `app/config.py`: `CYMAG_ENV`; produção/staging exigem `CYMAG_SECRET_KEY` forte
  (fail-closed) e não semeiam demo; cookie Secure por padrão em prod. `app/db.py`: seed gated.
- **DET-001** `core/business.py`: todo valor em R$ marcado `is_estimate`+`estimate_disclaimer`;
  removida linguagem de perda/economia como certa. +4 testes. (Assumido por Claude porque o
  Codex não pôde executar — ver abaixo.)
- **SEC-006** `app/reports/routes.py` reescrito: `/api/report/quick|detailed` agora exigem
  `scan_id` e montam o laudo a partir dos findings persistidos do scan do TENANT
  (posse verificada; cross-tenant → 404). Exec risks derivados no backend; `instructions`/
  `template` sanitizados. `app/reports/pdf.py`: selo "DADOS FICTÍCIOS — DEMONSTRAÇÃO"
  (quando `CYMAG_ENV=demo`) + linha de proveniência (scan_id, gerado_por, nº findings).
  `static/cymag.js`: caminho real envia `scan_id` (demo segue client-side). +4 testes
  (`tests/test_reports.py`). Suíte: **74 passed**.

### 🟢 Codex — DESBLOQUEADO e em execução
Causa raiz da falha anterior: `~/.codex/config.toml` tinha `[windows] sandbox = "elevated"`,
modo que o `codex.exe` não lança nesta máquina (CreateProcess → os error 3). O helper roda
quando chamado direto, então NÃO era o Defender. Corrigido para `sandbox = "unelevated"`
(backup `config.toml.bak`). Codex passou a executar comandos normalmente.
- **DET-002** delegado e executado por Codex (`codex exec -s workspace-write -c windows.sandbox="unelevated"`):
  reclassificou inferências fracas em `core/checks/{web,databases,remote,smb,iot_ot,base}.py`
  para linguagem de indício + campos `verification_status`/`confidence`, rebaixando severidades
  superestimadas (ex.: MS17-010/EternalBlue de "RCE confirmado crit 9.8" → "possível, suspected").
  Revisão/integração por Claude após conclusão (ver resultado do pytest no fim da task).

### Revisão cruzada (Claude revisando Codex) — DET-002 APROVADO
- Rodei a suíte completa de forma independente: **92 passed** (70 anteriores + 4 SEC-006 + 18 do Codex).
- Revisei o diff de `core/checks/*`: chaves de finding preservadas; `confirmed/high` mantido só
  onde há prova real (login MySQL efetivo); CVEs associadas sem prova removidas (CVE-2022-0543 Redis,
  CVE-2015-1427 Elastic, CVE-2016-6662 MySQL, CVE-2016-0777 SSH).
- **Bug real corrigido pelo Codex:** detecção MS17-010/MS12-020 usava `"vulnerable" in stdout`, que
  casava com a linha `State: NOT VULNERABLE` (falso-positivo crítico). Agora exige regex do estado
  `VULNERABLE` exato. Severidades infladas rebaixadas (EternalBlue crit 9.8→high 8.0 suspected).
- Removido diretório temporário de teste deixado pelo Codex (`core/checks/.det002-*`).
- Suíte combinada final: **92 passed**. Pronto para commit (aguardando autorização). Push será feito pelo Codex.

### Push (2026-10-11)
- Branch `seguranca/p0-tenant-isolation` enviada ao GitHub pelo fundador (git push direto; Credential Manager autenticou). Commit `cf5dcbb`. PR a abrir em: https://github.com/alefkaue/cymag_saas/pull/new/seguranca/p0-tenant-isolation

## Sessão ASTRO — 2026-10-10 — Codex coordenador

- Inventariou/extraiu 3 ZIPs sem sobrescrita; listagens e hashes em materials/inspection-20261010. Revisou tecnologias distintas, documentos de planejamento e SVGs oficiais; decisões em MATERIALS/DESIGN_MERGE.
- Criou design system aplicado ao frontend Flask: paleta ASTRO, Instrument Sans, mono técnico, temas sistema/claro/escuro persistidos, logo oficial, foco/reduced-motion e console com eventos/timestamps/run ID reais. Não importou telas bancárias ou runtimes dos protótipos.
- Criou app/dashboard.py e /api/dashboard com métricas persistidas por tenant, status de validação e limitações; demo implementa o mesmo contrato com proveniência sintética e contagens derivadas.
- Corrigiu UI de achados/evidência e seleção de achado no histórico; preserva scan_id do run autônomo para relatórios. Erros de consulta de escopo e polling agora ficam explícitos.
- AUTH-008: usuário ativo revalidado, IP de auditoria sem confiar em header, sem organização negado, owner/viewer barrados em início de scans. Testes negativos e de RBAC adicionados.
- SCAN-008: despacho somente inventário TCP, sem testes de credenciais/payloads/MQTT/planejamento de ataque; até 64 candidatos sem materializar CIDRs enormes; socket 24 workers e Nmap connect limitado. Código legado preservado para revisão, fora do caminho do produto. Cobertura atual publicada por API/áreas. Não anuncia novas vulnerabilidades confirmadas.
- PDF com paleta monocromática, SVG vetorial oficial e status observação/suspeita/confirmado/não classificado. PDF demo com SVG oficial e identidade atualizada. Guias legados receberam aviso de estado atual.

### Claude Code nesta sessão

Instalação/auth/help verificados; tarefa limitada enviada ao executável real com -p. Processo terminou **exit 1**, **ECONNREFUSED**, **zero tokens**, nenhuma implementação. Codex assumiu somente após o processo terminar. Prompt/resultado preservados para reprodução/revisão manual. Histórico anterior de Claude acima permanece intacto e não representa trabalho novo desta sessão.

### Validação final

- `.venv/Scripts/python.exe docs/agents/run_checks.py`: **110 passed, 13 warnings**, 8,66s; exit 0. Regressões tenant/PDF existentes e novos testes auth/RBAC/dashboard/inventário integrados. Warnings: API ln depreciada do fpdf2; não são erros. Saída em TEST_RESULTS.txt.
- `node tests/test_frontend_contracts.cjs`: aprovado; demo source sintético, contagens consistentes, zero fetch, tema e persistência.
- `node --check` em cymag.js, cymag-demo.js e astro-theme.js: aprovado.
- `git diff --check`: aprovado; apenas avisos Git de normalização CRLF, sem erros de whitespace.
- Testes convencionais inicialmente falharam ao reabrir diretórios com ACL owner-only criados pelo Python 3.14 neste sandbox. Runner usa novos temporários no workspace com ACL herdada, sem alterar permissões do sistema ou da aplicação.
- Não realizado: browser E2E/QA visual/contraste completo, scans contra infraestrutura real, carga, recuperação de worker, staging/deploy. Não declarar produção pronta. Nenhum commit/push realizado; alteração prévia do usuário preservada.

## Atualização 2026-10-11 — pacote de redesign

Integração detalhada e resultados em [REDESIGN.md](REDESIGN.md): navegação por URLs, avaliações com wizard/detalhe, API tenant-scoped, escopos com autorização owner e viewer somente leitura. Implementação por Codex. Claude executado pelo shell terminou exit 1 / ECONNREFUSED, sem alterações. 113 testes Python e contratos frontend passaram. QA visual continua pendente: Edge falhou por acesso negado e exibiu 0x80000003; não contornar proteções do ambiente. Scanner e dados reais preservados nesta etapa.

Colaboracao Claude confirmada no terminal do usuario; parecer concluido e correcoes verificadas/integradas por Codex. Detalhes e decisoes F1-F10 em CLAUDE_REVIEW_INTEGRATION.md. Suite: 114 testes Python passaram; QA visual pendente.

Pesquisa de plataformas e UX concluida por Codex; plano em PRODUCT_PLAN.md. Script agora aceita -Task product-plan e restringe Claude ao novo documento de revisao, sem sobrescrever parecer anterior. Sintaxe validada; tarefa Claude preparada para terminal normal, execucao nao confirmada.

Plano conjunto Claude+Codex integrado. Claude revisou e retornou parecer; Write negado, Codex salvou resultado sem contornar permissoes. Codex implementou isolamento da revisao gerenciada e transicoes atomicas; ver PRODUCT_PLAN_INTEGRATION.md.

## Experiencias por perfil — 2026-10-11

Implementacao Codex em EXPERIENCE_UI.md: sidebar por funcao, panorama executivo, centro operacional, galeria de relatorios e escopos em duas colunas. Dados das APIs existentes, sem alterar permissoes/scanner. Contratos frontend/boot/experiencia passaram; 8 regressoes Python passaram. Browser visual permanece pendente; Claude tem tarefa de revisao somente leitura preparada (-Task experience), ainda nao executada.

Analise de produto/comercializacao concluida por Codex em COMMERCIAL_READINESS.md com fontes NIST/W3C/OWASP/ANPD, gates, jornada e configuracoes. Ajustes seguros de leitura/contraste aplicados; testes frontend passaram; browser/cliente nao testado. Claude commercial preparado para terminal normal.

2026-10-11: Integrada revisao comercial concluida por Claude (somente leitura). Codex removeu inferencias financeiras/probabilidades offline, estimativas para observacoes e promessa de conformidade do catalogo. Suite: 118 testes passaram; QA visual pendente. Detalhes em COMMERCIAL_REVIEW_INTEGRATION.md.

2026-10-11: Codex implementou gates de implantacao, bloqueio de billing simulado/discovery hospedados e bloqueio de rede do AEGIS desabilitado. 124 testes Python e 3 suites JS passaram. Claude shell sem resposta interrompido exit 1; tarefa pilot-security preparada para terminal autenticado. Ver PILOT_SECURITY.md.

2026-10-11: Contencao defensiva implementada: redes especiais/IPv6 rejeitados, allow/deny, limite 64 sem truncamento, max_ips e refiltro de hosts. 139 testes passaram; nenhum scan externo. Parecer de Claude preservado.

## SEC-009b (Codex) — rate limit de login

Implementado limitador em memória com threading.Lock, janela deslizante por email normalizado e IP, limites configuráveis por ambiente (5/20 falhas em 900 segundos), bloqueio por uma janela completa, teto de 10000 chaves e descarte de entradas antigas/expiradas. Login bloqueado retorna 429 com Retry-After e auditoria; sucesso limpa apenas o email e emails inexistentes executam verificação contra hash dummy gerado uma vez. Adicionados 8 testes com reset automático, relógio injetável, banco temporário, expiração, equivalência de respostas, limite de memória e concorrência. Validação: .venv/Scripts/python.exe docs/agents/run_checks.py — 160 passed, 17 warnings (depreciações de PDF), em 20.73s; nenhuma falha por estado compartilhado. Estado do limitador é local a cada processo/worker.

## SEC-009a (Claude) — barreira CSRF da API + revisão do SEC-009b

- Novo `app/csrf.py` registrado no app factory: em POST/PUT/PATCH/DELETE sob `/api/`, recusa (403) origem divergente (`Origin`, ou `Referer` na falta dele; `null` nunca confiável; extras via `CYMAG_TRUSTED_ORIGINS`) e exige `application/json` ou header `X-Requested-With`. Fecha o vetor `<form enctype="text/plain">` que `get_json(force=True)` aceitava. SameSite=Lax segue como primeira barreira.
- `static/cymag.js`: `api()` e download de PDF enviam `X-Requested-With: ASTRO`.
- Testes: `tests/test_csrf.py` (13); 6 POSTs sem corpo em testes existentes passaram a enviar o header.
- Revisão do SEC-009b (Codex): aprovado. Ressalvas registradas: bloqueio por email permite lockout temporário de uma conta por terceiros (trade-off padrão; considerar CAPTCHA/MFA depois); estado é por processo — com vários workers o limite efetivo multiplica; `_prune` é O(n) por login (ok até 10k chaves).
- Suíte combinada: **160 passed**; 3 suites JS OK.

﻿
## 2026-10-11 — UX Onda 1 (Codex)

Referência: docs/agents/UX_WAVE1_CODEX.md. As duas análises da raiz scanner foram lidas. Alterações de produto restritas ao frontend; backend, scanner, SVGs e identidade monocromática preservados. Sem commit/push.

Arquivos: index.html, static/cymag.js, static/astro-experience.js, static/astro-workspace.js, static/astro-workspace.css e este CHANGELOG_AGENTS.md. Scripts auxiliares de edição/verificação ficaram em .test-runtime (ignorado pelo Git).

1. UX-16: estados de escopo em PT-BR, Organização/Relatórios/Operações de segurança substituem textos em inglês; papéis Analista de TI, Diretoria e Admin consistentes; títulos seguem o menu do perfil. Um mapa compartilhado traduz categorias; valor bruto preservado na evidência técnica.
2. UX-04: histórico de avaliações e tabela compartilhada de achados têm data-label em cada célula; até 720px as linhas viram cartões com rótulos explícitos, incluindo a tabela na aba Relatórios.
3. UX-12/UX-24: seletor de tema no cabeçalho do app e no login, sem posição fixa; barra demo recolhida no mobile com botão acessível para explorar papéis/reiniciar; cada toast substitui o anterior.
4. UX-13: erros locais com texto, borda, aria-invalid e aria-describedby nos campos obrigatórios de escopo, login, chave de IA e confirmação do wizard. Erros permanecem até correção; falha de cadastro exibida junto aos endereços. Busca sem resultado mantém termo escapado e oferece Limpar filtros em avaliações/relatórios.
5. UX-05: alvo efetivo concreto no passo inicial (atualizado ao editar/trocar escopo) e na revisão; envio explícito do alvo mostrado; explicação do que acontece em cada modo após iniciar, sem texto sobre backend/API no wizard.
6. UX-06: cadastro explicado como rascunho; endereços propostos sem alegação de autorização; ação Autorizar explicada como liberação de avaliações nesses endereços; usuários sem permissão orientados a pedir autorização ao Dono ou Admin da mesma organização.

Verificações:
- node tests/test_frontend_contracts.cjs: Frontend contracts: routes, demo persistence, unknown IDs, provenance, counts, zero fetches and themes passed.
- .venv/Scripts/python.exe docs/agents/run_checks.py: 160 passed, 17 warnings in 22.48s. Avisos de depreciação do parâmetro ln no gerador de PDF existente.
- node --check nos três JavaScripts alterados: aprovado.
- Verificação auxiliar offline: UX Wave 1: mobile labels, readable/raw categories, role navigation, escaped empty search and recovery passed.
- git diff --check: aprovado (aviso do Git sobre conversão LF/CRLF no CSS).

Limite: não houve inspeção visual em navegador ou dispositivo físico; validação feita por contratos, renderização de HTML offline, sintaxe e revisão de CSS/DOM.

## 2026-10-11 — UX Onda 2 (Codex)

Referência: UX_WAVE2_CODEX.md e regras da Onda 1; análises da raiz scanner consultadas. Alterações de produto somente no frontend, preservando backend/scanner, temas, SVGs e identidade monocromática. Sem commit/push. O registro integral da Onda 1 foi acrescentado a este changelog oficial sem apagar histórico; o CHANGELOG_AGENTS.md incorreto da raiz foi removido.

Arquivos tocados nesta onda: index.html, static/astro-experience.js, static/astro-workspace.js, static/astro-workspace.css, static/astro.css, static/cymag.js, tests/test_ux_wave2.cjs, tests/test_ux_contrast.cjs e docs/agents/CHANGELOG_AGENTS.md. Auxiliares em .test-runtime, ignorado pelo Git. Alterações anteriores da Onda 1 preservadas.

1. UX-01: número principal é suspeitas + não classificados aguardando revisão; confirmados em hierarquia secundária; ressalva “Zero confirmados não significa ausência de risco” e próximo passo explícitos. Banner institucional substituído pela situação real.
2. UX-02: resumo apresenta registrados = confirmados + suspeitas + não classificados + observações. Observações são um estado real distinto da API: foram mantidas na soma para não classificá-las incorretamente nem excluir registros. A decomposição acompanha atualização da avaliação em execução.
3. UX-07: banner operacional compacto; fila Próximo trabalho antes do banner e dos indicadores, priorizando revisão pendente inclusive no fluxo móvel.
4. UX-08: Diretoria (viewer) tem síntese própria com situação conhecida, pendências, cobertura e data localizada em PT-BR. Sem dados suficientes para comparar ou estimar impacto; número de avaliações ou alvo igual não prova comparabilidade, pois a API atual não versiona método/cobertura históricos. Nenhuma tendência ou perda financeira fabricada.
5. UX-09/10/11: busca por título/descrição/evidência/ativo, filtros combináveis de severidade/ativo/validação, chips removíveis e Limpar filtros; ordenação ascendente/descendente nos cabeçalhos com aria-sort; cabeçalho sticky no contêiner rolável; metadados recolhidos por padrão e área de achados ampla. Descrição completa sob demanda sem slice/truncamento; confortável/compacto persistido em localStorage. Fechar orientação restaura rolagem da página/lista e foco no botão de origem.
6. UX-03: ação Ver orientação de análise; modal separa evidência registrada, resultado e sugestão, mostra classificação e Dado sintético quando aplicável; permite copiar com alternativa manual caso clipboard falhe. Origem determinística explícita na demo. No ambiente real informa serviço AEGIS e possibilidade de IA/fallback: a API não identifica a origem efetivamente usada, portanto a UI não a presume. Resposta tardia não sobrescreve modal novo.
7. UX-17: tokens muted/faint claro #6B6B6B → #606060, escuro #8C8C8C → #B0B0B0; rótulos pequenos ajustados para 13px no workspace e componentes compartilhados. Teste reproduzível tests/test_ux_contrast.cjs verifica AA nos fundos dos dois temas.
8. UX-18: console sem referência acessível destaca Histórico indisponível, desabilita filtro/pausa com aparência visual própria e oferece Consultar resultados; não inventa eventos históricos.

Contraste WCAG (texto secundário; antes → depois):

| Tema | Fundo | Razão antes | Razão depois |
| --- | --- | --- | --- |
| Claro | #FFFFFF | 5,33:1 | 6,29:1 |
| Claro | #F2F2F2 | 4,76:1 | 5,62:1 |
| Claro | #E2E2E2 | 4,11:1 | 4,85:1 |
| Escuro | #0A0A0A | 5,89:1 | 9,13:1 |
| Escuro | #141414 | 5,48:1 | 8,49:1 |
| Escuro | #242424 | 4,62:1 | 7,16:1 |
| Escuro | #3A3A3A | 3,38:1 | 5,24:1 |

Validação:

- node tests/test_frontend_contracts.cjs: aprovado.
- node tests/test_workspace_boot.cjs e node tests/test_experience.cjs: aprovados.
- node tests/test_ux_wave2.cjs: aprovado; hero/síntese, limites honestos, filtros combinados, busca, ordenação bidirecional, escape e densidade persistida.
- node tests/test_ux_contrast.cjs: aprovado; sete fundos com razão final ≥4,5:1 para muted/faint.
- .venv/Scripts/python.exe docs/agents/run_checks.py: 160 passed, 17 warnings in 21.29s; avisos existentes de depreciação ln do PDF.
- node --check nos três JavaScripts alterados e git diff --check: aprovados.

QA visual em 390 × 844 não foi possível: a política de execução do ambiente rejeitou o comando que iniciaria servidor estático e Brave headless. Não houve captura/inspeção visual validada, nem contorno da restrição. Os testes de DOM simulado e CSS não substituem inspeção no navegador; posição acima da dobra e aparência móvel continuam sem comprovação visual.


## 2026-10-11 — Codex — Correções da inspeção UX Onda 2 (F1–F10)

Escopo: somente frontend e regressões offline; preservadas as alterações anteriores. Sem servidor, navegador, commit ou push.

Arquivos tocados nesta rodada: `static/astro-workspace.css`, `static/astro-workspace.js`, `static/astro-experience.js`, `static/cymag.js`, `tests/test_experience.cjs`, `tests/test_workspace_boot.cjs`, `tests/test_ux_wave2_fixes.cjs` e este changelog.

- F1: em até 720px, `.topbar` tem uma linha e altura de 56px, incluindo padding; menu, título com ellipsis e seletor compacto de tema (78px, alvo de 44px). `#astro-breadcrumb`, `#page-sub` e `#topbar-actions` ficam ocultos; o label do tema continua acessível. A altura fixa fica abaixo de 64px.
- F2: `.table.mobile-cards tbody tr` usa duas colunas, título/status ou título/severidade no cabeçalho; campos com rótulo e valor lado a lado. Retirada a moldura externa das tabelas/cartões de achados; mantida uma borda por cartão. Descrição/evidência continuam expansíveis; título longo limitado a duas linhas, conteúdo completo acessível na orientação/descrição. Meta de aproximadamente 180px para cartões fechados, sem limitar conteúdo expandido.
- F3: escolhida rolagem da página. `.findings-scroll` usa `max-height:none; overflow:visible`; `.findings-scroll thead th` usa `position:sticky; top:var(--topbar-height,76px)`. Topbar desktop: 76px. Reduzidos intro, tabs, metadados fechados, filtros e células para abrir espaço para seis linhas em viewport de 900px; células confortáveis com padding 8px 10px, compactas 5px 8px. Título limitado a duas linhas; descrição/evidência completas no disclosure.
- F4: placeholder `Buscar achado`; label de busca com `flex:1 1 280px; min-width:180px`.
- F5: removido prefixo numérico dos textos de passos, mantendo numeração semântica de `<ol>`.
- F6: passos recebem `Somente se confirmado:` quando status não é confirmed; comandos, cadeia, MITRE e recon dentro de `<details class="technical-guidance">`, fechado por padrão. owner/viewer usam explicitamente orientação executiva e não recebem esses campos no DOM. Orientação executiva não confirmada inclui condição de validação antes da remediação. Mantido Copiar orientação.
- F7: cinco cartões no resumo: registrados, confirmados, suspeitas, não classificados e observações; não classificados >0 ganha destaque. Polling atualiza os cinco contadores e o destaque; decomposição mantida como legenda.
- F8: removida repetição de risco zero na coluna direita; aviso preservado à esquerda. `.executive-hero .hero-summary strong` usa 24px/peso 400, secundário ao 17 principal.
- F9: síntese em `<dl class="synthesis-list">`, com Situação, Pendências, Limites, Tendência e Impacto. Situação informa execuções concluídas; Pendências informa execuções que falharam, sem repetir os contadores do hero. Preservadas limitações e falta de dados comparáveis.
- F10: mantidos flag/papel em `sessionStorage` (`astro-demo-session`), validado papel salvo e restaurada demo também quando `/api/me` falha, preservando pathname/query da avaliação. Sessão real autenticada continua prioritária. Login define título `Entrar · ASTRO Cyber`. Logout limpa flag.
- F11: pendente para Onda 3, sem implementação nesta rodada: Admin/Equipe ASTRO compartilham navegação/telas; Equipe ainda se confunde com Analista.

Validação:
- `node tests/test_*.cjs` (executados individualmente via PowerShell): 6 scripts passaram: experience, frontend_contracts, ux_contrast, ux_wave2, ux_wave2_fixes, workspace_boot.
- `node --check` nos três JS alterados: passou.
- `.venv/Scripts/python.exe docs/agents/run_checks.py`: **160 passed, 17 warnings in 20.60s**. Warnings existentes de depreciação do parâmetro `ln` do FPDF.
- `git diff --check`: passou, apenas aviso de conversão LF/CRLF nos testes versionados.
- `tests/browser_redesign.cjs` não executado: requer navegador/CDP e contraria a restrição desta tarefa.

Reconferência visual necessária: 390px (topbar 56px e cartões fechados aproximadamente 180px) e desktop com 900px de altura (seis linhas com os disclosures fechados, cabeçalho sticky a 76px). Estas dimensões são metas implementadas por CSS; não foram medidas em navegador nesta rodada. Conteúdo longo, zoom e disclosures abertos podem aumentar cartões/linhas.
# 2026-10-11 — UX Onda 3, grupos A–E (Codex)

Escopo: frontend e testes CJS, mais os registros de entrega solicitados. Identidade, temas, permissões existentes e alterações prévias preservados. Sem commit/push, servidores ou navegadores. Fontes lidas: `UX_WAVE3_CODEX.md`, `UX_WAVE2_FIXES_CODEX.md` e as duas análises na pasta pai `scanner/`.

| Item | Arquivos | Mudança | Teste novo/ajustado |
| --- | --- | --- | --- |
| A/R1 | `static/cymag.js` | Um aviso antes da lista quando o achado não está confirmado; itens sem prefixos e sem numeração duplicada. | `test_ux_wave2_fixes.cjs`: aviso único e escaping. |
| A/R2 | `static/astro-workspace.css` | Container focado por script sem outline quando não focus-visible; teclado mantém anel. | `test_ux_wave3.cjs`: contrato CSS; teclado real pendente. |
| A/R3 | `static/astro-workspace.css` | Filtros móveis em duas colunas, labels alinhados e inputs/selects em 100%, inclusive busca sem min-width antigo. | `test_ux_wave3.cjs`: grade; medidas visuais pendentes. |
| A/R4 | `static/astro-workspace.js`, CSS | Escopo não registrado, status e datas sem classe mono; identificadores/alvos mantêm indicação técnica. | Suíte frontend e contrato CSS; inspeção mobile pendente. |
| B/Admin | `static/astro-experience.js`, workspace | Página administrativa própria com atalhos reais de organização/equipe/IA e grupo Administração; sem métricas inventadas. | `test_ux_wave3.cjs`: Admin distinto do operacional. |
| B/Equipe ASTRO | experience, workspace | Cliente/organização atual em destaque no panorama, avaliações e detalhe; aviso de troca de organização indisponível. | `test_ux_wave3.cjs`: contexto e escaping; ausência de vínculo explícita. |
| B/Fila e legado | `static/cymag.js`, workspace | Coluna Cliente ligada a account_id; vínculo ausente explícito; menu próprio restrito a is_staff; explicação de risk_score legado, pesos e limites. | Contratos frontend; conferência da fila real pendente. |
| C/Configurações | workspace, CSS | Seções Organização/Equipe/IA/Operação interna com URLs próprias e navegação lateral no desktop; equipe em consulta; assinatura simulada e capacidades indisponíveis explícitas. Seções de consulta não simulam botão Salvar. | `test_ux_wave3.cjs`: contrato de seções; boot regressivo. |
| C/IA | `static/cymag.js` | Não testada/Teste OK/Falhou separado de Ativa/Offline; Testar não salva; Aplicar bloqueado até sucesso dos valores atuais; respostas de teste antigas ignoradas. Um primário por vez; modelo em select; endpoint avançado recolhido; provedor/modelo/endereço distintos; nenhuma máscara de chave exibida. | VM executa o renderizador real: aplicar sem teste, edição durante teste, falha, sucesso, aplicação e invalidação. |
| C/Restauração | `static/cymag.js` | Confirmação inline explica remoção da configuração salva e retorno aos valores do ambiente do servidor; cancelar não chama API. | VM verifica que abrir confirmação não restaura e confirmar chama reset uma vez. |
| D/Ajuda | workspace | Blocos Quero… por papel com 3–4 passos, estados Não encontrado/Não verificado/Confirmado, seção Método e limites; Admin tem tarefa própria. | `test_ux_wave3.cjs`: presença da seção; inspeção por papel pendente. |
| D/Glossário | `static/astro-glossary.js`, CSS, `index.html` | Componente único para sete termos nas telas executivas e autorizações: botão nativo Enter/Space, Escape devolve foco, aria-describedby/expanded, 1–2 frases e link de documentação. Conteúdo dinâmico recebe termos sem modificar links/controles/código. Ajuda sempre no cabeçalho. | VM verifica os sete termos, vínculo ARIA, abertura e Escape/foco. |
| D/Login e landing | `index.html` | Entrar com conta; Senha ou chave de acesso com dica; contato com administrador em vez de recuperação falsa; benefício explicado com serviços acessíveis. | Suíte de contratos frontend; inspeção visual pendente. |
| E/Datas | experience, workspace | Função única pt-BR com UTC±offset e horário local; registros sem fuso tratados como UTC do servidor; ISO no title técnico; histórico, painel, relatórios e detalhe usam a função. | `test_ux_wave3.cjs`: fuso explícito e data inválida. |
| E/Ambientes | experience, workspace | Nome do escopo recuperado pelo engagement_id junto ao IP; sem nome, IP + sem nome cadastrado. História recente, histórico, relatório e detalhe. Busca no histórico inclui nome. | `test_ux_wave3.cjs`: nome presente/ausente. |
| E/Relatórios | experience, workspace, CSS | Cartões sem linhas decorativas, data humana, alvo/nome, contagens por estado calculadas via achados autorizados (erro = Não mensurado), status Gerado sob demanda. Explicação técnico × IA; opção IA desabilitada quando offline/indisponível; Dono/Diretoria veem síntese na aba Relatórios. | `test_ux_wave3.cjs`: dados do cartão e ausência da decoração; suíte de relatórios Python. |

Limite de integração: não existe endpoint público de status da IA. Admin consulta `/api/admin/ai/status`; demais papéis recebem motivo explícito de indisponibilidade, sem supor online/offline. Nenhum endpoint novo foi inventado. Troca de organizações, cobertura persistida, carteira completa, edição de equipe/MFA e relatórios versionados continuam dependentes do backend. `TASKS.md` registra UX-01–UX-24 como done/parcial conforme esse alcance.

Validação final: todos os `tests/*.cjs` executados com `ASTRO_SKIP_BROWSER=1`: sete suítes offline passaram; `browser_redesign.cjs` marcou SKIP antes de acessar CDP/rede, respeitando a proibição. Sintaxe de todos os `static/*.js` passou. `.venv/Scripts/python.exe docs/agents/run_checks.py`: **160 passed**, 17 avisos preexistentes de depreciação FPDF. Nenhuma verificação visual foi alegada.

Para o Claude conferir (ambiente de navegador autorizado em sua sessão; não iniciado pelo Codex):

| Grupo | Rota / papel | Seletores e estados |
| --- | --- | --- |
| A | `/app/assessments/1001?tab=findings`, Analista, 390px e desktop | `.findings-toolbar` duas colunas e selects uniformes; abrir orientação: `.guidance-warning` apenas uma vez, `.technical-guidance` fechada; trocar rota/link direto: `#main-content` sem linhas brancas, Tab mantém anel. |
| A | `/app/assessments`, 390px | `.mobile-cards td[data-label="Escopo"]`, `[data-label="Status"]`, `[data-label="Início"]` fonte normal, cards alinhados. |
| B | `/app/overview`, Admin / Equipe ASTRO | `.admin-home` e grupo Administração; Equipe: `.client-context` e aviso sem seletor fictício. |
| B | `/app/assessments` e `/app/assessments/1001`, Equipe ASTRO | `.client-context`, nome da organização atual em destaque. |
| B | `/app/settings?tab=legacy-ops`, somente staff | Menu Operação interna; `.legacy-explanation`, coluna Cliente na fila, Cliente não vinculado se não houver account_id resolvido; Risco legado explicado. Não-staff deve receber acesso indisponível. |
| C | `/app/settings?tab=organization`, `?tab=team`, `?tab=ai`, `?tab=legacy-ops` | `.settings-nav`, `.settings-section`, `#settings-navigation`; URLs, descrições e leitura/assinatura simulada; mudar de rota deve esconder o shell externo. |
| C | `/app/settings?tab=ai`, Admin | `#ia-test-state`, `#ia-status`, `#ia-test`, `#ia-apply`: inicial bloqueado → sucesso habilitado → edição bloqueado; resposta de teste antiga não habilita; apenas um primário. `#ia-model` select; endpoint em details fechado; nenhuma chave/máscara no status. `#ia-reset-confirm` abrir/cancelar/confirmar. Teste real somente com credencial autorizada. |
| D | `/app/help`, Dono/Analista/Diretoria/Admin | `.task-help`, `#method-limits`, tarefas e passos por papel, três estados explicados. |
| D | `/app/overview`, `/app/scopes`, `/app/assessments/1001?tab=summary`, Dono/Diretoria | `.glossary-trigger` e `.glossary-popover`: Enter abre, Escape fecha/devolve foco, aria-describedby, link Ajuda; conferir foco, overflow e leitores de tela nos dois temas. |
| D | `/login`, claro/escuro/mobile | `#login-pass`, `#login-access-hint`, `#login-btn`, dica de contato e benefício simples. Cabeçalho app: `#topbar-actions a[href="/app/help"]` inclusive mobile. |
| E | `/app/overview`, `/app/assessments`, `/app/reports`, detalhe | Datas humanas e fuso local em `time`/cartões; title técnico; ambiente Nome · IP ou IP · sem nome cadastrado. Usar também avaliação com engagement_id válido. |
| E | `/app/reports`, `/app/assessments/1001?tab=reports`, Dono/Diretoria/Admin | `.report-document`, `.report-generation`: alvo/nome, data e quatro contagens; erro de consulta não vira zero. `.executive-report-summary` para executivo, tabela para técnico; `#detail-pdf-ai:disabled` + `#report-ai-reason`, técnico habilitado somente concluída. Admin online habilita IA conforme API. |
