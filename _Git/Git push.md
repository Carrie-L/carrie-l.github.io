---
layout: article
title: "Git push"
date: 2025-05-29
permalink: /git/git-push/
tags: ["Git", "基础知识"]
---

 

> git push origin main 和 git push origin v1.2.0 有什么区别？
 
### ✅ 简明对比

|命令|作用|推送的是什么？|
|---|---|---|
|`git push origin main`|推送代码分支|把你在 `main` 分支上的所有提交推送到远程仓库|
|`git push origin v1.2.0`|推送标签|把你打的 `v1.2.0` 标签推送到远程仓库，不影响代码分支|

### 🧠 更通俗地说

#### 🟩 `git push origin main`

👉 把你写的代码（main 分支上的提交）推送到远程  
📦 传的是“**代码内容**”

#### 🟦 `git push origin v1.2.0`

👉 把你给某次提交打的“版本标签”推送到远程  
📎 传的是“**某个快照的别名**”

### ✅ 示例场景

你在本地做了这些事：

```bash
# 做了一些修改
git commit -m "Add feature A"

# 推送代码到 GitHub
git push origin main

# 打上标签（表示这是 v1.2.0）
git tag -a v1.2.0 -m "Release version 1.2.0"

# 现在你需要推送这个标签
git push origin v1.2.0
```

如果 **只运行 `git push origin main`**，你的代码会推送成功，**但 GitHub 不会显示 Release 标签**，因为你没有推送 `v1.2.0`。

### ✅ 一个命令推送所有标签

```bash
git push origin --tags
```

等价于：

- `git push origin v1.2.0`
    
- `git push origin v1.2.1`
    
- …等所有本地已有的 tag
    
### ✅ 视觉类比图

```
本地仓库
├── main 分支 （你写的代码） ─────────┐
│                                     │
│                                     ▼
│                               git push origin main
│
├── v1.2.0 标签 ──► 对 main 某次提交打的标记
│                                     ▼
│                               git push origin v1.2.0
```

## 🔚 总结口诀

> 📦 `git push origin main` = 推送你写的“内容”  
> 🏷 `git push origin v1.2.0` = 推送你给“内容”起的“标签名”

相关页面：
[[Git Tag]]
