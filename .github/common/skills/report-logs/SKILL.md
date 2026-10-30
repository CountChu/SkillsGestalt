---
name: report-logs
description: The skill reads all MD files in the wiki directory, extracts Created/Updated timestamps, and displays a build log grouped by date.
---

# MUST FOLLOW

- Must run workflow step by step, and display each step number.

# Prompt Examples

## Prompt 1

```
/report-logs
```

## Prompt 2

```
/report-logs
run step 9 to reflect the fact that, I have added some tags.
```


# Workflow

## Step 0 - Warmup

- Read the workspace config [config.yaml](config.yaml) at the workspace root and resolve:
  - **`wikiDir`**: the Obsidian vault root — every wiki file this skill reads or writes lives under `{wikiDir}\`.
  - Substitute the resolved value wherever `{wikiDir}` appears in the steps below (including in commands).
  - If `config.yaml` is missing or `wikiDir` is absent, stop and ask the user.

- Capture the current wall-clock timestamp as `begin` (format `yyyy-MM-dd HH:mm:ss`) and remember it for Step 12.
- Locate the wiki directory at `{wikiDir}\`.
- List all subdirectories.
  Each subdirectory corresponds to a skill.
- Count all `.md` files across all subdirectories.
- Report the total number of MD files found.

## Step 1 - Collect Metadata via report-metadata Skill

- Trigger the `report-metadata` skill to collect (and summarize) metadata for all wiki MD files.
- Forward any `--date <yyyy-MM-dd>` filter from the user's prompt to that skill.
- The `report-metadata` skill writes (or updates) `database\metadata.yaml`, which is the input for all subsequent steps.
- If `report-metadata` reports "No changes detected" and `database\metadata.yaml` already exists, continue to Step 2 (downstream grouping/report files may still need to be regenerated).
- If `database\metadata.yaml` does not exist after Step 1, abort the skill.

## Step 2 - Group by Updated Date

- Run `group_by_date.py` to split metadata into per-date files:
  ```
  python .github\skills\report-logs\scripts\group_by_date.py database\metadata.yaml --output-dir checkpoints\report-logs
  ```
- Each date group is written to `checkpoints\report-logs\s3-updated-{yyyy-MM-dd}.yaml`, sorted by updated time ascending.
- Report the number of date files created and record counts per date.

## Step 3 - Group by Created Date

- Run `group_by_created.py` to split metadata into per-created-date files:
  ```
  python .github\skills\report-logs\scripts\group_by_created.py database\metadata.yaml --output-dir checkpoints\report-logs
  ```
- Each date group is written to `checkpoints\report-logs\s4-created-{yyyy-MM-dd}.yaml`, sorted by created time ascending.
- Stale `s4-created-*.yaml` files for dates no longer present are removed.
- Report the number of date files created, the number of stale files removed, and record counts per date.

## Step 4 - Group by Skill

- Run `group_by_skill.py` to split metadata into per-skill files:
  ```
  python .github\skills\report-logs\scripts\group_by_skill.py database\metadata.yaml --output-dir checkpoints\report-logs
  ```
- Each skill group is written to `checkpoints\report-logs\s5-skill-{skill-name}.yaml`, sorted by updated time ascending.
- Report the number of skill files created and record counts per skill.

## Step 5 - Group by Tag

- Run `group_by_tag.py` to split metadata into per-tag files:
  ```
  python .github\skills\report-logs\scripts\group_by_tag.py database\metadata.yaml --output-dir checkpoints\report-logs
  ```
- Each tag group is written to `checkpoints\report-logs\s6-tag-{tag-name}.yaml`, sorted by updated time ascending.
- Records without tags are skipped.
- Report the number of tag files created and record counts per tag.

## Step 6 - Group by Status

- Run `group_by_status.py` to split metadata into per-status files:
  ```
  python .github\skills\report-logs\scripts\group_by_status.py database\metadata.yaml --output-dir checkpoints\report-logs
  ```
- The script reads each record's tags and looks up their `status` field from `database\tags.yaml`.
- Each record is grouped by the status of its **first tag that has a status** (e.g., `active`, `done`, `archived`, `blocked`, `on-hold`).
- Records whose tags have no status (or have no tags) are grouped under `no-status`.
- Each status group is written to `checkpoints\report-logs\s7-status-{status}.yaml`, sorted by updated time ascending.
- Report the number of status files created and record counts per status.


## Step 7 - Save Report by Updated

- Run `save_report.py` to generate per-date Markdown reports grouped by **updated** date from the `s3-updated-*.yaml` files:
  ```
  python .github\skills\report-logs\scripts\save_report.py checkpoints\report-logs
  ```
- The script reads each `s3-updated-{yyyy-MM-dd}.yaml`, preserves the `Created` timestamp from any existing report file, and overwrites `{wikiDir}\report-logs\by-updated\<date>.md` with fresh content.
- **Exclude records where the skill is `report-logs`** — these are the report-logs skill's own generated reports and should not appear in the output.
- Each file includes:
  - Header fields (`**Skill**`, `**Created**`, `**Updated**`).
  - **Period**: `{first-date} ~ {last-date}` showing the date range of records (derived from earliest and latest `updated` date).
  - A `## Table` section containing the build log table with columns: `#`, `Hash` (first 6 characters), `File` (clickable link to `{file}.md` — paths with spaces use angle-bracket links, e.g. `[Pipeline - Build ID & Run ID](<write-topic/Pipeline - Build ID & Run ID.md>)`, otherwise percent-encoded; if tags exist, display them below the file name as `` `tag` `` using `<br>`), `Skill`, `Created` (yyyy-MM-dd HH:mm), `Updated` (yyyy-MM-dd HH:mm), `Source`.
  - A `## List` section containing the numbered description list.
  - A **Source** legend at the bottom.
