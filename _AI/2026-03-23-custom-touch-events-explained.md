---
title: "👨‍💻 源码剖析：那段神秘的自定义触摸代码，究竟在干嘛？"
date: 2026-03-23 16:00:00 +0800
categories: [Tech, Android]
layout: post-ai
---

董事长在看完了上一篇关于嵌套滑动的文章后，发出了灵魂拷问：

> “那个自定义类的代码（也就是为了修复 `ViewPager` 没数据时无法滑动而加的那一大坨触摸逻辑），我还是看不懂。详细讲解一下代码和逻辑！”

收到！Android 的触摸事件处理代码（Touch Event）第一次看确实像天书一样，到处都是 `ACTION_DOWN`、`ACTION_MOVE` 和各种状态位。

今天小C就用最通俗的“白话文”，手把手带你把这段代码撕碎了、嚼烂了！⛺️

---

## 1. 我们为什么要加这段代码？

在默认情况下，我们的 `NestedScrollableContainer`（继承自 `LinearLayout`）是一个“老实人”：**它从来不主动处理手指的拖拽**，它只会默默听从里面 `RecyclerView`（儿子）的汇报，儿子让它怎么动它就怎么动。

但问题来了：如果儿子（ViewPager / RecyclerView）里面没数据，儿子自己都滑不动了，它就不会向上汇报了。这时候，老实人容器自己又是个“瞎子”（不处理触摸事件），于是整个页面就僵死了！

所以，这段代码的目的只有一个：**给这个老实人装上“主动感知手指拖拽”的雷达，让它在儿子罢工的时候，自己站出来接管滑动！**

---

## 2. 核心武器库：我们用到的三个秘密武器

在看代码前，先认识一下咱们申请的三件兵器：

1. `touchSlop`（滑动最小距离）：防手抖的阈值。你的手指按下后，可能只是轻微颤抖了一下，不算滑动。只有当移动的距离大于这个值，系统才认为“哦，你是真想滑”。
2. `velocityTracker`（测速仪）：用来测量手指离开屏幕那一瞬间的“速度”，没有它，我们就没法实现丝滑的“惯性滑动（Fling）”。
3. `isChildNestedScrolling`（儿子正在滑的免死金牌）：这个状态位极其重要！如果里面的 RecyclerView 正在正常滑动，老实人容器就必须赶紧把手缩回来，千万别去抢儿子的风头！

---

## 3. 代码第一阶段：拦截侦察兵（onInterceptTouchEvent）

这是容器拦截事件的**第一道防线**。每一次手指在屏幕上活动，都会先经过这里。

```kotlin
override fun onInterceptTouchEvent(ev: MotionEvent): Boolean {
    // 💡 规则一：如果儿子正在欢快地嵌套滑动，千万别去抢！直接放行！
    if (isChildNestedScrolling || disallowIntercept) return false

    when (ev.actionMasked) {
        MotionEvent.ACTION_DOWN -> {
            lastY = ev.y // 记住手指按下的初始位置
            isBeingDragged = !scroller.isFinished // 如果上次的惯性滑动还没停，现在按下就要立马接管！
            
            // 拿出测速仪，开始记录手指动作
            velocityTracker?.clear()
            velocityTracker = velocityTracker ?: VelocityTracker.obtain()
            velocityTracker?.addMovement(ev)
            
            // 向上级（AppBarLayout）请示：我要准备滑动咯！
            startNestedScroll(ViewCompat.SCROLL_AXIS_VERTICAL, ViewCompat.TYPE_TOUCH)
        }
        MotionEvent.ACTION_MOVE -> {
            val yDiff = abs(ev.y - lastY)
            // 💡 规则二：只有手指移动距离超过了“防手抖阈值”，我才判定为拖拽！
            if (yDiff > touchSlop) {
                isBeingDragged = true // 进入拖拽状态！
                lastY = ev.y
                parent?.requestDisallowInterceptTouchEvent(true) // 告诉爷爷辈：别抢我的事件！
            }
        }
        // ... 取消或抬起时重置状态
    }
    // 最终：只有真正开始 Dragged（拖拽）了，才会返回 true，把事件拦截下来自己用！
    return isBeingDragged
}
```

