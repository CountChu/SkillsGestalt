---
name: report-week
description: The skill generates a weekly report from build-log MD files, summarizing test results, pipeline triages, root causes, and progress across a date range.
---

# MUST FOLLOW

- Must run workflow step by step, and display each step number.
- The report filename is `week-{start-date}` (e.g. `week-2026-05-06`).
  The full path is `{wikiDir}\report-week\week-{start-date}.md`.
- Follow [report-md-rules.md](.github/common/rules/report-md-rules.md) to create or update the MD report file.
- Follow [report-yaml-rules.md](.github/common/rules/report-yaml-rules.md) to save step outputs to the YAML checkpoint file.

# Prompt Examples

## Prompt 1

```
/report-week
```

## Prompt 2

```
/report-week
run step 0
```

## Prompt 3

```
Build weekly report 5/6 - 5/12
```


# Workflow

## Step 0 - Warmup

- Read the workspace config [config.yaml](config.yaml) at the workspace root and resolve:
  - **`wikiDir`**: the Obsidian vault root — every wiki file this skill reads or writes lives under `{wikiDir}\`.
  - Substitute the resolved value wherever `{wikiDir}` appears in the steps below (including in commands).
  - If `config.yaml` is missing or `wikiDir` is absent, stop and ask the user.

- Run `.venv` first.

- Check if the below scripts/files exist before running workflow.
  They must exist.
  - `.github\skills\report-week\scripts\locate_build_logs.py`
  - `.github\skills\report-week\scripts\merge_build_logs.py`
  - `.github\skills\report-week\scripts\rearrange_sections.py`

- Parse the user's prompt for required inputs:
  - Date range (e.g. `4/15 - 4/21` → `2026-04-15` to `2026-04-21`).
  - Optional override of the build-log directory (default uses both `{wikiDir}\report-logs\by-updated\` and `{wikiDir}\report-logs\by-created\`).

- Save the entire user prompt text for reference in later steps.

- Save YAML checkpoint with parsed inputs (date range, prompt text).
  Creating the MD report file is optional in this step since there may not be meaningful results yet.

## Step 1 - Locate Build-Log Files

- Run `.github\skills\report-week\scripts\locate_build_logs.py` with the parsed `start` and `end` dates from Step 0:
  - `python .github\skills\report-week\scripts\locate_build_logs.py {start} {end}`
  - Optional: pass `--dirs` to override the default directories (`{wikiDir}\report-logs\by-updated\` and `{wikiDir}\report-logs\by-created\`).
- The script outputs JSON with the per-directory `count` and `names` lists, plus the `date_range` and `total`.
- Report the number of files found per directory and the date range.

- Save YAML checkpoint.

## Step 2 - Merge Build Logs

- Run `.github\skills\report-week\scripts\merge_build_logs.py` with the parsed `start` and `end` dates from Step 0:
  - `python .github\skills\report-week\scripts\merge_build_logs.py {start} {end}` — prints the merged Markdown table to stdout.
  - Add `--format json` to capture the structured entry list (hash, file, link, skill, created, updated) for downstream steps.
  - Optional `--dirs` to override the default directories (`{wikiDir}\report-logs\by-updated\` and `{wikiDir}\report-logs\by-created\`).
- The script parses each MD file's table rows, deduplicates by `Hash`, and sorts by `Updated` ascending.
- This guarantees coverage of cross-range entries whose `[Created, Updated]` interval spans the requested window even if one of the two timestamps falls outside it (e.g. with period `5/7 - 5/12`, an entry with `Created = 2026-05-08` and `Updated = 2026-05-13` is kept via its presence in `by-created\2026-05-08.md`).
- Display the merged table and report the total number of unique entries.
- Append the merged table to the report file under a `## Build Log Entries` section.
  Create the report file with the header (per [report-md-rules.md](.github/common/rules/report-md-rules.md)) if it does not yet exist.

- Save YAML checkpoint.
- Save MD report file.

## Step 3 - Add Handled Column

- For each entry from Step 2, set `Handled` = the full `Updated` timestamp (e.g. `2026-05-08 16:58`).
- If the date portion of `Updated` falls **outside** the query date range (the `start` and `end` parsed in Step 0), fall back to `Created` instead.
  Example: with range `5/6 - 5/12`, an entry with `Created = 2026-05-08 08:47` and `Updated = 2026-05-13 10:25` gets `Handled = 2026-05-08 08:47`.
