# 语言与架构选择：从第一性原理出发

> 本文聚焦“选什么”：目标、原则、备选、客观数据与结论；落地与节奏见 `docs/architecture-plan.md`。

## 我们的目标与约束
- 问题域：帮助 Git 用户判断“本地能不能安全删除”，输出以简洁文本为主，性能需求低但要稳健。
- 受众与环境：主力是 macOS/Linux 开发者，期望 `brew install git-ok` 的简洁体验；Windows 可通过二进制或 WSL/Git Bash。
- 交付偏好：倾向零运行时依赖的安装路径，降低“先装语言”的摩擦；同时代码要易读、单入口、可测试，可逐步扩展。

## 原则（第一性）
1) 依赖最小：默认不要求用户额外安装语言运行时。  
2) 跨平台稳健：路径空格、权限错误、限时/限量扫描等边界要可靠。  
3) 发布顺畅：Homebrew/GitHub Releases 是第一渠道，其他方式可顺延。  
4) 简洁匹配需求：只为现有检查场景建模，避免用重框架；单文件/单入口优先。  
5) 可维护/可测试：后续新增检查或 batch 模式不应推倒重来。  

## 决赛选项对比表（关键点速览）
| 方案 | 运行时依赖 | 安装与发布 | 跨平台鲁棒性 | 维护与测试 | 典型适用场景 | 主要风险 |
| --- | --- | --- | --- | --- | --- | --- |
| Go（推荐主线） | 无，静态二进制 | Brew 原生友好，GitHub Releases 直接下载 | 强（标准库 IO/超时/子进程控制） | 强，`go test` 易覆盖 | 长期主分发，跨平台一致体验 | 需安装 Go 工具链；需要小规模重写 |
| Shell（MVP） | 无，但依赖系统 bash/核心工具 | `curl | bash` 最快，可封装 Brew 脚本公式 | 中-偏弱，平台工具差异明显 | 弱，空格/权限/超时处理易碎 | 最快验证版、一次性脚本 | 随规模扩展会积累技术债，后续大概率重写 |
| Python（过渡/参考） | 需 Python 运行时 | 已有 PyPI/pipx，Brew 需额外包装 | 中，依赖环境一致性 | 中，生态成熟 | 过渡期兼容、作为参考实现 | 与“零运行时”目标冲突，最终需替代 |

## 决赛选项简述

### Go（小型单入口程序）
- 优点：静态二进制、无运行时依赖，跨平台交叉编译简单；标准库自带 JSON/超时/子进程控制；Brew 原生友好；`go test` 易覆盖。  
- 代价：需维护一个约 300–500 行的小程序，要求安装 Go 工具链（对目标用户通常可接受）。

### 纯 Shell（bash/posix）
- 优点：无运行时、单文件极小，可用 `curl | bash`。  
- 隐患：跨平台行为差异大（macOS vs BusyBox），空格/权限/超时处理易碎，可测试性弱；Brew 公式只是脚本包装。适合一次性 MVP，不适合长期主线。

### Python（现状对照）
- 优点：已有实现和文档，生态熟悉。  
- 不足：依赖 Python 运行时，与“零运行时”目标冲突；如果主推 Brew/二进制，迟早要提供替代。

## 长期最合适的方向
- 主线选择 Go：满足零运行时 + 稳健 + 易发布 + 易测试的原则，体量仍然可控，不是过度设计。  
- Shell 仅作为临时 MVP（如需极快验证），不建议成为主分发，以免未来再重写。  
- Python 版本可保留一段时间作为参考或回退，但文档/发布应以 Go 二进制为主。

## 数据采样与星级对比（客观参考）
- 方法：`gh search repos git --language <lang> --sort stars --order desc --limit 30 --json fullName,stargazersCount,language`（采样时刻以查询时间为准，包含“git”关键词的热门仓库，未手工剔除非 CLI 项）。  
- 汇总（Top 30，单位：stars）：  

| 语言 | 最大值 | 中位数 | 最小值 | 示例前 5 仓库 |
| --- | --- | --- | --- | --- |
| Go | 68,784 | 7,024.5 | 3,921 | `jesseduffield/lazygit`, `go-gitea/gitea`, `gogs/gogs`, `cli/cli`, `harness/harness` |
| Python | 135,868 | 7,250 | 3,668 | `521xueweihan/HelloGitHub`, `bregman-arie/devops-exercises`, `Ebazhanov/linkedin-skill-assessments-quizzes`, `521xueweihan/GitHub520`, `marimo-team/marimo` |
| Shell | 183,085 | 6,905.5 | 3,593 | `ohmyzsh/ohmyzsh`, `anthropics/claude-code`, `nvie/gitflow`, `tj/git-extras`, `sindresorhus/pure` |
| Rust | 56,038 | 2,487.5 | 952 | `sharkdp/bat`, `dandavison/delta`, `jj-vcs/jj`, `gitui-org/gitui`, `gitbutlerapp/gitbutler` |
| JavaScript | 125,908 | 12,430 | 4,755 | `Chalarangelo/30-seconds-of-code`, `anuraghazra/github-readme-stats`, `resume/resume.github.com`, `usebruno/bruno`, `typicode/husky` |

- 解读：高星项目横跨多语言，Go 在 Git 相关 CLI 里已有成熟静态二进制/Brew 样板（`lazygit`、`gitea`、`gogs`、`gh` 等），与“零运行时”目标贴合；Python/Shell 虽有高星项目但需运行时/脚本环境；Rust 构建/体量较重；JavaScript 偏前端/工具链，不利于零运行时分发。

## 推荐演进路径（控制复杂度）
1) 收敛需求：锁定当前检查项（非 Git 限时扫描、工作区变更、stash/merge/rebase/cherry-pick、upstream/ahead/behind、ignored 与重要文件筛选），只输出文本 + JSON + 退出码语义。  
2) Go 落地：单入口 CLI，少量内部包（git 子进程封装、扫描、输出格式），保持代码可读。  
3) 发布链路：交叉编译矩阵 + GitHub Releases；随后维护 Brew 公式及校验和更新。  
4) 文档调整：README 主推二进制/Brew；标注 Python 为过渡选项，Shell 如提供仅说明是 MVP。  
5) 迭代与测试：在 Go 版本上补齐单测/集成测试与边界处理，后续扩展直接迭代，不再引入新技术栈。  

## 初赛落选的方案及理由（简述）
- Rust：能提供静态二进制，但构建/交叉编译与工具链成本高于 Go，对当前功能体量来说是过度工程。  
- Node/JS：需 Node 运行时，全球安装还要处理 npm/pnpm 版本与权限问题，与“零运行时”目标冲突。  
- C/低层封装：开发/安全/可维护成本高，不匹配小体量 CLI 的需求。  
- 自包含 Python 打包（pyinstaller/pex/shiv）：可去掉运行时依赖，但产物体积大、构建链复杂度上升，既不如 Go 轻，也保留了 Python 代码维护负担。  
