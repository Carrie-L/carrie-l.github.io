@echo off
setlocal

powershell -NoProfile -ExecutionPolicy Bypass -File AndroidDeveloperGuideStory/review/scripts/sync_toc_status.ps1
if errorlevel 1 (
  echo pre-commit blocked: TOC sync failed.
  exit /b 1
)

git add -- "AndroidDeveloperGuideStory/Contents/00-*.md" >nul 2>nul

powershell -NoProfile -ExecutionPolicy Bypass -File AndroidDeveloperGuideStory/review/scripts/review_changed_chapters.ps1 -Mode staged
if errorlevel 1 (
  echo pre-commit blocked: chapter review failed.
  exit /b 1
)

exit /b 0
