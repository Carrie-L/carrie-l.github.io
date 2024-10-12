---
layout: article
title: ScrollView 嵌套ListView会显示不全
date: 2024-10-13
tags: ['MeasureSpec', '源码分析', '自定义View']


---
    
    

因为ScrollView 传递给ListView时，用的是 `UNSPECIFIED` , ListView 设置了 heightSize
```java
if (heightMode == MeasureSpec.UNSPECIFIED) {  
        heightSize = mListPadding.top + mListPadding.bottom + childHeight +  
                getVerticalFadingEdgeLength() * 2;  
    }  
```

**解决：**
自定义ListView，在onMeasure()方法里重写 `heightMeasureSpec` ，让它进入到下面这个方法中：
```java
if (heightMode == MeasureSpec.AT_MOST) {  
        heightSize = measureHeightOfChildren(widthMeasureSpec, 0, NO_POSITION, heightSize, -1);  
}  
```

![](../assets/blogimages/../assets/blogimages/Pasted image 20241013034607.png)

 ListView 源码分析

```java
@Override  
protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {  
    // Sets up mListPadding  
    super.onMeasure(widthMeasureSpec, heightMeasureSpec);  
  
    final int widthMode = MeasureSpec.getMode(widthMeasureSpec);  
    final int heightMode = MeasureSpec.getMode(heightMeasureSpec);  
    int widthSize = MeasureSpec.getSize(widthMeasureSpec);  
    int heightSize = MeasureSpec.getSize(heightMeasureSpec);  
  
    int childWidth = 0;  
    int childHeight = 0;  
    int childState = 0;  
    
	  mItemCount = mAdapter == null ? 0 : mAdapter.getCount();  
	if (mItemCount > 0 && (widthMode == MeasureSpec.UNSPECIFIED  
        || heightMode == MeasureSpec.UNSPECIFIED)) {  
    final View child = obtainView(0, mIsScrap);  
  
    // Lay out child directly against the parent measure spec so that  
    // we can obtain exected minimum width and height.    measureScrapChild(child, 0, widthMeasureSpec, heightSize);  
  
    childWidth = child.getMeasuredWidth();  
    childHeight = child.getMeasuredHeight();  
    childState = combineMeasuredStates(childState, child.getMeasuredState());  
  
    if (recycleOnMeasure() && mRecycler.shouldRecycleViewType(  
            ((LayoutParams) child.getLayoutParams()).viewType)) {  
        mRecycler.addScrapView(child, 0);  
    }  
}
  
    if (heightMode == MeasureSpec.UNSPECIFIED) {  
        heightSize = mListPadding.top + mListPadding.bottom + childHeight +  
                getVerticalFadingEdgeLength() * 2;  
    }  
  
    if (heightMode == MeasureSpec.AT_MOST) {  
        // TODO: after first layout we should maybe start at the first visible position, not 0  
        heightSize = measureHeightOfChildren(widthMeasureSpec, 0, NO_POSITION, heightSize, -1);  
    }  
  
    setMeasuredDimension(widthSize, heightSize);  
  
    mWidthMeasureSpec = widthMeasureSpec;  
}



```

 UNSPECIFIED 模式下，heightSize 计算

 1. ListView 默认高度模式 UNSPECIFIED

重写 `ListView` ，在 `onMeasure()` 里获取高度模式：
```kotlin
override fun onMeasure(widthMeasureSpec: Int, heightMeasureSpec: Int) {    
    val heightMode = MeasureSpec.getMode(heightMeasureSpec)  // 0 UNSPECIFIED  
}
```
得到0，可知 `ScrollView` 传递给 `ListView` 的高度模式为 `UNSPECIFIED` 。

因此它会执行 `ListView.java` 中的这段代码：
```kotlin
if (heightMode == MeasureSpec.UNSPECIFIED) {  
        heightSize = mListPadding.top + mListPadding.bottom + childHeight +  
                getVerticalFadingEdgeLength() * 2;  
    }  
```
当 `MeasureSpec` 的模式为 `UNSPECIFIED` 时，这段代码的主要作用是给 `ListView` 提供一个合理的高度。

 2. childHeight 为第一个Item的高度

