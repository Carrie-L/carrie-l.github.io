---
chapter_id: '13'
title: '第十三课：Hilt 依赖注入 · 解耦与测试'
official_url: 'https://dagger.dev/hilt/'
status: 'done'
author: 'minimax m2.5 - OpenClaw'
plot_summary:
  time: '第十三天'
  location: 'Compose 村·工厂'
  scene: '小 Com 教小满用 Hilt 自动"生产"对象'
  season: '春季'
  environment: '自动化工厂，机器人在组装零件'
---

# 第十三课：Hilt 依赖注入 · 解耦与测试

---

“叮——”

林小满发现自己站在一个自动化工厂里。机器人在流水线上组装各种零件。

“今天我们要学 Hilt！”小 Com 戴着安全帽走了过来，“Hilt 是 Google 推荐的依赖注入库，学会它，你就不用手动创建对象了！”

“依赖注入？”林小满问。

“对！”小 Com 解释说，“就像这个工厂，零件（对象）由机器人（Hilt）自动组装，而不是人工一个个拧螺丝！”

---

## 什么是依赖注入？

“先说说为什么需要依赖注入。”小 Com 画了个图：

**不用 DI（手动创建）**：
```kotlin
class UserViewModel : ViewModel() {
    // 手动创建
    private val repository = UserRepository(
        api = RetrofitClient.instance,  // 手动注入
        userDao = AppDatabase.getDatabase(context)
    )
    
    fun loadUser() { ... }
}
```

**用 DI（Hilt 自动创建）**：
```kotlin
class UserViewModel @Inject constructor(
    private val repository: UserRepository  // Hilt 自动注入
) : ViewModel() {
    
    fun loadUser() { ... }
}
```

---

## 添加依赖

“首先添加依赖。”小 Com 写道：

```kotlin
// build.gradle (project)
plugins {
    id 'com.google.dagger.hilt.android' version '2.48.1' apply false
}

// build.gradle (app)
plugins {
    id 'com.google.dagger.hilt.android'
}

dependencies {
    implementation "com.google.dagger:hilt-android:2.48.1"
    ksp "com.google.dagger:hilt-compiler:2.48.1"
    implementation "androidx.hilt:hilt-navigation-compose:1.1.0"
}
```

---

## Application 配置

“在 Application 类上添加注解。”小 Com 展示了：

```kotlin
@HiltAndroidApp
class MyApplication : Application()
```

---

## @Inject 注解

“在构造函数上添加 @Inject。”小 Com 说：

```kotlin
class UserRepository @Inject constructor(
    private val api: ApiService,
    private val userDao: UserDao
) {
    suspend fun getUsers(): List<User> { ... }
}

class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {
    // ...
}
```

---

## @Module 和 @Provides

“有时候需要手动提供对象，比如接口或第三方库。”小 Com 展示了：

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    
    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient {
        return OkHttpClient.Builder()
            .build()
    }
    
    @Provides
    @Singleton
    fun provideRetrofit(okHttpClient: OkHttpClient): Retrofit {
        return Retrofit.Builder()
            .baseUrl("https://api.example.com/")
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }
    
    @Provides
    @Singleton
    fun provideApiService(retrofit: Retrofit): ApiService {
        return retrofit.create(ApiService::class.java)
    }
}

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {
    
    @Provides
    @Singleton
    fun provideDatabase(context: Context): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "app_database"
        ).build()
    }
    
    @Provides
    @Singleton
    fun provideUserDao(database: AppDatabase): UserDao {
        return database.userDao()
    }
}
```

---

## @Singleton

“用 @Singleton 让对象只创建一次。”小 Com 说：

```kotlin
@Singleton
class UserRepository @Inject constructor(
    private val api: ApiService,
    private val userDao: UserDao
) {
    // 整个应用只有一个实例
}
```

---

## @ViewModelInject（旧）vs @HiltViewModel（新）

“ViewModel 需要特殊处理。”小 Com 展示了：

```kotlin
// 旧写法（已废弃）
class UserViewModel @ViewModelInject constructor(
    private val repository: UserRepository
) : ViewModel()

// 新写法（推荐）
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel()
```

---

## 在 Compose 中使用

“在 Compose 中使用 Hilt 很简单。”小 Com 展示了：

```kotlin
@Composable
fun MyApp() {
    // 1. 注入 Navigation
    val navController = rememberNavController()
    
    NavHost(navController = navController, startDestination = "home") {
        composable("home") {
            // 2. 使用 viewModel() 自动注入
            val viewModel: HomeViewModel = viewModel()
            HomeScreen(viewModel = viewModel)
        }
    }
}

// 3. Activity/Fragment 注入
@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MyApp()
        }
    }
}
```

---

## @Qualifier：自定义限定符

“如果有两个同类型的对象，就需要限定符。”小 Com 展示了：

```kotlin
@Qualifier
@Retention(AnnotationRetention.BINARY)
annotation class IoDispatcher

@Qualifier
@Retention(AnnotationRetention.BINARY)
annotation class MainDispatcher

class UseCase @Inject constructor(
    @IoDispatcher private val ioDispatcher: CoroutineDispatcher,
    @MainDispatcher private val mainDispatcher: CoroutineDispatcher
) {
    // ...
}
```

---

## 实战：完整的 Hilt 项目

“我们来做最后一个练习——完整的 Hilt 项目结构！”小 Com 提议道。

```kotlin
// 1. Application
@HiltAndroidApp
class MyApplication

// 2. Module
@Module
@InstallIn(SingletonComponent::class)
object AppModule {
    @Provides
    @Singleton
    fun provideRepository(
        api: ApiService,
        userDao: UserDao
    ): UserRepository {
        return UserRepository(api, userDao)
    }
}

// 3. ViewModel
@HiltViewModel
class HomeViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {
    // ...
}

// 4. Activity
@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MyApp()
        }
    }
}

// 5. Composable
@Composable
fun HomeScreen(
    viewModel: HomeViewModel = viewModel()
) {
    // ...
}
```

---

## 为什么要用 Hilt？

小 Com 总结了使用 Hilt 的好处：

| 好处 | 说明 |
|------|------|
| **解耦** | 不需要手动创建对象 |
| **可测试** | 方便替换为 Mock 对象 |
| **单例** | 自动管理对象生命周期 |
| **简化代码** | 减少样板代码 |
| **官方推荐** | Google 官方推荐 |

---

## 本课小结

今天林小满学到了：

1. **依赖注入**：对象由外部提供
2. **@HiltAndroidApp**：Application 注解
3. **@Inject**：构造函数注解
4. **@Module / @Provides**：手动提供对象
5. **@Singleton**：单例
6. **@HiltViewModel**：ViewModel 注入
7. **@Qualifier**：自定义限定符

---

“Hilt 太强大了！”林小满说。

“没错！”小 Com 说，“学会 Hilt，你就能写出高质量的 Android 代码了！”

“明天我们学什么？”

“明天学——MVVM 架构！”小 Com 笑道，“把一切都组织起来！”

---

*”叮——“*

手机通知：**“第十三章 已解锁：Hilt 依赖注入”**

---

### 📚 课后练习

1. 给现有项目添加 Hilt
2. 创建自定义 @Qualifier
3. 测试 ViewModel 能否正常注入

---

**下集预告**：第十四课 · MVVM 架构 · 完整项目结构
