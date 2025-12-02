# git-ok

A tool to check what's not backed up in your Git repository.

## Why git-ok?

When managing multiple local repositories, it's common to want to clean up old projects. However, before deleting a repository, you need to ensure:
- All changes are committed and pushed
- No valuable local configuration files (like `.env` files with secrets) will be lost
- The local branch is fully synced with remote

This tool provides a comprehensive check for all these concerns in one simple command.

### Real-world Scenarios

1. **Non-Git Directory** - Most critical! No version control at all
   ```
   ❌ NOT A GIT REPOSITORY!
   All 156 files (2.3 MB) are NOT backed up!
   ```

2. **Orphaned Local Repository** - No remote configured with local commits
   ```
   ⚠️  No remote repository configured! (2 local commits)
   ```

3. **Database Files** - Local SQLite databases that might contain important data
   ```
   ⚠️  Important config/secret files:
      - addresses.db
   ```

4. **Environment Files** - Configuration files with API keys or secrets
   ```
   ⚠️  Important config/secret files:
      - .env.local
      - .claude/settings.local.json
   ```

5. **Large Node.js Projects** - Smart filtering to avoid false positives
   - Ignores `node_modules/` and build directories
   - Focuses on actual config files, not source code

### Design Principles

- **Check non-Git directories too**: The riskiest projects have no version control at all, so we treat that as the highest severity.
- **Be explicit**: Surface every class of risk (uncommitted work, ignored secrets, unsynced commits) so nothing is hidden.
- **Stay read-only**: The tool never mutates your repo; it only reports, so you stay in control.
- **Keep it simple**: No config files or setup hoops—clone once, or install the packaged CLI, and you're good to go.

### Why the name?

“git-ok” answers the exact question users ask before deleting a project: “Is this repo OK to remove?” The name stuck because it’s short, memorable, and mirrors the command’s yes/no verdict.

## Features

- **Non-Git Directory Detection**: Warns when directories have NO version control at all (most critical!)
- **Uncommitted Changes Detection**: Identifies staged, unstaged, and untracked files
- **Remote Sync Status**: Checks if your local branch is ahead or behind the remote
- **Ignored Files Listing**: Shows all files ignored by `.gitignore` (crucial for finding local configs)
- **Clean Output**: Clear, emoji-enhanced terminal output for easy reading
- **JSON Support**: Machine-readable output for automation

## Quick Start

```bash
# Clone the repository
git clone https://github.com/dongzhenye/git-ok.git
cd git-ok

# Run directly with Python
python3 git_ok.py /path/to/repo

# Or make it executable
chmod +x git_ok.py
./git_ok.py /path/to/repo
```

Want the `git-ok` command available everywhere? Jump down to [Installation](#installation).

## Installation

### From PyPI (recommended: pipx)

Install via `pipx` for isolation and automatic PATH wiring:

```bash
pipx install git-ok
```

`pipx` keeps dependencies in a managed venv and symlinks the `git-ok` command into your user bin directory (typically `~/.local/bin` on Linux or macOS `~/Library/Python/<version>/bin`), avoiding system/project dependency conflicts.

Prefer not to use `pipx`? A user-level `pip` install works too:

```bash
pip install --user git-ok
```

`pip` installs into the user site directory of the `python3` you invoked. On macOS, common paths look like `~/Library/Python/<version>/bin` (e.g., 3.9 or 3.12). If the command is not found after installation, run `python3 -m site --user-base`, append `/bin` from that path into your shell config, and reload:

```bash
echo 'export PATH="$(python3 -m site --user-base)/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
which git-ok
```

If you prefer Homebrew’s Python, call `/opt/homebrew/bin/python3 -m pip install git-ok` explicitly so the script is placed in that Python’s user directory.

### From the cloned repository

If you are hacking on the project locally, install the current checkout:

```bash
pip install .
# or
pipx install --force .
```

Both methods install the same console script entry point; rerun the same command with `--force`/`--upgrade` after pulling new changes to refresh the binary.

> Curious about broader distribution plans (Homebrew, curl installers, packages, etc.)? See `docs/distribution.md` for the maintainer-focused roadmap and reasoning.

## Usage

### Basic Check
```bash
# Check current directory
git-ok

# Check specific repository
git-ok /path/to/repo
```

### Show Ignored Files
This is especially useful for finding important local configuration files:
```bash
git-ok --show-ignored
```

### JSON Output
For scripting and automation:
```bash
git-ok --json
```

## Example Output

```
📁 Repository: /Users/example/my-project
============================================================
⚠️  Issues found:
   - Uncommitted changes found
   - Not in sync with remote

🔄 Sync Status:
   Local branch is 2 commits ahead of remote

📝 Uncommitted Changes:
   Modified files:
   src/main.py
   
   Untracked files:
   .env.local
   notes.txt

🚫 Ignored Files: 5 files
   Files ignored by .gitignore:
   - .env
   - .env.local
   - node_modules/
   - *.log
   - .DS_Store

============================================================
⚠️  WARNING: This repository has unsynced changes!
   Review the above before deleting this repository.
```

## Safety First

The tool helps you identify:
1. **Uncommitted work** that would be lost
2. **Unpushed commits** that exist only locally
3. **Ignored files** that might contain important data (API keys, local configs, etc.)

Always review the output carefully before deleting any repository!

## Requirements

- Python 3.6+
- Git command-line tool
- Unix-like environment (Linux, macOS, WSL)

## Project Status & Roadmap

- Current implementation: Python single-file CLI published on PyPI (`pipx/pip` install).
- Planned direction: migrate to a zero-runtime Go static binary with Homebrew distribution; see `docs/architecture-plan.md` for the phased plan.
- Language/architecture trade-offs: see `docs/language-choice.md`.
- Reference implementation patterns: see `docs/reference-gitleaks.md` for lessons from a similar Go-based Git scanner.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Author

Zhenye Dong ([@dongzhenye](https://github.com/dongzhenye))
