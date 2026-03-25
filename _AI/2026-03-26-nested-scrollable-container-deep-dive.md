---
title: "深入解析：自定义嵌套滑动容器 NestedScrollableContainer"
date: 2026-03-26 23:50:00 +0800
categories: [AI]
layout: post-ai
---

> 今天来解析一个 production-ready 的自定义嵌套滑动容器，它完美替代了 AppBarLayout + CollapsingToolbarLayout 的组合，同时支持更复杂的滚动协调逻辑。

## 一、组件定位与设计目标

`NestedScrollableContainer` 是一个**三区域协调滑动容器**，核心使命是解决以下滚动场景：

```
┌─────────────────────┐
│   🎴 Banner 区域     │  ← 可折叠，控制 MotionLayout 进度
│   (MotionLayout)    │
├─────────────────────┤
│  📦 资源卡片区域      │  ← 可滚动移出屏幕
│                     │
├─────────────────────┤
│  📰 Feed 列表        │  ← 内部有 RecyclerView
│  (ViewPager2)       │     继续嵌套滚动
└─────────────────────┘
```

**滚动顺序设计**：
- **向上滚动**：Banner 折叠 → 卡片滚出 → Feed 开始滚动
- **向下滚动**：Feed 回滚 → 卡片滚回 → Banner 展开

---

## 二、核心架构设计

### 2.1 类的继承关系

```kotlin
class NestedScrollableContainer : LinearLayout, NestedScrollingParent3
```

选择 `LinearLayout` 作为基类是因为：
1. 内部布局天然是垂直线性排列（Banner → 卡片 → Feed）
2. 轻量级，没有 FrameLayout/ConstraintLayout 的额外开销
3. 便于子 View 按顺序排列

实现 `NestedScrollingParent3` 是为了：
- 接收子 View（Feed 的 RecyclerView）的嵌套滚动事件
- 支持 AndroidX 最新的嵌套滑动协议（区分 Touch/Touchless 类型）

### 2.2 核心状态管理

```kotlin
// ====== Banner 状态 ======
var bannerScrollRange: Int = 0     // Banner 可折叠的总距离
var bannerOffset: Int = 0          // 当前折叠偏移量（0 = 展开）

// ====== 容器自身滚动状态 ======
private val maxScrollY: Int        // 卡片区域可滚动的最大距离

// ====== Feed RV 注册表 ======
private val feedRecyclerViews = SparseArray<RecyclerView>()
```

**关键设计**：使用 `SparseArray` 缓存 ViewPager2 每个页面的 RecyclerView，避免每次都 findViewById。

---

## 三、Banner 区域控制机制

### 3.1 Banner 折叠的核心逻辑

```kotlin
private fun updateBannerOffset(newOffset: Int) {
    val clamped = newOffset.coerceIn(0, bannerScrollRange)
    if (clamped != bannerOffset) {
        bannerOffset = clamped
        if (bannerScrollRange > 0) {
            // 通知外部 MotionLayout 更新进度
            onProgressChanged?.invoke(bannerOffset.toFloat() / bannerScrollRange)
        }
    }
}
```

这里用**回调模式**而非直接操作 MotionLayout，做到了**依赖倒置**：
- 容器只负责计算进度（0~1）
- Fragment 拿到进度后，自行决定如何驱动 MotionLayout
- 容器保持纯净，不关心具体 UI 实现

### 3.2 一键回到顶部

```kotlin
fun scrollToTop() {
    updateBannerOffset(bannerScrollRange)  // 折叠 Banner
    scrollTo(0, maxScrollY)                // 滚走卡片
}
```

这个 API 常用于点击 Toolbar 的返回顶部按钮。

---

## 四、触摸事件处理（直接触摸卡片区域）

### 4.1 为什么需要两套触摸处理？

Android 的嵌套滑动机制中：
- **onInterceptTouchEvent / onTouchEvent**：处理**直接触摸**容器本身
- **NestedScrollingParent 回调**：处理**子 View 传递上来**的滚动事件

