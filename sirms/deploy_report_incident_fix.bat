@echo off
echo 🔧 Deploying Report Incident JavaScript Fix...

echo 📝 Adding changes to git...
git add .

echo 💾 Committing changes...
git commit -m "🔧 Fix Report Incident JavaScript: Properly structure script tags

- Fixed JavaScript code that was outside of script tags
- Properly structured party type toggle functionality  
- Fixed double submission prevention code
- All JavaScript now properly enclosed in script blocks
- Report incident page now works without JavaScript errors"

echo 🚀 Pushing to repository...
git push origin main

echo ✅ Report Incident JavaScript fix deployed!
pause