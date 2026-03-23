---
chapter_id: '9'
title: '第九课：Navigation 导航 · 多页面应用'
official_url: 'https://developer.android.com/compose.navigation'
status: 'done'
author: 'minimax m2.5 - OpenClaw'
plot_summary:
  time: '第九天'
  location: 'Compose 村·火车站'
  scene: '小 Com 教小满坐火车去不同页面'
  season: '春季'
  environment: '火车站，人们在排队买票'
---

# 第九课：Navigation 导航 · 多页面应用

---

“叮——”

林小满发现自己站在一个火车站台上。远处一列火车缓缓驶入车站。

“今天我们要学导航！”小 Com 穿着列车员的制服走了过来，“就像坐火车去不同城市一样，在 Compose 里，我们需要用 Navigation 在不同页面之间切换！”

“导航？”林小满问。

“对！”小 Com 说，“没有导航，就只能做一个页面。学会导航，你就能做整个 App！”

---

## 什么是导航？

“在 Android 里，导航就是从一个页面跳转到另一个页面。”小 Com 解释。

传统的做法：
- Activity 跳转
- Fragment 切换

Compose 的做法：
- **Navigation Compose**：声明式导航

---

## 添加依赖

“首先需要添加依赖。”小 Com 写道：

```kotlin
// build.gradle
dependencies {
    implementation "androidx.navigation:navigation-compose:2.7.6"
}
```

---

## 定义目的地

“在 Navigation Compose 里，每个页面叫'目的地'（Destination）。”小 Com 展示了代码：

```kotlin
sealed class Screen(val route: String) {
    object Home : Screen("home")
    object Detail : Screen("detail/{itemId}") {
        fun createRoute(itemId: String) = "detail/$itemId"
    }
    object Profile : Screen("profile")
}
```

---

## 创建 NavHost

“然后创建 NavHost——导航的容器。”

```kotlin
@Composable
fun MyApp() {
    val navController = rememberNavController()
    
    NavHost(
        navController = navController,
        startDestination = Screen.Home.route
    ) {
        composable(Screen.Home.route) {
            HomeScreen(
                onNavigateToDetail = { itemId ->
                    navController.navigate(Screen.Detail.createRoute(itemId))
                }
            )
        }
        
        composable(
            route = Screen.Detail.route,
            arguments = listOf(
                navArgument("itemId") { type = NavType.StringType }
            )
        ) { backStackEntry ->
            val itemId = backStackEntry.arguments?.getString("itemId")
            DetailScreen(itemId = itemId)
        }
        
        composable(Screen.Profile.route) {
            ProfileScreen()
        }
    }
}
```

---

## HomeScreen

“每个页面都是一个 Composable 函数。”小 Com 展示了 HomeScreen：

```kotlin
@Composable
fun HomeScreen(
    onNavigateToDetail: (String) -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(title = { Text("首页") })
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            Text("欢迎来到首页")
            
            Button(onClick = { onNavigateToDetail("123") }) {
                Text("查看详情")
            }
            
            Button(onClick = { navController.navigate(Screen.Profile.route) }) {
                Text("我的")
            }
        }
    }
}
```

---

## DetailScreen

“详情页接收参数：”

```kotlin
@Composable
fun DetailScreen(itemId: String?) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("详情页") },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.Default.ArrowBack, "返回")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            Text("商品 ID: $itemId")
        }
    }
}
```

---

## 底部导航栏

“很多 App 有底部导航栏，我们来实现它。”

```kotlin
@Composable
fun BottomNavigationApp() {
    val navController = rememberNavController()
    
    Scaffold(
        bottomBar = {
            NavigationBar {
                NavigationBarItem(
                    icon = { Icon(Icons.Default.Home, "首页") },
                    label = { Text("首页") },
                    selected = currentRoute == Screen.Home.route,
                    onClick = {
                        navController.navigate(Screen.Home.route) {
                            popUpTo(Screen.Home.route) { inclusive = true }
                        }
                    }
                )
                
                NavigationBarItem(
                    icon = { Icon(Icons.Default.Search, "搜索") },
                    label = { Text("搜索") },
                    selected = currentRoute == Screen.Search.route,
                    onClick = {
                        navController.navigate(Screen.Search.route)
                    }
                )
                
                NavigationBarItem(
                    icon = { Icon(Icons.Default.Person, "我的") },
                    label = { Text("我的") },
                    selected = currentRoute == Screen.Profile.route,
                    onClick = {
                        navController.navigate(Screen.Profile.route)
                    }
                )
            }
        }
    ) { padding ->
        NavHost(
            navController = navController,
            startDestination = Screen.Home.route,
            modifier = Modifier.padding(padding)
        ) {
            // ...
        }
    }
}
```

