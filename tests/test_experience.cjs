const assert=require('node:assert/strict');
const vm=require('node:vm');
const fs=require('node:fs');
const experience=require('../static/astro-experience.js');
async function main() {
  const ctx={window:{},localStorage:{getItem:()=>null,setItem(){},removeItem(){}},URLSearchParams,Date,
    setTimeout:fn=>{fn();return 1;},fetch:()=>{throw Error('No network in demo');}};
  vm.createContext(ctx); vm.runInContext(fs.readFileSync('static/cymag-demo.js','utf8'),ctx);
  ctx.window.CYMAG_DEMO.enable();
  const summary=await ctx.window.__demoApi('/api/dashboard',{});
  const scopes=(await ctx.window.__demoApi('/api/engagements',{})).engagements;
  const owner=experience.overview(summary,ctx.window.CYMAG_DEMO.identity(),true,scopes);
  assert.match(owner,/executive-hero/);
  assert.match(owner,/DADOS SINTÉTICOS/);
  assert.match(owner,/Zero não significa risco zero/);
  assert.ok(!owner.includes('/app/assessments/new'));
  ctx.window.CYMAG_DEMO.setRole('operator');
  const operator=experience.overview(summary,ctx.window.CYMAG_DEMO.identity(),true,null);
  assert.match(operator,/operations-hero/);
  assert.match(operator,/Indisponível/); // Failed scopes fetch must not claim zero.
  assert.match(operator,/\/app\/assessments\/new/);
  for(const role of ['owner','viewer']) {
    assert.ok(!experience.profile(role).groups.flatMap(g=>g[1]).some(item=>item[0]==='assessments/new'));
  }
  assert.ok(experience.profile('operator').groups.flatMap(g=>g[1]).some(item=>item[0]==='assessments/new'));
  const scans=(await ctx.window.__demoApi('/api/scans',{})).scans;
  const reports=experience.reports([...scans,{id:777,target:'running-only',status:'running'}],true);
  assert.ok(!reports.includes('running-only'));
  assert.match(reports,/Não|não representa relatórios versionados/);
  const attack='<img src=x onerror=alert(1)>';
  const injected=experience.reports([{id:1,status:'done',target:attack,findings_count:0}],false,attack);
  assert.ok(!injected.includes(attack));
  assert.match(injected,/&lt;img/);
  const hostile=experience.overview(summary,{role:'owner',account:{name:attack}},false,[]);
  assert.ok(!hostile.includes(attack));
  const empty=experience.overview({...summary,counts:{assessments:0,completed:0,confirmed:0,running:0,failed:0,pending_validation:0,observations:0,unclassified:0,observed_hosts:0},recent:[],severity:{}},{role:'viewer',account:{name:'Empty'}},false,[]);
  assert.match(empty,/Nenhuma avaliação registrada/);
  assert.ok(!empty.includes('NaN'));
  console.log('Experience: role-specific navigation/actions, truthful scope errors, report eligibility, empty states and XSS escaping passed.');
}
main().catch(error=>{console.error(error);process.exitCode=1;});
