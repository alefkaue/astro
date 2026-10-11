/* Shared contextual terms; native buttons provide Enter/Space activation. */
(function () {
  'use strict';
  const definitions = {
    hosts:'Equipamentos ou endereços observados na avaliação. A lista não representa um inventário completo da rede.',
    achado:'Registro de algo observado na avaliação. Sua evidência e seu estado indicam se exige validação.',
    escopo:'Conjunto de alvos autorizados para esta avaliação. Autorizar exige permissão para avaliar esses ativos.',
    cobertura:'O que foi efetivamente verificado e seus limites. Sem cobertura suficiente, ausência de achados não comprova segurança.',
    CVSS:'Escala de severidade técnica de uma vulnerabilidade. Não comprova o achado e não estima prejuízo financeiro.',
    'CIDR/IP':'IP identifica um endereço de rede; CIDR descreve uma faixa, por exemplo 192.0.2.0/24. Peça à TI os endereços corretos antes de autorizar.',
    'não classificado':'Registro que ainda não foi classificado como observação, suspeita ou confirmação. Precisa de revisão técnica.'
  };
  let serial = 0;
  function term(key, label=key) {
    const wrapper = document.createElement('span'); wrapper.className = 'glossary-term';
    const button = document.createElement('button'); button.type = 'button'; button.className = 'glossary-trigger'; button.textContent = label;
    const panel = document.createElement('span'); panel.id = 'glossary-'+(++serial); panel.className = 'glossary-popover'; panel.hidden = true;
    button.setAttribute('aria-describedby',panel.id); button.setAttribute('aria-expanded','false');
    const description = document.createElement('span'); description.textContent = definitions[key]; panel.append(description);
    const help = document.createElement('a'); help.href='/app/help#method-limits'; help.dataset.route=''; help.textContent='Ajuda e documentação'; panel.append(' ',help);
    button.addEventListener('click',()=>{ panel.hidden=!panel.hidden; button.setAttribute('aria-expanded',String(!panel.hidden)); });
    wrapper.addEventListener('keydown',event=>{ if(event.key==='Escape'){ event.preventDefault(); panel.hidden=true; button.setAttribute('aria-expanded','false'); button.focus(); } });
    wrapper.append(button,panel); return wrapper;
  }
  function enhance() {
    if(!['owner','viewer'].includes(document.documentElement.dataset.role) && document.documentElement.dataset.workspace !== 'executive') return;
    const roots = [...document.querySelectorAll('#sec-workspace.active,#sec-engagements.active')];
    const pattern = /\b(hosts|achados?|escopos?|cobertura|CVSS|CIDRs?\/IPs?|não classificados?)\b/gi;
    for(const root of roots) {
      const walker = document.createTreeWalker(root,NodeFilter.SHOW_TEXT); const nodes=[];
      while(walker.nextNode()) if(!walker.currentNode.parentElement.closest('a,button,input,select,textarea,code,.mono,.glossary-term,script,style')) nodes.push(walker.currentNode);
      for(const node of nodes) {
        const value=node.textContent; pattern.lastIndex=0; if(!pattern.test(value)) continue; pattern.lastIndex=0;
        const fragment=document.createDocumentFragment(); let cursor=0;
        for(const match of value.matchAll(pattern)) {
          fragment.append(value.slice(cursor,match.index)); const lower=match[0].toLowerCase();
          const key = lower.startsWith('achad') ? 'achado' : lower.startsWith('escop') ? 'escopo' : lower.startsWith('cidr') ? 'CIDR/IP' : lower.startsWith('não classificado') ? 'não classificado' : lower === 'cvss' ? 'CVSS' : lower;
          fragment.append(term(key,match[0])); cursor=match.index+match[0].length;
        }
        fragment.append(value.slice(cursor)); node.replaceWith(fragment);
      }
    }
  }
  let scheduled=false;
  new MutationObserver(()=>{ if(scheduled) return; scheduled=true; queueMicrotask(()=>{ scheduled=false; enhance(); }); }).observe(document.querySelector('#main-content'),{childList:true,subtree:true});
  document.addEventListener('click',event=>{ document.querySelectorAll('.glossary-term').forEach(wrapper=>{ if(!wrapper.contains(event.target)){wrapper.querySelector('.glossary-popover').hidden=true;wrapper.querySelector('button').setAttribute('aria-expanded','false');} }); });
  window.ASTRO_GLOSSARY = {term,definitions};
})();
