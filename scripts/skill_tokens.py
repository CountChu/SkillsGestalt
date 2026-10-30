#!/usr/bin/env python3
"""統計 Claude Code session 紀錄中，每次執行 skill 所花的 token 與估算費用。

一次 skill 執行 = 從 skill 被呼叫（/slash 指令或 Skill 工具）開始，
（系統認不得、被當一般訊息送出的 /指令也算，例如放在 .claude/skills 以外的 skill），
到下一則「使用者真正輸入的訊息」或下一次 skill 呼叫為止，期間所有 assistant 回應的 usage 加總。

用法：
  python3 scripts/skill_tokens.py                  # 預設掃描 WORKSPACES 裡所有 workspace 的紀錄
  python3 scripts/skill_tokens.py <資料夾或.jsonl>  # 指定紀錄位置
  python3 scripts/skill_tokens.py --runs           # 另外列出每一次執行的明細
  python3 scripts/skill_tokens.py --yaml           # 更新 database/skill-tokens/ 的每次執行檔，
                                                   # 並存一份 database/skill-tokens-daily/yymmdd.yaml

每次執行檔：database/skill-tokens/{workspace}#{yyyy-mm-dd}#{session 前 8 碼}#{skill}.yaml
  yyyy-mm-dd 是 session 的建立日期（本機時區），skill 的 : 換成 ~。
  同一個 session 多次執行同一個 skill 放在同一檔的 runs 清單。session 紀錄檔還在就用最新數字更新；
  紀錄檔被刪除（或被 Claude Code 自動清除）後，檔案保留不動，只標記 session_deleted: true。
"""
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime

import yaml

# 每百萬 token 美元價格（Anthropic API 定價，2026-10）。
# cache 寫入：5 分鐘 = 1.25x input、1 小時 = 2x input。
PRICES = {
    "claude-opus-5-5": {"in": 4.00, "out": 20.00, "read": 0.20},
    "claude-sonnet-5-5": {"in": 2.00, "out": 10.00, "read": 0.20},
    # 上一代：cache 讀取以標準的 input 0.1 倍估算
    "claude-opus-5": {"in": 5.00, "out": 25.00, "read": 0.50},
    "claude-sonnet-5": {"in": 2.00, "out": 10.00, "read": 0.20},
    "claude-haiku-5-5": {"in": 0.10, "out": 0.50, "read": 0.01},
}

# 內建 slash 指令，不算 skill
BUILTIN_CMDS = {
    "model", "clear", "compact", "config", "cost", "context", "help", "login",
    "logout", "resume", "status", "memory", "permissions", "hooks", "doctor",
    "init", "fast", "effort", "rewind", "exit", "agents", "mcp", "usage",
}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUN_DIR = os.path.join(ROOT, "database", "skill-tokens")          # 每次執行檔
DAILY_DIR = os.path.join(ROOT, "database", "skill-tokens-daily")  # 每日快照

# dashboard 可切換的 workspace：名稱 → 專案資料夾（子資料夾的 session 也算進來）
WORKSPACES = {
    "SkillsGestalt": "~/Library/CloudStorage/Dropbox/2-Areas-I/SkillsGestalt",
    "InvestForge": "~/Library/CloudStorage/Dropbox/2-Areas-I/InvestForge",
}
PROJECTS_DIR = os.path.expanduser("~/.claude/projects")


def transcript_dirs(project_path):
    """專案路徑 → ~/.claude/projects 裡對應的紀錄資料夾（含子資料夾，例如 InvestForge/Inv）。"""
    enc = re.sub(r"[^A-Za-z0-9]", "-", os.path.expanduser(project_path).rstrip("/"))
    return sorted(d for d in glob.glob(os.path.join(PROJECTS_DIR, enc + "*"))
                  if os.path.basename(d) == enc or os.path.basename(d).startswith(enc + "-"))


