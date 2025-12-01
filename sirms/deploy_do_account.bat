@echo off
echo ========================================
echo Deploying DO Account Updates to Render
echo ========================================
echo.

git add -A
git commit -m "Add DO admin account for Render deployment"
git push origin main

echo.
echo ========================================
echo ✅ Pushed to Render!
echo ========================================
echo.
echo ⏳ Wait 5-10 minutes for deployment
echo.
echo 🔐 DO Account Credentials:
echo    Username: do_admin
echo    Password: do123
echo.
echo 🌐 Login at your Render URL
echo ========================================
pause
