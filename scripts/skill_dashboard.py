#!/usr/bin/env python3
"""產生 skill token dashboard（單一 HTML，不需網路、可直接用瀏覽器開）。

流程：
  1. 掃描 session 紀錄 → 更新 database/skill-tokens/{workspace}#{session}#{skill}.yaml（每次執行檔）
     → 合併成 database/skill-tokens-daily/yymmdd.yaml（每日快照，同一天重跑會覆寫）
  2. 從每日快照產生 dashboard/skill-dashboard.html（永遠是最新版）
  3. 同時存一份 dashboard-hist/skill-dashboard-yymmdd.html 當歷史紀錄

用法：
  python3 scripts/skill_dashboard.py                    # 跑完 1 → 3
  python3 scripts/skill_dashboard.py <資料夾或.jsonl>    # 只分析指定紀錄（不動每次執行檔）
  python3 scripts/skill_dashboard.py --from database/skill-tokens-daily/261011.yaml
                                                        # 跳過 1，從既有快照重新產生 2、3
"""
import argparse
import html
import json
import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(__file__))
from skill_tokens import ROOT, RUN_DIR, update_database  # noqa: E402

DASH_PATH = os.path.join(ROOT, "dashboard", "skill-dashboard.html")
HIST_DIR = os.path.join(ROOT, "dashboard-hist")

TEMPLATE = r"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Skill Token Dashboard</title>
<style>
:root {
  color-scheme: light;
  --surface-0: #f5f4f1; --surface-1: #fcfcfb; --border: #e4e2dc; --grid: #ecebe7;
  --text-primary: #0b0b0b; --text-secondary: #52514e; --text-muted: #7a7974;
  --s1: #2a78d6; --s2: #eb6834; --s3: #1baf7a; --s4: #eda100; --wait: #b4b2a9;
}
@media (prefers-color-scheme: dark) {
  :root:where(:not([data-theme="light"])) {
    color-scheme: dark;
    --surface-0: #121211; --surface-1: #1a1a19; --border: #2e2e2b; --grid: #262624;
    --text-primary: #ffffff; --text-secondary: #c3c2b7; --text-muted: #8f8e86;
    --s1: #3987e5; --s2: #d95926; --s3: #199e70; --s4: #c98500; --wait: #6b6a64;
  }
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --surface-0: #121211; --surface-1: #1a1a19; --border: #2e2e2b; --grid: #262624;
  --text-primary: #ffffff; --text-secondary: #c3c2b7; --text-muted: #8f8e86;
  --s1: #3987e5; --s2: #d95926; --s3: #199e70; --s4: #c98500; --wait: #6b6a64;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--surface-0); color: var(--text-primary);
  font: 14px/1.5 -apple-system, "PingFang TC", "Noto Sans TC", system-ui, sans-serif; }
main { max-width: 1100px; margin: 0 auto; padding: 24px 16px 48px; }
header { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }
header .sub { display: block; margin-top: 2px; }
.seg.ws button { padding: 6px 16px; font-size: 14px; }
h1 { font-size: 22px; margin: 0; }
h2 { font-size: 15px; margin: 0 0 4px; }
.sub { color: var(--text-secondary); font-size: 13px; }
.muted { color: var(--text-muted); font-size: 12px; }
.card { background: var(--surface-1); border: 1px solid var(--border); border-radius: 12px; padding: 16px; margin-top: 16px; }
.kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin-top: 16px; }
.kpi { background: var(--surface-1); border: 1px solid var(--border); border-radius: 12px; padding: 14px 16px; }
.kpi .v { font-size: 26px; font-weight: 600; font-variant-numeric: tabular-nums; }
.kpi .l { color: var(--text-secondary); font-size: 13px; }
.legend { display: flex; flex-wrap: wrap; gap: 14px; margin: 8px 0 4px; font-size: 12px; color: var(--text-secondary); }
.legend i { display: inline-block; width: 10px; height: 10px; border-radius: 3px; margin-right: 6px; vertical-align: -1px; }
svg { display: block; width: 100%; height: auto; overflow: visible; }
svg text { fill: var(--text-secondary); font-size: 12px; }
.multiples { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 12px; margin-top: 8px; }
.multiple { border: 1px solid var(--grid); border-radius: 10px; padding: 10px 12px 6px; min-width: 0; }
.multiple h3 { font-size: 13px; margin: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.multiple .muted { margin-bottom: 4px; }
.multiple svg text { font-size: 11px; }
.multiple { cursor: zoom-in; transition: border-color .15s, box-shadow .15s; }
.multiple:hover, .multiple:focus-visible { border-color: var(--s1); box-shadow: 0 0 0 1px var(--s1); outline: none; }
.zoom { position: fixed; inset: 0; background: rgba(0,0,0,.45); display: flex; align-items: center;
  justify-content: center; padding: 16px; z-index: 5; }
.zoom[hidden] { display: none; }
.relation { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.4fr); gap: 20px; margin-top: 12px; align-items: start; }
@media (max-width: 760px) { .relation { grid-template-columns: 1fr; } }
#priceTable th:first-child, #priceTable td:first-child { text-align: left; }
#priceTable .x { color: var(--text-muted); font-size: 12px; }
.rel-model { margin-bottom: 14px; }
.rel-model h3 { font-size: 14px; margin: 0 0 2px; }
.rel-row { display: grid; grid-template-columns: 64px 1fr; align-items: center; gap: 10px; margin-top: 6px; font-size: 12px; color: var(--text-secondary); }
.rel-bar { display: flex; height: 22px; gap: 2px; }
.rel-bar div { height: 100%; display: flex; align-items: center; justify-content: center; font-size: 11px;
  color: #fff; font-variant-numeric: tabular-nums; overflow: hidden; white-space: nowrap; min-width: 2px; }
.rel-bar div:first-child { border-radius: 4px 0 0 4px; }
.rel-bar div:last-child { border-radius: 0 4px 4px 0; }
.rel-bar div:only-child { border-radius: 4px; }
.rel-empty { color: var(--text-muted); font-size: 12px; margin-top: 4px; }
.zoom-box { background: var(--surface-1); border: 1px solid var(--border); border-radius: 14px; padding: 18px 20px;
  width: min(1100px, 100%); max-height: calc(100vh - 32px); overflow: auto; box-shadow: 0 12px 40px rgba(0,0,0,.3); }
.zoom-head { display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; }
.zoom-head h2 { font-size: 18px; }
.zoom-bar { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin: 8px 0 4px; }
.zoom-bar .legend { margin: 0; }
.seg { display: inline-flex; border: 1px solid var(--border); border-radius: 8px; padding: 2px; background: var(--surface-0); }
.seg button { border: 0; background: transparent; color: var(--text-secondary); padding: 4px 14px; border-radius: 6px;
  font: inherit; font-size: 13px; cursor: pointer; }
.seg button[aria-pressed="true"] { background: var(--surface-1); color: var(--text-primary); font-weight: 600;
  box-shadow: 0 1px 2px rgba(0,0,0,.15); }
.zoom-head button { border: 1px solid var(--border); background: var(--surface-0); color: var(--text-primary);
  width: 32px; height: 32px; border-radius: 8px; font-size: 20px; line-height: 1; cursor: pointer; flex: none; }
.zoom svg text { font-size: 13px; }
#zoomTable { margin-top: 12px; }
#zoomTable th:nth-child(-n+3), #zoomTable td:nth-child(-n+3) { text-align: left; }
.tip { position: fixed; pointer-events: none; background: var(--surface-1); border: 1px solid var(--border);
  border-radius: 8px; padding: 8px 10px; font-size: 12px; box-shadow: 0 4px 16px rgba(0,0,0,.15);
  opacity: 0; transition: opacity .1s; z-index: 10; min-width: 160px; }
.tip b { display: block; margin-bottom: 4px; color: var(--text-primary); }
.tip .row { display: flex; justify-content: space-between; gap: 16px; color: var(--text-secondary); }
.tip .row span:last-child { font-variant-numeric: tabular-nums; color: var(--text-primary); }
.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: 13px; font-variant-numeric: tabular-nums; }
th, td { padding: 7px 10px; border-bottom: 1px solid var(--grid); text-align: right; white-space: nowrap; }
th { color: var(--text-secondary); font-weight: 500; cursor: pointer; user-select: none; }
th:nth-child(-n+6), td:nth-child(-n+6) { text-align: left; }
tr:hover td { background: var(--surface-0); }
.hit { fill: transparent; cursor: default; }
.sess-meta { font-size: 11px; color: var(--text-muted); max-width: 220px; overflow: hidden; text-overflow: ellipsis; }
.badge { display: inline-block; margin-left: 6px; padding: 0 6px; border-radius: 4px; font-size: 11px;
  border: 1px solid var(--border); color: var(--text-secondary); background: var(--surface-0); }
