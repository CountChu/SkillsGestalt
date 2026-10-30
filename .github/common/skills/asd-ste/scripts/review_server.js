#!/usr/bin/env node
/**
 * Serve the review pages of the asd-ste skill, and keep each page's review statuses.
 *
 * Step 6 builds a review page, step_6-review.html, in a Checkpoint Dir under checkpoints/asd-ste/.
 * This server serves every one of them - /<dir>/ is the page of <root>/<dir>/ - with an index at /
 * that lists each page and how far its review is. A reviewer marks each item of the review notes
 * [ ] pending, [v] approved, [?] to be explained or [x] rejected; a page served from here sends the marks with
 * PUT /<dir>/status, and this server writes them to step_6-status.json in that Checkpoint Dir, the
 * one writer of that file. A key the page does not hold is refused, so a page built again after
 * an item changed cannot bring back the old item's mark. A page opened as a file cannot save, and
 * says so.
 *
 * Loopback only (127.0.0.1), port 8790 unless --port says otherwise. Node stdlib only - no npm
 * install, no CDN, works offline. It runs until it is stopped: kill <pid> on macOS and Linux,
 * Stop-Process -Id <pid> in PowerShell; /healthz gives the pid.
 *
 * Usage:
 *   node review_server.js [--root checkpoints/asd-ste] [--port 8790] [--host 127.0.0.1]
 *   node review_server.js --probe [--port 8790] [--host 127.0.0.1]
 *
 * --probe asks whether a review server answers at host:port, and exits 0 when one does, 1 when
 * nothing answers there, and 2 when something else does. Serving exits 1 when the port is taken.
 */

'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');

const SERVICE = 'asd-ste-review';
const PAGE = 'step_6-review.html';
const STATUS = 'step_6-status.json';
const DIR_RE = /^[A-Za-z0-9._-]+$/;
const KEY_RE = /^[0-9a-f]{12}$/;
const STATES = new Set(['v', 'x', '?']);
const KEY_IN_PAGE = /class="st" data-key="([0-9a-f]{12})"/g;
const MAX_BODY = 1024 * 1024;

function parseArgs(argv) {
  const opt = { root: 'checkpoints/asd-ste', port: 8790, host: '127.0.0.1', probe: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--probe') opt.probe = true;
    else if (a === '--root' || a === '--port' || a === '--host') {
      const v = argv[++i];
      if (v === undefined) throw new Error(`${a} needs a value`);
      opt[a.slice(2)] = a === '--port' ? Number(v) : v;
    } else throw new Error(`unknown argument: ${a}`);
  }
  if (!Number.isInteger(opt.port) || opt.port < 0 || opt.port > 65535) throw new Error(`not a port: ${opt.port}`);
  opt.root = path.resolve(opt.root);
  return opt;
}

