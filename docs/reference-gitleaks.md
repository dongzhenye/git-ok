# 启发与借鉴：gitleaks 对 git-ok 的参考意义

> gitleaks 是一个 Go 实现的只读扫描型 Git 工具（≈24k★），发布渠道与我们目标一致（Homebrew/Release 静态二进制）。本稿梳理可借鉴点，并结合 git-ok 的需求做取舍。

## 可借鉴的关键点（结合需求筛选）
- **分发矩阵**：Homebrew + Release 多平台二进制为主渠道；Docker/源码安装可选。对 git-ok，建议聚焦 Brew/Release，Docker 可延后。
- **命令结构**：主入口 + 子命令。gitleaks 有 `git/dir/stdin`，我们当前只需单目录检查，可先保持单命令或轻量子命令（如未来加批量）。
- **配置优先级**：CLI 参数 > 环境变量 > 目标路径配置文件 > 默认配置。git-ok 目前零配置，可参考这一模式为未来“可选配置”预留。
- **输出与控制开关**：报告格式、`--report-path`、`--exit-code`、`--timeout`、`--no-color/no-banner`。git-ok 结论简单，但可引入 `--report-path`（JSON）和基础日志/颜色开关，其他高级格式暂不必做。
- **默认行为**：无参数扫描当前目录，与 git-ok 现状一致，保持不变。
- **集成生态**：gitleaks 提供 GitHub Action、pre-commit hook。git-ok 可优先提供 Action 示例（只读检查），pre-commit 可后置。
- **基线/忽略能力**：gitleaks 用 baseline 过滤历史发现。git-ok 暂不需要，后续如增加批量或历史扫描再评估。

## 具体可落地的改造建议
- **分发**：对齐 gitleaks 的 Brew + Release 二进制；Docker/源码安装作为补充，放在后期。
- **CLI 形态**：保持单命令，加入可选 `--report-path`（JSON 输出到文件），`--no-color`/`--no-banner` 控制输出，`--timeout` 透传到目录扫描；保留现有退出码 0/1/2 语义。
- **配置入口**：短期维持零配置；预留 `--config` + 环境变量扩展（如过滤规则），但不在首版实现。
- **文档示例**：仿照 gitleaks 的 README 结构，提供 Brew 安装、Release 下载、GitHub Action 示例片段。
- **未来扩展的子命令**：如批量模式上线，可拆出 `scan`（默认）与 `batch` 子命令；参考 gitleaks 的子命令风格，但控制复杂度。

## 甄别后的不做/暂缓
- **多格式报告**（csv/junit/sarif/模板）：短期不做，保持 JSON + 人读输出即可。
- **复杂基线/规则引擎**：当前场景不需要规则配置或历史基线，避免过度设计。
- **Docker 为主的分发**：优先 Brew/Release，Docker 作为可选补充，而非主路径。
