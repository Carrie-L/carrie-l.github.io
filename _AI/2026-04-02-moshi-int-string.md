---
title: "Moshi解析JSON：int字段返回4.0的问题"
date: 2026-04-02 09:00:00 +0800
categories:
  - Knowledge
tags:
  - Kotlin
  - Moshi
  - JSON
layout: post-ai
---

# Moshi解析JSON：int字段返回4.0的问题

## 问题描述

用 Moshi 解析 JSON 时，明明返回的是 `4`，但解析出来是 `4.0`！

```kotlin
data class Response(
    val count: Int?
)

// JSON: {"count": 4}
// 解析结果: count = 4.0 ❌
```

## 根本原因

**JSON 本身没有整数类型！** JSON 规范里所有数字都是"数字"（类似 JavaScript 的 Number，是浮点数）。

Moshi 在解析时，如果遇到 `4.0`，有时候会先转成 `Double`，然后再尝试转成 `Int`。但 Kotlin 的类型推断出问题，就会保留 `Double`。

## 解决方案

### 方案1：改成 Double? 或 Long?

```kotlin
data class Response(
    val count: Double?  // 或者 Long?
)
```

### 方案2：自定义 JsonAdapter 处理 Int/String 兼容

```kotlin
@JsonQualifier
@Retention(RetentionPolicy.RUNTIME)
annotation class IntOrString

class IntOrStringAdapter {
    @FromJson(IntOrString::class) 
    fun fromJson(reader: JsonReader): Any {
        return when (reader.peek()) {
            JsonReader.Token.NUMBER -> reader.nextDouble()
            JsonReader.Token.STRING -> reader.nextString()
            else -> throw IllegalStateException("Expected NUMBER or STRING")
        }
    }
    
    @ToJson(IntOrString::class)
    fun toJson(writer: JsonWriter, value: Any?) {
        when (value) {
            is Int -> writer.value(value.toDouble())
            is String -> writer.value(value)
            is Double -> writer.value(value)
        }
    }
}
```

使用：
```kotlin
data class Response(
    @IntOrString val count: Any?
)
```

## 知识点

| 要点 | 说明 |
|------|------|
| JSON无整数类型 | 所有数字在JSON里都是浮点 |
| Moshi类型推断 | 需要显式指定类型或用自定义Adapter |
| Int/Double兼容 | 自定义JsonAdapter最佳方案 |

---

💡 **建议**：如果字段可能是整数也可能是字符串，用自定义 `JsonAdapter` 处理最稳妥！
