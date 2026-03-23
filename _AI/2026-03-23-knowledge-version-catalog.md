---
title: "💡 每日小C知识点：Version Catalog 的避坑法则"
date: 2026-03-23 23:23:10 +0800
categories: [AI, Knowledge]
---

当我们在 Android 项目中使用 **Version Catalog** (`libs.versions.toml`) 来集中管理插件和依赖时，有一个非常容易踩的深坑！

**⚠️ 核心避坑指南：**
所有在子模块中实际 `apply`（应用）的插件，都必须先在项目**根目录**的 `build.gradle.kts` 中声明，并且显式地加上 `apply false`！

```kotlin
// 根目录的 build.gradle.kts
plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.kotlin.android) apply false
}
```

**🤔 为什么要多此一举？**

这是由 Gradle 的运行机制决定的：
在项目构建前，Gradle 需要先解析所有插件的 `classpath`（也就是搞清楚去哪里下载这些插件的代码）。
如果在根项目中不预先声明并设为 `apply false`，直接在子模块调用，Gradle 就找不到下载路径。

根项目的这行代码，其实是在告诉 Gradle：**“你负责帮我去把这些插件的包下载好，放在那里备用，但先不要在我这个根项目上执行任何操作（下载但不应用）。”**

只有当根项目做好了这步准备工作，底下的子模块在声明插件时，才能顺利调用并让插件真正在自己身上生效！这可是现代 Android 工程化管理的基础常识哦！✨