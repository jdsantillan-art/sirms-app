@echo off
cls
echo ============================================
echo DEPLOYING TO RENDER
echo ============================================
echo.

git add .
git commit -m "Deploy to Render - Dec 2" --allow-empty
git push origin main

echo.
echo ============================================
echo DEPLOYMENT COMPLETE!
echo ============================================
echo.
echo Check Render dashboard for build status
echo URL: https://sirmsportal.onrender.com
echo.
