---
chapter_id: '11'
title: '第十一课：Retrofit 网络请求 · API 调用实战'
official_url: 'https://square.github.io/retrofit/'
status: 'done'
author: 'minimax m2.5 - OpenClaw'
plot_summary:
  time: '第十一天'
  location: 'Compose 村·API 大厦'
  scene: '小 Com 教小满用 Retrofit 调用 API'
  season: '春季'
  environment: '高楼大厦，程序员们在忙碌'
---

# 第十一课：Retrofit 网络请求 · API 调用实战

---

“叮——”

林小满发现自己站在一座高科技大厦前。大厦门口写着四个大字：“API 大厦”。

“今天我们要学 Retrofit！”小 Com 从大厦里走出来，“Retrofit 是 Android 最流行的网络请求库，学会它，你就能调用任何 API！”

“Retrofit？”林小满问。

“对！”小 Com 说，“它能把 API 调用变成简单的函数调用，非常方便！”

---

## 添加依赖

“首先添加依赖。”小 Com 写道：

```kotlin
// build.gradle
dependencies {
    implementation "com.squareup.retrofit2:retrofit:2.9.0"
    implementation "com.squareup.retrofit2:converter-gson:2.9.0"
    implementation "com.squareup.okhttp3:logging-interceptor:4.12.0"
}
```

---

## 定义 API 接口

“首先定义 API 接口。”小 Com 展示了代码：

```kotlin
interface ApiService {
    
    // GET 请求
    @GET("users/{id}")
    suspend fun getUser(@Path("id") id: String): User
    
    // 查询参数
    @GET("users")
    suspend fun getUsers(@Query("page") page: Int): UsersResponse
    
    // POST 请求
    @POST("users")
    suspend fun createUser(@Body user: CreateUserRequest): User
    
    // PUT 请求
    @PUT("users/{id}")
    suspend fun updateUser(
        @Path("id") id: String,
        @Body user: UpdateUserRequest
    ): User
    
    // DELETE 请求
    @DELETE("users/{id}")
    suspend fun deleteUser(@Path("id") id: String)
}
```

---

## 定义数据模型

“然后定义数据模型。”小 Com 说：

```kotlin
// 用户模型
data class User(
    val id: String,
    val name: String,
    val email: String,
    val avatar: String? = null
)

// 创建用户请求
data class CreateUserRequest(
    val name: String,
    val email: String
)

// 更新用户请求
data class UpdateUserRequest(
    val name: String? = null,
    val email: String? = null
)

// 分页响应
data class UsersResponse(
    val data: List<User>,
    val page: Int,
    val total: Int
)
```

---

## 创建 Retrofit 实例

“然后创建 Retrofit 实例。”小 Com 展示了代码：

```kotlin
object RetrofitClient {
    
    private const val BASE_URL = "https://api.example.com/"
    
    val instance: ApiService by lazy {
        val logging = LoggingInterceptor.Builder()
            .setLevel(Level.BODY)
            .build()
        
        val client = OkHttpClient.Builder()
            .addInterceptor(logging)
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            .build()
        
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }
}
```

---

## Repository 封装

“最好用 Repository 封装一下。”小 Com 说：

```kotlin
class UserRepository {
    private val api = RetrofitClient.instance
    
    suspend fun getUser(id: String): Result<User> {
        return try {
            val user = api.getUser(id)
            Result.success(user)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun getUsers(page: Int): Result<UsersResponse> {
        return try {
            val response = api.getUsers(page)
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun createUser(name: String, email: String): Result<User> {
        return try {
            val user = api.createUser(CreateUserRequest(name, email))
            Result.success(user)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
```

---

## 在 ViewModel 中使用

“在 ViewModel 中使用 Repository。”小 Com 展示了：

