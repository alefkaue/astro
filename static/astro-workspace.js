/* Product navigation from ASTRO_CYBER_REDESIGN_LAYOUT. Existing engines/API kept. */
(function () {
  'use strict';
  const routes = window.ASTRO_ROUTES;
  const workspace = $('#sec-workspace');
  const originalShowSection = showSection;
  const originalEnterDemo = enterDemo;
  let epoch = 0;
  let timer = null;
  let restoreFocus = null;
  let wizard = null;
  const labels = {overview:'Visão geral',assessments:'Avaliações',new:'Nova avaliação',detail:'Detalhe da avaliação',
    scopes:'Escopos e autorizações',reports:'Relatórios',settings:'Configurações',help:'Ajuda e método',notfound:'Página não encontrada'};
  const statusLabels = {running:'Em execução',done:'Concluída',error:'Falhou',pending:'Pendente'};
  const canRun = () => ['operator','cymag','admin'].includes(state.user?.role);
  const runKey = () => `astro-runs:${isDemo() ? 'demo' : 'real'}:${state.user?.account?.id}:${state.user?.id}`;
  function runs() { try { return JSON.parse(sessionStorage.getItem(runKey()) || '{}'); } catch (_) { return {}; } }
  function rememberRun(id, run) { try { sessionStorage.setItem(runKey(), JSON.stringify({...runs(),[id]:run})); } catch (_) {} }
  const stamp = value => `<time title="${esc(value || "Sem registro técnico")}">${esc(window.ASTRO_EXPERIENCE.humanDate(value))}</time>`;
  const environment = scan => esc(window.ASTRO_EXPERIENCE.environment(scan));
  async function namedScans(scans) { try { const {engagements=[]} = await api('/api/engagements'); return scans.map(s => ({...s,engagement_name:engagements.find(e => e.id === s.engagement_id)?.name || s.engagement_name})); } catch (_) { return scans; } }
  function stopTracking() { clearTimeout(timer); timer = null; clearInterval(state.autoTimer); }
  function link(path, text, cls = '') { return `<a href="${esc(path)}" data-route class="${cls}">${text}</a>`; }
  function busy() { workspace.innerHTML = '<div class="card" role="status"><span class="spinner"></span> Carregando dados da organização…</div>'; }
  function fail(error, retry) {
    workspace.innerHTML = `<div class="card" role="alert"><h2>${error.status === 404 ? 'Avaliação não encontrada ou sem acesso' : 'Não foi possível carregar os dados'}</h2><p>${esc(error.message)}</p>${link('/app/assessments','Voltar às avaliações','btn')} ${retry ? '<button class="btn" id="workspace-retry">Tentar novamente</button>' : ''}</div>`;
    $('#workspace-retry')?.addEventListener('click', renderRoute);
  }
  function nav() {
    const profile = window.ASTRO_EXPERIENCE.profile(state.user.role);
    document.documentElement.dataset.workspace = profile.kind;
    if (state.user.is_staff) profile.groups.push(['OPERAÇÃO INTERNA',[['settings?tab=legacy-ops','Operação interna','history']]]);
    $('#nav').innerHTML = `<div class="workspace-identity"><span class="eyebrow">ORGANIZAÇÃO</span><b>${esc(state.user.account?.name || 'Organização')}</b><span class="workspace-persona">${esc(profile.name)}</span><small>${esc(profile.description)}</small></div>` + profile.groups.map(([title,items]) => `<div class="nav-group-label">${title}</div>${items.map(([page,label,ic]) => link('/app/'+page,`${icon(ic)}<span>${label}</span>`,'nav-item'+(page === 'assessments/new' ? ' nav-launch' : ''))).join('')}`).join('');
  }
  function navigate(path, replace = false) {
    if (!path.startsWith('/app/')) return;
    if (location.pathname + location.search !== path) history[replace ? 'replaceState' : 'pushState']({},'',path);
    closeSidebar(); renderRoute();
  }
  showSection = id => navigate(routes.legacy(id));
  enterApp = user => {
    state.user = user;
    if (isDemo()) { try { sessionStorage.setItem('astro-demo-session',user.role); } catch (_) {} }
    else { try { sessionStorage.removeItem('astro-demo-session'); } catch (_) {} }
    $('#u-name').textContent = user.name;
    $('#u-role').textContent = `${user.account?.name || 'Sem organização'} · ${ROLE_LABEL[user.role] || user.role}`;
    $('#u-avatar').textContent = (user.name || '?')[0].toUpperCase();
    nav(); showApp();
    if (!location.pathname.startsWith('/app/')) history.replaceState({},'', '/app/overview');
    renderRoute();
  };
  enterDemo = role => {
    try { sessionStorage.setItem('astro-demo-session',role || 'owner'); } catch (_) {}
    originalEnterDemo(role);
  };
  // Existing event listeners capture original functions; observe logout button as well.
  $('#logout-btn').addEventListener('click', () => {
    stopTracking(); ++epoch;
    try { sessionStorage.removeItem('astro-demo-session'); } catch (_) {}
    history.replaceState({},'', '/login');
  });
  $('#demo-btn').addEventListener('click', () => { try { sessionStorage.setItem('astro-demo-session',window.CYMAG_DEMO.role); } catch (_) {} });
  async function renderRoute() {
    if (!state.user) return;
    stopTracking();
    const current = ++epoch;
    const route = routes.parse(location.href);
    const valid = () => current === epoch && !!state.user;
    state.section = 'workspace';
    $$('.section').forEach(s => s.classList.remove('active'));
    workspace.classList.add('active');
    $$('#nav .nav-item').forEach(a => {
      const active = route.page === 'new' ? a.pathname === '/app/assessments/new' : route.page === 'detail' ? a.pathname === '/app/assessments' : a.pathname === '/app/'+route.page && (route.page !== 'settings' || (new URLSearchParams(a.search).get('tab') || 'organization') === (route.query.tab || 'organization'));
      a.classList.toggle('active',active);
      if (active) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current');
    });
    const menuLabel = window.ASTRO_EXPERIENCE.profile(state.user.role).groups.flatMap(([,items]) => items).find(([page]) => page === route.page)?.[1];
    $('#page-title').textContent = menuLabel || labels[route.page];
    if (route.page === 'overview') $('#page-title').textContent = window.ASTRO_EXPERIENCE.profile(state.user.role).title;
    $('#page-sub').textContent = state.user.account?.name || 'Organização';
    $('#astro-breadcrumb').innerHTML = link('/app/overview','Início') + ' <span aria-hidden="true">/</span> ' +
      (route.page === 'detail' || route.page === 'new' ? link('/app/assessments','Avaliações')+' / ' : '') +
      `<span>${route.page === 'detail' ? '#'+esc(route.id) : esc(menuLabel || labels[route.page])}</span>`;
    $('#topbar-actions').innerHTML = link('/app/help','Ajuda','btn btn-sm') + (canRun() && ['overview','assessments'].includes(route.page) ? link('/app/assessments/new','Nova avaliação','btn btn-primary') : '');
    document.title = `${$('#page-title').textContent}${route.id ? ' #'+route.id : ''} · ASTRO Cyber`;
    $('#main-content').focus({preventScroll:true});
    if($('#settings-navigation')) $('#settings-navigation').hidden = true;
    busy();
    try {
      if (route.page === 'overview') {
        const [summary,scopes] = await Promise.allSettled([api('/api/dashboard'),api('/api/engagements')]);
        if (!valid()) return;
        if (summary.status === 'rejected') throw summary.reason;
        summary.value.recent = await namedScans(summary.value.recent || []);
        if (!valid()) return;
        workspace.innerHTML = window.ASTRO_EXPERIENCE.overview(summary.value,state.user,isDemo(),scopes.status === 'fulfilled' ? scopes.value.engagements : null);
        return;
      }
      if (route.page === 'assessments' || route.page === 'reports') await assessmentList(route,valid);
      else if (route.page === 'new') await newAssessment(route,valid);
      else if (route.page === 'detail') await assessmentDetail(route,valid);
      else if (route.page === 'scopes') {
        workspace.classList.remove('active'); $('#sec-engagements').classList.add('active');
        await renderEngagements();
        if (!valid()) return;
        $('#page-title').textContent = menuLabel || labels.scopes; $('#page-sub').textContent = 'Autorizações vinculadas à organização';
      } else if (route.page === 'settings') await settings(route,valid);
      else if (route.page === 'help') help();
      else workspace.innerHTML = `<div class="card"><h2>Página não encontrada</h2><p>A rota solicitada não existe.</p>${link('/app/overview','Voltar à visão geral','btn')}</div>`;
      if (valid()) document.title = `${$('#page-title').textContent}${route.id ? ' #'+route.id : ''} · ASTRO Cyber`;
      if (valid() && isDemo() && ['assessments','settings','scopes'].includes(route.page)) {
        const container = route.page === 'scopes' ? $('#sec-engagements') : workspace;
        container.insertAdjacentHTML('afterbegin','<p class="callout" role="status">DEMONSTRAÇÃO — dados sintéticos. Nenhuma avaliação real é realizada.</p>');
        if (['assessments','reports'].includes(route.page)) container.querySelector('.workspace-intro p').textContent = 'Histórico sintético da demonstração, salvo apenas neste navegador. Não representa avaliações reais.';
      }
    } catch (e) { if (valid()) fail(e,true); }
  }
  async function assessmentList(route,valid) {
    const result = await api('/api/scans');
    const scans = await namedScans(result.scans || []);
    if (!valid()) return;
    if (route.page === 'reports') {
      await Promise.allSettled(scans.filter(s=>s.status === 'done').map(async s=> { try { const {findings=[]} = await api('/api/scans/'+s.id+'/findings'); s.verification_counts = {confirmed:0,suspected:0,observation:0,unclassified:0}; findings.forEach(f => s.verification_counts[['confirmed','suspected','observation'].includes(f.verification_status) ? f.verification_status : 'unclassified']++); } catch (_) {} }));
      if(!valid()) return;
      workspace.innerHTML = window.ASTRO_EXPERIENCE.reports(scans,isDemo(),route.query.q || '');
      $('#assessment-search').addEventListener('submit',e => { e.preventDefault(); const query = new URLSearchParams(); if ($('#assessment-query').value.trim()) query.set('q',$('#assessment-query').value.trim()); navigate('/app/reports'+(query.size ? '?'+query : '')); });
      return;
    }
    const report = route.page === 'reports';
    const filtered = scans.filter(s => (!report || s.status === 'done') &&
      (!route.query.status || s.status === route.query.status) &&
      (!route.query.q || `${s.id} ${s.target} ${s.engagement_name || ""}`.toLowerCase().includes(route.query.q.toLowerCase())));
    workspace.innerHTML = `${state.user.role === "cymag" ? window.ASTRO_EXPERIENCE.client(state.user) : ""}<div class="workspace-intro"><div><div class="eyebrow">${report ? 'ENTREGÁVEIS' : 'OPERAÇÕES'} / ASTRO CYBER</div><h2>${report ? 'Relatórios por avaliação' : 'Histórico de avaliações'}</h2><p class="mut">${report ? 'Escolha uma avaliação concluída para visualizar os achados e exportar seu relatório. PDFs são gerados sob demanda; não há biblioteca versionada.' : 'Execuções persistidas da organização. A API retorna até 50 avaliações recentes.'}</p></div></div>
      ${report ? '' : `<div class="workspace-tabs" aria-label="Filtrar avaliações">${[['','Todas'],['running','Em execução'],['done','Concluídas'],['error','Falharam']].map(([value,text]) => link('/app/assessments'+(value ? '?status='+value : ''),text,`workspace-tab ${route.query.status === value || (!value && !route.query.status) ? 'active' : ''}`)).join('')}</div>`}
      <form id="assessment-search" class="row mb"><label for="assessment-query">Buscar ID ou alvo</label><input id="assessment-query" class="input" value="${esc(route.query.q || '')}" placeholder="Ex.: 1001 ou 192.0.2.10"><button class="btn">Buscar</button></form>
      <div class="card table-wrap">${filtered.length ? `<table class="table mobile-cards"><thead><tr><th>ID</th><th>Alvo</th><th>Escopo</th><th>Status</th><th>Achados</th><th>Início</th><th>Ação</th></tr></thead><tbody>${filtered.map(s => `<tr><td data-label="ID" class="mono">${link('/app/assessments/'+s.id,'#'+esc(s.id))}</td><td data-label="Alvo" class="mono">${environment(s)}</td><td data-label="Escopo">${s.engagement_id ? '#'+esc(s.engagement_id) : 'Não registrado'}</td><td data-label="Status">${esc(statusLabels[s.status] || s.status)}</td><td data-label="Achados">${esc(s.findings_count ?? 'Não mensurado')}</td><td data-label="Início">${stamp(s.started_at)}</td><td data-label="Ação">${link('/app/assessments/'+s.id+(report ? '?tab=reports' : ''),report ? 'Visualizar / exportar' : 'Abrir avaliação','btn btn-sm')}</td></tr>`).join('')}</tbody></table>` : `<h3>${scans.length ? 'Nenhuma avaliação corresponde aos filtros' : 'Nenhuma avaliação registrada'}</h3><p class="mut">${scans.length || route.query.q || route.query.status ? 'Busca: “'+esc(route.query.q || '')+'”. Revise a busca ou o status selecionado.' : 'Cadastre e autorize um escopo antes de iniciar. Ausência de avaliações não comprova segurança.'}</p>${scans.length || route.query.q || route.query.status ? link('/app/assessments','Limpar filtros','btn') : link('/app/scopes','Consultar escopos','btn')}`}</div>`;
    $('#assessment-search').addEventListener('submit',e => { e.preventDefault(); const q = new URLSearchParams(); if (route.query.status) q.set('status',route.query.status); if ($('#assessment-query').value.trim()) q.set('q',$('#assessment-query').value.trim()); navigate('/app/'+route.page+(q.size ? '?'+q : '')); });
  }
  async function newAssessment(route,valid) {
    if (!canRun()) { workspace.innerHTML = '<div class="card" role="alert"><h2>Acesso somente leitura</h2><p>Seu perfil permite consultar avaliações. Um operador autorizado precisa iniciar a execução.</p></div>'; return; }
    const {engagements=[]} = await api('/api/engagements');
    if (!valid()) return;
    const approved = engagements.filter(e => e.status === 'authorized');
    if (!approved.length) { workspace.innerHTML = `<div class="card"><h2>Autorize um escopo primeiro</h2><p>Nenhum escopo autorizado foi encontrado. Peça ao Dono ou Admin da organização que revise e autorize os endereços antes de iniciar.</p>${link('/app/scopes','Cadastrar ou revisar escopos','btn btn-primary')}</div>`; return; }
    wizard = {step:0,scope:String(approved[0].id),target:'',mode:route.query.mode === 'async' && hasFeature('autonomous') ? 'async' : 'manual',approved,valid};
    drawWizard();
  }
  function drawWizard() {
    const w = wizard;
    const selected = w.approved.find(e => String(e.id) === w.scope);
    const pages = [
      `<div class="field"><label for="assessment-scope">Escopo autorizado</label><select class="input" id="assessment-scope">${w.approved.map(e => `<option value="${e.id}" ${String(e.id) === w.scope ? 'selected' : ''}>${esc(e.name)} — ${esc(e.scope.join(', '))}</option>`).join('')}</select></div><div class="field"><label for="assessment-target">Alvo dentro do escopo (opcional)</label><input class="input mono" id="assessment-target" value="${esc(w.target)}" placeholder="Ex.: 192.0.2.10" aria-describedby="effective-target"></div><p class="mut" id="effective-target">Alvo efetivo: <code>${esc(w.target || selected?.scope[0])}</code>. Somente endereços autorizados podem ser avaliados.</p>`,
      `<fieldset class="mode-choices"><legend>Modo de execução</legend><label class="mode-choice"><input type="radio" name="assessment-mode" value="manual" ${w.mode === 'manual' ? 'checked' : ''}><span><b>Inventário defensivo</b><small>Aguarde a conclusão; depois, você será levado aos resultados e evidências.</small></span></label><label class="mode-choice"><input type="radio" name="assessment-mode" value="async" ${w.mode === 'async' ? 'checked' : ''} ${hasFeature('autonomous') ? '' : 'disabled'}><span><b>Execução automatizada</b><small>${hasFeature('autonomous') ? 'Execução em segundo plano e acompanhamento por eventos.' : 'Indisponível no plano atual.'}</small></span></label></fieldset><p class="mut">Os dois modos usam o perfil técnico atual; mudar o modo não habilita exploração.</p>`,
      '<h3>Limites do perfil atual</h3><dl class="detail-meta"><dt>Candidatos por execução</dt><dd>Até 64</dd><dt>Portas</dt><dd>Conjunto fixo de portas TCP</dd><dt>Workers socket por host</dt><dd>24</dd><dt>Timeout socket</dt><dd>1,5 segundos por conexão</dd></dl><div class="callout">Sem exploração intrusiva. Agendamento, cancelamento e orçamento global configurável ainda não estão disponíveis. Os limites são definidos pelo servidor.</div>',
      `<h3>Revise antes de iniciar</h3><dl class="detail-meta"><dt>Escopo</dt><dd>${esc(selected?.name)}</dd><dt>Alvos autorizados</dt><dd class="mono">${esc(selected?.scope.join(', '))}</dd><dt>Alvo efetivo</dt><dd class="mono">${esc(w.target || selected?.scope[0])}</dd><dt>Execução</dt><dd>${w.mode === 'async' ? 'Automatizada' : 'Inventário síncrono'}</dd></dl><p class="mut">A autorização será conferida novamente ao iniciar. ${w.mode === 'async' ? 'Você será levado ao console para acompanhar os eventos; os resultados ficam nas abas da avaliação.' : 'Aguarde a conclusão nesta tela; em seguida, abriremos o resumo com os resultados.'} Os resultados refletem apenas as verificações realizadas; não equivalem a um pentest completo.</p><label class="row"><input type="checkbox" id="assessment-confirm"> Revisado: executar somente dentro do escopo autorizado.</label>`
    ];
    workspace.innerHTML = `<div class="workspace-intro"><div class="eyebrow">NOVA AVALIAÇÃO / PASSO ${w.step+1} DE 4</div><h2>Configure sua avaliação</h2></div><ol class="wizard-steps">${['Escopo','Modo','Limites','Revisão'].map((s,i) => `<li ${i === w.step ? 'aria-current="step"' : ''} class="${i === w.step ? 'active' : ''}">${i+1}. ${s}</li>`).join('')}</ol><div class="card wizard-card">${pages[w.step]}<div id="wizard-error" role="alert"></div><div class="wizard-actions"><button class="btn" id="wizard-back" ${w.step === 0 ? 'disabled' : ''}>Voltar</button><button class="btn btn-primary" id="wizard-next">${w.step === 3 ? 'Iniciar avaliação' : 'Continuar'}</button></div></div>`;
    if (w.step === 0) {
      const updateTarget = () => { w.scope = $('#assessment-scope').value; w.target = $('#assessment-target').value.trim(); $('#effective-target').textContent = 'Alvo efetivo: ' + (w.target || w.approved.find(e => String(e.id) === w.scope)?.scope[0]) + '. Somente endereços autorizados podem ser avaliados.'; };
      $('#assessment-scope').addEventListener('change', updateTarget); $('#assessment-target').addEventListener('input', updateTarget);
    }
    $('#wizard-back').addEventListener('click',() => { w.step--; drawWizard(); });
    $('#wizard-next').addEventListener('click',async () => {
      if (w.step === 0) { w.scope = $('#assessment-scope').value; w.target = $('#assessment-target').value.trim(); }
      if (w.step === 1) w.mode = $('input[name="assessment-mode"]:checked').value;
      if (w.step < 3) { w.step++; drawWizard(); $('#main-content').focus({preventScroll:true}); return; }
      if (!$('#assessment-confirm').checked) { fieldError('assessment-confirm', 'Revise e confirme o escopo antes de iniciar.'); $('#assessment-confirm').focus(); return; }
      const button = $('#wizard-next'); button.disabled = true; $('#wizard-back').disabled = true;
      button.innerHTML = '<span class="spinner"></span> Iniciando…';
      const body = {engagement_id:Number(w.scope),target:w.target || w.approved.find(e => String(e.id) === w.scope)?.scope[0]};
      try {
        const response = await api(w.mode === 'async' ? '/api/autonomous/run' : '/api/scan',{method:'POST',body});
        if (response.run_id) rememberRun(response.scan_id,response.run_id);
        if (!w.valid()) { if (state.user) toast('Avaliação #'+response.scan_id+' iniciada. Consulte o histórico de avaliações.'); return; }
        navigate('/app/assessments/'+response.scan_id+(response.run_id ? '?tab=console' : ''));
      } catch (e) {
        if (document.contains(button)) { $('#wizard-error').textContent = e.message; button.disabled = false; $('#wizard-back').disabled = false; button.textContent = 'Iniciar avaliação'; }
      }
    });
  }
  async function assessmentDetail(route,valid) {
    const d = await api('/api/assessments/'+route.id);
    if (!valid()) return;
    const raw = d.assessment || d.scan;
    const s = raw ? (await namedScans([raw]))[0] : null;
    if (!valid()) return;
    if (!s) throw new Error('Contrato de avaliação inválido.');
    const findings = d.findings || [];
    state.lastScan = {scan_id:s.id,target:s.target,cyber_vulns:findings,risk_score:s.risk_score,exec_risks:[]};
    const confirmed = findings.filter(f => f.verification_status === 'confirmed').length;
    const suspected = findings.filter(f => f.verification_status === 'suspected').length;
    const observations = findings.filter(f => f.verification_status === 'observation').length;
    const unclassified = findings.length - confirmed - suspected - observations;
    const hosts = [...new Set(findings.map(f => f.host).filter(Boolean))];
    const title = {summary:'Resumo',console:'Console e eventos',hosts:'Hosts observados',findings:'Achados',coverage:'Cobertura',reports:'Relatórios'};
    let aiOnline = false;
    if(route.tab === 'reports' && hasFeature('ai')) { try { if(state.user.role !== 'admin') throw Error('Status não disponível para este papel'); const ai = await api('/api/admin/ai/status'); aiOnline = !!ai.online; } catch (_) {} if(!valid()) return; }
    let body;
    if (route.tab === 'findings') body = `<div class="card"><h3>Achados desta avaliação</h3>${findingsTable(findings)}</div>`;
    else if (route.tab === 'hosts') body = `<div class="card"><h3>Hosts presentes nos achados</h3><p class="mut">Dados derivados desta avaliação, sem inventário global persistido.</p>${hosts.length ? hosts.map(host => `<details class="host-observation"><summary class="mono">${esc(host)}</summary>${findings.filter(f => f.host === host).map(f => `<p><code>${esc(f.port)}</code> · ${esc(f.title)} · ${esc(VERIFICATION[f.verification_status] || 'Sem classificação')}</p>`).join('')}</details>`).join('') : '<p>Nenhum host com achados registrado. Não significa ausência de ativos.</p>'}</div>`;
    else if (route.tab === 'console') body = `<div class="console-panel"><div class="console-meta"><span>AVALIAÇÃO #${esc(s.id)}</span><span>EVENTOS / UTC</span></div><div class="console-controls"><label for="event-filter">Exibir</label><select id="event-filter"><option value="all">Todos</option><option value="error">Erros</option></select><label><input type="checkbox" id="pause-scroll"> Pausar rolagem</label><span id="event-status" role="status">Consultando execução…</span></div><div id="assessment-events" class="feed" role="log" aria-live="polite" aria-label="Eventos da avaliação"></div></div>`;
    else if (route.tab === 'coverage') body = `<div class="card"><h3>Cobertura e limitações</h3><dl class="detail-meta"><dt>Hosts previstos</dt><dd>Não mensurado</dd><dt>Checks executados</dt><dd>Não mensurado</dd><dt>Timeouts / falhas por check</dt><dd>Não registrado</dd><dt>Hosts com achados</dt><dd>${hosts.length}</dd></dl><p class="mut">O scanner atual executa inventário TCP limitado. A execução histórica não contém versionamento completo do método. Sem cobertura estruturada não é possível concluir que um ativo está seguro ou corrigido.</p><p class="mut">Eventos são mantidos em memória; podem se perder quando o servidor reinicia.</p></div>`;
    else if (route.tab === 'reports') body = `<div class="card"><h3>Visualização e exportação</h3><p>Relatório técnico: evidências registradas e limitações. Relatório com IA: acrescenta orientações do modelo, que exigem revisão humana e não confirmam achados.</p><p id="report-ai-reason">${aiOnline ? "IA disponível para orientações complementares." : "Relatório com IA indisponível: integração offline, recurso ausente no plano ou status indisponível para seu papel. Peça ao Admin para conferir."}</p><p class="mut">Avaliação #${esc(s.id)} · ${isDemo() ? 'DEMONSTRAÇÃO — dados sintéticos' : 'Achados persistidos e autorizados'}. O PDF será gerado sob demanda; não há relatório versionado armazenado.</p>${s.status === 'done' ? `<div class="row mb"><button class="btn btn-primary" id="detail-pdf">Exportar relatório técnico</button><button class="btn" id="detail-pdf-ai" ${aiOnline ? '' : 'disabled'} aria-describedby="report-ai-reason">Relatório com IA</button></div>${["owner","viewer"].includes(state.user.role) ? `<div class="executive-report-summary"><h3>Síntese da avaliação</h3><p>${confirmed} confirmados · ${suspected} suspeitas · ${observations} observações · ${unclassified} não classificados.</p><p>Solicite à TI a revisão das evidências. Ausência de achados não comprova segurança.</p></div>` : findingsTable(findings)}` : '<p>Finalize a avaliação para gerar o relatório.</p>'}</div>`;
    else body = `<div class="grid summary-metrics mb">${statCard(findings.length,'Achados registrados')}${statCard(confirmed,'Confirmados')}${statCard(suspected,'Suspeitas')}<div id="unclassified-count" class="${unclassified > 0 ? "needs-review" : ""}">${statCard(unclassified,'Não classificados')}</div>${statCard(observations,'Observações')}</div><p class="mut small" id="summary-decomposition">${findings.length} registrados = ${confirmed} confirmados + ${suspected} suspeitas + ${unclassified} não classificados + ${observations} observações.</p><div class="card"><h3>Resultado e próximos passos</h3><p>Consulte a evidência de cada achado antes de definir uma ação. A ausência de achados não comprova segurança.</p><div class="row">${link('/app/assessments/'+s.id+'?tab=findings','Investigar achados','btn')}${link('/app/assessments/'+s.id+'?tab=coverage','Consultar limitações','btn')}</div></div>`;
    workspace.innerHTML = `<div class="workspace-intro"><div><div class="eyebrow">AVALIAÇÃO #${esc(s.id)}</div><h2>${environment(s)}</h2>${state.user.role === "cymag" ? window.ASTRO_EXPERIENCE.client(state.user) : ""}<p>${stamp(s.started_at)}</p><p>${esc(statusLabels[s.status] || s.status)} · ${isDemo() ? 'Dados sintéticos' : 'Registro persistido'}</p></div><button class="btn" id="copy-assessment">Copiar link</button></div><div class="workspace-tabs" aria-label="Seções da avaliação">${routes.TABS.map(tab => link('/app/assessments/'+s.id+'?tab='+tab,title[tab],`workspace-tab ${route.tab === tab ? 'active' : ''}`)).join('')}</div><div class="assessment-layout"><div class="assessment-body">${body}</div><details class="card assessment-inspector"><summary>Metadados da execução</summary><dl class="detail-meta"><dt>ID</dt><dd class="mono">#${esc(s.id)}</dd><dt>Organização</dt><dd>${esc(state.user.account?.name)}</dd><dt>Escopo</dt><dd>${s.engagement_id ? '#'+esc(s.engagement_id) : 'Não registrado'}</dd><dt>Início</dt><dd>${stamp(s.started_at)}</dd><dt>Fim</dt><dd>${stamp(s.finished_at)}</dd><dt>Modo histórico</dt><dd>Não registrado no schema</dd></dl><p class="mut">Ativos, achados globais e correções com revalidação dependem de modelos persistidos ainda planejados.</p>${link('/app/scopes','Consultar escopos','btn btn-sm')}</details></div>`;
    wireFindingButtons(workspace,findings);
    workspace.querySelector('.workspace-intro > div > p:last-child').id = 'assessment-status';
    workspace.querySelectorAll('.assessment-inspector dd')[4].id = 'assessment-finished';
    $('#detail-pdf')?.addEventListener('click',() => downloadPDF('quick'));
    $('#detail-pdf-ai')?.addEventListener('click',() => downloadPDF('detailed'));
    $('#copy-assessment').addEventListener('click',async () => {
      const url = new URL(location.href); if (isDemo()) url.searchParams.set('demo','1');
      try { await navigator.clipboard.writeText(url.href); toast('Link copiado. Acesso real exige autenticação e organização autorizada.'); }
      catch (_) { openModal(`<h2>Link da avaliação</h2><input class="input" aria-label="Link para copiar" readonly value="${esc(url.href)}"><button class="btn" onclick="closeModalGlobal()">Fechar</button>`); }
    });
    if (route.tab === 'console') trackEvents(s,valid);
    else if (s.status === 'running') timer = setTimeout(() => refreshMetadata(s,valid),4000);
  }
  async function refreshMetadata(scan,valid,repeat=true) {
    try {
      const data = await api('/api/assessments/'+scan.id);
      if (!valid()) return;
      const current = data.assessment;
      state.lastScan = {scan_id:current.id,target:current.target,cyber_vulns:data.findings || [],risk_score:current.risk_score,exec_risks:[]};
      const counters = workspace.querySelectorAll('.stat .num');
      if (counters.length === 5) {
        const list = data.findings || [];
        const confirmed = list.filter(f => f.verification_status === 'confirmed').length;
        const suspected = list.filter(f => f.verification_status === 'suspected').length;
        const observations = list.filter(f => f.verification_status === 'observation').length;
        const breakdown = $('#summary-decomposition');
        if (breakdown) breakdown.textContent = `${list.length} registrados = ${confirmed} confirmados + ${suspected} suspeitas + ${list.length-confirmed-suspected-observations} não classificados + ${observations} observações.`;
        [list.length,confirmed,suspected,list.length-confirmed-suspected-observations,observations].forEach((count,index) => counters[index].textContent = count);
        $('#unclassified-count')?.classList.toggle('needs-review',list.length-confirmed-suspected-observations > 0);
      }
      $('#assessment-status').textContent = `${statusLabels[current.status] || current.status} · ${isDemo() ? 'Dados sintéticos' : 'Registro persistido'}`;
      $('#assessment-finished').innerHTML = stamp(current.finished_at);
      if (current.status !== 'running') {
        if (scan.status === 'running') toast('Avaliação finalizada. Consulte as abas para ver os resultados atualizados.');
        scan.status = current.status;
        return;
      }
      if (repeat) timer = setTimeout(() => refreshMetadata(scan,valid),4000);
    } catch (e) {
      if (valid() && repeat && e.status !== 404) timer = setTimeout(() => refreshMetadata(scan,valid),8000);
    }
  }
  function trackEvents(scan,valid) {
    const run = runs()[scan.id];
    if (!run) {
      $('#event-status').textContent = 'Histórico indisponível';
      $('#event-filter').disabled = true;
      $('#pause-scroll').disabled = true;
      $('#assessment-events').insertAdjacentHTML('beforebegin', `<div class="callout console-unavailable"><b>Histórico indisponível</b><p>Não há eventos acessíveis para esta execução.</p>${link('/app/assessments/'+scan.id+'?tab=findings','Consultar resultados','btn')}</div>`);
      $('#assessment-events').textContent = 'Eventos históricos não são persistidos. Os resultados e o estado da avaliação podem ser consultados nas outras abas.';
      if (scan.status === 'running') timer = setTimeout(() => refreshMetadata(scan,valid),4000);
      return;
    }
    let events = [], since = 0, failures = 0;
    function draw() {
      if (!valid()) return;
      const feed = $('#assessment-events'); const filter = $('#event-filter').value;
      feed.innerHTML = events.filter(e => filter === 'all' || e.phase === filter).map(e => `<div class="event-line"><time>${esc(e.ts || '')}</time><span>${esc(e.phase)}</span><span>${esc(e.message)}</span></div>`).join('');
      if (!$('#pause-scroll').checked) feed.scrollTop = feed.scrollHeight;
    }
    $('#event-filter').addEventListener('change',draw);
    async function poll() {
      try {
        const r = await api(`/api/autonomous/${encodeURIComponent(run)}?since=${since}`);
        if (!valid()) return;
        failures = 0;
        events.push(...(r.events || [])); since = r.event_count;
        $('#event-status').textContent = statusLabels[r.status] || r.status;
        draw();
        if (r.status === 'done' || r.status === 'error') { await refreshMetadata(scan,valid,false); return; }
        timer = setTimeout(poll,1500);
      } catch (e) { if (valid()) { failures++; $('#event-status').textContent = 'Falha de coleta'; if (failures === 1) $('#assessment-events').insertAdjacentHTML('beforeend',`<p role="alert">${esc(e.message)}. A execução pode continuar. Eventos podem ter se perdido após reinício.</p>`); if (e.status !== 404 && failures < 4) timer = setTimeout(poll,Math.min(12000,1500*2**failures)); } }
    }
    poll();
  }
  function settingsNav(tab) {
    return `<nav class="settings-nav" aria-label="Seções de configurações">${[['organization','Organização'],['team','Equipe'],...(state.user.role === 'admin' ? [['ai','Integração de IA']] : []),...(state.user.is_staff ? [['legacy-ops','Operação interna']] : [])].map(([key,label]) => link('/app/settings?tab='+key,label,'btn '+(tab === key ? 'active' : ''))).join('')}</nav>`;
  }
  async function settings(route,valid) {
    const tab = ['team','ai','legacy-ops'].includes(route.query.tab) ? route.query.tab : 'organization';
    if(tab === 'ai' || tab === 'legacy-ops') {
      if(tab === 'ai' ? state.user.role !== 'admin' : !state.user.is_staff) { workspace.innerHTML = '<div class="card" role="alert">Esta seção exige um papel autorizado.</div>'; return; }
      originalShowSection(tab === 'ai' ? 'ia' : 'central');
      const section = $(tab === 'ai' ? '#sec-ia' : '#sec-central');

      // Renderers are asynchronous: the persistent shell lives outside their content.
      let shell = $('#settings-navigation');
      if(!shell) { shell = document.createElement('div'); shell.id = 'settings-navigation'; section.before(shell); }
      shell.innerHTML = settingsNav(tab); shell.hidden = false;
      $('#page-title').textContent = tab === 'ai' ? 'Integração de IA' : 'Operação interna · legado';
      return;
    }
    const d = await api('/api/account'); if (!valid()) return;
    workspace.innerHTML = settingsNav(tab) + (tab === 'team' ? `<section class="card settings-section"><h2>Equipe</h2><p>Pessoas associadas à organização atual, em consulta somente leitura.</p><p>Convites, remoção, edição de papéis, MFA e sessões ainda não estão disponíveis.</p>${d.team?.length ? `<table class="table"><thead><tr><th>Nome</th><th>E-mail</th><th>Papel</th></tr></thead><tbody>${d.team.map(m=>`<tr><td>${esc(m.name)}</td><td>${esc(m.email)}</td><td>${esc(ROLE_LABEL[m.role] || m.role)}</td></tr>`).join('')}</tbody></table>` : '<p>Nenhum membro disponível para consulta com seu papel.</p>'}</section>` : `<section class="card settings-section"><h2>Organização</h2><p>Conta, papel de acesso e plano da organização atual.</p><h3>${esc(d.account.name)}</h3><dl class="detail-meta"><dt>Conta</dt><dd class="mono">#${esc(d.account.id)}</dd><dt>Papel atual</dt><dd>${esc(ROLE_LABEL[state.user.role] || state.user.role)}</dd><dt>Plano</dt><dd>${esc(d.plan.name)}</dd></dl><h3>Assinatura simulada</h3><p>Limite mensal de avaliações: ${esc(d.plan.scans_per_month ?? 'Não definido')}. Cobrança simulada; não comprova uma contratação paga.</p><p>Troca de organização e alteração de conta ainda não estão disponíveis. Esta seção é somente leitura.</p></section>`);
  }
  function help() {
    const tasks = {
      owner:[['Quero entender o painel',['Leia a pendência de revisão em destaque.','Confira os estados dos achados.','Abra a avaliação e consulte a cobertura.','Peça à TI a revisão das evidências.']],['Quero autorizar um alvo',['Abra Autorizações.','Revise com a TI o nome e os endereços do escopo.','Confirme que você pode autorizar esses ativos.','Autorize somente o escopo revisado.']]],
      viewer:[['Quero ler a síntese',['Leia Situação e Pendências no panorama.','Confira a data da informação.','Abra Relatórios e leia o resumo.','Apresente os limites junto com os resultados.']]],
      operator:[['Quero iniciar uma avaliação',['Confira se o escopo foi autorizado.','Abra Nova avaliação e confira o alvo efetivo.','Escolha o modo e leia os limites.','Revise e confirme antes de iniciar.']],['Quero investigar um achado',['Abra a avaliação e a aba Achados.','Filtre pelo ativo e pelo estado.','Leia a evidência técnica e a origem.','Valide o achado antes de seguir a orientação de correção.']]]
    };
    const items = tasks[state.user.role] || (state.user.role === 'admin' ? [['Quero configurar a organização',['Abra Configurações e confira a conta e seu papel.','Consulte Equipe para conferir os acessos disponíveis.','Abra Integração de IA e teste os valores.','Aplique somente após receber Teste OK.']]] : tasks.operator);
    workspace.innerHTML = `<div class="workspace-intro"><h2>Ajuda por tarefa</h2></div><div class="grid grid-2 task-help">${items.map(([title,steps])=>`<section class="card"><h3>${title}</h3><ol>${steps.map(step=>`<li>${step}</li>`).join('')}</ol></section>`).join('')}</div><section class="card box-end"><h3>Como interpretar os estados</h3><p><b>Não encontrado:</b> a verificação não observou o problema; isso não comprova segurança.</p><p><b>Não verificado:</b> há um indício ou registro sem validação suficiente.</p><p><b>Confirmado:</b> há evidência validada para o achado, dentro do método e da cobertura informados.</p></section><section id="method-limits" class="card box-end"><h3>Método e limites</h3><p>Cadastre e autorize o escopo, configure a avaliação, investigue evidências e exporte o relatório.</p><p>Observação, suspeita e confirmação são estados diferentes. O perfil atual registra inventário TCP limitado; não executa exploração intrusiva.</p><p>Inventário global, responsáveis, prazos, correções revalidadas e agendamento dependem de capacidades ainda indisponíveis. Eventos não são duráveis; ausência em uma avaliação não significa correção.</p></section>`;
  }
  // Same-origin route anchors retain normal opening in another tab.
  document.addEventListener('click',e => {
    const anchor = e.target.closest('a[data-route]');
    if (!anchor || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey || e.button !== 0) return;
    e.preventDefault(); navigate(anchor.pathname+anchor.search);
  });
  window.addEventListener('popstate',renderRoute);
  const originalOpenModal = openModal;
  const originalCloseModal = closeModal;
  let modalReturnFocus = null;
  openModal = (html,wide) => {
    modalReturnFocus = document.activeElement;
    originalOpenModal(html,wide);
    $('#modal').setAttribute('role','dialog'); $('#modal').setAttribute('aria-modal','true');
    $('#modal').setAttribute('aria-label',$('#modal h2')?.textContent || 'Detalhes');
    $('#modal').querySelector('button,input,select,a[href]')?.focus();
  };
  closeModal = () => { originalCloseModal(); modalReturnFocus?.focus(); };
  window.closeModalGlobal = closeModal;
  const originalOpenSidebar = openSidebar;
  const originalCloseSidebar = closeSidebar;
  closeSidebar = () => { originalCloseSidebar(); $('#menu-toggle').setAttribute('aria-expanded','false'); };
  openSidebar = () => { restoreFocus = document.activeElement; originalOpenSidebar(); $('#menu-toggle').setAttribute('aria-expanded','true'); $('#sidebar').querySelector('a,button')?.focus(); };
  $('#menu-toggle').removeEventListener('click',originalOpenSidebar);
  $('#menu-toggle').addEventListener('click',openSidebar);
  document.addEventListener('keydown',e => {
    if ($('#modal-back').classList.contains('open')) {
      if (e.key === 'Escape') { closeModal(); return; }
      if (e.key === 'Tab') {
        const elements = [...$('#modal').querySelectorAll('button,input,select,a[href],textarea')].filter(el => !el.disabled && el.offsetParent !== null);
        if (e.shiftKey && document.activeElement === elements[0]) { e.preventDefault(); elements.at(-1)?.focus(); }
        else if (!e.shiftKey && document.activeElement === elements.at(-1)) { e.preventDefault(); elements[0]?.focus(); }
      }
      return;
    }
    if (!$('#sidebar').classList.contains('open')) return;
    if (e.key === 'Escape') { closeSidebar(); $('#menu-toggle').setAttribute('aria-expanded','false'); restoreFocus?.focus(); }
    if (e.key === 'Tab') {
      const focusable = [...$('#sidebar').querySelectorAll('a,button')].filter(el => el.offsetParent !== null);
      const first = focusable[0], last = focusable.at(-1);
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });
  window.ASTRO_ROUTER = {navigate,renderRoute,async boot() {
    let demoRole = null; try { demoRole = sessionStorage.getItem('astro-demo-session'); } catch (_) {}
    if (!['owner','operator','viewer','cymag','admin'].includes(demoRole)) demoRole = null;
    if (location.pathname === '/demo') {
      const requestedRole = new URLSearchParams(location.search).get('role');
      enterDemo(['owner','operator','viewer','cymag','admin'].includes(requestedRole) ? requestedRole : demoRole || 'operator'); return;
    }
    try { const me = await api('/api/me'); if (me.authenticated) { enterApp(me); return; } if (new URLSearchParams(location.search).get('demo') === '1' || (demoRole && location.pathname.startsWith('/app/'))) enterDemo(demoRole || 'operator'); else showLogin(); }
    catch (_) { if (demoRole && location.pathname.startsWith('/app/')) enterDemo(demoRole); else showLogin(); }
  }};
})();
