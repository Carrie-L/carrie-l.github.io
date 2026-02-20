# 章节创作流水线（Main Agent + Writer Subagent）

## 架构

| 角色 | 职责 | 禁止 |
|------|------|------|
| **Main Agent** (编排者) | 审查、push、派发任务 | ❌ 写/改小说正文 |
| **Writer Subagent** (写作者) | 写章节、修订、git add/commit | ❌ git push |

## 流程
1. Main Agent 读取 `Contents/00-目录.md`，找到下一个 `[ ]` 章节
2. Main Agent 派发写作任务给 Writer Subagent
3. Writer Subagent 按《创作提示词》写章节
4. Writer Subagent 执行 `git add` + `git commit`（触发 pre-commit 门禁）
5. 若 pre-commit FAIL：Writer 自行修改 → 重新 commit
6. commit 成功后，Main Agent 按《章节审查提示词》执行内容级审查
7. 若 FAIL：Main Agent 发修订指令（附具体原因）→ Writer 修改 → 重新 commit → 回到步骤 6
8. PASS → Main Agent 执行 `git push`
9. 自动开始下一章（回到步骤 1）

## 审查层级

### 第一层：自动门禁（pre-commit hook）
- `review/scripts/sync_toc_status.ps1`：目录状态同步
- `review/scripts/review_changed_chapters.ps1`：结构/格式检查
- 由 Writer Subagent 的 `git commit` 自动触发
- FAIL 时 commit 被阻止，Writer 需自行修复

### 第二层：内容审查（Main Agent）
- 按 `review/《…》章节审查提示词.md` 检查
- 核心策略：**3分风景，7分技术**
- 检查技术准确性、文风、连贯性、Task 可执行性
- FAIL 时派发修订任务给 Writer

## 创作规范来源
- `Contents/《美少女的Android摇曳露营奇遇记》创作提示词.md`

## status 字段规则（必填）

- **draft**：骨架/未写
- **done**：AI 写完必须设为 `done`，触发 review
- **published**：审查通过且 push 后改为 `published`，不再参与后续 review

## 审查门槛（硬门禁）
以下任一不满足即 FAIL：
- 场景/人物连贯性破坏
- 格式违反既定规则
- 代码注释不够新手友好
- Task 不可执行或验收模糊
- 比喻滥用/术语不清
- 缺乏环境描写/阅读疲劳

## 备注
- Main Agent 是"质量门禁 + 发布者"，不是第二个作者
- Writer Subagent 是唯一写小说的角色
- 遇到 "continue" 指令时，Main Agent 先检查状态再决定行动
