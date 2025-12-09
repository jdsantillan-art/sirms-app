@echo off
echo ========================================
echo Deploying Automatic Repeat Offender Detection
echo ========================================
echo.

echo Step 1: Adding files to git...
git add incidents/signals.py
git add incidents/apps.py
git add incidents/repeat_offender_utils.py
git add incidents/management/commands/detect_repeat_offenders.py
git add AUTO_REPEAT_OFFENDER_SYSTEM.md
git add deploy_auto_repeat_detection.bat

echo.
echo Step 2: Committing changes...
git commit -m "Add automatic repeat offender detection system"

echo.
echo Step 3: Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo Deployment initiated!
echo ========================================
echo.
echo Next steps:
echo 1. Wait for Render deployment to complete (~10-15 minutes)
echo 2. SSH into Render or use Render shell
echo 3. Run: python manage.py detect_repeat_offenders
echo 4. Verify badges appear on All Reports page
echo.
echo Press any key to exit...
pause > nul
