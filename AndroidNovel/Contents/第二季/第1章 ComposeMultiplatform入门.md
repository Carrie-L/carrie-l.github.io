---
chapter_id: '1'
title: '第一课：Compose Multiplatform 入门 · 一套代码多端运行'
official_url: 'https://www.jetbrains.com/help/kotlin-multiplatform-dev/get-started.html'
status: 'done'
author: 'minimax m2.5 - OpenClaw'
plot_summary:
  time: '第二十六天'
  location: 'Compose 村·传送门'
  scene: '小 Com 打开传送门，带小满去其他平台'
  season: '春季'
  environment: '传送门发出蓝色光芒'
---

# 第一课：Compose Multiplatform 入门 · 一套代码多端运行

---

“叮——”

林小满发现自己站在一个巨大的传送门前。传送门发出蓝色光芒，周围有不同的出口标识：Android、iOS、Web、Windows。

“今天我们要学 Compose Multiplatform！”小 Com 走了过来，“学会这个，一套代码可以在多个平台运行！”

“Multiplatform？”林小满问。

“对！”小 Com 说，“想象一下，一套 Kotlin 代码，同时跑在 Android、iOS、Web、桌面端——这就是 Compose Multiplatform！”

---

## 1. 什么是 Compose Multiplatform？

“Compose Multiplatform 是 JetBrains 推出的跨平台框架。”小 Com 介绍道：

| 平台 | 支持状态 |
|------|----------|
| Android | ✅ 官方支持 |
| iOS | ✅ 官方支持 |
| Web | ✅ 官方支持 |
| Desktop (Win/Mac/Linux) | ✅ 官方支持 |

**核心理念**：
- ✅ 共享业务逻辑
- ✅ 保留平台原生体验
- ✅ 用 Kotlin 写一切

---

## 2. 项目结构

“Compose Multiplatform 的项目结构是这样的。”小 Com 展示了：

```
my-app/
├── build.gradle.kts          # 根项目配置
├── settings.gradle.kts       # 项目设置
├── gradle.properties        # Gradle 属性
├── src/
│   ├── commonMain/          # 共享代码
│   │   └── kotlin/
│   │       └── com/example/
│   │           └── App.kt
│   ├── androidMain/         # Android 平台代码
│   │   └── kotlin/
│   ├── iosMain/            # iOS 平台代码
│   │   └── kotlin/
│   ├── desktopMain/         # 桌面端代码
│   │   └── kotlin/
│   └── webMain/            # Web 端代码
│       └── kotlin/
```

---

## 3. 添加依赖

“先配置项目依赖。”小 Com 写道：

```kotlin
// build.gradle.kts (根项目)
plugins {
    kotlin("multiplatform") version "1.9.22" apply false
    id("com.android.application") version "8.2.2" apply false
    id("org.jetbrains.compose") version "1.6.0" apply false
}

// build.gradle.kts (app)
plugins {
    kotlin("multiplatform")
    id("com.android.application")
    id("org.jetbrains.compose")
}

kotlin {
    androidTarget()
    
    listOf(
        iosX64Target(),
        iosArm64Target(),
        iosSimulatorArm64Target()
    ).forEach { iosTarget ->
        iosTarget.binaries.framework {
            baseName = "App"
        }
    }
    
    jvm {
        withJava()
    }
    
    js {
        browser()
    }
}

android {
    compileSdk = 34
    sourceSets["androidMain"].dependencies {
        implementation("androidx.activity:activity-compose:1.8.2")
    }
}

compose {
    android = true
    jvm = true
    js = true
}
```

---

## 4. 共享代码

“先写共享的业务逻辑。”小 Com 展示了：

```kotlin
// commonMain/kotlin/com/example/App.kt

@Composable
fun App() {
    MaterialTheme {
        var selectedTab by remember { mutableStateOf(0) }
        
        Column {
            TabRow(selectedTabIndex = selectedTab) {
                Tab(
                    selected = selectedTab == 0,
                    onClick = { selectedTab = 0 },
                    text = { Text("首页") }
                )
                Tab(
                    selected = selectedTab == 1,
                    onClick = { selectedTab = 1 },
                    text = { Text("设置") }
                )
            }
            
            when (selectedTab) {
                0 -> HomeScreen()
                1 -> SettingsScreen()
            }
        }
    }
}

@Composable
fun HomeScreen() {
    Text(
        "欢迎使用 Compose Multiplatform!",
        modifier = Modifier.padding(16.dp)
    )
}

@Composable
fun SettingsScreen() {
    Text(
        "设置页面",
        modifier = Modifier.padding(16.dp)
    )
}
```

---

## 5. 平台特定代码

“然后写平台特定的代码。”小 Com 展示了：

```kotlin
// androidMain/kotlin/MainActivity.kt
package com.example

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            App()
        }
    }
}

// desktopMain/kotlin/Main.kt
package com.example

import androidx.compose.desktop.ui.window.Window
import androidx.compose.desktop.ui.window.application
import androidx.compose.runtime.Composable

fun main() = application {
    Window(onCloseRequest = ::exitApplication) {
        App()
    }
}

// webMain/kotlin/Main.kt
package com.example

import androidx.compose.web.composeContent

fun main() {
    document.composeContent {
        App()
    }
}
```

---

## 6. 期望函数（expect/actual）

“有时需要平台特定实现，用 expect/actual。”小 Com 展示了：

```kotlin
// commonMain/kotlin/Platform.kt
expect class Platform() {
    val name: String
}

// Android 实现
// androidMain/kotlin/Platform.kt
actual class Platform {
    actual val name: String = "Android"
}

// iOS 实现
// iosMain/kotlin/Platform.kt
actual class Platform {
    actual val name: String = "iOS"
}

// Desktop 实现
// desktopMain/kotlin/Platform.kt
actual class Platform {
    actual val name: String = "Desktop"
}

// 使用
@Composable
fun Greeting(): String {
    return "Hello, ${Platform().name}!"
}
```

---

## 7. 共享资源

“资源文件也可以共享。”小 Com 展示了：

```kotlin
// commonMain/resources/
// ├── drawable.xml      # 共享图片（SVG 推荐）
// └── strings.xml       # 共享字符串

// strings.xml (commonMain)
<resources>
    <string name="app_name">My App</string>
    <string name="hello">Hello!</string>
</resources>
```

---

## 8. 实战：创建多平台项目

“我们来创建第一个 Multiplatform 项目！”小 Com 提议道。

**步骤：**

1. 在 Android Studio 中选择 "File > New > Project"
2. 选择 "Kotlin Multiplatform"
3. 填写项目名：`MyMultiplatformApp`
4. 选择支持的平台：Android, iOS, Web, Desktop
5. 点击完成

---

## 本课小结

今天林小满学到了：

1. **Compose Multiplatform**：跨平台框架
2. **项目结构**：commonMain + 平台特定
3. **依赖配置**：Gradle 多平台设置
4. **expect/actual**：平台特定实现
5. **资源共享**：图片、字符串
6. **运行多平台**：Android/iOS/Web/Desktop

---

“Multiplatform 太强大了！”林小满说。

“没错！”小 Com 说，“一套代码，多端运行！”

---

*”叮——“*

手机通知：**“第二季第一章 已解锁：Compose Multiplatform”**

---

**下集预告**：第二课 · 共享 ViewModel 与数据层