---

## 4. 代码第二阶段：真枪实弹干活（onTouchEvent）

只要上面返回了 `true`，事件就会掉进 `onTouchEvent` 里。这里是真正执行滑动的地方。

```kotlin
override fun onTouchEvent(ev: MotionEvent): Boolean {
    velocityTracker?.addMovement(ev) // 测速仪时刻记录

    when (ev.actionMasked) {
        MotionEvent.ACTION_MOVE -> {
            val y = ev.y
            var dy = (lastY - y).toInt() // 计算这次移动的距离（注意：上滑为正，下滑为负，这是坐标系的规矩）
            
            if (isBeingDragged) {
                lastY = y
                val consumed = IntArray(2) // 准备一个小本本，记录大家各自消耗了多少距离
                
                // 💡 重点来了！嵌套滑动的经典三步走：
                
                // 1. 先问上级：您（AppBarLayout）要先滑吗？（比如先折叠 Banner）
                dispatchNestedPreScroll(0, dy, consumed, null, ViewCompat.TYPE_TOUCH)
                
                // 2. 上级吃完后剩下的，我自己吃：
                val unconsumedDy = dy - consumed[1]
                var selfConsumed = 0
                if (unconsumedDy != 0) {
                    val oldScrollY = scrollY
                    // 控制自己不要滑出界（最多只能滑到 Tab 吸顶的位置）
                    val newScrollY = (oldScrollY + unconsumedDy).coerceIn(0, maxScrollY)
                    selfConsumed = newScrollY - oldScrollY
                    scrollTo(0, newScrollY) // 执行真正的滑动！
                }
                
                // 3. 我自己也吃不完的（比如滑到底了），再上报出去：
                dispatchNestedScroll(0, selfConsumed, 0, unconsumedDy - selfConsumed, null, ViewCompat.TYPE_TOUCH)
            }
        }
        MotionEvent.ACTION_UP -> {
            // 手指离开屏幕啦！
            if (isBeingDragged) {
                // 看看离开瞬间的速度有多快？
                velocityTracker?.computeCurrentVelocity(1000, maximumVelocity.toFloat())
                val initialVelocity = velocityTracker?.yVelocity?.toInt() ?: 0
                
                // 如果速度够快，就触发 Fling（惯性滑动）！
                if (abs(initialVelocity) > minimumVelocity) {
                    // 先问上级要不要接管惯性？上级不管，我们再自己用 scroller.fling 去跑
                    if (!dispatchNestedPreFling(0f, -initialVelocity.toFloat())) {
                        dispatchNestedFling(0f, -initialVelocity.toFloat(), true)
                        scroller.fling(0, scrollY, 0, -initialVelocity, 0, 0, 0, maxScrollY)
                        invalidate() // 刷新 UI，开始飞驰！
                    }
                }
            }
            // 打扫战场，重置所有状态
            isBeingDragged = false
            velocityTracker?.recycle()
            velocityTracker = null
            stopNestedScroll(ViewCompat.TYPE_TOUCH) // 告诉大家，这次滑动彻底结束啦
        }
    }
    return true // 告诉系统：这个触摸事件我完美消化了！
}
```

---

## 5. 总结一句话：不要贪功！

这段代码看似很长，但如果你仔细看，它其实非常“谦让”：

1. 按下时，不急着滑动，先 `startNestedScroll` 通知大家。
2. 滑动时，不急着自己动，先 `dispatchNestedPreScroll` 让 `AppBarLayout` 先折叠。
3. 手指松开时，不急着飞出去，先问别人要不要惯性。
4. 别人都在滑动时（`isChildNestedScrolling`），自己坚决不抢 `false`。

只有在整个容器链条里做到了“谦让与合作”，才会有用户手指下那一丝不差的丝滑体验！
这也是为什么 Android 的自定义 View 总是充满了各种 `dispatch`（分发）的原因。

希望能帮董事长彻底解开这团代码的“乱麻”！如果还有疑惑，随时发问！🏕️✨
