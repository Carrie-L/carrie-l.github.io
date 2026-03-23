---
chapter_id: '21'
title: '第二十一课：WorkManager 后台任务 · 定时任务'
official_url: 'https://developer.android.com/topic/libraries/architecture/workmanager'
status: 'done'
<invoke name="author">'minimax m2.5 - OpenClaw'
plot_summary:
  time: '第二十一天'
  location: 'Compose 村·调度中心'
  scene: '小 Com 教小满用 WorkManager 处理后台任务'
  season: '春季'
  environment: '调度中心大屏幕上显示任务列表'
---

# 第二十一课：WorkManager 后台任务 · 定时任务

---

“叮——”

林小满发现自己站在一个调度中心里。大屏幕上显示着各种定时任务。

“今天我们要学 WorkManager！”小 Com 拿着调度表走了过来，“学会这个，你就能让 App 在后台定时执行任务，比如同步数据、清理缓存、发送报告！”

“后台任务？”林小满问。

“对！”小 Com 说，“有些任务不需要用户守着，比如凌晨3点同步数据，这就需要 WorkManager！”

---

## 1. 什么是 WorkManager？

“WorkManager 是 Android 的后台任务管理库。”小 Com 介绍道：

**WorkManager 的特点：**
- ✅ 保证任务执行（即使 App 退出）
- ✅ 支持定时任务
- ✅ 支持约束条件（网络、充电等）
- ✅ 电池友好
- ✅ 支持链式任务

---

## 2. 添加依赖

“首先添加依赖。”小 Com 写道：

```kotlin
dependencies {
    implementation "androidx.work:work-runtime-ktx:2.9.0"
    
    // 如果用 Hilt
    implementation "androidx.hilt:hilt-work:1.1.0"
    ksp "androidx.hilt:hilt-compiler:1.1.0"
}
```

---

## 3. 创建 Worker

“首先创建 Worker。”小 Com 展示了：

```kotlin
class SyncDataWorker(
    context: Context,
    workerParams: WorkerParameters
) : CoroutineWorker(context, workerParams) {
    
    override suspend fun doWork(): Result {
        return try {
            // 执行同步任务
            val data = fetchDataFromServer()
            saveToLocalDatabase(data)
            
            Result.success()
        } catch (e: Exception) {
            if (runAttemptCount < 3) {
                Result.retry()  // 重试
            } else {
                Result.failure()  // 失败
            }
        }
    }
    
    private suspend fun fetchDataFromServer(): String {
        // 模拟网络请求
        delay(2000)
        return "data"
    }
    
    private suspend fun saveToLocalDatabase(data: String) {
        // 保存到本地
    }
}
```

---

## 4. 一次性任务

“先看一次性任务。”小 Com 展示了：

```kotlin
@Composable
fun OneTimeTaskExample() {
    val workRequest = OneTimeWorkRequestBuilder<SyncDataWorker>()
        .build()
    
    WorkManager.getInstance(context)
        .enqueue(workRequest)
}
```

---

## 5. 定时任务

“然后是定时任务。”小 Com 展示了：

```kotlin
@Composable
fun PeriodicTaskExample() {
    // 每小时执行一次
    val workRequest = PeriodicWorkRequestBuilder<SyncDataWorker>(
        1, TimeUnit.HOURS  // 最小间隔
    )
        .setConstraints(
            Constraints.Builder()
                .setRequiredNetworkType(NetworkType.CONNECTED)  // 需要网络
                .setRequiresBatteryNotLow(true)  // 电量不低
                .build()
        )
        .setInitialDelay(1, TimeUnit.HOURS)  // 首次延迟
        .build()
    
    WorkManager.getInstance(context)
        .enqueueUniquePeriodicWork(
            "sync_data",
            ExistingPeriodicWorkPolicy.KEEP,  // 保留已有的
            workRequest
        )
}
```

---

## 6. 约束条件

“可以设置约束条件。”小 Com 展示了：

```kotlin
val constraints = Constraints.Builder()
    .setRequiredNetworkType(NetworkType.CONNECTED)      // 需要网络
    .setRequiresBatteryNotLow(true)                     // 电量不低
    .setRequiresCharging(true)                          // 充电中
    .setRequiresDeviceIdle(true)                        // 设备空闲
    .setRequiresStorageNotLow(true)                     // 存储不低
    .build()

val workRequest = OneTimeWorkRequestBuilder<SyncDataWorker>()
    .setConstraints(constraints)
    .build()
```

---

## 7. 延迟执行

“可以延迟执行。”小 Com 展示了：

```kotlin
val workRequest = OneTimeWorkRequestBuilder<SyncDataWorker>()
    .setInitialDelay(10, TimeUnit.MINUTES)  // 延迟 10 分钟执行
    .build()

// 或者立即开始，但设置输入数据
val inputData = workDataOf(
    "key" to "value"
)

val workRequest = OneTimeWorkRequestBuilder<SyncDataWorker>()
    .setInputData(inputData)
    .build()
```

---

## 8. 监听任务状态

“可以监听任务状态。”小 Com 展示了：