```kotlin
class UserViewModel(
    private val repository: UserRepository = UserRepository()
) : ViewModel() {
    
    private val _userState = MutableStateFlow<UserScreenState>(UserScreenState.Initial)
    val userState: StateFlow<UserScreenState> = _userState
    
    fun loadUser(id: String) {
        viewModelScope.launch {
            _userState.value = UserScreenState.Loading
            
            repository.getUser(id)
                .onSuccess { user ->
                    _userState.value = UserScreenState.Success(user)
                }
                .onFailure { error ->
                    _userState.value = UserScreenState.Error(error.message ?: "未知错误")
                }
        }
    }
}

sealed class UserScreenState {
    object Initial : UserScreenState()
    object Loading : UserScreenState()
    data class Success(val user: User) : UserScreenState()
    data class Error(val message: String) : UserScreenState()
}
```

---

## 在 Compose 中显示

“在 Compose 中显示数据。”小 Com 展示了：

```kotlin
@Composable
fun UserScreen(userId: String) {
    val viewModel: UserViewModel = viewModel()
    val userState by viewModel.userState.collectAsState()
    
    LaunchedEffect(userId) {
        viewModel.loadUser(userId)
    }
    
    Scaffold(
        topBar = {
            TopAppBar(title = { Text("用户详情") })
        }
    ) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentAlignment = Alignment.Center
        ) {
            when (val state = userState) {
                is UserScreenState.Initial -> {
                    Text("请输入用户 ID")
                }
                is UserScreenState.Loading -> {
                    CircularProgressIndicator()
                }
                is UserScreenState.Success -> {
                    UserDetailContent(user = state.user)
                }
                is UserScreenState.Error -> {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(state.message, color = Color.Red)
                        Spacer(modifier = Modifier.height(8.dp))
                        Button(onClick = { viewModel.loadUser(userId) }) {
                            Text("重试")
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun UserDetailContent(user: User) {
    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        AsyncImage(
            model = user.avatar,
            contentDescription = "头像",
            modifier = Modifier
                .size(100.dp)
                .clip(CircleShape)
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Text(
            text = user.name,
            style = MaterialTheme.typography.headlineSmall
        )
        
        Text(
            text = user.email,
            style = MaterialTheme.typography.bodyMedium,
            color = Color.Gray
        )
    }
}
```

---

## 实战：用户列表 + 分页

“我们来做最后一个练习——用户列表 + 分页加载！”小 Com 提议道。

```kotlin
class UsersViewModel : ViewModel() {
    
    private val repository = UserRepository()
    
    private val _users = MutableStateFlow<List<User>>(emptyList())
    val users: StateFlow<List<User>> = _users
    
    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading
    
    private var currentPage = 1
    private var hasMore = true
    
    fun loadMore() {
        if (_isLoading.value || !hasMore) return
        
        viewModelScope.launch {
            _isLoading.value = true
            
            repository.getUsers(currentPage)
                .onSuccess { response ->
                    _users.value = _users.value + response.data
                    hasMore = response.data.isNotEmpty()
                    currentPage++
                }
                .onFailure {
                    // 错误处理
                }
            
            _isLoading.value = false
        }
    }
}

@Composable
fun UsersScreen() {
    val viewModel: UsersViewModel = viewModel()
    val users by viewModel.users.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        onReached = { viewModel.loadMore() }
    ) {
        items(users) { user ->
            UserListItem(user = user)
        }
        
        if (isLoading) {
            item {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator()
                }
            }
        }
    }
}
```

---

## 本课小结

今天林小满学到了：

1. **Retrofit**：网络请求库
2. **@GET / @POST**：HTTP 方法注解
3. **@Path / @Query / @Body**：参数注解
4. **OkHttp**：底层 HTTP 客户端
5. **Gson**：JSON 解析
6. **Repository 模式**：封装数据层
7. **Result**：结果包装

---

“Retrofit 太强大了！”林小满说。

“没错！”小 Com 说，“学会 Retrofit，你就能调用任何 API 了！”

“明天我们学什么？”

“明天学——Room！”小 Com 笑道，“本地数据库！”

---

*”叮——“*

手机通知：**“第十一章 已解锁：Retrofit 网络请求”**

---

### 📚 课后练习

1. 调用一个真实的 API（如 JSONPlaceholder）
2. 实现用户列表的分页加载
3. 做一个搜索功能，带防抖

---

**下集预告**：第十二课 · Room 数据库 · 本地数据存储
