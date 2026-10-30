#!/usr/bin/env node
/**
 * Serve a hub: one page of buttons, one per configured link.
 *
 * WHICH hub is not known here and must not become known here. The title, the
 * port and every button arrive through app.config.json, so two hubs are this
 * same file reading two different configs (design 2.10). Nothing below may be
 * specialised to whichever hub was built first.
 *
 * The buttons are rendered HERE, on the server, from app.config.json - not by a
 * build step baking them into a static file, and not by script in the browser.
 * That is what lets the page carry no JavaScript at all: there is nothing for a
 * client to fetch and nothing for it to render, so a label out of config can
 * never reach the DOM as anything but escaped text.
 *
 * A link may also be MOUNTED (design 2.9): the hub requires that app's app.js,
 * calls its createApp() once at startup, and routes the link's path to the
 * handler it returns - so the app answers on this port without its own server
 * being up. The prefix is stripped before the app sees the request, and a mount
 * that cannot be prepared fails at its own prefix and nowhere else.
 *
 * A file:// link is rendered like any other button on purpose. A browser blocks
 * it from a page served over http and says nothing, but the hub cannot know how
 * the reader arrived, and the same link list may also be published as a page
 * opened straight off a share where that button works (design 2.7). The fact is
 * kept in /healthz instead, where it does not change the look.
 *
 * Node stdlib only - no npm install, no CDN, works offline.
 */

'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');

const PUBLIC_DIR = path.join(__dirname, 'public');
const APP_CONFIG = path.join(__dirname, 'app.config.json');

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith('--')) continue;
    const eq = a.indexOf('=');
    if (eq > -1) { out[a.slice(2, eq)] = a.slice(eq + 1); continue; }
    const next = argv[i + 1];
    if (next === undefined || next.startsWith('--')) { out[a.slice(2)] = true; }
    else { out[a.slice(2)] = next; i++; }
  }
  return out;
}

function resolveOptions() {
  const args = parseArgs(process.argv.slice(2));
  let app = {};
  try { app = JSON.parse(fs.readFileSync(APP_CONFIG, 'utf8')); }
  catch { /* an absent field falls to the default below - design 4.6 lists it as a defect */ }

  // explicit argument -> the app's own configuration -> built-in default
  const pick = (argKey, key, fallback) =>
    args[argKey] !== undefined ? args[argKey]
    : app[key] !== undefined && app[key] !== null ? app[key]
    : fallback;

  return {
    // The two defaults below are deliberately generic. A hub's real title and port live in its
    // app config; a default that named one would make this file know a hub (design 2.10).
    port: Number(pick('port', 'port', 8080)),
    host: String(args.host || '127.0.0.1'),
    title: String(pick('title', 'title', 'Home')),
    links: Array.isArray(app.links) ? app.links : [],
    assembledAt: app.assembledAt || null,
  };
}

/** Every string on this page comes from config, so it is escaped before it is markup.
 *  Both quote forms are escaped because a value is used in an attribute as well as in text. */
