# Android Passpoint 官方文档内容

## developer.android.com 页面摘要
URL: https://developer.android.com/develop/connectivity/wifi/passpoint

**概述：**
Passpoint 是 Wi-Fi 联盟（WFA）制定的协议，使移动设备能够发现并认证提供互联网接入的 Wi-Fi 热点。

**核心要点：**
- Passpoint（也称 Hotspot 2.0）让设备自动发现并连接支持该标准的 Wi-Fi 热点
- 使用 WPA3-Enterprise 或 WPA2-Enterprise 认证，比开放 Wi-Fi 更安全
- 优势：自动连接（无需手动输入密码）、安全认证、运营商网络漫游
- 相关类：PasspointConfiguration、WifiNetworkSuggestion.Builder.addPasspointConfig()
- 漫游：Passpoint 让设备在不同地点（咖啡馆、机场、酒店）自动连接，无需重复认证
- 更多信息参考：Wi-Fi suggestion API for internet connectivity

---

## source.android.com 完整文档

URL: https://source.android.com/docs/core/connectivity/wifi-passpoint

### 概述
Passpoint 是 Wi-Fi 联盟（WFA）制定的协议，使移动设备能够发现并认证提供互联网接入的 Wi-Fi 热点。

### 设备支持
注意：支持 Passpoint 是运行 Android 11 或更高版本且具有 Wi-Fi 功能的设备的必要条件。

设备制造商需要实现 Supplicant 接口才能支持 Passpoint：
- Android 13 起，接口使用 AIDL 进行 HAL 定义
- Android 13 之前，使用 HIDL

### 实现要求

**Android 11 及更高版本：**
运行 Android 11 或更高版本的设备支持 Passpoint 需：
- 设备制造商需提供 802.11u 的固件支持
- AOSP 已包含所有其他支持要求

**Android 10 及更低版本：**
需同时提供框架、HAL 和固件支持：
- 框架：启用 Passpoint（需要功能标志）
- 固件：支持 802.11u

在 device.mk（位于 device/<oem>/<device>）中修改 PRODUCT_COPY_FILES 环境变量以包含 Passpoint 功能支持：
```
PRODUCT_COPY_FILES += frameworks/native/data/etc/android.hardware.wifi.passpoint.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.wifi.passpoint.xml
```

### 验证
运行以下 Passpoint 包单元测试来验证实现：
- 服务测试：`atest com.android.server.wifi.hotspot2`
- 管理器测试：`atest android.net.wifi.hotspot2`

### Passpoint R1 配置
Android 6.0 起已支持 Passpoint R1，允许通过 Web 下载包含配置文件和凭证信息的特殊文件来配置 Passpoint R1（版本 1）凭证。客户端自动启动特殊的 Wi-Fi 安装程序，让用户在看或拒绝内容前查看部分信息。

**支持的 EAP 类型：**
- EAP-TTLS
- EAP-TLS
- EAP-SIM
- EAP-AKA
- EAP-AKA'

**下载机制：**
- Passpoint 配置文件必须托管在 Web 服务器上
- 应使用 TLS（HTTPS）保护（因为可能包含明文密码或私钥数据）
- 内容由 MIME 多部分文本组成，使用 UTF-8 编码和 base64 编码（RFC-2045 第 6.8 节）
- HTTP 头字段：
  - Content-Type 必须设置为 application/x-wifi-config
  - Content-Transfer-Encoding 必须设置为 base64
  - Content-Disposition 不得设置
  - HTTP 方法必须是 GET
- 下载必须通过点击 HTML 元素（如按钮）触发（不支持自动重定向到下载 URL）
- 此行为特定于 G

### Passpoint R2 及更高版本
（文档内容待补充，R2 增加了更多自动化特性）

### 相关技术对比
| 特性 | Passpoint | Wi-Fi Suggestion | Wi-Fi Bootstrap (P2P) |
|------|-----------|-----------------|---------------------|
| 用途 | 自动连接热点 | 建议系统连接网络 | 请求连接P2P设备 |
| 认证 | WPA3/WPA2 Enterprise | WPA2/WPA3 Personal | 无（设备间直连）|
| 漫游 | 支持多地点漫游 | 不支持 | 不支持 |
| 授权 | 首次配置后自动 | 首次批准后自动 | 每次需用户授权 |
