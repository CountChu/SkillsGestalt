# {APP} - Wireframe

> **This is the template, not a document.** The `reverse` command copies this shape into
> `{appDir}\docs\Wireframe.md` and its 繁體中文 twin `Wireframe-tw.md`, filling it from the **live
> DOM of the running page** — not from the markup file. An inventory written from the markup lists
> what the author believes the page has; finding out is the point of the scan.
>
> **There is no `-tw` template.** The twin keeps every heading, element kind, label and path in
> English and translates the prose around them.
>
> **This inventory is prescriptive.** Every row marked required must be on the page, and anything on
> the page that is not listed here is a defect at one end or the other. Nothing else restates it:
> a step or a document that lists a panel of its own is a second inventory, and the two will drift.
>
> **This document never names the skill, the command or the tool that produced it.**
>
> Delete this block when the document is written.

- **App**: {APP}
- **Page**: {URL_PATH}, served by {WHICH_FILE}
- **Scanned**: {WHEN}, in {WHICH_BROWSER}, at {WHICH_WINDOW_WIDTH}
- **Authority**: any page disagreeing with this inventory is what changes.

# 1 Page structure

Top to bottom, one bullet per element, each tagged with its kind — `[Panel]`, `[Heading]`, `[Text]`, `[Button]`, `[Select]`, `[Input]`, `[Table]`, `[Link]`, `[Status]` — and carrying the label a user actually sees, never the element's id.
Indent to show containment.

- `[Panel]` {PANEL_LABEL} — {WHAT_IT_IS_FOR}
  - `[{KIND}]` {LABEL_AS_SHOWN} — {WHAT_IT_DOES} · required: {YES_OR_NO}

# 2 Tables

Every table as a table of its own columns, in the order the page shows them.

## 2.1 {TABLE_NAME}

| # | Column as shown | Holds | Empty when |
|---|-----------------|-------|------------|
| 1 | {COLUMN} | {WHAT_THE_CELL_HOLDS} | {WHEN_IT_IS_BLANK} |

# 3 Visibility states

Which parts are hidden until something happens, and what makes each appear.
A wireframe of only the opening screen documents a fraction of the app, so each state below was **opened** before it was written down.

| State | What it shows | What makes it appear | Reached in the scan by |
|-------|---------------|----------------------|------------------------|
| {STATE} | {ELEMENTS} | {THE_TRIGGER} | {WHAT_WAS_DONE} |

# 4 Other pages

{EVERY_PAGE_THAT_IS_NOT_THE_MAIN_ONE} — including the ones nobody clicks to: an error body, an empty view, `/healthz`.
Each with what it carries.

# 5 What the page must not contain

- Nothing loaded from outside the app's own origin — no CDN script, no remote stylesheet, no web font, no tracking pixel.
- {ANYTHING_ELSE_THIS_PAGE_DELIBERATELY_LACKS}, with why it is absent rather than missing.

# 6 Defects

What the scan found that the page should not do, or does wrongly.
An element that shows a wrong value is still an element: it is listed in 1 **and** here, and the same defect is written into the design document's Specification.

| Defect | Where | Observed | Which document must change |
|--------|-------|----------|----------------------------|
| {DEFECT} | {ELEMENT} | {WHAT_IT_SHOWED} | {THIS_ONE_OR_THE_RSDC} |
