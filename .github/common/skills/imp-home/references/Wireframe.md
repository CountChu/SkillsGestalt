# Home — Wireframe

**This document owns the page's element inventory and how it looks: what the page must *contain*, and what it must *look like*.**
What the hub must *do* is not decided here.

**Neither design document names the other, in either direction.**
Each states its own scope instead, so either can be read first, and neither goes stale when the other is renumbered.
A rule whose reason lives in the other file is stated here **in full** rather than cited — a reason worth having is worth writing down where it applies.
**A color, a hover state or a border belongs here**, with the elements it describes; a statement that would still be true if the buttons were repainted belongs in the design instead.

It is **prescriptive, not a scan**: it says what the page must have, and a running page is checked against it.
Every element below is required unless its Visibility says otherwise.

---

## 1 Page structure

One page, one column, centred.
No panels, no filters, no controls — everything the hub does is navigate.

```
<main>
  <h1>            title, from the app config
  <p>             one-line summary
  <div.buttons>   the button grid, in link-list order
    <a>           one per link entry
      <span.label>
      <span.url>
      <span.note>   only when the entry has a note
```

## 2 Elements

| # | Element | Kind | Content | Visibility |
|---|---|---|---|---|
| 1 | Heading | `h1` | the app config's `title`, escaped | always |
| 2 | Summary | `p` | one fixed line inviting the reader to pick an app | always |
| 3 | Button grid | `div.buttons` | one anchor per link entry, in the link list's order | always |
| 4 | Button | `a` | the whole entry; `href` is the entry's `href` verbatim and escaped | one per link entry |
| 5 | Button label | `span.label` | the entry's `label`, escaped | always, inside every button |
| 6 | Button URL | `span.url` | the entry's `href` verbatim, escaped, in a monospace face | always, inside every button |
| 7 | Button note | `span.note` | the entry's `note`, escaped | only when the entry carries a note |
| 8 | Empty state | `p.empty` | a line saying no links are configured and what to do about it | only when the link list is empty, and then instead of the grid |

**Every button is the same element with the same classes.**
A link the page cannot navigate to, and one the hub serves itself, are rendered by rows 4–7 exactly like any other entry: no extra class, no badge, no ordering difference.
The page has no way to tell them apart, and that is the design, not an omission.

## 3 Pages other than the hub page

These are reachable but are not the hub page, and they carry their own markup rather than the stylesheet — a mount failure answers at any depth under its prefix, so no one relative path to the stylesheet would be correct.

| Page | Reached by | Must contain |
|---|---|---|
| Mount not prepared | any path under a mount whose app could not be loaded | the mount's label, the reason, the directory looked in, the skill that assembles it, and a link back to `/` |
| Mount failed while answering | a mounted app that threw or rejected | plain text naming the app and the error, and saying the hub and its other mounts are unaffected |
| Health | `GET /healthz` | JSON: `{ok, title, links, dead, mounts, assembledAt}`, `mounts` being one `{prefix, label, ok, error}` per configured mount |

## 4 Visibility states

- The **button note** (row 7) is the only element inside a button that can be absent.
- The **empty state** (row 8) and the **button grid** (row 3) are mutually exclusive.
- Nothing on the page appears in response to an interaction — there are none.
  A page whose inventory changes after a click means something was added that this document does not carry.

## 5 What the page must not contain

- **No `<script>`, anywhere.**
  Rendering happens on the server; there is nothing for a client to run.
- **No external reference** other than the one same-origin stylesheet: no CDN, no web font, no image, no analytics.
- **No per-button styling hook** beyond the classes in §2, which is what keeps 2.4's rule enforceable by inspection.

## 6 Defects found by checking a running page

Record here what a live page showed that this inventory did not predict, with the date.
An element that shows a wrong value is still an element — record both facts, and write the rule it breaks into the design's Specification as well.

*(none recorded)*
