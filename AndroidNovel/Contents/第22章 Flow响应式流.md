---
chapter_id: '22'
title: '第二十二课：Kotlin 协程进阶 · Flow 响应式流'
official_url: 'https://kotlinlang.org/docs/flow.html'
status: 'done'
<invoke name="author">'minimax m2.5 - OpenClaw'
plot_summary:
  time: '第二十二天'
  location: 'Compose 村·河流'
  scene: '小 Com 教小满用 Flow 处理数据流'
  season: '春季'
  environment: '小河边，水在流动'
---

# 第二十二课：Kotlin 协程进阶 · Flow 响应式流

---

“叮——”

林小满发现自己站在一条小河边。水在潺潺流动，非常清澈。

“今天我们要学 Flow！”小 Com 指着河流说，“就像这条河一样，数据会源源不断地流动——这就是 Flow！”

“Flow？”林小满问。

“对！”小 Com 说，“Flow 是 Kotlin 的响应式流，能处理异步数据序列，非常强大！”

---

## 1. 什么是 Flow？

“Flow 是一种异步数据流。”小 Com 介绍道：

**Flow vs suspend：**

| | suspend | Flow |
|---|---|---|
| 返回值 | 单个值 | 多个值（序列） |
| 用途 | 一次性操作 | 异步数据流 |
| 例子 | API 请求 | 数据库观察 |

```kotlin
// suspend：返回单个值
suspend fun getUser(): User { ... }

// Flow：返回数据流
fun getUsers(): Flow<List<User>> { ... }
```

---

## 2. 创建 Flow

“有多种方式创建 Flow。”小 Com 展示了：

```kotlin
// 1. flowOf：创建固定值的 Flow
val flow1 = flowOf(1, 2, 3, 4, 5)

// 2. list.asFlow()：从集合创建
val flow2 = listOf(1, 2, 3).asFlow()

// 3. flow { }：自定义 Flow
val flow3 = flow {
    for (i in 1..5) {
        emit(i)  // 发送数据
        delay(100)  // 模拟异步
    }
}

// 4. ChannelFlow：带多个发射器
val flow4 = channelFlow {
    send(1)
    send(2)
}

// 5. MutableStateFlow：可变的 Flow
val stateFlow = MutableStateFlow(0)
```

---

## 3. 收集 Flow

“创建 Flow 后需要收集。”小 Com 展示了：

```kotlin
// 在协程中收集
CoroutineScope(Dispatchers.Main).launch {
    flow.collect { value ->
        println("收到: $value")
    }
}

// 在 Compose 中收集
@Composable
fun FlowExample() {
    val flow = remember { flowOf(1, 2, 3) }
    
    val value by flow.collectAsState(initial = 0)
    
    Text("值: $value")
}
```

---

## 4. 变换操作符

“Flow 有很多变换操作符。”小 Com 展示了：

```kotlin
// map：转换数据
flowOf(1, 2, 3)
    .map { it * 2 }  // 2, 4, 6
    .collect { println(it) }

// filter：过滤数据
flowOf(1, 2, 3, 4, 5)
    .filter { it > 2 }  // 3, 4, 5
    .collect { println(it) }

// take：取前几个
flowOf(1, 2, 3, 4, 5)
    .take(3)  // 1, 2, 3
    .collect { println(it) }

// drop：跳过前几个
flowOf(1, 2, 3, 4, 5)
    .drop(2)  // 3, 4, 5
    .collect { println(it) }

// flatMap：扁平化
flowOf(1, 2, 3)
    .flatMapConcat { flowOf(it * 2, it * 2) }  // 2, 2, 4, 4, 6, 6
    .collect { println(it) }
```

---

## 5. 组合操作符

“还有组合操作符。”小 Com 展示了：

```kotlin
// zip：组合两个 Flow
val flow1 = flowOf(1, 2, 3)
val flow2 = flowOf("a", "b", "c")

flow1.zip(flow2) { num, letter ->
    "$num$letter"
}.collect { println(it) }  // 1a, 2b, 3c

// combine：组合两个 Flow（任一变化都触发）
val flowA = MutableStateFlow(1)
val flowB = MutableStateFlow("a")

combine(flowA, flowB) { a, b ->
    "$a$b"
}.collect { println(it) }  // 1a

flowA.value = 2  // 触发: 2a
flowB.value = "b"  // 触发: 2b
```

---

## 6. 错误处理

“Flow 支持错误处理。”小 Com 展示了：