---

## 传递数据

“导航时还可以传递数据。”小 Com 展示了两种方式：

### 方式1：通过 Route 参数

```kotlin
// 定义
object Detail : Screen("detail/{itemId}") {
    fun createRoute(itemId: String) = "detail/$itemId"
}

// 导航时
navController.navigate(Detail.createRoute("123"))

// 接收时
val itemId = backStackEntry.arguments?.getString("itemId")
```

### 方式2：通过 SavedStateHandle（推荐）

```kotlin
// 导航时
navController.navigate("detail?itemId=123")

// 接收时
val itemId = backStackEntry.savedStateHandle.get<String>("itemId")
```

---

## 动画过渡

“页面切换还可以加动画！”小 Com 展示了代码：

```kotlin
composable(
    route = Screen.Detail.route,
    enterTransition = {
        slideInHorizontally(initialOffsetX = { it }) + fadeIn()
    },
    exitTransition = {
        slideOutHorizontally(targetOffsetX = { -it }) + fadeOut()
    },
    popEnterTransition = {
        slideInHorizontally(initialOffsetX = { -it }) + fadeIn()
    },
    popExitTransition = {
        slideOutHorizontally(targetOffsetX = { it }) + fadeOut()
    }
) {
    DetailScreen()
}
```

---

## 深层链接

“还可以处理深层链接——从外部打开特定页面。”小 Com 说：

```kotlin
composable(
    route = Screen.Profile.route,
    deepLinks = listOf(
        navDeepLink {
            uriPattern = "myapp://profile"
        },
        navDeepLink {
            uriPattern = "https://myapp.com/profile"
        }
    )
) {
    ProfileScreen()
}
```

---

## 实战：完整的导航示例

“我们来做最后一个练习——一个带底部导航的完整 App！”小 Com 说。

```kotlin
// 1. 定义屏幕
sealed class Screen(val route: String) {
    object Home : Screen("home")
    object Search : Screen("search")
    object Profile : Screen("profile")
}

// 2. 主 App
@Composable
fun MainApp() {
    val navController = rememberNavController()
    
    Scaffold(
        bottomBar = {
            NavigationBar {
                val navBackStackEntry by navController.currentBackStackEntryAsState()
                val currentRoute = navBackStackEntry?.destination?.route
                
                Screen.entries.forEach { screen ->
                    NavigationBarItem(
                        icon = {
                            when (screen) {
                                Screen.Home -> Icon(Icons.Default.Home, "首页")
                                Screen.Search -> Icon(Icons.Default.Search, "搜索")
                                Screen.Profile -> Icon(Icons.Default.Person, "我的")
                            }
                        },
                        label = {
                            when (screen) {
                                Screen.Home -> Text("首页")
                                Screen.Search -> Text("搜索")
                                Screen.Profile -> Text("我的")
                            }
                        },
                        selected = currentRoute == screen.route,
                        onClick = {
                            if (currentRoute != screen.route) {
                                navController.navigate(screen.route) {
                                    popUpTo(Screen.Home.route) {
                                        saveState = true
                                    }
                                    launchSingleTop = true
                                    restoreState = true
                                }
                            }
                        }
                    )
                }
            }
        }
    ) { padding ->
        NavHost(
            navController = navController,
            startDestination = Screen.Home.route,
            modifier = Modifier.padding(padding)
        ) {
            composable(Screen.Home.route) { HomeScreen() }
            composable(Screen.Search.route) { SearchScreen() }
            composable(Screen.Profile.route) { ProfileScreen() }
        }
    }
}
```

---

## 本课小结

今天林小满学到了：

1. **Navigation Compose**：声明式导航
2. **Screen 定义**：用 sealed class 定义路由
3. **NavHost**：导航的容器
4. **导航方法**：navigate / popBackStack
5. **传递参数**：通过 route 或 SavedStateHandle
6. **底部导航**：NavigationBar
7. **动画过渡**：slideIn / slideOut
8. **深层链接**：处理外部链接

---

“导航太重要了！”林小满说。

“没错！”小 Com 说，“学会导航，你就能做完整的多页面 App 了！”

“明天我们学什么？”

“明天学——协程！”小 Com 笑道，“异步编程的基础！”

---

*”叮——“*

手机通知：**“第九章 已解锁：Navigation 导航”**

---

### 📚 课后练习

1. 做一个两页面的 App，从首页跳转到详情页
2. 做一个带底部导航栏的 App
3. 实现页面切换动画

---

**下集预告**：第十课 · 协程基础 · 异步编程入门
