# Purple Organization — Recovery Log

**Date:** 2026-03-07 to 2026-03-08
**Agent:** Violet
**Reason:** iCloud Desktop sync failure — files would not materialize for bulk operations

---

## What Happened

The primary workspace at `~/Library/Mobile Documents/com~apple~CloudDocs/Desktop/PurpleDirective/` (iCloud Desktop) became unreliable. iCloud refused to materialize files fast enough for git operations, bulk copies, or any tooling that needed to traverse the full directory tree. Multiple approaches were attempted over ~18 hours before the transfer completed.

## Transfer Method

| Step | Method | Result |
|------|--------|--------|
| 1 | OneDrive upload | Abandoned — too slow |
| 2 | Private git repo | Abandoned — `git add -A` hung for 50+ min |
| 3 | `ditto` to /tmp | Partial success, moved to local |
| 4 | `cp -R` per directory | Stuck on Knowledge/mdn-web-docs + _archive/github-advisory-db |
| 5 | `rsync` with timeouts | Completed most directories |
| 6 | Fresh git clones | mdn-web-docs + github-advisory-db downloaded from GitHub source |
| 7 | `npm install` | Site/node_modules rebuilt from package.json |
| 8 | Final `cp -R` | Research-Coordinator, Side-Ventures, A1-Clinical/data copied last |

## What Was Freshly Downloaded (NOT copied from iCloud)

These items were re-downloaded from source and may differ from iCloud originals:

| Item | Source | Risk |
|------|--------|------|
| `Knowledge/datasets/mdn-web-docs/` | GitHub (mdn/content) | HEAD at clone time, not original version |
| `Knowledge/datasets/github-advisory-db/` | GitHub (github/advisory-database) | HEAD at clone time, not original version |
| `_archive/Sapphire/Knowledge/github-advisory-db/` | GitHub | Same as above |
| `Site/node_modules/` | npm (from package.json) | Current versions, not locked versions |
| `build-tools/` | Fresh download | May differ from original |
| `platform-tools/` | Fresh download | May differ from original |

## What Was Verified Identical

| Directory | iCloud Size | Local Size | Match |
|-----------|-------------|------------|-------|
| Operations/Research-Coordinator/ | 38M | 38M | Exact |
| Operations/Side-Ventures/ | 480K | 480K | Exact |
| Operations/A1-Clinical/data/ | 3.3M | 3.3M | Exact |
| Core/ | 72K | 72K | Exact |
| Admin/ | 60K | 60K | Exact |
| Advisory/ | 104K | 104K | Exact |
| Memory/ | 40K | 40K | Exact |

## Security Fixes Applied

1. **`.gitignore` restored** — `*` wildcard + explicit allowlist for framework files only
2. **Pre-commit hook created** — Blocks: .env, credentials, CVs, clinical data, files >50MB
3. **Git status reduced** from 30 untracked items to 3 (only legitimate framework files)

## This Directory

`/Users/purple/PurpleDirective-Local/` is a **flat file copy** (no `.git`). It contains:

```
Total: ~6.0 GB

Top-level:
├── Admin/              60K   — Violet identity, directives
├── Advisory/          104K   — E.I.K. council identities
├── Agent - Banker/     28K   — Financial agent (incomplete)
├── Core/               72K   — Foundation, guidelines, protocols
├── Knowledge/         1.7G   — Datasets (mdn-web-docs, swe-bench, etc.)
├── Local/              20K   — Local workspace config
├── Memory/             40K   — Kernel, schemas, shared → symlink
├── OneDrive_1_3-5-2026/ 1.9G — Clinical research training materials
├── Operations/        678M   — A1-Clinical, Book-to-Brain, Purpleroom,
│                               Research-Coordinator, Side-Ventures, _Template
├── PurpleDirective-Recovery/ 5.4M — Old backup artifacts
├── Site/              160M   — Astro 5 website (purpledirective.com)
├── _archive/          1.8G   — Archived Sapphire content + datasets
├── build-tools/       186M   — Build utilities
├── platform-tools/     38M   — Platform utilities
├── platforms/         125M   — Platform SDKs
├── .claude/            28K   — Agent definitions
├── .github/             4K   — GitHub workflows
└── [root files]       ~230K  — CHARTER.md, CLAUDE.md, README.md, LICENSE,
                                CV.pdf, CV_final.docx, Ahmad CV 6Mar26.docx
```

## Empty Directories (cleanup candidates)

- `untitled folder/` — Finder artifact
- `References/` — Created but never populated
- `.temp/` — Empty temp directory

## Infrastructure State at Recovery Time

| Node | Status | Key Finding |
|------|--------|-------------|
| purpleroom | Online | Disk 82% (388/504G). 4 Docker containers + Ollama + llama-server. |
| purpledesk | Online | Proxmox VE hypervisor. Hosts purplecore as LXC (VMID 100). |
| purplecore | Online | LXC container. Runs cloudflared + Postfix + Docker. SSH password forgotten. |
| purplepi-1 | Online | Pi-hole + ntfy. 446G free (underutilized). 19 days uptime. |
| purplemac | Online | 3.2TB free. vllm-mlx serving 80B. Tailscale version mismatch. |

## Open Issues Post-Recovery

1. purpleroom disk at 82% — .cache (61G) clearable
2. purplecore SSH password forgotten — needs Tailscale SSH enabled
3. Tailscale CLI version mismatch on purplemac (1.92.5 vs 1.94.1)
4. No .git in this local copy — no version history or rollback
5. Freshly-downloaded datasets may not match iCloud originals
6. GitHub/ directory is redundant (legacy from pre-flatten)

## Decision: Working Directory

This local copy (`/Users/purple/PurpleDirective-Local/`) is now the active working directory. The iCloud location remains as backup with git tracking and the restored .gitignore protection.

---

— Violet, 2026-03-08