- Sort the entries by `Handled` ascending and renumber the `#` column accordingly.
- Rewrite the `## Build Log Entries` section in the report file so the table has columns: `#`, `Hash`, `File`, `Skill`, `Created`, `Updated`, `Handled`.
- Display the updated table to confirm the new column.

- Save YAML checkpoint.
- Save MD report file.

## Step 4 - Read Build Logs

- For each entry in the merged list from Step 3, locate the build-log MD file it came from (under `{wikiDir}\report-logs\by-updated\` or `{wikiDir}\report-logs\by-created\`) and extract:
  - **Tags**: backtick-quoted tokens after the file link in the `File` cell (e.g. `<br>\`2605-white-list\` \`todo\``); empty if none.
- Build a table with columns: **#**, **Date**, **File**, **Skill**, **Tags** where:
  - **#**: row number (preserving the Step 3 sort order by `Handled` ascending).
  - **Date**: the date portion of `Handled` from Step 3 (e.g. `2026-05-08 08:47` → `2026-05-08`).
  - **File**: the `File` link from Step 2.
  - **Skill**: the skill name from Step 2.
  - **Tags**: space-separated backtick tokens (e.g. `` `2605-white-list` `todo` ``); leave the cell empty if the entry has no tags.
- Display the table and report the total number of entries.
- Append the table to the report file under a `## Build Log Descriptions` section (replace the section if it already exists).

- Save YAML checkpoint.
- Save MD report file.

## Step 5 - Summarize Entry Descriptions