DEFAULT_DIR = os.path.expanduser(
    "~/.claude/projects/"
    + re.sub(r"[^A-Za-z0-9]", "-", os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
)


def cost_parts(model, u):
    """回傳各部分的美元費用：in / write / read / out。"""
    p = PRICES.get(model)
    if not p:
        return {"in": 0.0, "write": 0.0, "read": 0.0, "out": 0.0}
    cc = u.get("cache_creation") or {}
    w5 = cc.get("ephemeral_5m_input_tokens", 0)
    w1h = cc.get("ephemeral_1h_input_tokens", 0)
    if not cc:
        w5 = u.get("cache_creation_input_tokens", 0)
    return {
        "in": u.get("input_tokens", 0) * p["in"] / 1e6,
        "write": (w5 * 1.25 + w1h * 2) * p["in"] / 1e6,
        "read": u.get("cache_read_input_tokens", 0) * p["read"] / 1e6,
        "out": u.get("output_tokens", 0) * p["out"] / 1e6,
    }


def is_real_prompt(o):
    """使用者真正打的訊息（不是 tool_result、不是系統注入的 meta）。"""
    if o.get("type") != "user" or o.get("isMeta") or o.get("isSidechain"):
        return False
    c = (o.get("message") or {}).get("content")
    if isinstance(c, str):
        return True
    if isinstance(c, list):
        return any(b.get("type") == "text" for b in c) and not any(
            b.get("type") == "tool_result" for b in c
        )
    return False


def scan_file(path, seen, seen_runs, meta):
    """seen / seen_runs / meta 跨檔共用。

    resume 或分支出來的 session 會把原 session 的紀錄複製進來：分支保留原本的 sessionId，
    有些 resume 則改寫成新 session 的 id。所以同一次執行（同一個 key）可能帶著多個 sessionId，
    先全部記在 cands，掃完後由 apply_meta 歸給建立最早的那個（複本一定比原 session 晚建立）。
    meta[sessionId] 收集各 session 的建立時間與標題（原 session 刪除後，只能從複本裡找）。
    """
    runs, cur = [], None
    session_id = os.path.basename(path).split(".")[0]

    def start(name, ts, via, key, sid):
        nonlocal cur
        cur = {"key": key, "skill": name, "session": sid[:8], "session_id": sid,
               "transcript": os.path.join(os.path.dirname(path), sid + ".jsonl"),
               "time": (ts or "")[:16], "via": via,
               # 執行時間（推算）：開始 = 呼叫 skill 的時間；結束 = 這次執行最後一筆回應的時間；
               # 等待 = 選擇題（AskUserQuestion）從提問到你回答的時間。asks / answers 以工具呼叫 id 為鍵，
               # 同一筆在多個複本裡出現也只算一次
               "start_ts": ts, "end_ts": None, "asks": {}, "answers": {},
               "calls": 0, "in": 0, "write": 0, "read": 0, "out": 0, "cost": 0.0,
               "cost_parts": {"in": 0.0, "write": 0.0, "read": 0.0, "out": 0.0},
               "models": Counter(), "efforts": Counter()}
        cur["cands"] = {sid: os.path.dirname(path)}
        # 有些 resume 連紀錄 id 都改寫，但保留原本的時間戳記：同一個 skill、開始時間到毫秒都相同就是同一次執行
        alias = ("@", name, ts)
        if key not in seen_runs and ts and alias in seen_runs:
            seen_runs[key] = seen_runs[alias]
        if key in seen_runs:
            cur = seen_runs[key]
            cur["cands"].setdefault(sid, os.path.dirname(path))
            if ts and (not cur["start_ts"] or ts < cur["start_ts"]):
                cur["start_ts"] = ts
        else:
            seen_runs[key] = cur
            if ts:
                seen_runs[alias] = cur
            runs.append(cur)

    for line in open(path, encoding="utf-8"):
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue
        sid = o.get("sessionId") or session_id
        # session 建立時間：屬於該 session id 的最早時間（檔案內順序不一定照時間）
        ts = o.get("timestamp")
        if ts:
            md = meta.setdefault(sid, {})
            md["created"] = min(md.get("created") or ts, ts)
        if o.get("type") == "custom-title" and o.get("customTitle"):
            # 自己檔案裡的標題最新；複本裡帶過來的是舊標題，只在找不到自己的時候使用
            meta.setdefault(sid, {})["title_own" if sid == session_id else "title"] = o["customTitle"]
        m = o.get("message") or {}
        content = m.get("content")

        if o.get("type") == "user" and not o.get("isMeta"):
            text = content if isinstance(content, str) else " ".join(
                b.get("text", "") for b in content or [] if isinstance(b, dict))
            cmd = re.search(r"<command-name>/?(.*?)</command-name>", text)
            if cmd:
                name = cmd.group(1).strip()
                if name in BUILTIN_CMDS:
                    cur = None
                else:
                    start(name, o.get("timestamp"), "/", o.get("uuid"), sid)
                continue
            if is_real_prompt(o):
                slash = re.match(r"\s*/([\w:.-]+)(?=\s|$)", text)  # 排除 /Users/... 這類路徑
                if slash and slash.group(1) not in BUILTIN_CMDS:
                    start(slash.group(1), o.get("timestamp"), "/?", o.get("uuid"), sid)
                else:
                    cur = None
                continue

        if cur is not None and ts and isinstance(content, list):
            for b in content:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "tool_use" and b.get("name") == "AskUserQuestion":
                    cur["asks"][b.get("id")] = min(cur["asks"].get(b.get("id")) or ts, ts)
                elif b.get("type") == "tool_result" and b.get("tool_use_id") in cur["asks"]:
                    cur["answers"][b["tool_use_id"]] = max(cur["answers"].get(b["tool_use_id"]) or ts, ts)

        if o.get("type") != "assistant":
            continue
        # 結束時間只看模型真的回答的紀錄；resume 時 Claude Code 自動產生的 <synthetic> 回應不算
        if cur is not None and ts and m.get("model") != "<synthetic>":
            cur["end_ts"] = max(cur["end_ts"] or ts, ts)
        u, mid = m.get("usage"), m.get("id")
        # 同一則回應會拆成多行，usage 重複，只算一次
        if u and mid not in seen and cur is not None:
            seen.add(mid)
            cur["calls"] += 1
            if m.get("model") != "<synthetic>":  # Claude Code 自己產生的訊息，不是模型呼叫
                cur["models"][m.get("model") or "?"] += 1
                cur["efforts"][o.get("effort") or "?"] += 1
            cur["in"] += u.get("input_tokens", 0)
            cur["write"] += u.get("cache_creation_input_tokens", 0)
            cur["read"] += u.get("cache_read_input_tokens", 0)
            cur["out"] += u.get("output_tokens", 0)
            for k, v in cost_parts(m.get("model"), u).items():
                cur["cost_parts"][k] += v
                cur["cost"] += v
        elif mid:
            seen.add(mid)
        # Skill 工具呼叫：之後的回應算到這個 skill
        for b in content if isinstance(content, list) else []:
            if b.get("type") == "tool_use" and b.get("name") == "Skill":
                start(b.get("input", {}).get("skill", "?"), o.get("timestamp"), "tool", b.get("id"), sid)
    for r in runs:
        r["model"] = mix(r.pop("models"), short_model)
        r["effort"] = mix(r.pop("efforts"))
    return runs


def apply_meta(runs, meta):
    """決定每次執行的歸屬 session（候選中建立最早的），並填入建立時間與標題。"""
    for r in runs:
        cands = r.get("cands") or {r["session_id"]: os.path.dirname(r["transcript"])}
        sid = min(cands, key=lambda c: (meta.get(c, {}).get("created") or "9999", c))
        r["session_id"], r["session"] = sid, sid[:8]
        r["transcript"] = os.path.join(cands[sid], sid + ".jsonl")
        md = meta.get(sid, {})
        r["session_created"] = to_local(md.get("created"))
        r["session_title"] = md.get("title_own") or md.get("title") or ""
        r["title_own"] = bool(md.get("title_own"))
        r["timing"] = timing_of(r)
    return runs


def _secs(a, b):
    return (datetime.fromisoformat(b.replace("Z", "+00:00")) -
            datetime.fromisoformat(a.replace("Z", "+00:00"))).total_seconds()


def timing_of(r):
    """推算的執行時間；沒有任何回應時回傳 None。"""
    if not r.get("start_ts") or not r.get("end_ts"):
        return None
    total = max(_secs(r["start_ts"], r["end_ts"]), 0)
    wait = sum(max(_secs(r["asks"][k], v), 0) for k, v in r["answers"].items() if k in r["asks"])
    wait = min(wait, total)
    return {"started": to_local(r["start_ts"]), "ended": to_local(r["end_ts"]),
            "seconds": {"total": round(total), "waiting": round(wait), "active": round(total - wait)}}


def to_local(ts):
    """UTC 時間字串 → 本機時區 ISO 字串（到秒）。"""
    if not ts:
        return ""
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    return dt.astimezone().isoformat(timespec="seconds")


def short_model(name):
    return name.removeprefix("claude-")


def mix(counter, f=str):
    """單一值直接顯示；混用時依次數排序並標出比例，例如 opus-5-5 ×20 / sonnet-5-5 ×3。"""
    if not counter:
        return "–"
    items = counter.most_common()
    if len(items) == 1:
        return f(items[0][0])
    return " / ".join(f"{f(k)} ×{v}" for k, v in items)


def collect_runs(target=DEFAULT_DIR, seen=None, seen_runs=None, meta=None):
    """掃描資料夾（或單一 .jsonl）並回傳去重後的 skill 執行清單。"""
    files = [target] if target.endswith(".jsonl") else glob.glob(
        os.path.join(target, "**", "*.jsonl"), recursive=True)
    if not files:
        sys.exit(f"找不到紀錄檔：{target}")
    seen = set() if seen is None else seen
    seen_runs = {} if seen_runs is None else seen_runs
    meta = {} if meta is None else meta
    runs = [r for f in sorted(files, key=os.path.getmtime) for r in scan_file(f, seen, seen_runs, meta)]
    return apply_meta(runs, meta)


def workspace_of(transcript_path, workspaces=WORKSPACES):
    """紀錄檔 → 所屬 workspace 名稱；不屬於任何 workspace 回傳 None。"""
    d = os.path.dirname(os.path.abspath(transcript_path))
    for name, path in workspaces.items():
        if any(os.path.abspath(t) == d for t in transcript_dirs(path)):
            return name
    return None


def collect_workspaces(workspaces=WORKSPACES):
    """掃描所有 workspace，每筆執行標上 workspace 名稱。"""
    runs, seen, seen_runs, meta = [], set(), {}, {}
    for name, path in workspaces.items():
        for d in transcript_dirs(path):
            for r in collect_runs(d, seen, seen_runs, meta):
                r["workspace"] = name
                runs.append(r)
    return apply_meta(runs, meta)


def record_of(r):
    """掃描結果 → 存檔用的格式（每次執行一筆）。"""
    cp = r["cost_parts"]
    return {
        "key": r["key"],
        "time": r["time"],
        "via": r["via"],
        "model": r["model"],
        "effort": r["effort"],
        "calls": r["calls"],
        **({"timing": r["timing"]} if r.get("timing") else {}),
        "tokens": {"input": r["in"], "cache_write": r["write"], "cache_read": r["read"], "output": r["out"]},
        "cost_usd": {"input": round(cp["in"], 6), "cache_write": round(cp["write"], 6),
                     "cache_read": round(cp["read"], 6), "output": round(cp["out"], 6),
                     "total": round(r["cost"], 6)},
    }


def run_file_name(workspace, created, session, skill):
    """created 是 session 建立時間（本機時區 ISO 字串），只取日期。"""
    return f"{workspace}#{created[:10] or 'unknown'}#{session}#{re.sub(r'[:/]', '~', skill)}.yaml"


def _file_date(data):
    """檔名用的日期：session 建立日期；舊資料沒有時退而用最早一次執行的日期。"""
    if data.get("session_created"):
        return data["session_created"]
    times = [run["time"] for run in data.get("runs") or [] if run.get("time")]
    return to_local(min(times) + ":00Z") if times else ""


def _home(path):
    return path.replace(os.path.expanduser("~"), "~", 1)


def _dump(data):
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=120)


