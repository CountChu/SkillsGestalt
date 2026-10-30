---
name: set-tag-status
description: The skill sets the status field of a tag in tags.yaml to one of the allowed values (active, done, archived, blocked, on-hold), or removes it.
---

# MUST FOLLOW

- Must run workflow step by step, and display each step number.
- The report filename is `set-tag-status-{yymmdd}`.
- Follow [report-md-rules.md](.github/common/rules/report-md-rules.md) to create or update the MD report file.

# Prompt Examples

## Prompt 1

```
/set-tag-status
```

## Prompt 2

```
/set-tag-status 2605-run-pr active
```

## Prompt 3

```
Set the tag 2605-clear-cmos status to done
```


# Workflow

## Step 0 - Warmup

- Parse the user's prompt for:
  - **Tag** (optional): The tag name to update (e.g., `2605-run-pr`).
  - **Status** (optional): One of the allowed values below.

- Verify the tag exists in `database/tags.yaml`.
  If provided but not found, warn the user and stop.


## Step 1 - Select Tag and Status

- If the tag name is missing, read `database/tags.yaml` and display all tags with their current status in a table, then ask the user to pick one:

  | # | Tag | Status |
  |---|-----|--------|
  | 1 | ... | ...    |

- If the status is missing, ask the user to select one:

  | # | Status | Description |
  |---|--------|-------------|
  | 1 | active | Currently in progress |
  | 2 | done | Work completed |
  | 3 | archived | No longer relevant, kept for history |
  | 4 | blocked | Waiting on something external |
  | 5 | on-hold | Paused intentionally |
  | 6 | (none) | Remove the status field entirely |


## Step 2 - Update Tag Status

- Read `database/tags.yaml`.

- Find the entry matching the specified tag name.

- If the user selected `(none)`, remove the `status` line from the tag entry entirely.

- If a `status` field already exists on that entry, replace its value with the new status.

- If no `status` field exists, add `status: <value>` as a new line after the `description` field of that tag entry.

- Write the updated content back to `database/tags.yaml`.

- Display the updated tag entry:

  ```yaml
  - tag: <tag_name>
    description: <description>
    status: <new_status>
  ```


## Step 3 - List Tag Table

- Read `database/tags.yaml`.

- Display all tags in a table:

  | # | Tag | Status | Description |
  |---|-----|--------|-------------|
  | 1 | ... | ...    | ...         |

- Tags without a `status` field should show an empty cell.

- Save MD report file following this format:

  ```markdown
  # set-tag-status-{yymmdd}

  - **Skill**: set-tag-status
  - **Created**: {YYYY-MM-DD HH:MM}
  - **Updated**: {YYYY-MM-DD HH:MM}
  - **Prompt**:
  ```
  {user prompt}
  ```

  ## Updated Tags

  ```yaml
  - tag: <tag_name>
    description: <description>
    status: <new_status>
  ```

  (Append each new update below the previous ones when the report file already exists for today.)

  ## All Tags

  | # | Tag | Status | Description |
  |---|-----|--------|-------------|
  | 1 | ... | ...    | ...         |
  ```
