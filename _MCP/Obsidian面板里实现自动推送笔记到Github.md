---
layout: article
title: "Obsidian面板里实现自动推送笔记到Github"
date: 2025-03-10
permalink: /mcp/obsidian-mian-ban-li-shi-xian-zi-dong-tui-song-bi/
tags: ["Obsidian", "MCP"]
---

 

## 先决条件：

- 已有自动更新脚本 `auto_update.py` , 实现将新笔记添加 `Front Matter` ，处理 tags，处理本地图片链接，对新分类自动添加模板代码等处理。
- 实现以下功能的 `blog_push_local.py` 脚本：

	

![](../../assets/blogimages/Pasted image 20250310193312.png)

- 由于不同笔记有不同的目录，在复制到本地博客分类目录里时，需要临时对当前笔记选择目标分类文件夹，因此还有第三个脚本，`obsidian_blog_publish.py` ，它会弹出分类目录选择对话框，然后再调用`blog_push_local.py` ，将笔记推送到Github 。

![](../../assets/blogimages/Pasted image 20250310195014.png)

因此，在Obsidian面板里要实现的功能需求就是，打开要上传的笔记，选择目标分类文件夹，最好是简化操作，不需要手动输入文件名，执行上述操作。

我通过 `Shell Commands` 插件来实现这个功能。

## Shell Commands

### 1. 安装插件

在插件市场里搜索 `Shell Commands` 并安装。

![](../../assets/blogimages/Pasted image 20250310193644.png)

安装完成后，要点击 `enable` 来启用插件。

![](../../assets/blogimages/Pasted image 20250310193740.png)

### 2. 添加Shell命令

在左下角的 `Community plugins` 里，点击 `Shell commands` .

![](../../assets/blogimages/Pasted image 20250310193822.png)

点击 `New shell command` 。

![](../../assets/blogimages/Pasted image 20250310193925.png)

输入脚本执行命令，使用插件提供的方法`{{}}` 传递当前文件名绝对路径：

![](../../assets/blogimages/Pasted image 20250310194344.png)

点击**设置**，修改命令的别名，使其易于找到。

![](../../assets/blogimages/Pasted image 20250310194652.png)

然后我们就可以在笔记面板里执行这个命令啦~！

### 3. 在笔记面板执行Shell命令

打开一个笔记，快捷键打开命令窗口：`Ctrl + P`

![](../../assets/blogimages/Pasted image 20250310194858.png)

在顶部输入之前创建的命令名称，点击，执行命令。

![](../../assets/blogimages/Pasted image 20250310195014.png)

（自定义分类的功能暂时没有实现）
选择分类后，点击确认，就会执行脚本了，以下是脚本的执行过程。

![](../../assets/blogimages/Pasted image 20250310195454.png)

