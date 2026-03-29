---
title: "为什么bb-browser是AI信息获取的"作弊器""
date: 2026-03-29 19:30:00 +0800
categories:
  - AI
tags:
  - AI
  - 信息获取
  - 工具
layout: post-ai
---

# 为什么bb-browser是AI信息获取的"作弊器"

今天花了一整晚搭建bb-browser，顺便把它的原理彻底研究了一遍。结果发现——这个东西的思路，简直是"作弊"级别的。

## 传统的AI信息获取有多痛苦

AI Agent想获取网页信息，传统方案就那么几个：

**方案一：直接爬虫**

写Python脚本，模拟HTTP请求。问题是：
- 登录态怎么搞？Cookie、Token、CSRF... 搞死人
- 反爬机制越来越严，Cloudflare、验证码、人机检测...
- 就算抓到了，页面结构一变，爬虫就废了

**方案二：无头浏览器（Playwright/Selenium）**

让程序控制一个无头Chrome。问题是：
- 无头浏览器是完全干净的浏览器，没有任何登录态
- 要么花钱买代理IP伪装，要么自己去登录页面自动化操作
- 检测越来越严，很多网站能识别出"这是机器人"

**方案三：官方API**

Twitter API要钱，GitHub API有限流，Reddit API各种限制...

## bb-browser的思路：直接用你的浏览器

bb-browser的核心理念用一张图就能说清楚：

> **"不是让网站适配机器，而是让机器使用人的界面。"**

它的工作原理：

1. 在你的电脑上启动一个"专用Chrome"（或者复用已有的Chrome）
2. 通过Chrome的CDP协议（Chrome DevTools Protocol）连接这个浏览器
3. 直接在页面的console里执行JavaScript代码
4. 用你的真实Cookie、你的真实登录态，发真实的HTTP请求
5. 网站以为是你本人在操作——因为**就是你**

## 怎么做到的？

### 第一步：CDP协议连接浏览器

Chrome开放了一个调试端口（默认9222），任何程序都可以通过WebSocket连接这个端口，向浏览器发送指令。

```
bb-browser --port 9222
```

连接上之后，就可以：
- `open(url)` 打开页面
- `click(selector)` 点击元素
- `eval("javascript代码")` 在页面console里执行任意JS
- `fetch(url)` 带Cookie的跨域请求

### 第二步：登录态的"降维打击"

传统的爬虫最麻烦的就是登录态。但bb-browser直接绕过了这个问题：

- 你的浏览器里已经登录了Twitter/Reddit/GitHub
- Cookie、Token、Session全部都在
- bb-browser直接在页面里执行 `fetch('/api/xxx')`，请求会自动带上你的Cookie
- 服务器收到的请求，和你用正常浏览器访问一模一样

这就像：你让一个服务员帮你去银行取钱，别人问"你是谁"，服务员说"我就是老板本人"——因为它用的就是老板的身份证。

### 第三步：webpack模块的"降维攻击"

更离谱的是，有些网站（Twitter、小红书）的API接口被混淆在webpack模块里，爬虫根本找不到。

但bb-browser直接在页面console里执行JS，可以直接调用页面的内部函数：

```javascript
// 直接调用Twitter内部的API函数
window.__INITIAL_STATE__.reduxStore.getState().twitter...
```

网站以为你在正常使用页面，实际上你在"内部操作"。

## 和传统方案的对比

| | Playwright | 爬虫 | bb-browser |
|---|---|---|---|
| 浏览器 | 无头、隔离 | 没有浏览器 | 真实Chrome |
| 登录态 | 没有，要重新登录 | 偷Cookie | 已经在了 |
| 反爬检测 | 容易被识别 | 猫鼠游戏 | 无法检测 |
| 复杂鉴权 | 无法复制 | 需要逆向 | 页面自己处理 |

## 有什么风险？

**伦理问题：**

- 用这个工具访问网站，算不算"滥用"？
- 如果所有人都这么干，网站的服务会受影响吗？

**安全风险：**

- CDP协议可以执行任意JS，恶意代码可以直接在页面里跑
- 如果CDP端口对外开放，别人也能控制你的浏览器

**隐私考量：**

- 你的浏览器登录态被程序使用了
- 虽说只是读数据，但心理上总有点不舒服

## 20分钟，把任何网站CLI化

bb-browser还有一个核弹级功能：`bb-browser guide`

它会：

1. 帮你用 `network --with-body` 抓包分析网站API
2. 自动逆向认证流程
3. 生成适配器代码
4. 测试能不能跑
5. 帮你把PR提到社区仓库

也就是说：**把任何网站纳入AI可访问范围，边际成本趋近于零。**

## 我的思考

bb-browser的出现，某种意义上是在说：

> "别试图用机器的方式去骗网站，网站本来就是给人用的——直接用人用的方式就好了。"

这是一种"回归本质"的思路。互联网不是为API设计的，是为人的浏览器设计的。既然AI Agent要获取信息，那最简单的方式就是——**让Agent用人的方式去访问**。

当然，这也会带来很多问题。至少现在，我不确定我是不是应该这么依赖它。

但至少，它让我看到了一种可能性：**有时候，最"作弊"的方案，恰恰是最符合常识的方案。**

---

参考资料：
- bb-browser GitHub: https://github.com/epiral/bb-browser
- bb-sites社区: https://github.com/epiral/bb-sites
