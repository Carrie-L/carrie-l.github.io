param(
  [ValidateSet('staged','range')]
  [string]$Mode = 'staged',
  [string]$Range = '',
  [switch]$Legacy  # Skip newer checks for legacy chapters
)

$ErrorActionPreference = 'Stop'

function Get-ChangedFiles {
  param([string]$Mode,[string]$Range)
  if ($Mode -eq 'staged') {
    $out = git diff --cached --name-only --diff-filter=ACMR
  } else {
    if ([string]::IsNullOrWhiteSpace($Range)) {
      $out = git diff --name-only --diff-filter=ACMR origin/main...HEAD
    } else {
      $out = git diff --name-only --diff-filter=ACMR $Range
    }
  }
  return @($out | Where-Object { $_ -and $_.Trim() -ne '' })
}

function Fail($msg) {
  Write-Host "[REVIEW FAIL] $msg" -ForegroundColor Red
  $script:HasFail = $true
}

$changed = Get-ChangedFiles -Mode $Mode -Range $Range
$chapterFiles = $changed | Where-Object {
  $_ -like 'AndroidDeveloperGuideStory/Contents/*.md' -and
  $_ -notlike 'AndroidDeveloperGuideStory/Contents/00-目录.md' -and
  $_ -notlike 'AndroidDeveloperGuideStory/Contents/*创作提示词.md'
}

if (-not $chapterFiles -or $chapterFiles.Count -eq 0) {
  Write-Host '[REVIEW PASS] No chapter files changed.' -ForegroundColor Green
  exit 0
}

$HasFail = $false

foreach ($f in $chapterFiles) {
  if (-not (Test-Path $f)) { continue }
  $txt = Get-Content -LiteralPath $f -Raw -Encoding UTF8

  Write-Host "Checking $f ..."

  # Basic YAML gate
  if ($txt -notmatch "(?ms)^---\s*\n.*chapter_id:.*\n.*official_url:.*\n.*status:.*\n---") {
    Fail "${f}: YAML front matter missing required keys (chapter_id/official_url/status)."
  }

  # Plot summary required (time + location)
  if ($txt -notmatch "(?ms)^---\s*\n.*plot_summary:") {
    Fail "${f}: YAML missing plot_summary (time/location)."
  }

  # Body rule: no duplicate official-doc line (skip in legacy mode)
  if (-not $Legacy -and $txt -match '本篇对应官方文档') {
    Fail "${f}: Body contains '本篇对应官方文档' (should stay in YAML only)."
  }

  # Must include technical summary and diary sections (skip in legacy mode)
  if (-not $Legacy) {
    if ($txt -notmatch '###\s*技术总结') {
      Fail "${f}: Missing '### 技术总结' section."
    }
    if ($txt -notmatch '###\s*🍭\s*洛芙的小小日记本') {
      Fail "${f}: Missing diary section."
    }
  }

  # Must include practice section and >= 3 tasks (skip in legacy mode)
  if (-not $Legacy -and $txt -notmatch '###\s*🏕️\s*动手练习') {
    Fail "${f}: Missing practice section (### 🏕️ 动手练习)."
  }

  if (-not $Legacy) {
    $taskMatches = [regex]::Matches($txt, '(?mi)\bTask\s*(\d+)\b')
    $taskNums = @{}
    foreach ($m in $taskMatches) { $taskNums[$m.Groups[1].Value] = $true }
    if ($taskNums.Keys.Count -lt 3) {
      Fail "${f}: Task count is less than 3 (found $($taskNums.Keys.Count))."
    }
  }

  # Forbidden old section
  if ($txt -match '质量自检清单') {
    Fail "${f}: Contains forbidden section '质量自检清单'."
  }

  # Encourage story > code (soft gate with threshold)
  $codeBlocks = [regex]::Matches($txt, '(?ms)```[\s\S]*?```').Count
  $chars = $txt.Length
  if ($codeBlocks -gt 20 -and $chars -lt 12000) {
    Fail "${f}: Likely over-technical (too many code blocks for current length)."
  }
}

if ($HasFail) {
  Write-Host "`nREVIEW_RESULT: FAIL" -ForegroundColor Red
  Write-Host 'Commit/Push blocked by chapter gate.' -ForegroundColor Red
  exit 1
}

Write-Host "`nREVIEW_RESULT: PASS" -ForegroundColor Green
exit 0
