@echo off
echo ========================================
echo SIRMS - Switch to PostgreSQL
echo ========================================
echo.

echo Setting environment variables...
set USE_POSTGRESQL=true
set DB_NAME=sirms_db
set DB_USER=postgres
set /p DB_PASSWORD="Enter PostgreSQL password: "
set DB_HOST=localhost
set DB_PORT=5432

echo.
echo Environment variables set!
echo.
echo Now run these commands:
echo   1. python manage.py migrate
echo   2. python manage.py loaddata backup_data.json
echo   3. python manage.py runserver
echo.
echo Press any key to start Django shell in PostgreSQL mode...
pause > nul

cmd /k
