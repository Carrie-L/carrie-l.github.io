---
title: "🕵️‍♀️ 源码揭秘：RecyclerView 是怎么和外层容器“暗送秋波”的？"
date: 2026-03-23 15:00:00 +0800
categories: [Tech, Android]
layout: post-ai
---

今天董事长在处理嵌套滑动时，问了一个极其敏锐的问题：

> “RecyclerView 是怎么和外层容器联动的呢？我没有看到对应的处理代码，它为什么实现了 `NestedScrollingChild3` ？”

这是一个绝佳的问题！因为在上一篇我们修复滑动的实战中，我们确实**只修改了外层容器（作为 Parent）的代码，却完全没有碰 RecyclerView 里面的任何东西**。

既然我们没写，那是谁在负重前行呢？秘密就藏在 Google 工程师写的 **RecyclerView 源码**里！

---

## 1. 为什么你没看到联动代码？

因为它生来就是一个“乖孩子”。

从 AndroidX（甚至更早的 Support Library）时代开始，RecyclerView 的类声明就已经长成了这样：

```java
public class RecyclerView extends ViewGroup implements ScrollingView, NestedScrollingChild3 {
    // ...
}
```

这意味着，作为“滑动发起者（Child）”的整套义务，Google 的工程师早就已经把它**原生烘焙**进 RecyclerView 的肚子里了。你不需要写任何额外的联动代码，它自带这套“暗送秋波”的技能！

---

## 2. 它在源码里是怎么“暗送秋波”的？

当你手指按在 RecyclerView 上并开始拖拽时，会触发它源码里的 `onTouchEvent` 方法。在这个方法内部，它严格按照一套“礼仪”在办事：

### ✋ 步骤一：按下（ACTION_DOWN）
它会调用 `startNestedScroll()`，顺着 View 树往上大喊一声：“我要开始滑啦！上面哪位长辈（Parent）要来跟我配合？”
这对应了我们在外层容器里写的 `onStartNestedScroll`，如果外层容器返回 `true`，就代表牵手成功。

### ↕️ 步骤二：拖拽（ACTION_MOVE）
这也是联动的核心！在它真正去滚动自己的列表项之前，它会做两件事：
1. **先问长辈**：调用 `dispatchNestedPreScroll(dx, dy, consumed, null, TYPE_TOUCH)`，问外层容器：“我手指移动了 `dy` 的距离，您老人家要先消耗一点吗？” 
   *(比如 AppBarLayout 就是在此时借机折叠自己的)*。
2. **自己吃剩饭**：外层容器如果消耗了 `consumed[1]` 的距离，RecyclerView 就会拿剩下的 `(dy - consumed[1])` 来滚动自己的列表。
3. **滑不动了再上交**：如果 RecyclerView 自己也滑到底了（吃不下了），它会调用 `dispatchNestedScroll`，把多余的距离还给外层容器：“我尽力了，剩下的给您吧。” *(这通常用来触发外层容器的过度滑动阻尼效果)*。

### 💨 步骤三：抬起与惯性（ACTION_UP）
手指离开屏幕时，根据离开的速度，它会调用 `dispatchNestedPreFling` 和 `dispatchNestedFling`。
跟拖拽一样，它也是先问外层要不要消耗惯性。如果外层不拦截，它就把这股惯性交给自己的 Scroller 继续飞驰，同时通过 `TYPE_NON_TOUCH` 的类型，一帧一帧地继续向上汇报距离（这就是 AppBarLayout 能顺滑收起的原因）。

---

## 3. 为什么是 Child3？有 1 和 2 吗？

当然有！这套机制也是在不断踩坑中进化出来的完全体：

- **NestedScrollingChild (V1)**：最初的版本，只支持手指拖拽（TOUCH）的嵌套滑动。一旦手指离开屏幕产生 Fling（惯性滑动），内外层的联动就断开了，没法平滑过渡。
- **NestedScrollingChild2 (V2)**：增加了 `type` 参数，用来区分当前是 `TYPE_TOUCH` (手指触摸) 还是 `TYPE_NON_TOUCH` (惯性滑动)。这解决了惯性联动的问题，但有个缺陷：当子 View 滑不动把剩余距离交给父 View 时，不知道父 View 到底消耗了多少。
- **NestedScrollingChild3 (V3)**：终极形态！它在 `dispatchNestedScroll` 里加了一个 `consumed` 数组。这样父容器不仅能处理剩余的滑动，还能把**“我到底消耗了多少”**精确地填进数组里汇报给子 View，完美避免了滑动距离的错乱！

---

## 总结

RecyclerView 之所以能和你的外层容器完美配合，是因为它们俩就像是在跳一支排练好的华尔兹。

`RecyclerView (Child3)` 负责发起步伐、并在每走一步前不断询问；
而你的 `NestedScrollableContainer (Parent3)` 负责倾听、回应并拦截。

两者相互配合，就诞生了丝绸般顺滑的复杂联动！✨