.avgbar { display: flex; align-items: center; gap: 8px; justify-content: flex-end; }
.avgbar span { display: inline-block; height: 10px; border-radius: 0 4px 4px 0; background: var(--s1); }
#avg td:nth-child(3) { min-width: 180px; }
#avg th:nth-child(-n+5), #avg td:nth-child(-n+5) { text-align: right; }
#avg th:first-child, #avg td:first-child { text-align: left; }
</style>
</head>
<body>
<main>
  <header>
    <div>
      <h1>Skill Token Dashboard</h1>
      <span class="sub">__SUBTITLE__</span>
    </div>
    <div class="seg ws" id="wsToggle" role="group" aria-label="workspace"></div>
  </header>

  <section class="kpis" id="kpis"></section>

  <section class="card">
    <h2>token 和 cost 的關係</h2>
    <div class="muted">cost = Σ（各類 token 數 × 該類單價）。四類 token 單價差很多，所以 token 多不一定貴。</div>
    <div class="relation">
      <div class="table-wrap"><table id="priceTable"></table></div>
      <div><div class="legend" id="legend0"></div><div id="relModels"></div></div>
    </div>
  </section>

  <section class="card">
    <h2 id="bySkillTitle">各 skill 的 cost 組成</h2>
    <div class="muted" id="bySkillSub">依總 cost 排序；把滑鼠移到長條上看明細</div>
    <div class="zoom-bar">
      <div class="legend" id="legend"></div>
      <div class="seg" id="bySkillToggle" role="group" aria-label="長條單位">
        <button data-m="cost" aria-pressed="true">cost</button><button data-m="token" aria-pressed="false">token</button><button data-m="time" aria-pressed="false">time</button>
      </div>
    </div>
    <svg id="bySkill"></svg>
  </section>

  <section class="card">
    <h2>各 skill 平均花費</h2>
    <div class="muted">平均只計入有產生回應的執行（中斷、沒有回應的不算）；點欄位標題排序</div>
    <div class="table-wrap"><table id="avg"></table></div>
  </section>

  <section class="card">
    <h2 id="multiTitle">各 skill 每次執行的 token</h2>
    <div class="muted" id="multiSub"></div>
    <div class="zoom-bar">
      <div class="legend" id="legend2"></div>
      <div class="seg" id="multiToggle" role="group" aria-label="Y 軸">
        <button data-m="token" aria-pressed="true">token</button><button data-m="cost" aria-pressed="false">cost</button><button data-m="time" aria-pressed="false">time</button>
      </div>
    </div>
    <div class="multiples" id="multiples"></div>
  </section>

  <section class="card">
    <h2 id="byRunTitle">每次執行的 cost</h2>
    <div class="zoom-bar">
      <div class="muted" id="byRunSub">依時間排序；每根長條是一次 skill 執行</div>
      <div class="seg" id="byRunToggle" role="group" aria-label="長條單位">
        <button data-m="cost" aria-pressed="true">cost</button><button data-m="token" aria-pressed="false">token</button><button data-m="time" aria-pressed="false">time</button>
      </div>
    </div>
    <svg id="byRun"></svg>
  </section>

  <section class="card">
    <h2>執行明細</h2>
    <div class="muted">點欄位標題排序</div>
    <div class="table-wrap"><table id="runs"></table></div>
  </section>

  <p class="muted">cost 以 API 定價估算（每百萬 token）：Opus 5.5 $4 / $20、Sonnet 5.5 $2 / $10，cache 讀取 $0.20，cache 寫入 1.25x（5 分鐘）或 2x（1 小時）input 價格。訂閱方案下為等值 API 價格，非實際收費。</p>
</main>
<div class="zoom" id="zoom" hidden>
  <div class="zoom-box" role="dialog" aria-modal="true" aria-labelledby="zoomTitle">
    <div class="zoom-head">
      <div><h2 id="zoomTitle"></h2><div class="muted" id="zoomSub"></div></div>
      <button id="zoomClose" aria-label="關閉">×</button>
    </div>
    <div class="zoom-bar">
      <div class="legend" id="legend3"></div>
      <div class="seg" id="zoomToggle" role="group" aria-label="Y 軸">
        <button data-m="token" aria-pressed="true">token</button><button data-m="cost" aria-pressed="false">cost</button><button data-m="time" aria-pressed="false">time</button>
      </div>
    </div>
    <svg id="zoomSvg"></svg>
    <div class="table-wrap"><table id="zoomTable"></table></div>
  </div>
