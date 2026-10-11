const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const experience = require('../static/astro-experience.js');
const source = fs.readFileSync('static/cymag.js','utf8');
const workspace = fs.readFileSync('static/astro-workspace.js','utf8');
const css = fs.readFileSync('static/astro-workspace.css','utf8');
const tick = () => new Promise(resolve => setImmediate(resolve));
function element() {
  const classes = new Set();
  return {value:'',hidden:true,disabled:false,innerHTML:'',textContent:'',children:[],attrs:{},handlers:{},dataset:{},
    classList:{add:c=>classes.add(c),remove:c=>classes.delete(c),toggle:(c,on)=>on?classes.add(c):classes.delete(c),contains:c=>classes.has(c)},
    addEventListener(name,fn){this.handlers[name]=fn;},setAttribute(k,v){this.attrs[k]=v;},
    append(...items){this.children.push(...items);},focus(){this.focused=true;}};
}
async function aiFlow() {
  const elements = new Map(); const calls=[]; let answer;
  const get = id => {if(!elements.has(id)) elements.set(id,element()); return elements.get(id);};
  const ctx = {$:get,esc:String,toast(){},fieldError(){},api:async(url,options)=>{
    calls.push([url,options]);
    if(url.endsWith('/status')) return {online:false,model:'model',provider:'Groq',known_models:['model'],source:'none'};
    if(url.endsWith('/test')) return new Promise(resolve=>answer=resolve);
    return {ok:true};
  }};
  vm.createContext(ctx); vm.runInContext(source.slice(source.indexOf('function iaStatusBadge'),source.indexOf('function renderConta')),ctx);
  ctx.renderIA(); await tick();
  // Browser parses the disabled attribute; handlers must independently guard it.
  get('#ia-key').value='secret'; get('#ia-model').value='model';
  get('#ia-apply').handlers.click(); await tick();
  assert.equal(calls.filter(([u])=>u.endsWith('/apply')).length,0);
  get('#ia-test').handlers.click();
  get('#ia-model').value='other'; get('#ia-model').handlers.input();
  answer({ok:true,model:'old'}); await tick();
  assert.equal(get('#ia-apply').disabled,true,'stale test must not enable apply');
  get('#ia-test').handlers.click(); answer({ok:false,error:'Modelo desconhecido'}); await tick();
  assert.equal(get('#ia-apply').disabled,true); assert.match(get('#ia-test-state').textContent,/Falhou: Modelo/);
  get('#ia-test').handlers.click(); answer({ok:true,model:'other'}); await tick();
  assert.equal(get('#ia-apply').disabled,false); assert.match(get('#ia-test-state').textContent,/Teste OK: resposta recebida/);
  assert.equal(get('#ia-apply').classList.contains('btn-primary'),true);
  assert.equal(get('#ia-test').classList.contains('btn-primary'),false);
  get('#ia-apply').handlers.click(); await tick();
  assert.equal(calls.filter(([u])=>u.endsWith('/apply')).length,1); assert.equal(get('#ia-key').value,'');
  assert.equal(get('#ia-apply').disabled,true);
  get('#ia-reset').handlers.click(); await tick();
  assert.equal(calls.filter(([u])=>u.endsWith('/reset')).length,0,'reset requires inline confirmation');
  get('#ia-reset-yes').handlers.click(); await tick();
  assert.equal(calls.filter(([u])=>u.endsWith('/reset')).length,1);
  assert.ok(!ctx.iaStatusBadge({online:true,key_mask:'secret',source:'runtime'}).includes('secret'));
}
function glossary() {
  const ctx={window:{},MutationObserver:class {observe(){}},document:{createElement:element,querySelector:()=>element(),addEventListener(){}}};
  vm.createContext(ctx);vm.runInContext(fs.readFileSync('static/astro-glossary.js','utf8'),ctx);
  assert.equal(Object.keys(ctx.window.ASTRO_GLOSSARY.definitions).length,7);
  const term=ctx.window.ASTRO_GLOSSARY.term('CVSS'); const [button,panel]=term.children;
  assert.equal(button.attrs['aria-describedby'],panel.id);
  button.handlers.click();assert.equal(panel.hidden,false);assert.equal(button.attrs['aria-expanded'],'true');
  term.handlers.keydown({key:'Escape',preventDefault(){}});assert.equal(panel.hidden,true);assert.equal(button.focused,true);
}
(async()=>{
  const admin=experience.overview({source:'persisted'}, {role:'admin',account:{name:'Conta'}},false,[]);
  assert.match(admin,/admin-home/);assert.ok(!admin.includes('operations-hero'));
  assert.ok(experience.profile('admin').groups.some(([title])=>title==='ADMINISTRAÇÃO'));
  assert.match(experience.client({account:{name:'<img>'}}),/&lt;img&gt;/);
  assert.match(experience.client({}),/Cliente não vinculado/);
  assert.equal(experience.environment({target:'192.0.2.1',engagement_name:'Escritório'}),'Escritório · 192.0.2.1');
  assert.equal(experience.environment({target:'192.0.2.1'}),'192.0.2.1 · sem nome cadastrado');
  assert.match(experience.humanDate('2026-10-11T18:03:00Z'),/UTC.*horário local/);
  assert.equal(experience.humanDate('invalid'),'Data não registrada');
  const report=experience.reports([{id:1,target:'192.0.2.1',status:'done',verification_counts:{confirmed:2,suspected:3,observation:4,unclassified:5}}],false);
  assert.match(report,/Gerado sob demanda/);assert.match(report,/<dt>Confirmados<\/dt><dd>2/);assert.ok(!report.includes('report-lines'));
  assert.match(css,/#main-content:focus:not\(:focus-visible\)/); assert.match(css,/\.findings-toolbar \{ display:grid; grid-template-columns:repeat\(2/);
  assert.match(workspace,/executive-report-summary/);assert.match(workspace,/settingsNav/);assert.match(workspace,/Método e limites/);
  await aiFlow();glossary();
  console.log('UX Wave 3: role separation, escaping, reports, dates, glossary keyboard and AI stale/failed/success/apply/reset states passed.');
})().catch(error=>{console.error(error);process.exitCode=1;});
