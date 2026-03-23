---
chapter_id: '23'
title: '第二十三课：Compose 性能优化 · 让 App 更快'
official_url: 'https://developer.android.com/compose/performance'
status: 'done'
<invoke name="author">'minimax m2.5 - OpenClaw'
plot_summary:
  time: '第二十三天'
  location: 'Compose 村·维修站'
  scene: '小 Com 教小满优化 Compose 性能'
  season: '春季'
  environment: '维修站里工具齐全'
---

# 第二十三课：Compose 性能优化 · 让 App 更快

---

“叮——”

林小满发现自己站在一个维修站里。墙上挂满了各种工具。

“今天我们要学性能优化！”小 Com 拿着扳手走了过来，“再好的代码，如果不优化，也会卡顿！”

“性能优化？”林小满问。

“对！”小 Com 说，“学会优化，你的 App 就会变得丝般顺滑！”

---

## 1. 重组（Recomposition）原则

“先理解重组。”小 Com 介绍了：

**重组规则：**
- ✅ 状态变化时重组
- ❌ 不要在重组中创建新对象
- ❌ 不要在重组中做耗时操作

```kotlin
// ❌ 错误：在重组中创建对象
@Composable
fun BadExample(items: List<String>) {
    Column {
        items.forEach { item ->
            // 每次重组都会创建新 lambda
            ItemCard(name = item)  // Good
        }
    }
}

// ✅ 正确：用 remember 缓存
@Composable
fun GoodExample(items: List<String>) {
    LazyColumn {
        items(items) { item ->
            ItemCard(name = item)
        }
    }
}
```

---

## 2. 使用 remember

“用 remember 避免重复计算。”小 Com 展示了：

```kotlin
@Composable
fun RememberExample(data: String) {
    // 只计算一次
    val processedData = remember(data) {
        processData(data)  // 耗时操作
    }
    
    Text(processedData)
}
```

---

## 3. 稳定的数据类型

“用稳定的数据类型。”小 Com 展示了：

```kotlin
// ❌ 不稳定：每次重组创建新对象
@Composable
fun BadExample() {
    val items = listOf(1, 2, 3)  // 每次重组都新建
    LazyColumn(items = items) { }
}

// ✅ 稳定：记住列表
@Composable
fun GoodExample() {
    val items = remember { listOf(1, 2, 3) }  // 只创建一次
    LazyColumn(items = items) { }
}

// ✅ 更稳定：用 data class + @Stable
@Stable
class StableData(val value: String)
```

---

## 4. key 参数

“用 key 优化列表。”小 Com 展示了：

```kotlin
// ❌ 错误：没有 key
@Composable
fun BadList(items: List<Item>) {
    LazyColumn {
        items(items) { item ->
            ItemCard(item = item)
        }
    }
}

// ✅ 正确：用 key
@Composable
fun GoodList(items: List<Item>) {
    LazyColumn {
        items(
            items = items,
            key = { it.id }  // 用唯一 ID 作为 key
        ) { item ->
            ItemCard(item = item)
        }
    }
}
```

---

## 5. 避免不必要的重组

“用 Stable 和 immutable 数据。”小 Com 展示了：

```kotlin
// ✅ 用 immutable 数据
private val ImmutableList<T> = listOf(...)

// ✅ 用 remember 避免重组
@Composable
fun StableExample() {
    val state = remember { mutableStateOf(0) }
}

// ✅ 用 derivedStateOf 减少派生
@Composable
fun DerivedExample(items: List<String>) {
    val sortedItems = remember(items) {
        derivedStateOf { items.sorted() }
    }
}
```

---

## 6. 延迟加载

“用 rememberCoroutineScope 延迟加载。”小 Com 展示了：

```kotlin
@Composable
fun LazyLoadExample() {
    var data by remember { mutableStateOf<String?>(null) }
    val scope = rememberCoroutineScope()
    
    Button(onClick = {
        scope.launch {
            data = loadData()  // 点击时才加载
        }
    }) {
        Text("加载数据")
    }
    
    data?.let {
        Text(it)
    }
}
```

---

## 7. 优化图片加载

“图片加载要优化。”小 Com 展示了：

