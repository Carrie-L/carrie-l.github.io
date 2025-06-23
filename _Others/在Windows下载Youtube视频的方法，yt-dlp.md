---
layout: article
title: "在Windows下载Youtube视频的方法，yt-dlp"
date: 2025-06-23
permalink: /others/zai-windows-xia-zai-youtube-shi-pin-de-fang-fa-yt/
tags: ["Others", "Tools"]
---

简单介绍一下使用 `yt-dlp` 下载youtube视频的方法。

### 一、安装 yt-dlp
打开 [安装页面](https://github.com/yt-dlp/yt-dlp/wiki/Installation) , 点击 [windows](https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe)

### 二、在 `yt-dlp.exe` 下载到本地的路径打开cmd
例如我的下载位置：`C:\Users\windows\Downloads\Programs` , 那么我就在这个位置打开 `CMD`

切记**不是双击exe**安装！而是 `使用命令行` 下载！

### 三、下载视频的命令行
```
.\yt-dlp [url]
```

但是 youtube 会提示要求登录以验证不是机器人。怎么解决呢？看下面的步骤。

### 四、浏览器安装 cookies 插件
1. 在 [chrome应用商店](https://chromewebstore.google.com/) 输入 `get cookies` ， 选择一个插件安装。
2. 安装完成后，把插件固定到浏览器状态栏。
3. 打开youtube界面（登录状态），点击 `get cookies`插件，导出youtube的`cookies`。

![](../../assets/blogimages/Snipaste_2025-06-23_17-22-29.png)

4. 复制cookies在本地的路径到记事本里，如: `C:\Users\windows\Pictures\www.youtube.com_cookies.txt` 。

### 五、 正式开始下载：
按照下面这个例子的格式下载youtube视频。

`.\yt-dlp --cookies ` 不变，中间填你在步骤四导出的`cookies`本地路径，然后是youtube视频链接。

```ssh
.\yt-dlp --cookies "C:\Users\windows\Pictures\www.youtube.com_cookies.txt" https://www.youtube.com/watch?
```

下载完成后的视频就在 `yt-dlp.exe`的安装目录下。

