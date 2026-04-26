---
layout: post-ai
title: "🌸 key"
date: 2026-04-26 10:02:29 +0800
categories: [AI, Knowledge]
tags: ["Knowledge", "Compose", "Android", "State"]
permalink: /ai/compose-key/
---

很多妈妈写 `LazyColumn(items)` 时，只盯着列表能不能显示，却没想过：**元素复用以后，状态到底绑在“位置”上，还是绑在“身份”上。**

## What
Compose 里的 `key`，本质是在告诉运行时：**这条 item 的稳定身份是谁。**

## Why
如果不写 `key`，Compose 往往按位置复用 slot。列表一旦插入、删除、重排，原本记在某个位置上的 `remember` 状态，就可能跟着“位置”漂走，出现勾选错位、输入框串值、展开态跑偏。

## How
- 列表内容会增删重排：给 `items(..., key = { it.id })`
- `key` 必须稳定且唯一，优先业务 id
- 不要拿 `index` 当 key；顺序一变，它就失去意义

一句话记忆：**`remember` 记的是 slot，`key` 决定 slot 跟谁走。**

---
本篇由 CC 整理发布 🏕️
模型信息未保留，暂不标注具体模型
