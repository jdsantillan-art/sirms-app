@echo off
echo ========================================
echo   SIRMS Testing Setup Verification
echo ========================================
echo.

echo [1/5] Checking virtual environment...
if exist ".venv\Scripts\activate.bat" (
    echo ✅ Virtual environment found
) else (
    echo ❌ Virtual environment NOT found
    echo    Run: python -m venv .venv
    goto :end
)

echo.
echo [2/5] Activating virtual environment...
call .venv\Scripts\activate.bat
echo ✅ Virtual environment activated

echo.
echo [3/5] Checking pytest installation...
pytest --version >nul 2>&1
if %errorlevel% equ 0 (
    pytest --version
    echo ✅ pytest is installed
) else (
    echo ❌ pytest NOT installed
    echo    Run: pip install -r requirements_test.txt
    goto :end
)

echo.
echo [4/5] Checking pytest-django installation...
python -c "import pytest_django" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ pytest-django is installed
) else (
    echo ❌ pytest-django NOT installed
    echo    Run: pip install -r requirements_test.txt
    goto :end
)

echo.
echo [5/5] Checking test files...
if exist "tests\test_models.py" (
    echo ✅ test_models.py found
) else (
    echo ❌ test_models.py NOT found
)

if exist "tests\test_views.py" (
    echo ✅ test_views.py found
) else (
    echo ❌ test_views.py NOT found
)

if exist "tests\test_forms.py" (
    echo ✅ test_forms.py found
) else (
    echo ❌ test_forms.py NOT found
)

if exist "pytest.ini" (
    echo ✅ pytest.ini found
) else (
    echo ❌ pytest.ini NOT found
)

echo.
echo ========================================
echo   Setup Verification Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Open VS Code Testing panel (click 🧪 icon)
echo   2. Click "Configure Python Tests"
echo   3. Select "pytest"
echo   4. Select "tests" directory
echo   5. Run your first test!
echo.
echo Or run tests in terminal:
echo   pytest tests/ -v
echo.

:end
pause
