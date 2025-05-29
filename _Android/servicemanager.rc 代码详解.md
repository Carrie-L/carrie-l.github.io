---
layout: article
title: "servicemanager.rc 代码详解"
date: 2025-05-06
permalink: /android/servicemanager-rc-dai-ma-xiang-jie/
tags: ["AOSP", "Android", "源码分析"]
---

   

### servicemanager 本身在做什么？——10 步快览

| 顺序     | 代码/行为                                         | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------ | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1**  | `init` fork-exec `/system/bin/servicemanager` | 权限：`user system`、`group system`，标记 `critical`，若反复崩溃系统会重启                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **2**  | 进程 `main()` 打开 **/dev/binder**                | 获得 Binder 驱动 FD                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **3**  | `ioctl(fd, BINDER_SET_CONTEXT_MGR, 0)`        | 把自己注册成 **Binder Context Manager**（“0 号服务”）([Android Go Source](https://android.googlesource.com/platform/system/hwservicemanager/%2B/e09e6b11976c7111018fb5e5ce92465df89b4235/hw_service_manager.cpp?utm_source=chatgpt.com "hw_service_manager.cpp - platform/system/hwservicemanager"))                                                                                                                                                                                                                                                |
| **4**  | 创建 Binder 线程池、Looper                          | 为后续事务收发做准备                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **5**  | 初始化内部哈希表 `ServiceTable`                       | 用于存放 **名字→Binder 引用**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **6**  | `SetProperty("servicemanager.ready","true")`  | 通知世界“我就绪了”，客户端 `IServiceManager.cpp` 会轮询等这个属性([Android Go Source](https://android.googlesource.com/platform/frameworks/native/%2B/master/cmds/servicemanager/main.cpp?autodive=0%2F%2F%2F%2F&utm_source=chatgpt.com "cmds/servicemanager/main.cpp - platform/frameworks/native"), [Android Go Source](https://android.googlesource.com/platform//frameworks/native/%2B/7456c7e8d93fbf8ac1c2baba7d1533f056d630d6/libs/binder/IServiceManager.cpp?utm_source=chatgpt.com "libs/binder/IServiceManager.cpp - platform//frameworks/native")) |
| **7**  | 进入 `binder_loop(handle_transaction)`          | 死循环等待事务                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **8**  | 处理四大指令                                        | `ADD_SERVICE`、`GET_SERVICE`、`CHECK_SERVICE`、`LIST_SERVICES`                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **9**  | 监听服务死亡通知                                      | 当被注册的服务进程死掉，发送 `binder::Status::linkToDeath` 回调给使用者                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **10** | 停不下来的守护                                       | 标记 `critical`；若 4 分钟内崩 4 次以上，init 会触发 reboot，保证系统一致性                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

![](../../assets/blogimages/mermaid-diagram-2025-05-06-155815.png)

**servicemanager = Binder 世界的“户籍处”**：必须在 zygote 之前建好档案柜，否则 Java 世界注册 / 查询系统服务全都会因“查无此人”而失败。

### servicemanager.rc 代码

**servicemanager** 的启动位置：
`frameworks/native/cmds/servicemanager/servicemanager.rc` :

```c++
service servicemanager /system/bin/servicemanager
    class core animation
    user system
    group system readproc
    critical
    file /dev/kmsg w
    onrestart setprop servicemanager.ready false
    onrestart restart --only-if-running apexd
    onrestart restart audioserver
    onrestart restart gatekeeperd
    onrestart class_restart --only-enabled main
    onrestart class_restart --only-enabled hal
    onrestart class_restart --only-enabled early_hal
    task_profiles ProcessCapacityHigh
    shutdown critical
```

这个代码块定义了核心的 `servicemanager` 进程应该如何被 `init` 系统管理。

- **`service servicemanager /system/bin/servicemanager`**
    
    - **`service`**: 这个关键字标志着一个服务定义块的开始。
    - **`servicemanager`**: 这是在 `init` 系统内部赋予该服务的**名称**。`.rc` 文件的其他部分将使用这个名称来控制该服务（例如 `start servicemanager`）。`servicemanager` 通常指 Android Binder 机制的服务注册和查询中心。
    - **`/system/bin/servicemanager`**: 这是 `init` 启动此服务时将要运行的**可执行文件的完整路径**。这个二进制文件包含了 `servicemanager` 的实际代码。

- **`class core animation`**
    
    - **`class`**: 指定该服务所属的**类**。类用于将相关服务分组，以便于管理（例如，一次性启动或停止某个类中的所有服务）。
    - **`core animation`**: 将此服务同时分配给 `core` 类（通常是系统启动早期所需的核心服务）和 `animation` 类（可能与图形/显示栈相关的服务）。

- **`user system`**
    
    - **`user`**: 指定 `servicemanager` 进程在被 `init`（初始以 root 身份运行）启动后，应该以哪个**用户账户**运行。
    - **`system`**: 该进程将以 `system` 用户（UID 通常为 1000）的身份运行，这限制了其权限，使其低于 root 权限。

- **`group system readproc`**
    
    - **`group`**: 指定 `servicemanager` 进程应该在哪个**用户组**下运行。
    - **`system readproc`**: 该进程的主用户组将是 `system`（GID 通常为 1000），并且它也将属于 `readproc` 这个附加组。`readproc` 组很可能授予了从 `/proc` 文件系统读取进程信息的权限。
- **`critical`**
    
    - **`critical`**: 这是一个**选项**，标记该服务对于系统的基本运行（尤其是在启动期间）至关重要。如果一个标记为 `critical` 的服务在启动初期反复崩溃，`init` 可能会触发设备重启进入 recovery（恢复）模式，以防启动循环。它也影响关闭顺序（关键服务通常在后面关闭）。

- **`file /dev/kmsg w`**
    
    - **`file`**: 这个选项与文件描述符有关。
    - **`/dev/kmsg`**: 指定内核消息缓冲区设备。
    - **`w`**: 表示**写入（write）**权限。这行代码很可能是为了确保 `servicemanager` 进程启动时拥有一个可用于写入内核日志 (`/dev/kmsg`) 的文件描述符，以便在标准日志系统尚未就绪时也能直接记录关键错误。

- **`onrestart setprop servicemanager.ready false`**
    
    - **`onrestart`**: 定义了**当 `servicemanager` 进程崩溃并被 `init` 自动重启时**，`init` 应该执行的命令。
    - **`setprop servicemanager.ready false`**: 这个命令设置名为 `servicemanager.ready` 的 Android 系统属性，值为 `false`。这可能是向系统的其他部分发出信号，表明 servicemanager 在重启期间暂时不可用。

- **`onrestart restart --only-if-running apexd`**
    
    - **`onrestart`**: `servicemanager` 重启时执行的另一条命令。
    - **`restart --only-if-running apexd`**: 告诉 `init` 重启名为 `apexd` 的服务，但 `--only-if-running` 标志确保**仅当 `apexd` 在 `servicemanager` 崩溃时确实在运行时**才尝试重启。这用于处理依赖关系；`apexd` 很可能依赖于 `servicemanager`。

- **`onrestart restart audioserver`**
    
    - **`onrestart`**: `servicemanager` 重启时执行的另一条命令。
    - **`restart audioserver`**: 告诉 `init` 重启 `audioserver` 服务，表明存在另一个依赖关系。

- **`onrestart restart gatekeeperd`**
    
    - **`onrestart`**: `servicemanager` 重启时执行的另一条命令。
    - **`restart gatekeeperd`**: 告诉 `init` 重启 `gatekeeperd` 服务，表明存在另一个依赖关系。

- **`onrestart class_restart --only-enabled main`**
    
    - **`onrestart`**: `servicemanager` 重启时执行的另一条命令。
    - **`class_restart --only-enabled main`**: 告诉 `init` 重启所有属于 `main` 类的服务，但 `--only-enabled` 标志表示**仅重启那些当前被标记为“已启用”的服务**。这是一个更广泛的重启动作，针对可能受 `servicemanager` 崩溃影响的服务。

- **`onrestart class_restart --only-enabled hal`**
    
    - **`onrestart`**: `servicemanager` 重启时执行的另一条命令。
    - **`class_restart --only-enabled hal`**: 告诉 `init` 重启所有属于 `hal`（硬件抽象层）类的已启用服务。HAL 服务通常严重依赖 `servicemanager` 进行注册和发现。

- **`onrestart class_restart --only-enabled early_hal`**
    
    - **`onrestart`**: `servicemanager` 重启时执行的另一条命令。
    - **`class_restart --only-enabled early_hal`**: 告诉 `init` 重启所有属于 `early_hal` 类的已启用服务。

- **`task_profiles ProcessCapacityHigh`**
    
    - **`task_profiles`**: 一个**选项**，用于将特定的调度策略和资源分配配置文件（通常在 `task_profiles.json` 等文件中定义）应用到此服务的进程。
    - **`ProcessCapacityHigh`**: 要应用的配置文件的名称。这很可能给予 `servicemanager` 更高的 CPU 优先级或保证其获得足够的 CPU 资源，反映其作为核心 Binder 服务注册中心的重要性。

- **`shutdown critical`**
    
    - **`shutdown`**: 一个**选项**，指定该服务在设备关机期间的行为。
    - **`critical`**: 与启动时的 `critical` 选项类似，这确保该服务在设备关机过程中被优先处理（通常关闭得较晚，并可能给予更多时间来完成清理工作）。

总而言之，这个代码块详细指示 `init` 进程如何启动和管理 `/system/bin/servicemanager`：以 `system` 用户/组身份运行，标记为关键服务，赋予特定权限，应用性能配置，并定义了一套详细的恢复机制（主要是重启依赖服务），以应对其意外崩溃和重启的情况。