</div>
<div class="tip" id="tip"></div>

<script>
const ALL_RUNS = __DATA__;
const WORKSPACES = __WORKSPACES__;
let RUNS = ALL_RUNS;
const PRICING = __PRICING__;
const PARTS = [
  { key: "read",  label: "cache 讀取", color: "var(--s1)" },
  { key: "write", label: "cache 寫入", color: "var(--s2)" },
  { key: "out",   label: "output",     color: "var(--s3)" },
  { key: "in",    label: "input",      color: "var(--s4)" },
];
// 時間：實際執行 + 等你回答（選擇題），兩段堆疊成總經過時間
const TIME_PARTS = [
  { key: "active", label: "實際執行", color: "var(--s1)" },
  { key: "wait",   label: "等你回答", color: "var(--wait)" },
];
const legendHtml = (parts) => parts.map((p) => `<span><i style="background:${p.color}"></i>${p.label}</span>`).join("");
// 秒 → 分:秒，超過一小時 → 時:分:秒
function fmtDur(sec) {
  if (sec == null || isNaN(sec)) return "–";
  const t = Math.round(sec), h = Math.floor(t / 3600), m = Math.floor((t % 3600) / 60), x = t % 60;
  const p = (n) => String(n).padStart(2, "0");
  return h ? `${h}:${p(m)}:${p(x)}` : `${m}:${p(x)}`;
}
// 時間軸刻度：取整齊的分鐘數
function niceMaxDur(v) {
  const steps = [15, 30, 60, 120, 300, 600, 900, 1200, 1800, 2400, 2700, 3600, 5400, 7200, 10800, 21600];
  return (steps.find((st) => st * 4 >= v) || Math.ceil(v / 4 / 3600) * 3600) * 4;
}
const NS = "http://www.w3.org/2000/svg";
const $ = (id) => document.getElementById(id);
const usd = (v) => "$" + v.toFixed(v >= 10 ? 2 : 3);
const num = (v) => Math.round(v).toLocaleString("en-US");
const short = (v) => v >= 1e9 ? (v / 1e9).toFixed(2) + "B" : v >= 1e6 ? (v / 1e6).toFixed(1) + "M" : v >= 1e3 ? (v / 1e3).toFixed(0) + "K" : String(v);
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

// 取一個好讀的軸上限（整齊級距 x 10^n 的 4 等分）
function niceMax(v) {
  const step = v / 4, mag = 10 ** Math.floor(Math.log10(step));
  const nice = [1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10].find((m) => m * mag >= step) * mag;
  return nice * 4;
}
const axisUsd = (v) => "$" + (v >= 1 || v === 0 ? +v.toFixed(2) : +v.toFixed(3));

function el(tag, attrs, parent) {
  const n = document.createElementNS(NS, tag);
  for (const k in attrs) n.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(n);
  return n;
}

// ---------- tooltip ----------
const tip = $("tip");
function showTip(ev, title, rows) {
  tip.innerHTML = "<b>" + esc(title) + "</b>" +
    rows.map(([k, v]) => `<div class="row"><span>${esc(k)}</span><span>${esc(v)}</span></div>`).join("");
  tip.style.opacity = 1;
  const pad = 14, w = tip.offsetWidth, h = tip.offsetHeight;
  let x = ev.clientX + pad, y = ev.clientY + pad;
  if (x + w > innerWidth - 8) x = ev.clientX - w - pad;
  if (y + h > innerHeight - 8) y = ev.clientY - h - pad;
  tip.style.left = x + "px"; tip.style.top = y + "px";
}
const hideTip = () => (tip.style.opacity = 0);

// 執行時間欄：顯示實際執行，滑鼠提示總經過與等待
const durCell = (r) => r.dur_total == null ? "–" :
  `<span title="總經過 ${fmtDur(r.dur_total)} · 等你回答 ${fmtDur(r.dur_wait)}（推算）">${fmtDur(r.dur_active)}</span>`;

// ---------- aggregate ----------
let bySkill, skills, total, tokens;
function aggregate() {
bySkill = {};
for (const r of RUNS) {
  const a = bySkill[r.skill] ||= { skill: r.skill, n: 0, cost: 0, calls: 0, in: 0, write: 0, read: 0, out: 0,
    parts: { in: 0, write: 0, read: 0, out: 0 }, active: 0, wait: 0, timed: 0 };
  a.n++; a.cost += r.cost; a.calls += r.calls;
  if (r.dur_total != null) { a.active += r.dur_active; a.wait += r.dur_wait; a.timed++; }
  for (const k of ["in", "write", "read", "out"]) { a[k] += r[k]; a.parts[k] += r.cost_parts[k]; }
}
skills = Object.values(bySkill).sort((a, b) => b.cost - a.cost);
total = RUNS.reduce((s, r) => s + r.cost, 0);
tokens = RUNS.reduce((s, r) => s + r.in + r.write + r.read + r.out, 0);
}

// ---------- KPIs ----------
function renderKpis() {
$("kpis").innerHTML = [
  [usd(total), "估算總 cost"],
  [RUNS.length, "skill 執行次數"],
  [RUNS.length ? usd(total / RUNS.length) : "–", "平均每次 cost"],
  [short(tokens), "處理的 token 總量"],
].map(([v, l]) => `<div class="kpi"><div class="v">${v}</div><div class="l">${l}</div></div>`).join("");
}

$("legend0").innerHTML = $("legend3").innerHTML = $("legend2").innerHTML = $("legend").innerHTML = legendHtml(PARTS);

// ---------- chart 1: stacked horizontal bars by skill ----------
// metric = "cost"：長條是美元；"token"：長條是 token 數
let bySkillMetric = "cost";
function setBySkillMetric(m) {
  bySkillMetric = m;
  document.querySelectorAll("#bySkillToggle button").forEach((b) => b.setAttribute("aria-pressed", b.dataset.m === m));
  const label = ` ${m} `;
  $("bySkillTitle").textContent = `各 skill 的${label}組成`;
  $("bySkillSub").textContent = `依總${label}排序；把滑鼠移到長條上看明細` +
    (m === "time" ? "（所有執行的合計；time 是推算的：呼叫 skill 到最後一則回應）" : "");
  $("legend").innerHTML = legendHtml(m === "time" ? TIME_PARTS : PARTS);
  drawBySkill();
}
document.querySelectorAll("#bySkillToggle button").forEach((b) => b.onclick = () => setBySkillMetric(b.dataset.m));

