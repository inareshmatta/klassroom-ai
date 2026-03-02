@echo off
echo ========================================
echo   KlassroomAI - Starting Backend
echo ========================================

:: Kill any existing uvicorn/python processes on port 8080
echo Killing previous instances on port 8080...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8080" ^| findstr "LISTENING"') do (
    echo   Killing PID %%a
    taskkill /F /PID %%a >nul 2>&1
)
timeout /t 1 /nobreak >nul

:: Navigate to backend
cd /d d:\KlassroomAI\backend

:: Start the server
echo.
echo Starting KlassroomAI backend on http://localhost:8080
echo Press Ctrl+C to stop.
echo ========================================
python -m uvicorn main:app --host 0.0.0.0 --port 8080 --workers 1
