@echo off
echo Deploying to Render...
git add .
git commit -m "Fix indentation error and update all_reports template"
git push origin main
echo.
echo Deployment pushed! Check Render dashboard.
pause
