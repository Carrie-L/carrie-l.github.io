@echo off
setlocal enabledelayedexpansion
set SCRIPT_PATH="I:\B-MioBlogSites\blog_monitor_service.py"

:: 调试参数
echo Received parameter: [%1]

if /i "%~1"=="install" (
    echo Installing Blog Monitor Service...
    sc delete BlogMonitorService >nul 2>&1
    python %SCRIPT_PATH% install
    echo Setting service to auto-start mode...
    sc config BlogMonitorService start= auto
    echo.
    echo Service installed and set to auto-start.
    goto :eof
)

if /i "%~1"=="remove" (
    echo Stopping service...
    sc stop BlogMonitorService >nul 2>&1
    timeout /t 2 /nobreak >nul
    echo Removing Blog Monitor Service...
    sc delete BlogMonitorService
    if %errorlevel% neq 0 (
        echo Failed to delete the service.
        goto :eof
    )
    echo Service removed successfully.
    goto :eof
)

if /i "%~1"=="status" (
    echo Checking service status...
    sc query BlogMonitorService
    goto :eof
)

if /i "%~1"=="stop" (
    echo Stopping service...
    sc stop BlogMonitorService
    echo Service stopped.
    goto :eof
)

if /i "%~1"=="start" (
    echo Starting service...
    sc start BlogMonitorService
    echo Service started.
    goto :eof
)

if /i "%~1"=="restart" (
    echo Restarting service...
    sc stop BlogMonitorService
    timeout /t 2 /nobreak >nul
    sc start BlogMonitorService
    echo Service restarted.
    goto :eof
)

if /i "%~1"=="logs" (
    echo Opening log file...
    start notepad "I:\B-MioBlogSites\monitor_service.log"
    goto :eof
)

echo Blog Monitor Service Manager
echo ---------------------------
echo Unknown command: [%1]
echo Usage:
echo   manage_service.bat install  - Install the service (auto-start)
echo   manage_service.bat remove   - Remove the service
echo   manage_service.bat start    - Start the service
echo   manage_service.bat stop     - Stop the service
echo   manage_service.bat restart  - Restart the service
echo   manage_service.bat status   - Check service status
echo   manage_service.bat logs     - View service logs
echo.
echo Note: Service will automatically start on system boot
echo       after installation. You can also manage the service
echo       using Windows Services (services.msc)

endlocal
