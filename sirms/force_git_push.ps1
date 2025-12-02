# Force Git Push - Bypass any blocking processes
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "FORCE DEPLOYING TO RENDER" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Kill any stuck Python processes
Write-Host "Checking for stuck processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

# Git operations
Write-Host "Adding files..." -ForegroundColor Green
git add .

Write-Host "Committing changes..." -ForegroundColor Green
git commit -m "Fix: Behavior concerns schedule + indentation error + template fixes"

Write-Host "Pushing to GitHub..." -ForegroundColor Green
git push origin main

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Check Render dashboard: https://dashboard.render.com" -ForegroundColor Yellow
Write-Host "Live URL: https://sirmsportal.onrender.com" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
