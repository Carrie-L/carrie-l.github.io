import os
import sys
import tkinter as tk
from tkinter import simpledialog
import subprocess

def main():
    # 获取传入的文件名参数
    if len(sys.argv) < 2:
        print("请提供文件名作为参数")
        return
    
    article_name = sys.argv[1]
    
    # 创建一个简单的对话框
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    # 预设目录列表
    dirs = ["Android", "Algorithm", "DSA", "MCP", "Language"]
    
    # 显示目录选择对话框
    dir_choice = simpledialog.askstring(
        "选择目标目录", 
        "请输入目标目录名称:\n(预设: " + ", ".join(dirs) + ")\n",
        initialvalue="Android"
    )
    
    if not dir_choice:
        print("已取消发布")
        return
    
    # 执行发布命令
    script_dir = r"T:\PythonProject\MCPServer"
    os.chdir(script_dir)
    
    # 打开新的命令窗口执行发布命令
    cmd = f'call .venv\\Scripts\\activate.bat && python blog_push_local.py "{article_name}" --dir={dir_choice}'
    subprocess.run(f'start cmd /k "cd /d {script_dir} && {cmd}"', shell=True)

if __name__ == "__main__":
    main()