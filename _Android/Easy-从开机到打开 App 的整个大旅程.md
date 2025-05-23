---
layout: article
title: "Easy-从开机到打开 App 的整个大旅程"
date: 2025-05-01
permalink: /android/easy-cong-kai-ji-dao-da-kai-app-de-zheng-ge-da-lv/
tags: ["Android", "Activity"]
---

 

想象你的手机是一座需要慢慢唤醒并开始工作的**超级大工厂**。

1. **按下电源键（按下工厂总开关）**
    
    - 手机通电，就像给整个工厂接通了电源。
    - 一个叫做 **Bootloader** 的“守门老大爷”先醒来，做一些最最基础的检查，确保硬件没问题，然后决定下一步该叫醒谁。

2. **启动 Linux 内核（启动工厂的“大脑”）**
    
    - 守门老大爷叫醒了工厂的“**中央电脑**”（Linux Kernel）。这是手机操作系统的核心，负责管理最底层的资源，比如电力、内存等。它开始启动，让工厂有了基本的运作能力。

3. **`init` 进程启动（第一个“工头”上班）**
    
    - 中央电脑启动后，它会叫醒第一个“**工头**”，名字叫 `init`。这个工头非常重要，是所有其他管理者和工人的“祖先”。
    - `init` 工头会按照一个清单，开始做很多准备工作，比如准备好文件柜（文件系统）、启动一些基础服务。

4. **启动 Zygote（“复印机妈妈”上岗）**
    
    - `init` 工头的一项重要任务就是把我们之前说的“**复印机妈妈”（Zygote）** 通上电，让它准备好。
    - Zygote 启动后，会把自己需要的基础工具（共享的 Java 类库等）都加载好，进入待命状态，随时准备“复印”。

5. **启动 SystemServer（“总管”办公室开门）**
    
    - Zygote 准备好之后，它的第一个大任务就是**复制**出我们说的那个“**总管**”办公室（**SystemServer** 进程）。
    - SystemServer 这个“总管”开始工作，把它办公室里的各个部门经理都叫醒，比如：
        - **AMS (Activity Manager Service)**：“活动经理”，负责管理所有的“活动”（比如哪个 App 页面该显示）。
        - **WMS (Window Manager Service)**：“窗口经理”，负责管理屏幕上的所有“窗口”。
        - **PMS (Package Manager Service)**：“包裹经理”，知道工厂里安装了哪些“App 包裹”。
        - 还有电源经理、通知经理等等好多好多……它们都开始运行，整个工厂的核心管理层就绪了。

6. **显示桌面（Launcher）（工厂“大厅”展示出来）**
    
    - 等 SystemServer 里的经理们准备得差不多了，“活动经理”（AMS）会说：“好了，先把工厂的**大厅**（**Launcher**，也就是你的手机桌面）展示出来给用户看吧！”
    - 于是，AMS 通知 Zygote：“快，复印一个‘大厅’程序出来！” Zygote 就创建了 Launcher 应用的进程。
    - Launcher 启动后，会向“包裹经理”（PMS）要来所有已安装 App 的信息（图标和名字），并把它们显示在屏幕上，也就是你看到的布满图标的手机桌面。这个过程也需要“窗口经理”（WMS）来分配屏幕上的位置。

7. **点击 App 图标（按下某个“车间”的门铃）**
    
    - 你在手机桌面上，用手指点击了某个 App 的图标，比如“小游戏”App。

8. **启动 App 进程（为“小游戏车间”开门并派工人）**
    
    - “大厅”程序（Launcher）接收到你的点击，它立刻报告给“活动经理”（AMS）：“报告！用户想启动‘小游戏’App！”
    - AMS 收到请求，它会先检查“小游戏”这个“车间”是不是已经开着了。如果没开：
        - AMS 会再次找到“复印机妈妈”（Zygote）：“嘿，Zygote，快帮我复印一个新的、专门给‘小游戏’用的‘车间’（进程）出来！”
        - Zygote “唰”地一下，基于自己身上的模板，快速复制出一个新的进程，这就是“小游戏”App 运行的地方。

9. **App 内部初始化（“小游戏车间”内部准备）**
    
    - 新的“小游戏车间”（App 进程）启动后，它内部也要做准备工作：
        - 创建自己的“车间主任”（`ActivityThread`）。
        - 创建 `Application` 对象（整个 App 的全局管家）。

10. **启动首页 Activity（开始生产第一个“玩具”）**
    
    - “活动经理”（AMS）看到“小游戏车间”准备好了，就对里面的“车间主任”下指令：“开始生产你们的第一个‘玩具’（首页 Activity）！”
    - “车间主任”（`ActivityThread`）收到指令，就会创建 `Activity` 对象，然后按照顺序调用它的 `onCreate()`, `onStart()`, `onResume()` 这些方法，让这个“玩具”（Activity 页面）开始组装。

11. **视图绘制与显示（把“玩具”摆到橱窗展示）**
    
    - 在 Activity 的 `onResume()` 之后，Activity 需要显示界面了：
        - Activity 会向“窗口经理”（WMS）申请一个“橱窗”（Window）。
        - WMS 批准后，Activity 就会开始把它界面上的按钮、图片、文字等（Views）画在一个叫做 `Surface` 的“画布”上。
        - 这个“画布”画好后，会交给一个叫做 **SurfaceFlinger** 的“超级快递员”。
    - **SurfaceFlinger**（这个“快递员”其实在 SystemServer 启动后不久也由 `init` 或 Zygote 相关流程启动了）负责把所有 App 画好的“画布”、状态栏、导航栏等组合（合成）在一起。
    - 最后，SurfaceFlinger 把最终合成好的完整画面，交给**屏幕硬件**，唰！你就看到了“小游戏”App 的首页显示在眼前了！

这个过程是不是很长很神奇？从按下电源键到看到 App 界面，手机内部的“工人们”和“管理者们”做了超级多的工作！每一步都紧密相连。