def sync_run_files(runs, directory=RUN_DIR, prune=False):
    """把掃描結果寫進每次執行檔，回傳 (所有執行 record, 寫入檔案數)。

    - 每個檔案對應一組 (workspace, session, skill)；同一次執行（依 key）只會存在一個檔案。
    - 之前歸錯 session 的執行會搬到正確的檔案，搬空的舊檔刪除。
    - 檔案裡有、但這次沒掃到的執行保留不動（session 被刪除後資料仍在）。
    - session 紀錄檔不存在時標記 session_deleted: true。
    - 改寫過紀錄 id 的複本：以 (skill, 開始時間) 對應回已存的那一筆。
    - prune=True（完整掃描）：session 紀錄還在、但這次掃描已認定為複本的舊紀錄會被清掉；
      已刪除 session 的資料一律不動。hook 只讀單一 session，不做清除。
    """
    os.makedirs(directory, exist_ok=True)
    files, ident_index, key_index, alias_index = {}, {}, {}, {}
    for path in glob.glob(os.path.join(directory, "*#*.yaml")):
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        files[path] = data
        ident_index.setdefault((data.get("workspace"), data.get("session_id"), data.get("skill")), path)
        for run in data.get("runs") or []:
            key_index[run.get("key")] = path
            started = (run.get("timing") or {}).get("started")
            if started:
                alias_index.setdefault((data.get("skill"), started), run.get("key"))

    fresh, scanned = defaultdict(list), set()
    for r in runs:
        started = (r.get("timing") or {}).get("started")
        alias_key = alias_index.get((r["skill"], started)) if started else None
        if r["key"] not in key_index and alias_key in key_index:
            r = {**r, "key": alias_key}
        scanned.add(r["key"])
        old_path = key_index.get(r["key"])
        if old_path:
            # 已經存在於其他 session 的檔案：只有這次找到建立更早的 session 才搬（hook 只讀單一檔案時，
            # 看到的可能是改寫過 id 的複本，不能據此把正確的歸屬搬走）
            old_created = files[old_path].get("session_created") or ""
            if not r["session_created"] or (old_created and old_created <= r["session_created"]):
                # 留在原檔：複本的建立時間與標題不屬於那個 session，不帶進去
                r = {**r, "workspace": files[old_path].get("workspace"), "session_id": files[old_path].get("session_id"),
                     "skill": files[old_path].get("skill"), "session_created": "", "session_title": ""}
        ident = (r["workspace"], r["session_id"], r["skill"])
        path = ident_index.get(ident)
        if path is None:
            path = os.path.join(directory, run_file_name(r["workspace"], r["session_created"], r["session"], r["skill"]))
            files[path] = {"workspace": r["workspace"], "session": r["session"], "session_id": r["session_id"],
                           "session_created": r["session_created"], "session_title": r["session_title"],
                           "skill": r["skill"], "transcript": _home(r["transcript"]), "session_deleted": False,
                           "runs": []}
            ident_index[ident] = path
        data = files[path]
        if old_path and old_path != path:  # 之前歸錯 session：連同已存的數字一起搬過來
            old_runs = files[old_path].get("runs") or []
            data.setdefault("runs", []).extend(x for x in old_runs if x.get("key") == r["key"])
            files[old_path]["runs"] = [x for x in old_runs if x.get("key") != r["key"]]
            key_index[r["key"]] = path
        # 建立時間取最早的；標題以 session 自己檔案裡的為準（標題可能被改名）
        if r["session_created"]:
            data["session_created"] = min(filter(None, [data.get("session_created"), r["session_created"]]))
        if r["session_title"] and (r.get("title_own") or not data.get("session_title")):
            data["session_title"] = r["session_title"]
        fresh[path].append(record_of(r))

    written, records = 0, []
    for path, data in sorted(files.items()):
        before = _dump(data) if os.path.exists(path) else None
        # 欄位順序固定，舊格式的檔案補上新欄位
        data = {k: data.get(k, "") for k in ("workspace", "session", "session_id", "session_created",
                                             "session_title", "skill", "transcript")} | \
               {"session_deleted": data.get("session_deleted", False), "runs": data.get("runs") or []}
        if path in fresh:
            merged = {}
            for run in data["runs"]:
                old = merged.get(run["key"])
                if old is None or run.get("calls", 0) >= old.get("calls", 0):
                    merged[run["key"]] = run
            for run in fresh[path]:
                old = merged.get(run["key"])
                # resume/分支出來的 session 可能只複製了部分紀錄：數字變少時保留原本的
                if old is None or run["calls"] >= old.get("calls", 0):
                    merged[run["key"]] = run
            data["runs"] = sorted(merged.values(), key=lambda run: run["time"])
        if prune and os.path.exists(os.path.expanduser(data.get("transcript", ""))):
            data["runs"] = [run for run in data["runs"] if run.get("key") in scanned]
        if not data["runs"]:  # 執行都搬走或清掉了：刪除空檔
            if os.path.exists(path):
                os.remove(path)
                written += 1
            continue
        data["session_deleted"] = not os.path.exists(os.path.expanduser(data.get("transcript", "")))
        text = _dump(data)
        target = os.path.join(directory, run_file_name(data["workspace"], _file_date(data), data["session"], data["skill"]))
        if target != path:  # 舊檔名或建立日期改變：改成新檔名
            if os.path.exists(path):
                os.remove(path)
            path, before = target, None
        if text != before:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            written += 1
        for run in data["runs"]:
            records.append({"workspace": data["workspace"], "session": data["session"], "skill": data["skill"],
                            "session_created": data["session_created"], "session_title": data["session_title"],
                            "session_deleted": data["session_deleted"], **run})
    return records, written