```kotlin
// catch：捕获异常
flowOf(1, 2, 3)
    .map { 
        if (it == 2) throw Exception("错误")
        it 
    }
    .catch { e -> println("捕获: ${e.message}") }
    .collect { println(it) }

// retry：重试
flowOf(1, 2, 3)
    .map { 
        if (it == 2) throw Exception("错误")
        it 
    }
    .retry(3)  // 重试3次
    .collect { println(it) }

// onEach + onSuccess + onFailure
flowOf(1, 2, 3)
    .onEach { println("数据: $it") }
    .onStart { println("开始") }
    .onCompletion { println("完成") }
    .catch { println("错误: ${it.message}") }
    .collect { }
```

---

## 7. StateFlow

“StateFlow 是特殊的 Flow。”小 Com 介绍了：

```kotlin
// 创建 StateFlow
val stateFlow = MutableStateFlow(0)

// 读取值
val value = stateFlow.value

// 作为 StateFlow（只读）
val readOnlyFlow: StateFlow<Int> = stateFlow

// 在 Compose 中使用
@Composable
fun StateFlowExample() {
    val stateFlow = remember { MutableStateFlow(0) }
    
    // collectAsState：转为 Compose State
    val value by stateFlow.collectAsState()
    
    Button(onClick = { stateFlow.value++ }) {
        Text("计数: $value")
    }
}
```

---

## 8. SharedFlow

“SharedFlow 也是特殊的 Flow。”小 Com 展示了：

```kotlin
// 创建 SharedFlow
val sharedFlow = MutableSharedFlow<Int>()

// 发送数据
sharedFlow.emit(1)

// 或者
sharedFlow.tryEmit(1)  // 不抛异常

// 作为 SharedFlow（只读）
val readOnlyFlow: SharedFlow<Int> = sharedFlow

// 收集
sharedFlow.collect { value ->
    println(value)
}

// replay：重新发送几个历史值
val replayFlow = MutableSharedFlow<Int>(replay = 2)
```

---

## 9. 实战：搜索功能

“我们来做最后一个练习——带防抖的搜索功能！”小 Com 提议道。

```kotlin
@HiltViewModel
class SearchViewModel @Inject constructor(
    private val api: ApiService
) : ViewModel() {
    
    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery
    
    // 搜索结果
    val searchResults: StateFlow<List<SearchResult>> = _searchQuery
        .debounce(300)  // 防抖：等待300ms
        .filter { it.length >= 2 }  // 至少2个字符
        .distinctUntilChanged()  // 过滤重复
        .flatMapLatest { query ->  // 只处理最新请求
            flow {
                emit(emptyList())  // 先显示空
                try {
                    val results = api.search(query)
                    emit(results)
                } catch (e: Exception) {
                    emit(emptyList())
                }
            }
        }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = emptyList()
        )
    
    fun updateQuery(query: String) {
        _searchQuery.value = query
    }
}

@Composable
fun SearchScreen(
    viewModel: SearchViewModel = viewModel()
) {
    val query by viewModel.searchQuery.collectAsState()
    val results by viewModel.searchResults.collectAsState()
    
    Column {
        OutlinedTextField(
            value = query,
            onValueChange = viewModel::updateQuery,
            placeholder = { Text("搜索...") }
        )
        
        LazyColumn {
            items(results) { result ->
                Text(result.title)
            }
        }
    }
}
```

---

## 10. 实战：倒计时

“再来一个——倒计时功能！”

```kotlin
@Composable
fun CountdownTimer(
    seconds: Int,
    onFinish: () -> Unit
) {
    val countdownFlow = remember {
        flow {
            for (i in seconds downTo 0) {
                emit(i)
                delay(1000)
            }
            onFinish()
        }
    }
    
    val currentSeconds by countdownFlow.collectAsState(initial = seconds)
    
    Text("倒计时: $currentSeconds 秒")
}

// 使用
@Composable
fun TimerScreen() {
    var showTimer by remember { mutableStateOf(false) }
    
    Column {
        Button(onClick = { showTimer = true }) {
            Text("开始倒计时")
        }
        
        if (showTimer) {
            CountdownTimer(
                seconds = 10,
                onFinish = { showTimer = false }
            )
        }
    }
}
```

---

## 本课小结

今天林小满学到了：

1. **Flow**：异步数据流
2. **创建 Flow**：flowOf / asFlow / flow { }
3. **收集 Flow**：collect / collectAsState
4. **变换操作符**：map / filter / take / drop
5. **组合操作符**：zip / combine
6. **错误处理**：catch / retry
7. **StateFlow**：可观察的状态
8. **SharedFlow**：事件流
9. **debounce**：防抖
10. **flatMapLatest**：只处理最新请求

---

“Flow 太强大了！”林小满说。

“没错！”小 Com 说，“学会 Flow，你就能处理各种异步数据流了！”

---

*”叮——“*

手机通知：**“第二十二章 已解锁：Flow 响应式流”**

---

**下集预告**：第二十三课 · Compose 性能优化 · 让 App 更快
