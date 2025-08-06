# 文件监控脚本 - 自动检测Obsidian文件变化
# 需要安装: pip install watchdog

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os

class ObsidianHandler(FileSystemEventHandler):
    def __init__(self, script_path):
        self.script_path = script_path
        self.last_sync = 0
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        if event.src_path.endswith('.md'):
            # 防止频繁触发，至少间隔30秒
            current_time = time.time()
            if current_time - self.last_sync > 30:
                print(f"检测到文件变化: {event.src_path}")
                self.sync_and_deploy()
                self.last_sync = current_time
    
    def sync_and_deploy(self):
        """同步文件并触发部署"""
        try:
            # 运行同步脚本
            subprocess.run(['python', self.script_path], check=True)
            
            # Git提交和推送
            subprocess.run(['git', 'add', '.'], check=True)
            subprocess.run(['git', 'commit', '-m', f'Auto sync from Obsidian at {time.strftime("%Y-%m-%d %H:%M:%S")}'], check=True)
            subprocess.run(['git', 'push'], check=True)
            
            print("自动同步和部署成功！")
            
        except subprocess.CalledProcessError as e:
            print(f"同步失败: {e}")

def start_monitoring(obsidian_path, sync_script):
    """开始监控Obsidian文件夹"""
    event_handler = ObsidianHandler(sync_script)
    observer = Observer()
    observer.schedule(event_handler, obsidian_path, recursive=True)
    observer.start()
    
    try:
        print(f"开始监控 {obsidian_path}")
        print("按 Ctrl+C 停止监控")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("停止监控")
    
    observer.join()

if __name__ == "__main__":
    obsidian_path = "./obsidian-vault/blog-posts"
    sync_script = "./obsidian-hugo-sync.py"
    
    if os.path.exists(obsidian_path):
        start_monitoring(obsidian_path, sync_script)
    else:
        print(f"Obsidian路径不存在: {obsidian_path}")
