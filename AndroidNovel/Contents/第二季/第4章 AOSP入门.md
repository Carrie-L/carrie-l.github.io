---
chapter_id: '4'
title: '第四课：AOSP 入门 · Android 系统结构'
official_url: 'https://source.android.com/docs'
status: 'done'
<parameter name="author">minimax m2.5 - OpenClaw'
plot_summary:
  time: '第二十九天'
  location: 'Compose 村·城市规划馆'
  scene: '小 Com 展示 Android 系统的城市规划'
  season: '春季'
  environment: '城市规划馆里巨大的城市模型'
---

# 第四课：AOSP 入门 · Android 系统结构

---

“叮——”

林小满发现自己站在一个巨大的城市规划馆里。一个巨大的城市模型展示在眼前。

“今天我们要学 AOSP！”小 Com 走了过来，“AOSP 是 Android 开放源代码项目，学会它，你就能理解 Android 是怎么工作的！”

“AOSP？”林小满问。

“对！”小 Com 说，“AOSP = Android Open Source Project，就是 Android 的源代码！”

---

## 1. Android 系统架构

“先看 Android 的整体架构。”小 Com 展示了：

```
┌─────────────────────────────────────────────────────┐
│                    应用层 (Apps)                   │
│         微信、抖音、王者荣耀、你的 App              │
├─────────────────────────────────────────────────────┤
│                Java 框架层 (Framework)              │
│    Activity Manager、Package Manager、Window Manager│
├─────────────────────────────────────────────────────┤
│                  Native 本地层 (Native)            │
│        SurfaceFlinger、MediaPlayer、WebView         │
├─────────────────────────────────────────────────────┤
│                    HAL 硬件抽象层                   │
│        Camera HAL、Bluetooth HAL、Sensor HAL        │
├─────────────────────────────────────────────────────┤
│                    Linux 内核                       │
│          驱动、内存管理、电源管理、安全              │
└─────────────────────────────────────────────────────┘
```

---

## 2. AOSP 目录结构

“AOSP 源码的目录结构是这样的。”小 Com 展示了：

```
aosp/
├── art/                  # Android Runtime (ART 虚拟机)
├── bionic/               # C 库
├── bootable/             # 启动相关
├── build/                # 构建系统
├── dalvik/               # Dalvik 虚拟机（旧）
├── external/             # 开源第三方库
├── frameworks/           # 框架层（Java）
│   ├── base/
│   │   ├── core/        # 核心 API
│   │   ├── graphics/    # 图形
│   │   ├── package/     # 包管理
│   │   └── policy/      # 策略
│   └── native/          # 本地框架
├── hardware/            # HAL 接口
├── kernel/              # 内核
├── libcore/             # 核心库
├── packages/            # 系统应用
├── prebuilts/           # 预编译工具
├── system/              # 系统组件
└── toolchain/          # 工具链
```

---

## 3. Framework 层

“Framework 层是 Android 的核心。”小 Com 介绍了：

**主要服务**：

| 服务 | 作用 |
|------|------|
| ActivityManagerService | Activity 管理 |
| WindowManagerService | 窗口管理 |
| PackageManagerService | 应用管理 |
| ContentProvider | 数据共享 |
| Binder | 进程间通信 |

---

## 4. Binder 机制

“Binder 是 Android 的核心 IPC 机制。”小 Com 展示了：

```
┌──────────────┐      ┌──────────────┐
│   进程 A     │      │   进程 B     │
│  (App)       │      │  (System)    │
│              │      │   Service    │
│   Proxy      │◄────►│   Stub       │
│              │ Binder │              │
└──────────────┘      └──────────────┘
```

**Binder 原理**：
- Client/Server 架构
- 一次拷贝（比其他 IPC 快）
- 基于共享内存

```kotlin
// AIDL 示例
interface IMyService {
    void doSomething(int value);
    int getValue();
}
```

---

## 5. Handler 机制

“Handler 是 Android 的消息机制。”小 Com 展示了：

