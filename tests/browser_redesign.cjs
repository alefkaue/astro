if (process.env.ASTRO_SKIP_BROWSER === '1') { console.log('SKIP browser_redesign: offline requested; no browser or server used.'); process.exit(0); }
// Real Edge smoke test through local CDP. Start Edge on debug port 9222 first.
const fs = require('node:fs');
const assert = require('node:assert/strict');
async function main() {
  const pages = await (await fetch('http://127.0.0.1:9222/json/list')).json();
  const socket = new WebSocket(pages.find(p => p.type === 'page').webSocketDebuggerUrl);
  await new Promise(resolve => socket.addEventListener('open',resolve,{once:true}));
  let next = 0; const pending = new Map(); const errors = [];
  socket.addEventListener('message',event => {
    const message = JSON.parse(event.data);
    if (message.method === 'Runtime.exceptionThrown') errors.push(message.params.exceptionDetails);
    if (message.id) { const request = pending.get(message.id); pending.delete(message.id); message.error ? request.reject(message.error) : request.resolve(message.result); }
  });
  const send = (method,params={}) => new Promise((resolve,reject) => {const id=++next; pending.set(id,{resolve,reject}); socket.send(JSON.stringify({id,method,params}));});
  const evaluate = async expression => {
    const response = await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});
    if (response.exceptionDetails) throw new Error(JSON.stringify(response.exceptionDetails));
    return response.result.value;
  };
  const wait = async expression => { for(let i=0;i<100;i++) { if(await evaluate(expression)) return; await new Promise(r=>setTimeout(r,100)); } throw new Error('Timeout: '+expression); };
  const go = async path => { await evaluate(`ASTRO_ROUTER.navigate(${JSON.stringify(path)})`); };
  try {
    await send('Page.enable'); await send('Runtime.enable');
    await send('Page.navigate',{url:'http://127.0.0.1:5000/demo'});
    await wait(`document.querySelector('#sec-workspace .operations-hero') && document.querySelector('#page-title').textContent === 'Centro de operações'`);
    await go('/app/assessments'); await wait(`document.querySelector('#sec-workspace tbody a')`);
    assert.equal(await evaluate(`document.querySelectorAll('#nav a').length`),7);
    await go('/app/assessments/1001?tab=findings');
    await wait(`document.querySelector('#sec-workspace').textContent.includes('Redis')`);
    await send('Page.reload'); await wait(`document.querySelector('#sec-workspace').textContent.includes('Redis')`);
    await go('/app/assessments/999999'); await wait(`document.querySelector('#sec-workspace [role=alert]')`);
    await go('/app/assessments/new'); await wait(`document.querySelector('#wizard-next')`);
    for(let step=0;step<3;step++) await evaluate(`document.querySelector('#wizard-next').click()`);
    await evaluate(`document.querySelector('#assessment-confirm').checked=true;document.querySelector('#wizard-next').click()`);
    await wait(`location.pathname.match(/assessments\/\d+$/) && document.querySelector('.assessment-layout')`);
    const createdPath = await evaluate('location.pathname');
    await send('Page.reload'); await wait(`document.querySelector('.assessment-layout')`);
    assert.equal(await evaluate('location.pathname'),createdPath);
    fs.mkdirSync('docs/screenshots',{recursive:true});
    for(const width of [320,375,768,1024,1440]) {
      await send('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:false});
      await evaluate(`document.documentElement.dataset.theme='light'`);
      await new Promise(r=>setTimeout(r,150));
      const overflow = await evaluate('document.documentElement.scrollWidth > innerWidth');
      assert.equal(overflow,false,'Horizontal overflow at '+width);
      if(width===375 || width===1440) {
        const screenshot = await send('Page.captureScreenshot',{format:'png'});
        fs.writeFileSync('docs/screenshots/redesign-'+width+'.png',Buffer.from(screenshot.data,'base64'));
      }
    }
    await evaluate(`document.documentElement.dataset.theme='dark'`);
    const dark = await send('Page.captureScreenshot',{format:'png'});
    fs.writeFileSync('docs/screenshots/redesign-dark.png',Buffer.from(dark.data,'base64'));
    assert.equal(errors.length,0,JSON.stringify(errors));
    console.log('Edge: unified navigation, detail reload, missing ID, four-step demo assessment, persistent demo detail, light/dark screenshots, 320–1440px overflow checks passed; no JS exceptions.');
  } finally {socket.close();}
}
main().catch(error => {console.error(error);process.exitCode=1;});
