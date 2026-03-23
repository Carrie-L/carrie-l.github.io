---
chapter_id: '14'
title: '第十四课：MVVM 架构 · 把一切都组织起来'
official_url: 'https://developer.android.com/topic/libraries/architecture'
status: 'done'
author: 'minimax m2.5 - OpenClaw'
plot_summary:
  time: '第十四天'
  location: 'Compose 村·城市规划馆'
  scene: '小 Com 展示完整的 MVVM 架构'
  season: '春季'
  environment: '城市规划馆，墙上挂着各种设计图'
---

# 第十四课：MVVM 架构 · 把一切都组织起来

---

“叮——”

林小满发现自己站在一个城市规划馆里。墙上挂着各种设计图，展示着城市的布局。

“今天我们要学 MVVM！”小 Com 拿着一张设计图走了过来，“MVVM 是 Android 开发的最佳架构，学会它，你的代码就会变得整整齐齐！”

“MVVM？”林小满问。

“对！”小 Com 说，“它能把 UI、业务逻辑、数据分得清清楚楚，就像城市规划一样！”

---

## 什么是 MVVM？

“MVVM = Model + View + ViewModel。”小 Com 画了个图：

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    View     │ ←── │  ViewModel  │ ←── │    Model    │
│  (Compose)  │     │  (逻辑层)   │     │ (Repository)│
└─────────────┘     └─────────────┘     └─────────────┘
     UI 展示            业务逻辑           数据来源
```

| 层 | 职责 | 例子 |
|---|------|------|
| **View** | UI 显示 | Composable 函数 |
| **ViewModel** | 业务逻辑 | 状态管理、用户操作处理 |
| **Model** | 数据层 | Repository、API、数据库 |

---

## 完整项目结构

“我们来看一个完整的 MVVM 项目结构！”小 Com 展示了：

```
app/src/main/java/com/example/app/
├── data/
│   ├── api/
│   │   └── ApiService.kt
│   ├── local/
│   │   ├── database/
│   │   │   ├── AppDatabase.kt
│   │   │   └── UserDao.kt
│   │   └── entity/
│   │       └── User.kt
│   └── repository/
│       └── UserRepository.kt
├── di/
│   └── AppModule.kt
├── ui/
│   ├── theme/
│   │   └── Theme.kt
│   ├── home/
│   │   ├── HomeScreen.kt
│   │   └── HomeViewModel.kt
│   └── navigation/
│       └── AppNavigation.kt
└── MyApplication.kt
```

---

## Model 层：数据

“首先看 Model 层——数据。”小 Com 展示了：

```kotlin
// Entity
@Entity(tableName = "users")
data class User(
    @PrimaryKey val id: String,
    val name: String,
    val email: String,
    val avatar: String? = null
)

// API Service
interface ApiService {
    @GET("users/{id}")
    suspend fun getUser(@Path("id") id: String): User
    
    @GET("users")
    suspend fun getUsers(): List<User>
}

// Repository
class UserRepository(
    private val api: ApiService,
    private val userDao: UserDao
) {
    suspend fun getUser(id: String): Result<User> { ... }
    
    fun getUsersFlow(): Flow<List<User>> = userDao.getAllUsersFlow()
}
```

---

## ViewModel 层：业务逻辑

“然后看 ViewModel 层——业务逻辑。”小 Com 展示了：

```kotlin
@HiltViewModel
class HomeViewModel(
    private val repository: UserRepository
) : ViewModel() {
    
    // UI 状态
    private val _uiState = MutableStateFlow(HomeUiState())
    val uiState: StateFlow<HomeUiState> = _uiState
    
    // 用户列表
    private val _users = MutableStateFlow<List<User>>(emptyList())
    val users: StateFlow<List<User>> = _users
    
    // 加载数据
    fun loadUsers() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            
            repository.getUsersFlow().collect { userList ->
                _users.value = userList
                _uiState.update { it.copy(isLoading = false) }
            }
        }
    }
    
    // 删除用户
    fun deleteUser(user: User) {
        viewModelScope.launch {
            repository.deleteUser(user)
        }
    }
}

data class HomeUiState(
    val isLoading: Boolean = false,
    val error: String? = null
)
```

---

## View 层：UI

“最后看 View 层——UI。”小 Com 展示了：

```kotlin
@Composable
fun HomeScreen(
    viewModel: HomeViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    val users by viewModel.users.collectAsState()
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("用户列表") },
                actions = {
                    IconButton(onClick = { /* 刷新 */ }) {
                        Icon(Icons.Default.Refresh, "刷新")
                    }
                }
            )
        }
    ) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            when {
                uiState.isLoading -> {
                    CircularProgressIndicator(
                        modifier = Modifier.align(Alignment.Center)
                    )
                }
                users.isEmpty() -> {
                    Text(
                        "暂无数据",
                        modifier = Modifier.align(Alignment.Center)
                    )
                }
                else -> {
                    LazyColumn {
                        items(users, key = { it.id }) { user ->
                            UserItem(
                                user = user,
                                onDelete = { viewModel.deleteUser(user) }
                            )
                        }
                    }
                }
            }
        }
    }
}
```

---

## 状态流向

“数据是这样流动的：”小 Com 画了张图：

```
用户操作
   ↓
