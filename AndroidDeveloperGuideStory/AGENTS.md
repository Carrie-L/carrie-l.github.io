# AGENTS.md — 《美少女的Android摇曳露营奇遇记》

本文件为 AI Agent 在本仓库中的行为规范。请在每次会话开始时阅读本文件。

## 项目概述

本仓库是技术教学小说《美少女的Android摇曳露营奇遇记》的创作仓库。将 Android 官方开发文档转化为二次元西幻露营风格的教学小说。

## 目录结构

```
AndroidDeveloperGuideStory/
├── Contents/                    # 章节正文（核心产出）
│   ├── 00-目录.md               # 章节目录（自动同步状态）
│   └── 1.x.x *.md              # 各章节文件
├── Contents/《…》创作提示词.md    # Writer Agent 的系统指令
├── review/                      # 审查相关（全部集中在此）
│   ├── CONTRIBUTING.md          # 提交规范
│   ├── WORKFLOW-审查流水线.md    # 审查流程说明
│   ├── 《…》章节审查提示词.md    # Reviewer Agent 的系统指令
│   └── scripts/                 # 自动化脚本
│       ├── review_changed_chapters.ps1   # 章节审查门禁
│       └── sync_toc_status.ps1           # 目录状态同步
├── Styles/                      # 风格参考素材
└── AGENTS.md                    # 本文件
```

## Agent 角色分工（双 Agent 架构）

### Main Agent（编排者 / Orchestrator）

> **Main Agent 绝不亲自写章节内容。**

- **职责**：
  1. 读取 `Contents/00-目录.md` 确认下一个待写章节
  2. 派发写作任务给 Writer Subagent
  3. Writer commit 后，按 `review/《…》章节审查提示词.md` 审查章节
  4. 审查 PASS → `git push`
  5. 审查 FAIL → 发修订指令给 Writer Subagent（附具体 FAIL 原因）
  6. 循环直到 PASS 后开始下一章

- **审查触发方式**：
  - `pre-commit` hook 自动调用 `review/scripts/review_changed_chapters.ps1`（基础门禁）
  - Main Agent 额外按审查提示词做内容级审查（文风、技术准确性、连贯性）

- **关键规则**：
  - ❌ 不写小说 ❌ 不改正文 ❌ 不跳过审查直接 push
  - 遇到中断/错误时：先 `git status` + `git log -1` 判断状态，再决定行动

### Writer Subagent（写作者）

- **职责**：根据 `Contents/《…》创作提示词.md` 的规范创作章节
- **输入**：章节编号、官方文档 URL、上一章 plot_summary、**现有文件路径**
- **输出**：符合六段式结构的完整章节文件
- **关键规则**：
  - **覆写现有文件**：`Contents/` 下已预建好所有章节 md 文件（带 YAML frontmatter 和骨架），Writer 必须写入这个现有文件，**绝不新建文件**。文件名可能是英文，以章节号数字匹配为准（如 `13.1.12`）。
  - 写作前必读 `Contents/00-目录.md` 确认章节顺序
  - 必读 `Contents/《…》创作提示词.md` 确认创作规范
  - 必读上一章节 YAML 元数据 `plot_summary` 对象，确保场景/人物/时间线连贯
  - **"上一章"定义**：同一卷中章节号紧邻本章之前的章节（6.1.2 → 6.1.1）。卷首章节看上一卷最后一章；上一卷未写时本章为"本卷开篇"，可自由定义时间/地点/季节。并行写作时各章只看自己的上一章。
  - 必读章节 YAML 中的 `official_url` 对应的官方文档，以此为内容基础改编
  - 保留现有文件中的 `chapter_id`、`official_url` 等 YAML 字段
  - 小说正文 ≥ 2000 字（不含技术总结、代码、注释）
  - 每章至少 2 幅 mermaid 图示
  - 每章 8 道 Task + 5 道面试题
  - **连贯性检查（强制）**：
    - 输出 YAML 必须包含 `plot_summary` 对象（time/location/scene/season/environment 必填）
    - 季节只能前进或保持，不能来回跳（秋→冬 OK；秋→冬→秋 FAIL）
    - 地点变化时正文必须有过渡描写
    - 时间自然推进（下午→傍晚 OK；下午→上午 FAIL）
  - 写完后执行 `git add . && git commit -m "feat(chapter-X.X.X): English summary"` — **commit message 必须全英文**（避免 push 乱码）
  - **❌ 不执行 git push** — push 由 Main Agent 负责

## Main Agent 派发任务时的关键步骤

**Main Agent 在派发写作任务前，必须：**
1. 读取上一章文件，提取其 YAML 中的 `plot_summary`
2. 将 `plot_summary` 完整粘贴到 subagent 任务描述中
3. 明确告知 Writer：本章的季节/地点/时间必须与上一章衔接

## 标准工作流

```
Main Agent                          Writer Subagent
    │                                      │
    ├─ 1. 读 00-目录.md，找到下一个 [ ] 章节    │
    ├─ 1.5 读取上一章的 plot_summary           │
    ├─ 2. 构建写作任务（附上一章 plot_summary），│
    │     派发给 Writer ─────────────────────→│
    │                                      ├─ 3. 读创作提示词 + 任务中的上一章 plot_summary
    │                                      ├─ 4. 读 official_url 官方文档
    │                                      ├─ 5. 写章节 + 更新 plot_summary
    │                                      ├─ 6. git add + git commit
    │                                      │     (pre-commit 自动门禁)
    │                                      ├─ 7. 门禁 FAIL → 自行修改 → 重新 commit
    │  ←── 8. commit 成功，返回结果 ──────────┤
    ├─ 9. 按审查提示词执行内容级审查             │
    ├─ 10. PASS → git push                   │
    │       FAIL → 发修订指令 ─────────────→│
    │                                      ├─ 11. 根据反馈修改 → 重新 commit
    │  ←── 12. 修订完成 ──────────────────────┤
    ├─ 13. 再次审查 → 循环直到 PASS             │
    ├─ 14. git push                          │
    ├─ 15. 回到步骤 1，开始下一章               │
    └───────────────────────────────────────┘
```

### 如果 review FAIL

1. Main Agent 描述具体 FAIL 原因
2. 派发修订任务给 Writer Subagent（附 FAIL 原因）
3. Writer 修订后重新 `git add` → `git commit`
4. Main Agent 重新审查
5. 循环直到 PASS

## Git 规范

- **Commit message 必须全英文**，避免 push 时乱码。
- 提交格式：`feat(chapter-1.x.x): English summary`
- 批量提交示例：`feat: add chapters 1.8.1-1.8.2 (batch 5: sharing simple data)`
- 每批完成后立即 push
- 详见 `review/CONTRIBUTING.md`

## 关键文件引用

| 用途 | 路径 |
|------|------|
| 创作规范 | `Contents/《…》创作提示词.md` |
| 审查规范 | `review/《…》章节审查提示词.md` |
| 审查流程 | `review/WORKFLOW-审查流水线.md` |
| 提交规范 | `review/CONTRIBUTING.md` |
| 章节目录 | `Contents/00-目录.md` |
| 审查脚本 | `review/scripts/review_changed_chapters.ps1` |
| 目录同步 | `review/scripts/sync_toc_status.ps1` |
| Git Hooks | `.githooks/pre-commit`, `.githooks/pre-push` |
