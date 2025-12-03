@echo off
echo ============================================
echo DEPLOYING BEHAVIOR CONCERNS FEATURE
echo ============================================
echo.

echo [1/5] Checking Git status...
git status

echo.
echo [2/5] Adding changes to Git...
git add templates/do/behavior_concerns.html
git add incidents/export_views.py
git add incidents/urls.py
git add CLICKABLE_BEHAVIOR_CONCERNS_FEATURE.md
git add BEHAVIOR_CONCERNS_VISUAL_GUIDE.md
git add BEHAVIOR_CONCERNS_SUMMARY.md
git add BEHAVIOR_CONCERNS_QUICK_REF.md
git add DEPLOY_BEHAVIOR_CONCERNS_FEATURE.md
git add test_behavior_concerns_filtering.py

echo.
echo [3/5] Committing changes...
git commit -m "Add clickable counter cards and Excel export to Behavior Concerns - Clickable Total/Pending/Completed cards with filtering - Excel export for completed counseling sessions - Comprehensive data export with appointments and notes - Visual feedback and smooth transitions - Role-based access (DO only)"

echo.
echo [4/5] Pushing to repository...
git push origin main

echo.
echo [5/5] Deployment Status
echo ============================================
echo.
echo Changes pushed to repository!
echo.
echo If using Render or auto-deployment:
echo - Your service will auto-deploy in 1-2 minutes
echo - Monitor deployment at your hosting dashboard
echo.
echo If using manual deployment:
echo - SSH into your server
echo - Run: git pull origin main
echo - Restart your service
echo.
echo ============================================
echo DEPLOYMENT COMPLETE
echo ============================================
echo.
echo Next Steps:
echo 1. Monitor deployment logs
echo 2. Test the feature as DO user
echo 3. Verify filtering works correctly
echo 4. Test Excel export functionality
echo.
pause
