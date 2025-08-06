# Obsidian + Hugo 同步脚本（高级版本）
# 支持图片处理、标签自动化等功能

import os
import re
import shutil
import yaml
from datetime import datetime
from pathlib import Path

class ObsidianHugoSync:
    def __init__(self, obsidian_dir="./obsidian-vault", hugo_dir="./content/post"):
        self.obsidian_dir = Path(obsidian_dir)
        self.hugo_dir = Path(hugo_dir)
        self.blog_posts_dir = self.obsidian_dir / "blog-posts"
        
    def process_images(self, content, source_file):
        """处理图片链接，从Obsidian格式转换为Hugo格式"""
        # Obsidian: ![[image.png]]
        # Hugo: ![](images/image.png)
        
        obsidian_images = re.findall(r'!\[\[(.*?)\]\]', content)
        for img in obsidian_images:
            # 复制图片到static/images目录
            src_img = self.obsidian_dir / img
            if src_img.exists():
                dst_img = Path("static/images") / img
                dst_img.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_img, dst_img)
                
                # 替换链接格式
                content = content.replace(f'![[{img}]]', f'![](/images/{img})')
        
        return content
    
    def process_front_matter(self, content):
        """处理和验证Front Matter"""
        if not content.startswith('---'):
            return content
            
        try:
            parts = content.split('---', 2)
            if len(parts) < 3:
                return content
                
            front_matter = yaml.safe_load(parts[1])
            
            # 确保必需字段存在
            if 'date' not in front_matter:
                front_matter['date'] = datetime.now().isoformat()
            
            if 'title' not in front_matter:
                front_matter['title'] = "未命名文章"
            
            # 重新构建内容
            new_front_matter = yaml.dump(front_matter, allow_unicode=True, default_flow_style=False)
            return f"---\n{new_front_matter}---{parts[2]}"
            
        except Exception as e:
            print(f"处理Front Matter时出错: {e}")
            return content
    
    def sync_files(self):
        """同步文件从Obsidian到Hugo"""
        if not self.blog_posts_dir.exists():
            print("Obsidian博客文章目录不存在")
            return
            
        for md_file in self.blog_posts_dir.glob("*.md"):
            print(f"处理文件: {md_file.name}")
            
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否为草稿
            if 'draft: true' in content:
                print(f"跳过草稿: {md_file.name}")
                continue
            
            # 处理内容
            content = self.process_front_matter(content)
            content = self.process_images(content, md_file)
            
            # 保存到Hugo目录
            dst_file = self.hugo_dir / md_file.name
            with open(dst_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"已同步: {md_file.name}")

if __name__ == "__main__":
    syncer = ObsidianHugoSync()
    syncer.sync_files()
    print("同步完成！")
