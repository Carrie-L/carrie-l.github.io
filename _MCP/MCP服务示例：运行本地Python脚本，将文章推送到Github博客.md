---
layout: article
title: "MCP服务示例：运行本地Python脚本，将文章推送到Github博客"
date: 2025-03-10
permalink: /mcp/mcp-fu-wu-shi-li-yun-xing-ben-di-python-jiao-ben-j/
tags: ["MCP"]
---

 
在上一篇文章里，我们学习了[MCP的入门操作](https://carrie-l.github.io/mcp/mcp-quickstart-guide/)，在这篇文章，我们使用MCP服务来解决我的一个实际需求。

我的博客是用jekyll部署的Github静态页面，当我完成一篇Obsidian笔记后，我需要手动将这篇笔记复制到本地的博客目录，由我的自动更新脚本[auto_update](https://github.com/Carrie-L/carrie-l.github.io/blob/main/auto_update.py)来修改笔记的格式，为它添加顶部Front Matter。如果笔记里有图片，我还需要手动将图片复制到博客目录，并执行`git`操作推送到远程仓库。

这个过程太繁琐了，因此我想简化这个流程，于是借助Cursor写了一个新的自动化脚本[blog_push_local.py]()，提供笔记路径和目标分类文件夹后，它会自动将源目录下的笔记和图片复制到目标路径，调用[auto_update.py](https://github.com/Carrie-L/carrie-l.github.io/blob/main/auto_update.py)，然后执行`git`操作。

我在命令行输入以下命令，就会执行这个过程：

```sh
python blog_push_local.py "MCP QuickStart Guide" --dir=MCP
```

这个流程也可以借助MCP服务来完成。

---

### 1. 导入MCP服务器模块 

安装mcp库：

```
pip install mcp
```

### 2. 创建MCP服务器实例 

```python
from mcp.server import FastMCP

# 初始化 MCP 服务器
mcp = FastMCP("blog_publisher", timeout=300) # 5分钟超时时间
```

其中第一个参数就是mcp服务的名称。

### 3. 将现有功能注册为MCP工具 

`工具 tools` 允许服务器将函数暴露给客户端调用，并由LLMs执行。

在方法顶部添加 `@mcp.tool()` 
```python
# 将现有函数转换为MCP工具
@mcp.tool(name="blog")
def publish_to_blog(article_name: str, dir: str = "Android") -> str:
```

通过这种方式，客户端的`tools` 里就能看到可用的工具了，如下所示：

![](../../assets/blogimages/Pasted image 20250310144459.png)

使用 `tools/call` 调用工具，服务器执行请求操作，并返回结果。

### 4. 添加服务器启动代码 

完整代码见Github仓库。

### 5. 测试和部署

测试MCP服务器:

```
python blog_push.py
```

脚本会启动MCP服务器，并在控制台显示启动信息。

#### 1. 配置Claude使用MCP服务

打开 **Claude for Desktop** , 点击左上角菜单 —— File —— Settings —— Developer

点击 `Edit Config` ，如果没有 `claude_desktop_config.json` 就会在  `C:\Users\windows\AppData\Roaming\Claude` 目录下自动创建 `claude_desktop_config.json` 文件。

打开 `claude_desktop_config.json` , 添加如下代码：

```json
"blog_publisher":{
            "command": "uv",
            "args": [
                "--directory",
                "T:\\PythonProject\\MCPServer",
                "run",
                "blog_push.py"
            ]
        }
```

第一行 `blog_publisher` 是我们的服务名称，也就是在第二步中指定的。
下面是服务器运行路径。

在`任务管理器`结束Claude，再重新打开Claude，就能看到配置成功了。

![](../../assets/blogimages/Pasted image 20250310155646.png)

在上面图片里，我们看到的工具描述是通过如下方式添加的：
```python
@mcp.tool(name="blog")
async def blog_command(article_name: str, dir: str = "_Android") -> str:
    """博客发布工具
    Args:
        article_name: 要发布的文章名称
        dir: 目标目录，默认为_Android
    """
```

同时在设置页里我们也可以看到有两个服务：

![](../../assets/blogimages/Pasted image 20250310155718.png)

#### 2. 在Claude使用服务

在对话框里输入：
```python
blog MCP QuickStart Guide --dir=MCP
# 或
/tool blog MCP QuickStart Guide --dir=MCP
```

**为什么我这么输入？**

因为在我的blog服务里，我将工具命名为了`blog` ，在函数里添加了两个参数，一个接收 文件名，一个接收目标分类名称，其中：

- blog : 工具名
- MCP QuickStart Guide ： 文章名
- --dir ：目标目录分类名

因此它会形成这样的Json格式：

```json
{
	"dir": "MCP",
	"article_name": "MCP QuickStart Guide"
}
```

最终输出结果：

![](../../assets/blogimages/Pasted image 20250310155819.png)

我们在Claude成功调用了blog_publisher服务！

#### 3. 在Cursor使用MCP服务

打开 **Cursor设置 —— MCP —— Add new MCP server**

![](../../assets/blogimages/Pasted image 20250310160725.png)

它需要我们填写几个参数，在上一步的Claude配置里，我们在json文件中添加了如下配置：

```json
"blog_publisher":{
            "command": "uv",
            "args": [
                "--directory",
                "T:\\PythonProject\\MCPServer",
                "run",
                "blog_push.py"
            ]
        }
```

在这里，我们将它复制过来即可。

- **`Name`** ： 服务名，也就是 `blog_publisher` .
- **`Type`** : 选择 `command`
- **`Command`** : `uv --directory T:\PythonProject\MCPServer run blog_push.py` 

![](../../assets/blogimages/Pasted image 20250310160938.png)

点击 `Save` 保存。

然后我们就能在Cursor看到已成功配置服务了，绿点表示已启用。

![](../../assets/blogimages/Pasted image 20250310161340.png)

接着我们来实际测试一下：

```

```

![](../../assets/blogimages/Pasted image 20250310161501.png)
