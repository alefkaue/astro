/* Presentation from real API contracts. Profile selection grants no permissions. */
(function(root) {
  'use strict';
  const e = value => String(value ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const a = (href,text,cls='') => `<a href="${e(href)}" data-route class="${cls}">${text}</a>`;
  const status = {done:'Concluída',running:'Em execução',error:'Falhou',pending:'Pendente'};
  const operational = role => ['operator','cymag','admin'].includes(role);
  function profile(role) {
    if (operational(role)) return {kind:'operations',title:'Centro de operações',name:role === 'operator' ? 'Operador' : 'Equipe ASTRO',description:'Execução, cobertura e evidências',groups:[
      ['TRABALHO',[['overview','Centro de operações','overview'],['assessments/new','Nova avaliação','scan'],['assessments','Execuções','history']]],
      ['CONTROLE',[['scopes','Escopos autorizados','engagements'],['reports','Relatórios técnicos','resumo']]],
      ['WORKSPACE',[['settings','Configurações','conta'],['help','Método e limites','areas']]]
    ]};
    const viewer = role === 'viewer';
    return {kind:'executive',title:'Panorama de segurança',name:viewer ? 'Consulta executiva' : 'Gestão da organização',description:'Prioridades, avaliações e decisões',groups:[
      ['SEGURANÇA',[['overview','Panorama','overview'],['reports','Relatórios','resumo'],['assessments','Avaliações','history']]],
      ['ORGANIZAÇÃO',[...(!viewer ? [['scopes','Autorizações','engagements']] : []),['settings',viewer ? 'Minha organização' : 'Organização e equipe','conta']]],
      ['SUPORTE',[['help','Ajuda e método','areas']]]
    ]};
  }
  function provenance(summary,demo) {
    return `<div class="data-provenance"><span>${demo || summary.source === 'synthetic_demo' ? 'DEMONSTRAÇÃO · DADOS SINTÉTICOS' : 'DADOS PERSISTIDOS DA ORGANIZAÇÃO'}</span><span>Atualização: <time>${e(summary.generated_at)}</time></span></div>`;
  }
  function metric(value,label,note='') {
    return `<div class="experience-metric"><span class="metric-label">${e(label)}</span><strong>${e(value ?? '—')}</strong><small>${e(note)}</small></div>`;
  }
  function activity(scans,compact=false) {
    if (!scans.length) return '<div class="experience-empty"><h3>O primeiro resultado começa com um escopo</h3><p>Nenhuma avaliação registrada. Defina e autorize os ativos antes de executar.</p>'+a('/app/scopes','Consultar escopos','btn')+'</div>';
    return `<div class="execution-list">${scans.map(s=>a('/app/assessments/'+s.id,`<span class="execution-id mono">#${e(s.id)}</span><span class="execution-target"><b class="mono">${e(s.target)}</b><small>${e(s.started_at || 'Data não registrada')}</small></span><span class="execution-state"><i class="state-marker state-${e(s.status)}" aria-hidden="true"></i>${e(status[s.status] || s.status)}</span>${compact ? '' : `<span class="execution-count">${e(s.findings_count ?? '—')} <small>achados</small></span>`}<span aria-hidden="true">↗</span>`,'execution-row')).join('')}</div>`;
  }
  function distribution(severity) {
    const names={crit:'Crítica',high:'Alta',med:'Média',low:'Baixa',info:'Informativa'};
    const total = Object.values(severity).reduce((sum,n)=>sum+Number(n || 0),0);
    return `<div class="severity-distribution">${Object.entries(names).map(([key,name])=>`<div class="distribution-row"><span>${name}</span><div class="distribution-track"><span style="width:${total ? Number(severity[key] || 0)/total*100 : 0}%"></span></div><b>${e(severity[key] || 0)}</b></div>`).join('')}</div><p class="mut small">Severidade não comprova vulnerabilidade. Confirmação e evidência são avaliadas separadamente.</p>`;
  }
  function overview(summary,user,demo,scopes) {
    const p=profile(user.role), c=summary.counts, recent=summary.recent || [];
    const authorized=scopes ? scopes.filter(s=>s.status==='authorized').length : null;
    const priorities=[];
    if (c.pending_validation) priorities.push([`${c.pending_validation} suspeitas aguardam validação`,'Confirme a evidência antes de priorizar uma correção.','/app/assessments']);
    if (c.unclassified) priorities.push([`${c.unclassified} achados sem classificação`,'Resultados legados precisam de revisão técnica.','/app/assessments']);
    if (c.failed) priorities.push([`${c.failed} avaliações falharam`,'Investigue a execução; falha não significa que o ativo está seguro.','/app/assessments?status=error']);
    if (authorized===0) priorities.push(['Nenhum escopo autorizado','Revise os ativos e obtenha autorização antes da primeira execução.','/app/scopes']);
    const priorityHTML=priorities.length ? priorities.map(([title,description,href],index)=>a(href,`<span class="priority-number mono">${String(index+1).padStart(2,'0')}</span><span><b>${e(title)}</b><small>${e(description)}</small></span><span aria-hidden="true">↗</span>`,'priority-row')).join('') : '<p class="experience-empty">Nenhuma pendência identificada nestes indicadores. Isso não comprova ausência de riscos; consulte cobertura e evidências.</p>';
    const coverage=`<div class="coverage-statement"><span class="eyebrow">O QUE OS DADOS PERMITEM DIZER</span><h3>${e(c.observed_hosts)} hosts com achados</h3><p>${e(summary.coverage)}</p><ul>${(summary.limitations || []).map(v=>`<li>${e(v)}</li>`).join('')}</ul>${a('/app/assessments','Investigar a origem dos dados →')}</div>`;
    if(p.kind==='executive') return `${provenance(summary,demo)}<section class="experience-hero executive-hero"><div><span class="eyebrow">${e(user.account?.name)} / ${e(p.name)}</span><h2>A segurança da sua<br>organização, em perspectiva.</h2><p>Entenda o que foi avaliado, o que precisa de atenção e quais evidências sustentam as decisões.</p>${a('/app/reports','Consultar relatórios','btn btn-primary')} ${!['viewer'].includes(user.role) ? a('/app/scopes','Revisar autorizações','btn') : ''}</div><aside class="hero-summary"><span class="eyebrow">RESULTADOS CLASSIFICADOS</span><strong>${e(c.confirmed)}</strong><span>achados confirmados</span><p>Dentro da cobertura registrada.<br>Zero não significa risco zero.</p></aside></section><section class="experience-metrics">${metric(c.assessments,'Avaliações registradas','Histórico da organização')}${metric(c.completed,'Concluídas','Execuções finalizadas')}${metric(c.pending_validation,'A validar','Suspeitas, não confirmações')}${metric(c.observations,'Observações','Serviços e exposições observados')}</section><div class="experience-columns"><section class="card priority-panel"><div class="experience-heading"><div><span class="eyebrow">PRÓXIMAS DECISÕES</span><h3>Atenção prioritária</h3></div>${a('/app/assessments','Ver avaliações →')}</div>${priorityHTML}</section><section class="card">${coverage}</section></div><section class="card box-end"><div class="experience-heading"><div><span class="eyebrow">RASTREABILIDADE</span><h3>Avaliações recentes</h3></div>${a('/app/assessments','Histórico completo →')}</div>${activity(recent.slice(0,5),true)}</section>`;
    return `${provenance(summary,demo)}<section class="experience-hero operations-hero"><div><span class="eyebrow">SECURITY OPERATIONS / ${e(user.account?.name)}</span><h2>Observe. Investigue.<br>Valide com evidências.</h2><p>Execute avaliações em escopos autorizados e acompanhe os resultados de cada operação.</p>${a('/app/assessments/new','Iniciar avaliação','btn btn-primary')} ${a('/app/assessments?status=running','Acompanhar execuções','btn')}</div><aside class="operational-readout"><div><span>EM EXECUÇÃO</span><strong>${e(c.running)}</strong></div><div><span>FALHAS NO HISTÓRICO</span><strong>${e(c.failed)}</strong></div><div><span>ESCOPOS AUTORIZADOS</span><strong>${authorized===null ? 'Indisponível' : e(authorized)}</strong></div></aside></section><section class="experience-metrics">${metric(c.completed,'Finalizadas')}${metric(c.confirmed,'Confirmados','Evidência validada')}${metric(c.pending_validation,'Suspeitas','Validação pendente')}${metric(c.unclassified,'Não classificados','Revisar dados legados')}</section><div class="operations-grid"><section class="card operations-activity"><div class="experience-heading"><div><span class="eyebrow">EXECUTION WORKSPACE</span><h3>Últimas operações</h3></div>${a('/app/assessments','Todas →')}</div>${activity(recent)}</section><aside><section class="card"><span class="eyebrow">TRIAGEM</span><h3>Distribuição por severidade</h3>${distribution(summary.severity)}</section><section class="card box-end"><h3>Próximo trabalho</h3>${priorityHTML}</section></aside></div><section class="card box-end">${coverage}</section>`;
  }
  function reports(scans,demo,query='') {
    const completed=scans.filter(s=>s.status==='done');
    const filtered=completed.filter(s=>`${s.id} ${s.target}`.toLowerCase().includes(query.toLowerCase()));
    return `<div class="report-studio-header"><div><span class="eyebrow">ASTRO / REPORT STUDIO</span><h2>Resultados que podem<br>ser compartilhados.</h2><p>Abra uma avaliação para consultar a evidência e exportar seu relatório técnico.</p></div><div class="report-total"><strong>${completed.length}</strong><span>avaliações disponíveis</span></div></div>${demo ? '<p class="callout">DEMONSTRAÇÃO — dados sintéticos, nenhuma avaliação real realizada.</p>' : ''}<form id="assessment-search" class="row mb"><label for="assessment-query">Buscar avaliação</label><input class="input" id="assessment-query" value="${e(query)}" placeholder="ID ou alvo"><button class="btn">Buscar</button></form><p class="mut small">PDFs são gerados sob demanda. Esta lista não representa relatórios versionados ou previamente assinados.</p><div class="report-gallery">${filtered.length ? filtered.map(s=>`<article class="report-document"><div class="report-paper"><span class="eyebrow">ASTRO CYBER</span><span class="report-document-type">AVALIAÇÃO DE SEGURANÇA</span><h3 class="mono">${e(s.target)}</h3><div class="report-lines" aria-hidden="true"><i></i><i></i><i></i></div><dl><dt>Avaliação</dt><dd class="mono">#${e(s.id)}</dd><dt>Achados registrados</dt><dd>${e(s.findings_count ?? 'Não mensurado')}</dd><dt>Finalização</dt><dd>${e(s.finished_at || 'Não registrada')}</dd></dl></div><footer><span>${demo ? 'DEMONSTRAÇÃO' : 'Dados persistidos'}</span>${a('/app/assessments/'+s.id+'?tab=reports','Visualizar e exportar ↗','btn btn-sm')}</footer></article>`).join('') : '<div class="card experience-empty"><h3>Nenhuma avaliação concluída corresponde à busca</h3><p>Relatórios ficam disponíveis depois da execução.</p>'+a('/app/assessments','Consultar avaliações','btn')+'</div>'}</div>`;
  }
  const experience={profile,overview,reports};
  root.ASTRO_EXPERIENCE=experience;
  if(typeof module!=='undefined') module.exports=experience;
})(typeof window!=='undefined' ? window : globalThis);
