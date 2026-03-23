---
chapter_id: '16'
title: '第十六课：Compose 动画 · 让界面动起来'
official_url: 'https://developer.android.com/compose.animation'
status: 'done'
author: 'minimax m2.5 - OpenClaw'
plot_summary:
  time: '第十六天'
  location: 'Compose 村·游乐园'
  scene: '小 Com 教小满用动画让界面动起来'
  season: '春季'
  environment: '游乐园里各种设施在运转'
---

# 第十六课：Compose 动画 · 让界面动起来

---

“叮——”

林小满发现自己站在一个游乐园里。旋转木马、摩天轮、碰碰车……一切都在动。

“今天我们要学动画！”小 Com 戴着遮阳帽走了过来，“在 Compose 里做动画超级简单，学会之后，你的 App 就会变得生动有趣！”

“动画？”林小满问。

“对！”小 Com 说，“好的动画能让用户体验更好，比如页面切换、按钮点击、加载提示……都离不开动画！”

---

## 1. 简单动画：animateFloatAsState

“最简单的动画是数值动画。”小 Com 写道：

```kotlin
var expanded by remember { mutableStateOf(false) }

val width by animateFloatAsState(
    targetValue = if (expanded) 200f else 100f,
    animationSpec = tween(durationMillis = 300)
)

Box(
    modifier = Modifier
        .width(width.dp)
        .height(100.dp)
        .background(Color.Blue)
)
```

---

## 2. 动画参数

“动画可以有很多参数。”小 Com 展示了：

```kotlin
val value by animateFloatAsState(
    targetValue = target,
    
    // 动画规格
    animationSpec = tween(
        durationMillis = 300,      // 持续时间
        easing = FastOutSlowInEasing  // 缓动函数
    ),
    
    // 快速到达目标值时是否跳过动画
    finishedListener = { /* 动画完成回调 */ }
)
```

**常用的动画规格：**

| 规格 | 用途 |
|------|------|
| `tween` | 线性过渡 |
| `spring` | 弹性效果 |
| `snap` | 立即切换 |
| `repeatable` | 重复动画 |

---

## 3. 颜色动画

“颜色也可以动画！”小 Com 展示了：

```kotlin
var isOn by remember { mutableStateOf(false) }

val backgroundColor by animateColorAsState(
    targetValue = if (isOn) Color.Green else Color.Gray,
    animationSpec = tween(300)
)

Box(
    modifier = Modifier
        .size(100.dp)
        .background(backgroundColor)
)
```

---

## 4. 可见性动画：AnimatedVisibility

“还有可见性动画——元素出现和消失。”小 Com 展示了：

```kotlin
var visible by remember { mutableStateOf(true) }

Column {
    Button(onClick = { visible = !visible }) {
        Text("切换")
    }
    
    AnimatedVisibility(
        visible = visible,
        enter = fadeIn() + expandVertically(),  // 进入动画
        exit = fadeOut() + shrinkVertically()   // 退出动画
    ) {
        Text("我出现啦！")
    }
}
```

**进入/退出动画：**

```kotlin
// 淡入
fadeIn()

// 淡出
fadeOut()

// 垂直展开
expandVertically()

// 垂直收缩
shrinkVertically()

// 水平展开
expandHorizontally()

// 水平收缩
shrinkHorizontally()

// 组合
fadeIn() + expandVertically()
```

---

## 5. 交叉淡入淡出：Crossfade

“切换内容时用 Crossfade。”小 Com 展示了：

```kotlin
var currentScreen by remember { mutableStateOf("home") }

Crossfade(
    targetState = currentScreen,
    animationSpec = tween(300)
) { screen ->
    when (screen) {
        "home" -> HomeScreen()
        "detail" -> DetailScreen()
        "profile" -> ProfileScreen()
    }
}
```

---

## 6. 无限循环动画：rememberInfiniteTransition

“有些动画需要无限循环，比如加载指示器。”小 Com 展示了：

```kotlin
@Composable
fun LoadingAnimation() {
    val infiniteTransition = rememberInfiniteTransition()
    
    val alpha by infiniteTransition.animateFloat(
        initialValue = 0.3f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(1000),
            repeatMode = RepeatMode.Reverse
        )
    )
    
    Box(
        modifier = Modifier
            .size(50.dp)
            .background(Color.Blue.copy(alpha = alpha))
    )
}
```

