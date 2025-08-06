# Obsidian到Hugo的文件转换脚本 (PowerShell版本)
# 用法: .\convert-obsidian-to-hugo.ps1

$ObsidianDir = ".\obsidian-vault\blog-posts"
$HugoContentDir = ".\content\post"

Write-Host "开始转换Obsidian文件到Hugo格式..." -ForegroundColor Green

# 检查目录是否存在
if (!(Test-Path $ObsidianDir)) {
    Write-Host "错误: Obsidian目录不存在: $ObsidianDir" -ForegroundColor Red
    exit 1
}

if (!(Test-Path $HugoContentDir)) {
    Write-Host "错误: Hugo内容目录不存在: $HugoContentDir" -ForegroundColor Red
    exit 1
}

# 遍历Obsidian博客文章目录
Get-ChildItem -Path $ObsidianDir -Filter "*.md" | ForEach-Object {
    $file = $_.FullName
    $filename = $_.Name
    
    # 读取文件内容
    $content = Get-Content $file -Raw
    
    # 检查文件是否已经是发布状态（不是draft）
    if ($content -match "draft:\s*false" -or $content -notmatch "draft:\s*true") {
        Write-Host "处理文件: $filename" -ForegroundColor Yellow
        
        # 复制文件到Hugo内容目录
        Copy-Item $file -Destination $HugoContentDir
        
        Write-Host "已复制: $filename" -ForegroundColor Green
    } else {
        Write-Host "跳过草稿文件: $filename" -ForegroundColor Gray
    }
}

Write-Host "转换完成!" -ForegroundColor Green
