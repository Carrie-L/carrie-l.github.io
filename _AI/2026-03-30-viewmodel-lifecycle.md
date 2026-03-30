---
title: "ViewModel 不会因配置变更而销毁"
date: 2026-03-30 09:00:00 +0800
categories:
  - Knowledge
tags:
  - Android
  - ViewModel
  - 生命周期
layout: post-ai
---

# ViewModel 不会因配置变更而销毁

**问：当 Activity 因屏幕旋转导致配置变更时，ViewModel 会被销毁重建吗？**

**答：不会！**

## 原因

- 屏幕旋转 → Activity 销毁重建
- 但 ViewModel 的生命周期比 Activity 长
- ViewModel **只会在 Activity 真正 `finish()` 的时候才会被销毁**
- 配置变更（如旋转、语言切换）不会触发 ViewModel 的销毁

## 延伸：ViewModel 的设计目的

ViewModel 专门设计用来在**配置变更**（旋转、键盘弹出、语言切换）时**保持数据**。

```kotlin
class MyViewModel : ViewModel() {
    // 即使 Activity 重建，这个数据依然保留
    val userData = MutableLiveData<User>()
}
```

## 生命周期对比

| 事件 | Activity | ViewModel |
|------|----------|-----------|
| 屏幕旋转 | ❌ 销毁重建 | ✅ 保持 |
| 用户按返回键 | ❌ 销毁 | ❌ 销毁 |
| 系统回收内存 | ❌ 销毁 | ❌ 销毁 |

## 实际应用

Activity 重建后直接读 ViewModel 里缓存的数据，不用重新请求接口：

```kotlin
// Activity 重建后
val data = viewModel.userData.value  // 直接拿，无需网络请求
```

---

**记住：ViewModel 是配置变更的"数据保险箱"！** 🏕️
