import os
import sys
import tkinter as tk
from tkinter import Toplevel, Label, Button, Radiobutton, StringVar, Frame, Canvas, Scrollbar, messagebox
import subprocess

# 预设目录列表
dirs = ["Android", "Algorithm", "DSA", "MCP", "Language","OS","Others"]

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
        self.selector.resizable(True, True)
        
        # 使窗口置顶
        self.selector.attributes('-topmost', True)
        
        # 创建Canvas和Scrollbar
        canvas = Canvas(self.selector)
        scrollbar = Scrollbar(self.selector, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)
        
        # 配置Canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 绑定滚动框架大小变化事件
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # 在Canvas中创建窗口
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # 显示文章名
        Label(scrollable_frame, text=f"文章: {self.article_name}", 
              font=("Arial", 10), pady=5).pack(pady=10)
        
        # 标题
        Label(scrollable_frame, text="选择要发布到的博客分类:", 
              font=("Arial", 12, "bold")).pack(pady=10)
        
        # 创建单选按钮组
        self.dir_var = StringVar(value=dirs[0])  # 默认选择第一个
        
        for dir_name in dirs:
            Radiobutton(scrollable_frame, text=dir_name, variable=self.dir_var,
                       value=dir_name, font=("Arial", 11),
                       pady=5, padx=20, anchor="w").pack(fill="x")
        
        # 自定义选项
        Label(scrollable_frame, text="或输入自定义分类\n（_前缀 + 首字母大写的英文名）:", 
              font=("Arial", 10)).pack(pady=(15, 5), anchor="w", padx=20)
        
        self.custom_var = tk.Entry(scrollable_frame, font=("Arial", 10))
        self.custom_var.pack(fill="x", padx=20, pady=5)
        
        # 按钮区域
        button_frame = tk.Frame(scrollable_frame)
        button_frame.pack(pady=20)
        
        Button(button_frame, text="确认", font=("Arial", 11),
              bg="#4CAF50", fg="white", width=10,
              command=self.confirm).pack(side="left", padx=10)
        
        Button(button_frame, text="取消", font=("Arial", 11),
              width=10, command=self.cancel).pack(side="left", padx=10)
        
        # 布局Canvas和Scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=5)
        scrollbar.pack(side="right", fill="y")
        
        # 设置初始窗口大小和最大高度
        self.selector.update()
        content_height = scrollable_frame.winfo_reqheight()
        window_width = 300
        window_height = min(content_height + 20, 600)  # 最大高度600像素
        
        # 窗口居中
        screen_width = self.selector.winfo_screenwidth()
        screen_height = self.selector.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.selector.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 绑定鼠标滚轮事件
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def confirm(self):
        # 优先使用自定义输入
        custom_dir = self.custom_var.get().strip()
        if custom_dir:
            # 验证自定义输入格式
            if not custom_dir.startswith('_'):
                messagebox.showerror("格式错误", "自定义分类必须以_开头", parent=self.selector)
                return
            
            # 移除_前缀并获取分类名
            category_name = custom_dir[1:]
            
            # 验证首字母是否大写
            if not category_name[0].isupper():
                messagebox.showerror("格式错误", "分类名称首字母必须大写", parent=self.selector)
                return
            
            # 检查分类名是否已存在
            if category_name in dirs:
                messagebox.showerror("分类已存在", f"分类 '{category_name}' 已存在，请直接在上方选择或使用其他分类名", parent=self.selector)
                return
                
            # 添加新的分类名到dirs数组
            dirs.append(category_name)
            print(f"新增分类: {category_name}")
            
            self.selected_dir = category_name
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
        script_dir = r"I:\B-MioBlogSites\scripts"
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