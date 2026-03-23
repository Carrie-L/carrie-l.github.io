---
chapter_id: '12'
title: '第十二课：Room 数据库 · 本地数据存储'
official_url: 'https://developer.android.com/training/data-storage/room'
status: 'done'
author: 'minimax m2.5 - OpenClaw'
plot_summary:
  time: '第十二天'
  location: 'Compose 村·图书馆'
  scene: '小 Com 教小满用 Room 存储数据'
  season: '春季'
  environment: '古老的图书馆，书架上摆满了书'
---

# 第十二课：Room 数据库 · 本地数据存储

---

“叮——”

林小满发现自己站在一个图书馆里。书架上摆满了各种书籍，空气中弥漫着纸张的香味。

“今天我们要学 Room！”小 Com 拿着一本书走了过来，“Room 是 Android 的本地数据库，学会它，你就能在手机里存储数据！”

“数据库？”林小满问。

“对！”小 Com 说，“就像图书馆存书一样，Room 能在手机里持久化存储数据！”

---

## 添加依赖

“首先添加依赖。”小 Com 写道：

```kotlin
// build.gradle
plugins {
    id 'com.google.devtools.ksp' version '1.9.10-1.0.13'
}

dependencies {
    implementation "androidx.room:room-runtime:2.6.1"
    implementation "androidx.room:room-ktx:2.6.1"
    ksp "androidx.room:room-compiler:2.6.1"
}
```

---

## 定义实体

“首先定义实体——就是数据库的表。”小 Com 展示了代码：

```kotlin
@Entity(tableName = "users")
data class User(
    @PrimaryKey
    val id: String,
    
    val name: String,
    
    val email: String,
    
    val avatar: String? = null,
    
    val createdAt: Long = System.currentTimeMillis()
)
```

---

## 定义 DAO

“然后定义 DAO——数据库操作接口。”小 Com 说：

```kotlin
@Dao
interface UserDao {
    
    // 插入
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUser(user: User)
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUsers(users: List<User>)
    
    // 查询
    @Query("SELECT * FROM users")
    suspend fun getAllUsers(): List<User>
    
    @Query("SELECT * FROM users WHERE id = :id")
    suspend fun getUserById(id: String): User?
    
    @Query("SELECT * FROM users WHERE name LIKE '%' || :query || '%'")
    suspend fun searchUsers(query: String): List<User>
    
    // 更新
    @Update
    suspend fun updateUser(user: User)
    
    // 删除
    @Delete
    suspend fun deleteUser(user: User)
    
    @Query("DELETE FROM users")
    suspend fun deleteAllUsers()
}
```

---

## 定义 Database

“然后定义 Database——数据库本身。”小 Com 展示了：

```kotlin
@Database(
    entities = [User::class],
    version = 1,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
    
    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null
        
        fun getDatabase(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "app_database"
                ).build()
                INSTANCE = instance
                instance
            }
        }
    }
}
---

## Repository 封装

“用 Repository 封装数据操作。”小 Com 说：

```kotlin
class UserRepository(private val userDao: UserDao) {
    
    suspend fun insertUser(user: User) {
        userDao.insertUser(user)
    }
    
    suspend fun getAllUsers(): List<User> {
        return userDao.getAllUsers()
    }
    
    suspend fun getUserById(id: String): User? {
        return userDao.getUserById(id)
    }
    
    suspend fun searchUsers(query: String): List<User> {
        return userDao.searchUsers(query)
    }
    
    suspend fun deleteUser(user: User) {
        userDao.deleteUser(user)
    }
}
```

---

## Flow 响应式查询

“Room 支持 Flow，可以实时观察数据变化！”小 Com 展示了：

```kotlin
@Dao
interface UserDao {
    
    // 返回 Flow，数据变化时自动更新
    @Query("SELECT * FROM users ORDER BY createdAt DESC")
    fun getAllUsersFlow(): Flow<List<User>>
    
    @Query("SELECT * FROM users WHERE id = :id")
    fun getUserByIdFlow(id: String): Flow<User?>
    
