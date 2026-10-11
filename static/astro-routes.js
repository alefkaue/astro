(function(root) {
  'use strict';
  const PAGES = ['overview','assessments','scopes','reports','settings','help'];
  const TABS = ['summary','console','hosts','findings','coverage','reports'];
  function parse(input) {
    const url = new URL(input, 'http://localhost');
    const path = url.pathname.replace(/\/$/, '') || '/';
    const query = Object.fromEntries(url.searchParams);
    if (path === '/app/assessments/new') return { page:'new', query };
    const match = path.match(/^\/app\/assessments\/(\d+)$/);
    if (match) return { page:'detail', id:Number(match[1]), query, tab:TABS.includes(query.tab) ? query.tab : 'summary' };
    const page = path.replace(/^\/app\//, '');
    if (PAGES.includes(page)) return { page, query };
    if (['/','/app','/demo','/login'].includes(path)) return { page:'overview', query };
    return { page:'notfound', query };
  }
  function legacy(id) {
    const map = {overview:'/app/overview',exec:'/app/overview',resumo:'/app/overview',
      scan:'/app/assessments/new',autonomous:'/app/assessments/new?mode=async',history:'/app/assessments',
      engagements:'/app/scopes',areas:'/app/help',conta:'/app/settings',billing:'/app/settings?tab=subscription',
      planos:'/app/settings?tab=plans',ia:'/app/settings?tab=ai',central:'/app/settings?tab=legacy-ops'};
    return map[id] || '/app/overview';
  }
  const api = {parse,legacy,PAGES,TABS};
  root.ASTRO_ROUTES = api;
  if (typeof module !== 'undefined') module.exports = api;
})(typeof window !== 'undefined' ? window : globalThis);
