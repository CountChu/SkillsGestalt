# Show-Reminder.ps1
# Displays a reminder message as a Windows message box.
#
# The message text and title are read from reminder.txt / title.txt (same
# folder as this script) as explicit UTF-8, so non-ASCII characters (e.g.
# Chinese) render correctly regardless of the PowerShell host's default code
# page. Keep this script body ASCII-only.
#
# This script is copied by the notify-week skill into a stable per-user
# location (%LOCALAPPDATA%\notify-week\<task-slug>\) and launched by a weekly
# Windows Scheduled Task.

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$textPath = Join-Path $scriptDir 'reminder.txt'
$message  = [System.IO.File]::ReadAllText($textPath, [System.Text.UTF8Encoding]::new($false))

$titlePath = Join-Path $scriptDir 'title.txt'
if (Test-Path $titlePath) {
    $title = [System.IO.File]::ReadAllText($titlePath, [System.Text.UTF8Encoding]::new($false)).Trim()
} else {
    $title = 'Weekly Reminder'
}

Add-Type -AssemblyName System.Windows.Forms | Out-Null
[System.Windows.Forms.MessageBox]::Show(
    $message,
    $title,
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Warning
) | Out-Null