function esc(s) {
  return String(s === null || s === undefined ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function schemeOf(href) {
  const m = /^([a-z][a-z0-9+.-]*):/i.exec(String(href || ''));
  return m ? m[1].toLowerCase() : '';
}

// ----------------------------------------------------------------- mounts (design 2.8, 2.9) ---

// The hub's own routes. A mount prefix equal to one of these would shadow it, so it is refused.
const RESERVED_PREFIXES = new Set(['/index.html', '/app.css', '/healthz']);

/** A mounted entry's href is a path on this origin, and that path IS the prefix (design 2.6). */
function mountPrefix(href) {
  const raw = String(href || '').split('?')[0].split('#')[0];
  if (!raw.startsWith('/')) return null;
  return raw.replace(/\/+$/, '') || null;
}

async function prepareMounts(links) {
  const mounts = [];
  const taken = new Map();

  for (const l of links) {
    if (!l || !l.mount || !l.mount.appDir) continue;
    const spec = String(l.mount.appDir);
    const m = {
      prefix: mountPrefix(l.href),
      label: String(l.label || ''),
      appDir: path.isAbsolute(spec) ? spec : path.join(__dirname, spec),
      owner: l.mount.skill ? String(l.mount.skill) : null,
      handler: null,
      error: null,
    };
    try {
      if (!m.prefix) {
        throw new Error(`href ${JSON.stringify(l.href)} is not a path on this origin, `
                        + 'so there is no prefix to mount under');
      }
      if (RESERVED_PREFIXES.has(m.prefix) || m.prefix === '/') {
        throw new Error(`${m.prefix} is one of the hub's own routes and would shadow it`);
      }
      if (taken.has(m.prefix)) {
        throw new Error(`${m.prefix} is already mounted by ${taken.get(m.prefix)}`);
      }
      const entry = path.join(m.appDir, 'app.js');
      if (!fs.existsSync(entry)) {
        throw new Error(`no app.js in ${m.appDir} - that app is not mountable yet (design 2.9)`);
      }
      const mod = require(entry);
      if (typeof mod.createApp !== 'function') {
        throw new Error(`${entry} exports no createApp(options) - see design 2.9`);
      }
      const handler = await mod.createApp({ mountedAt: m.prefix });
      if (typeof handler !== 'function') {
        throw new Error('createApp did not return a (req, res) handler');
      }
      m.handler = handler;
      taken.set(m.prefix, m.label || m.appDir);
    } catch (err) {
      // Design 2.9: preparing one mount cannot stop the hub or any other mount.
      m.error = String(err && err.message ? err.message : err);
    }
    mounts.push(m);
  }
  return mounts;
}

/** Longest prefix first, so /a/b is not swallowed by /a. */
function matchMount(mounts, rawPath) {
  for (const m of mounts) {
    if (m.prefix && (rawPath === m.prefix || rawPath.startsWith(`${m.prefix}/`))) return m;
  }
  return null;
}

function renderMountFailure(opt, m) {
  const owner = m.owner
    ? `<p>It is assembled by <code>${esc(m.owner)}</code>.</p>`
    : '';
  // Styled inline rather than from /app.css: this page answers at ANY depth under the prefix, so
  // no one relative path to the stylesheet is correct and an absolute one assumes the hub owns
  // the origin - the very thing a mounted app must not assume.
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(m.label)} - not mounted</title>
<style>
  body { margin: 0; padding: 3rem 1.5rem; font: 15px/1.6 system-ui, sans-serif;
         background: #1e1e1e; color: #d4d4d4; }
  main { max-width: 44rem; margin: 0 auto; }
  h1 { font-size: 1.25rem; margin: 0 0 1rem; }
  p { margin: 0 0 .75rem; }
  .empty { color: #ce9178; }
  code { color: #9cdcfe; word-break: break-all; }
  a { display: inline-block; margin-top: 1.5rem; padding: .5rem 1rem; background: #0e639c;
      color: #fff; text-decoration: none; border-radius: 3px; }
</style>
</head>
<body>
<main>
  <h1>${esc(m.label)} is not mounted</h1>
  <p class="empty">${esc(m.error)}</p>
  <p>Looked in <code>${esc(m.appDir)}</code> for <code>app.js</code>.</p>
  ${owner}
  <a href="/">Back to ${esc(opt.title)}</a>
</main>
</body>
</html>
`;
}

function mountFailed(res, m, err) {
  const msg = String(err && err.message ? err.message : err);
  console.error(`mount ${m.prefix} failed while answering: ${msg}`);
  if (res.headersSent) { res.destroy(); return; }
  send(res, 502, 'text/plain; charset=utf-8',
       `${m.label} failed while answering this request.\n\n${msg}\n\n`
       + 'The hub and its other mounts are unaffected.\n');
}

/** Strip the prefix, then delegate. The app never sees a path it was not written to answer. */
function delegate(opt, m, req, res) {
  const cut = req.url.indexOf('?');
  const rawPath = cut === -1 ? req.url : req.url.slice(0, cut);
  const query = cut === -1 ? '' : req.url.slice(cut);

  if (!m.handler) {
    return send(res, 503, 'text/html; charset=utf-8', renderMountFailure(opt, m));
  }
  if (rawPath === m.prefix) {
    // Design 2.8: without the trailing slash the app's relative URLs resolve above the mount.
    res.writeHead(308, { location: `${m.prefix}/${query}` });
    return res.end();
  }

  req.url = rawPath.slice(m.prefix.length) + query;
  try {
    const out = m.handler(req, res);
    if (out && typeof out.catch === 'function') out.catch((err) => mountFailed(res, m, err));
  } catch (err) {
    mountFailed(res, m, err);
  }
}

function renderButtons(links) {
  if (!links.length) {
    return '    <p class="empty">No links configured. Add entries to this hub\'s link list '
           + 'and assemble it again.</p>';
  }
  // Design 2.7: label, the URL verbatim, and the note when there is one. Every entry renders
  // identically - a link this page cannot navigate to included (design 2.7), and a mount too.
  return links.map((l) => {
    const note = l.note ? `\n      <span class="note">${esc(l.note)}</span>` : '';
    return `    <a href="${esc(l.href)}">
      <span class="label">${esc(l.label)}</span>
      <span class="url">${esc(l.href)}</span>${note}
    </a>`;
  }).join('\n');
}

function renderPage(opt) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(opt.title)}</title>
<link rel="stylesheet" href="./app.css">
</head>
<body>
<main>
  <h1>${esc(opt.title)}</h1>
  <p>Pick an app.</p>
  <div class="buttons">
${renderButtons(opt.links)}
  </div>
</main>
</body>
</html>
`;
}

function send(res, code, type, body) {
  res.writeHead(code, {
    'content-type': type,
    'content-length': Buffer.byteLength(body),
    'cache-control': 'no-store',
  });
  res.end(body);
}

async function main() {
  const opt = resolveOptions();

  // Prepared once, at startup, so a mounted app's own setup failure is a startup fact rather
  // than a surprise for whoever happens to arrive first (design 2.9).
  const mounts = await prepareMounts(opt.links);
  const byPrefix = mounts.slice()
    .sort((a, b) => (b.prefix || '').length - (a.prefix || '').length);

  const server = http.createServer((req, res) => {
    const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);

    // A mount owns everything under its prefix, so it is matched before the hub's own routes.
    const mount = matchMount(byPrefix, url.pathname);
    if (mount) return delegate(opt, mount, req, res);

    if (url.pathname === '/' || url.pathname === '/index.html') {
      return send(res, 200, 'text/html; charset=utf-8', renderPage(opt));
    }
    if (url.pathname === '/app.css') {
      // The one static asset. Resolved by a fixed name, never from the request path,
      // so nothing a caller sends can reach the filesystem.
      try {
        return send(res, 200, 'text/css; charset=utf-8',
                    fs.readFileSync(path.join(PUBLIC_DIR, 'app.css'), 'utf8'));
      } catch {
        return send(res, 500, 'text/plain; charset=utf-8', 'app.css is missing from public/\n');
      }
    }
    if (url.pathname === '/healthz') {
      return send(res, 200, 'application/json; charset=utf-8', JSON.stringify({
        ok: true, title: opt.title, links: opt.links.length,
        dead: opt.links.filter((l) => schemeOf(l.href) === 'file').length,
        mounts: mounts.map((m) => ({ prefix: m.prefix, label: m.label,
                                     ok: Boolean(m.handler), error: m.error })),
        assembledAt: opt.assembledAt,
      }));
    }
    send(res, 404, 'text/plain; charset=utf-8', 'not found\n');
  });

  server.on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
      console.error(`port ${opt.port} is already in use - another server is running there.`);
      process.exit(3);
    }
    throw err;
  });

  server.listen(opt.port, opt.host, () => {
    // Design 2.10: a failure the hub was never handed must not be fatal either. A mounted app that
    // throws on a later tick, or starts a promise and forgets to return it, gives delegate()
    // nothing to catch - the request it belonged to has already been answered. The runtime would
    // end the process, letting one app's loose end take down every other mount.
    //
    // Recorded and survived, never attributed: there is no request left to blame, and guessing
    // would be worse than saying so. The cost - continuing in a state the hub cannot vouch for -
    // is accepted because the hub holds no data of its own (design 2.10).
    //
    // Installed HERE, not before listen: until the hub is actually serving there is nothing to
    // keep alive, and a startup failure must stay loud (design 4.1).
    const survive = (kind) => (err) => {
      console.error(`[${new Date().toISOString()}] ${kind} - the hub is still answering. It is not `
                    + 'attributed to a mount: the request that caused it is already gone.');
      console.error(err && err.stack ? err.stack : String(err));
    };
    process.on('uncaughtException', survive('uncaught exception'));
    process.on('unhandledRejection', survive('unhandled rejection'));

    const dead = opt.links.filter((l) => schemeOf(l.href) === 'file').length;
    console.log(`${opt.title}`);
    console.log(`  links       ${opt.links.length}`
                + (dead ? `  (${dead} cannot navigate from an http page)` : ''));
    for (const l of opt.links) console.log(`    ${l.label}  ->  ${l.href}`);
    if (mounts.length) {
      const up = mounts.filter((m) => m.handler).length;
      console.log(`  mounts      ${up}/${mounts.length} served by this hub`);
      for (const m of mounts) {
        console.log(m.handler ? `    ${m.prefix}/  <-  ${m.appDir}`
                              : `    ${m.prefix || '(no prefix)'}  NOT MOUNTED  ${m.error}`);
      }
    }
    console.log(`  serving     http://${opt.host}:${opt.port}/`);
    console.log(opt.host === '127.0.0.1'
      ? '  bound to loopback - this machine only'
      : `  bound to ${opt.host} - reachable from other machines`);
    console.log('  Ctrl+C to stop');
  });
}

main().catch((err) => { console.error(err); process.exit(1); });
