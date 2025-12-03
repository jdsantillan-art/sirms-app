@echo off
echo ============================================================
echo ESP TEACHER SYSTEM - RENDER DEPLOYMENT
echo ============================================================
echo.
echo This script will deploy the ESP Teacher feature to Render
echo.

REM Check if git is available
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git and try again
    pause
    exit /b 1
)

echo Step 1: Checking Git Status...
echo.
git status
echo.

echo Step 2: Adding all changes...
git add .
echo.

echo Step 3: Committing changes...
git commit -m "Deploy ESP Teacher Management System - Dec 4, 2025

Features:
- Manage ESP Teachers (add/edit/deactivate up to 5)
- For VPF page with assignment functionality
- ESP teacher dropdown with full information display
- Email format: lastnameespteacher@gmail.com
- Phone format: 09XX XXX XXXX
- Complete documentation (6 comprehensive guides)
- Tested and verified locally

Files Added:
- incidents/esp_teacher_views.py
- templates/counselor/manage_esp_teachers.html
- templates/counselor/esp_teacher_form.html
- templates/counselor/assign_esp_teacher.html
- populate_esp_teachers.py
- test_esp_teacher_system.py
- ESP_TEACHER_*.md (documentation)

Files Modified:
- incidents/urls.py (ESP teacher routes)
- templates/counselor/for_vpf.html (updated)
"
echo.

if errorlevel 1 (
    echo.
    echo WARNING: Commit failed or no changes to commit
    echo This might be because changes were already committed
    echo.
)

echo Step 4: Pushing to GitHub...
echo.
git push origin main
echo.

if errorlevel 1 (
    echo.
    echo ERROR: Push failed!
    echo Please check your internet connection and GitHub credentials
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo DEPLOYMENT INITIATED SUCCESSFULLY!
echo ============================================================
echo.
echo Render will now automatically:
echo   1. Detect the push
echo   2. Pull latest code
echo   3. Run build.sh
echo   4. Install dependencies
echo   5. Run migrations
echo   6. Deploy the application
echo.
echo Expected deployment time: 10-15 minutes
echo.
echo Next Steps:
echo   1. Go to Render Dashboard: https://dashboard.render.com
echo   2. Monitor the deployment progress
echo   3. Wait for "Live" status
echo   4. Run: python populate_esp_teachers.py (in Render Shell)
echo   5. Test the system in your browser
echo.
echo URLs to test after deployment:
echo   - /manage-esp-teachers/
echo   - /for-vpf/
echo   - /esp-teacher/add/
echo.
echo ============================================================
echo.
pause