在这个代码段中，`childHeight` 代表了 `ListView` 子项的高度。

通常情况下，当 `ListView` 开始测量时，它会测量**第一个子项的高度**，并将其作为 `childHeight`。

这个测量过程会调用 `ListAdapter` 的 `getView()` 方法来获取子项的 `View`，然后测量这个子项的高度。
```java
View child = adapter.getView(0, null, this);  // 获取第一个子项
child.measure(0, 0);  // 测量子项的宽高
int childHeight = child.getMeasuredHeight();  // 获取测量后的高度
```

- 如果 `ListView` 有子项（即有内容），`childHeight` 是**第一个可见子项的高度**。
- 如果 `ListView` 没有子项（即内容为空），则 `childHeight` 通常是 `0`，因为没有任何内容可供测量。

 3. heightSize

- `heightSize` 被设定为 `ListView` 的上下内边距 (`mListPadding.top` 和 `mListPadding.bottom`) 加上 `childHeight`（第一个子项的高度），再加上视图淡出长度的两倍（即 `getVerticalFadingEdgeLength()` * 2）。

- **`getVerticalFadingEdgeLength()`**：这是 `ListView` 的垂直淡出边缘长度，即列表项在滚动边缘时淡出的区域长度。乘以 `2` 是因为考虑了上下两个边缘的淡出区域。


 重写onMeasure

通过上面的步骤，我们知道了想要让ListView显示完全，就要修改高度模式为 AT_MOST，因此重写onMeasure()，并设置

```java
override fun onMeasure(widthMeasureSpec: Int, heightMeasureSpec: Int) {
	val heightMeasureSpec = MeasureSpec.makeMeasureSpec(Int.MAX_VALUE shr 2 , MeasureSpec.AT_MOST)
	super.onMeasure(widthMeasureSpec, heightMeasureSpec)
}
```

 1. 为什么 makeMeasureSpec ？

`makeMeasureSpec()` 是  `View` 系统中用于创建 `MeasureSpec` 的方法，它将大小 (`size`) 和模式 (`mode`) 组合成一个 32 位的 `MeasureSpec` 整数。

`MeasureSpec` 用于传递视图的测量需求，决定视图应该占用多大的空间。

`makeMeasureSpec()` 的作用是将测量**模式和尺寸**合并在一起，用于传递给 `View` 进行测量（`onMeasure()` 方法）。

```java
public static int makeMeasureSpec(@IntRange(from = 0, to = (1 << MeasureSpec.MODE_SHIFT) - 1) int size,  
                                  @MeasureSpecMode int mode) {  
    if (sUseBrokenMakeMeasureSpec) {  
        return size + mode;  
    } else {  
        return (size & ~MODE_MASK) | (mode & MODE_MASK);  
    }  
}
```

在这个方法中，参数size 指定了范围，表示 `size` 的有效范围是 0 到 `(1 << 30) - 1`，即 0 到 `1073741823`
```yaml
1 的二进制为：0000  0000  0000  0000  0000  0000  0000  0001
左移30位为：   0100  0000  0000  0000  0000  0000  0000  0000
结果： 1 * 2^30 = 1073741824
-1： 1073741823
```

`(size & ~MODE_MASK) | (mode & MODE_MASK)`：
	将 `size` 的低 30 位与 `mode` 的高 2 位合并在一起，构成完整的 `MeasureSpec` 值。

 2. 为什么是 Int.MAX_VALUE shr 2 ？

`shr` 是 `右移` 运算符，相当于 `>>` 。

`Int.MAX_VALUE shr 2` 表示将 `Int.MAX_VALUE` 右移两位，即将其**除以 4**，得到一个较小的数。右移两位的结果为 `536870911`，即 `2147483647 / 4`。

`Int.MAX_VALUE` 
```yaml
0111 1111 1111 1111 1111 1111 1111 1111 
最高位为0，表示正数。
=  2^31 -1    (相当于 1000  0000  0000  0000  0000  0000  0000  0000  - 1)
= 2147483647
``` 
显然超出了 `size` 的最大范围 `1073741823`，因此要将其值缩小。

