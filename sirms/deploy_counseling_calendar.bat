@echo off
echo ========================================
echo Deploying Counseling Schedule Calendar
echo ========================================
echo.

cd sirms

echo Step 1: Adding changes to git...
git add templates/counseling_schedule.html
git status

echo.
echo Step 2: Committing changes...
git commit -m "Add calendar view to counseling schedule - matches DO schedule format"

echo.
echo Step 3: Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Render will automatically detect the changes and redeploy.
echo Check your Render dashboard for deployment status.
echo.
pause
