---
chapter_id: '2'
title: '第二课：共享 ViewModel 与数据层'
official_url: 'https://kotlinlang.org/docs/multiplatform-connect-native-apis.html'
status: 'done'
<parameter name="author">'minimax m2.5 - OpenClaw'
plot_summary:
  time: '第二十七天'
  location: 'Compose 村·数据中心'
  scene: '小 Com 教小满在多平台共享数据层'
  season: '春季'
  environment: '数据中心里服务器在运转'
---

# 第二课：共享 ViewModel 与数据层

---

“叮——”

林小满发现自己站在一个数据中心里。巨大的服务器闪烁着灯光。

“今天我们要学在 Multiplatform 中共享数据层！”小 Com 走了过来，“把 ViewModel 和 Repository 也共享出去！”

“数据层也能共享？”林小满问。

“对！”小 Com 说，“业务逻辑、数据模型、Repository……都可以放在 commonMain！”

---

## 1. 共享数据模型

“先从共享数据模型开始。”小 Com 展示了：

```kotlin
// commonMain/kotlin/com/example/model/User.kt

@kotlinx.serialization.Serializable
data class User(
    val id: String,
    val name: String,
    val email: String,
    val avatarUrl: String? = null
)

@kotlinx.serialization.Serializable
data class LoginRequest(
    val username: String,
    val password: String
)

@kotlinx.serialization.Serializable
data class LoginResponse(
    val token: String,
    val user: User
)
```

---

## 2. 添加序列化依赖

“先添加序列化依赖。”小 Com 写道：

```kotlin
// build.gradle.kts
plugins {
    kotlin("multiplatform")
    kotlin("plugin.serialization") version "1.9.22"
}

kotlin {
    sourceSets {
        val commonMain by getting {
            dependencies {
                implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.2")
            }
        }
    }
}
```

---

## 3. 共享 Repository

“然后共享 Repository。”小 Com 展示了：

```kotlin
// commonMain/kotlin/com/example/repository/UserRepository.kt

expect class HttpClient()

class UserRepository(
    private val httpClient: HttpClient
) {
    suspend fun login(username: String, password: String): Result<User> {
        return try {
            val response = httpClient.post(
                "https://api.example.com/login",
                body = LoginRequest(username, password)
            )
            Result.success(response.user)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun getUser(id: String): Result<User> {
        return try {
            val response = httpClient.get("https://api.example.com/users/$id")
            Result.success(response.user)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
```

---

## 4. 平台特定 HTTP 客户端

“然后实现平台特定的 HTTP 客户端。”小 Com 展示了：

```kotlin
// Android 实现
// androidMain/kotlin/HttpClient.kt
actual typealias HttpClient = io.ktor.client.HttpClient

// iOS 实现
// iosMain/kotlin/HttpClient.kt
actual typealias HttpClient = io.ktor.client.HttpClient

// Desktop 实现
// desktopMain/kotlin/HttpClient.kt
actual typealias HttpClient = io.ktor.client.HttpClient

// Web 实现
// webMain/kotlin/HttpClient.kt
actual typealias HttpClient = io.ktor.client.HttpClient
```

---

## 5. 共享 ViewModel

“在 commonMain 中共享 ViewModel。”小 Com 展示了：

```kotlin
// commonMain/kotlin/com/example/viewmodel/UserViewModel.kt

class UserViewModel(
    private val repository: UserRepository
) {
    private val _user = MutableStateFlow<UserViewState>(UserViewState.Initial)
    val user: StateFlow<UserViewState> = _user
    
    fun login(username: String, password: String) {
        viewModelScope.launch {
            _user.value = UserViewState.Loading
            
            repository.login(username, password)
                .onSuccess { user ->
                    _user.value = UserViewState.Success(user)
                }
                .onFailure { error ->
                    _user.value = UserViewState.Error(error.message ?: "登录失败")
                }
        }
    }
    
    fun logout() {
        _user.value = UserViewState.Initial
    }
}

sealed class UserViewState {
    object Initial : UserViewState()
    object Loading : UserViewState()
    data class Success(val user: User) : UserViewState()
    data class Error(val message: String) : UserViewState()
}
```

---

## 6. 依赖注入

“Multiplatform 中用 Koin 做依赖注入。”小 Com 展示了：

```kotlin
// commonMain/kotlin/di/AppModule.kt

fun initKoin() = koin {
    viewModel { UserViewModel(get()) }
    single { UserRepository(get()) }
    
    // 平台特定的 HTTP 客户端
    single { HttpClient() }
}

// Android
// androidMain/kotlin/MainActivity.kt
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        initKoin()
        
        setContent {
            App()
        }
    }
}

// Desktop
// desktopMain/kotlin/Main.kt
fun main() = application {
    initKoin()
    Window {
        App()
    }
}
```

---

## 7. 本地存储

“本地存储也可以共享。”小 Com 展示了：

```kotlin
// commonMain/kotlin/storage/Storage.kt
expect class Storage() {
    fun getString(key: String): String?
    fun setString(key: String, value: String)
    fun remove(key: String)
}

// Android 实现（用 SharedPreferences）
// androidMain/kotlin/storage/Storage.kt
actual class Storage(private val context: Context) {
    private val prefs = context.getSharedPreferences("app", Context.MODE_PRIVATE)
    
    actual fun getString(key: String): String? = prefs.getString(key, null)
    actual fun setString(key: String, value: String) = prefs.edit().putString(key, value).apply()
    actual fun remove(key: String) = prefs.edit().remove(key).apply()
}

// Desktop 实现（用 Properties）
// desktopMain/kotlin/storage/Storage.kt
actual class Storage {
    private val props = Properties()
    
    actual fun getString(key: String): String? = props.getProperty(key)
    actual fun setString(key: String, value: String) { props.setProperty(key, value) }
    actual fun remove(key: String) { props.remove(key) }
}
```

---

## 8. 实战：完整的多平台架构

“我们来做最后一个练习——完整的架构！”小 Com 提议道。

```kotlin
// 完整架构

// commonMain/
// ├── model/           # 数据模型
// │   └── User.kt
// ├── repository/      # 数据仓库
// │   └── UserRepository.kt
// ├── viewmodel/       # ViewModel
// │   └── UserViewModel.kt
// ├── storage/         # 本地存储
// │   └── Storage.kt
// ├── di/              # 依赖注入
// │   └── AppModule.kt
// └── App.kt           # 共享 UI

// 平台特定/
// ├── androidMain/     # Android 入口
// ├── iosMain/         # iOS 入口
// ├── desktopMain/     # Desktop 入口
// └── webMain/        # Web 入口
```

---

## 本课小结

今天林小满学到了：

1. **共享数据模型**：Serializable data class
2. **共享 Repository**：业务逻辑共享
3. **expect/actual**：平台特定实现
4. **共享 ViewModel**：状态管理共享
5. **Koin DI**：跨平台依赖注入
6. **共享 Storage**：本地存储抽象

---

“Multiplatform 架构太棒了！”林小满说。

“没错！”小 Com 说，“一套代码，多端运行！”

---

*”叮——“*

手机通知：**“第二季第二章 已解锁：共享 ViewModel 与数据层”**

---

**下集预告**：第三课 · Kotlin 协程底层原理
