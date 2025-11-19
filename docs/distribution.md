# Installation & Distribution

_This document is aimed at maintainers/product planners who want the reasoning behind each release channel. End users can stick to the quick instructions in the main README._

## Quick Installation

```bash
# Install from the checked-out repo
pip install .

# Or keep it isolated with pipx
pipx install --force .
```

Both commands expose the `git-ok` console script system-wide, so you can run `git-ok` from any directory (verify with `git-ok --help`). Re-run the same command with `--force` or `--upgrade` after pulling new changes.

## Distribution Strategy

We layer the delivery channels to balance reach and maintenance effort:

- **pip / pipx (Primary)** – default recommendation; works anywhere Python ≥3.8 is available and keeps upgrades simple (`pip install --upgrade git-ok`). `pipx` is ideal when users want isolation from system site-packages.
- **Homebrew Tap (Secondary)** – planned once releases stabilize (`brew install dongzhenye/git-ok/git-ok`). Requires maintaining a formula and checksum bumps but offers the familiar `brew upgrade git-ok` flow for macOS/Linux developers.
- **curl installer (Tertiary)** – optional convenience script (`curl -fsSL ... | bash`) that would likely call `pipx` under the hood. We will only publish this with automated checksum/signature verification and clear documentation to avoid security surprises.
- **Self-contained binaries (Deferred)** – bundling via `shiv`, `pex`, or `pyinstaller` helps users without a modern Python runtime, but adds CI/build complexity. We will revisit when demand surfaces.
- **OS package managers (Deferred)** – apt, yum, Scoop, winget, etc. provide native experiences, yet every ecosystem needs its own packaging pipeline and approval. These stay on hold until we see strong platform-specific demand.

This staged plan keeps low-effort channels (pip/pipx) as the canonical path, adds Brew for developers who prefer it, and postpones high-maintenance options until user demand justifies the investment.
