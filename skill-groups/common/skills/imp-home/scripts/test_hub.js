#!/usr/bin/env node
/**
 * Observe a hub against its design, Home-RSDC: the checks that its 4.5 Verification Obligations
 * name, made on a running hub rather than read in its code.
 *
 * The hub is the seed's own server/ unless a hub directory is given. Only its server.js and its
 * public/ are copied, into a work directory beside the small apps the checks mount; the
 * configuration is the script's own, so the hub's real app.config.json is never read or written.
 *
 * With --run {yymmdd}.{N}, given by the step of an imp-home run, the work directory is test-hub/
 * in the Working Dir of that run, the Checkpoint Dir checkpoints/imp-home/{yymmdd}.{N}/test-hub/
 * at the workspace root. A test-hub/ that an earlier call of the same run left there is replaced;
 * the script does not remove the Working Dir, and the work directory stays when the script ends.
 * Without --run, as when it is run by hand after a change to the seed, the work directory is a new
 * temp/test-hub-* at the workspace root, removed by its full name when the script ends, failed or
 * not. The workspace root is the root of the workspace the skill runs in: the directory --workspace
 * names, or else the nearest directory, from the current directory up, whose config.yaml has
 * skillGroups. It is never found from this file: a workspace can read this skill group in place from
 * a different workspace, and the config.yaml above this file is then that other workspace's.
 *
 * Run it after a change to the seed's server.js, or to a hub's:
 *
 *   node test_hub.js [--run {yymmdd}.{N}] [--workspace DIR] [hub directory]
 *
 * Every check prints one line, [PASS] or [FAIL], each failure followed by what was seen.
 * It needs Node 16 or later, and nothing installed.
 *
 * Exit status: 0 every check passed; 1 a check failed; 2 the hub directory has no server.js, the
 * arguments are wrong, or no workspace root is found.
 */

'use strict';

const { spawn } = require('child_process');
const fs = require('fs');
const http = require('http');
const net = require('net');
const path = require('path');

const SEED = path.join(__dirname, '..', 'server');
const WAIT_MS = 3000;

