# Data Directory

## Purpose
This directory holds structured reference data and operational data that the agent uses during task execution. Data files are read by tools (Layer 3) and referenced by directives (Layer 1).

## Organization

### Reference Data
Static or slow-changing data that the agent needs for its domain. Examples:
- Drug interaction databases
- Pricing tables
- Regulatory thresholds
- Classification taxonomies
- Configuration parameters

Format: JSON files with descriptive names (`drug_interactions.json`, `pricing_tiers.json`).

### Operational Data
Data generated or updated during agent operation. Examples:
- Audit logs
- Task history
- Accumulated domain knowledge
- Performance metrics

Format: JSON or JSONL (one record per line for append-friendly logs).

## Conventions

**JSON for structured data.** Use JSON as the default format. It is readable by both humans and tools, parseable without ambiguity, and version-controllable.

**No plaintext secrets.** Credentials, API keys, and passwords must never appear in data files. Use placeholder values (`CHANGE_ME`, `[REDACTED]`) and store actual secrets in a secure credential manager.

**Descriptive file names.** Name files by what they contain, not by how they are used: `drug_interactions.json` not `lookup_table.json`.

**Schema documentation.** For non-obvious data structures, include a comment or companion file describing the schema. At minimum, document the top-level keys and their types.

## Example Structure
```
data/
├── README.md              # This file
├── [domain]_reference.json   # Primary reference data
├── [domain]_config.json      # Agent configuration parameters
└── audit_log.jsonl           # Append-only operational log
```

## Updating Data
- Reference data updates should be reviewed before deployment
- Operational data (logs, metrics) may be written by tools during execution
- All data modifications should be traceable — include timestamps and source identifiers
