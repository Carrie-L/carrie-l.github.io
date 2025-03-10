import os
import sys
import tkinter as tk
from tkinter import Toplevel, Label, Button, Radiobutton, StringVar
import subprocess

# 预设目录列表
dirs = ["Android", "Algorithm", "DSA", "MCP", "Language"]

class DirSelector:
    def __init__(self, file_path):
        self.file_path = file_path
        self.selected_dir = None
        
        # 从文件路径中提取文件名(不含扩展名)
        self.article_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # 创建主窗口
        self.root = tk.Tk()
        self.root.withdraw()  # 隐藏主窗口
        
        # 创建选择窗口
        self.create_selector_window()
        
        # 运行主循环
        self.root.mainloop()
    
    def create_selector_window(self):
        # 创建顶层窗口
        self.selector = Toplevel(self.root)
        self.selector.title("选择博客分类")
        self.selector.geometry("300x400")
        self.selector.resizable(False, False)
        
        # 使窗口置顶
        self.selector.attributes('-topmost', True)
        
        # 窗口居中
        screen_width = self.selector.winfo_screenwidth()
        screen_height = self.selector.winfo_screenheight()
        x = (screen_width - 300) // 2
        y = (screen_height - 400) // 2
        self.selector.geometry(f"300x400+{x}+{y}")
        
        # 显示文章名
        Label(self.selector, text=f"文章: {self.article_name}", 
              font=("Arial", 10), pady=5).pack(pady=10)
        
        # 标题
        Label(self.selector, text="选择要发布到的博客分类:", 
              font=("Arial", 12, "bold")).pack(pady=10)
        
        # 创建单选按钮组
        self.dir_var = StringVar(value=dirs[0])  # 默认选择第一个
        
        for dir_name in dirs:
            Radiobutton(self.selector, text=dir_name, variable=self.dir_var,
                       value=dir_name, font=("Arial", 11),
                       pady=5, padx=20, anchor="w").pack(fill="x")
        
        # 自定义选项
        Label(self.selector, text="或输入自定义分类:", 
              font=("Arial", 10)).pack(pady=(15, 5), anchor="w", padx=20)
        
        self.custom_var = tk.Entry(self.selector, font=("Arial", 10))
        self.custom_var.pack(fill="x", padx=20, pady=5)
        
        # 按钮区域
        button_frame = tk.Frame(self.selector)
        button_frame.pack(pady=20)
        
        Button(button_frame, text="确认", font=("Arial", 11),
              bg="#4CAF50", fg="white", width=10,
              command=self.confirm).pack(side="left", padx=10)
        
        Button(button_frame, text="取消", font=("Arial", 11),
              width=10, command=self.cancel).pack(side="left", padx=10)
    
    def confirm(self):
        # 优先使用自定义输入
        custom_dir = self.custom_var.get().strip()
        if custom_dir:
            self.selected_dir = custom_dir
        else:
            self.selected_dir = self.dir_var.get()
        
        self.publish_article()
        self.selector.destroy()
        self.root.quit()
    
    def cancel(self):
        self.selector.destroy()
        self.root.quit()
    
    def publish_article(self):
        if not self.selected_dir:
            return
        
        # 执行发布命令
        script_dir = r"I:\B-MioBlogSites"
        os.chdir(script_dir)
        
        cmd = f'call .venv\\Scripts\\activate.bat && python blog_push_local.py "{self.article_name}" --dir={self.selected_dir}'
        
        # 在新窗口中执行命令
        subprocess.run(f'start cmd /k "cd /d {script_dir} && {cmd}"', shell=True)
        print(f"正在发布：{self.article_name} 到 {self.selected_dir} 目录")

def main():
    # 检查参数
    if len(sys.argv) < 2:
        print("请提供文件路径作为参数")
        return
    
    file_path = sys.argv[1]
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误：文件不存在 {file_path}")
        return
    
    # 创建并运行选择器
    DirSelector(file_path)

if __name__ == "__main__":
    main()