@echo off
REM Deploy Status Sync Feature
REM This script deploys the automatic status synchronization feature

echo ========================================
echo  DEPLOY STATUS SYNC FEATURE
echo ========================================
echo.

REM Step 1: Run tests
echo [1/5] Running tests...
python test_status_sync.py
if errorlevel 1 (
    echo.
    echo ERROR: Tests failed! Please fix issues before deploying.
    pause
    exit /b 1
)
echo Tests passed!
echo.

REM Step 2: Check for uncommitted changes
echo [2/5] Checking git status...
git status
echo.

REM Step 3: Add files
echo [3/5] Adding files to git...
git add incidents/do_schedule_views.py
git add incidents/behavior_concerns_views.py
git add test_status_sync.py
git add AUTO_STATUS_SYNC_FEATURE.md
git add STATUS_SYNC_VISUAL_GUIDE.md
git add STATUS_SYNC_COMPLETE.md
git add STATUS_SYNC_INDEX.md
git add STATUS_SYNC_QUICK_REF.md
git add DEPLOY_STATUS_SYNC.md
git add deploy_status_sync.bat
echo Files added!
echo.

REM Step 4: Commit
echo [4/5] Committing changes...
git commit -m "Add automatic status sync between Behavioral Concerns and DO Schedule"
if errorlevel 1 (
    echo.
    echo Note: Nothing to commit or commit failed
    echo.
)
echo.

REM Step 5: Push
echo [5/5] Pushing to repository...
set /p confirm="Push to remote repository? (y/n): "
if /i "%confirm%"=="y" (
    git push origin main
    echo.
    echo ========================================
    echo  DEPLOYMENT COMPLETE!
    echo ========================================
    echo.
    echo The feature has been pushed to the repository.
    echo If using Render, it will auto-deploy.
    echo Monitor deployment at: https://dashboard.render.com
    echo.
) else (
    echo.
    echo Push cancelled. You can push manually later with:
    echo   git push origin main
    echo.
)

echo.
echo Next steps:
echo 1. Monitor deployment logs
echo 2. Test on production
echo 3. Notify users about the new feature
echo.

pause
