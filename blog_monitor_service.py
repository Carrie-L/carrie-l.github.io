import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
import subprocess
from datetime import datetime

# 配置日志
LOG_FILE = r"I:\B-MioBlogSites\monitor_service.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class FolderMonitor(FileSystemEventHandler):
    def __init__(self):
        self.script_path = r"I:\B-MioBlogSites\auto_update.py"
        self.git_dir = r"I:\B-MioBlogSites"
        self.last_run_time = 0
        self.cooldown = 5
        self.python_path = r"C:\Users\windows\AppData\Local\Programs\Python\Python312\python.exe"
        
    def git_commit_and_push(self):
        """执行Git提交和推送操作"""
        try:
            # 确保在 main 分支
            subprocess.run(['git', 'checkout', 'main'], cwd=self.git_dir, capture_output=True, text=True, encoding='utf-8')
            
            # 获取当前时间作为提交信息
            commit_message = f"Auto update at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # 设置环境变量
            env = os.environ.copy()
            env['HOME'] = os.path.expanduser('~')
            env['SSH_AUTH_SOCK'] = ''
            
            # Git 命令列表
            git_commands = [
                ['git', 'add', '.'],
                ['git', 'commit', '-m', commit_message],
                ['git', 'pull', '--no-rebase', 'origin', 'main'],
                ['git', 'push', 'origin', 'main']
            ]
            
            # 执行Git命令
            for cmd in git_commands:
                logging.info(f'Executing Git command: {" ".join(cmd)}')
                result = subprocess.run(
                    cmd,
                    cwd=self.git_dir,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    env=env
                )
                
                if result.stdout:
                    logging.info(f'Git output: {result.stdout}')
                if result.stderr and 'warning:' not in result.stderr.lower():
                    logging.error(f'Git error: {result.stderr}')
                    
                if result.returncode != 0:
                    if 'nothing to commit' in result.stdout + result.stderr:
                        logging.info('Nothing to commit, continuing...')
                        continue
                    logging.error(f'Git command failed: {" ".join(cmd)}')
                    return False
            
            logging.info('Git commit and push completed successfully')
            return True
            
        except Exception as e:
            logging.error(f'Error in Git operations: {str(e)}')
            import traceback
            logging.error(f'Traceback:\n{traceback.format_exc()}')
            return False

    def execute_update(self):
        try:
            logging.info('Starting auto_update.py execution...')
            
            # 设置环境变量
            env = os.environ.copy()
            env['PYTHONPATH'] = os.path.dirname(self.script_path)
            env['HOME'] = os.path.expanduser('~')
            
            # 记录执行信息
            logging.info(f'Using Python: {self.python_path}')
            logging.info(f'Script path: {self.script_path}')
            logging.info(f'Working directory: {os.path.dirname(self.script_path)}')
            
            # 执行脚本
            result = subprocess.run(
                [self.python_path, self.script_path],
                capture_output=True,
                text=True,
                encoding='utf-8',
                cwd=os.path.dirname(self.script_path),
                env=env
            )
            
            # 记录输出
            if result.stdout:
                logging.info(f'Script stdout:\n{result.stdout}')
            if result.stderr:
                logging.error(f'Script stderr:\n{result.stderr}')
                
            if result.returncode == 0:
                logging.info('Script executed successfully')
                # 如果脚本执行成功，进行Git操作
                self.git_commit_and_push()
            else:
                logging.error(f'Script failed with return code: {result.returncode}')
            
        except Exception as e:
            logging.error(f'Error executing auto_update.py: {str(e)}')
            import traceback
            logging.error(f'Traceback:\n{traceback.format_exc()}')

    def on_created(self, event):
        if event.is_directory:
            return
            
        current_time = time.time()
        if current_time - self.last_run_time < self.cooldown:
            logging.info('In cooldown period, skipping execution')
            return
            
        self.last_run_time = current_time
        logging.info(f'Detected new file: {event.src_path}')
        self.execute_update()

class BlogMonitorService(win32serviceutil.ServiceFramework):
    _svc_name_ = "BlogMonitorService"
    _svc_display_name_ = "Blog Monitor Service"
    _svc_description_ = "Monitor blog folders and run auto_update.py when files change"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.observer = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        if self.observer:
            self.observer.stop()
        logging.info('Service stopping...')

    def SvcDoRun(self):
        try:
            logging.info('Service starting...')
            self.main()
        except Exception as e:
            logging.error(f'Service error: {str(e)}')
            import traceback
            logging.error(f'Traceback:\n{traceback.format_exc()}')
            self.SvcStop()

    def main(self):
        folders_to_monitor = [
            r"I:\B-MioBlogSites\_English",
            r"I:\B-MioBlogSites\_Algorithm",
            r"I:\B-MioBlogSites\_Android",
            r"I:\B-MioBlogSites\_DSA"
        ]

        # 验证文件夹
        for folder in folders_to_monitor:
            if not os.path.exists(folder):
                logging.error(f'Folder not found: {folder}')
                return

        # 创建监控器
        event_handler = FolderMonitor()
        self.observer = Observer()

        for folder in folders_to_monitor:
            self.observer.schedule(event_handler, folder, recursive=False)
            logging.info(f'Monitoring folder: {folder}')

        self.observer.start()
        logging.info('Monitor started successfully')

        while True:
            if win32event.WaitForSingleObject(self.stop_event, 1000) == win32event.WAIT_OBJECT_0:
                break

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(BlogMonitorService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(BlogMonitorService)