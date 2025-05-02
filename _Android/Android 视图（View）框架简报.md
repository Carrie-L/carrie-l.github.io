---
layout: article
title: "Android 视图（View）框架简报"
date: 2025-03-06
tags: [ "Android","View"]
permalink: /android/android-shi-tu-view-kuang-jia-jian-bao/
---

**简介：**

本文档旨在概述 Android 视图（View）框架的关键组件和概念，包括 View、ViewGroup、ViewManager、ViewRootImpl 和 ViewTreeObserver。该框架负责在 Android 应用程序中呈现用户界面，处理布局、绘制、输入事件和窗口管理等方面。通过分析提供的源代码片段，我们可以深入了解这些组件之间的关系以及它们在构建用户界面中的作用。

**一、View 类**

- **核心概念：** View 类是 Android 用户界面元素的基础构建块。它代表屏幕上的一个矩形区域，负责绘制自身和处理用户交互。
- **Padding（内边距）和 Margin（外边距）：**
- View 可以定义内边距，通过getPaddingLeft(), getPaddingTop(), getPaddingRight(), getPaddingBottom(), getPaddingStart(), getPaddingEnd()方法获取。
- View 本身不支持外边距，外边距由 ViewGroup 及其 MarginLayoutParams 提供支持。
- 源代码示例：
- * method and queried by calling {@link  {@link 
- * {@link  {@link  {@link 
- * {@link 
- *
- * Even though a view can define a padding, it does not provide any support for
- * margins. However, view groups provide such a support. Refer to
- * {@link android.view.ViewGroup} and
- * {@link android.view.ViewGroup.MarginLayoutParams} for further information.
- **Layout（布局）：** 布局过程分为两个阶段：测量（measure）和布局（layout）。
- **属性处理：** View 的属性可以通过 XML 属性设置，并读取。例如，背景、内边距、滚动位置、标签、焦点等等。
- case com.android.internal.R.styleable.View_background:
- background = a.getDrawable(attr);
- break;
- case com.android.internal.R.styleable.View_padding:
- padding = a.getDimensionPixelSize(attr, -1);
- mUserPaddingLeftInitial = padding;
- mUserPaddingRightInitial = padding;
- leftPaddingDefined = true;
- rightPaddingDefined = true;
- break;
- **状态标志：** View 使用多个标志来跟踪其状态，包括可见性（VISIBILITY_MASK），焦点（PFLAG_FOCUSED），选择状态（PFLAG_SELECTED），按下状态（PFLAG_PRESSED），激活状态（PFLAG_ACTIVATED），脏标记（PFLAG_DIRTY_MASK）等等。
- out.append((mViewFlags&SCROLLBARS_VERTICAL) != 0 ? 'V' : '.');
- out.append((mViewFlags&CLICKABLE) != 0 ? 'C' : '.');
- out.append((mViewFlags&LONG_CLICKABLE) != 0 ? 'L' : '.');
- out.append((mViewFlags&CONTEXT_CLICKABLE) != 0 ? 'X' : '.');
- out.append(' ');
- out.append((mPrivateFlags&PFLAG_IS_ROOT_NAMESPACE) != 0 ? 'R' : '.');
- out.append((mPrivateFlags&PFLAG_FOCUSED) != 0 ? 'F' : '.');
- out.append((mPrivateFlags&PFLAG_SELECTED) != 0 ? 'S' : '.');
- **窗口内嵌（Window Insets）：** fitSystemWindows属性允许 View 消耗系统窗口的内嵌（insets），并将它们应用为 View 的内边距。
- **Dirty Flag（脏标记）：** 用于标记 View 是否需要重绘。
- public boolean isDirty() {
- return (mPrivateFlags & PFLAG_DIRTY_MASK) != 0;
- }
- **坐标设置：** 提供setLeft(), setTop(), setRight(), setBottom()方法设置 View 的位置。注意，这些方法通常由布局系统调用。
- **Float 属性限制：** setMax()和setMin()方法对 float 类型属性进行了范围限制，避免非法值。
- **触点检测：** pointInView() 方法用于确定给定点是否在 View 内部。
- **刷新和重绘：** 提供 invalidate() 系列方法用于请求重绘 View。
- **调试工具：** outputDirtyFlags() 方法用于调试输出 View 及其子 View 的脏标记状态。
- **可访问性：** 提供 isAccessibilityFocused() 和 addChildrenForAccessibility() 方法，支持可访问性功能。
- **框架速率：** 根据 View 的尺寸决定帧率等级（FRAME_RATE_CATEGORY_LOW, FRAME_RATE_CATEGORY_NORMAL）。
- **View 状态:** getViewState() 决定了 View 的状态，例如：启用、焦点、选择、窗口焦点、激活状态等等。 用于绘制不同的状态效果。
- if ((mViewFlags & ENABLED_MASK) == ENABLED) viewStateIndex |= StateSet.VIEW_STATE_ENABLED;
- if (isFocused()) viewStateIndex |= StateSet.VIEW_STATE_FOCUSED;
- if ((privateFlags & PFLAG_SELECTED) != 0) viewStateIndex |= StateSet.VIEW_STATE_SELECTED;
- if (hasWindowFocus()) viewStateIndex |= StateSet.VIEW_STATE_WINDOW_FOCUSED;
- if ((privateFlags & PFLAG_ACTIVATED) != 0) viewStateIndex |= StateSet.VIEW_STATE_ACTIVATED;

**二、ViewGroup 类**

- **核心概念：** ViewGroup 是 View 的子类，可以包含其他 View（子 View）。它负责管理子 View 的布局和绘制。
- **子 View 管理：** ViewGroup 维护一个子 View 列表，并提供方法来添加、删除和访问这些子 View。
- **Padding 处理:** internalSetPadding() 方法设置内边距时，会设置 FLAG_PADDING_NOT_NULL 标志，用于优化绘制。
- @Override
- protected void internalSetPadding(int left, int top, int right, int bottom) {
- super.internalSetPadding(left, top, right, bottom);
- if ((mPaddingLeft | mPaddingTop | mPaddingRight | mPaddingBottom) != 0) {
- mGroupFlags |= FLAG_PADDING_NOT_NULL;
- } else {
- mGroupFlags &= ~FLAG_PADDING_NOT_NULL;
- }
- }
- **布局模式：** ViewGroup 支持不同的布局模式，例如 LAYOUT_MODE_OPTICAL_BOUNDS，用于基于光学校正进行布局。
- **裁剪（Clipping）：** setClipToPadding()方法控制是否将子 View 裁剪到 ViewGroup 的内边距区域内。
- **查找 View：** 提供findViewById(), findViewWithTag(), findViewByPredicate()等方法在 ViewGroup 及其子 View 中查找特定的 View。
- **Transient View (瞬时 View)：** addTransientView() 和 removeTransientView() 方法允许添加和移除临时的 View，这些 View 主要用于绘制目的，不会作为普通的子 View 管理。
- **invalidate 机制：** onDescendantInvalidated() 方法用于处理子 View 的 invalidate 请求，并将该请求传递到父 View。
- **MeasureChild:** measureChild() 和 measureChildWithMargins() 方法帮助测量子 View，同时考虑父 View 的 MeasureSpec 和 padding。
- **WindowInsets分发:** dispatchApplyWindowInsets() 方法负责将 WindowInsets 分发给子 View。存在broken和new两种分发模式。
- **重置绘制状态:** resetResolvedDrawables() 重置所有子View的可绘制对象的状态。
- **MarginLayoutParams：**
- ViewGroup.MarginLayoutParams 是 ViewGroup 子 View 的 LayoutParams 的扩展，用于指定 View 的外边距。
- 支持相对外边距（marginStart、marginEnd），并根据布局方向（layoutDirection）进行解析。
- setLayoutDirection()方法设置布局方向，并根据布局方向更新外边距。
- doResolveMargins()方法解析相对外边距，将其转换为绝对外边距（leftMargin、rightMargin）。
- **MotionEvent分发:** dispatchTouchEvent()负责将MotionEvent传递到子View。
- **比较子视图的位置：** compareBoundsOfTree() 方法比较子视图的边界，用于确定它们的绘制顺序。

**三、ViewManager 接口**

- **核心概念：** ViewManager 是一个接口，允许向 Activity 添加和删除子 View。
- **实现：** WindowManager 是 ViewManager 的一个主要实现，用于管理窗口中的 View。

**四、ViewRootImpl 类**

- **核心概念：** ViewRootImpl 是连接 View 层次结构和窗口系统的桥梁。它负责执行布局、绘制和输入事件处理。
- **窗口属性：** ViewRootImpl 维护一个 WindowManager.LayoutParams 对象，用于描述窗口的属性，例如标题、标志和布局参数。
- mClientWindowLayoutFlags 记录了客户端提供的窗口标志。
- **SurfaceHolder：** 如果 View 是 RootViewSurfaceTaker 的实例，ViewRootImpl 会创建一个 SurfaceHolder 来管理 Surface。
- **窗口标志：** getWindowFlags() 方法返回窗口的标志。
- **绘制流程：** ViewRootImpl 负责执行完整的绘制流程，包括测量、布局和绘制 View 层次结构。
- **性能优化：** 包含一些性能优化策略，如 PRIVATE_FLAG_OPTIMIZE_MEASURE 标志，用于控制是否优化测量过程。
- **窗口尺寸调整：** ViewRootImpl 包含测量层级结构的方法 measureHierarchy()，并且能够处理窗口尺寸的改变。
- shouldOptimizeMeasure()方法判断是否应该优化measure过程。
- getWindowBoundsInsetSystemBars() 获取窗口边框并排除系统栏的影响。
- **系统 UI 可见性监听：** ViewRootImpl 会监听系统 UI 可见性的变化，并做出相应的调整。
- **窗口焦点处理：** ViewRootImpl 负责处理窗口焦点事件，并将焦点传递给适当的 View。
- **输入事件处理：** ViewRootImpl 接收输入事件，并将它们分发到 View 层次结构。
- **Dpad导航支持：** 提供了对Dpad导航键的支持。
- moveFocusToAdjacentWindow() 允许将焦点移动到相邻窗口。
- **调试支持：** 提供了调试功能，包括性能分析和布局调试。
- **窗口绘制请求：** requestDrawWindow() 用于请求窗口绘制。
- **SurfaceControl 获取：** getSurfaceControl() 用于获取 SurfaceControl 对象。

**五、ViewTreeObserver 类**

- **核心概念：** ViewTreeObserver 用于注册监听器，这些监听器可以在全局布局、绘制和其他 View 树事件发生时收到通知。
- **监听器管理：** ViewTreeObserver 维护一个监听器列表，包括 OnGlobalLayoutListener、OnWindowFocusChangeListener 等。
- 提供一系列 add 和 remove 方法来注册和注销监听器，例如： addOnGlobalLayoutListener(), removeOnGlobalLayoutListener()。
- **事件通知：** 当 View 树发生变化时，ViewTreeObserver 会通知所有已注册的监听器。
- **合并Observer:** merge()方法可以将其他Observer的监听器合并到当前Observer。

**总结：**

Android 视图框架是一个复杂的系统，负责在 Android 设备上呈现用户界面。 View、ViewGroup、ViewManager、ViewRootImpl 和 ViewTreeObserver 等核心组件协同工作，以处理布局、绘制、输入事件和窗口管理。理解这些组件之间的关系对于构建高性能、响应迅速的 Android 应用程序至关重要。

这份简报只是一个概述，更深入的理解需要仔细研究源代码和 Android 官方文档。