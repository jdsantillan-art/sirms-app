@echo off
echo ========================================
echo SIRMS - Switch to SQLite
echo ========================================
echo.

echo Setting environment variables...
set USE_POSTGRESQL=false

echo.
echo Switched back to SQLite!
echo.
echo You can now run: python manage.py runserver
echo.
pause

cmd /k
