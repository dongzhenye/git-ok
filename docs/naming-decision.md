# Naming Decision Document

## Final Decision: `git-ok`

### The Journey

We started with `git-sync-check` which was descriptive but:
- Too long (14 characters)
- Not entirely accurate (we check more than just sync)
- Lacks memorability

### Key Requirements

1. **Accurate**: Reflects what the tool actually does
2. **Simple**: Easy to type and remember  
3. **Practical**: Works well in command line usage

### What This Tool Really Does

The tool answers one fundamental question: **"Is this repository OK to delete/archive?"**

It checks:
- Working directory state (uncommitted changes, stash, operations in progress)
- Repository configuration (remotes, branch tracking)
- Sync status (ahead/behind/diverged)
- Important local-only files (configs, databases, certificates)

### Key Question (2025 revisit)
- **Are we delivering a one-command verdict that a Git repository is fully backed up (committed + pushed) so it is safe to delete locally?**

### Facts
- Non-Git directories remain the riskiest scenario we surface, yet mainstream demand (and marketing) centers on Git repos being ready for deletion after remote backup checks.
- `git-*` prefixes still dominate discoverability: users search for “git check before delete” or “git ok” far more than generic “repo” phrasing.
- Collision research (GitHub, PyPI, npm) shows `gitcheck`/`git-check` namespaces already host other tooling, while `gitok` has lighter GitHub usage but conflicts with an npm CLI; `repook` is clean yet drops the Git keyword.
- The existing `git-ok` PyPI package and documentation already align the brand with the “Is my repo OK?” story, minimizing migration friction if we keep the name.

### Conclusions
- Keep `git-ok` as the primary command while documenting alias explorations; it best answers the key question and already owns the namespace we care about most (PyPI + existing docs).
- If we ever ship an alternate name for discoverability, `repook` is the least-colliding option but would require deliberate messaging to reintroduce the Git focus.
- Record explorations and collision data (see “2025 Naming Exploration” below) so future contributors understand why certain names were accepted or rejected.

### Candidates Considered

1. **`git-ok`** ✅ (CHOSEN)
   - Pros: Minimal (6 chars), intuitive, no conflicts, Unix philosophy
   - Cons: Might be too simple without context

2. **`repo-ok`**
   - Pros: Semantically accurate (we check the whole repo)
   - Cons: Less discoverable in git ecosystem

3. **`git-check`**
   - Pros: Clear function
   - Cons: Too generic, lacks personality

4. **`git-ready`**
   - Pros: Positive connotation
   - Cons: Ambiguous (ready for what?)

5. **`repostat`**
   - Pros: Follows Unix naming (like netstat)
   - Cons: Already exists, suggests statistics not safety check

### Why `git-ok`?

1. **Ecosystem Integration**: The `git-*` pattern immediately signals this is a Git tool
2. **Search Optimization**: Users naturally search for "git" tools
3. **Simplicity**: "OK" is universally understood
4. **Unix Philosophy**: Simple name, clear purpose, can be used in conditionals
5. **No Conflicts**: Completely original in the Git ecosystem

### Usage Philosophy

```bash
# Simple check
git-ok

# Conditional usage  
git-ok && echo "Safe to delete!"

# Scriptable
if git-ok; then
    archive_repository
fi
```

The name embodies the tool's essence: a simple yes/no answer to whether your repository is in a good state.

## 2025 Naming Exploration (Divergent Phase)

Purpose: capture a wide funnel of whole-command names that could replace or augment `git-ok` before any filtering happens. This phase intentionally stayed divergent to satisfy the “≥10 ideas / ≥50 candidates” brief.

### Inputs & Constraints

- Current name rationale emphasizes short `git-*` familiarity, the yes/no verdict, and Unix composability.
- User goals: quick safety verdict before deleting local repos, clear handling of non-Git directories, assurance around remote sync plus ignored secrets.
- Competitive language observed in other CLIs: `brew doctor`, `npm doctor`, `cargo check`, `gitleaks`, `pre-commit`, `terraform plan`, `turso dump`, `fly status`, `docker scout`.
- Desired qualities from successful CLIs: pronounceable, short (≤2 words), immediate mental model (`git-*` or `repo-*` prefixes help discoverability), optionally action-oriented.

### Naming Territories & Candidates
Each territory mentions an inspiration and then lists at least five name candidates (no screening yet). Total candidates at this stage: 72.

