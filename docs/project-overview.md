# Project Overview

## What git-ok Does
`git-ok` scans a directory and reports what is not safely backed up before you delete old projects. It inspects Git status, remote sync, ignored secrets/configs, and even whether the directory is under version control at all.

## History & Naming
- Started as **`git-sync-check`** and later renamed to **`git-ok`** to mirror the user’s question: “Is this repo OK to remove?”
- The most important learning came from user feedback: non-Git directories are far riskier than dirty Git repos, so we treat them as the highest severity case.
- Naming decisions and alternatives live in `docs/naming-decision.md`.

## Feature Highlights
- Detect non-Git directories and estimate how many files/bytes would be lost.
- Enumerate staged/unstaged/untracked changes plus stashes.
- Check remote sync (ahead/behind/diverged, missing upstream, detached HEAD).
- List ignored files (with emphasis on important configs/secrets).
- JSON output for scripts and automation.

See the README for user-facing examples and CLI usage.

## Technical Footprint
- Language: Python 3.8+ (stdlib + `subprocess` only).
- Entry point: `git_ok.py` (single-module CLI).
- Distribution: published on PyPI (`pip install git-ok`) with console script `git-ok`.
- Safe by design: read-only inspection, exit codes (0 clean, 1 issues, 2 non-Git).

## Important File Detection
Ignored files are filtered to surface likely-critical assets:

- **Patterns**: `.env`, `secret`, `credential`, `key`, `password`, `.local`, `config.local`
- **Extensions**: `.db`, `.sqlite`, `.sqlite3`, `.pem`, `.key`, `.cert`, `.crt`, `.pfx`, `.p12`
- **Ignored directories**: `node_modules/`, `.next/`, `dist/`, `build/`, `.venv/`, `__pycache__/`, `.cache/`

## Roadmap Snapshot
- **Shell installer** (`curl | bash`) for quick onboarding.
- **Homebrew formula** so macOS/Linux users can `brew install git-ok`.
- **Test suite and stricter error handling** to cover more edge cases.
- Potential batch/scanning mode once UX safeguards are designed.

Track active issues on GitHub for up-to-date priorities.
