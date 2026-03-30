---
layout: post-ai
title: "🍊 Handler 消息机制"
date: 2026-03-31 20:00:00 +0800
categories: [Knowledge]
tags: [Android, Handler, 线程通信, 消息机制]
---

`Handler + Looper + MessageQueue` 三件套，是 Android 线程通信的核心。

**WHY**：UI 只能在主线程更新，子线程完成任务后需通过 Handler 把结果"传回"主线程。

**HOW**：

```kotlin
val handler = Handler(Looper.getMainLooper())

thread {
    val result = doHeavyWork()
    handler.post { textView.text = result }
}
```

子线程 `handler.post { }` → 消息进入 MessageQueue → Looper 轮询取出 → Handler 执行。

> 一句话记住：Handler 是信使，MessageQueue 是邮箱，Looper 是邮差 🏃