由于卡片区域是容器的一部分（不是独立可滚动的 View），所以必须通过 `onTouchEvent` 自己消费滚动。

### 4.2 触摸拦截逻辑

```kotlin
override fun onInterceptTouchEvent(ev: MotionEvent): Boolean {
    when (ev.actionMasked) {
        ACTION_DOWN -> {
            directTouchActive = isTouchInResourceArea(ev.y)
            // ... 初始化状态
        }
        ACTION_MOVE -> {
            // 只有在卡片区域且滑动距离超过 touchSlop 才拦截
            if (directTouchActive && !isDragging) {
                if (abs(ev.y - initialTouchY) > touchSlop) {
                    isDragging = true
                    parent?.requestDisallowInterceptTouchEvent(true)
                    return true  // 拦截！自己处理
                }
            }
        }
    }
    return false
}
```

**关键点**：
- `isTouchInResourceArea()` 判断触摸点是否在 TabLayout 上方（即卡片区域）
- 超过 `touchSlop`（默认 8dp）才判定为拖动，避免误触
- 拦截后调用 `requestDisallowInterceptTouchEvent(true)`，防止父 View 抢事件

### 4.3 直接触摸的滚动消费

```kotlin
private fun consumeDirectTouchScroll(dy: Int) {
    var remaining = dy
    
    if (remaining > 0) {
        // 向上滚动：先折叠 Banner
        if (bannerOffset < bannerScrollRange) {
            val bannerConsume = min(remaining, bannerScrollRange - bannerOffset)
            updateBannerOffset(bannerOffset + bannerConsume)
            remaining -= bannerConsume
        }
        // 再滚动卡片
        if (remaining > 0 && scrollY < maxScrollY) {
            val selfConsume = min(remaining, maxScrollY - scrollY)
            scrollBy(0, selfConsume)
            remaining -= selfConsume
        }
        // 注意：直接触摸不传递剩余滚动给 Feed
    }
}
```

这里体现了**分阶段消费**的思想：用一个 `remaining` 变量追踪剩余滚动距离，每个区域按需消费。

---

## 五、嵌套滑动处理（接收 Feed 的滚动事件）

### 5.1 onNestedPreScroll：提前消费

这是 NestedScrollingParent3 的核心回调，Feed 的 RecyclerView 在滚动前会先询问父容器：

```kotlin
override fun onNestedPreScroll(target: View, dx: Int, dy: Int, consumed: IntArray, type: Int) {
    var remaining = dy
    var totalConsumed = 0
    
    if (remaining > 0) {
        // 向上滚动：Banner 折叠 → 卡片滚出 → 剩余给 Feed
        if (bannerOffset < bannerScrollRange) {
            val bannerConsume = min(remaining, bannerScrollRange - bannerOffset)
            updateBannerOffset(bannerOffset + bannerConsume)
            totalConsumed += bannerConsume
            remaining -= bannerConsume
        }
        if (remaining > 0 && scrollY < maxScrollY) {
            val selfConsume = min(remaining, maxScrollY - scrollY)
            scrollBy(0, selfConsume)
            totalConsumed += selfConsume
            remaining -= selfConsume
        }
    } else if (remaining < 0) {
        // 向下滚动：只有 Feed 到顶后才处理
        if (!target.canScrollVertically(-1)) {
            // 卡片滚回 → Banner 展开
            if (scrollY > 0) {
                val selfConsume = max(remaining, -scrollY)
                scrollBy(0, selfConsume)
                totalConsumed += selfConsume
                remaining -= selfConsume
            }
            if (remaining < 0 && bannerOffset > 0) {
                val bannerConsume = max(remaining, -bannerOffset)
                updateBannerOffset(bannerOffset + bannerConsume)
                totalConsumed += bannerConsume
                remaining -= bannerConsume
            }
        }
    }
    consumed[1] = totalConsumed  // 报告消费了多少
}
```

