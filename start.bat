@echo off
title Klassbook AI
color 0A

echo.
echo  ========================================
echo    Klassbook AI - Starting App
echo  ========================================
echo.

:: Kill any existing processes on port 8080
echo [1/3] Cleaning up old processes...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8080" ^| findstr "LISTENING" 2^>nul') do (
    taskkill /F /PID %%a >nul 2>&1
)
timeout /t 1 /nobreak >nul

:: Build frontend
echo [2/4] Building frontend...
cd /d "%~dp0frontend"
if not exist "node_modules\" (
    echo Installing frontend dependencies...
    call npm install
)
echo Compiling frontend...
call npm run build

:: Copy frontend build to backend static folder
echo.
echo Copying frontend build to backend...
xcopy /s /e /y "%~dp0frontend\dist\*" "%~dp0backend\static\" >nul 2>&1

:: Navigate to backend
cd /d "%~dp0backend"

echo [3/4] Opening browser...
start http://localhost:8080

echo [4/4] Starting backend server...
echo.
echo  ========================================
echo    Klassbook AI is running!
echo    Frontend ^& Backend: http://localhost:8080
echo  ========================================
echo.
echo Press Ctrl+C to stop the server and close the app.
echo.

:: Start server
python -m uvicorn main:app --host 0.0.0.0 --port 8080 --workers 1
