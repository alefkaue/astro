// Offline demo contract and theme checks. No browser or third-party packages.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');

async function main() {
  const storage = new Map();
  const localStorage = { getItem:k => storage.get(k) || null, setItem:(k,v) => storage.set(k,v), removeItem:k => storage.delete(k) };
  const context = { window:{}, localStorage, URLSearchParams, console, setTimeout:fn => { fn(); return 1; }, Date,
    fetch:() => { throw new Error('Demo must not call the network'); } };
  vm.createContext(context);
  vm.runInContext(fs.readFileSync('static/cymag-demo.js','utf8'), context);
  context.window.CYMAG_DEMO.enable();
  const summary = await context.window.__demoApi('/api/dashboard',{});
  assert.equal(summary.source,'synthetic_demo');
  assert.equal(summary.counts.assessments,summary.recent.length);
  assert.equal(Object.values(summary.severity).reduce((a,b) => a+b,0),
    summary.counts.confirmed + summary.counts.pending_validation + summary.counts.observations + summary.counts.unclassified);
  assert.match(summary.coverage,/DEMO/);
  const routes = require('../static/astro-routes.js');
  assert.equal(routes.parse('/app/assessments/new?mode=async').page,'new');
  assert.equal(routes.parse('/app/assessments/1001?tab=console').tab,'console');
  assert.equal(routes.parse('/app/assessments/1001?tab=unknown').tab,'summary');
  assert.equal(routes.parse('/app/unknown').page,'notfound');
  const api = context.window.__demoApi;
  await assert.rejects(api('/api/assessments/999999',{}));
  await assert.rejects(api('/api/scans/999999/findings',{}));
  const created = await api('/api/scan',{method:'POST',body:{target:'192.168.0.15',engagement_id:1}});
  const detail = await api('/api/assessments/'+created.scan_id,{});
  assert.equal(detail.assessment.findings_count,detail.findings.length);
  assert.equal(detail.source,'synthetic_demo');
  assert.equal(detail.assessment.target,'192.168.0.15');
  assert.ok(detail.findings.every(f => f.host === '192.168.0.15'));
  vm.runInContext(fs.readFileSync('static/cymag-demo.js','utf8'),context);
  context.window.CYMAG_DEMO.enable();
  const restored = await context.window.__demoApi('/api/assessments/'+created.scan_id,{});
  assert.equal(restored.findings.length,detail.findings.length);
  const originalNow = Date.now;
  try {
    const started = await context.window.__demoApi('/api/autonomous/run',{method:'POST',body:{target:'192.168.0.15',engagement_id:1}});
    const pending = await context.window.__demoApi('/api/assessments/'+started.scan_id,{});
    assert.equal(pending.assessment.status,'running');
    assert.equal(pending.findings.length,0);
    Date.now = () => originalNow()+600000;
    const completed = await context.window.__demoApi('/api/autonomous/'+started.run_id+'?since=0',{});
    assert.equal(completed.status,'done');
    const final = await context.window.__demoApi('/api/assessments/'+started.scan_id,{});
    assert.equal(final.assessment.findings_count,final.findings.length);
    assert.equal(final.assessment.status,'done');
  } finally { Date.now = originalNow; }
  const themeEvents = {};
  const select = { value:'', addEventListener:(name,fn) => themeEvents[name]=fn };
  let domReady;
  const media = { matches:true, addEventListener:() => {} };
  context.window.matchMedia = () => media;
  context.document = { documentElement:{dataset:{}}, getElementById:() => select, addEventListener:(name,fn) => domReady=fn };
  vm.runInContext(fs.readFileSync('static/astro-theme.js','utf8'),context);
  assert.equal(context.document.documentElement.dataset.theme,'dark');
  domReady(); select.value='light'; themeEvents.change();
  assert.equal(context.document.documentElement.dataset.theme,'light');
  assert.equal(storage.get('astro-theme'),'light');
  console.log('Frontend contracts: routes, demo persistence, unknown IDs, provenance, counts, zero fetches and themes passed.');
}
main().catch(e => { console.error(e); process.exitCode=1; });