**向下滚动的特殊判断**：
```kotlin
!target.canScrollVertically(-1)  // Feed 是否还能继续向下滚？
```
- `true`：Feed 已经到顶，父容器开始消费
- `false`：Feed 还有内容，父容器不拦截

### 5.2 为什么向上不判断 Feed 位置？

因为向上滚动时，我们**希望优先折叠 Banner 和滚走卡片**，让用户先看到更多 Feed 内容。这是典型的 "sticky header" 行为。

---

## 六、Fling 处理与惯性滚动

### 6.1 什么是 Fling？

用户快速滑动后抬手，系统会计算一个初速度，触发惯性滚动（fling）。Android 使用 `OverScroller` 计算 fling 动画。

### 6.2 统一的 Combined 坐标系

为了协调多个区域的 fling，代码设计了一个**虚拟组合坐标系**：

```kotlin
private val combinedOffset: Int get() = bannerOffset + scrollY
private val combinedMax: Int get() = bannerScrollRange + maxScrollY
```

想象把 Banner 和卡片区域「粘」在一起，形成一个可滚动的长区域：

```
0 ────────────────────────────────── combinedMax
│ Banner 区域 │   卡片区域   │ Feed 区域 │
│  可折叠     │   可滚走     │  子 RV    │
└─────────────┴─────────────┴───────────┘
```

### 6.3 Fling 启动

```kotlin
override fun onNestedPreFling(target: View, velocityX: Float, velocityY: Float): Boolean {
    // 向上 fling：如果 Banner 或卡片还能收缩，自己消费
    if (velocityY > 0 && (bannerOffset < bannerScrollRange || scrollY < maxScrollY)) {
        selfFling(velocityY.toInt())
        return true  // 拦截，不让 Feed fling
    }
    
    // 向下 fling：如果 Feed 到顶且卡片/Banner 能展开，自己消费
    if (velocityY < 0 && !target.canScrollVertically(-1) && (scrollY > 0 || bannerOffset > 0)) {
        selfFling(velocityY.toInt())
        return true
    }
    return false  // 不拦截，交给 Feed
}
```

### 6.4 Fling 动画执行

```kotlin
override fun computeScroll() {
    if (!scroller.computeScrollOffset()) {
        if (isSelfFlinging) {
            isSelfFlinging = false
        }
        return
    }
    
    val targetCombined = scroller.currY      // Scroller 计算的目标位置
    val currentCombined = combinedOffset      // 当前实际位置
    val dy = targetCombined - currentCombined // 本次需要移动的距离
    
    if (dy > 0) {
        // 向上 fling：Banner → 卡片 → 剩余传给 Feed
        var remaining = dy
        
        if (bannerOffset < bannerScrollRange) {
            val bannerConsume = min(remaining, bannerScrollRange - bannerOffset)
            updateBannerOffset(bannerOffset + bannerConsume)
            remaining -= bannerConsume
        }
        
        if (remaining > 0 && scrollY < maxScrollY) {
            val selfConsume = min(remaining, maxScrollY - scrollY)
            scrollBy(0, selfConsume)
            remaining -= selfConsume
        }
        
        if (remaining > 0) {
            // 还有剩余速度！传给 Feed RV 继续 fling
            getCurrentFeedRecyclerView()?.fling(0, scroller.currVelocity.toInt())
            abortFling()
            return
        }
    }
    
    invalidate()  // 请求重绘，下次继续 computeScroll
}
```

**这里有一个非常巧妙的设计**：当 Scroller 计算的速度足够大，大到能滚完 Banner 和卡片还有剩余时，代码会主动把剩余速度传递给 Feed 的 RecyclerView！

```kotlin
getCurrentFeedRecyclerView()?.fling(0, scroller.currVelocity.toInt())
```

这保证了用户体验的连续性——用户感觉自己在「甩」一个连贯的长列表，而不是三个割裂的区域。

---

## 七、性能优化细节

### 7.1 VelocityTracker 的复用

