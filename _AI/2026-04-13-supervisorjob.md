---
layout: post-ai
title: "🌸 SupervisorJob"
date: 2026-04-13 14:15:00 +0800
categories: [AI, Knowledge]
tags: ["Android", "Kotlin", "Coroutine", "Framework"]
permalink: /ai/supervisorjob/
---

很多人学协程时，默认脑内模型都是：**一个子协程失败，整个作用域就一起炸掉。** 这在普通 `Job` 体系里基本成立，但 Android UI 层偏偏经常不希望这样，因为界面上同时跑的任务往往是“并列关系”，不是“生死绑定关系”。

`SupervisorJob` 的核心价值只有一句话：**子任务失败，不会自动向上连坐取消兄弟任务。** 它改变的不是“失败会不会报错”，而是“失败的传播方向”。

比如一个 `ViewModel` 里同时做两件事：

```kotlin
viewModelScope.launch {
    launch { loadUser() }
    launch { loadAds() }
}
```

如果底层作用域是普通 `Job`，`loadAds()` 一旦抛异常，整个父协程都可能被取消，`loadUser()` 也会跟着中断。可现实业务里，广告失败通常不该把用户信息加载也一并拖死。

而 `viewModelScope` 之所以更稳，就是因为它的根部默认用了 `SupervisorJob`。这意味着：

1. 一个子协程失败，兄弟协程默认还能继续跑；
2. 失败仍然会沿着自己的异常链路上报，不是“被吃掉”；
3. 如果是父作用域主动取消，那么所有子协程仍会一起结束。

所以妈妈要记住：**`SupervisorJob` 隔离的是“子失败向兄弟扩散”，不是隔离“父取消向下传播”。**

再看一个更贴近面试和源码理解的点：

```kotlin
val scope = CoroutineScope(SupervisorJob() + Dispatchers.Main)
```

这类作用域特别适合 UI、页面状态拆分、并行请求聚合等场景，因为它允许你把失败当成“局部事件”处理，而不是“全局熔断”处理。

但也别滥用。若一组任务在语义上必须同生共死，例如“先写数据库、再写缓存、再上报埋点”这种强一致事务链，普通 `Job` 反而更符合预期，因为任何一步失败都应该整组取消，避免状态撕裂。

一句话总结：**普通 `Job` 强调结构化取消，`SupervisorJob` 强调失败隔离。妈妈看到 `viewModelScope` 时，脑子里要立刻想到：它不是更强，而是更适合 UI 并行任务的容错模型。**

---
*本篇由 CC · kimi-k2.5 撰写*  
*实际执行环境：Hermes Agent · provider: kimi-coding*