function drawBySkill() {
  const svg = $("bySkill");
  svg.innerHTML = "";
  const isCost = bySkillMetric === "cost", isTime = bySkillMetric === "time";
  const PS = isTime ? TIME_PARTS : PARTS;
  const part = (s, p) => isCost ? s.parts[p.key] : s[p.key];
  const totalOf = (s) => isTime ? s.active + s.wait : isCost ? s.cost : s.in + s.write + s.read + s.out;
  const fmtV = isTime ? fmtDur : isCost ? usd : short;
  const rows = [...skills].sort((a, b) => totalOf(b) - totalOf(a));
  const W = svg.clientWidth || 1000, rowH = 34, barH = 18, top = 8;
  const left = Math.min(230, W * 0.36), right = 64;
  const maxChars = Math.floor((left - 14) / 7);
  const H = top + rows.length * rowH + 24;
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  const top1 = Math.max(...rows.map(totalOf), isCost ? 0.001 : 1);
  const max = isTime ? niceMaxDur(top1) : niceMax(top1);
  const x = (v) => (v / max) * (W - left - right);

  for (let i = 0; i <= 4; i++) {
    const gx = left + (i / 4) * (W - left - right);
    el("line", { x1: gx, x2: gx, y1: top, y2: H - 22, stroke: "var(--grid)" }, svg);
    el("text", { x: gx, y: H - 6, "text-anchor": "middle" }, svg).textContent = (isTime ? fmtDur : isCost ? axisUsd : short)((max * i) / 4);
  }
  rows.forEach((s, i) => {
    const y = top + i * rowH + (rowH - barH) / 2;
    const lbl = el("text", { x: left - 10, y: y + barH / 2 + 4, "text-anchor": "end" }, svg);
    lbl.textContent = s.skill.length > maxChars ? s.skill.slice(0, maxChars - 1) + "…" : s.skill;
    let cx = left;
    const segs = PS.filter((p) => x(part(s, p)) >= 0.5);
    segs.forEach((p, j) => {
      const w = x(part(s, p));
      const gap = j < segs.length - 1 ? 2 : 0;
      el("rect", { x: cx, y, width: Math.max(w - gap, 0.5), height: barH, rx: 3, fill: p.color }, svg);
      cx += w;
    });
    el("text", { x: cx + 8, y: y + barH / 2 + 4, fill: "var(--text-primary)" }, svg).textContent = fmtV(totalOf(s));
    const hit = el("rect", { class: "hit", x: 0, y: top + i * rowH, width: W, height: rowH }, svg);
    hit.addEventListener("mousemove", (ev) => showTip(ev, s.skill, isTime ? [
      ["執行次數", s.timed === s.n ? s.n : `${s.timed} / ${s.n}`],
      ["平均實際執行", s.timed ? fmtDur(s.active / s.timed) : "–"],
      ["實際執行合計", fmtDur(s.active)], ["等你回答合計", fmtDur(s.wait)], ["總經過合計", fmtDur(s.active + s.wait)],
      ["cost", usd(s.cost)],
    ] : [
      ["執行次數", s.n], ["平均每次", fmtV(totalOf(s) / s.n)],
      ...PARTS.map((p) => [p.label, isCost ? `${usd(s.parts[p.key])}（${short(s[p.key])}）`
                                           : `${short(s[p.key])}（${usd(s.parts[p.key])}）`]),
      ["總計", `${usd(s.cost)} · ${short(s.in + s.write + s.read + s.out)} token`],
    ]));
    hit.addEventListener("mouseleave", hideTip);
  });
}

// ---------- chart 2: cost per run over time ----------
// metric = cost / token / time（time 是推算的實際執行時間）；長條維持單色
let byRunMetric = "cost";
function setByRunMetric(m) {
  byRunMetric = m;
  document.querySelectorAll("#byRunToggle button").forEach((b) => b.setAttribute("aria-pressed", b.dataset.m === m));
  $("byRunTitle").textContent = `每次執行的 ${m}`;
  $("byRunSub").textContent = "依時間排序；每根長條是一次 skill 執行" +
    (m === "time" ? "（實際執行時間，推算；等待時間看滑鼠提示）" : "");
  drawByRun();
}
document.querySelectorAll("#byRunToggle button").forEach((b) => b.onclick = () => setByRunMetric(b.dataset.m));

function drawByRun() {
  const svg = $("byRun");
  svg.innerHTML = "";
  const W = svg.clientWidth || 1000, H = 260, left = 56, right = 8, top = 10, bottom = 40;
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  const runs = [...RUNS].sort((a, b) => a.time.localeCompare(b.time));
  const m = byRunMetric;
  const val = (r) => m === "time" ? (r.dur_active || 0) : m === "token" ? r.in + r.write + r.read + r.out : r.cost;
  const fmtAxis = m === "time" ? fmtDur : m === "token" ? short : axisUsd;
  const top1 = Math.max(...runs.map(val), m === "cost" ? 0.001 : 1);
  const max = m === "time" ? niceMaxDur(top1) : niceMax(top1);
  const ih = H - top - bottom, iw = W - left - right;
  const slot = iw / Math.max(runs.length, 1), bw = Math.min(36, slot * 0.6);
  const y = (v) => top + ih - (v / max) * ih;

  for (let i = 0; i <= 4; i++) {
    const gy = top + ih - (i / 4) * ih;
    el("line", { x1: left, x2: W - right, y1: gy, y2: gy, stroke: "var(--grid)" }, svg);
    el("text", { x: left - 8, y: gy + 4, "text-anchor": "end" }, svg).textContent = fmtAxis((max * i) / 4);
  }
  let lastDay = "", lastX = null;
  runs.forEach((r, i) => {
    const cx = left + slot * i + slot / 2, h = Math.max(top + ih - y(val(r)), 1);
    // 只有頂端圓角、底部貼齊基準線
    const x0 = cx - bw / 2, y0 = top + ih - h, rad = Math.min(4, h, bw / 2);
    el("path", { d: `M${x0},${top + ih} V${y0 + rad} Q${x0},${y0} ${x0 + rad},${y0} H${x0 + bw - rad} Q${x0 + bw},${y0} ${x0 + bw},${y0 + rad} V${top + ih} Z`,
      fill: "var(--s1)" }, svg);
    const day = r.time.slice(5, 10);
    if (day !== lastDay && slot * (i - (lastX ?? -99)) >= 44) {
      el("text", { x: cx, y: H - bottom + 18, "text-anchor": "middle" }, svg).textContent = day;
      lastDay = day; lastX = i;
    }
    const hit = el("rect", { class: "hit", x: left + slot * i, y: top, width: slot, height: ih }, svg);
    // 三種都顯示，目前單位的細項排前面
    const tok = r.in + r.write + r.read + r.out;
    const costRows = [...PARTS.map((p) => [p.label, `${usd(r.cost_parts[p.key])}（${short(r[p.key])}）`]), ["cost 合計", usd(r.cost)]];
    const tokRows = [...PARTS.map((p) => [p.label, `${short(r[p.key])}（${usd(r.cost_parts[p.key])}）`]), ["token 合計", num(tok)]];
    const timeRows = [["實際執行", fmtDur(r.dur_active)], ["等你回答", fmtDur(r.dur_wait)], ["總經過", fmtDur(r.dur_total)]];
    const detail = m === "time" ? [...timeRows, ["cost", usd(r.cost)], ["token 合計", num(tok)]]
      : m === "token" ? [...tokRows, ["cost", usd(r.cost)], ["執行時間", fmtDur(r.dur_active)]]
      : [...costRows, ["token 合計", num(tok)], ["執行時間", fmtDur(r.dur_active)]];
    hit.addEventListener("mousemove", (ev) => showTip(ev, r.skill, [
      ["時間（UTC）", r.time.replace("T", " ")], ["session", r.session],
      ["model", r.model], ["effort", r.effort], ["回應數", r.calls], ...detail,
    ]));
    hit.addEventListener("mouseleave", hideTip);
  });
  el("line", { x1: left, x2: W - right, y1: top + ih, y2: top + ih, stroke: "var(--text-muted)" }, svg);
}