```kotlin
private fun initVelocityTracker() {
    if (velocityTracker == null) velocityTracker = VelocityTracker.obtain()
}

private fun recycleVelocityTracker() {
    velocityTracker?.recycle()
    velocityTracker = null
}
```

`VelocityTracker.obtain()` 是从对象池获取，用完必须 `recycle()` 归还，避免频繁创建。

### 7.2 scrollTo 的边界保护

```kotlin
override fun scrollTo(x: Int, y: Int) {
    val clampedY = y.coerceIn(0, maxScrollY.coerceAtLeast(0))
    super.scrollTo(x, clampedY)
}
```

重写 `scrollTo` 强制边界检查，防止外部调用传入非法值导致过度滚动。

### 7.3 SparseArray 代替 HashMap

```kotlin
private val feedRecyclerViews = SparseArray<RecyclerView>()
```

`SparseArray` 在 key 为 Integer 时比 `HashMap<Integer, V>` 更省内存（避免自动装箱）。

---

## 八、使用示例

```kotlin
// 1. XML 布局
<com.carrie.demoupdatetheme.ui.widget.NestedScrollableContainer
    android:id="@+id/nestedContainer"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical">
    
    <!-- Banner 区域：MotionLayout -->
    <androidx.constraintlayout.motion.widget.MotionLayout
        android:id="@+id/motionLayout"
        android:layout_width="match_parent"
        android:layout_height="200dp"
        app:layoutDescription="@xml/scene_banner" />
    
    <!-- 资源卡片区域 -->
    <androidx.recyclerview.widget.RecyclerView
        android:id="@+id/resourceCardsRv"
        android:layout_width="match_parent"
        android:layout_height="wrap_content" />
    
    <!-- TabLayout -->
    <com.google.android.material.tabs.TabLayout
        android:id="@+id/tabLayout"
        android:layout_width="match_parent"
        android:layout_height="48dp" />
    
    <!-- Feed 区域：ViewPager2 -->
    <androidx.viewpager2.widget.ViewPager2
        android:id="@+id/viewPager"
        android:layout_width="match_parent"
        android:layout_height="match_parent" />
        
</com.carrie.demoupdatetheme.ui.widget.NestedScrollableContainer>

// 2. Fragment 中初始化
class HomeFragment : Fragment() {
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        val container = view.findViewById<NestedScrollableContainer>(R.id.nestedContainer)
        val motionLayout = view.findViewById<MotionLayout>(R.id.motionLayout)
        
        // 设置 Banner 可折叠范围
        container.bannerScrollRange = motionLayout.height - toolbarHeight
        
        // 监听进度变化，驱动 MotionLayout
        container.onProgressChanged = { progress ->
            motionLayout.progress = progress
        }
        
        // 注册 Feed 的 RecyclerView
        viewPager.registerOnPageChangeCallback(object : ViewPager2.OnPageChangeCallback() {
            override fun onPageSelected(position: Int) {
                val feedRv = viewPager.getChildAt(0) as? RecyclerView
                feedRv?.let { container.registerFeedRecyclerView(position, it) }
            }
        })
    }
}
```

---

## 九、总结

这个组件的设计亮点：

1. **协议分离**：直接触摸走 `onTouchEvent`，嵌套滑动走 `NestedScrollingParent3`，职责清晰
2. **统一坐标系**：用 `combinedOffset` 把多个区域抽象成一个虚拟长列表，简化 fling 处理
3. **速度传递**：Scroller 速度过剩时主动传递给子 RV，保证滚动连贯性
4. **依赖倒置**：通过回调暴露进度，不直接依赖 MotionLayout，可复用性更强
5. **边界严谨**：多处 `coerceIn` 和 `scrollTo` 重写，防止越界崩溃

这是一个**工程化程度很高**的自定义 View，值得收藏参考！

---

💡 **一句话总结**：通过 NestedScrollingParent3 + 虚拟 Combined 坐标系 + OverScroller，实现了三区域丝滑协调滚动，完美替代 AppBarLayout 的复杂嵌套结构。
