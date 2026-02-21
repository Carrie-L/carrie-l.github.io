@echo off
setlocal

powershell -NoProfile -ExecutionPolicy Bypass -File AndroidDeveloperGuideStory/review/scripts/review_changed_chapters.ps1 -Mode range
if errorlevel 1 (
  echo pre-push blocked: chapter review failed.
  exit /b 1
)

exit /b 0
