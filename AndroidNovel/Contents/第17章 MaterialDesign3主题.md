---
chapter_id: '17'
title: '第十七课：Material Design 3 主题设计'
official_url: 'https://m3.material.io/'
status: 'done'
author: 'minimax m2.5 - OpenClaw'
plot_summary:
  time: '第十七天'
  location: 'Compose 村·设计工作室'
  scene: '小 Com 教小满用 Material Design 3 设计主题'
  season: '春季'
  environment: '设计工作室，墙上挂满了设计稿'
---

# 第十七课：Material Design 3 主题设计

---

“叮——”

林小满发现自己站在一个设计工作室里。墙上挂满了各种设计稿，桌上摆满了色卡。

“今天我们要学主题设计！”小 Com 拿着色卡走了过来，“用 Material Design 3，让你的 App 既有颜值又专业！”

“主题设计？”林小满问。

“对！”小 Com 说，“主题包括颜色、字体、形状……统一的主题能让 App 看起来更专业！”

---

## 1. 什么是 Material Design 3？

“Material Design 3（也叫 Material You）是 Google 的最新设计语言。”小 Com 介绍道：

**Material Design 3 的特点：**
- ✅ 动态颜色（从壁纸提取颜色）
- ✅ 更大的圆角
- ✅ 更清晰的层次
- ✅ 新的组件设计

---

## 2. 添加依赖

“首先添加依赖。”小 Com 写道：

```kotlin
dependencies {
    implementation "androidx.compose.material3:material3"
}
```

---

## 3. 定义主题颜色

“首先定义颜色。”小 Com 展示了：

```kotlin
// Color.kt
private val Purple80 = Color(0xFFD0BCFF)
private val PurpleGrey80 = Color(0xFFCCC2DC)
private val Pink80 = Color(0xFFEFB8C8)

private val Purple40 = Color(0xFF6650a4)
private val PurpleGrey40 = Color(0xFF625b71)
private val Pink40 = Color(0xFF7D5260)

private val md_theme_light_primary = Color(0xFF6750A4)
private val md_theme_light_onPrimary = Color(0xFFFFFFFF)
private val md_theme_light_primaryContainer = Color(0xFFEADDFF)
private val md_theme_light_onPrimaryContainer = Color(0xFF21005D)

private val md_theme_light_secondary = Color(0xFF625B71)
private val md_theme_light_onSecondary = Color(0xFFFFFFFF)
private val md_theme_light_secondaryContainer = Color(0xFFE8DEF8)
private val md_theme_light_onSecondaryContainer = Color(0xFF1D192B)

private val md_theme_light_error = Color(0xFFB3261E)
private val md_theme_light_onError = Color(0xFFFFFFFF)

private val md_theme_light_background = Color(0xFFFFFBFE)
private val md_theme_light_onBackground = Color(0xFF1C1B1F)
```

---

## 4. 定义主题

“然后定义主题。”小 Com 展示了：

```kotlin
// Theme.kt
@Composable
fun MyAppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        darkTheme -> darkColorScheme(
            primary = Purple80,
            secondary = PurpleGrey80,
            tertiary = Pink80
        )
        lightTheme -> lightColorScheme(
            primary = Purple40,
            secondary = PurpleGrey40,
            tertiary = Pink40
        )
    }
    
    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        shapes = Shapes,
        content = content
    )
}
```

---

## 5. Typography（字体）

“然后定义字体。”小 Com 展示了：

```kotlin
val Typography = Typography(
    displayLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 57.sp,
        lineHeight = 64.sp,
        letterSpacing = (-0.25).sp
    ),
    displayMedium = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 45.sp,
        lineHeight = 52.sp,
        letterSpacing = 0.sp
    ),
    displaySmall = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 36.sp,
        lineHeight = 44.sp,
        letterSpacing = 0.sp
    ),
    headlineLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 32.sp,
        lineHeight = 40.sp,
        letterSpacing = 0.sp
    ),
    // ... 更多字体样式
    bodyLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.5.sp
    ),
    labelSmall = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Medium,
        fontSize = 11.sp,
        lineHeight = 16.sp,
        letterSpacing = 0.5.sp
    )
)
```

---

## 6. Shapes（形状）

“然后定义形状。”小 Com 展示了：

```kotlin
val Shapes = Shapes(
    extraSmall = RoundedCornerShape(4.dp),
    small = RoundedCornerShape(8.dp),
    medium = RoundedCornerShape(12.dp),
    large = RoundedCornerShape(16.dp),
    extraLarge = RoundedCornerShape(28.dp)
)
```

