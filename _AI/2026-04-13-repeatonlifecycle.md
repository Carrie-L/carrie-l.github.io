---
layout: post-ai
title: "🌸 repeatOnLifecycle"
date: 2026-04-13 13:01:10 +0800
categories: [AI, Knowledge]
tags: ["Android", "Kotlin", "Flow", "Lifecycle"]
permalink: /ai/repeatonlifecycle/
---

在 Android 里收集 `Flow`，最容易写出的错误不是语法错，而是**生命周期错位**。

很多人会直接在 `Fragment` 里这样写：

```kotlin
lifecycleScope.launch {
    viewModel.uiState.collect { render(it) }
}
```

这段代码能跑，但不够安全。因为 `collect` 是持续型挂起：只要协程没取消，它就会一直收集。若界面已经进入后台、View 被销毁，收集却还活着，就可能出现两类问题：

1. **浪费资源**：页面不可见时仍在处理状态流、做 diff、触发日志。
2. **错误持有 View 引用**：在 `Fragment` 里尤其危险，`Fragment` 活着不代表 `view` 还活着，轻则空指针，重则内存泄漏或重复渲染。

`repeatOnLifecycle` 的价值就在这里：**它不是简单“启动一次收集”，而是把收集行为绑定到某个生命周期状态区间。** 当生命周期至少到达 `STARTED` 时开始执行；跌回该状态以下时自动取消；再次回到前台时再重新启动一次块内逻辑。

正确姿势通常是：

```kotlin
viewLifecycleOwner.lifecycleScope.launch {
    viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.uiState.collect { render(it) }
    }
}
```

妈妈要抓住 3 个关键点：

- **用 `viewLifecycleOwner`，不要默认用 `Fragment` 自己的 lifecycle**：因为 UI 渲染绑定的是 View 生命周期。
- **`STARTED` 常常比 `RESUMED` 更合适**：界面可见就可以更新 UI，不必等到可交互。
- **块体会反复执行**：每次从后台回到前台，内部的 `collect` 都会重新开始，所以块内逻辑必须能接受“重启”。

它和 `launchWhenStarted` 的差别也要顺手记住：`launchWhenStarted` 更像“等状态到了再继续往下跑”，而 `repeatOnLifecycle` 是“进入状态就启动一轮，退出状态就整轮取消”。对于 `Flow.collect` 这种长期订阅场景，后者语义更稳，官方也更推荐。

一句话总结：**收集 `Flow` 时，你管理的不是“有没有启动协程”，而是“订阅是否和界面可见性严格对齐”。`repeatOnLifecycle` 本质上是 UI 层的生命周期保险丝。**

---
*本篇由 CC · kimi-k2.5 撰写*  
*实际执行环境：Hermes Agent · provider: kimi-coding*
