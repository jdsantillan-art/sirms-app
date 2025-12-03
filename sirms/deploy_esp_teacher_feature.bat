@echo off
echo ========================================
echo ESP Teacher Management Feature Deployment
echo ========================================
echo.

echo Step 1: Running populate_esp_teachers.py...
python populate_esp_teachers.py
if errorlevel 1 (
    echo ERROR: Failed to populate ESP teachers
    pause
    exit /b 1
)
echo.

echo Step 2: Collecting static files...
python manage.py collectstatic --noinput
echo.

echo Step 3: Adding changes to git...
git add .
echo.

echo Step 4: Committing changes...
git commit -m "Add ESP Teacher Management Feature - Manage 5 ESP teachers and assign to VPF cases"
echo.

echo Step 5: Pushing to repository...
git push origin main
if errorlevel 1 (
    echo WARNING: Git push failed. You may need to pull first or resolve conflicts.
    echo Try: git pull origin main
    pause
)
echo.

echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Features Added:
echo - Manage ESP Teachers (max 5)
echo - Add/Edit/Delete ESP Teachers
echo - Assign ESP Teachers to VPF Cases
echo - View For VPF page with pending assignments
echo.
echo Next Steps:
echo 1. Access "Manage ESP Teachers" from counselor dashboard
echo 2. Add up to 5 ESP teachers with contact info
echo 3. Go to "For VPF" to assign teachers to VPF cases
echo.
pause