def build_snapshot(records, target=None, now=None):
    """把執行 record 整理成每日快照。target 為 None 表示所有 workspace。"""
    now = now or datetime.now()
    if target is None:
        project, source = "All", dict(WORKSPACES)
    else:
        project, source = os.path.basename(target.rstrip("/")), _home(target)
    out = [{"workspace": r["workspace"], "time": r["time"], "skill": r["skill"], "session": r["session"],
            "session_created": r.get("session_created", ""), "session_title": r.get("session_title", ""),
            "session_deleted": r.get("session_deleted", False),
            **{k: r[k] for k in ("via", "model", "effort", "calls", "tokens", "cost_usd")},
            **({"timing": r["timing"]} if r.get("timing") else {})}
           for r in sorted(records, key=lambda r: r["time"])]
    workspaces = list(WORKSPACES) if target is None else [project]
    return {
        "date": now.strftime("%y%m%d"),
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%S"),
        "project": project,
        "source": source,
        "workspaces": workspaces,
        "pricing_usd_per_mtok": {m: {"input": p["in"], "output": p["out"], "cache_read": p["read"],
                                     "cache_write_5m": p["in"] * 1.25, "cache_write_1h": p["in"] * 2}
                                 for m, p in PRICES.items()},
        "summary": {
            "runs": len(out),
            "cost_usd": round(sum(r["cost_usd"]["total"] for r in out), 6),
            "from_deleted_sessions": sum(1 for r in out if r["session_deleted"]),
            "by_workspace": {w: {"runs": sum(1 for r in out if r["workspace"] == w),
                                 "cost_usd": round(sum(r["cost_usd"]["total"] for r in out if r["workspace"] == w), 6)}
                             for w in workspaces},
        },
        "runs": out,
    }


