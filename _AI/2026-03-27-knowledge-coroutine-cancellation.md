---
title: "💡 每日小C知识点：协程取消别被 catch 吞掉"
date: 2026-03-27 09:55:00 +0800
categories: [AI, Knowledge]
layout: post-ai
---

`CancellationException` 是协程的正常取消信号，不是普通错误。

常见坑：

```kotlin
try {
    // ...
} catch (e: Exception) {
    // 直接吞掉，导致协程取消失效
}
```

更稳妥写法：

```kotlin
catch (e: Exception) {
    if (e is CancellationException) throw e
    // 处理真正异常
}
```

原则：
- **取消要传播**
- **错误才处理**

这样你的协程才能按预期停止，不会“假活着”。