View.onClick → ViewModel.XXX()
   ↓
ViewModel 更新 State
   ↓
Compose 重组（Recomposition）
   ↓
UI 更新
```

---

## 通信方式

“各层之间是这样通信的：”

| 通信 | 方式 |
|------|------|
| View → ViewModel | 函数调用，如 `viewModel.loadUsers()` |
| ViewModel → View | StateFlow / SharedFlow |
| ViewModel → Model | 协程调用，如 `repository.getUsers()` |

---

## 实战：完整的登录功能

“我们来做最后一个练习——完整的登录功能！”小 Com 提议道。

```kotlin
// 1. Model
class LoginRepository {
    suspend fun login(username: String, password: String): Result<User> {
        // 模拟网络请求
        delay(1000)
        return if (username == "admin" && password == "123456") {
            Result.success(User("1", "管理员", "admin@example.com"))
        } else {
            Result.failure(Exception("用户名或密码错误"))
        }
    }
}

// 2. ViewModel
@HiltViewModel
class LoginViewModel(
    private val repository: LoginRepository
) : ViewModel() {
    
    private val _uiState = MutableStateFlow(LoginUiState())
    val uiState: StateFlow<LoginUiState> = _uiState
    
    fun login(username: String, password: String) {
        if (username.isBlank() || password.isBlank()) {
            _uiState.update { it.copy(error = "请输入用户名和密码") }
            return
        }
        
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            
            repository.login(username, password)
                .onSuccess { user ->
                    _uiState.update { it.copy(isLoading = false, isLoggedIn = true) }
                }
                .onFailure { e ->
                    _uiState.update { it.copy(isLoading = false, error = e.message) }
                }
        }
    }
    
    fun clearError() {
        _uiState.update { it.copy(error = null) }
    }
}

data class LoginUiState(
    val isLoading: Boolean = false,
    val isLoggedIn: Boolean = false,
    val error: String? = null
)

// 3. View
@Composable
fun LoginScreen(
    onNavigateToHome: () -> Unit,
    viewModel: LoginViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    
    LaunchedEffect(uiState.isLoggedIn) {
        if (uiState.isLoggedIn) {
            onNavigateToHome()
        }
    }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        OutlinedTextField(
            value = uiState.username,
            onValueChange = { },
            label = { Text("用户名") },
            modifier = Modifier.fillMaxWidth()
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        OutlinedTextField(
            value = uiState.password,
            onValueChange = { },
            label = { Text("密码") },
            modifier = Modifier.fillMaxWidth(),
            visualTransformation = PasswordVisualTransformation()
        )
        
        if (uiState.error != null) {
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                uiState.error!!,
                color = Color.Red,
                style = MaterialTheme.typography.bodySmall
            )
        }
        
        Spacer(modifier = Modifier.height(24.dp))
        
        Button(
            onClick = { viewModel.login("admin", "123456") },
            modifier = Modifier.fillMaxWidth(),
            enabled = !uiState.isLoading
        ) {
            if (uiState.isLoading) {
                CircularProgressIndicator(
                    modifier = Modifier.size(24.dp),
                    color = Color.White
                )
            } else {
                Text("登录")
            }
        }
    }
}
```

---

## 为什么要用 MVVM？

小 Com 总结了 MVVM 的好处：

| 好处 | 说明 |
|------|------|
| **职责分离** | UI / 业务 / 数据各司其职 |
| **可测试** | ViewModel 可以单独测试 |
| **可维护** | 代码结构清晰 |
| **生命周期感知** | ViewModel 自动管理生命周期 |
| **状态保存** | 配置变更时状态不丢失 |

---

## 本课小结

今天林小满学到了：

1. **MVVM 架构**：Model + View + ViewModel
2. **各层职责**：UI 展示 / 业务逻辑 / 数据管理
3. **数据流向**：用户操作 → ViewModel → State → UI
4. **StateFlow**：状态管理
5. **Repository 模式**：数据统一入口
6. **完整项目结构**：分层组织代码

---

“MVVM 太重要了！”林小满说。

“没错！”小 Com 说，“学会 MVVM，你就能写出专业的 Android 代码了！”

“明天我们学什么？”

“明天学——实战项目！”小 Com 笑道，“做一个完整的 App！”

---

*”叮——“*

手机通知：**“第十四章 已解锁：MVVM 架构”**

---

### 📚 课后练习

1. 按照 MVVM 结构重构现有代码
2. 创建一个带登录注册功能的完整项目
3. 给项目添加单元测试

---

**下集预告**：第十五课 · 实战项目 · 做一个完整的 App
