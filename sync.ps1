param (
    [Parameter(Mandatory = $true)]
    [string]$BranchName,

    [Parameter(Mandatory = $true)]
    [string]$CommitMsg
)

# 临时设置输出编码，以防中文乱码
[console]::InputEncoding = [console]::OutputEncoding = New-Object System.Text.UTF8Encoding

Write-Host ">>> 1. 确保在正确的专属分支 ($BranchName)..." -ForegroundColor Cyan
git checkout $BranchName

Write-Host ">>> 2. 提交当前改动..." -ForegroundColor Cyan
git add .
git commit -m $CommitMsg

# 检查提交是否成功，以兼容门禁（pre-commit hook）审查机制
if ($LASTEXITCODE -ne 0) {
    Write-Host ">>> [错误] 提交失败！可能是未通过预提交审查门禁（pre-commit hook）。" -ForegroundColor Red
    Write-Host ">>> 请根据上方的报错信息修正代码后，重新运行同步脚本。" -ForegroundColor Yellow
    exit 1
}

git push origin $BranchName

Write-Host ">>> 3. 切到 main 分支并拉取最新代码..." -ForegroundColor Cyan
git checkout main
git pull origin main

Write-Host ">>> 4. 将 $BranchName 合并到 main..." -ForegroundColor Cyan
git merge $BranchName --no-ff -m "Merge branch '$BranchName' into main"

# 检查合并是否遇到冲突
if ($LASTEXITCODE -ne 0) {
    Write-Host ">>> [警告] 合并遇到冲突！请手动解决冲突后执行:" -ForegroundColor Red
    Write-Host "    git add ." -ForegroundColor Yellow
    Write-Host "    git commit" -ForegroundColor Yellow
    Write-Host "    git push origin main" -ForegroundColor Yellow
    Write-Host "    git checkout $BranchName" -ForegroundColor Yellow
    exit 1
}

Write-Host ">>> 5. 推送 main 分支..." -ForegroundColor Cyan
git push origin main

Write-Host ">>> 6. 切回 $BranchName 分支待命..." -ForegroundColor Cyan
git checkout $BranchName

Write-Host ">>> 同步流程全部完成！" -ForegroundColor Green
