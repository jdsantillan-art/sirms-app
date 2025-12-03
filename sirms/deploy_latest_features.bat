@echo off
echo ========================================
echo DEPLOYING LATEST FEATURES TO RENDER
echo ========================================
echo.
echo Features being deployed:
echo - Email notifications (Brevo SMTP)
echo - Report submission fix (fast + no duplicates)
echo - Counselor login fix (VPFCase error)
echo - DO Schedule calendar view
echo.
echo ========================================
echo.

echo Step 1: Checking Git status...
git status
echo.

echo Step 2: Adding all changes...
git add .
echo.

echo Step 3: Committing changes...
git commit -m "Deploy latest features: Email notifications, Report submission fix, Counselor login fix, DO Schedule calendar view"
echo.

echo Step 4: Pushing to GitHub...
git push origin main
echo.

echo ========================================
echo DEPLOYMENT INITIATED!
echo ========================================
echo.
echo Render will automatically deploy in 2-5 minutes.
echo.
echo What was deployed:
echo   ✅ Email notifications with Brevo
echo   ✅ Fast report submission (no duplicates)
echo   ✅ Counselor dashboard fix
echo   ✅ DO Schedule calendar + list view
echo.
echo Monitor deployment:
echo   https://dashboard.render.com
echo.
echo ========================================
pause
