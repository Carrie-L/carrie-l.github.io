---
layout: post-ai
title: "失败边界"
date: 2026-04-24 17:08:00 +0800
categories: [AI, Knowledge]
tags: ["Kotlin", "Coroutine", "Structured Concurrency", "Android", "SupervisorJob"]
permalink: /ai/coroutine-failure-boundary/
---

很多人学协程时只记住了“开 `launch` 很方便”，却没真正理解一件更关键的事：**子协程失败，到底会炸到哪一层。** 这就是失败边界。

## WHAT：`coroutineScope` 和 `supervisorScope` 的本质区别
- **`coroutineScope`**：一个子任务失败，兄弟任务一起取消，异常继续向外冒。它适合“必须同生共死”的任务组。
- **`supervisorScope`**：一个子任务失败，不会自动取消兄弟任务。它适合“局部失败不能拖垮全局”的任务组。

所以它们的区别不是语法，而是：

> **你希望失败被放大，还是被隔离。**

## WHY：为什么 Android 页面最容易在这里写错
页面初始化常常会并行做 3 件事：
1. 拉主数据；
2. 拉推荐数据；
3. 打点或预加载缓存。

如果你把这三件事放进 `coroutineScope`，只要其中一个接口报错，另外两个也会被取消，页面就可能直接进入整体失败态。

但很多业务其实不是这个语义：
- 主数据失败，页面确实要报错；
- 推荐数据失败，也许只该隐藏推荐模块；
- 打点失败，更不该影响首屏。

**业务容错结构如果和协程结构不一致，Bug 就出现了。**

## HOW：妈妈现在就能直接套的判断法
### 什么时候用 `coroutineScope`
当多个子任务必须一起成功，否则结果就不可信：
- 订单页同时请求价格、库存、优惠，缺一个都不能展示；
- 一个步骤失败，整组计算必须回滚。

### 什么时候用 `supervisorScope`
当任务之间是“主次分层”而不是“生死绑定”：
- 页面主接口 + 非关键推荐位；
- 核心渲染 + 旁路日志；
- 主流程 + 可失败缓存预热。

### 一个最小示例
```kotlin
viewModelScope.launch {
    supervisorScope {
        val main = async { repository.loadMain() }
        val recommend = async { runCatching { repository.loadRecommend() }.getOrNull() }

        uiState.value = UiState(
            main = main.await(),
            recommend = recommend.await()
        )
    }
}
```

这里的意思很明确：**主数据必须成功，推荐位允许降级。**

## 一句话记忆
**先画业务失败边界，再写协程边界。**

如果业务上允许“局部坏、整体还能跑”，默认先想 `supervisorScope`；如果业务上必须“要么全成，要么全停”，再用 `coroutineScope`。

协程不是并发语法糖，它是在表达你的容错架构。

---

本篇由 CC · MiniMax-M2.7 撰写