- Report the number of files saved and record counts per date.

## Step 8 - Save Report by Created

- Run `save_report_by_created.py` to generate per-date Markdown reports grouped by **created** date from the `s4-created-*.yaml` files:
  ```
  python .github\skills\report-logs\scripts\save_report_by_created.py checkpoints\report-logs
  ```
- The script reads each `s4-created-{yyyy-MM-dd}.yaml`, preserves the `Created` timestamp from any existing report file, and overwrites `{wikiDir}\report-logs\by-created\<date>.md` with fresh content.
- **Exclude records where the skill is `report-logs`** — these are the report-logs skill's own generated reports and should not appear in the output.
- Each file includes:
  - Header fields (`**Skill**`, `**Created**`, `**Updated**`).
  - **Period**: `{first-date} ~ {last-date}` showing the date range of records (derived from earliest and latest `created` date).
  - A `## Table` section containing the build log table with columns: `#`, `Hash` (first 6 characters), `File` (clickable link to `{file}.md` — paths with spaces use angle-bracket links, e.g. `[Pipeline - Build ID & Run ID](<write-topic/Pipeline - Build ID & Run ID.md>)`, otherwise percent-encoded; if tags exist, display them below the file name as `` `tag` `` using `<br>`), `Skill`, `Created` (yyyy-MM-dd HH:mm), `Updated` (yyyy-MM-dd HH:mm), `Source`.
  - A `## List` section containing the numbered description list.
  - A **Source** legend at the bottom.
- Report the number of files saved and record counts per date.

## Step 9 - Save Report by Tag

- Run `save_report_by_tag.py` to generate per-tag Markdown reports from the `s6-tag-*.yaml` files:
  ```
  python .github\skills\report-logs\scripts\save_report_by_tag.py checkpoints\report-logs
  ```
- The script reads each `s6-tag-{tag-name}.yaml`, preserves the `Created` timestamp from any existing report file, and overwrites `{wikiDir}\report-logs\by-tag\<tag-name>.md` with fresh content.
- **Exclude records where the skill is `report-logs`**.
- Each file includes:
  - Header fields (`**Skill**`, `**Created**`, `**Updated**`).
  - **Period**: `{first-date} ~ {last-date}` showing the date range of records (derived from earliest and latest `updated` date).
  - A `## Table` section containing the build log table with columns: `#`, `Hash` (first 6 characters), `File` (clickable link to `{file}.md` — paths with spaces use angle-bracket links, e.g. `[Pipeline - Build ID & Run ID](<write-topic/Pipeline - Build ID & Run ID.md>)`, otherwise percent-encoded; if tags exist, display them below the file name as `` `tag` `` using `<br>`), `Skill`, `Created` (yyyy-MM-dd HH:mm), `Updated` (yyyy-MM-dd HH:mm), `Source`.
  - A `## List` section containing the numbered description list.
  - A **Source** legend at the bottom.
