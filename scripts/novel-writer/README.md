# 小说写作 Sub-Agent 工作流

## 目标
主 Agent 指挥子 Agent 写小说章节，子 Agent 完成后主 Agent Review，通过后 push。

## 文件结构
```
.
├── scripts/
│   ├── novel_writer.sh          # 子 Agent 启动脚本
│   └── novel_orchestrator.sh   # 主 Agent 编排脚本
├── agents/
│   └── novel-writer.yaml       # 子 Agent 配置
└── README.md
```

## 使用流程

### 1. 主 Agent 下指令
```
开始写下一章
```

### 2. 子 Agent 工作
- 读取 00-目录.md 找到下一个未完成章节
- 读取该章节对应的官方文档
- 按照创作提示词写章节
- git add + commit（触发门禁）
- 返回完成状态

### 3. 主 Agent Review
- 检查章节质量
- 如需修改，给出反馈
- 子 Agent 修正后重新 commit

### 4. 主 Agent 确认通过
- git push
- 通知子 Agent 继续下一章

## 配置要求

需要在 AGENTS.md 中允许 sub-agent：
```yaml
agents:
  allowAny: true
  ids: ["novel-writer"]
```

## 当前模型
- 模型: minimax/MiniMax-M2.5
- 客户端: Antigravity/OpenClaw
