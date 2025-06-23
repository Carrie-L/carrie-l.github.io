import subprocess
import os
import logging

# 创建空提交，当页面404时，执行这个git命令，使github actions重建

# 配置日志
LOG_FILE = r"I:\Z-logs\push_empty.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def push_empty_commit():
    try:
        git_dir = r"I:\B-MioBlogSites"
        
        # 设置环境变量
        env = os.environ.copy()
        env['HOME'] = os.path.expanduser('~')
        env['SSH_AUTH_SOCK'] = ''
        env['GIT_AUTHOR_NAME'] = 'Carrie-L'
        env['GIT_AUTHOR_EMAIL'] = '11453154+Carrie-L@users.noreply.github.com'
        env['GIT_COMMITTER_NAME'] = 'Carrie-L'
        env['GIT_COMMITTER_EMAIL'] = '11453154+Carrie-L@users.noreply.github.com'
        
        # Git 命令列表
        git_commands = [
            ['git', 'commit', '--allow-empty', '-m', "Trigger rebuild"],
            ['git', 'push', 'origin', 'main']
        ]
        
        for cmd in git_commands:
            logging.info(f'Executing: {" ".join(cmd)}')
            result = subprocess.run(
                cmd,
                cwd=git_dir,
                capture_output=True,
                text=True,
                encoding='utf-8',
                env=env
            )
            
            if result.stdout:
                logging.info(f'Output: {result.stdout}')
            if result.stderr:
                logging.error(f'Error: {result.stderr}')

            if result.returncode != 0:
                logging.error(f'Command failed: {" ".join(cmd)}')
                return False
        
        logging.info('Empty commit pushed successfully')
        return True
        
    except Exception as e:
        logging.error(f'Error: {str(e)}')
        return False

if __name__ == '__main__':
    push_empty_commit()