```kotlin
@Composable
fun ObserveWorkStatus() {
    val workManager = WorkManager.getInstance(context)
    
    val workInfos = workManager.getWorkInfosForUniqueWorkLiveData("sync_data")
    
    // 或者用 Flow
    LaunchedEffect(Unit) {
        workManager.getWorkInfosForUniqueWorkFlow("sync_data")
            .collect { workInfos ->
                workInfos.forEach { workInfo ->
                    when (workInfo.state) {
                        WorkInfo.State.ENQUEUED -> println("排队中")
                        WorkInfo.State.RUNNING -> println("执行中")
                        WorkInfo.State.SUCCEEDED -> println("成功")
                        WorkInfo.State.FAILED -> println("失败")
                        WorkInfo.State.BLOCKED -> println("阻塞")
                        WorkInfo.State.CANCELLED -> println("取消")
                    }
                }
            }
    }
}
```

---

## 9. 链式任务

“可以创建链式任务。”小 Com 展示了：

```kotlin
fun createWorkChain() {
    val workA = OneTimeWorkRequestBuilder<WorkerA>().build()
    val workB = OneTimeWorkRequestBuilder<WorkerB>().build()
    val workC = OneTimeWorkRequestBuilder<WorkerC>().build()
    
    // A -> B -> C 顺序执行
    WorkManager.getInstance(context)
        .beginUniqueWork(
            "work_chain",
            ExistingWorkPolicy.REPLACE,
            workA
        )
        .then(workB)
        .then(workC)
        .enqueue()
}

// Worker A
class WorkerA(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {
    override suspend fun doWork(): Result {
        // 设置输出，供下一个 Worker 使用
        val outputData = workDataOf("result" to "A 完成")
        return Result.success(outputData)
    }
}

// Worker B 接收 A 的输出
class WorkerB(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {
    override suspend fun doWork(): Result {
        // 接收 A 的输出
        val inputFromA = inputData.getString("result")
        println("收到 A 的数据: $inputFromA")
        
        return Result.success()
    }
}
```

---

## 10. 带 Hilt 的 Worker

“可以用 Hilt 注入依赖。”小 Com 展示了：

```kotlin
@HiltWorker
class SyncDataWorker @Inject constructor(
    @ApplicationContext private val context: Context,
    workerParams: WorkerParameters,
    private val repository: UserRepository  // 注入 Repository
) : CoroutineWorker(context, workerParams) {
    
    override suspend fun doWork(): Result {
        return try {
            repository.syncData()
            Result.success()
        } catch (e: Exception) {
            Result.failure()
        }
    }
}

// 使用
@Composable
fun HiltWorkerExample() {
    val workRequest = OneTimeWorkRequestBuilder<SyncDataWorker>()
        .build()
    
    WorkManager.getInstance(context).enqueue(workRequest)
}
```

---

## 11. 实战：数据同步

“我们来做最后一个练习——数据同步任务！”小 Com 提议道。

```kotlin
// 1. 同步 Worker
@HiltWorker
class DataSyncWorker @Inject constructor(
    @ApplicationContext private val context: Context,
    workerParams: WorkerParameters,
    private val api: ApiService,
    private val database: AppDatabase
) : CoroutineWorker(context, workerParams) {
    
    override suspend fun doWork(): Result {
        return try {
            // 1. 从服务器获取数据
            val remoteData = api.getAllData()
            
            // 2. 保存到本地数据库
            database.dataDao().insertAll(remoteData)
            
            // 3. 返回成功
            Result.success(
                workDataOf("synced_count" to remoteData.size)
            )
        } catch (e: Exception) {
            if (runAttemptCount < 3) {
                Result.retry()  // 重试最多3次
            } else {
                Result.failure()  // 失败
            }
        }
    }
}

// 2. 调度任务
@Composable
fun ScheduleDataSync() {
    val constraints = Constraints.Builder()
        .setRequiredNetworkType(NetworkType.CONNECTED)
        .setRequiresBatteryNotLow(true)
        .build()
    
    val workRequest = PeriodicWorkRequestBuilder<DataSyncWorker>(
        repeatInterval = 6,
        repeatIntervalTimeUnit = TimeUnit.HOURS  // 每6小时同步一次
    )
        .setConstraints(constraints)
        .setBackoffCriteria(
            BackoffPolicy.EXPONENTIAL,
            WorkRequest.MIN_BACKOFF_MILLIS,
            TimeUnit.MILLISECONDS
        )
        .build()
    
    WorkManager.getInstance(context)
        .enqueueUniquePeriodicWork(
            "data_sync",
            ExistingPeriodicWorkPolicy.KEEP,
            workRequest
        )
}

// 3. 取消任务
fun cancelDataSync(context: Context) {
    WorkManager.getInstance(context)
        .cancelUniqueWork("data_sync")
}
```

---

## 本课小结

今天林小满学到了：

1. **WorkManager**：后台任务管理
2. **CoroutineWorker**：协程 Worker
3. **OneTimeWorkRequest**：一次性任务
4. **PeriodicWorkRequest**：定时任务
5. **Constraints**：约束条件
6. **setInitialDelay**：延迟执行
7. **WorkInfo**：任务状态监听
8. **链式任务**：beginUniqueWork + then
9. **HiltWorker**：带依赖注入的 Worker

---

“WorkManager 太强大了！”林小满说。

“没错！”小 Com 说，“学会 WorkManager，你就能做后台定时任务了！”

---

*”叮——“*

手机通知：**“第二十一章 已解锁：WorkManager 后台任务”**

---

**下集预告**：第二十二课 · Kotlin 协程进阶 · Flow 响应式流