function now() {
  const d = new Date(), p = n => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}`;
}

function escape(s) {
  return String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
}

function pageKeys(dir) {
  const text = fs.readFileSync(path.join(dir, PAGE), 'utf8');
  return new Set(Array.from(text.matchAll(KEY_IN_PAGE), m => m[1]));
}

function readStatus(dir) {
  try {
    const j = JSON.parse(fs.readFileSync(path.join(dir, STATUS), 'utf8'));
    if (j && typeof j.items === 'object' && j.items) return j;
  } catch (e) { /* no status yet, or one that cannot be read: the page starts from pending */ }
  return { items: {} };
}

function counts(keys, items) {
  let v = 0, x = 0, q = 0;
  for (const k of keys) {
    const s = items[k] && items[k].s;
    if (s === 'v') v++;
    else if (s === 'x') x++;
    else if (s === '?') q++;
  }
  return { total: keys.size, v, x, q, open: keys.size - v - x - q };
}

function reviewDirs(root) {
  let names = [];
  try { names = fs.readdirSync(root); } catch (e) { return []; }
  return names.filter(n => DIR_RE.test(n) && fs.existsSync(path.join(root, n, PAGE))).sort();
}

const STYLE = `:root{--bg:#fbfbfa;--fg:#1f2328;--mut:#6b7280;--line:#e5e7eb;--card:#fff;--acc:#2563eb;--ok:#15803d;--no:#b91c1c;--q:#b45309}
@media (prefers-color-scheme: dark){:root{--bg:#16181d;--fg:#e6e8eb;--mut:#9aa1ab;--line:#2b2f36;--card:#1d2026;--acc:#6ea8ff;--ok:#4ade80;--no:#f87171;--q:#f0b35a}}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 -apple-system,"PingFang TC","Noto Sans TC",system-ui,sans-serif;padding:20px 24px}
h1{font-size:22px;margin:0 0 4px} .mut{color:var(--mut);font-size:13px} a{color:var(--acc)}
table{border-collapse:collapse;margin-top:14px;background:var(--card);border:1px solid var(--line)}
th,td{border-top:1px solid var(--line);padding:6px 12px;text-align:left} th{font-size:12px;color:var(--mut)}
.ok{color:var(--ok)} .no{color:var(--no)} .q{color:var(--q)} code{font:13px ui-monospace,Menlo,monospace}`;

function indexPage(opt) {
  const rows = reviewDirs(opt.root).map(name => {
    const dir = path.join(opt.root, name);
    let c = { total: 0, v: 0, x: 0, q: 0, open: 0 }, updated = '';
    try {
      const st = readStatus(dir);
      c = counts(pageKeys(dir), st.items);
      updated = st.updated || '';
    } catch (e) { /* a page that cannot be read shows no counts */ }
    const link = `<td><a href="/${encodeURIComponent(name)}/">${escape(name)}</a></td>`;
    if (!c.total) return `<tr>${link}<td colspan="6" class="mut">沒有審核狀態：頁面是加上狀態之前建的，以 run step 6 重建</td></tr>`;
    return `<tr>${link}<td>${c.total}</td>`
      + `<td class="ok">${c.v}</td><td class="q">${c.q}</td><td class="no">${c.x}</td><td>${c.open}</td><td class="mut">${escape(updated)}</td></tr>`;
  });
  return `<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>asd-ste 審核</title><style>${STYLE}</style></head><body>
<h1>asd-ste 審核</h1><div class="mut">審核伺服器服務 <code>${escape(opt.root)}</code> 底下每一份對照頁；審核狀態存在各自 Checkpoint Dir 的 <code>${STATUS}</code>。
PID ${process.pid}：要關掉它，macOS／Linux 執行 <code>kill ${process.pid}</code>，PowerShell 執行 <code>Stop-Process -Id ${process.pid}</code>。</div>
<table><tr><th>草稿</th><th>項目</th><th>通過</th><th>待解釋</th><th>不通過</th><th>待審</th><th>最後更新</th></tr>${rows.join('') || '<tr><td colspan="7" class="mut">還沒有任何對照頁</td></tr>'}</table>
</body></html>\n`;
}

function send(res, code, type, body, extra = {}) {
  res.writeHead(code, { 'Content-Type': type, 'Cache-Control': 'no-store', ...extra });
  res.end(body);
}

function json(res, code, value) {
  send(res, code, 'application/json; charset=utf-8', JSON.stringify(value));
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let size = 0;
    req.on('data', c => {
      size += c.length;
      if (size > MAX_BODY) { reject(new Error('body over 1 MiB')); req.destroy(); return; }
      chunks.push(c);
    });
    req.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    req.on('error', reject);
  });
}

async function saveStatus(req, res, dir) {
  let body;
  try { body = JSON.parse(await readBody(req)); } catch (e) { return json(res, 400, { error: `not JSON: ${e.message}` }); }
  const items = body && body.items;
  if (!items || typeof items !== 'object' || Array.isArray(items)) return json(res, 400, { error: 'the body holds no items object' });
  let keys;
  try { keys = pageKeys(dir); } catch (e) { return json(res, 404, { error: 'the review page cannot be read' }); }
  const out = {};
  for (const [k, v] of Object.entries(items)) {
    if (!KEY_RE.test(k) || !keys.has(k)) return json(res, 400, { error: `no item ${k} on this review page` });
    const s = v && v.s;
    if (!STATES.has(s)) return json(res, 400, { error: `not a review status: ${JSON.stringify(s)}` });
    out[k] = { s, text: String((v && v.text) || '').slice(0, 120) };
  }
  const record = { version: 1, updated: now(), items: out };
  const file = path.join(dir, STATUS), tmp = `${file}.tmp-${process.pid}`;
  try {
    fs.writeFileSync(tmp, JSON.stringify(record, null, 1) + '\n', 'utf8');
    fs.renameSync(tmp, file);
  } catch (e) {
    return json(res, 500, { error: `${STATUS} cannot be written: ${e.message}` });
  }
  const c = counts(keys, out);
  return json(res, 200, { saved: Object.keys(out).length, updated: record.updated, ...c });
}

function handler(opt) {
  return (req, res) => {
    const url = new URL(req.url, 'http://localhost');
    let parts;
    try { parts = url.pathname.split('/').filter(Boolean).map(decodeURIComponent); }
    catch (e) { return send(res, 400, 'text/plain; charset=utf-8', 'bad path\n'); }
    if (url.pathname === '/') return send(res, 200, 'text/html; charset=utf-8', indexPage(opt));
    if (url.pathname === '/healthz') return json(res, 200, { service: SERVICE, root: opt.root, pid: process.pid });
    const name = parts[0];
    if (!name || !DIR_RE.test(name) || parts.length > 2) return send(res, 404, 'text/plain; charset=utf-8', 'not found\n');
    const dir = path.join(opt.root, name);
    if (!fs.existsSync(path.join(dir, PAGE))) return send(res, 404, 'text/plain; charset=utf-8', `no review page in ${name}\n`);
    if (parts.length === 1) {
      if (!url.pathname.endsWith('/')) return send(res, 301, 'text/plain; charset=utf-8', '', { Location: `/${encodeURIComponent(name)}/` });
      if (req.method !== 'GET' && req.method !== 'HEAD') return send(res, 405, 'text/plain; charset=utf-8', 'GET only\n');
      return send(res, 200, 'text/html; charset=utf-8', fs.readFileSync(path.join(dir, PAGE)));
    }
    if (parts[1] !== 'status') return send(res, 404, 'text/plain; charset=utf-8', 'not found\n');
    if (req.method === 'GET') return json(res, 200, readStatus(dir));
    if (req.method === 'PUT') return saveStatus(req, res, dir);
    return send(res, 405, 'text/plain; charset=utf-8', 'GET or PUT only\n');
  };
}

function probe(opt) {
  const req = http.get({ host: opt.host, port: opt.port, path: '/healthz', timeout: 1500 }, res => {
    let body = '';
    res.on('data', c => { body += c; });
    res.on('end', () => {
      let j = null;
      try { j = JSON.parse(body); } catch (e) { /* not ours */ }
      if (j && j.service === SERVICE) {
        console.log(`a review server answers at http://${opt.host}:${opt.port}/ - root ${j.root}, pid ${j.pid}`);
        process.exit(0);
      }
      console.log(`something else answers at http://${opt.host}:${opt.port}/ - not a review server`);
      process.exit(2);
    });
  });
  req.on('timeout', () => { req.destroy(); console.log(`nothing answers at http://${opt.host}:${opt.port}/`); process.exit(1); });
  req.on('error', () => { console.log(`nothing answers at http://${opt.host}:${opt.port}/`); process.exit(1); });
}

function main() {
  let opt;
  try { opt = parseArgs(process.argv.slice(2)); } catch (e) { console.error(`error: ${e.message}`); process.exit(2); }
  if (opt.probe) return probe(opt);
  const server = http.createServer(handler(opt));
  server.on('error', e => {
    if (e.code === 'EADDRINUSE') console.error(`port ${opt.port} is already in use - another program, or another review server, is running there.`);
    else console.error(`error: ${e.message}`);
    process.exit(1);
  });
  server.listen(opt.port, opt.host, () => {
    console.log(`asd-ste review server, pid ${process.pid}`);
    console.log(`  root        ${opt.root}`);
    console.log(`  serving     http://${opt.host}:${server.address().port}/`);
  });
}

main();
