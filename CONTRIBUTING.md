# CONTRIBUTING.md

本仓库用于《美少女的Android摇曳露营奇遇记》创作与维护。
目标：可追溯、可回滚、低噪音版本管理。

## 1. 提交原则

不要“每改一行就提交”。
采用：**最小完整单元提交（Atomic Commit）**。

满足以下任一条件应提交一次：
- 完成一个章节草稿/定稿
- 完成一次明确返工（文风、结构、连贯性）
- 修复一个明确问题（格式、编号、链接、逻辑）
- 新增或修改流程文档（提示词、审查规则、工作流）

## 2. 提交信息规范

**⚠️ Commit message 必须使用全英文**，避免 push 时出现乱码（Windows/Git 编码问题）。

格式：

`type(scope): summary`

### type
- `feat`：新增内容（如新增章节）
- `fix`：修复问题
- `refactor`：重构（不改核心结论，改表达/结构）
- `docs`：文档与规则
- `chore`：杂务（如 .gitignore、目录整理）

### scope（建议）
- `chapter-1.6.1`
- `workflow`
- `prompt-reviewer`
- `repo`

### 示例
- `feat(chapter-1.6.2): draft Room entity chapter`
- `refactor(chapter-1.6.1): improve narrative tone and humor`
- `fix(chapter-1.6.1): align tasks with executable acceptance criteria`
- `docs(workflow): add reviewer pass/fail gate`
- `chore(repo): update gitignore`

## 3. 推送（Push）策略

默认：每 1~3 个提交 push 一次。

以下场景必须立即 push：
- 一章定稿
- 大改完成并通过审查
- 当天收工前
- 跨设备协作前

## 4. 分支策略

默认主分支：`main`

大改建议开短分支：
- `rewrite/1.6.1-tone`
- `feature/1.6.2-entities`

完成后合并回 `main`。

## 5. 章节流水线（强制）

每章遵循：
1. 写作（Writer）
2. 审查（Reviewer，PASS/FAIL）
3. FAIL 则修订并复审
4. PASS 才进入下一章

参考文件：
- `AndroidDeveloperGuideStory/SystemPrompts/《美少女的Android摇曳露营奇遇记》章节审查提示词.md`
- `AndroidDeveloperGuideStory/WORKFLOW-审查流水线.md`

### 自动门禁补充
- 目录文件：`AndroidDeveloperGuideStory/Contents/00-目录.md`
- 目录条目建议统一为复选框格式：`- [ ] \'章节文件名\'`
- `pre-commit` 会运行 `scripts/sync_toc_status.ps1`：
  - 章节 frontmatter `status: 'done'` -> 目录对应条目标记为 `- [x]`
  - 其他状态 -> `- [ ]`
- 写完一章并设为 `done` 后，提交时会自动同步目录进度。- `AndroidDeveloperGuideStory/SystemPrompts/《美少女的Android摇曳露营奇遇记》创作提示词.md`

## 6. 禁止事项

- 把多个无关改动塞进一个提交
- 未审查通过就跨章节推进
- 直接在正文重复 YAML 已有信息（如官方链接）

## 7. 最佳实践

- 每次提交前自问：这次改动能否一句话说清？
- 保持提交历史可读：让未来自己能看懂“为什么改”
- 小步快跑，持续可回滚
