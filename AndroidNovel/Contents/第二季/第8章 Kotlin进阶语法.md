---
chapter_id: '8'
title: '第八课：Kotlin 进阶语法 · 高级特性'
official_url: 'https://kotlinlang.org/docs/advanced-types.html'
status: 'done'
<parameter name="author">'minimax m2.5 - OpenClaw'
plot_summary:
  time: '第三十三天'
  location: 'Compose 村·高级教室'
  scene: '小 Com 教小满 Kotlin 高级特性'
  season: '春季'
  environment: '高级教室里各种高级知识'
---

# 第八课：Kotlin 进阶语法 · 高级特性

---

“叮——”

林小满发现自己站在一个高级教室里。黑板上写着各种高级语法。

“今天我们要学 Kotlin 高级语法！”小 Com 走了过来，“学会这些，你的 Kotlin 水平会更高！”

“高级语法？”林问。

“对！”小 Com 说，“高阶函数、扩展、内联……都是 Kotlin 的精髓！”

---

## 1. 高阶函数

“高阶函数是函数式编程的核心。”小 Com 展示了：

```kotlin
// 高阶函数：接收函数作为参数
fun executeTwice(block: () -> Unit) {
    block()
    block()
}

// 使用
executeTwice {
    println("Hello")
}

// 返回函数
fun multiplier(factor: Int): (Int) -> Int {
    return { number -> number * factor }
}

val double = multiplier(2)
println(double(5))  // 10
```

---

## 2. lambda 表达式

“lambda 是匿名函数。”小 Com 展示了：

```kotlin
// 基本语法
val lambda: (Int, Int) -> Int = { a, b -> a + b }

// 简写
val sum = { a: Int, b: Int -> a + b }

// it 参数（单参数时）
val list = listOf(1, 2, 3)
val doubled = list.map { it * 2 }

// 方法引用
val list2 = list.map(String::toString)
```

---

## 3. 内联函数

“内联可以减少函数调用开销。”小 Com 展示了：

```kotlin
// 普通函数：有调用开销
inline fun repeat(times: Int, block: () -> Unit) {
    for (i in 0 until times) {
        block()
    }
}

// noinline：不内联
inline fun example(noinline block: () -> Unit) {
    block()
}

// crossinline：不允许直接返回
inline fun example(crossinline block: () -> Unit) {
    block()
}
```

---

## 4. 扩展函数

“扩展函数给现有类添加方法。”小 Com 展示了：

```kotlin
// 扩展函数
fun String.addExclamation(): String {
    return this + "!"
}

// 使用
"Hello".addExclamation()  // "Hello!"

// 扩展属性
val String.lastChar: Char
    get() = this[length - 1]

// "Kotlin".lastChar  // 'n'
```

---

## 5. 泛型

“泛型让代码更灵活。”小 Com 展示了：

```kotlin
// 泛型类
class Box<T>(val value: T) {
    fun get(): T = value
}

// 泛型函数
fun <T> first(list: List<T>): T? = list.firstOrNull()

// 泛型约束
fun <T : Number> sum(list: List<T>): Double {
    return list.sumOf { it.toDouble() }
}

// 多重约束
fun <T> ensureNotNull(value: T?) where T : CharSequence, T : Comparable<T> {
    // ...
}
```

---

## 6. 协程与 Flow

“协程和 Flow 是 Kotlin 的异步神器。”小 Com 展示了：

```kotlin
// Flow 构建器
val flow = flow {
    for (i in 1..3) {
        emit(i)
        delay(100)
    }
}

// 操作符
val result = flow
    .map { it * 2 }
    .filter { it > 2 }
    .take(2)

// 协程作用域
viewModelScope.launch {
    flow.collect { value ->
        println(value)
    }
}
```

---

## 7. 序列

“序列比集合更高效。”小 Com 展示了：

```kotlin
// 集合：立即执行
listOf(1, 2, 3, 4, 5)
    .map { it * 2 }
    .filter { it > 4 }

// 序列：惰性执行（更高效）
sequenceOf(1, 2, 3, 4, 5)
    .map { it * 2 }
    .filter { it > 4 }
    .toList()
```

---

## 8. 委托

“委托是代码复用的神器。”小 Com 展示了：

```kotlin
// 属性委托
class Delegate {
    operator fun getValue(thisRef: Any?, property: KProperty<*>): String {
        return "${property.name} = $thisRef"
    }
    
    operator fun setValue(thisRef: Any?, property: KProperty<*>, value: String) {
        println("${property.name} = $value")
    }
}

class Example {
    var prop: String by Delegate()
}

// lazy 委托
val lazyValue: String by lazy {
    println("computed!")
    "Hello"
}

// observable 委托
var observable by Delegates.observable("初始值") { prop, old, new ->
    println("${prop.name}: $old -> $new")
}
```

---

## 9. 注解与反射

“注解和反射用于元编程。”小 Com 展示了：

```kotlin
// 定义注解
@Target(AnnotationTarget.CLASS, AnnotationTarget.FUNCTION)
@Retention(AnnotationRetention.RUNTIME)
annotation class MyAnnotation(val value: String)

// 使用注解
@MyAnnotation("example")
class MyClass {
    @MyAnnotation("method")
    fun myMethod() {}
}

// 反射获取注解
val annotation = MyClass::class.java.getAnnotation(MyAnnotation::class.java)
println(annotation?.value)  // "example"
```

---

## 10. DSL 构建

“DSL 让代码更简洁。”小 Com 展示了：

```kotlin
// 定义 DSL
class HtmlBuilder {
    private val elements = mutableListOf<String>()
    
    fun p(text: String) {
        elements.add("<p>$text</p>")
    }
    
    fun build() = elements.joinToString("\n")
}

fun html(block: HtmlBuilder.() -> Unit): String {
    return HtmlBuilder().apply(block).build()
}

// 使用
val html = html {
    p("Hello")
    p("World")
}
```

---

## 本课小结

今天林小满学到了：

1. **高阶函数**：函数作为参数和返回值
2. **lambda**：匿名函数
3. **内联**：减少调用开销
4. **扩展**：给现有类添加方法
5. **泛型**：类型参数化
6. **序列**：惰性执行
7. **委托**：代码复用
8. **注解与反射**：元编程
9. **DSL**：领域特定语言

---

“Kotlin 高级语法太强大了！”林小满说。

“没错！”小 Com 说，“学会这些，你的 Kotlin 水平就很高了！”

---

*”叮——“*

手机通知：**“第二季第八章 已解锁：Kotlin 进阶语法”**

---

## 🎉 第二季也完结啦！

---

**第二季内容回顾**：

| 章节 | 主题 |
|------|------|
| 1 | Compose Multiplatform 入门 |
| 2 | 共享 ViewModel 与数据层 |
| 3 | Kotlin 协程底层原理 |
| 4 | AOSP 入门 |
| 5 | Hook 与插件化 |
| 6 | 逆向工程基础 |
| 7 | 安全与加解密 |
| 8 | Kotlin 进阶语法 |

---

**学完两季，你已经掌握了：**

- ✅ Jetpack Compose 基础 → 高级
- ✅ MVVM 架构与工程实践
- ✅ 网络、数据库、DI
- ✅ 跨平台开发 (Multiplatform)
- ✅ 系统原理 (AOSP)
- ✅ Hook 与逆向
- ✅ 安全与加密
- ✅ Kotlin 高级语法

---

**接下来你想学什么？** 🎯
- 音视频开发
- AR/VR 开发
- Flutter 跨平台
- 其他方向

随时告诉我！ 🚀