1. **Git Health Check Verbs** – Inspired by `git status`, `brew doctor`: `git-checkup`, `git-health`, `git-audit`, `git-inspect`, `git-pulse`, `git-vitals`.
2. **Preflight & Clearance** – Inspired by `cargo check`, `terraform plan`: `git-preflight`, `git-cleared`, `git-ready`, `git-liftoff`, `git-runway`, `git-pass`.
3. **Guardians & Sentries** – Inspired by `gitleaks`, `sentry`: `git-guard`, `git-sentinel`, `git-watch`, `git-warden`, `git-shield`, `git-keeper`.
4. **Safety Nets & Lifelines** – Inspired by backup metaphors: `repo-saver`, `repo-safety`, `repo-secure`, `repo-lifeguard`, `repo-safeguard`, `repo-sentry`.
5. **Deletion & Cleanup Gatekeepers** – Inspired by `docker prune`, `brew cleanup`: `repo-retire`, `repo-trim`, `repo-dustoff`, `repo-dispose`, `repo-scrub`, `repo-cleanout`.
6. **Backup-Oriented Names** – Inspired by `aws backup`: `backup-check`, `backup-guard`, `backup-alert`, `backup-sure`, `backup-safe`, `backup-watch`.
7. **Cleanliness & Hygiene** – Inspired by `go fmt`: `repo-neat`, `repo-sterile`, `repo-fresh`, `repo-pure`, `repo-tidy`, `repo-gleam`.
8. **Integrity & Trust** – Inspired by security tooling: `repo-integrity`, `repo-trust`, `repo-proof`, `repo-bond`, `repo-seal`, `repo-verify`.
9. **Confidence / “OK” Variants** – Inspired by the current name: `repo-okay`, `repo-affirm`, `repo-go`, `repo-sound`, `repo-solid`, `repo-approve`.
10. **Archival & Preservation** – Inspired by `git archive`: `repo-archive`, `repo-shelve`, `repo-preserve`, `repo-box`, `repo-store`, `repo-museum`.
11. **Sync & Alignment** – Inspired by `git sync`: `repo-sync`, `repo-synced`, `repo-bridge`, `repo-link`, `repo-aligned`, `repo-match`.
12. **Rescue & Emergency Handling** – Inspired by `git fsck`: `repo-rescue`, `repo-orphan`, `repo-signal`, `repo-alarms`, `repo-firstaid`, `repo-lifeline`.

### Deep Check Snapshot (2025-11-20)

Focused on the five finalists requested (`gitok`, `git-ok`, `gitcheck`, `git-check`, `repook`). Data sources: GitHub search samples, `pypi.org/pypi/<name>/json`, and npm registry metadata.

| Candidate | Fit Summary | GitHub Presence (sample) | PyPI Status | npm Registry |
| --- | --- | --- | --- | --- |
| `gitok` | Short, Git-focused verdict; non-hyphen aesthetic | `okwareddevnest/gitok` (54★), `CofficLab/GitOK` (3★), smaller personal forks via `gh search repos gitok` | **Available** (no project registered) | `gitok@1.1.0` – CLI to clone parts of repos |
| `git-ok` | Current brand; mirrors “Is this repo OK?” question | ~4.6k hits for `git-ok in:name`; direct matches include `gandhi546/git-ok`, `arfanshakil/git-ok`, `dongzhenye/git-ok` | **Taken** – existing package `git-ok` 0.1.0 (this project) | Not registered (404) |
| `gitcheck` | Literal “check” verb; Git-prefixed | `badele/gitcheck` (176★), `mynameisfiber/gitcheck`, `EternalCodeTeam/GitCheck` etc. | **Taken** – `gitcheck` 0.3 (“Check multiple git repository in one pass”) | `gitcheck@1.0.0` – multi-repo checker |
| `git-check` | Verb-object clarity; hyphen helps readability | Collides with `yonchu/git-check`, `cict-ccs229/git-check` and broader “git check*” repos | **Available** (hyphenated slug unused) | `git-check@2.0.0` – micro tool to verify git installation |
| `repook` | Pronounceable, repo-centric “OK” | Only tiny repos (`ivancorrales/repook`, `Repook/Repook`) with zero stars | **Available** | Not registered (npm 404) |

Observations:
- `gitcheck`/`git-check` already overlap with active OSS tooling on both GitHub and npm; renaming to either would inherit existing traffic (good for discovery) but likely confuse users.
- `gitok` has lighter OSS usage yet an npm package with a related Git workflow, so cross-ecosystem confusion is still likely even though the PyPI slot is free.
- `git-ok` remains the most discoverable in the Git ecosystem but already collides with numerous small repos; retaining it avoids new namespace fights.
- `repook` is the cleanest namespace-wise (free on PyPI/npm with negligible GitHub presence) but sacrifices the Git keyword in search.
