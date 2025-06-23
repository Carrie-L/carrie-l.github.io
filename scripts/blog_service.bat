@echo off
setlocal enabledelayedexpansion
set SCRIPT_PATH="I:\B-MioBlogSites\scripts\blog_monitor_service.py"

if "%1"=="install" (
    echo Installing Blog Monitor Service...
    sc delete BlogMonitorService >nul 2>&1
    python %SCRIPT_PATH% install
    echo Setting service to auto-start mode...
    sc config BlogMonitorService start= auto
    echo Service installed and set to auto-start.
    goto :eof
)

if "%1"=="remove" (
    echo Removing Blog Monitor Service...
    sc stop BlogMonitorService >nul 2>&1
    sc delete BlogMonitorService
    echo Service removed successfully.
    goto :eof
)

if "%1"=="status" (
    echo Checking service status...
    sc query BlogMonitorService
    goto :eof
)

if "%1"=="stop" (
    echo Stopping service...
    sc stop BlogMonitorService
    echo Service stopped.
    goto :eof
)

if "%1"=="start" (
    echo Starting service...
    sc start BlogMonitorService
    echo Service started.
    goto :eof
)

if "%1"=="restart" (
    echo Restarting service...
    sc stop BlogMonitorService
    timeout /t 2 /nobreak >nul
    sc start BlogMonitorService
    echo Service restarted.
    goto :eof
)

if "%1"=="logs" (
    echo Opening log file...
    start notepad "I:\Z-logs\blog_monitor_service.log"
    goto :eof
)

if "%1"=="push" (
    echo Executing empty commit...
    python "I:\B-MioBlogSites\scripts\push_empty.py"
    goto :eof
)

echo Blog Monitor Service Manager
echo ---------------------------
echo Usage:
echo   manage_service.bat install  - Install the service (auto-start)
echo   manage_service.bat remove   - Remove the service
echo   manage_service.bat start    - Start the service
echo   manage_service.bat stop     - Stop the service
echo   manage_service.bat restart  - Restart the service
echo   manage_service.bat status   - Check service status
echo   manage_service.bat logs     - View service logs
echo   manage_service.bat push     - Push empty commit to trigger rebuild
echo.
echo Note: Service will automatically start on system boot
echo       after installation.

endlocal