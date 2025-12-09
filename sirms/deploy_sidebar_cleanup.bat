@echo off
echo ========================================
echo Deploying Sidebar Cleanup Changes
echo ========================================
echo.

echo Adding changes to git...
git add templates/base.html

echo.
echo Committing changes...
git commit -m "Remove sidebar items: Dashboard from ESP Teacher, Advisee Records and Legal References from Teacher, Legal References from Student"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Render will auto-deploy in 5-10 minutes.
echo Check: https://dashboard.render.com
echo.
pause