// ---------- 各 skill 每次執行的 token（small multiples，X 為時間軸）----------
const HOUR = 3600e3, DAY = 24 * HOUR;
const parseUtc = (t) => new Date(t + "Z").getTime();
const pad2 = (n) => String(n).padStart(2, "0");
const fmtDay = (ms) => { const d = new Date(ms); return `${pad2(d.getUTCMonth() + 1)}-${pad2(d.getUTCDate())}`; };
const fmtHm = (ms) => { const d = new Date(ms); return `${pad2(d.getUTCHours())}:${pad2(d.getUTCMinutes())}`; };
const TOKEN_KEYS = { read: "read", write: "write", out: "out", in: "in" };

function timeTicks(t0, t1, maxTicks) {
  const steps = [10 * 60e3, 15 * 60e3, 30 * 60e3, HOUR, 2 * HOUR, 3 * HOUR, 6 * HOUR, 12 * HOUR, DAY, 2 * DAY, 7 * DAY];
  const step = steps.find((s) => (t1 - t0) / s <= maxTicks) || steps[steps.length - 1];
  const ticks = [];
  for (let t = Math.ceil(t0 / step) * step; t <= t1; t += step) ticks.push(t);
  return { ticks, step };
}

// 一個切換鈕控制全部小圖；點小圖放大時，放大檢視先用這裡的選擇
let multiMetric = "token";
const MULTI_SUB = {
  token: "Y 軸是 token 數，長條依 token 種類堆疊",
  cost: "Y 軸是 cost，長條依 token 種類的 cost 堆疊",
  time: "Y 軸是執行時間（推算），長條是實際執行加上等你回答",
};
function setMultiMetric(m) {
  multiMetric = m;
  document.querySelectorAll("#multiToggle button").forEach((b) => b.setAttribute("aria-pressed", b.dataset.m === m));
  $("multiTitle").textContent = `各 skill 每次執行的 ${m}`;
  $("multiSub").textContent = `每個 skill 一張圖；X 軸是執行時間（UTC），${MULTI_SUB[m]}（各圖刻度不同）；點一張圖可放大`;
  $("legend2").innerHTML = legendHtml(m === "time" ? TIME_PARTS : PARTS);
  drawMultiples();
}
document.querySelectorAll("#multiToggle button").forEach((b) => b.onclick = () => setMultiMetric(b.dataset.m));

function drawMultiples() {
  const box = $("multiples");
  box.innerHTML = "";
  const groups = {};
  for (const r of RUNS) if (r.calls > 0) (groups[r.skill] ||= []).push(r);
  const order = skills.map((s) => s.skill).filter((k) => groups[k]);

  // 先把所有卡片放進版面，再依實際寬度繪圖（否則第一張會以整列寬度計算）
  const cards = order.map((name) => {
    const runs = groups[name].map((r) => ({ ...r, t: parseUtc(r.time), tok: r.in + r.write + r.read + r.out }))
      .sort((a, b) => a.t - b.t);
    const avgOf = (f) => runs.reduce((x, r) => x + f(r), 0) / runs.length;
    const timed = runs.filter((r) => r.dur_active != null);
    const avgText = multiMetric === "cost" ? `平均 ${usd(avgOf((r) => r.cost))}`
      : multiMetric === "time" ? `平均實際執行 ${timed.length ? fmtDur(timed.reduce((x, r) => x + r.dur_active, 0) / timed.length) : "–"}`
      : `平均 ${short(avgOf((r) => r.tok))} token`;
    const card = document.createElement("div");
    card.className = "multiple";
    card.innerHTML = `<h3 title="${esc(name)}">${esc(name)}</h3>` +
      `<div class="muted">${runs.length} 次 · ${avgText}</div>`;
    const svg = el("svg", {});
    card.appendChild(svg);
    box.appendChild(card);
    card.tabIndex = 0;
    card.setAttribute("role", "button");
    card.setAttribute("aria-label", `放大 ${name} 的圖`);
    const open = () => { zoomMetric = multiMetric; openZoom(name, runs); };
    card.onclick = open;
    card.onkeydown = (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(); } };
    return { name, runs, svg };
  });
  for (const c of cards) drawSkillChart(c.svg, c.name, c.runs, 170, multiMetric);
}