    @Query("SELECT * FROM users WHERE name LIKE '%' || :query || '%'")
    fun searchUsersFlow(query: String): Flow<List<User>>
}
```

---

## 在 ViewModel 中使用

“在 ViewModel 中使用 Room。”小 Com 展示了：

```kotlin
class UserViewModel(
    private val repository: UserRepository
) : ViewModel() {
    
    // 响应式数据
    val allUsers: Flow<List<User>> = repository.getAllUsersFlow()
    
    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery
    
    // 搜索结果
    val searchResults: StateFlow<List<User>> = _searchQuery
        .debounce(300)  // 防抖
        .flatMapLatest { query ->
            if (query.isBlank()) {
                flowOf(emptyList())
            } else {
                repository.searchUsersFlow(query)
            }
        }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = emptyList()
        )
    
    fun updateSearchQuery(query: String) {
        _searchQuery.value = query
    }
    
    fun insertUser(user: User) {
        viewModelScope.launch {
            repository.insertUser(user)
        }
    }
    
    fun deleteUser(user: User) {
        viewModelScope.launch {
            repository.deleteUser(user)
        }
    }
}
```

---

## 在 Compose 中显示

“在 Compose 中显示数据。”小 Com 展示了：

```kotlin
@Composable
fun UsersScreen(viewModel: UserViewModel = viewModel()) {
    val users by viewModel.allUsers.collectAsState(initial = emptyList())
    
    LazyColumn {
        items(users, key = { it.id }) { user ->
            UserItem(
                user = user,
                onDelete = { viewModel.deleteUser(user) }
            )
        }
    }
}

@Composable
fun UserItem(
    user: User,
    onDelete: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        AsyncImage(
            model = user.avatar,
            contentDescription = null,
            modifier = Modifier
                .size(48.dp)
                .clip(CircleShape)
        )
        
        Spacer(modifier = Modifier.width(12.dp))
        
        Column(modifier = Modifier.weight(1f)) {
            Text(user.name, style = MaterialTheme.typography.titleMedium)
            Text(user.email, style = MaterialTheme.typography.bodySmall, color = Color.Gray)
        }
        
        IconButton(onClick = onDelete) {
            Icon(Icons.Default.Delete, contentDescription = "删除")
        }
    }
}
```

---

## 实战：网络数据缓存

“我们来做最后一个练习——网络数据缓存！”小 Com 提议道。

```kotlin
class UserRepository(
    private val api: ApiService,
    private val userDao: UserDao
) {
    // 优先从网络获取，存入本地
    suspend fun refreshUsers(): Result<List<User>> {
        return try {
            val users = api.getUsers()
            userDao.insertUsers(users)
            Result.success(users)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    // 本地数据（优先显示）
    fun getUsers(): Flow<List<User>> = userDao.getAllUsersFlow()
    
    // 如果本地没有，从网络加载
    suspend fun getUsersWithCache(): List<User> {
        val localUsers = userDao.getAllUsers()
        return if (localUsers.isEmpty()) {
            val remoteUsers = api.getUsers()
            userDao.insertUsers(remoteUsers)
            remoteUsers
        } else {
            localUsers
        }
    }
}
```

---

## 本课小结

今天林小满学到了：

1. **Room**：本地数据库
2. **Entity**：数据表定义
3. **DAO**：数据库操作
4. **Database**：数据库实例
5. **Repository**：数据仓库
6. **Flow**：响应式查询
7. **缓存**：网络 + 本地

---

“Room 太强大了！”林小满说。

“没错！”小 Com 说，“学会 Room，你就能在手机里存数据了！”

“明天我们学什么？”

“明天学——Hilt！”小 Com 笑道，“依赖注入！”

---

*”叮——“*

手机通知：**“第十二章 已解锁：Room 数据库”**

---

### 📚 课后练习

1. 创建一个 Todo 应用，用 Room 存储
2. 实现数据的增删改查
3. 实现网络数据缓存

---

**下集预告**：第十三课 · Hilt 依赖注入 · 解耦与测试
