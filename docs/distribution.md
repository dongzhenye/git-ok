# Installation & Distribution

_This document is aimed at maintainers/product planners who want the reasoning behind each release channel. End users can stick to the quick instructions in the main README._

## Quick Installation

| 安装场景 | 命令 | 说明 |
| --- | --- | --- |
| 隔离安装（推荐） | `pipx install git-ok` | 自动创建虚拟环境并将脚本链接到 `~/.local/bin`（或 macOS `~/Library/Python/<版本>/bin`），无需手动处理 PATH。 |
| 用户级安装 | `pip install --user git-ok` | 使用当前 `python3` 的用户目录安装。若命令找不到，执行 `python3 -m site --user-base` 并把输出路径的 `/bin` 加入 `PATH`。 |
| 本地开发 | `python3 -m venv .venv && source .venv/bin/activate && pip install -e .` | 贡献者在仓库里工作时使用，保持依赖隔离。 |

无论哪种方式，安装后都能在 shell 中直接运行 `git-ok --help`。更新时使用相同指令加 `--upgrade`。

## Distribution Strategy

We layer the delivery channels to balance reach and maintenance effort:

- **pipx (Primary)** – default end-user recommendation; works anywhere Python ≥3.8 is available, keeps dependencies isolated, and puts the console script on PATH automatically.
- **pip --user (Secondary, fallback)** – for environments without `pipx`, still low-friction and cross-platform; requires PATH check (`python3 -m site --user-base` + `/bin`).
- **Homebrew Tap (Secondary)** – planned once releases stabilize (`brew install dongzhenye/git-ok/git-ok`). Requires maintaining a formula and checksum bumps but offers the familiar `brew upgrade git-ok` flow for macOS/Linux developers.
- **curl installer (Tertiary)** – optional convenience script (`curl -fsSL ... | bash`) that would likely call `pipx` under the hood. We will only publish this with automated checksum/signature verification and clear documentation to avoid security surprises.
- **Self-contained binaries (Deferred)** – bundling via `shiv`, `pex`, or `pyinstaller` helps users without a modern Python runtime, but adds CI/build complexity. We will revisit when demand surfaces.
- **OS package managers (Deferred)** – apt, yum, Scoop, winget, etc. provide native experiences, yet every ecosystem needs its own packaging pipeline and approval. These stay on hold until we see strong platform-specific demand.

This staged plan keeps low-effort channels (pipx/pip) as the canonical path, adds Brew for developers who prefer it, and postpones high-maintenance options until user demand justifies the investment.

## Release Workflow

1. **Version & changelog** – bump `__version__` in `git_ok.py`,更新日志/README。
2. **本地验证** – 在一个真实仓库上跑 `git-ok`，并执行 `python -m build` 确认打包可行。
3. **合并到 main** – 提 PR，review 后合并。
4. **打 Tag + 发布 GitHub Release** – 例如 `v0.1.0`。发布后触发 “Publish to PyPI” workflow。
5. **Approve deployment** – workflow 到 `pypi-release` 环境时如需审批，点击 Approve。Trusted Publisher 会用 OIDC 上传，无需 API Token。
6. **验证公开安装** – 用 `python3 -m venv /tmp/ok && source ... && pip install git-ok` 简单运行 `git-ok --help`。
7. **沟通同步** – 关闭相关 Issue/里程碑，必要时发公告。

For the very first publish, PyPI auto-creates the `git-ok` project when the workflow uploads. Future releases follow the same steps without any extra configuration.
