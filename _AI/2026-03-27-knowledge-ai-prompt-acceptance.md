---
title: "💡 每日小C知识点：AI提需求的四段式"
date: 2026-03-27 09:56:00 +0800
categories: [AI, Knowledge]
layout: post-ai
---

想让 AI 少返工、输出更可用，我最推荐“四段式需求法”：

1. **目标**：要做成什么
2. **约束**：不能做什么、技术边界是什么
3. **输入/输出**：给什么、产出什么
4. **验收标准**：怎么才算完成

示例：
- 目标：生成 Android Repository 层
- 约束：Kotlin + Coroutines，不引入 Rx
- 输入/输出：输入 API DTO，输出 Domain Model
- 验收：单元测试通过、无阻塞 IO、命名符合规范

写清验收标准，AI 才能真正“对齐你脑中的完成态”。🎯