```kotlin
// ✅ 用 Coil 优化图片加载
AsyncImage(
    model = imageUrl,
    contentDescription = null,
    modifier = Modifier.size(100.dp),
    
    // 加载中显示
    loading = {
        CircularProgressIndicator()
    },
    
    // 加载失败显示
    error = {
        Image(
            painter = painterResource(R.drawable.placeholder),
            contentDescription = null
        )
    },
    
    // 变换
    transform = {
        it.circleCrop()
    }
)
```

---

## 8. 减少嵌套

“减少 UI 嵌套层级。”小 Com 展示了：

```kotlin
// ❌ 嵌套太深
@Composable
fun DeepNesting() {
    Column {
        Row {
            Column {
                // 太多嵌套
            }
        }
    }
}

// ✅ 用更少的层级
@Composable
fun ShallowNesting() {
    Column {
        // 直接用 Row，没有中间层
    }
}
```

---

## 9. 使用 derivedStateOf

“用 derivedStateOf 减少计算。”小 Com 展示了：

```kotlin
@Composable
fun DerivedStateExample(items: List<Item>) {
    // ❌ 每次重组都排序
    val sortedItems = items.sortedByDescending { it.score }
    
    // ✅ 只在 items 变化时重新排序
    val sortedItems = remember(items) {
        derivedStateOf { items.sortedByDescending { it.score } }
    }
    
    LazyColumn {
        items(sortedItems.value) { item ->
            ItemCard(item = item)
        }
    }
}
```

---

## 10. 实战：优化列表

“我们来做最后一个练习——优化大列表！”小 Com 提议道。

```kotlin
// 优化前
@Composable
fun BadLargeList(items: List<Item>) {
    LazyColumn {
        items(items) { item ->
            // 没有 key，每次都重组
            ItemRow(item = item)
        }
    }
}

// 优化后
@Composable
fun OptimizedLargeList(
    items: List<Item>,
    onItemClick: (Item) -> Unit
) {
    LazyColumn(
        // 1. 预加载更多
        beyondBoundsItemCount = 5,
        
        // 2. 使用 key
        key = { it.id }
    ) {
        // 3. 分离 header 和 items
        stickyHeader {
            Text("列表头")
        }
        
        items(
            items = items,
            key = { item -> item.id }
        ) { item ->
            // 4. 用 Stable 的点击回调
            ItemRow(
                item = item,
                onClick = remember(item.id) {
                    { onItemClick(item) }
                }
            )
        }
    }
}

@Composable
fun ItemRow(
    item: Item,
    onClick: () -> Unit
) {
    // 5. 减少不必要的重组
    val modifier = remember(item.id) { Modifier }
    
    Card(
        onClick = onClick,
        modifier = modifier
            .fillMaxWidth()
            .padding(4.dp)
    ) {
        Row(
            modifier = Modifier.padding(12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            AsyncImage(
                model = item.imageUrl,
                contentDescription = null,
                modifier = Modifier.size(48.dp)
            )
            
            Spacer(modifier = Modifier.width(12.dp))
            
            Column(modifier = Modifier.weight(1f)) {
                Text(item.title)
                Text(item.subtitle, color = Color.Gray)
            }
        }
    }
}
```

---

## 性能检查清单

小 Com 总结了性能优化清单：

| 检查项 | 建议 |
|--------|------|
| 列表 key | 用唯一 ID 作为 key |
| remember | 用 remember 缓存对象 |
| lambda | 用 remember 缓存点击回调 |
| derivedStateOf | 减少重复计算 |
| 图片加载 | 用 Coil 异步加载 |
| UI 嵌套 | 减少不必要的嵌套 |
| 状态 | 用稳定的数据类型 |
| 日志 | 用 Layout Inspector 检查 |

---

## 本课小结

今天林小满学到了：

1. **重组原则**：理解 Compose 重组
2. **remember**：避免重复计算
3. **稳定数据**：用 @Stable
4. **key 参数**：优化列表
5. **derivedStateOf**：减少派生
6. **图片优化**：用 Coil
7. **减少嵌套**：优化层级
8. **LazyColumn**：正确使用列表

---

“性能优化太重要了！”林小满说。

“没错！”小 Com 说，“学会优化，你的 App 就能丝般顺滑！”

---

*”叮——“*

手机通知：**“第二十三章 已解锁：Compose 性能优化”**

---

**下集预告**：第二十四课 · 测试 · 单元测试与 UI 测试
