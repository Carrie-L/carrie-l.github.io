#MCP
## MCP是什么？

### 1. MCP的基本概念

MCP（Model Context Protocol，模型上下文协议）是一个开放协议，旨在标准化应用程序如何向大型语言模型（LLM）提供上下文。它允许LLM与外部数据源和工具无缝集成，从而使AI模型能够访问实时数据并执行更复杂的任务。

[官方MCP Github主页](https://github.com/modelcontextprotocol)
[官方文档Introduction](https://modelcontextprotocol.io/introduction)
[支持MCP特性的客户端列表](https://modelcontextprotocol.io/clients)

### 2. MCP的架构

MCP的核心组件包括：

- **主机（Host）**：运行LLM的应用程序（如Claude Desktop），负责发起与MCP服务器的连接。
- **客户端（Client）**：在主机应用程序内部运行，与MCP服务器建立1:1连接。
- **服务器（Server）**：提供对外部数据源和工具的访问，响应客户端的请求。
- **LLM**：大型语言模型，通过MCP获取上下文并生成输出。
- **工作流程**：
    1. 主机启动客户端。
    2. 客户端连接到MCP服务器。
    3. 服务器提供资源、提示或工具。
    4. LLM使用这些信息生成响应。

![[Pasted image 20250309141722.png]]

### 3. MCP的原语

MCP通过三种主要原语（Primitives）增强LLM的功能，理解这些原语是编写MCP的关键：

1. **提示（Prompts）**：预定义的指令或模板，指导LLM如何处理输入或生成输出。
2. **资源（Resources）**：提供额外上下文的结构化数据，例如文件或数据库内容。
3. **工具（Tools）**：可执行的函数，允许LLM执行操作（如查询API）或检索信息。

- **关键点**：这些原语是MCP的核心，决定了服务器能为LLM提供什么能力。

## MCP Server 构建一个简单的MCP服务器

在我们的示例中，使用 **Claude for Desktop** 作为客户端，自己编写python文件作为服务端，在 Claude Desktop 里调用server.py。

**先决条件**
- 已安装 python 3.10 或更高
- 已安装 Claude for Desktop

### 1. 安装uv，设置环境变量

打开 Powershell，输入如下命令：
```sh
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

打开系统高级环境变量，在 `Path` 将uv路径添加进去：
```
C:\Users\windows\.local\bin
```
![[Pasted image 20250309142611.png]]
重启 Powershell 。
在命令行输入 `uv --version` ， 能返回版本信息就算安装成功了:
![[Pasted image 20250309142737.png]]

### 2. 创建和设置项目

打开 **Powershell** ， `cd` 到你想要创建项目的目录位置，如:
![[Pasted image 20250309142936.png]]

接着依次输入以下命令：
```sh
# Create a new directory for our project
uv init weather
cd weather

# Create virtual environment and activate it
uv venv
.venv\Scripts\activate

# Install dependencies
uv add mcp[cli] httpx

# Create our server file。new-item 是powershell 命令，用于创建文件
new-item weather.py
```

### 3. 添加代码

将以下代码整个复制到 `weather.py`：
```python
from typing import Any  
import httpx  
from mcp.server.fastmcp import FastMCP  
  
# Initialize FastMCP server  
mcp = FastMCP("weather")  
  
# Constants  
NWS_API_BASE = "https://api.weather.gov"  
USER_AGENT = "weather-app/1.0"  
  
async def make_nws_request(url: str) -> dict[str, Any] | None:  
    """Make a request to the NWS API with proper error handling."""  
    headers = {  
        "User-Agent": USER_AGENT,  
        "Accept": "application/geo+json"  
    }  
    async with httpx.AsyncClient() as client:  
        try:  
            response = await client.get(url, headers=headers, timeout=30.0)  
            response.raise_for_status()  
            return response.json()  
        except Exception:  
            return None  
  
def format_alert(feature: dict) -> str:  
    """Format an alert feature into a readable string."""  
    props = feature["properties"]  
    return f"""  
Event: {props.get('event', 'Unknown')}  
Area: {props.get('areaDesc', 'Unknown')}  
Severity: {props.get('severity', 'Unknown')}  
Description: {props.get('description', 'No description available')}  
Instructions: {props.get('instruction', 'No specific instructions provided')}  
"""  
  
@mcp.tool()  
async def get_alerts(state: str) -> str:  
    """Get weather alerts for a US state.  
  
    Args:        state: Two-letter US state code (e.g. CA, NY)    """    url = f"{NWS_API_BASE}/alerts/active/area/{state}"  
    data = await make_nws_request(url)  
  
    if not data or "features" not in data:  
        return "Unable to fetch alerts or no alerts found."  
  
    if not data["features"]:  
        return "No active alerts for this state."  
  
    alerts = [format_alert(feature) for feature in data["features"]]  
    return "\n---\n".join(alerts)  
  
@mcp.tool()  
async def get_forecast(latitude: float, longitude: float) -> str:  
    """Get weather forecast for a location.  
  
    Args:        latitude: Latitude of the location        longitude: Longitude of the location    """    # First get the forecast grid endpoint  
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"  
    points_data = await make_nws_request(points_url)  
  
    if not points_data:  
        return "Unable to fetch forecast data for this location."  
  
    # Get the forecast URL from the points response  
    forecast_url = points_data["properties"]["forecast"]  
    forecast_data = await make_nws_request(forecast_url)  
  
    if not forecast_data:  
        return "Unable to fetch detailed forecast."  
  
    # Format the periods into a readable forecast  
    periods = forecast_data["properties"]["periods"]  
    forecasts = []  
    for period in periods[:5]:  # Only show next 5 periods  
        forecast = f"""  
{period['name']}:  
Temperature: {period['temperature']}°{period['temperatureUnit']}  
Wind: {period['windSpeed']} {period['windDirection']}  
Forecast: {period['detailedForecast']}  
"""  
        forecasts.append(forecast)  
  
    return "\n---\n".join(forecasts)  
  
if __name__ == "__main__":  
    # Initialize and run the server  
    mcp.run(transport='stdio')
```

如果代码里提示依赖错误，安装对应的包就好。

### 4. 运行服务

打开 **Claude for Desktop** , 点击左上角菜单 —— File —— Settings —— Developer

点击 `Edit Config` ，就会在 `C:\Users\windows\AppData\Roaming\Claude` 目录下自动创建 `claude_desktop_config.json` 文件。

打开 `claude_desktop_config.json` , 添加如下代码：

```json
{
    "mcpServers": {
        "weather": {
            "command": "uv",
            "args": [
                "--directory",
                "T:\\PythonProject\\weather",
                "run",
                "weather.py"
            ]
        }
    }
}
```

其中路径为在上一步创建的`weather`目录, 使用**绝对路径**。

这会告诉 Claude for Desktop ，
- 我们的服务名叫 `weather` , 
- 通过 `uv --directory T:\\PythonProject\\weather run weather` 来启动服务。

保存文件。


### 5. 在Claude中使用服务

打开**任务管理器**，将 Claude **结束任务**，彻底关掉。
重新打开 **Claude for Desktop** 。

如果在Claude的对话框下看到了一把**锤子**，说明我们的MCP服务配置成功了。
![[Pasted image 20250309144616.png]]

点击锤子能看到：
![[Pasted image 20250309144830.png]]

在设置页显示如下：
![[Pasted image 20250309144513.png]]

**下面测试服务：**

在对话框输入：*what's the weather in NY*
![[Pasted image 20250309144742.png]]

服务配置成功啦！



## MCP Client

> 要使用Claude API, 需要充值购买credits
> 否则请求会报Error: Error code: 403 - {'error': {'type': 'forbidden', 'message': 'Request not allowed'}}

### 1. 创建和设置项目

前期的步骤与上文介绍的一致，先决条件和uv的安装看 **MCP Server** 部分。
打开Powershell , cd 到python项目的目录下，依次输入如下命令：

```sh
# Create project directory
uv init mcp-client
cd mcp-client

# Create virtual environment
uv venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Unix or MacOS:
source .venv/bin/activate

# Install required packages
uv add mcp anthropic python-dotenv

# Create our main file
new-item client.py
```

### 2. 配置API_KEY

```SH
new-item .env
```
打开`.env`文件，复制以下代码：
```
ANTHROPIC_API_KEY=<your key here>
```
在[Claude控制台](https://console.anthropic.com/settings/keys)创建KEY（需充值才能用），将API Key复制到`.env` （确保key的安全，不要分享出去！）

将`.env`文件添加到.gitignore , 在 powershell 输入以下命令：
```sh
echo ".env" >> .gitignore
```

### 3. 添加代码
```python
import asyncio  
from typing import Optional  
from contextlib import AsyncExitStack  
  
from mcp import ClientSession, StdioServerParameters  
from mcp.client.stdio import stdio_client  
  
from anthropic import Anthropic  
from dotenv import load_dotenv  
  
load_dotenv()  # load environment variables from .env  
  
class MCPClient:  
    def __init__(self):  
        # Initialize session and client objects  
        self.session: Optional[ClientSession] = None  
        self.exit_stack = AsyncExitStack()  
        self.anthropic = Anthropic()  
    # methods will go here  
  
    async def connect_to_server(self, server_script_path: str):  
        """Connect to an MCP server  
  
        Args:            server_script_path: Path to the server script (.py or .js)        """        is_python = server_script_path.endswith('.py')  
        is_js = server_script_path.endswith('.js')  
        if not (is_python or is_js):  
            raise ValueError("Server script must be a .py or .js file")  
  
        command = "python" if is_python else "node"  
        server_params = StdioServerParameters(  
            command=command,  
            args=[server_script_path],  
            env=None  
        )  
  
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))  
        self.stdio, self.write = stdio_transport  
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))  
  
        await self.session.initialize()  
  
        # List available tools  
        response = await self.session.list_tools()  
        tools = response.tools  
        print("\nConnected to server with tools:", [tool.name for tool in tools])  
  
    async def process_query(self, query: str) -> str:  
        """Process a query using Claude and available tools"""  
        messages = [  
            {  
                "role": "user",  
                "content": query  
            }  
        ]  
  
        response = await self.session.list_tools()  
        available_tools = [{  
            "name": tool.name,  
            "description": tool.description,  
            "input_schema": tool.inputSchema  
        } for tool in response.tools]  
  
        # Initial Claude API call  
        response = self.anthropic.messages.create(  
            model="claude-3-5-sonnet-20241022",  
            max_tokens=1000,  
            messages=messages,  
            tools=available_tools  
        )  
  
        # Process response and handle tool calls  
        tool_results = []  
        final_text = []  
  
        assistant_message_content = []  
        for content in response.content:  
            if content.type == 'text':  
                final_text.append(content.text)  
                assistant_message_content.append(content)  
            elif content.type == 'tool_use':  
                tool_name = content.name  
                tool_args = content.input  
  
                # Execute tool call  
                result = await self.session.call_tool(tool_name, tool_args)  
                tool_results.append({"call": tool_name, "result": result})  
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")  
  
                assistant_message_content.append(content)  
                messages.append({  
                    "role": "assistant",  
                    "content": assistant_message_content  
                })  
                messages.append({  
                    "role": "user",  
                    "content": [  
                        {  
                            "type": "tool_result",  
                            "tool_use_id": content.id,  
                            "content": result.content  
                        }  
                    ]  
                })  
  
                # Get next response from Claude  
                response = self.anthropic.messages.create(  
                    model="claude-3-5-sonnet-20241022",  
                    max_tokens=1000,  
                    messages=messages,  
                    tools=available_tools  
                )  
  
                final_text.append(response.content[0].text)  
  
        return "\n".join(final_text)  
  
    async def chat_loop(self):  
        """Run an interactive chat loop"""  
        print("\nMCP Client Started!")  
        print("Type your queries or 'quit' to exit.")  
  
        while True:  
            try:  
                query = input("\nQuery: ").strip()  
  
                if query.lower() == 'quit':  
                    break  
  
                response = await self.process_query(query)  
                print("\n" + response)  
  
            except Exception as e:  
                print(f"\nError: {str(e)}")  
  
    async def cleanup(self):  
        """Clean up resources"""  
        await self.exit_stack.aclose()  
  
async def main():  
    if len(sys.argv) < 2:  
        print("Usage: python client.py <path_to_server_script>")  
        sys.exit(1)  
  
    client = MCPClient()  
    try:  
        await client.connect_to_server(sys.argv[1])  
        await client.chat_loop()  
    finally:  
        await client.cleanup()  
  
if __name__ == "__main__":  
    import sys  
    asyncio.run(main())
```

如果开头anthropic报错，安装anthropic就好。

### 4. 运行Client

这里我们使用上文创建的mcp服务**weather**
在powershell输入：
```sh
uv run client.py T:/PythonProject/weather/weather.py
```

![[Pasted image 20250309153533.png]]

接着，我们就可以在 Query 输入问题了。

至此，我们的第一个MCP服务端和客户端编写完成。

