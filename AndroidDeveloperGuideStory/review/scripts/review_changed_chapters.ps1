param(
  [ValidateSet('staged','range')]
  [string]$Mode = 'staged',
  [string]$Range = ''
)

$ErrorActionPreference = 'Stop'

function Get-ChangedFiles {
  param([string]$Mode,[string]$Range)

  # pre-commit (staged): check all modified/added chapter files
  # pre-push (range): only check NEWLY ADDED chapter files (A)
  # This prevents retroactive review of existing chapters during structural commits
  if ($Mode -eq 'staged') {
    $out = git -c core.quotepath=false diff --cached --name-only --diff-filter=ACMR
  } else {
    if ([string]::IsNullOrWhiteSpace($Range)) {
      $out = git -c core.quotepath=false diff --name-only --diff-filter=A origin/main...HEAD
    } else {
      $out = git -c core.quotepath=false diff --name-only --diff-filter=A $Range
    }
  }

  $normalized = @()
  foreach ($i in $out) {
    if (-not $i) { continue }
    $p = $i.Trim()
    if ($p.Length -eq 0) { continue }
    $p = $p.Trim('"')
    $p = $p -replace '\\','/'
    $normalized += $p
  }
  return $normalized
}

function Fail($msg) {
  Write-Host "[REVIEW FAIL] $msg" -ForegroundColor Red
  $script:HasFail = $true
}

$changed = Get-ChangedFiles -Mode $Mode -Range $Range

$chapterFiles = $changed | Where-Object {
  ($_ -match '^(?:workspace/)?AndroidDeveloperGuideStory/Contents/.+\.md$') -and
  ([System.IO.Path]::GetFileName($_) -match '^\d+\.\d+\.\d+\s+.+\.md$')
}

if (-not $chapterFiles -or $chapterFiles.Count -eq 0) {
  Write-Host '[REVIEW PASS] No chapter files changed.' -ForegroundColor Green
  exit 0
}

$HasFail = $false

foreach ($f in $chapterFiles) {
  if (-not (Test-Path -LiteralPath $f)) {
    Fail "${f}: file not found."
    continue
  }

  $txt = Get-Content -LiteralPath $f -Raw -Encoding UTF8

  # Skip published chapters (already reviewed and pushed)
  if ($txt -match '(?m)^status:\s*[''"]?published[''"]?\s*$') {
    Write-Host "[SKIP] $f (status=published, already reviewed)" -ForegroundColor DarkGray
    continue
  }

  # Skip skeleton/draft files — only review chapters with status: done
  if ($txt -notmatch '(?m)^status:\s*[''"]?done[''"]?\s*$') {
    Write-Host "[SKIP] $f (status != done, skeleton/draft file)" -ForegroundColor DarkGray
    continue
  }

  Write-Host "Checking $f ..."

  # --- YAML frontmatter gate ---
  if ($txt -notmatch "(?ms)^---\s*\r?\n.*chapter_id:.*\r?\n.*official_url:.*\r?\n.*status:.*\r?\n---") {
    Fail "${f}: YAML front matter missing required keys (chapter_id/official_url/status)."
  }

  # --- Body rule: no duplicate official-doc line ---
  $bodyDocPattern = [regex]::Escape([char]0x672C + [char]0x7BC7 + [char]0x5BF9 + [char]0x5E94 + [char]0x5B98 + [char]0x65B9 + [char]0x6587 + [char]0x6863)
  if ($txt -match $bodyDocPattern) {
    Fail "${f}: Body contains official-doc duplicate line (should stay in YAML only)."
  }

  # --- Must include technical summary section ---
  $techSummaryPattern = '###\s*' + [char]0x6280 + [char]0x672F + [char]0x603B + [char]0x7ED3
  if ($txt -notmatch $techSummaryPattern) {
    Fail "${f}: Missing technical summary section."
  }

  # --- Must include diary section ---
  $diaryPattern = '###\s*.*' + [char]0x6D1B + [char]0x8299 + [char]0x7684 + [char]0x5C0F + [char]0x5C0F + [char]0x65E5 + [char]0x8BB0 + [char]0x672C
  if ($txt -notmatch $diaryPattern) {
    Fail "${f}: Missing diary section."
  }

  # --- Must include practice section and >= 3 tasks ---
  $practicePattern = '###\s*.*' + [char]0x52A8 + [char]0x624B + [char]0x7EC3 + [char]0x4E60
  if ($txt -notmatch $practicePattern) {
    Fail "${f}: Missing practice section."
  }

  $taskMatches = [regex]::Matches($txt, '(?mi)\bTask\s*(\d+)\b')
  $taskNums = @{}
  foreach ($m in $taskMatches) { $taskNums[$m.Groups[1].Value] = $true }
  if ($taskNums.Keys.Count -lt 3) {
    Fail "${f}: Task count is less than 3 (found $($taskNums.Keys.Count))."
  }

  # --- Forbidden: 章节质量自检 must be deleted when all passed ---
  $selfCheckPattern = [char]0x7AE0 + [char]0x8282 + [char]0x8D28 + [char]0x91CF + [char]0x81EA + [char]0x68C0
  if ($txt -match $selfCheckPattern) {
    Fail "${f}: Contains 章节质量自检 section. Delete it when all items passed to keep content clean."
  }

  # --- plot_summary must exist in YAML frontmatter ---
  if ($txt -notmatch 'plot_summary:') {
    Fail "${f}: Missing plot_summary in YAML frontmatter (required for chapter continuity)."
  } else {
    $yamlBlock = ''
    if ($txt -match '(?ms)^---\s*\r?\n(.*?)\r?\n---') {
      $yamlBlock = $Matches[1]
    }
    if ($yamlBlock -and $yamlBlock -match 'plot_summary') {
      $missingFields = @()
      foreach ($field in @('time:', 'location:', 'season:')) {
        if ($yamlBlock -notmatch $field) { $missingFields += $field }
      }
      if ($missingFields.Count -gt 0) {
        Fail "${f}: plot_summary missing required fields: $($missingFields -join ', ')"
      }
    }
  }

  # --- Separator rule: fiction body must NOT contain --- ---
  # Only 3 allowed: before 专业技术总结, 动手练习, 学习建议. Fiction body = content before 专业技术总结.
  $techSummary = [char]0x4E13 + [char]0x4E1A + [char]0x6280 + [char]0x672F + [char]0x603B + [char]0x7ED3
  $afterYaml = $txt -replace '(?ms)^---\s*\r?\n.*?\r?\n---\s*\r?\n', '', 1
  $parts = $afterYaml -split "(?m)^##\s*$techSummary", 2
  if ($parts.Count -ge 2) {
    $fictionBody = $parts[0]
    if ($fictionBody -match '(?m)^\s*---\s*$') {
      Fail "${f}: Fiction body must NOT contain --- separator. Only 3 allowed: before 专业技术总结, 动手练习, 学习建议."
    }
  }

  # --- Encourage story > code (soft gate) ---
  $codeBlocks = [regex]::Matches($txt, '(?ms)``' + '`[\s\S]*?``' + '`').Count
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
