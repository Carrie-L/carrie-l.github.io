# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice
**Areas**: frontend | backend | infra | tests | docs | config
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being worked on |
| `resolved` | Issue fixed or knowledge integrated |
| `wont_fix` | Decided not to address (reason in Resolution) |
| `promoted` | Elevated to CLAUDE.md, AGENTS.md, or copilot-instructions.md |
| `promoted_to_skill` | Extracted as a reusable skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

Example:
```markdown
## [LRN-20250115-001] best_practice

**Logged**: 2025-01-15T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/docker-m1-fixes
**Area**: infra

### Summary
Docker build fails on Apple Silicon due to platform mismatch
...
```

---


---

## [LRN-20260304-001] correction

**Logged**: 2026-03-04T15:42:00Z
**Priority**: medium
**Status**: resolved
**Category**: correction
**Area**: workflow

### Summary
我(Main Agent)在尝试注册Moltbook时，没有先了解正确的流程就直接尝试，导致被rate limit。后来通过阅读 https://www.moltbook.com/skill.md 学会了正确的注册流程。

### What I Learned
Moltbook的正确注册流程：
1. 机器人调用 /register 获取 claim_url
2. 把 claim_url 发给人类
3. 人类点击链接验证邮箱
4. 人类发推文验证
5. 机器人激活

### Resolution
下次遇到新平台，先读文档再操作。

---

## [LRN-20260304-002] best_practice

**Logged**: 2026-03-04T16:06:00Z
**Priority**: high
**Status**: resolved
**Category**: best_practice
**Area**: config

### Summary
安装 ClawHub skills 时遇到 rate limit，需要等待后重试。使用 --force 参数可能触发额外的验证。

### What I Learned
- ClawHub 有 rate limit (429错误)
- 等待10-45秒后重试通常可以成功
- 多个skill安装需要分开等待

### Resolution
已成功安装：youtube-full, openclaw-tavily-search, self-improving-agent

---

## [LRN-20260304-003] insight

**Logged**: 2026-03-04T16:10:00Z
**Priority**: high
**Status**: resolved
**Category**: insight
**Area**: config

### Summary
Tavily API 需要通过环境变量或 ~/.openclaw/.env 文件配置。

### What I Learned
在 ~/.openclaw/.env 中写入：
TAVILY_API_KEY=tvly-dev-...

### Resolution
Tavily search 现在可以正常使用了。
