@echo off
echo ============================================
echo DEPLOYING FIXES TO RENDER
echo ============================================
echo.
echo Fixes included:
echo - Indentation error in views.py
echo - All reports template section name display
echo - Behavior concerns schedule functionality
echo.

git add .
git commit -m "Fix: Behavior concerns schedule + indentation error + all reports display"
git push origin main

echo.
echo ============================================
echo DEPLOYMENT PUSHED!
echo ============================================
echo.
echo Check Render dashboard for build status
echo URL: https://sirmsportal.onrender.com
echo.
pause
