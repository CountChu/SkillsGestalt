#!/usr/bin/env python3
"""Claude Code hook（Stop / SessionEnd）：把剛回完話的 session 的 skill 執行存進 database/skill-tokens/。

由 ~/.claude/settings.json 的 hook 呼叫，stdin 是 hook 的 JSON（含 transcript_path）。
只讀這一個 session 的紀錄檔，不產生每日快照和 dashboard。
不屬於 WORKSPACES 的 session 直接略過。無論成功失敗都不輸出、一律 exit 0，
所以不會進入對話、不花 token；錯誤寫到 ~/.claude/logs/skill-tokens-hook.log。
"""
import fcntl
import json
import os
import sys
import traceback
from datetime import datetime

LOG_DIR = os.path.expanduser("~/.claude/logs")
LOG = os.path.join(LOG_DIR, "skill-tokens-hook.log")
LOCK = os.path.join(LOG_DIR, "skill-tokens-hook.lock")


def main():
    payload = json.load(sys.stdin)
    transcript = payload.get("transcript_path") or ""
    if not transcript.endswith(".jsonl") or not os.path.exists(transcript):
        return

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import skill_tokens as st

    workspace = st.workspace_of(transcript)
    if workspace is None:
        return
    runs = st.collect_runs(transcript)
    if not runs:
        return
    for r in runs:
        r["workspace"] = workspace

    os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOCK, "w") as lock:  # 多個 session 同時觸發時排隊寫入
        fcntl.flock(lock, fcntl.LOCK_EX)
        st.sync_run_files(runs)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        try:
            os.makedirs(LOG_DIR, exist_ok=True)
            with open(LOG, "a", encoding="utf-8") as f:
                f.write(f"--- {datetime.now():%Y-%m-%d %H:%M:%S}\n{traceback.format_exc()}\n")
        except Exception:
            pass
    sys.exit(0)
