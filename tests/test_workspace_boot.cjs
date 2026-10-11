// Executes the actual workspace boot in a VM: a saved demo marker must not
// override a real authenticated session. UI rendering is stubbed, no browser.
const vm = require('node:vm');
const fs = require('node:fs');
const assert = require('node:assert/strict');
async function scenario(path,authenticated,captureRole=false,offline=false) {
  const calls=[];
  const element={addEventListener(){},removeEventListener(){}};
  const ctx={window:{ASTRO_ROUTES:{},addEventListener(){}},document:{addEventListener(){}},
    $:()=>element,$$:()=>[],state:{user:null},showSection(){},enterDemo(){},enterApp(){},
    openModal(){},closeModal(){},openSidebar(){},closeSidebar(){},showLogin:()=>calls.push('login'),
    sessionStorage:{getItem:()=> 'operator'},location:{pathname:path.split('?')[0],search:path.includes('?')?'?'+path.split('?')[1]:''},
    URLSearchParams,api:async()=>{if(offline) throw Error('offline'); return {authenticated,name:'Real user'};},clearTimeout,clearInterval};
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync('static/astro-workspace.js','utf8'),ctx);
  ctx.enterDemo=role=>calls.push(captureRole ? role : 'demo'); ctx.enterApp=()=>calls.push('real');
  await ctx.window.ASTRO_ROUTER.boot();
  return calls;
}
(async()=>{
  assert.deepEqual(await scenario('/app/overview',true),['real']);
  assert.deepEqual(await scenario('/app/assessments/1001?demo=1',true),['real']);
  assert.deepEqual(await scenario('/app/overview',false),['demo']);
  assert.deepEqual(await scenario('/app/assessments/1001?tab=findings',false,true,true),['operator']);
  assert.deepEqual(await scenario('/login',false,false,true),['login']);
  assert.deepEqual(await scenario('/demo',true),['demo']);
  assert.deepEqual(await scenario('/demo?role=owner',true,true),['owner']);
  assert.deepEqual(await scenario('/demo?role=invalid',false,true),['operator']);
  assert.deepEqual(await scenario('/login',false),['login']);
  console.log('Workspace boot: real sessions take precedence, explicit demo entry and login fallback passed.');
})().catch(error=>{console.error(error);process.exitCode=1;});
