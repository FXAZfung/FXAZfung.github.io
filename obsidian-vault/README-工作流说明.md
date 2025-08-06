# Obsidian + Hugo 自动化博客工作流

## 📋 概述
这个工作流允许您在Obsidian中写作，然后自动同步到Hugo博客并部署到GitHub Pages。

## 🚀 设置步骤

### 1. Obsidian配置
1. 在Obsidian中打开 `obsidian-vault` 文件夹作为vault
2. 安装以下插件：
   - **Obsidian Git** - 自动Git同步
   - **Templater** - 模板功能（可选）
   - **Natural Language Dates** - 日期处理（可选）

### 2. Git配置
1. 配置Obsidian Git插件：
   - 设置自动提交间隔：30分钟
   - 设置自动推送间隔：60分钟
   - 提交消息模板：`vault backup: {{date}}`

### 3. 写作流程
1. 使用模板创建新文章：`templates/blog-post-template.md`
2. 在 `blog-posts` 文件夹中写作
3. 文章完成后，将 `draft: true` 改为 `draft: false`
4. 保存文件，Obsidian Git会自动提交并推送
5. GitHub Actions会自动构建和部署

## 📁 目录结构
```
obsidian-vault/
├── blog-posts/          # 博客文章（已发布的）
├── drafts/              # 草稿文章
├── templates/           # 文章模板
└── .obsidian/          # Obsidian配置
```

## 📝 写作建议

### Front Matter 必需字段
```yaml
---
title: "文章标题"
date: 2025-08-06T12:00:00+08:00
draft: false  # 发布时改为false
tags: ["标签1", "标签2"]
categories: ["分类"]
description: "文章描述"
---
```

### 内容结构
1. 使用 `<!--more-->` 标记摘要结束
2. 合理使用标题层级（H1用于文章标题）
3. 图片放在 `static/images/` 目录下

## 🔄 自动化流程

### Obsidian → GitHub
1. Obsidian Git插件自动提交和推送
2. 或手动使用 `Ctrl+P` → `Obsidian Git: Commit all changes`

### GitHub → 部署
1. GitHub Actions检测到推送
2. 转换Obsidian文件到Hugo格式
3. 构建Hugo网站
4. 部署到GitHub Pages

## 🛠️ 手动操作命令

### Windows PowerShell
```powershell
# 转换Obsidian文件到Hugo
.\convert-obsidian-to-hugo.ps1

# 构建和预览
hugo server
```

### Linux/macOS
```bash
# 转换Obsidian文件到Hugo
./convert-obsidian-to-hugo.sh

# 构建和预览
hugo server
```

## 📱 移动端支持
- 使用 Obsidian 移动应用
- 配置Git同步（需要GitHub token）
- 支持离线写作，联网后自动同步

## 🔧 故障排除

### 常见问题
1. **图片不显示**：检查图片路径是否正确
2. **文章未发布**：确认 `draft: false`
3. **Git同步失败**：检查网络连接和GitHub token

### 检查构建状态
访问：https://github.com/FXAZfung/FXAZfung.github.io/actions

## 💡 高级功能

### 1. 自动标签生成
可以使用Obsidian插件根据内容自动生成标签

### 2. 图片优化
在转换脚本中添加图片压缩功能

### 3. 多语言支持
为不同语言创建不同的文件夹结构

---

**享受写作吧！🎉**
