---
layout: article
title: "init.rc 介绍"
date: 2025-05-06
permalink: /android/init-rc-jie-shao/
tags: ["Android", "AOSP"]
---

  

### 1. `init.rc` 是什么编程语言？

严格来说，Android 的 `init.rc` 文件使用的**不是**一种通用的“编程语言”，而是一种**自定义的、领域特定的配置脚本语言 (Domain-Specific Language, DSL)**。

- **设计目的:** 这种语言专门为 Android 的 `init` 进程设计，用于在系统启动过程中定义服务 (services)、动作 (actions)、命令 (commands) 和选项 (options)。

- **特点:**
    - **声明式:** 主要描述系统应该处于什么状态（例如，哪些服务应该运行，哪些属性应该设置）。
    - **基于事件/触发器:** 大量使用 `on <trigger>` 结构来定义在特定事件（如 `boot`, `property:sys.boot_completed=1`）发生时要执行的一系列命令。
    - **结构化:** 文件由不同的节 (sections) 组成，如 `on`, `service` 等。
    - **包含特定命令:** 它有自己的一套内置命令（如 `start`, `stop`, `write`, `exec`, `chown`, `chmod`, `setprop` 等），这些命令由 `init` 进程直接解析和执行。

所以，它不是 C、Java、Python 或标准的 Shell 脚本（尽管它的一些命令看起来像 Shell 命令）。它就是 **Android Init Language**。

### 2. init.rc 是什么？

`init.rc` 是 **Android 操作系统中一个核心的配置文件**。
可以把它理解为 Android 系统**启动过程中的主要"脚本"或"指令集"**。

以下是关于 `init.rc` 的关键信息：

1. **使用者:** 它主要由 Android 的 `init` 进程使用。`init` 是 Linux 内核启动后运行的第一个用户空间进程 (PID 1)，它的核心职责就是根据配置（主要是 `.rc` 文件）来初始化和启动系统的其余部分。
    
2. **用途和功能:** `init.rc` 文件（以及它导入的其他 `.rc` 文件）定义了系统启动时需要执行的一系列任务，包括：
    
    - **挂载文件系统:** 如 `/system`, `/data`, `/cache` 等，使存储设备可用。
    - **设置系统属性 (System Properties):** 定义各种系统配置参数（如 `ro.product.model`, `persist.sys.timezone`），这些参数供系统和应用程序使用。
    - **启动核心服务 (Services):** 启动和管理系统运行所必需的后台进程（守护进程/daemons），例如：
        - `zygote`: Android 应用进程的孵化器。
        - `surfaceflinger`: 图形界面合成器。
        - `logd`: 系统日志服务。
        - 各种硬件相关的服务（如 RIL - 无线接口层、传感器服务等）。
        - 网络服务 (`netd`) 等。
    - **定义动作 (Actions):** 基于特定的触发器 (Triggers) 执行一系列命令。例如，`on boot` 会在系统启动时执行，`on property:sys.boot_completed=1` 会在系统启动完成后执行。
    - **设置权限和属主:** 配置设备节点、文件或目录的访问权限、用户和用户组。

3. **语言:** 它使用一种特殊的、为 `init` 进程定制的脚本语言，称为 **Android Init Language**。这是一种声明式、基于事件的语言，包含特定的节（如 `on`, `service`）和命令（如 `start`, `stop`, `write`, `mount`, `setprop`, `chmod`, `chown` 等）。它不是标准的 Shell 脚本，虽然有些命令看起来相似。
    
4. **位置:** 在现代 Android 系统中，主 `init.rc` 文件通常位于系统分区的根目录（早期是设备根目录 `/init.rc`），但更常见的是，配置被拆分到多个 `.rc` 文件中，分布在 `/system/etc/init/`, `/vendor/etc/init/`, `/odm/etc/init/` 等目录下，并通过 `import` 命令相互关联。
    
**总之，`init.rc` 是 Android 系统启动的蓝图，它指导 `init` 进程如何设置系统环境、启动必要的服务，并响应特定的系统事件，最终将设备带入正常运行状态。** 对这个文件的修改会直接影响设备的启动行为和核心功能。

### init.cpp 和 init.rc 是什么关系？

- **`init.cpp` 是程序的实现 (The Engine/Executor)。**
- **`init.rc` 是程序的配置和指令 (The Instructions/Blueprint)。**

详细解释如下：

1. **`init.cpp`:**
    - **性质:** 这是一个 **C++ 源代码文件**。它是构成 Android `init` 可执行程序（通常位于 `/sbin/init` 或类似路径）的主要源文件之一。
    - **角色:** 它包含了实现 `init` 进程核心功能的 **C++ 代码逻辑**。这包括：
        - **解析器 (Parser):** 代码用于读取、理解和解析 `.rc` 文件（包括 `init.rc` 及其导入的其他文件）。
        - **命令执行器:** 代码用于执行在 `.rc` 文件中定义的各种命令（如 `start`, `stop`, `write`, `mount`, `setprop` 等）。
        - **服务管理器:** 代码用于启动、停止、重启和管理在 `.rc` 文件中定义的系统服务。
        - **事件/属性处理:** 代码用于监视系统事件（如 `boot` 完成）和属性变化，并执行 `.rc` 文件中与这些触发器关联的动作。
        - **进程管理:** 作为 PID 1，它负责管理子进程（主要是系统服务）。
    - **结果:** `init.cpp` 和其他相关的 C/C++ 源文件经过编译和链接后，生成一个**可执行的二进制文件** (`/sbin/init`)，这个文件在系统启动时由内核加载并运行。

2. **`init.rc`:**
    - **性质:** 这是一个**文本配置文件/脚本文件**。它使用一种特定的、为 `init` 进程设计的脚本语言（Android Init Language）。
    - **角色:** 它包含了 `init` 进程在启动过程中需要执行的**具体指令和配置**。它告诉 `init` 进程：
        - **何时 (When):** 基于不同的触发器（`on boot`, `on property:sys.boot_completed=1` 等）。
        - **做什么 (What):** 执行哪些命令（`mount`, `write`, `start` 等）。
        - **启动哪些服务 (Which Services):** 定义系统核心服务及其属性（路径、用户、组、权限、启动参数等）。
        - **设置什么环境 (Environment):** 配置系统属性、文件系统挂载点等。
    - **结果:** 它被 `init` 进程（也就是由 `init.cpp` 编译成的程序）读取和解释。

**关系总结:**

可以把 `init.cpp` 想象成一个**解释器或执行引擎**，而 `init.rc` 则是这个引擎需要读取和执行的**脚本或蓝图**。

- `init` 进程（由 `init.cpp` 构建）启动后，它的首要任务之一就是去查找并**解析** `init.rc`（以及它 `import` 的其他 `.rc` 文件）。
- 根据 `init.rc` 文件中的**指令**，`init` 进程执行相应的动作，如挂载文件系统、设置属性、启动服务等。
- 没有 `init.rc`（或有效的 `.rc` 文件），`init` 进程（`init.cpp` 的产物）就不知道该做什么来启动整个 Android 系统。
- 反过来，只有 `init.rc` 文件而没有 `init` 进程（`init.cpp` 的产物）来读取和执行它，这些指令也无法生效。

它们共同构成了 Android 系统初始化和启动的核心机制。开发者或设备制造商通过修改 `.rc` 文件来定制不同设备的启动行为，而 `init` 进程（`init.cpp`）则提供了执行这些定制化指令的通用框架。