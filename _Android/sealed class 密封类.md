---
layout: article
title: "sealed class 密封类"
date: 2025-07-16
permalink: /android/sealed-class-mi-feng-lei/
tags: ["kotlin", "Android"]
---

 

sealed class 定义了一个“加强版”的枚举类。为什么说是“加强”？

因为它可以携带状态 (`Stateful`) , 子类可以是 `data class` 、`object` 或 `class` 。

它的核心作用是定义一个**严格的、有限的、可继承的类层级结构**。

等于在告诉编辑器，这个类**只能**有我在这里定义的这几个子类，不允许有任何其它未知的新子类出现。

### 核心特性

#### 1. 受限制的继承  (Restricted Inheritance)

一个密封类的所有直接子类都必须定义在与它**同一个文件中、或同一个包/模块类**。但通常为了清晰，还是放在同一个文件中。

#### 2. when 表达式的详尽性检查 (Exhaustive when)

这是密封类最强大的优势。因为编辑器知道它的所有子类，所有如果代码里没有对所有子类进行处理，将无法通过编译。

例如：

```kotlin
sealed class NetworkState {
    object Loading : NetworkState()
    data class Success(val data: String) : NetworkState()
    data class Error(val message: String) : NetworkState()
    // 假设你后来新增了一个状态
    object Retrying : NetworkState() 
}

fun handleState(state: NetworkState) {
    when (state) { // 如果你不写 Retrying 分支，这里会报错！
        is NetworkState.Loading -> println("加载中...")
        is NetworkState.Success -> println("成功: ${state.data}")
        is NetworkState.Error -> println("失败: ${state.message}")
        is NetworkState.Retrying -> println("正在重试...") // 必须处理，否则编译不通过
    }
}
```

#### 3. 可以携带状态 (Stateful)

这是它相比于枚举（Enum）的最大优势。

*   **枚举（Enum）** 的每个成员都是一个**单例对象**，它们不能携带不同的实例数据。
*   **密封类（Sealed Class）** 的子类可以是 `data class`、`object` 或普通的 `class`。这意味着每个子类都可以有自己独特的属性和状态。

在上面的例子中：

*   `Success` 是一个 `data class`，它携带了成功时获取的 `data` 数据。
*   `Error` 也是一个 `data class`，它携带了错误信息 `message`。
*   `Loading` 和 `Retrying` 是 `object`，因为它们只是一个状态，不需要携带额外的数据。

### sealed class VS enum

| 特性         | `enum class` (枚举类)            | `sealed class` (密封类)                 |
| :--------- | :---------------------------- | :----------------------------------- |
| **本质**     | 一组固定的**常量实例**                 | 一个固定的、可继承的**类型层级**                   |
| **实例**     | 每个成员都是一个单例对象                  | 子类可以有多个不同的实例                         |
| **携带数据**   | 所有成员结构相同，可以有属性，但不能为不同成员定义不同状态 | **不同子类可以有完全不同的属性和状态** (`data class`) |
| **`when`** | 支持详尽性检查                       | **支持详尽性检查（核心优势）**                    |
| **继承**     | 不能被继承                         | 必须在同一文件/包/模块内被继承                     |
### 什么时候使用密封类？

当你想表示一个来自**有限集合**中的**状态或结果**，并且每种状态可能需要携带不同的数据时，密封类就是最佳选择。

应用场景举例：

1.  **管理 UI 状态**：如 `Loading`, `Success(data)`, `Error(message)`。

2.  **表示操作结果**：如 `LoginResult.Success(userProfile)`, `LoginResult.Failure(errorType)`。

3.  **模块间通信**：用它来定义模块间传递的事件，既清晰又类型安全。
