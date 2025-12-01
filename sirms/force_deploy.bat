@echo off
echo Forcing deployment...
git add .
git commit -m "Force redeploy" --allow-empty
git push origin main
echo Done!
pause