通过传递一个非常大的值（如 `Int.MAX_VALUE shr 2`），实际上是告诉 `ListView` 你可以使用最多 `536870911`的高度。这足够大，可以让 `ListView` 计算所有子项的高度并显示出来。

那么缩小到什么值合适呢？

在 `onMeasure()` 里有这样一段代码：
```java
if (heightMode == MeasureSpec.AT_MOST) {  
    // TODO: after first layout we should maybe start at the first visible position, not 0  
    heightSize = measureHeightOfChildren(widthMeasureSpec, 0, NO_POSITION, heightSize, -1);  
}
```
通过设定模式为 `AT_MOST` 后，会调用 `measureHeightOfChildren()` 测量 `ListView` 的子项高度，从而决定整个 `ListView` 的高度。

```java
final int measureHeightOfChildren(int widthMeasureSpec, int startPosition, int endPosition,  
        int maxHeight, int disallowPartialChildPosition) {  
    // ......省略其它代码
    int returnedHeight = mListPadding.top + mListPadding.bottom;  
    
    for (i = startPosition; i <= endPosition; ++i) {  
        child = obtainView(i, isScrap);  
        measureScrapChild(child, i, widthMeasureSpec, maxHeight);  
        if (i > 0) {  
            // Count the divider for all but one child  
            returnedHeight += dividerHeight;  
        }  
  
        returnedHeight += child.getMeasuredHeight();  
  
        if (returnedHeight >= maxHeight) {  
            // We went over, figure out which height to return.  If returnedHeight > maxHeight,  
            // then the i'th position did not fit completely.            return (disallowPartialChildPosition >= 0) // Disallowing is enabled (> -1)  
                        && (i > disallowPartialChildPosition) // We've past the min pos  
                        && (prevHeightWithoutPartialChild > 0) // We have a prev height  
                        && (returnedHeight != maxHeight) // i'th child did not fit completely  
                    ? prevHeightWithoutPartialChild  
                    : maxHeight;  
        }  
        if ((disallowPartialChildPosition >= 0) && (i >= disallowPartialChildPosition)) {  
            prevHeightWithoutPartialChild = returnedHeight;  
        }  
    }    
    // At this point, we went through the range of children, and they each  
    // completely fit, so return the returnedHeight   
    return returnedHeight;
}

```

`measureHeightOfChildren()` 在测量每个子项时会**不断累加其高度**，并与 `maxHeight`（即 `Int.MAX_VALUE shr 2`）进行比较。
当累加的高度超过 `maxHeight` 时，测量过程会停止。

由于 `536870911` 是一个非常大的值，通常情况下 `ListView` 的总高度不会超过这个值，所以传递这个值实际上意味着**允许 `ListView` 测量所有子项的高度而不受限制**。

 3. 为什么不使用 0 或较小的值？

如果传递 `0` 或较小的值作为 `maxHeight`，意味着 `ListView` 在测量子项时一旦累加高度达到这个值，便会停止测量，这样 `ListView` 只会显示有限的子项。

例如：
- **传递 `0`**：`ListView` 会认为没有任何高度可用，因此可能完全不显示子项。
- **传递较小值**：如 `100` 或 `200`，`ListView` 会在测量到超过 `100` 或 `200` 的高度时停止，无法显示所有的子项。

因此，为了确保 `ListView` 可以显示所有子项，使用一个足够大的 `maxHeight` 是必不可少的。

  4. Int.MAX_VALUE shr 2 的作用

1. **给 `ListView` 足够大的高度限制**：
	通过使用 `Int.MAX_VALUE shr 2`，给 `ListView` 提供了一个非常大的 `maxHeight`，确保它能够自由测量所有子项的高度而不被过早限制。
    
2. **防止溢出或异常**：
	通过将 `Int.MAX_VALUE` 右移两位，得到 `536870911`，避免了直接使用最大值可能带来的溢出或其他系统异常，同时这个值仍然足够大，可以满足实际测量需求。
    
3. **确保子项完全显示**：
	这段代码有效地确保了 `ListView` 在 `ScrollView` 或 `NestedScrollView` 中时，能够测量出所有子项的高度并显示出来，而不会被默认的高度限制。

