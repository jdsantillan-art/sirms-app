@echo off
echo 🚀 Deploying 500 Error Fix...

echo 📝 Adding changes to git...
git add .

echo 💾 Committing changes...
git commit -m "🔧 Fix 500 errors: Fixed syntax error in views.py and template issues

- Fixed broken comment causing syntax error in views.py line 335
- Fixed duplicate endblock tags in report_incident.html template  
- All views now working properly (dashboard, report_incident, analytics)
- Tested with guidance counselor account - all endpoints return 200 status"

echo 🚀 Pushing to repository...
git push origin main

echo ✅ Deployment complete! 500 errors should be resolved.
pause