$ErrorActionPreference = 'Stop'

$contentsDir = 'AndroidDeveloperGuideStory/Contents'
$tocFile = Get-ChildItem -Path $contentsDir -File -Filter '00-*.md' | Select-Object -First 1

if (-not $tocFile) {
  Write-Host "[TOC SYNC] skip: TOC file (00-*.md) not found"
  exit 0
}
$toc = $tocFile.FullName

$files = Get-ChildItem -Path $contentsDir -File -Filter '*.md' | Where-Object {
  $_.Name -ne $tocFile.Name -and $_.Name -notlike '*创作提示词.md'
}

$text = Get-Content -LiteralPath $toc -Raw -Encoding UTF8
$changed = $false

foreach ($f in $files) {
  $raw = Get-Content -LiteralPath $f.FullName -Raw -Encoding UTF8

  $status = ''
  if ($raw -match "(?ms)^---\s*\r?\n(?<fm>.*?)\r?\n---") {
    $fm = $Matches['fm']
    if ($fm -match '(?m)^status:\s*[''\"]?(?<s>[A-Za-z0-9_-]+)[''\"]?\s*$') {
      $status = $Matches['s'].ToLowerInvariant()
    }
  }

  $cb = if ($status -in 'done','published') { '[x]' } else { '[ ]' }
  $nameEsc = [regex]::Escape($f.Name)

  # 支持以下目录行：
  # - `xxx.md` — ...
  # - [ ] `xxx.md` — ...
  # - [x] `xxx.md` — ...
  $pattern = '(?m)^\s*-\s*(?:\[[ xX]\]\s*)?' + [regex]::Escape('`' + $f.Name + '`')
  $replacement = "- $cb " + '`' + $f.Name + '`'

  $newText = [regex]::Replace($text, $pattern, $replacement)
  if ($newText -ne $text) {
    $text = $newText
    $changed = $true
  }
}

if ($changed) {
  Set-Content -LiteralPath $toc -Value $text -Encoding UTF8
  Write-Host "[TOC SYNC] updated $toc"
} else {
  Write-Host "[TOC SYNC] no changes"
}
