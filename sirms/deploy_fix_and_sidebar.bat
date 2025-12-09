@echo off
echo ========================================
echo Deploying Sidebar Cleanup + Build Fix
echo ========================================
echo.

echo Adding changes to git...
git add templates/base.html
git add static/images/
git add .

echo.
echo Committing changes...
git commit -m "Fix build error and remove sidebar items: Remove README.md from static/images causing WhiteNoise error, remove Dashboard from ESP Teacher, Advisee Records and Legal References from Teacher, Legal References from Student"

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
echo Changes:
echo   - Fixed: Removed README.md from static/images (was causing build error)
echo   - Removed: Dashboard from ESP Teacher sidebar
echo   - Removed: Advisee Records from Teacher sidebar
echo   - Removed: Legal References from Teacher sidebar
echo   - Removed: Legal References from Student sidebar
echo.
pause
