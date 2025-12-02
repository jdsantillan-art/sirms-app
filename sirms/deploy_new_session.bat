@echo off
echo Killing stuck Python processes...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting deployment in new session...
start cmd /k "cd /d %~dp0 && git add . && git commit -m "Fix: Behavior concerns schedule + indentation + template" && git push origin main && echo. && echo DEPLOYMENT PUSHED! && echo Check Render dashboard && pause"