// metric = "token"：Y 軸是 token 數；"cost"：Y 軸是美元
function drawSkillChart(svg, name, runs, H, metric = "token") {
    svg.innerHTML = "";
    const isCost = metric === "cost", isTime = metric === "time";
    const PS = isTime ? TIME_PARTS : PARTS;
    const part = (r, p) => isTime ? (r["dur_" + p.key] || 0) : isCost ? r.cost_parts[p.key] : r[TOKEN_KEYS[p.key]];
    const total = (r) => isTime ? (r.dur_total || 0) : isCost ? r.cost : r.tok;
    const fmtAxis = isTime ? fmtDur : isCost ? axisUsd : short;
    const big = H > 200;
    const W = svg.clientWidth || 320, left = big ? 56 : 44, right = 14, top = 8, bottom = 34;
    svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
    const iw = W - left - right, ih = H - top - bottom;

    // 時間範圍：左右各留 8%（至少 30 分鐘），只有一次就前後各 1 小時，讓長條置中
    let t0 = runs[0].t, t1 = runs[runs.length - 1].t;
    const padT = runs.length === 1 ? HOUR : Math.max((t1 - t0) * 0.08, HOUR / 2);
    t0 -= padT; t1 += padT;
    const x = (t) => left + ((t - t0) / (t1 - t0)) * iw;
    const top1 = Math.max(...runs.map(total), isCost ? 0.001 : 1);
    const max = isTime ? niceMaxDur(top1) : niceMax(top1);
    const y = (v) => top + ih - (v / max) * ih;

    for (let i = 0; i <= 4; i++) {
      const gy = y((max * i) / 4);
      el("line", { x1: left, x2: W - right, y1: gy, y2: gy, stroke: "var(--grid)" }, svg);
      el("text", { x: left - 6, y: gy + 4, "text-anchor": "end" }, svg).textContent = fmtAxis((max * i) / 4);
    }
    const { ticks, step } = timeTicks(t0, t1, Math.max(2, Math.floor(iw / (big ? 90 : 70))));
    let lastDay = "";
    for (const t of ticks) {
      const tx = x(t);
      el("line", { x1: tx, x2: tx, y1: top + ih, y2: top + ih + 4, stroke: "var(--text-muted)" }, svg);
      const day = fmtDay(t);
      if (step < DAY) {
        el("text", { x: tx, y: top + ih + 16, "text-anchor": "middle" }, svg).textContent = fmtHm(t);
        if (day !== lastDay) el("text", { x: tx, y: top + ih + 29, "text-anchor": "middle" }, svg).textContent = day;
      } else {
        el("text", { x: tx, y: top + ih + 16, "text-anchor": "middle" }, svg).textContent = day;
      }
      lastDay = day;
    }

    const bw = Math.max(4, Math.min(big ? 28 : 12, iw / runs.length / 2));
    for (const r of runs) {
      const cx = x(r.t);
      let base = top + ih;
      const segs = PS.filter((p) => part(r, p) > 0);
      segs.forEach((p, j) => {
        const h = (part(r, p) / max) * ih;
        if (h < 0.5) return;
        const isTop = j === segs.length - 1;
        const gap = isTop ? 0 : 1;
        el("rect", { x: cx - bw / 2, y: base - h, width: bw, height: Math.max(h - gap, 0.5),
          rx: isTop ? Math.min(3, bw / 2) : 0, fill: p.color }, svg);
        base -= h;
      });
      const hit = el("rect", { class: "hit", x: cx - Math.max(bw, 14) / 2, y: top, width: Math.max(bw, 14), height: ih }, svg);
      hit.addEventListener("mousemove", (ev) => showTip(ev, name, [
        ["時間（UTC）", r.time.replace("T", " ")], ["model", r.model], ["effort", r.effort],
        ...(isTime ? [["實際執行", fmtDur(r.dur_active)], ["等你回答", fmtDur(r.dur_wait)], ["總經過", fmtDur(r.dur_total)]]
                   : PARTS.map((p) => [p.label, isCost ? usd(part(r, p)) : num(part(r, p))])),
        ["token 合計", num(r.tok)], ["cost", usd(r.cost)],
      ]));
      hit.addEventListener("mouseleave", hideTip);
    }
    el("line", { x1: left, x2: W - right, y1: top + ih, y2: top + ih, stroke: "var(--text-muted)" }, svg);
}

// ---------- 放大檢視 ----------
let zoomed = null, zoomMetric = "token";
function setZoomMetric(m) {
  zoomMetric = m;
  document.querySelectorAll("#zoomToggle button").forEach((b) => b.setAttribute("aria-pressed", b.dataset.m === m));
  $("legend3").innerHTML = legendHtml(m === "time" ? TIME_PARTS : PARTS);
  drawZoom();
}
document.querySelectorAll("#zoomToggle button").forEach((b) => b.onclick = () => setZoomMetric(b.dataset.m));
function openZoom(name, runs) {
  zoomed = { name, runs };
  const z = $("zoom");
  const tok = runs.reduce((x, r) => x + r.tok, 0), cost = runs.reduce((x, r) => x + r.cost, 0);
  $("zoomTitle").textContent = name;
  $("zoomSub").textContent = `${runs.length} 次 · 平均 ${short(tok / runs.length)} token · 平均 ${usd(cost / runs.length)} · 總計 ${usd(cost)}`;
  $("zoomTable").innerHTML = "<thead><tr><th>時間（UTC）</th><th>model</th><th>effort</th><th>回應數</th>" +
    PARTS.map((p) => `<th>${p.label}</th>`).join("") + "<th>token 合計</th><th>cost</th><th>執行時間</th></tr></thead><tbody>" +
    runs.map((r) => `<tr><td>${r.time.replace("T", " ")}</td><td>${esc(r.model)}</td><td>${esc(r.effort)}</td><td>${r.calls}</td>` +
      PARTS.map((p) => `<td>${num(r[TOKEN_KEYS[p.key]])}</td>`).join("") +
      `<td>${num(r.tok)}</td><td>${usd(r.cost)}</td><td>${durCell(r)}</td></tr>`).join("") + "</tbody>";
  z.hidden = false;
  document.body.style.overflow = "hidden";
  setZoomMetric(zoomMetric);
  $("zoomClose").focus();
}
function drawZoom() {
  if (!zoomed) return;
  const h = Math.max(260, Math.min(440, innerHeight * 0.5));
  drawSkillChart($("zoomSvg"), zoomed.name, zoomed.runs, h, zoomMetric);
}
function closeZoom() {
  zoomed = null;
  $("zoom").hidden = true;
  document.body.style.overflow = "";
  hideTip();
}
$("zoomClose").onclick = closeZoom;
$("zoom").onclick = (e) => { if (e.target.id === "zoom") closeZoom(); };
addEventListener("keydown", (e) => { if (e.key === "Escape" && zoomed) closeZoom(); });

