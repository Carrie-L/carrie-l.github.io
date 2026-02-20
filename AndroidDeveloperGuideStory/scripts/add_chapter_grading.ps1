# Add volume_priority, volume_grade, chapter_importance to all chapter YAML frontmatter
# Based on: 《美少女的Android摇曳露营奇遇记》完整小说目录.md learning path

$ContentsDir = Join-Path $PSScriptRoot "..\Contents"
$ExcludeFiles = @("00-目录.md", "《美少女的Android摇曳露营奇遇记》创作提示词.md")

# Volume -> (priority, grade)
$VolumeMap = @{
    1 = @(8, 'A')   # 数据与文件
    2 = @(4, 'A')   # 权限
    3 = @(16, 'B')  # 用户身份
    4 = @(10, 'A')  # 导航
    5 = @(5, 'A')   # Intent
    6 = @(6, 'A')   # 后台任务
    7 = @(7, 'A')   # 服务
    8 = @(13, 'B')  # 闹钟
    9 = @(18, 'B')  # 音频和视频
    10 = @(17, 'B') # 摄像头
    11 = @(19, 'B') # 传感器
    12 = @(15, 'B') # 用户位置
    13 = @(14, 'B') # 连接
    14 = @(11, 'A') # 应用兼容性
    15 = @(12, 'A') # App Bundle
    16 = @(1, 'A')  # 编写与调试
    17 = @(2, 'A')  # 构建项目
    18 = @(3, 'A')  # 测试应用
    19 = @(9, 'A')  # 性能优化
    20 = @(20, 'B') # 命令行工具
    21 = @(21, 'B') # Gradle 插件 API
}

function Get-ChapterImportance {
    param([int]$Vol, [string]$ChapterId)
    $parts = $ChapterId -split '\.'
    $major = if ($parts.Length -ge 2) { [int]$parts[1] } else { 0 }
    $minor = if ($parts.Length -ge 3) { [int]$parts[2] } else { 0 }

    switch ($Vol) {
        1 { if ($major -le 7) { 5 } elseif ($major -le 12) { 3 } else { 4 } }
        2 { 5 }
        3 { if (($major -eq 1 -and $minor -eq 7) -or ($major -eq 1 -and $minor -eq 36)) { 5 } else { 3 } }
        4 { 5 }
        5 { 5 }
        6 {
            if ($major -eq 1) {
                if ($minor -ge 1 -and $minor -le 8) { 5 }
                elseif ($minor -ge 15 -and $minor -le 29) { 5 }
                else { 3 }
            } else { 3 }
        }
        7 {
            if ($major -eq 1) {
                if ($minor -in @(1, 3, 4)) { 5 } else { 3 }
            } else { 3 }
        }
        8 { 3 }
        9 { 3 }
        10 { 3 }
        11 { 3 }
        12 { 3 }
        13 { if ($major -eq 1 -and $minor -in @(1, 2)) { 5 } else { 3 } }
        14 { 5 }
        15 { 5 }
        16 { if ($major -eq 1 -or $major -eq 2) { 5 } else { 4 } }
        17 {
            if ($major -eq 1 -and $minor -le 30) { 5 }
            else { 3 }
        }
        18 { 5 }
        19 {
            if ($major -eq 1) {
                if ($minor -in @(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 19, 20)) { 5 }
                else { 3 }
            } else { 3 }
        }
        20 { 3 }
        21 { 3 }
        default { 4 }
    }
}

$files = Get-ChildItem -Path $ContentsDir -Filter "*.md" -File | Where-Object { $_.Name -notin $ExcludeFiles }
$count = 0
$updated = 0

foreach ($f in $files) {
    $count++
    $content = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
    if ($content -match 'volume_priority:') {
        continue
    }
    $chapterId = $null
    if ($content -match "chapter_id:\s*'([^']+)'") {
        $chapterId = $Matches[1]
    } elseif ($f.Name -match '^(\d+\.\d+(?:\.\d+)?)[\s\-\.]') {
        $chapterId = $Matches[1]
    } else {
        continue
    }
    $volMatch = $chapterId -match '^(\d+)\.'
    if (-not $volMatch) { continue }
    $vol = [int]$Matches[1]
    if ($vol -lt 1 -or $vol -gt 21) { continue }

    $map = $VolumeMap[$vol]
    if (-not $map) { continue }
    $priority = $map[0]
    $grade = $map[1]
    $importance = Get-ChapterImportance -Vol $vol -ChapterId $chapterId

    $newFields = @"

volume_priority: $priority
volume_grade: '$grade'
chapter_importance: $importance
"@

    $newContent = $content
    if ($content -match 'plot_summary:') {
        $newContent = $content -replace '(\r?\n)(plot_summary:)', "$newFields`n`$1`$2"
    } else {
        $newContent = $content -replace '(?s)^(---\r?\n.*?)(\r?\n---\r?\n)', "`$1$newFields`n`$2"
    }
    if ($newContent -eq $content) { continue }

    [System.IO.File]::WriteAllText($f.FullName, $newContent, [System.Text.UTF8Encoding]::new($false))
    $updated++
    if ($updated -le 5) {
        Write-Host "Updated: $($f.Name) -> priority=$priority grade=$grade importance=$importance"
    }
}

Write-Host "Processed $count files, updated $updated"