- For each entry in the table from Step 4, locate the build-log MD file it came from (under `{wikiDir}\report-logs\by-updated\` or `{wikiDir}\report-logs\by-created\`) and extract:
  - **Description**: a summary of the entry, **at most three sentences**.
    Derive it by combining:
    - the raw description text for its `Hash` from the numbered list below the table,
    - context from the entry's `Skill` (read `.github\skills\{skill}\SKILL.md` for the skill's purpose), and
    - context from the entry's `Tags` from Step 4.
      Look up each tag's description in `database\tags.yaml` and use it to disambiguate or enrich the summary (e.g. topical tags like `2605-white-list`, status tags like `todo`, `note`).
  - If the raw description is already three sentences or fewer and concise, you may use it as-is.
- Build a table with columns: **#**, **Date**, **File**, **Description** where:
  - **#**: row number (preserving the Step 4 sort order by `Handled` ascending).
  - **Date**: the `Date` from Step 4.
  - **File**: the `File` link from Step 4.
  - **Description**: the summary derived above (at most three sentences).
- Display the table and report the total number of entries.
- Append the table to the report file under a `## Entry Descriptions` section (replace the section if it already exists).

- Save YAML checkpoint.
- Save MD report file.


## Step 6 - Chronological Summary

- Summarize all entries in chronological order, grouped by date.
- Keep it short and scannable.
  Format:
  - **Date header**: `**MM-DD (Day)** — N entries`
  - **Test cases**: Merge repeated runs into one line with `FAIL → PASS` flow and brief root cause in parentheses.
  - **Pipelines**: List on one line using ✅/❌ icons, e.g. `Pipelines: 2431264 ❌, 2440215 ✅`
  - **PRs**: One line each with PR number, short description, and affected file.
  - **Reports/Other**: One line each.
- End with a single **Key Outcomes** line summarizing resolved cases, PRs merged, and pipeline status.
- Append this section to the report file.

- Save YAML checkpoint.
- Save MD report file.

## Step 7 - Summarize Progress

- **Before generating the summary**, ask the user to select one or more `Tags` (from the union of tags collected in Step 4, with their descriptions from `database\tags.yaml`) whose entries must be preserved verbatim.
  Wait for the user's selection before proceeding.
  If the user selects none, skip the preservation rule.
- For each date in the range, write a summary of the key activities and outcomes (**at most three sentences** per date).
- Highlight:
  - What was investigated.
  - What was resolved (any PASS after prior FAILs).
  - What remains unresolved.
- For any entry whose `Tags` (from Step 4) include one of the user-selected tags, preserve its description as a dedicated sentence in the date's summary so it is not dropped.
- Append this section to the report file.

- Save YAML checkpoint.
- Save MD report file.

## Step 8 - Build Summary Table

- Display the build-log directory path before the table.
- Display a summary table with the following columns:
  - `Date`
  - `Entries` (total count for that date)
  - `PASS` (count of entries whose description starts with `PASS`)
  - `FAIL` (count of entries whose description starts with `FAIL` or `FAILED`)
  - `Skills` (unique skill names for that date)
- Display empty cells instead of `0` values.
- Display a **Total** row at the bottom.
- Append this section to the report file.

- Save YAML checkpoint.
- Save MD report file.

## Step 9 - Build Skills Usage Table

- Build a pivot table showing skill usage across dates.
- Columns: `Skill`, one column per date in the range, `Total`, `PASS`, `FAIL/FAILED`, `Other`.
- Each cell shows the entry count for that skill on that date.
- Display empty cells instead of `0` values.
- Display a **Total** row at the bottom.
- Append this section to the report file.

- Save YAML checkpoint.
- Save MD report file.

## Step 10 - Skills Summary Table

- Summarize skill usage into a compact table.
- Display `**Period**: {start-date} - {end-date}` (e.g. `2026/4/22 - 2026/5/5`) before the table.
- Columns: `Skill`, `Description` (one-sentence from the skill's SKILL.md), `Total` (count of entries using that skill).
- Sort by Total descending.
- Display a **Total** row at the bottom.
- Append this section to the report file.

- Save YAML checkpoint.
- Save MD report file.

## Step 11 - Key Takeaways

- **Before generating the takeaways**, ask the user to select one or more `Tags` (from the union of tags collected in Step 4, with their descriptions from `database\tags.yaml`) to **highlight**.
  Wait for the user's selection before proceeding.
  If the user selects none, skip the highlight rule.
- Generate a concise **Key Takeaways** section summarizing the entire week in bullet points.
- Include:
  - **Resolved**: Test cases that went from FAIL → PASS, with brief root cause.
  - **Unresolved**: Test cases still failing at the end of the period, with distinct issue count.
  - **PRs**: Count and brief description of PRs submitted/merged.
  - **Pipeline triages**: Total count of pipeline builds triaged.
- For any entry whose `Tags` (from Step 4) include one of the user-selected highlight tags, add a dedicated bullet that calls it out (prefix the bullet with the tag in backticks, e.g. `` - **`2605-run-pr`**: ... ``) so it is not merged away.
- Keep each bullet to one line.
  No more than 5-10 bullets total (highlight bullets count toward this limit).
- After the bullets, add a `**Top 3**:` line listing the 3 most important items (by impact) as a numbered list.
  - **Top 3 must not duplicate a Highlight addition**: exclude any item whose underlying work (same test case + ADO, pipeline build, PR, or skill rollout) is already surfaced by a user-selected highlight tag in the `**Highlight additions**:` list below.
    Highlight-tagged work is guaranteed its own visibility, so reserve Top 3 for other high-impact items — if one of the top items overlaps a highlight, drop it and promote the next most important distinct item.
    (Skip this rule if no highlight tags were selected.)
- After the `**Top 3**:` list, add a `**Highlight tag additions**:` line that appends the user-selected highlight tags as a separate numbered list (one per tag, each summarizing the most important entry carrying that tag).
- After the `**Highlight tag additions**:` list, add a `**Highlight additions**:` line with the same content as `**Highlight tag additions**:` but with MD file names removed (each item is just `` `tag` `` followed by the summary, no leading file/MD name reference).
- Append this section to the report file.

- Save YAML checkpoint.
- Save MD report file.

## Step 12 - Build Weekly Report

- Build a short, presentation-ready **Weekly Report** section by combining the `**Top 3**:` and `**Highlight additions**:` lists from Step 11.
- Format:
  - Heading line: `### Top 3` followed by the same numbered list from Step 11's `**Top 3**:`.
  - Heading line: `### Highlight additions` followed by the same numbered list from Step 11's `**Highlight additions**:` (no MD file names).
- Non-overlap rule: `### Top 3` and `### Highlight additions` must not duplicate each other.
  Step 11 already builds `**Top 3**:` to exclude highlight-covered work, so both blocks are shown in full.
  An item is a duplicate when it describes the same underlying work — same test case + ADO, same pipeline build, same PR, or same skill rollout.
- If a residual duplicate is found, the **Highlight addition wins**: drop the duplicated item from `### Top 3` and replace it with the next most important distinct item (update Step 11's `**Top 3**:` to match), keeping the Highlight additions intact and renumbered.
- Do not invent new content; copy verbatim from Step 11 (subject to the non-overlap rule above).
  Omit the `### Highlight additions` block only if Step 11 had no highlight tags selected.
- Append this section to the report file under `## Weekly Report`.

- Save YAML checkpoint.
- Save MD report file.

## Step 13 - Build Test Cases Triaged Table

- Group entries by test case name (extract from the `File` column, e.g. `tc3390136_processor_cache_os_verification`).
- For each test case, report:
  - `Test Case` (name)
  - `ADO` (work item number extracted from the name, e.g. `3390136`)
  - `Runs` (total number of runs)
  - `Results` (e.g. `4 FAIL`, `1 FAIL, 1 PASS`)
- Sort by number of runs descending.
- Only include entries with skill `triage-test-case`.
- Append this section to the report file.

- Save YAML checkpoint.
- Save MD report file.

## Step 14 - Build Pipeline Triages Table

- Filter entries with skill `triage-pipeline-run`.
- For each pipeline triage, report:
  - `Build` (build number extracted from the file name)
  - `Result` (PASS/FAILED)
  - `Details` (brief summary from the description)
- Sort by date ascending.
- Append this section to the report file.

- Save YAML checkpoint.
- Save MD report file.

## Step 15 - Identify Key Root Causes

- Analyze all FAIL descriptions across the week.
- Group related failures into root cause categories, for example:
  - **ADO/Config issues** — Missing child test cases, shared parameter errors.
  - **Host JSON config errors** — Wrong JSON loaded, missing sections.
  - **BIOS/Firmware issues** — Flavor mismatch, update failures.
  - **Code bugs** — Parsing errors, missing attributes, regex issues.
  - **Infrastructure** — Missing directories, missing tools.
- List each category with specific examples from the descriptions.
- Append this section to the report file.

- Save YAML checkpoint.
- Save MD report file.

## Step 16 - Resolution Timeline Table

- Identify test cases that went from FAIL → PASS within the week.
- For each, report:
  - `Test Case` (name)
  - `ADO` (work item number)
  - `First FAIL` (date and time of the first FAIL entry)
  - `Final PASS` (date and time of the final PASS entry)
  - `Time to Resolve` (approximate duration between first FAIL and final PASS)
- Only include test cases that have both a FAIL and a subsequent PASS.
- Sort by time to resolve descending.
- Append this section to the report file.

- Save YAML checkpoint.
- Save MD report file.

## Step 17 - Root Cause Distribution Table

- Count the number of FAIL entries per root cause category (from Step 14).
- Display a table with columns:
  - `Root Cause Category`
  - `Count`
  - `%` (percentage of total FAILs)
- Display a **Total** row at the bottom.
- Append this section to the report file.

- Save YAML checkpoint.
- Save MD report file.

## Step 18 - Test Case Heatmap Table

- Build a grid table: test cases (rows) × dates (columns).
- Each cell shows the chronological sequence of results using ✅ (PASS) and ❌ (FAIL).
- Display empty cells for dates with no runs.
- Include a legend below the table.
- Only include entries with skill `triage-test-case`.
- Append this section to the report file.

- Save YAML checkpoint.
- Save MD report file.

## Step 19 - Repeat Offenders Table

- Identify test cases with multiple FAIL runs during the week.
- For each, report:
  - `Test Case` (name)
  - `ADO` (work item number)
  - `FAIL Runs` (count of FAIL entries)
  - `Root Causes` (brief list of distinct root causes from their FAIL descriptions)
- Sort by FAIL runs descending.
- Append this section to the report file.

- Save YAML checkpoint.
- Save MD report file.

## Step 20 - Builds per Day Table

- Display a table showing workload volume per day in the date range.
- Columns:
  - `Date`
  - `Day` (weekday abbreviation, e.g. Mon, Tue)
  - `Entries` (count)
  - Bar visualization (one █ character per entry)
- Skip days that have 0 entries (do not emit a row for them).
- After the table, add a **Skills usage per day** subsection.
  Lead with a line `**Total N skills, usage per day**:` where `N` is the sum of all entries across the listed days.
  Then for each day in the table, list the skills used and their entry counts on one line (e.g. `- **2026-05-13** — triage-test-case (3), write-note (1)`).
  Sort skills by count descending, then by name.
- Append this section to the report file.

- Save YAML checkpoint.
- Save MD report file.

## Step 21 - ADO Work Item Summary Table

- List each unique ADO work item from triage-test-case entries.
- Columns:
  - `ADO` (work item number)
  - `Test Case` (name)
  - `Runs` (total runs)
  - `Final Status` (PASS or FAIL based on the last chronological entry)
  - `Resolved?` (✅ if final status is PASS, ❌ if FAIL)
- Sort by number of runs descending.
- Append this section to the report file.

- Save YAML checkpoint.
- Save MD report file.

## Step 22 - Pipeline Build Summary Table

- List each unique pipeline build from triage-pipeline-run entries.
- Columns:
  - `Build` (build number)
  - `Tests Failed` (count or description of failed tests)
  - `Root Causes` (brief summary from the description)
- Sort by build number ascending.
- Append this section to the report file.

- Save YAML checkpoint.
- Save MD report file.

## Step 23 - Summarize Top 3 and Highlight Tags

- Synthesize a short, standup-ready summary of the week by re-reading the **Top 3** and **Highlight tag additions** produced in Step 11.
- Format as 3-5 one-line bullets, each leading with a bold theme label (e.g. `**Top focus**:`, `**New feature track**:`, `**Skill rollout**:`, `**Unresolved**:`, `**Process**:`, `**Contribution**:`).
- Each bullet must:
  - Cite specific identifiers (test case + ADO, pipeline build, PR number, skill name, tag).
  - End with a `(covers ...)` annotation listing which Top 3 item(s) and/or highlight tag(s) it covers, e.g. `` (covers Top #1 + `2605-run-pr` + `2605-build-pr`) ``.
- Top 3 and highlight tags are non-overlapping by construction (Step 11 excludes highlight-covered work from Top 3), so they normally yield separate bullets; merge a Top 3 item and a highlight tag into one bullet only when they genuinely share the same theme.
  Do not produce two bullets for the same underlying work.
- Every Top 3 item and every highlight tag must be covered by exactly one bullet's `(covers ...)` annotation — verify by tallying before saving.
- Append this section to the report file under `## Summarize Top 3 and Highlight Tags`.

- Save YAML checkpoint.
- Save MD report file.

## Step 24 - Rearrange Sections

- Reorder the sections in the report file so that **Weekly Report** appears first (immediately after the header), followed by **Key Takeaways**, **Progress Summary**, and **Summarize Top 3 and Highlight Tags**.
- Final section order:
  1. Header (Skill, Created, Updated, Prompt)
  2. **Weekly Report**
  3. **Key Takeaways**
  4. Progress Summary
  5. **Summarize Top 3 and Highlight Tags**
  6. Skills Summary
  7. Skills Usage
  8. Build Log Entries
  9. Build Log Descriptions
  10. Entry Descriptions
  11. Chronological Summary
  12. Build Summary
  13. Test Cases Triaged
  14. Pipeline Triages
  15. Key Root Causes
  16. Resolution Timeline
  17. Root Cause Distribution
  18. Test Case Heatmap
  19. Repeat Offenders
  20. Builds per Day
  21. ADO Work Item Summary
  22. Pipeline Build Summary
- Run `rearrange_sections.py` to reorder and update the timestamp:
  ```
  python .github\skills\report-week\scripts\rearrange_sections.py {wikiDir}\report-week\week-{start-date}.md
  ```
- The script splits the file on `## ` headings, reorders them per the list above, preserves any unknown sections at the end, and updates `- **Updated**:` to the current time.

- Save YAML checkpoint.
- Save MD report file.
