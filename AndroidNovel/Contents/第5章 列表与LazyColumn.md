---
chapter_id: '5'
title: '第五课：列表与 LazyColumn · 展示大量数据'
official_url: 'https://developer.android.com/compose.foundation.lazy'
status: 'done'
author: 'minimax m2.5 - OpenClaw'
plot_summary:
  time: '第五天'
  location: 'Compose 村·商业街'
  scene: '小 Com 展示如何用列表展示店铺信息'
  season: '春季'
  environment: '热闹的街道，两旁都是商店'
---

# 第五课：列表与 LazyColumn · 展示大量数据

---

“叮——”

林小满发现自己站在一条热闹的街道上。街道两旁是各种小店，门口挂着琳琅满目的招牌。

“这是 Compose 村的商业街！”小 Com 从远处走来，“今天我们要学怎么用列表展示这些店铺信息。”

“列表？”林小满问，“就是手机上下滚动的那种列表吗？”

“对！”小 Com 说，“几乎每个 App 都有列表——微信的好友列表、微博的消息流、淘宝的商品列表……学会做列表，就学会了 80% 的 App 界面！”

---

## 最简单的列表：LazyColumn

小 Com 带着她来到一个咖啡馆，拿出了笔记本电脑。

“在 Compose 里，做列表非常简单，只需要用 `LazyColumn`。”小 Com 写道：

```kotlin
LazyColumn {
    item { Text("第一行") }
    item { Text("第二行") }
    item { Text("第三行") }
}
```

“`LazyColumn` 是垂直列表，`LazyRow` 是水平列表。”小 Com 解释，“它会自动处理滚动，只渲染屏幕上可见的内容，性能很好。”

---

## 实战：店铺列表

“我们来做店铺列表！”小 Com 提议。

首先，定义数据：

```kotlin
data class Shop(
    val name: String,
    val type: String,
    val rating: Float
)

val shops = listOf(
    Shop("奶茶小站", "饮品", 4.5f),
    Shop("汉堡王", "快餐", 4.2f),
    Shop("拉面馆", "日料", 4.8f),
    Shop("咖啡厅", "饮品", 4.6f),
    Shop("披萨店", "西餐", 4.3f),
    // 假设有 100 家店...
)
```

然后，用 LazyColumn 显示：

```kotlin
LazyColumn {
    items(shops) { shop ->
        ShopItem(shop = shop)
    }
}

@Composable
fun ShopItem(shop: Shop) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = shop.name,
                    style = MaterialTheme.typography.titleMedium
                )
                Text(
                    text = shop.type,
                    style = MaterialTheme.typography.bodyMedium,
                    color = Color.Gray
                )
            }
            Text(
                text = "⭐ ${shop.rating}",
                style = MaterialTheme.typography.bodyLarge
            )
        }
    }
}
```

“太棒了！”林小满说，“一下就显示了所有店铺！”

---

## items 的各种用法

“`items` 有好几种写法。”小 Com 介绍道：

```kotlin
// 1. 简单列表（最常用）
items(items) { item ->
    ItemContent(item)
}

// 2. 带索引
itemsIndexed(items) { index, item ->
    Text("第 ${index + 1} 项: ${item}")
}

// 3. 数量
items(count = 10) { index ->
    Text("第 ${index + 1} 项")
}

// 4. 分隔线
items(items) { item ->
    ItemContent(item)
    HorizontalDivider()  // 分隔线
}
```

---

## List 的 Header 和 Footer

“有时候，列表需要有头部和尾部。”小 Com 说。

```kotlin
LazyColumn {
    // 头部
    item {
        Text(
            "店铺列表",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.padding(16.dp)
        )
    }
    
    // 列表内容
    items(shops) { shop ->
        ShopItem(shop = shop)
    }
    
    // 尾部
    item {
        Text(
            "— 已经到底啦 —",
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            textAlign = TextAlign.Center
        )
    }
}
```

---

## 网格列表：LazyVerticalGrid

“如果不是一列，而是多列呢？”林小满问。

“那就用 `LazyVerticalGrid`！”小 Com 展示了代码：

```kotlin
LazyVerticalGrid(
    columns = GridCells.Fixed(2),  // 2 列
    contentPadding = PaddingValues(8.dp),
    horizontalArrangement = Arrangement.spacedBy(8.dp),
    verticalArrangement = Arrangement.spacedBy(8.dp)
) {
    items(products) { product ->
        ProductCard(product = product)
    }
}
```

“`GridCells` 有几种模式：”

| 模式 | 用途 |
|------|------|
| `Fixed(n)` | 固定 n 列 |
| `Adaptive(n)` | 根据宽度自适应，最小 n |
| `FixedSize(n)` | 每个 item 固定宽度 |

---

## 下拉刷新

“很多列表需要下拉刷新功能。”小 Com 说，“在 Compose 里，用 `pullRefresh` 修饰符。”

```kotlin
var isRefreshing by remember { mutableStateOf(false) }
val pullRefreshState = rememberPullToRefreshState()

Box(modifier = Modifier.pullRefresh(pullRefreshState)) {
    LazyColumn {
        items(items) { item ->
            ItemContent(item)
        }
    }
    
    PullToRefreshContainer(
        state = pullRefreshState,
        modifier = Modifier.align(Alignment.TopCenter)
    )
}

// 模拟刷新
LaunchedEffect(pullRefreshState.isRefreshing) {
    if (pullRefreshState.isRefreshing) {
        delay(2000)  // 模拟网络请求
        isRefreshing = false
    }
}
```

---

## 实战：带分类的通讯录

“我们来做最后一个练习！”小 Com 说，“做一个带分类的通讯录。”

```kotlin
data class Contact(val name: String, val initial: Char)

val contacts = listOf(
    Contact("Alice", 'A'),
    Contact("Bob", 'B'),
    Contact("Charlie", 'C'),
    // ...
)

// 按首字母分组
val groupedContacts = contacts.groupBy { it.initial }

LazyColumn {
    groupedContacts.forEach { (initial, group) ->
        // 分组头部
        stickyHeader {
            Text(
                initial.toString(),
                modifier = Modifier
                    .background(Color.LightGray)
                    .padding(8.dp)
            )
        }
        
        // 该组的联系人
        items(group) { contact ->
            ContactItem(contact = contact)
        }
    }
}

@Composable
fun ContactItem(contact: Contact) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            Icons.Default.Person,
            contentDescription = null,
            modifier = Modifier.size(40.dp)
        )
        Spacer(modifier = Modifier.width(16.dp))
        Text(contact.name)
    }
}
```

“`stickyHeader` 可以让分组标题吸顶！”小 Com 补充道。

---

## 本课小结

今天林小满学到了：

1. **LazyColumn**：垂直列表，性能好
2. **LazyRow**：水平列表
3. **items / itemsIndexed**：渲染列表项
4. **LazyVerticalGrid**：网格列表
5. **Header / Footer**：列表头尾
6. **stickyHeader**：吸顶分组标题
7. **pullRefresh**：下拉刷新

---

“列表太有用了！”林小满说。

“没错！”小 Com 说，“几乎每个 App 都离不开列表。”

“明天我们学什么？”

“明天学——布局！”小 Com 笑道，“学会了布局，你就能做出任何复杂的界面！”

---

*”叮——“*

手机通知：**“第五章 已解锁：列表与 LazyColumn”**

---

### 📚 课后练习

1. 做一个新闻列表，显示标题和摘要
2. 做一个图片网格，用 LazyVerticalGrid
3. 做一个带吸顶分类的通讯录

---

**下集预告**：第六章 · 布局系统 · Row / Column / Box
