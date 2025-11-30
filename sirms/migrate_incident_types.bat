@echo off
echo ========================================
echo Migrating Incident Types Classification
echo ========================================
echo.

echo Step 1: Making migrations...
python manage.py makemigrations
echo.

echo Step 2: Running migrations...
python manage.py migrate
echo.

echo Step 3: Updating incident types...
python update_incident_types.py
echo.

echo ========================================
echo Migration Complete!
echo ========================================
echo.
echo Summary:
echo - 30 Prohibited Acts created
echo - 6 Other School Policies created
echo - Total: 36 incident types
echo.
pause