// The workspace configuration: a config.yaml with a top-level skillGroups mapping, which names the
// skill groups the workspace reads. Node has no YAML parser, so the one key is read as text: a line
// `skillGroups:` with nothing after it but a comment, and then an indented key; or a flow mapping on
// the line itself. The skill config, also named config.yaml, has no such key, so it is passed over.
function isWorkspaceConfig(dir) {
  let lines;
  try { lines = fs.readFileSync(path.join(dir, 'config.yaml'), 'utf8').split(/\r?\n/); } catch (e) { return false; }
  for (let i = 0; i < lines.length; i++) {
    const m = /^skillGroups:(.*)$/.exec(lines[i]);
    if (!m) continue;
    const rest = m[1].replace(/(^|\s)#.*$/, '').trim();
    if (rest) return rest.startsWith('{');
    for (let j = i + 1; j < lines.length; j++) {
      if (/^\s*(#.*)?$/.test(lines[j])) continue;
      return /^\s+[^\s#-][^:]*:(\s|$)/.test(lines[j]);
    }
    return false;
  }
  return false;
}

// The workspace root: --workspace, or else the nearest directory, from the current directory up,
// whose config.yaml has skillGroups - never found from this file. The checks need no isolation from
// the workspace (the hub copy reads only the configuration this script writes, and the mounted apps
// require nothing), so the work directory goes into the Working Dir of the run, or outside a run into
// temp/, as run-data-rules.md tells, not into the temporary directory of the system.
function workspaceRoot(explicit) {
  if (explicit) {
    let root;
    try { root = fs.realpathSync(path.resolve(explicit)); } catch (e) { throw new Error(`--workspace ${explicit}: no such directory`); }
    if (!isWorkspaceConfig(root)) throw new Error(`--workspace ${explicit}: ${root} holds no config.yaml with skillGroups - name the root of the workspace the skill runs in`);
    return root;
  }
  const here = fs.realpathSync(process.cwd());
  for (let dir = here; ; dir = path.dirname(dir)) {
    if (isWorkspaceConfig(dir)) return dir;
    if (path.dirname(dir) === dir) throw new Error(`no config.yaml with skillGroups in ${here} or in a directory above it - run from the workspace the skill runs in, or pass --workspace`);
  }
}

// The apps the checks mount: each answers, fails or is absent in one of the ways design 2.9 and
// 2.10 name. They are written fresh for every run, so no app of the repository is loaded.
const APPS = {
  ok: "exports.createApp = async ({ mountedAt }) => (req, res) => {\n"
      + "  res.writeHead(200, { 'content-type': 'application/json' });\n"
      + '  res.end(JSON.stringify({ url: req.url, mountedAt }));\n};\n',
  throw: "exports.createApp = () => () => { throw new Error('thrown on purpose'); };\n",
  reject: "exports.createApp = () => async () => { throw new Error('rejected on purpose'); };\n",
  float: "exports.createApp = () => (req, res) => {\n"
         + "  res.end('answered');\n  setTimeout(() => { throw new Error('a later tick'); }, 20);\n};\n",
  forget: "exports.createApp = () => (req, res) => {\n"
          + "  res.end('answered');\n  Promise.reject(new Error('forgotten'));\n};\n",
  none: null, // a directory with no app.js
};

const results = [];
function note(name, ok, seen) {
  results.push(ok);
  console.log(`[${ok ? 'PASS' : 'FAIL'}] ${name}`);
  if (!ok) console.log(`         ${seen}`);
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function freePort() {
  return new Promise((resolve, reject) => {
    const s = net.createServer();
    s.on('error', reject);
    s.listen(0, '127.0.0.1', () => { const { port } = s.address(); s.close(() => resolve(port)); });
  });
}

function get(port, p) {
  return new Promise((resolve, reject) => {
    const req = http.request({ host: '127.0.0.1', port, path: p, timeout: WAIT_MS }, (res) => {
      let body = '';
      res.setEncoding('utf8');
      res.on('data', (c) => { body += c; });
      res.on('end', () => resolve({ status: res.statusCode, headers: res.headers, body }));
    });
    req.on('timeout', () => req.destroy(new Error(`no answer to ${p} within ${WAIT_MS} ms`)));
    req.on('error', reject);
    req.end();
  });
}

/** The hub as a child process, its output gathered; `done` settles with its exit code. */
function start(hubDir, args = []) {
  const child = spawn(process.execPath, ['server.js', ...args], { cwd: hubDir });
  child.out = '';
  child.err = '';
  child.stdout.on('data', (c) => { child.out += c; });
  child.stderr.on('data', (c) => { child.err += c; });
  child.done = new Promise((r) => child.on('exit', (code) => r(code)));
  return child;
}

async function startListening(hubDir) {
  const child = start(hubDir);
  for (let waited = 0; waited < WAIT_MS; waited += 30) {
    if (child.out.includes('serving') || child.exitCode !== null) break;
    await sleep(30);
  }
  return child;
}

async function stop(child) {
  if (child && child.exitCode === null) { child.kill(); await child.done; }
}

function copyDir(from, to) {
  fs.mkdirSync(to, { recursive: true });
  for (const e of fs.readdirSync(from, { withFileTypes: true })) {
    if (e.isDirectory()) copyDir(path.join(from, e.name), path.join(to, e.name));
    else fs.copyFileSync(path.join(from, e.name), path.join(to, e.name));
  }
}

const escaped = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;').replace(/'/g, '&#39;');

async function checks(hubDir, appsDir) {
  const conf = path.join(hubDir, 'app.config.json');
  const writeConf = (c) => fs.writeFileSync(conf, typeof c === 'string' ? c : JSON.stringify(c, null, 2));
  const mount = (name) => ({ appDir: path.join(appsDir, name) });
  const complete = (port) => ({
    title: 'Test Hub', port, assembledAt: '2026-11-02 10:00:00',
    links: [
      { label: 'Alpha <script>alert(1)</script>', href: 'http://127.0.0.1:1/"x"', note: "it's </a> here" },
      { label: 'Share', href: 'file:///tmp/x' },
      { label: 'OK', href: '/ok/', mount: { ...mount('ok'), skill: 'some-skill' } },
      { label: 'None', href: '/none/', mount: { ...mount('none'), skill: 'owner-skill' } },
      { label: 'Throw', href: '/throw/', mount: mount('throw') },
      { label: 'Reject', href: '/reject/', mount: mount('reject') },
      { label: 'Float', href: '/float/', mount: mount('float') },
      { label: 'Forget', href: '/forget/', mount: mount('forget') },
    ],
  });
  const without = (port, ...keys) => { const c = complete(port); for (const k of keys) delete c[k]; return c; };

  // Design 2.5: a file that breaks the schema stops the hub before it listens, with exit 2
  const refusals = [
    ['no port', (p) => without(p, 'port'), [], /port is missing/],
    ['no port, with --port', (p) => without(p, 'port'), ['--port', '0'], /port is missing/],
    ['no title, with --title', (p) => without(p, 'title'), ['--title', 'X'], /title is missing/],
    ['no links and no assembledAt', (p) => without(p, 'links', 'assembledAt'), [],
      /links is missing[\s\S]*assembledAt is missing/],
    ['port as text, links not a list', (p) => ({ ...complete(p), port: String(p), links: {} }), [],
      /port is not a whole number[\s\S]*links is not a list/],
    ['a file that is not JSON', () => '{ "title": "x", ', [], /is not JSON/],
    ['no file', null, [], /cannot be read/],
  ];
  for (const [name, make, args, expected] of refusals) {
    const port = await freePort();
    if (make) writeConf(make(port)); else fs.rmSync(conf, { force: true });
    const child = start(hubDir, args);
    const code = await Promise.race([child.done, sleep(WAIT_MS).then(() => `still running after ${WAIT_MS} ms`)]);
    await stop(child);
    const listened = child.out.includes('serving');
    note(`refuses to start: ${name}`, code === 2 && expected.test(child.err) && !listened,
         `exit ${code}, listened ${listened}, stderr ${JSON.stringify(child.err.trim())}`);
  }

  const port = await freePort();
  writeConf(complete(port));
  const hub = await startListening(hubDir);
  try {
    note('starts on a complete configuration', hub.out.includes(`http://127.0.0.1:${port}/`),
         `exit ${hub.exitCode}, stdout ${JSON.stringify(hub.out)}, stderr ${JSON.stringify(hub.err)}`);

    // Design 2.7: the page
    let r = await get(port, '/');
    const anchors = [...r.body.matchAll(/<a href="([^"]*)">\s*<span class="label">([^<]*)<\/span>/g)]
      .map((m) => [m[1], m[2]]);
    const wanted = complete(port).links.map((l) => [escaped(l.href), escaped(l.label)]);
    note('the buttons match the configuration, in order', JSON.stringify(anchors) === JSON.stringify(wanted),
         `anchors ${JSON.stringify(anchors)}`);
    const anchorCount = (r.body.match(/<a /g) || []).length;
    note('configuration text cannot become markup',
         !/<script/i.test(r.body) && anchorCount === 8 && r.body.includes('&lt;script&gt;')
           && r.body.includes('&#39;s &lt;/a&gt;'),
         `${anchorCount} anchors; a script tag ${/<script/i.test(r.body) ? 'present' : 'absent'}`);
    const refs = [...r.body.matchAll(/(?:src|href)="([^"]*)"/g)].map((m) => m[1])
      .filter((h) => !wanted.some(([href]) => href === h));
    note('the page loads nothing but ./app.css', JSON.stringify(refs) === '["./app.css"]' && !/<script/i.test(r.body),
         `references besides the buttons: ${JSON.stringify(refs)}`);
    const health = JSON.parse((await get(port, '/healthz')).body);
    note('the dead count is in /healthz, not on the page', health.dead === 1 && !/dead|cannot navigate/i.test(r.body),
         `/healthz dead ${health.dead}`);

    // Design 2.3 and 2.7: the page reads the file again at each request
    const edited = complete(port);
    edited.title = 'Edited Title';
    edited.links = [...edited.links, { label: 'Added', href: 'http://127.0.0.1:2/' }];
    writeConf(edited);
    r = await get(port, '/');
    note('an edit reaches the page on the next request',
         r.status === 200 && r.body.includes('<title>Edited Title</title>') && r.body.includes('>Added</span>'),
         `status ${r.status}`);
    writeConf('{ broken');
    r = await get(port, '/');
    const healthWhileBroken = await get(port, '/healthz');
    note('a file broken while the hub runs is refused with 500, and the hub goes on',
         r.status === 500 && /is not JSON/.test(r.body) && healthWhileBroken.status === 200,
         `page ${r.status} ${JSON.stringify(r.body)}, /healthz ${healthWhileBroken.status}`);
    writeConf(without(port, 'title'));
    r = await get(port, '/');
    note('a field removed while the hub runs is refused with 500, by name',
         r.status === 500 && /title is missing/.test(r.body), `page ${r.status} ${JSON.stringify(r.body)}`);
    writeConf(complete(port));
    r = await get(port, '/');
    note('the page answers again once the file is whole', r.status === 200, `status ${r.status}`);

    // Design 2.8 and 2.9: mounts
    r = await get(port, '/ok/');
    note('a mounted app answers under its prefix',
         r.status === 200 && JSON.parse(r.body).mountedAt === '/ok', `status ${r.status}, ${r.body}`);
    r = await get(port, '/ok/a/b?q=1');
    note('the prefix is stripped before the app sees it',
         r.status === 200 && JSON.parse(r.body).url === '/a/b?q=1', `status ${r.status}, ${r.body}`);
    r = await get(port, '/ok?q=1');
    note('a bare prefix is redirected into the mount', r.status === 308 && r.headers.location === '/ok/?q=1',
         `status ${r.status}, location ${r.headers.location}`);
    r = await get(port, '/none/');
    const okAfterNone = await get(port, '/ok/');
    note('an absent mount answers 503 naming its owner, and breaks nothing',
         r.status === 503 && /not mounted/.test(r.body) && /owner-skill/.test(r.body) && okAfterNone.status === 200,
         `/none/ ${r.status}, /ok/ ${okAfterNone.status}`);

    // Design 2.10: a mounted app's failure stays inside its mount
    r = await get(port, '/throw/');
    note("a mounted app's throw stays in its mount",
         r.status === 502 && (await get(port, '/healthz')).status === 200 && (await get(port, '/ok/')).status === 200,
         `/throw/ ${r.status}`);
    r = await get(port, '/reject/');
    note("a mounted app's rejected promise stays in its mount",
         r.status === 502 && (await get(port, '/healthz')).status === 200, `/reject/ ${r.status}`);
    r = await get(port, '/float/');
    await sleep(150);
    note("a mounted app's floating throw is not fatal",
         r.status === 200 && hub.exitCode === null && (await get(port, '/healthz')).status === 200,
         `/float/ ${r.status}, process ${hub.exitCode === null ? 'alive' : `ended with ${hub.exitCode}`}`);
    r = await get(port, '/forget/');
    await sleep(150);
    note("a mounted app's forgotten rejection is not fatal",
         r.status === 200 && hub.exitCode === null && (await get(port, '/healthz')).status === 200,
         `/forget/ ${r.status}, process ${hub.exitCode === null ? 'alive' : `ended with ${hub.exitCode}`}`);
    r = await get(port, '/nowhere');
    note('any other path is 404', r.status === 404, `status ${r.status}`);
  } finally {
    await stop(hub);
  }

  // Design 2.10: two hubs are the same code reading two files
  const port2 = await freePort();
  writeConf({ title: 'Another Hub', port: port2, assembledAt: '2026-11-02 11:00:00',
              links: [{ label: 'Only', href: 'http://127.0.0.1:3/' }] });
  const hub2 = await startListening(hubDir);
  try {
    const r = await get(port2, '/');
    note('the same code serves another configuration as its own',
         r.body.includes('<title>Another Hub</title>') && (r.body.match(/<a /g) || []).length === 1,
         `status ${r.status}`);
  } finally {
    await stop(hub2);
  }
}

// The arguments: an optional --run {yymmdd}.{N}, an optional --workspace and an optional hub
// directory, in any order.
function parseArgs(argv) {
  const args = { run: null, workspace: null, hub: null };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--run') {
      args.run = argv[++i];
      if (!/^\d{6}\.\d+$/.test(args.run || '')) throw new Error(`--run needs a Run Number {yymmdd}.{N}, not ${args.run}`);
    } else if (argv[i] === '--workspace') {
      args.workspace = argv[++i];
      if (!args.workspace) throw new Error('--workspace needs a directory');
    } else if (argv[i].startsWith('--')) {
      throw new Error(`unknown option ${argv[i]}`);
    } else if (args.hub === null) {
      args.hub = argv[i];
    } else {
      throw new Error(`one hub directory only, not also ${argv[i]}`);
    }
  }
  return args;
}

// The work directory: test-hub/ in the Working Dir of the run, kept; or, outside a run, a new
// temp/test-hub-* that main removes.
function workDir(run, workspace) {
  const root = workspaceRoot(workspace);
  const tempDir = path.join(root, 'temp');
  if (run) {
    const work = path.join(root, 'checkpoints', 'imp-home', run, 'test-hub');
    fs.rmSync(work, { recursive: true, force: true });
    fs.mkdirSync(work, { recursive: true });
    return work;
  }
  fs.mkdirSync(tempDir, { recursive: true });
  return fs.mkdtempSync(path.join(tempDir, 'test-hub-'));
}

async function main() {
  let args;
  try {
    args = parseArgs(process.argv.slice(2));
  } catch (err) {
    console.error(err.message);
    process.exitCode = 2;
    return;
  }
  const source = path.resolve(args.hub || SEED);
  if (!fs.existsSync(path.join(source, 'server.js'))) {
    console.error(`no server.js in ${source}`);
    process.exitCode = 2;
    return;
  }
  let work;
  try {
    work = workDir(args.run, args.workspace);
  } catch (err) {
    console.error(err.message);
    process.exitCode = 2;
    return;
  }
  try {
    const hubDir = path.join(work, 'hub');
    const appsDir = path.join(work, 'apps');
    fs.mkdirSync(hubDir);
    fs.copyFileSync(path.join(source, 'server.js'), path.join(hubDir, 'server.js'));
    if (fs.existsSync(path.join(source, 'public'))) copyDir(path.join(source, 'public'), path.join(hubDir, 'public'));
    for (const [name, code] of Object.entries(APPS)) {
      fs.mkdirSync(path.join(appsDir, name), { recursive: true });
      if (code) fs.writeFileSync(path.join(appsDir, name, 'app.js'), code);
    }
    console.log(`hub: ${source}`);
    await checks(hubDir, appsDir);
  } finally {
    if (!args.run) fs.rmSync(work, { recursive: true, force: true });
  }
  if (args.run) console.log(`work directory kept: ${work}`);
  const failed = results.filter((ok) => !ok).length;
  console.log(`\n${results.length - failed} passed, ${failed} failed`);
  process.exitCode = failed ? 1 : 0;
}

main().catch((err) => { console.error(err); process.exitCode = 1; });