```
┌─────────────────────────────────────┐
│            MessageQueue             │
│  [msg1] → [msg2] → [msg3] → ...   │
└──────────────────┬──────────────────┘
                   │
         ┌─────────┴─────────┐
         │                   │
    ┌────▼────┐        ┌────▼────┐
    │ Handler │        │  Looper │
    │ (发送)  │───────►│ (循环)  │
    └─────────┘        └─────────┘
```

```kotlin
// Handler 使用
val handler = Handler(Looper.getMainLooper()) {
    // 处理消息
    true
}

// 发送消息
handler.sendMessage(Message.obtain().apply {
    what = 1
    obj = "数据"
})

// 或者
handler.post {
    // 在主线程执行
}
```

---

## 6. Activity 启动流程

“Activity 是怎么启动的？”小 Com 展示了：

```
App                ActivityManagerService      ActivityThread
  │                        │                        │
  │  startActivity()       │                        │
  │───────────────────────►│                        │
  │                        │                        │
  │                        │  createActivity()     │
  │                        │──────────────────────►│
  │                        │                        │
  │                        │   Activity Created    │
  │◄───────────────────────│───────────────────────│
  │                        │                        │
  │  onCreate()           │                        │
  │◄───────────────────────│                        │
  │                        │                        │
```

**关键类**：
- `ActivityManagerService` - 系统服务
- `ActivityTaskManagerService` - Activity 任务管理
- `ActivityThread` - 应用主线程
- `Instrumentation` - 生命周期控制

---

## 7. View 系统

“View 是怎么绘制到屏幕的？”小 Com 展示了：

```
setContentView()
      │
      ▼
DecorView 创建
      │
      │ measure()
      ▼
View 测量大小
      │
      │ layout()
      ▼
View 确定位置
      │
      │ draw()
      ▼
View 绘制内容
      │
      ▼
SurfaceFlinger 合成
      │
      ▼
显示到屏幕
```

---

## 8. 编译 AOSP

“怎么编译 AOSP？”小 Com 展示了：

```bash
# 1. 初始化仓库
source build/envsetup.sh

# 2. 选择目标
lunch aosp_x86_64-eng

# 3. 编译
m -j8

# 4. 运行模拟器
emulator
```

---

## 9. System Server

“System Server 是 Android 的大脑。”小 Com 介绍了：

**System Server 启动的服务**：

```kotlin
// SystemServer.java
private void run() {
    // 1. 启动引导服务
    traceBeginAndSlog("StartBootstrapServices");
    // ActivityManagerService, PowerManagerService...
    traceEnd();
    
    // 2. 启动核心服务
    traceBeginAndSlog("StartCoreServices");
    // BatteryService, UsageStatsService...
    traceEnd();
    
    // 3. 启动其他服务
    traceBeginAndSlog("StartOtherServices");
    // WindowManagerService, PackageManagerService...
    traceEnd();
}
```

---

## 10. 实战：调试系统服务

“来调试一个系统服务！”小 Com 提议道。

**用 ADB 调试**：

```bash
# 查看系统服务
adb shell dumpsys -l

# 查看特定服务
adb shell dumpsys activity

# 查看内存
adb shell dumpsys meminfo

# 查看包信息
adb shell dumpsys package <package-name>
```

---

## 本课小结

今天林小满学到了：

1. **Android 架构**：分层设计
2. **AOSP 目录**：源码结构
3. **Framework**：核心框架
4. **Binder**：进程间通信
5. **Handler**：消息机制
6. **Activity 启动**：完整流程
7. **View 绘制**：measure-layout-draw
8. **编译 AOSP**：构建流程

---

“AOSP 太复杂了！”林小满说。

“没错！”小 Com 说，“但理解系统，才能成为高级开发者！”

---

*”叮——“*

手机通知：**“第二季第四章 已解锁：AOSP 入门”**

---

**下集预告**：第五课 · Hook 与插件化 · 动态修改 Android 系统