---

## 7. 动画修饰符

“还有一些动画修饰符。”小 Com 展示了：

```kotlin
// 旋转动画
Modifier.animateContentSize()  // 大小变化时动画

// 点击波纹（Material Design）
Modifier
    .clickable { }
    .ripple(bounded = true)

// 拖拽
Modifier.draggable(
    state = dragState,
    orientation = Orientation.Horizontal,
    onDragStopped = { velocity -> }
)
```

---

## 8. 实战：可展开的卡片

“我们来做个好玩的——可展开的卡片！”小 Com 提议道。

```kotlin
@Composable
fun ExpandableCard(
    title: String,
    content: String
) {
    var expanded by remember { mutableStateOf(false) }
    
    Card(
        onClick = { expanded = !expanded },
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleMedium
                )
                Icon(
                    imageVector = if (expanded)
                        Icons.Default.ExpandLess
                    else
                        Icons.Default.ExpandMore,
                    contentDescription = null
                )
            }
            
            AnimatedVisibility(
                visible = expanded,
                enter = fadeIn() + expandVertically(),
                exit = fadeOut() + shrinkVertically()
            ) {
                Text(
                    text = content,
                    modifier = Modifier.padding(top = 8.dp),
                    style = MaterialTheme.typography.bodyMedium
                )
            }
        }
    }
}
```

---

## 9. 实战：点赞按钮

“再来一个——点赞按钮动画！”

```kotlin
@Composable
fun LikeButton(
    isLiked: Boolean,
    onClick: () -> Unit
) {
    var liked by remember { mutableStateOf(isLiked) }
    var scale by remember { mutableFloatStateOf(1f) }
    
    val animatedScale by animateFloatAsState(
        targetValue = scale,
        animationSpec = spring(
            dampingRatio = Spring.DampingRatioMediumBouncy,
            stiffness = Spring.StiffnessLow
        ),
        finishedListener = { scale = 1f }
    )
    
    IconButton(
        onClick = {
            liked = !liked
            scale = 1.3f
            onClick()
        },
        modifier = Modifier.size(48.dp)
    ) {
        Icon(
            imageVector = if (liked) Icons.Default.Favorite else Icons.Default.FavoriteBorder,
            contentDescription = "点赞",
            tint = if (liked) Color.Red else Color.Gray,
            modifier = Modifier
                .size(32.dp)
                .graphicsLayer {
                    scaleX = animatedScale
                    scaleY = animatedScale
                }
        )
    }
}
```

---

## 10. 页面切换动画

“最后是页面切换动画。”小 Com 展示了：

```kotlin
@Composable
fun AnimatedNavHost() {
    val navController = rememberNavController()
    
    AnimatedNavHost(
        navController = navController,
        startDestination = "home",
        enterTransition = {
            slideInHorizontally(
                initialOffsetX = { it },
                animationSpec = tween(300)
            ) + fadeIn(animationSpec = tween(300))
        },
        exitTransition = {
            slideOutHorizontally(
                targetOffsetX = { -it },
                animationSpec = tween(300)
            ) + fadeOut(animationSpec = tween(300))
        },
        popEnterTransition = {
            slideInHorizontally(
                initialOffsetX = { -it },
                animationSpec = tween(300)
            ) + fadeIn(animationSpec = tween(300))
        },
        popExitTransition = {
            slideOutHorizontally(
                targetOffsetX = { it },
                animationSpec = tween(300)
            ) + fadeOut(animationSpec = tween(300))
        }
    ) {
        composable("home") { HomeScreen() }
        composable("detail") { DetailScreen() }
    }
}
```

---

## 本课小结

今天林小满学到了：

1. **animateFloatAsState**：数值动画
2. **animateColorAsState**：颜色动画
3. **AnimatedVisibility**：可见性动画
4. **Crossfade**：交叉淡入淡出
5. **rememberInfiniteTransition**：无限循环动画
6. **animateContentSize**：内容大小动画
7. **页面切换动画**：NavHost 动画

---

“动画太有意思了！”林小满说。

“没错！”小 Com 说，“好的动画能让 App 变得栩栩如生！”

---

*”叮——“*

手机通知：**“第十六章 已解锁：Compose 动画”**

---

**下集预告**：第十七课 · Material Design 3 主题设计
