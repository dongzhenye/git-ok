# Basic Design Decisions

## 1. Single Repository Focus (for now)
**Decision**: Default command checks one repository path at a time, but the codebase stays open to future batch tooling.

**Rationale**:
- Current UX emphasizes careful review of each repo before deletion.
- Batch modes risk hiding important warnings, so we defer them until we can design a safe summary view.
- Users who really need batch behavior today can still script around `git-ok` (e.g. `fd -H '.git' | xargs -I {} git-ok {}/..`).
- Feedback indicates bulk scanning would be useful, so we keep the architecture simple enough to add it later.

## 2. Packaged CLI Distribution
**Decision**: Ship an installable console script (`pip install git-ok`, `pipx install git-ok`) instead of relying solely on manual script execution.

**Rationale**:
- Users now expect to call `git-ok` globally like other CLIs (`git`, `gh`, etc.).
- Packaging via `pyproject.toml` keeps dependency metadata explicit and reduces “copy this script” friction.
- `pipx`/`pip` installs still keep the code auditable (single module) while improving discoverability.

## 3. Non-Git Directory Support
**Decision**: Full support with highest severity warnings

**Context**: Initially overlooked, added after user feedback
**Learning**: The most dangerous case is no version control at all

## 4. Important File Detection
**Decision**: Pattern-based detection with smart filtering

**Detected**:
- Config patterns: `.env`, `secret`, `credential`, `key`, `password`, `.local`
- Database files: `.db`, `.sqlite`, `.sqlite3`
- Certificates: `.pem`, `.key`, `.cert`, `.crt`, `.pfx`, `.p12`

**Filtered out**: `node_modules/`, build directories, common source files

## 5. Read-Only Operation
**Decision**: Never modify files or repository state

**Rationale**:
- Safety first - no accidental commits or pushes
- Users must understand issues before taking action
- Prevents tool from becoming a crutch

## 6. Exit Code Semantics
**Decision**: Different codes for different severities

- `0`: Repository is clean and safe
- `1`: Git repository has issues
- `2`: Not a Git repository (most severe)

**Use case**: Shell scripts can handle different scenarios:
```bash
git-ok || handle_issues $?
```

## 7. No Configuration Files
**Decision**: Convention over configuration

**Rationale**:
- Works the same everywhere
- No hidden surprises
- Learned patterns work well for 90% of cases
