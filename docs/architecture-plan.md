# git-ok 架构与工程计划（草案）

> 目标：在不丢失现有价值的前提下，将项目演进到零运行时依赖的长期形态，过程可控、可回滚、可测试。
> 本文聚焦“怎么落地”：分支策略、阶段计划、发布与风险。选型与客观数据见 `docs/language-choice.md`。

## 当前状态
- 语言/实现：Python 单文件 CLI（`git_ok.py`），已发布 PyPI，主要通过 `pipx/pip` 安装。
- 功能：非 Git 目录限时/限量扫描、工作区/暂存/未跟踪检查、stash/merge/rebase/cherry-pick 状态、upstream + ahead/behind、ignored 与重要文件筛选、文本/JSON 输出、退出码 0/1/2。
- 痛点：依赖 Python 运行时，与“零运行时”目标冲突；Brew/二进制体验有缺口。

## 目标与约束
- 体验：主推静态二进制 + Brew，开箱即用；保持当前 UX/JSON/退出码语义。
- 范围控制：先实现现有功能等价，不在迁移期叠加新特性。
- 兼容：迁移阶段保留 Python 版本作为参考/回退，避免服务中断。
- 质量：新增代码要有基本单测/集成测试，保证行为一致。

## 决策指引
- 主线语言：Go（见 `docs/language-choice.md` 的第一性分析与对比表）。
- Shell 只作为极短期 MVP 选项，不进入长期分发。
- Python 保留到 Go 版稳定后再决定是否废弃/存档。

## 分支与节奏
- 创建专属长期分支（示例名：`feature/go-port`），所有迁移相关改动集中在此分支，按小步可合并的 PR 推进。
- 保持 `main` 稳定，允许双线并行（修复/小特性可直接走 `main`，并在 Go 分支定期 rebase/merge）。
- 每个阶段结束前提交可回滚的检查点（tag 或 PR 合并节点），防止大爆炸式变更。

> 参考实现与分发样板：见 `docs/reference-gitleaks.md`。

## 分阶段计划

### 阶段 1：对齐与基线（当前）
- 产出：语言选择与架构计划文档（本文件 + `language-choice.md`），README 说明当前状态和迁移方向。
- 验证：复盘现有功能列表与测试覆盖，列出必须保持的行为。

### 阶段 2：Go 骨架与行为等价
- 产出：Go CLI 雏形（单入口、git 子进程封装、扫描/输出模块），通过核心单测/集成测试。
- 范围：只实现现有功能，JSON/文本/退出码等价，暂不扩展新特性。
- 里程碑：在分支内提供可下载的预览二进制（CI artifact）。

### 阶段 3：发布链路与文档
- 产出：交叉编译 CI（darwin/linux amd64/arm64）、GitHub Releases 产物、Homebrew 公式（或 tap）。
- 文档：更新 README，主推二进制/Brew，保留 Python 作为过渡说明；记录升级/回退路径。

### 阶段 4：收尾与切换
- 产出：将 Go 版本合入 `main`，发布首个 Go 版（带 tag/release）。
- 兼容：评估是否下线 PyPI，或标记为“legacy/兼容”；给出迁移提示。
- 展望：收集反馈，决定是否添加新特性（批量扫描等）。

## 参考项目（客观佐证 Go 静态 CLI 路线）
- `gitleaks/gitleaks`（Go，≈24k★）：Git 仓库泄露扫描，提供 Homebrew 公式和多平台二进制。  
- `trufflesecurity/trufflehog`（Go，≈23k★）：Git 历史敏感信息扫描，Homebrew/Release 分发。  
- `git-lfs/git-lfs`（Go，≈13k★）：Git 扩展，长期通过 Homebrew/Release 提供静态二进制。  
- 对照参考（非 Go）：`pre-commit/pre-commit`（Python，≈14k★）、`git-filter-repo`（Python，≈11k★）、`git-secrets`（Shell，≈13k★）。Go 方案在高星 Git 衍生 CLI 中占比更高，且分发路径与我们目标一致（Brew + Release 二进制）。  
> 更多语言分布采样与星级数据，见 `docs/language-choice.md` 的“数据采样与星级对比”。

## 风险与缓解
- 行为偏差：用集成测试对比 Python 版，必要时保留 Golden 输出对照。
- 平台差异：在 CI 跑多平台构建/测试；预发布二进制给早期使用者试用。
- 进度失控：严格阶段边界，避免在迁移期引入新功能；小 PR、频同步。

## 成功判定
- 功能等价：Go 版在主要功能与退出码上与现有版一致。
- 分发无摩擦：`brew install`/直接下载二进制开箱可用，不需额外运行时。
- 文档清晰：README/文档同步迁移方向和状态，用户知道该用哪个渠道。
