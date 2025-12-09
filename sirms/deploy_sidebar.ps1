# Sidebar Cleanup Deployment Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deploying Sidebar Cleanup Changes" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Adding changes to git..." -ForegroundColor Yellow
git add templates/base.html SIDEBAR_CLEANUP_DEC9.md deploy_sidebar_cleanup.bat deploy_sidebar.ps1

Write-Host ""
Write-Host "Committing changes..." -ForegroundColor Yellow
git commit -m "Remove sidebar items: Dashboard from ESP Teacher, Advisee Records and Legal References from Teacher, Legal References from Student"

Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Render will auto-deploy in 5-10 minutes." -ForegroundColor White
Write-Host "Check: https://dashboard.render.com" -ForegroundColor White
Write-Host ""
Write-Host "Changes made:" -ForegroundColor Cyan
Write-Host "  - Removed Dashboard from ESP Teacher sidebar" -ForegroundColor White
Write-Host "  - Removed Advisee Records from Teacher sidebar" -ForegroundColor White
Write-Host "  - Removed Legal References from Teacher sidebar" -ForegroundColor White
Write-Host "  - Removed Legal References from Student sidebar" -ForegroundColor White
Write-Host ""
