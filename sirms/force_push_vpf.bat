@echo off
echo ========================================
echo FORCE PUSHING VPF (Working Version)
echo ========================================
echo.
echo This will revert to the working VPF version
echo and remove all VRF changes from GitHub.
echo.
pause
echo.
echo Pushing to GitHub...
git push --force origin main
echo.
echo ========================================
echo Done! Render will auto-deploy VPF version
echo ========================================
pause