- Report the number of files saved and record counts per tag.

## Step 10 - Save Report by Status

- Run `save_report_by_status.py` to generate per-status Markdown reports from the `s7-status-*.yaml` files:
  ```
  python .github\skills\report-logs\scripts\save_report_by_status.py checkpoints\report-logs
  ```
- The script reads each `s7-status-{status}.yaml`, preserves the `Created` timestamp from any existing report file, and overwrites `{wikiDir}\report-logs\by-status\<status>.md` with fresh content.
- **Exclude records where the skill is `report-logs`**.
- Each file includes:
  - Header fields (`**Skill**`, `**Created**`, `**Updated**`).
  - **Period**: `{first-date} ~ {last-date}` showing the date range of records (derived from earliest and latest `updated` date).
  - A `## Table` section containing the build log table with columns: `#`, `Hash` (first 6 characters), `File` (clickable link to `{file}.md` — paths with spaces use angle-bracket links, e.g. `[Pipeline - Build ID & Run ID](<write-topic/Pipeline - Build ID & Run ID.md>)`, otherwise percent-encoded; if tags exist, display them below the file name as `` `tag` `` using `<br>`), `Skill`, `Created` (yyyy-MM-dd HH:mm), `Updated` (yyyy-MM-dd HH:mm), `Source`.
  - A `## List` section containing the numbered description list.
  - A **Source** legend at the bottom.
- Report the number of files saved and record counts per status.

## Step 11 - Save Report by Skill

- Run `save_report_by_skill.py` to generate per-skill Markdown reports from the `s5-skill-*.yaml` files:
  ```
  python .github\skills\report-logs\scripts\save_report_by_skill.py checkpoints\report-logs
  ```
- The script reads each `s5-skill-{skill-name}.yaml`, preserves the `Created` timestamp from any existing report file, and overwrites `{wikiDir}\report-logs\by-skill\<skill-name>.md` with fresh content.
- **Exclude records where the skill is `report-logs`** — the `s5-skill-report-logs.yaml` file is skipped entirely.
- Each file includes:
  - Header fields (`**Skill**`, `**Created**`, `**Updated**`).
  - **Period**: `{first-date} ~ {last-date}` showing the date range of records (derived from earliest and latest `updated` date).
  - A `## Table` section containing the build log table with columns: `#`, `Hash` (first 6 characters), `File` (clickable link to `{file}.md` — paths with spaces use angle-bracket links, e.g. `[Pipeline - Build ID & Run ID](<write-topic/Pipeline - Build ID & Run ID.md>)`, otherwise percent-encoded; if tags exist, display them below the file name as `` `tag` `` using `<br>`), `Skill`, `Created` (yyyy-MM-dd HH:mm), `Updated` (yyyy-MM-dd HH:mm), `Source`.
  - A `## List` section containing the numbered description list.
  - A **Source** legend at the bottom.
- Report the number of files saved and record counts per skill.
- After the report is saved, capture the current wall-clock timestamp as `end` (format `yyyy-MM-dd HH:mm:ss`) and remember it for Step 12.

## Step 12 - Summarize Run Time

- Use the `begin` timestamp captured in Step 0 and the `end` timestamp captured in Step 11.
- Compute `total = end - begin` and format it as `"{minutes}m {seconds}s"` (e.g. `"0m 42s"`, `"3m 5s"`).
- Write a single YAML checkpoint to `checkpoints\report-logs\s12-timing.yaml` with the following shape:
  ```yaml
  skill: report-logs
  begin: <yyyy-MM-dd HH:mm:ss>
  end: <yyyy-MM-dd HH:mm:ss>
  total: "<Xm Ys>"
  ```
- Display the YAML inline so the user can see the timing summary.
