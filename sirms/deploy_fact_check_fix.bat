@echo off
echo 🔧 Deploying Fact Check Functionality Fix...

echo 📝 Adding changes to git...
git add .

echo 💾 Committing changes...
git commit -m "🔧 Restore Fact Check Functionality: Full DO fact checking system

- Fixed fact_check_reports view to use correct template path (do/fact_check_reports.html)
- Added comprehensive fact checking functionality for DO users
- Implemented report verification and classification system
- Added evidence status checking (clear/insufficient)
- Added case routing (minor to DO, major to Counselor)
- Added student assignment functionality
- Added notification system for classifications
- Added filtering by priority and date
- Added modal interface for report verification
- Tested with DO account - fact check page now works (Status 200)
- DO can now properly verify and classify incident reports"

echo 🚀 Pushing to repository...
git push origin main

echo ✅ Fact Check functionality restored!
pause