// ---------- token 和費用的關係（Opus 5.5 / Sonnet 5.5）----------
function renderRelation() {
  const MODELS = [["claude-opus-5-5", "Opus 5.5"], ["claude-sonnet-5-5", "Sonnet 5.5"]];
  const ROWS = [
    ["cache_read", "cache 讀取"], ["input", "input"],
    ["cache_write_5m", "cache 寫入（5 分鐘）"], ["cache_write_1h", "cache 寫入（1 小時）"], ["output", "output"],
  ];
  const price = (v) => "$" + (+v.toFixed(3));
  $("priceTable").innerHTML = "<thead><tr><th>每百萬 token</th>" +
    MODELS.map(([, l]) => `<th>${l}</th>`).join("") + "</tr></thead><tbody>" +
    ROWS.map(([k, l]) => `<tr><td>${l}</td>` + MODELS.map(([m]) => {
      const p = PRICING[m];
      if (!p) return "<td>–</td>";
      return `<td>${price(p[k])} <span class="x">${+(p[k] / p.input).toFixed(2)}x</span></td>`;
    }).join("") + "</tr>").join("") + "</tbody>";

  // 依 model 加總 token 與費用，比較「token 佔比」和「費用佔比」
  const KEY = { read: "read", write: "write", out: "out", in: "in" };
  const box = $("relModels");
  box.innerHTML = MODELS.map(([m, label]) => {
    const runs = RUNS.filter((r) => "claude-" + r.model === m);
    const tok = {}, cost = {};
    for (const p of PARTS) {
      tok[p.key] = runs.reduce((x, r) => x + r[KEY[p.key]], 0);
      cost[p.key] = runs.reduce((x, r) => x + r.cost_parts[p.key], 0);
    }
    const T = Object.values(tok).reduce((a, b) => a + b, 0), C = Object.values(cost).reduce((a, b) => a + b, 0);
    if (!runs.length || !T) return `<div class="rel-model"><h3>${label}</h3><div class="rel-empty">目前沒有用 ${label} 執行的紀錄</div></div>`;
    const bar = (vals, total, fmt) => `<div class="rel-bar">` + PARTS.filter((p) => vals[p.key] / total >= 0.002).map((p) => {
      const pct = (vals[p.key] / total) * 100;
      return `<div style="flex:${pct} 0 0;background:${p.color}" data-tip="${label}|${p.label}|${fmt(p.key)}|${pct.toFixed(1)}%">` +
        (pct >= 9 ? pct.toFixed(0) + "%" : "") + "</div>";
    }).join("") + "</div>";
    return `<div class="rel-model"><h3>${label}</h3>` +
      `<div class="muted">${runs.length} 次 · ${short(T)} token · ${usd(C)} · 平均每百萬 token ${usd((C / T) * 1e6)}</div>` +
      `<div class="rel-row"><span>token 佔比</span>${bar(tok, T, (k) => num(tok[k]) + " token")}</div>` +
      `<div class="rel-row"><span>cost 佔比</span>${bar(cost, C, (k) => usd(cost[k]))}</div></div>`;
  }).join("");
  box.querySelectorAll("[data-tip]").forEach((d) => {
    const [m, part, val, pct] = d.dataset.tip.split("|");
    d.addEventListener("mousemove", (ev) => showTip(ev, `${m} · ${part}`, [["數量", val], ["佔比", pct]]));
    d.addEventListener("mouseleave", hideTip);
  });
}

function drawCharts() { drawBySkill(); drawMultiples(); drawByRun(); drawZoom(); }
let resizeTimer;
addEventListener("resize", () => { clearTimeout(resizeTimer); resizeTimer = setTimeout(drawCharts, 100); });

// ---------- 各 skill 平均花費 ----------
function renderAvg() {
  const rows = Object.values(bySkill).map((a) => {
    const ok = RUNS.filter((r) => r.skill === a.skill && r.calls > 0);
    const costs = ok.map((r) => r.cost);
    const n = ok.length || 1;
    return {
      skill: a.skill, runs: a.n, ok: ok.length,
      avg: costs.reduce((x, y) => x + y, 0) / n,
      min: costs.length ? Math.min(...costs) : 0,
      max: costs.length ? Math.max(...costs) : 0,
      calls: ok.reduce((x, r) => x + r.calls, 0) / n,
      tokens: ok.reduce((x, r) => x + r.in + r.write + r.read + r.out, 0) / n,
      dur: ok.some((r) => r.dur_active != null)
        ? ok.reduce((x, r) => x + (r.dur_active || 0), 0) / ok.filter((r) => r.dur_active != null).length : null,
      total: a.cost,
    };
  });
  const maxAvg = Math.max(...rows.map((r) => r.avg), 0.001);
  const cols = [
    ["skill", "skill", (r) => esc(r.skill)],
    ["runs", "次數", (r) => r.ok === r.runs ? r.runs : `${r.ok} / ${r.runs}`],
    ["avg", "平均每次", (r) => `<div class="avgbar"><span style="width:${(r.avg / maxAvg) * 110}px"></span>${usd(r.avg)}</div>`],
    ["min", "最低", (r) => usd(r.min)],
    ["max", "最高", (r) => usd(r.max)],
    ["calls", "平均回應數", (r) => r.calls.toFixed(1)],
    ["tokens", "平均 token", (r) => short(r.tokens)],
    ["dur", "平均執行時間", (r) => fmtDur(r.dur)],
    ["total", "總 cost", (r) => usd(r.total)],
  ];
  let sortKey = "avg", asc = false;
  const t = $("avg");
  function render() {
    const sorted = [...rows].sort((a, b) => {
      const va = a[sortKey], vb = b[sortKey];
      return (typeof va === "string" ? va.localeCompare(vb) : va - vb) * (asc ? 1 : -1);
    });
    t.innerHTML = "<thead><tr>" + cols.map(([k, l]) =>
      `<th data-k="${k}">${l}${k === sortKey ? (asc ? " ▲" : " ▼") : ""}</th>`).join("") + "</tr></thead><tbody>" +
      sorted.map((r) => "<tr>" + cols.map(([k, , f]) =>
        `<td>${r.ok === 0 && !["skill", "runs", "total"].includes(k) ? "–" : f(r)}</td>`).join("") + "</tr>").join("") + "</tbody>";
    t.querySelectorAll("th").forEach((th) => th.onclick = () => {
      const k = th.dataset.k; asc = k === sortKey ? !asc : k === "skill"; sortKey = k; render();
    });
  }
  render();
}

