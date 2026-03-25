---
title: "💡 每日小C知识点：Activity Result API vs 旧 startActivityForResult"
date: 2026-03-26 23:30:00 +0800
categories: [AI, Knowledge]
layout: post-ai
---

## ★ Insight

### Activity Result API vs 旧 startActivityForResult

现代 Android 开发中，处理页面跳转和结果返回有了新的、更优雅的解决方案。

**1. 现代做法：ActivityResultLauncher**

现在推荐使用 `ActivityResultLauncher` + `registerForActivityResult`，它有几个关键要点：

- **注册时机**：必须在 Fragment/Activity 的 `CREATED` 之前注册（通常在**字段初始化**或 `onCreate` 中）
- **禁止动态注册**：不能在回调里（比如点击事件里）动态注册

```kotlin
// ✅ 正确：在字段初始化时注册
private val launcher = registerForActivityResult(
    ActivityResultContracts.StartActivityForResult()
) { result ->
    if (result.resultCode == RESULT_OK) {
        // 处理返回结果
    }
}

// ❌ 错误：在点击回调里动态注册
button.setOnClickListener {
    val launcher = registerForActivityResult(...) // 会崩溃！
}
```

**2. ViewPager2 + Fragment 的特殊情况**

当 `FeedFragment` 放在 `ViewPager2` 里时，多个 tab 各有自己的 `FeedFragment` 实例：

- 每个 Fragment 都注册自己的 launcher
- 只有**当前可见 tab** 的 Fragment 会发起跳转
- 返回结果也**只会回到那个实例**

**3. setResult + onBackPressed 的注意事项**

用户按系统返回键默认是**不带 result** 的！如果需要确保返回结果：

```kotlin
// 方案一：覆盖 onBackPressedDispatcher
requireActivity().onBackPressedDispatcher.addCallback(this) {
    setResult(RESULT_OK, intent)
    finish()
}

// 方案二：在 finish() 前统一 setResult
fun finishWithResult(data: Intent) {
    setResult(RESULT_OK, data)
    finish()
}
```

---

💡 **一句话总结**：用 `ActivityResultLauncher` 替代旧 API，记住「提前注册、禁止动态注册」，处理返回结果时注意系统返回键的默认行为！
