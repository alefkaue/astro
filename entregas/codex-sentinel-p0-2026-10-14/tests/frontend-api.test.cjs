const fs = require('node:fs');
const vm = require('node:vm');
const test = require('node:test');
const assert = require('node:assert/strict');

function client() {
  const source = fs.readFileSync('static/cymag.js', 'utf8');
  const start = source.indexOf('async function api(');
  const end = source.indexOf('/* ─── UI helpers', start);
  const calls = [];
  const state = { user: null };
  const context = vm.createContext({
    state, isDemo: () => false,
    fetch: async (url, options = {}) => {
      calls.push({ url, options });
      const data = url === '/api/csrf' ? { csrf_token: 'before-login' }
        : url === '/api/login' ? { csrf_token: 'after-login' } : { ok: true };
      return { status: 200, ok: true, headers: { get: () => 'application/json' }, json: async () => data };
    },
  });
  vm.runInContext(source.slice(start, end), context);
  return { api: context.api, calls, state };
}

test('login obtains CSRF and rotates token used for later mutations', async () => {
  const c = client();
  await c.api('/api/login', { method: 'POST', body: { email: 'a@example.test', password: 'fixture' } });
  assert.equal(c.calls[0].url, '/api/csrf');
  assert.equal(c.calls[1].options.headers['X-CSRF-Token'], 'before-login');
  await c.api('/api/engagements', { method: 'POST', body: { name: 'Local fixture', scope: ['192.0.2.1'] } });
  assert.equal(c.calls[2].options.headers['X-CSRF-Token'], 'after-login');
});

test('bodyless mutation sends valid JSON and CSRF', async () => {
  const c = client();
  await c.api('/api/logout', { method: 'POST' });
  assert.equal(c.calls[1].options.body, '{}');
  assert.equal(c.calls[1].options.headers['Content-Type'], 'application/json');
  assert.equal(c.calls[1].options.headers['X-CSRF-Token'], 'before-login');
});

test('read-only request does not create an extra CSRF request', async () => {
  const c = client();
  await c.api('/api/engagements');
  assert.equal(c.calls.length, 1);
  assert.equal(c.calls[0].options.method, 'GET');
});
