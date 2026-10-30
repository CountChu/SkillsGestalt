---
name: report-skills
description: The skill reads all SKILL.md files in the skills directory and generates a structured report of all available skills.
---

# MUST FOLLOW

- Must run workflow step by step, and display each step number.
- Follow [report-md-rules.md](.github/common/rules/report-md-rules.md) to create or update the report file.
- The report file name is `skills_report_{yyyyMMdd}.md`.

# Prompt Examples

## Prompt 1
```
What skills do you support?
```

## Prompt 2
```
Report all skills.
Run all steps.
```

## Prompt 3
```
Read all SKILL.md files and generate a report.
Save the report to the wiki.
```


# Workflow

## Step 0 - Warmup

- Read the workspace config [config.yaml](config.yaml) at the workspace root and resolve:
  - **`wikiDir`**: the Obsidian vault root — every wiki file this skill reads or writes lives under `{wikiDir}\`.
  - Substitute the resolved value wherever `{wikiDir}` appears in the steps below (including in commands).
  - If `config.yaml` is missing or `wikiDir` is absent, stop and ask the user.

- Locate the skills directory at `.github\skills\`.
- List all subdirectories.
  Each subdirectory is a skill.
- Verify that each subdirectory contains a `SKILL.md` file.
- Report the total number of skills found.

- The user provides a **checkpoints directory** for output files.
  - If no checkpoints directory is provided, default to `{wikiDir}\report-skills`.

- Check if the checkpoints directory exists.
  Create it if not.

- Save the entire user prompt text for reference in later steps.

- Follow [report-md-rules.md](.github/common/rules/report-md-rules.md) to create or update the report file.

## Step 1 - Read All SKILL.md Files

- Read every `SKILL.md` file found in Step 0.
- For each skill, extract:
  - **Name**: From the YAML front matter `name` field.
  - **Description**: From the YAML front matter `description` field.
  - **Steps**: Count the `## Step` headings.
    Note the range (e.g. Step 0–3).
  - **Scripts**: List all script file paths mentioned (e.g. `scripts\*.py`).
  - **MCP Tools**: List any MCP tool names referenced (e.g. `mcp_ado_wit_*`).
  - **Output Artifacts**: Identify what files or reports the skill produces (YAML, Markdown, HTML, CSV, console output).

## Step 2 - Summary Table

- Display a summary table with the following columns:
  - `#` (row number)
  - `Skill` (name, bold)
  - `Steps` (count)
  - `Scripts` (count)
  - `MCP` (Yes/No)
  - `Primary Output` (brief description of output artifacts)

- Follow [report-md-rules.md](.github/common/rules/report-md-rules.md) "Update report" to append the **Summary Table** section to the report file.

## Step 3 - Skills Description

- Display a table with the following columns:
  - `Skill` (name, bold)
  - `Description` (from the YAML front matter `description` field)
- Sort by skill name alphabetically.

- Follow [report-md-rules.md](.github/common/rules/report-md-rules.md) "Update report" to append the **Skills Description** section to the report file.

## Step 4 - Category Breakdown

- Group skills into categories based on their name prefix or purpose:
  - **Build/Create**: Skills that create ADO work items or generate files from templates.
  - **Check/Validate**: Skills that validate data against references.
  - **Compare**: Skills that diff two sources.
  - **Report**: Skills that fetch and display information.
  - **Triage**: Skills that diagnose failures and generate triage reports.
  - **Utility/Format**: Skills that modify, reformat, or synchronize files.
- For each category, list:
  - A description table with skill names and brief descriptions.
  - Total skills, steps, and scripts in the category.

- Follow [report-md-rules.md](.github/common/rules/report-md-rules.md) "Update report" to append the **Category Breakdown** section to the report file.

## Step 5 - Key Metrics

- Report aggregate metrics:
  - Total steps across all skills.
  - Total scripts across all skills.
  - Number of skills using MCP (ADO).
  - List of MCP skill names.
  - Output format breakdown table (Format, Count, Skills).

- Follow [report-md-rules.md](.github/common/rules/report-md-rules.md) "Update report" to append the **Key Metrics** section to the report file.

## Step 6 - Per-Skill Details

- For each skill, write a detail entry with:
  - **Description**: From the YAML front matter.
  - **Steps**: Range and brief summary of each step.
  - **Scripts**: List of script file paths.
  - **MCP Tools**: MCP tool names or "None".
  - **Output**: Output artifacts.

- Follow [report-md-rules.md](.github/common/rules/report-md-rules.md) "Update report" to append the **Per-Skill Details** section to the report file.
