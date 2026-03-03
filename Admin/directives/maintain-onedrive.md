# CloudDrive Maintenance Directive

## Purpose
Define how Violet manages CloudDrive organization and sync for the Purple Directive.

## Scope

Violet maintains the organizational structure of files synced through CloudDrive, ensuring documents are findable, consistently named, and properly categorized.

## Directory Conventions

- Use descriptive folder names (no abbreviations unless standard)
- Separate active projects from archive
- Keep reference materials in dedicated reference folders
- No plaintext secrets in any synced file

## Maintenance Tasks

### On Request

1. **Organize** — Sort new files into appropriate directories
2. **Rename** — Apply consistent naming conventions
3. **Deduplicate** — Identify and resolve duplicate files
4. **Archive** — Move completed project files to archive

### Periodic Review

1. **Check sync status** — Verify CloudDrive is syncing without errors
2. **Review large files** — Flag files that consume disproportionate storage
3. **Clean temp files** — Remove temporary or draft files that are no longer needed

## Naming Conventions

- Documents: `YYYY-MM-DD_descriptive-name.ext`
- Meeting notes: `YYYY-MM-DD_meeting-topic.md`
- Versioned documents: `document-name_v1.2.ext`
- No spaces in filenames when possible; use hyphens

## Escalation

- Sync failures: **High** — investigate and resolve or notify Purple (human)
- Storage approaching limits: **Moderate** — propose cleanup plan
- Missing files: **Critical** — notify Purple (human) immediately