def update_database(target=None):
    """掃描 → 更新每次執行檔 → 寫每日快照。回傳 (快照路徑, 快照, 寫入的執行檔數)。

    指定 target（單一資料夾或 .jsonl）時只寫每日快照，不動每次執行檔。
    """
    if target:
        name = os.path.basename(target.rstrip("/"))
        records = [{"workspace": name, "session": r["session"], "skill": r["skill"],
                    "session_created": r["session_created"], "session_title": r["session_title"], **record_of(r)}
                   for r in collect_runs(target)]
        written = 0
    else:
        records, written = sync_run_files(collect_workspaces(), prune=True)
    snapshot = build_snapshot(records, target)
    return write_yaml(snapshot), snapshot, written


def write_yaml(snapshot, directory=DAILY_DIR):
    """寫入 <directory>/yymmdd.yaml（同一天重跑會覆寫），回傳路徑。"""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, f"{snapshot['date']}.yaml")
    with open(path, "w", encoding="utf-8") as f:
        f.write(_dump(snapshot))
    return path


def fmt(n):
    return f"{n:,}"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    target = args[0] if args else None
    runs = collect_runs(target) if target else collect_workspaces()
    if not runs:
        print("沒有找到任何 skill 執行紀錄。")
        return

    if "--yaml" in sys.argv:
        path, snap, written = update_database(target)
        if not target:
            print(f"每次執行檔：更新 {written} 個 → {RUN_DIR}")
        print(f"每日快照：{snap['summary']['runs']} 筆執行紀錄 → {path}")
        return

    if "--runs" in sys.argv:
        print(f"{'workspace':<15}{'時間':<17}{'session':<10}{'skill':<34}{'model':<16}{'effort':<9}{'回應數':>6}{'input':>9}"
              f"{'cache寫':>11}{'cache讀':>13}{'output':>9}{'費用$':>9}")
        for r in sorted(runs, key=lambda r: r["time"]):
            print(f"{r.get('workspace', ''):<15}{r['time']:<17}{r['session']:<10}{r['skill'][:33]:<34}{r['model']:<16}{r['effort']:<9}{r['calls']:>6}"
                  f"{fmt(r['in']):>9}{fmt(r['write']):>11}{fmt(r['read']):>13}"
                  f"{fmt(r['out']):>9}{r['cost']:>9.3f}")
        print()

    agg = defaultdict(lambda: defaultdict(float))
    for r in runs:
        a = agg[r["skill"]]
        a["n"] += 1
        for k in ("calls", "in", "write", "read", "out", "cost"):
            a[k] += r[k]

    print(f"{'skill':<34}{'次數':>5}{'input':>10}{'cache寫':>12}{'cache讀':>14}"
          f"{'output':>10}{'總費用$':>10}{'平均$/次':>10}")
    total = defaultdict(float)
    for name, a in sorted(agg.items(), key=lambda kv: -kv[1]["cost"]):
        print(f"{name[:33]:<34}{int(a['n']):>5}{fmt(int(a['in'])):>10}{fmt(int(a['write'])):>12}"
              f"{fmt(int(a['read'])):>14}{fmt(int(a['out'])):>10}{a['cost']:>10.3f}"
              f"{a['cost'] / a['n']:>10.3f}")
        for k, v in a.items():
            total[k] += v
    print("-" * 104)
    print(f"{'合計':<32}{int(total['n']):>5}{fmt(int(total['in'])):>10}{fmt(int(total['write'])):>12}"
          f"{fmt(int(total['read'])):>14}{fmt(int(total['out'])):>10}{total['cost']:>10.3f}")


if __name__ == "__main__":
    main()
