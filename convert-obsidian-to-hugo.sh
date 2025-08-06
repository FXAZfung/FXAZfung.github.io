#!/bin/bash

# Obsidian到Hugo的文件转换脚本
# 用法: ./convert-obsidian-to-hugo.sh

OBSIDIAN_DIR="./obsidian-vault/blog-posts"
HUGO_CONTENT_DIR="./content/post"

echo "开始转换Obsidian文件到Hugo格式..."

# 检查目录是否存在
if [ ! -d "$OBSIDIAN_DIR" ]; then
    echo "错误: Obsidian目录不存在: $OBSIDIAN_DIR"
    exit 1
fi

if [ ! -d "$HUGO_CONTENT_DIR" ]; then
    echo "错误: Hugo内容目录不存在: $HUGO_CONTENT_DIR"
    exit 1
fi

# 遍历Obsidian博客文章目录
for file in "$OBSIDIAN_DIR"/*.md; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        
        # 检查文件是否已经是发布状态（不是draft）
        if grep -q "draft: false" "$file" || ! grep -q "draft: true" "$file"; then
            echo "处理文件: $filename"
            
            # 复制文件到Hugo内容目录
            cp "$file" "$HUGO_CONTENT_DIR/"
            
            echo "已复制: $filename"
        else
            echo "跳过草稿文件: $filename"
        fi
    fi
done

echo "转换完成!"
