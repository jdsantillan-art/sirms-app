@echo off
echo ============================================
echo RUNNING MIGRATIONS FOR PROPER PROCESS SYSTEM
echo ============================================
echo.

echo Step 1: Creating migrations...
python manage.py makemigrations

echo.
echo Step 2: Applying migrations...
python manage.py migrate

echo.
echo ============================================
echo MIGRATIONS COMPLETE!
echo ============================================
echo.
echo Next steps:
echo 1. Update report form template
echo 2. Update report view
echo 3. Test the system
echo.
echo See IMPLEMENTATION_STEPS_NOW.md for details
echo.
pause