---

## 7. 使用主题颜色

“在组件中使用主题颜色。”小 Com 展示了：

```kotlin
@Composable
fun MyButton() {
    Button(
        onClick = { },
        colors = ButtonDefaults.buttonColors(
            containerColor = MaterialTheme.colorScheme.primary,
            contentColor = MaterialTheme.colorScheme.onPrimary
        )
    ) {
        Text("按钮")
    }
}

@Composable
fun MyCard() {
    Card(
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant
        ),
        shape = MaterialTheme.shapes.medium
    ) {
        Text("卡片")
    }
}
```

---

## 8. 动态颜色（Dynamic Color）

“Android 12+ 支持动态颜色——从壁纸提取颜色！”小 Com 展示了：

```kotlin
@Composable
fun DynamicColorApp() {
    val dynamicColor = Build.VERSION.SDK_INT >= Build.VERSION_CODES.S
    val colorScheme = when {
        dynamicColor && darkTheme -> dynamicDarkColorScheme(context)
        dynamicColor -> dynamicLightColorScheme(context)
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }
    
    MaterialTheme(
        colorScheme = colorScheme,
        content = content
    )
}
```

---

## 9. 深色主题

“深色主题也很重要。”小 Com 展示了：

```kotlin
private val DarkColorScheme = darkColorScheme(
    primary = Purple80,
    onPrimary = Purple40,
    primaryContainer = PurpleGrey80,
    onPrimaryContainer = Color(0xFFEADDFF),
    secondary = Color(0xFFCCC2DC),
    onSecondary = Color(0xFF332D41),
    secondaryContainer = Color(0xFF4A4458),
    onSecondaryContainer = Color(0xFFE8DEF8),
    tertiary = Pink80,
    onTertiary = Color(0xFF492532),
    tertiaryContainer = Color(0xFF633B48),
    onTertiaryContainer = Color(0xFFFFD8E4),
    error = Color(0xFFF2B8B5),
    onError = Color(0xFF601410),
    errorContainer = Color(0xFF8C1D18),
    onErrorContainer = Color(0xFFF9DEDC),
    background = Color(0xFF1C1B1F),
    onBackground = Color(0xFFE6E1E5),
    surface = Color(0xFF1C1B1F),
    onSurface = Color(0xFFE6E1E5),
)
```

---

## 10. 主题切换

“实现主题切换功能。”小 Com 展示了：

```kotlin
@Composable
fun ThemeSwitcherApp() {
    var darkTheme by remember { mutableStateOf(false) }
    
    MaterialTheme(
        colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme
    ) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("主题演示") },
                    actions = {
                        IconButton(onClick = { darkTheme = !darkTheme }) {
                            Icon(
                                if (darkTheme) Icons.Default.LightMode
                                else Icons.Default.DarkMode,
                                contentDescription = "切换主题"
                            )
                        }
                    }
                )
            }
        ) { padding ->
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
                    .padding(16.dp)
            ) {
                // 使用主题颜色的按钮
                Button(
                    onClick = { },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("主要按钮")
                }
                
                Spacer(modifier = Modifier.height(8.dp))
                
                OutlinedButton(
                    onClick = { },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("次要按钮")
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                // 卡片
                Card(
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text(
                        "卡片内容",
                        modifier = Modifier.padding(16.dp)
                    )
                }
            }
        }
    }
}
```

---

## 11. 自定义颜色

“有时候需要自定义颜色。”小 Com 展示了：

```kotlin
// 扩展颜色
val MaterialTheme = MaterialTheme
val MyColors = MaterialTheme.colorScheme

// 使用
Text(
    text = "自定义颜色",
    color = MyColors.primary
)

// 或者定义自己的颜色
object MyBrandColors {
    val BrandBlue = Color(0xFF2196F3)
    val BrandOrange = Color(0xFFFF9800)
    val BrandGreen = Color(0xFF4CAF50)
}
```

---

## 本课小结

今天林小满学到了：

1. **Material Design 3**：最新设计语言
2. **Color Scheme**：颜色配置
3. **Typography**：字体配置
4. **Shapes**：形状配置
5. **Light / Dark Theme**：浅色/深色主题
6. **Dynamic Color**：动态颜色
7. **Theme Switcher**：主题切换

---

“主题设计太重要了！”林小满说。

“没错！”小 Com 说，“好的主题能让 App 看起来更专业！”

---

*”叮——“*

手机通知：**“第十七章 已解锁：Material Design 3 主题设计”**

---

**下集预告**：第十八课 · 权限请求 · 相机、位置、通知
