@echo off
echo ========================================
echo Deploying to Render...
echo ========================================
cd /d %~dp0
echo.
echo [1/3] Adding changes...
git add templates/base.html
echo.
echo [2/3] Committing changes...
git commit -m "Deploy: Guidance All Reports uses all_reports view matching DO"
echo.
echo [3/3] Pushing to GitHub...
git push origin main
echo.
echo ========================================
echo Deployment triggered!
echo ========================================
echo.
echo Render will automatically deploy your changes.
echo Check your Render dashboard for deployment status.
echo.
pause