// ---------- table ----------
function renderRunsTable() {
  const cols = [
    ["workspace", "workspace", (r) => esc(r.workspace || "")],
    ["time", "時間（UTC）", (r) => r.time.replace("T", " ")],
    ["skill", "skill", (r) => esc(r.skill)],
    ["session", "session", (r) => r.session + (r.deleted ? ' <span class="badge" title="session 已刪除，資料來自保存的執行檔">已刪除</span>' : "") +
      (r.title || r.created ? `<div class="sess-meta" title="session 建立於 ${esc(r.created.replace("T", " ").slice(0, 16))}（本機時間）">` +
        [r.title, r.created ? r.created.slice(5, 10) + " 建立" : ""].filter(Boolean).map(esc).join(" · ") + "</div>" : "")],
    ["model", "model", (r) => esc(r.model)],
    ["effort", "effort", (r) => esc(r.effort)],
    ["calls", "回應數", (r) => r.calls],
    ["in", "input", (r) => num(r.in)],
    ["write", "cache 寫入", (r) => num(r.write)],
    ["read", "cache 讀取", (r) => num(r.read)],
    ["out", "output", (r) => num(r.out)],
    ["cost", "cost", (r) => usd(r.cost)],
    ["dur_active", "執行時間", durCell],
  ];
  let sortKey = "time", asc = false;
  const t = $("runs");
  function render() {
    const rows = [...RUNS].sort((a, b) => {
      const va = a[sortKey], vb = b[sortKey];
      return (typeof va === "string" ? va.localeCompare(vb) : va - vb) * (asc ? 1 : -1);
    });
    t.innerHTML = "<thead><tr>" + cols.map(([k, l]) =>
      `<th data-k="${k}">${l}${k === sortKey ? (asc ? " ▲" : " ▼") : ""}</th>`).join("") + "</tr></thead><tbody>" +
      rows.map((r) => "<tr>" + cols.map(([, , f]) => `<td>${f(r)}</td>`).join("") + "</tr>").join("") + "</tbody>";
    t.querySelectorAll("th").forEach((th) => th.onclick = () => {
      const k = th.dataset.k; asc = k === sortKey ? !asc : ["workspace", "skill", "session", "model", "effort"].includes(k); sortKey = k; render();
    });
  }
  render();
}

// ---------- workspace 切換 ----------
function applyWorkspace(ws) {
  if (ws !== "All" && !WORKSPACES.includes(ws)) ws = "All";
  RUNS = ws === "All" ? ALL_RUNS : ALL_RUNS.filter((r) => r.workspace === ws);
  document.querySelectorAll("#wsToggle button").forEach((b) => b.setAttribute("aria-pressed", b.dataset.ws === ws));
  if (zoomed) closeZoom();
  aggregate(); renderKpis(); renderRelation(); renderAvg(); renderRunsTable(); drawCharts();
  try { localStorage.setItem("skill-dashboard-ws", ws); } catch (e) {}
  history.replaceState(null, "", "#" + encodeURIComponent(ws));
}
const WS_OPTIONS = WORKSPACES.length > 1 ? [...WORKSPACES, "All"] : WORKSPACES;
$("wsToggle").innerHTML = WS_OPTIONS.map((w) => {
  const n = w === "All" ? ALL_RUNS.length : ALL_RUNS.filter((r) => r.workspace === w).length;
  return `<button data-ws="${esc(w)}" aria-pressed="false" title="${n} 次執行">${esc(w)}</button>`;
}).join("");
document.querySelectorAll("#wsToggle button").forEach((b) => b.onclick = () => applyWorkspace(b.dataset.ws));
$("multiSub").textContent = `每個 skill 一張圖；X 軸是執行時間（UTC），${MULTI_SUB.token}（各圖刻度不同）；點一張圖可放大`;
let initialWs = decodeURIComponent(location.hash.slice(1));
if (!initialWs) { try { initialWs = localStorage.getItem("skill-dashboard-ws") || ""; } catch (e) {} }
applyWorkspace(initialWs || WS_OPTIONS[0]);

</script>
</body>
</html>
"""


def to_page_runs(snapshot):
    """YAML 的欄位名稱轉成頁面 JS 使用的精簡欄位。"""
    runs = []
    for r in snapshot.get("runs") or []:
        t, c = r["tokens"], r["cost_usd"]
        runs.append({
            "workspace": r.get("workspace", snapshot.get("project", "")),
            "deleted": bool(r.get("session_deleted")),
            "created": str(r.get("session_created") or ""), "title": r.get("session_title") or "",
            "time": str(r["time"]), "skill": r["skill"], "session": r["session"], "via": r.get("via", ""),
            "model": r.get("model", "–"), "effort": r.get("effort", "–"), "calls": r["calls"],
            "in": t["input"], "write": t["cache_write"], "read": t["cache_read"], "out": t["output"],
            **({"dur_total": tm["total"], "dur_wait": tm["waiting"], "dur_active": tm["active"]}
               if (tm := (r.get("timing") or {}).get("seconds")) else
               {"dur_total": None, "dur_wait": None, "dur_active": None}),
            "cost": c["total"],
            "cost_parts": {"in": c["input"], "write": c["cache_write"], "read": c["cache_read"], "out": c["output"]},
        })
    return runs


def render(snapshot):
    generated = str(snapshot["generated_at"]).replace("T", " ")[:16]
    subtitle = f"資料日期 {snapshot['date']} · 產生於 {generated}"
    data = json.dumps(to_page_runs(snapshot), ensure_ascii=False).replace("</", "<\\/")
    pricing = json.dumps(snapshot.get("pricing_usd_per_mtok") or {})
    return (TEMPLATE.replace("__SUBTITLE__", html.escape(subtitle))
            .replace("__PRICING__", pricing)
            .replace("__WORKSPACES__", json.dumps(snapshot.get("workspaces") or [snapshot.get("project", "")]))
            .replace("__DATA__", data))


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", nargs="?", help="只分析這個紀錄資料夾或 .jsonl 檔（預設：所有 workspace）")
    ap.add_argument("--from", dest="from_yaml", help="從既有的 YAML 產生，不重新掃描紀錄")
    args = ap.parse_args()

    # 1. 紀錄 → 每次執行檔 → 每日快照
    if args.from_yaml:
        yaml_path = args.from_yaml
    else:
        yaml_path, _, written = update_database(args.target)
        if not args.target:
            print(f"1. 執行檔    → 更新 {written} 個（{RUN_DIR}）")
        print(f"1. 每日快照  → {yaml_path}")

    # 2、3. YAML → HTML（最新版 + 歷史版）
    with open(yaml_path, encoding="utf-8") as f:
        snapshot = yaml.safe_load(f)
    page = render(snapshot)
    hist_path = os.path.join(HIST_DIR, f"skill-dashboard-{snapshot['date']}.html")
    write(DASH_PATH, page)
    write(hist_path, page)
    print(f"2. dashboard → {DASH_PATH}")
    print(f"3. 歷史紀錄  → {hist_path}")
    deleted = snapshot["summary"].get("from_deleted_sessions", 0)
    print(f"共 {len(snapshot.get('runs') or [])} 筆執行紀錄（{deleted} 筆來自已刪除的 session），"
          f"估算 ${snapshot['summary']['cost_usd']:.2f}")


if __name__ == "__main__":
    main()
