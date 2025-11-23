---
layout: article
title: "什么是 Bootloader？——“点火钥匙 + 发动机自检”"
date: 2025-05-01
permalink: /android/shen-me-shi-bootloader-dian-huo-yao-shi-fa-dong-ji/
tags: ["Android", "Activity"]
---

 

把手机当一辆车：

|类比|真正做的事|为什么必须有|
|---|---|---|
|**钥匙点火**(按下电源键)|电源管理芯片 (PMIC) 把各路电压拉起来，SoC 脱离掉电状态。|只有先来电，芯片才能开始执行指令。|
|**行车电脑自检**(Boot ROM)|SoC 里烧死的 **Boot ROM** 代码从片内 SRAM 跑起来，找可启动介质（eMMC/UFS/SD）。|保证“第一条指令”不可被篡改，建立信任链的根。|
|**一级 Bootloader**(SPL / BL1 / XBL)|体积极小：先把 **DRAM 初始化**（让内存可用），再把二级 Bootloader 读到 DRAM。|没内存就加载不了大东西；放片内 SRAM 容量有限，只能写很小的初始化程序。|
|**二级 Bootloader**(LK、Aboot、U-Boot、UEFI ABL…)|- 初始化更多外设（LCD、USB、调试口）- **验证签名** ➜ Android Verified Boot (AVB)- 提供 **Fastboot/Recovery** 模式- 读取 **Kernel + dtb + ramdisk**，填好启动参数，最后 `jump` 到 Kernel 入口|① 把硬件准备到“操作系统可接管”的水平② 保证系统分区未被篡改③ 给用户/厂商留刷机、救砖入口|

> **一句话记：Bootloader = “上电后负责把 Linux 内核安全、完整、正确地请上台的主持人。”**

---

## “点火”全过程 5 步 30 秒读完

1. **Power Key → PMIC 上电**  
    电源键被拉低 → PMIC 依次给核心、IO、内存通电并稳定时钟。
    
2. **Boot ROM 执行**
    
    - 固化在芯片，地址固定。
        
    - 查启动顺序 (eFuse/OTP 配置)：UFS → eMMC → USB 等。
        
    - 把找到的 **一级 Bootloader** 读进片内 SRAM，跳转过去。
        
3. **一级 Bootloader (SPL)**
    
    - 打开 PLL、DDR 控制器，把 **DRAM** 配好。
        
    - 读取二级 Bootloader 到 DRAM。
        
    - 简单签名校验（很多平台直接信任二级 BL 的公钥）。
        
4. **二级 Bootloader**
    
    - **更多硬件初始化**：比如显示、触摸、USB OTG。
        
    - **AVB 验签**：校验 vbmeta/table，确保 `boot.img` 没被改。
        
    - 若长按组合键 → 进入 **Fastboot/Recovery** 模式（常见刷机界面）。
        
    - 读取 `boot.img`（Kernel + dtb + ramdisk），设置内核参数 (`cmdline`)。
        
    - 关闭缓存/MMU，设置栈，跳入 Kernel 入口地址。
        
5. **Linux Kernel 接管**  
    从此开始装驱动、挂根文件系统，再启动 `init`。→ 进入你熟悉的 Android 世界。
    

---

## 面试高频问点（Bootloader 篇）

1. **为什么要多级 Bootloader？**  
    片内 SRAM 小；先用小 SPL 把 DRAM 打开，再加载功能丰富的大 Bootloader。
    
2. **Bootloader 做“Verified Boot”在哪一层？**  
    通常在 **二级 Bootloader** 做（基于 Google AVB 2.0）；它自己由 Boot ROM 的烧死公钥验证。
    
3. **Fastboot 模式属于谁提供？**  
    由二级 Bootloader（LK/Aboot/ABL）里的命令循环实现，USB 设备枚举为 0x18d1:0x4EE0。
    
4. **BL31 / TrustZone 跟 Bootloader 什么关系？**  
    BL31 是 ARM Trusted Firmware（ATF）的 EL3 固件，常由二级 Bootloader 加载并把 EL3 控制权让渡给它。
    

---

### 记忆口诀

```
点电 → Boot ROM 找头靴 → SPL 开内存 → 大 BL 验签 + 加载内核 → Kernel 接棒
```
