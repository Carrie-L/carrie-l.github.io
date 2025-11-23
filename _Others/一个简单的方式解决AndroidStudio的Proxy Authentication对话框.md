---
layout: article
title: "一个简单的方式解决AndroidStudio的Proxy Authentication对话框"
date: 2025-09-14
permalink: /others/yi-ge-jian-dan-de-fang-shi-jie-jue-androidstudio-d/
tags: ["Others", "工具"]
---

 

Android Studio 突然总是弹 Proxy Authentication，而本地代理无需鉴权，每次都要手动把对话框关掉，挺烦的，试了一些方案都没解决，今天终于用这个最简单的方式解决了。

简单来说，就是把 `HTTP Proxy` 里的代理设置关掉。

![](../../assets/blogimages/Snipaste_2025-09-14_13-52-20.png)

1. 在项目的 `gradle.properties` 添加：

```shell
systemProp.http.nonProxyHosts=localhost;127.*;10.*;172.16.*;172.17.*;172.18.*;172.19.*;172.20.*;172.21.*;172.22.*;172.23.*;172.24.*;172.25.*;172.26.*;172.27.*;172.28.*;172.29.*;172.30.*;172.31.*;192.168.*  
systemProp.http.proxyHost=127.0.0.1  
systemProp.http.proxyPort=  

systemProp.https.nonProxyHosts=localhost;127.*;10.*;172.16.*;172.17.*;172.18.*;172.19.*;172.20.*;172.21.*;172.22.*;172.23.*;172.24.*;172.25.*;172.26.*;172.27.*;172.28.*;172.29.*;172.30.*;172.31.*;192.168.*  
systemProp.https.proxyHost=127.0.0.1  
systemProp.https.proxyPort=
```

![](../../assets/blogimages/Pasted image 20250914180927.png)

2. 在**设置 —— HTTP Proxy** 里，选择 `No proxy` 保存。**重启 Android Studio** 。

![](../../assets/blogimages/Pasted image 20250914180711.png)

因为这里面已经添加了代理，所以 `HTTP Proxy` 里选择 `No proxy`  不影响 Gradle 下载，但是能杜绝 IDE 弹窗。 

IDE 的 `HTTP Proxy` 是使用 检查更新、插件市场、内置浏览器等。