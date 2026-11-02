"""Build the interactive HTML dependency graph for a check-wiki-doc architecture document.

Reads four things from the architecture document:
  - 〈文件依賴關係表〉: managed documents, their 階層, and which dependencies are （私有）.
  - 〈文件依賴狀態表〉: one row per edge with its 術語數 / 狀態 / 備註.
  - 〈文件依賴圖〉: the mermaid code itself — the HTML draws exactly this graph — and the
    tier legend beside it.

Then, for every edge, collects the borrowed terms from the upper document's
第 2 節〈使用術語〉 — a row belongs to the edge named by `經由`, or by `出處` when
`經由` is empty — and fills assets/dependency-graph.html with that data.

The rules this script implements live in references/dependency-graph.md.

Usage:
    python3 scripts/build_dependency_graph.py --arch <架構文件.md> --root <wikiRootDir> [--out <file.html>]

The default output is `{架構文件名}-文件依賴圖.html` next to the architecture document.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import pathlib
import re
import sys

SKILL_DIR = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "assets" / "dependency-graph.html"
DATA_PLACEHOLDER = "/*__GRAPH_DATA__*/null"
TITLE_PLACEHOLDER = "__TITLE__"

LINK_NAME = re.compile(r"\[\[([^\]|#]+)")
UNMANAGED_SUFFIX = re.compile(r"（未納管）\s*$")
ARROW = r"(==>|-->|-\.->)"


def warn(msg: str) -> None:
    print(f"WARNING: {msg}", file=sys.stderr)


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def sections(text: str) -> dict[str, str]:
    """Split a Markdown document into {`## ` heading: body}."""
    out: dict[str, str] = {}
    for chunk in re.split(r"^## ", text, flags=re.M)[1:]:
        heading, _, body = chunk.partition("\n")
        out[heading.strip()] = body
    return out


def find_section(secs: dict[str, str], keyword: str) -> str | None:
    for heading, body in secs.items():
        if keyword in heading:
            return body
    return None


def table_rows(body: str) -> list[list[str]]:
    """Data rows of every Markdown table in `body`, each table's header and separator dropped.

    A section may hold several tables — 第 2 節 is often grouped under `###` subheadings.
    """
    rows: list[list[str]] = []
    table: list[list[str]] = []
    for line in body.splitlines() + [""]:
        if line.lstrip().startswith("|"):
            table.append([c.strip().replace("\\|", "|")
                          for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))])
        elif table:
            rows += [r for r in table[1:] if not all(set(c) <= set(":- ") for c in r)]
            table = []
    return rows


def plain_name(cell: str) -> str:
    """`[[X]]`, `[[X|alias]]` or `X（未納管）` → `X`."""
    m = LINK_NAME.search(cell)
    name = m.group(1) if m else cell
    return UNMANAGED_SUFFIX.sub("", name).strip()


def parse_relation(body: str) -> tuple[list[dict], set[tuple[str, str]]]:
    docs, private = [], set()
    for cells in table_rows(body):
        if len(cells) < 3:
            continue
        level, name_cell, deps_cell = cells[0], cells[1], cells[2]
        names = LINK_NAME.findall(name_cell)
        if not names:
            continue
        name = names[0].strip()
        docs.append({"name": name, "level": int(level) if level.isdigit() else None})
        for part in re.split(r"<br\s*/?>", deps_cell):
            if "（私有）" in part:
                for dep in LINK_NAME.findall(part):
                    private.add((name, dep.strip()))
    return docs, private


def parse_status(body: str) -> list[dict]:
    edges = []
    for cells in table_rows(body):
        if len(cells) < 4:
            continue
        up, down = LINK_NAME.findall(cells[0]), LINK_NAME.findall(cells[1])
        if not up or not down:
            continue
        count = cells[2]
        if not count.isdigit():
            warn(f"〈文件依賴狀態表〉 {cells[0]} → {cells[1]} 的 術語數 不是數字：{count!r}")
            continue
        edges.append({
            "up": up[0].strip(),
            "down": down[0].strip(),
            "count": int(count),
            "status": cells[3],
            "note": "|".join(cells[4:]).strip(),
        })
    return edges


def parse_tiers(body: str) -> list[dict]:
    """Tier legend lines such as `粗線 `==>`：≥ 8。`, `一般線 `-->`：2～7。`, `虛線 `-.->`：1。`."""
    tiers = []
    for line in body.splitlines():
        m = re.search(rf"^\s*-\s*(.*?)\s*`{ARROW}`\s*[：:]\s*(.+?)\s*。?\s*$", line)
        if not m:
            continue
        label, arrow, rng = m.group(1), m.group(2), m.group(3).replace(" ", "")
        if r := re.fullmatch(r"[≥>=]+(\d+)", rng):
            lo, hi = int(r.group(1)), None
        elif r := re.fullmatch(r"[≤<=]+(\d+)", rng):
            lo, hi = None, int(r.group(1))
        elif r := re.fullmatch(r"(\d+)[～~\-–](\d+)", rng):
            lo, hi = int(r.group(1)), int(r.group(2))
        elif r := re.fullmatch(r"(\d+)", rng):
            lo = hi = int(r.group(1))
        else:
            warn(f"看不懂的級距：{line.strip()}")
            continue
        tiers.append({"label": label, "arrow": arrow, "min": lo, "max": hi, "text": m.group(3)})
    return tiers


def parse_mermaid(body: str) -> tuple[str | None, dict[str, dict], list[dict]]:
    """The mermaid code block, its node definitions {ID: {name, shape}}, and its links in order.

    Link order matters: mermaid numbers edges in definition order, and the template maps
    each rendered edge back to its link by that number.
    """
    m = re.search(r"```mermaid[^\n]*\n(.*?)```", body, re.S)
    if not m:
        return None, {}, []
    code = m.group(1)
    nodes: dict[str, dict] = {}
    links: list[dict] = []
    for line in code.splitlines():
        s = line.strip()
        if not s or s.startswith("%%") or s.startswith("graph") or s.startswith("flowchart"):
            continue
        if e := re.fullmatch(rf"(\w+)\s*{ARROW}\s*(?:\|([^|]*)\|)?\s*(\w+)", s):
            links.append({"source": e.group(1), "arrow": e.group(2), "label": (e.group(3) or "").strip(), "target": e.group(4)})
        elif n := re.fullmatch(r"(\w+)\s*(?:\(\((.+)\)\)|\[(.+)\])", s):
            nodes[n.group(1)] = {"name": (n.group(2) or n.group(3)).strip(), "shape": "circle" if n.group(2) else "rect"}
        elif re.search(ARROW, s):
            warn(f"看不懂的 mermaid 邊（一行只能寫一條邊）：{s}")
    return code, nodes, links


def vault_of(path: pathlib.Path) -> pathlib.Path | None:
    for parent in path.parents:
        if (parent / ".obsidian").is_dir():
            return parent
    return None


def index_docs(root: pathlib.Path) -> dict[str, list[pathlib.Path]]:
    index: dict[str, list[pathlib.Path]] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for f in filenames:
            if f.endswith(".md"):
                index.setdefault(f[:-3], []).append(pathlib.Path(dirpath) / f)
    return index


def locate(name: str, index: dict[str, list[pathlib.Path]], vault: pathlib.Path | None) -> pathlib.Path | None:
    cands = index.get(name, [])
    if vault is not None and len(cands) > 1:
        cands = [c for c in cands if vault in c.parents] or cands
    if len(cands) > 1:
        warn(f"〈{name}〉有 {len(cands)} 份同名檔案，取 {cands[0]}")
    return cands[0] if cands else None


def parse_terms(doc: pathlib.Path) -> list[dict]:
    body = None
    for heading, text in sections(doc.read_text(encoding="utf-8")).items():
        if re.match(r"2\.\s", heading):
            body = text
            break
    if body is None:
        warn(f"{doc.name} 沒有第 2 節")
        return []
    terms = []
    for cells in table_rows(body):
        if len(cells) < 6:
            warn(f"{doc.name} 第 2 節有一列不足六欄：{cells}")
            continue
        if len(cells) > 6:  # an unescaped `|` inside a cell — keep it in 定義
            cells = cells[:4] + ["|".join(cells[4:-1])] + cells[-1:]
        name, src, via, pub, dfn, use = cells
        terms.append({
            "name": name,
            "src": plain_name(src),
            "via": plain_name(via) if via else "",
            "public": pub,
            "definition": dfn,
            "usage": use,
        })
    return terms


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arch", required=True, help="architecture document (.md)")
    ap.add_argument("--root", required=True, help="wikiRootDir — where the managed documents are searched for")
    ap.add_argument("--out", help="output HTML (default: {架構文件名}-文件依賴圖.html beside --arch)")
    args = ap.parse_args()

    arch = pathlib.Path(os.path.expanduser(args.arch)).resolve()
    root = pathlib.Path(os.path.expanduser(args.root)).resolve()
    out = pathlib.Path(os.path.expanduser(args.out)) if args.out else arch.with_name(f"{arch.stem}-文件依賴圖.html")

    secs = sections(arch.read_text(encoding="utf-8"))
    relation = find_section(secs, "文件依賴關係表")
    status = find_section(secs, "文件依賴狀態表")
    graph = find_section(secs, "文件依賴圖")
    if relation is None or status is None or graph is None:
        fail("架構文件缺少〈文件依賴關係表〉、〈文件依賴狀態表〉或〈文件依賴圖〉其中一節")

    docs, private = parse_relation(relation)
    status_edges = parse_status(status)
    tiers = parse_tiers(graph)
    if not tiers:
        fail("〈文件依賴圖〉旁找不到線型級距；級距以架構文件為準，不自行假設")
    code, mnodes, links = parse_mermaid(graph)
    if code is None:
        fail("〈文件依賴圖〉裡沒有 mermaid 程式碼；HTML 依賴圖照它繪製，不自行排版")
    updated = re.search(r"最近一次更新\s*(\d{4}-\d{2}-\d{2})", status)

    # terms per edge, read from each upper document's 第 2 節
    index = index_docs(root)
    vault = vault_of(arch)
    borrowed: dict[tuple[str, str], list[dict]] = {}
    for up in dict.fromkeys(e["up"] for e in status_edges):
        path = locate(up, index, vault)
        if path is None:
            warn(f"在 {root} 找不到〈{up}〉，這份文件的邊不會列出術語")
            continue
        for t in parse_terms(path):
            borrowed.setdefault((up, t["via"] or t["src"]), []).append(t)

    managed = {d["name"] for d in docs}
    by_pair = {(e["up"], e["down"]): e for e in status_edges}
    mismatches = 0
    for e in status_edges:
        scanned = len(borrowed.get((e["up"], e["down"]), []))
        if scanned != e["count"]:
            mismatches += 1
            warn(f"{e['up']} → {e['down']}：表上 術語數 {e['count']}，第 2 節掃到 {scanned} 列")
    for key in borrowed.keys() - by_pair.keys():
        if key[0] in managed:
            warn(f"{key[0]} 第 2 節有走 {key[1]} 的術語，但〈文件依賴狀態表〉沒有這條邊")

    # nodes and edges exactly as the mermaid graph defines them, joined to the status table by name
    level = {d["name"]: d["level"] for d in docs}
    for link in links:  # mermaid creates a node for an undefined ID, labelled with the ID itself
        for node_id in (link["source"], link["target"]):
            if node_id not in mnodes:
                warn(f"mermaid 圖的節點 {node_id} 沒有定義標籤")
                mnodes[node_id] = {"name": node_id, "shape": "rect"}
    nodes = [{"id": i, "name": v["name"], "shape": v["shape"], "level": level.get(v["name"]),
              "managed": v["name"] in managed} for i, v in mnodes.items()]

    edges = []
    for i, link in enumerate(links):
        up, down = mnodes[link["source"]]["name"], mnodes[link["target"]]["name"]
        row = by_pair.get((up, down))
        drawn = re.match(r"\d+", link["label"])
        if row is None:
            warn(f"mermaid 圖有 {up} → {down}，但〈文件依賴狀態表〉沒有這一列")
            row = {"count": int(drawn.group()) if drawn else 0, "status": "", "note": ""}
        elif drawn and int(drawn.group()) != row["count"]:
            warn(f"mermaid 圖上 {up} → {down} 的數字是 {drawn.group()}，表上是 {row['count']}")
        terms = borrowed.get((up, down), [])
        edges.append({
            "index": i, "source": link["source"], "target": link["target"], "up": up, "down": down,
            "arrow": link["arrow"], "count": row["count"], "status": row["status"], "note": row["note"],
            "private": (up, down) in private, "terms": terms, "scanned": len(terms),
        })
    for up, down in by_pair.keys() - {(e["up"], e["down"]) for e in edges}:
        warn(f"〈文件依賴狀態表〉有 {up} → {down}，但 mermaid 圖沒有這條邊")

    data = {
        "title": arch.stem,
        "tableUpdated": updated.group(1) if updated else None,
        "generated": datetime.date.today().isoformat(),
        "tiers": tiers,
        "mermaid": code,
        "nodes": nodes,
        "edges": edges,
    }
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.read_text(encoding="utf-8")
    if DATA_PLACEHOLDER not in html:
        fail(f"範本 {TEMPLATE} 裡找不到 {DATA_PLACEHOLDER}")
    html = html.replace(TITLE_PLACEHOLDER, f"{arch.stem}-文件依賴圖").replace(DATA_PLACEHOLDER, payload)
    out.write_text(html, encoding="utf-8")

    print(f"wrote {out}")
    # Obsidian does not track .html files, so a wikilink or relative link would stay unresolved;
    # a file:// URL is handed to the OS and opens in the browser.
    print(f"link: [{out.name}]({out.resolve().as_uri()})")
    print(f"nodes {len(nodes)}  edges {len(edges)}  terms {sum(e['scanned'] for e in edges)}  "
          f"count mismatches {mismatches}")


if __name__ == "__main__":
    main()
